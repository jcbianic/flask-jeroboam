"""Solved Specialized Params.

Params are solved at registration time. This way we reduce indirections when
handling requests thus reducing overhead.
"""

import re
from copy import deepcopy
from typing import Any

from flask import request

from flask_jeroboam._compat import BaseConfig, ErrorWrapper, ModelField, V1FieldInfo as FieldInfo
from pydantic.v1 import ValidationError as _V1ValidationError, create_model as _v1_create_model
from werkzeug.datastructures import FileStorage, Headers, MultiDict

from flask_jeroboam._utils import is_sequence_field
from flask_jeroboam.view_arguments._utils import (
    _extract_scalar,
    _extract_sequence,
    _extract_subfields,
)
from flask_jeroboam.view_arguments.arguments import ArgumentLocation, ViewArgument

empty_field_info = FieldInfo()

_DUMMY_V1_MODEL = _v1_create_model("_JeroboamRequest")


def _error_wrapper_to_dicts(ew: ErrorWrapper) -> list[dict]:
    """Convert a pydantic.v1 ErrorWrapper to a list of plain error dicts.

    Uses pydantic.v1.ValidationError as the canonical converter so the output
    format (including ctx for constrained fields) is guaranteed to match what
    pydantic.v1 would produce. Returns a list because a single ErrorWrapper
    wrapping a nested ValidationError may expand to multiple field errors.
    """
    return _V1ValidationError([ew], _DUMMY_V1_MODEL).errors()


class SolvedArgument(ModelField):
    """Generic Solved Parameter."""

    def __init__(
        self,
        *,
        name: str,
        type_: type,
        required: bool = False,
        view_param: ViewArgument | None = None,
        class_validators: dict | None = None,
        model_config: type[BaseConfig] = BaseConfig,
        field_info: FieldInfo = empty_field_info,
        **kwargs,
    ):
        self.name = name
        self.location: ArgumentLocation = getattr(
            view_param, "location", ArgumentLocation.unknown
        )
        if self.location == ArgumentLocation.file:
            model_config.arbitrary_types_allowed = True
        self.required = required
        self.embed = getattr(view_param, "embed", None)
        self.in_body = getattr(view_param, "in_body", None)
        default = getattr(view_param, "default", field_info.default)
        if default is Ellipsis:
            default = None
        class_validators = class_validators or {}
        kwargs["alias"] = kwargs.get("alias", getattr(view_param, "alias", None))
        self.include_in_schema = getattr(view_param, "include_in_schema", True)
        super().__init__(
            name=name,
            type_=type_,
            class_validators={},
            default=default,
            required=required,
            model_config=model_config,
            field_info=view_param,
            **kwargs,
        )

    @classmethod
    def specialize(
        cls,
        *,
        name: str,
        type_: type,
        required: bool = False,
        view_param: ViewArgument | None = None,
        class_validators: dict | None = None,
        model_config: type[BaseConfig] = BaseConfig,
        field_info: FieldInfo = empty_field_info,
        **kwargs,
    ):
        """Specialize the Current class to each location."""
        location = getattr(view_param, "location", ArgumentLocation.unknown)
        target_class = {
            ArgumentLocation.query: SolvedQueryArgument,
            ArgumentLocation.header: SolvedHeaderArgument,
            ArgumentLocation.path: SolvedPathArgument,
            ArgumentLocation.cookie: SolvedCookieArgument,
            ArgumentLocation.body: SolvedBodyArgument,
            ArgumentLocation.file: SolvedFileArgument,
            ArgumentLocation.form: SolvedFormArgument,
        }.get(location, cls)

        return target_class(
            name=name,
            type_=type_,
            required=required,
            view_param=view_param,
            class_validators=class_validators,
            model_config=model_config,
            field_info=field_info,
            **kwargs,
        )

    def validate_request(self) -> tuple[dict, list[dict]]:
        """Validate the request."""
        values: dict = {}
        errors: list[dict] = []
        assert self.location is not None  # noqa: S101
        inbound_values = self._get_values()
        if inbound_values is None and self.required:
            errors.append({
                "loc": [self.location.value, self.alias],
                "msg": "field required",
                "type": "value_error.missing",
            })
            return values, errors
        elif inbound_values is None:
            inbound_values = deepcopy(self.default)
        if _is_v2_only_model(self.type_):
            # Pydantic v2 BaseModel: use model_validate directly
            from pydantic import ValidationError as V2ValidationError

            try:
                values[self.name] = self.type_.model_validate(inbound_values)
            except V2ValidationError as e:
                for err in e.errors(include_url=False):
                    loc = [self.location.value, self.alias] + [
                        str(l) for l in err.get("loc", ())
                    ]
                    errors.append({"loc": loc, "msg": err["msg"], "type": err["type"]})
            except Exception as e:
                errors.append({"loc": [self.location.value, self.alias], "msg": str(e), "type": "value_error"})
            return values, errors
        values_, errors_ = self.validate(
            inbound_values, values, loc=(self.location.value, self.alias)
        )
        if isinstance(errors_, ErrorWrapper):
            errors.extend(_error_wrapper_to_dicts(errors_))
        else:
            values[self.name] = values_
        return values, errors

    def _get_values(
        self,
    ) -> FileStorage | MultiDict | dict | str | None | list[Any]:
        """The Value extraction method is specialized by location."""
        raise NotImplementedError


