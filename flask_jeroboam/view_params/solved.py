"""View params for solved problems."""
import re
from copy import deepcopy
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Type
from typing import Union

from flask import current_app
from flask import request
from pydantic import BaseConfig
from pydantic.error_wrappers import ErrorWrapper
from pydantic.errors import MissingError
from pydantic.fields import FieldInfo
from pydantic.fields import ModelField
from werkzeug.datastructures import MultiDict

from flask_jeroboam.utils import is_sequence_field

from .parameters import ParamLocation
from .parameters import ViewParameter


empty_field_info = FieldInfo()


class SolvedParameter(ModelField):
    """A Parameter that have been solved, ready to validate data."""

    def __init__(
        self,
        *,
        name: str,
        type_: type,
        required: bool = False,
        view_param: Optional[ViewParameter] = None,
        class_validators: Optional[Dict] = None,
        model_config: Type[BaseConfig] = BaseConfig,
        field_info: FieldInfo = empty_field_info,
        **kwargs,
    ):
        self.name = name
        self.location: Optional[ParamLocation] = getattr(view_param, "location", None)
        if self.location == ParamLocation.file:
            model_config.arbitrary_types_allowed = True
        self.required = required
        self.embed = getattr(view_param, "embed", None)
        self.in_body = getattr(view_param, "in_body", None)
        default = getattr(view_param, "default", field_info.default)
        class_validators = class_validators or {}
        if getattr(view_param, "convert_underscores", False):
            self.alias = re.sub(
                r"_(\w)", lambda x: f"-{x.group(1).upper()}", self.name.capitalize()
            )
            kwargs["alias"] = self.alias
        else:
            kwargs["alias"] = kwargs.get("alias", getattr(view_param, "alias", None))
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

    def validate_request(self):
        """Validate the request."""
        values = {}
        errors = []
        assert self.location is not None  # noqa: S101
        inbound_values = self._get_values()
        if inbound_values is None and self.required:
            errors.append(
                ErrorWrapper(MissingError(), loc=(self.location.value, self.alias))
            )
            return values, errors
            # Should I return errors here ?
        elif inbound_values is None and not self.required:
            inbound_values = deepcopy(self.default)
        values_, errors_ = self.validate(
            inbound_values, values, loc=(self.location.value, self.alias)
        )
        if isinstance(errors_, ErrorWrapper):
            errors.append(errors_)
        else:
            values[self.name] = values_
        return values, errors

    def _get_values(self) -> Union[dict, Optional[str], List[Any]]:
        """Get the values from the request."""
        if self.in_body:
            return self._get_values_from_body()
        elif self.location == ParamLocation.query:
            source = request.args
        elif self.location == ParamLocation.path:
            source = MultiDict(request.view_args)
        elif self.location == ParamLocation.header:
            source = MultiDict(request.headers)
        elif self.location == ParamLocation.cookie:
            source = request.cookies
        else:
            raise ValueError("Unknown location")
        has_key_transformer = (
            getattr(current_app, "query_string_key_transformer", False) is not None
        )
        return self._get_values_from_request(
            self, source, self.name, self.alias, has_key_transformer
        )

    def _get_values_from_body(self) -> Any:
        """Get the values from the request body."""
        source: Any = {}
        if self.location == ParamLocation.form:
            source = request.form
        elif self.location == ParamLocation.file:
            source = request.files
        else:
            source = request.json or {}
        return source.get(self.alias or self.name) if self.embed else source

    def _get_values_from_request(
        self,
        field: ModelField,
        source: MultiDict,
        name: str,
        alias: str,
        has_key_transformer: bool = False,
    ) -> Union[dict, Optional[str], List[Any]]:
        """Get the values from the request.

        # TODO: Gestion des alias de fields.
        # TODO: Gestion des default empty et des valeurs manquantes.
        # Est-ce qu'on gère le embed dans les QueryParams ?
        """
        values: Union[dict, Optional[str], List[Any]] = {}
        if hasattr(field.type_, "__fields__"):
            assert isinstance(values, dict)  # noqa: S101
            for field_name, subfield in field.type_.__fields__.items():
                values[field_name] = self._get_values_from_request(
                    subfield, source, field_name, subfield.alias, has_key_transformer
                )
        elif is_sequence_field(field):
            values = _extract_sequence(source, alias, name)
            if len(values) == 0 and has_key_transformer:
                values = _extract_sequence_with_key_transformer(source, alias, name)
        else:
            values = _extract_scalar(source, alias, name)
        return values


def _extract_scalar(source: MultiDict, name: Optional[str], alias: Optional[str]):
    """Extract a scalar value from a source."""
    return source.get(alias, source.get(name))


def _extract_sequence(
    source: MultiDict, name: Optional[str], alias: Optional[str]
) -> List:
    """Extract a Sequence value from a source."""
    _values = source.getlist(alias)
    if len(_values) == 0:
        _values = source.getlist(name)
    return _values


def _extract_sequence_with_key_transformer(
    source: MultiDict, name: Optional[str], alias: Optional[str]
):
    """Apply the key transformer to the source."""
    transformed_source = current_app.query_string_key_transformer(  # type: ignore
        current_app, source.to_dict()
    )
    return _extract_scalar(transformed_source, name, alias)