class SolvedPathArgument(SolvedArgument):
    """Solved Path parameter."""

    def _get_values(self) -> dict | str | None | list[Any]:
        source: dict = request.view_args or {}
        return _extract_scalar(source=source, alias=self.alias, name=self.name)


class SolvedHeaderArgument(SolvedArgument):
    """Solved Header parameter."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.alias = re.sub(
            r"_(\w)", lambda x: f"-{x.group(1).upper()}", self.name.capitalize()
        )

    def _get_values(self) -> dict | str | None | list[Any]:
        source: Headers | dict = request.headers or {}
        return _extract_scalar(source=source, alias=self.alias, name=self.name)


class SolvedCookieArgument(SolvedArgument):
    """Solved Cookie parameter."""

    def _get_values(self) -> dict | str | None | list[Any]:
        source: dict = request.cookies or {}
        return _extract_scalar(source=source, alias=self.alias, name=self.name)


class SolvedQueryArgument(SolvedArgument):
    """Solved Query parameter."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if hasattr(self.type_, "model_fields") or hasattr(self.type_, "__fields__"):
            self.extractor = _extract_subfields
        elif is_sequence_field(self):
            self.extractor = _extract_sequence
        else:
            self.extractor = _extract_scalar

    def _get_values(self) -> dict | str | None | list[Any]:
        source: MultiDict = request.args
        fields = getattr(self.type_, "model_fields", None) or getattr(
            self.type_, "__fields__", {}
        )
        return self.extractor(
            source=source,
            alias=self.alias,
            name=self.name,
            fields=fields,
        )


def _is_v2_only_model(type_: Any) -> bool:
    """Check if type_ is a pydantic v2 BaseModel that lacks __get_validators__."""
    from pydantic import BaseModel as V2BaseModel
    from pydantic.v1 import BaseModel as V1BaseModel

    return (
        isinstance(type_, type)
        and issubclass(type_, V2BaseModel)
        and not issubclass(type_, V1BaseModel)
        and not hasattr(type_, "__get_validators__")
    )


class SolvedBodyArgument(SolvedArgument):
    """Solved Body parameter."""

    def _get_values(self) -> dict | str | None | list[Any]:
        source: dict | list = request.json or {}
        if isinstance(source, list):
            return source
        return source.get(self.alias or self.name) if self.embed else source



class SolvedFileArgument(SolvedArgument):
    """Solved File Parameter."""

    def _get_values(
        self,
    ) -> FileStorage | MultiDict | dict | str | None | list[Any]:
        source: MultiDict = request.files or MultiDict()
        return source.get(self.alias or self.name) if self.embed else source


class SolvedFormArgument(SolvedArgument):
    """Solved Form parameter."""

    def _get_values(self) -> dict | str | None | list[Any]:
        source: MultiDict = request.form or MultiDict()
        return source.get(self.alias or self.name) if self.embed else source
