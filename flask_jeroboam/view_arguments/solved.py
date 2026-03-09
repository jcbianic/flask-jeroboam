"""Solved Specialised Params.

Params are solved at registration time. This way we reduce indirections when
handling requests thus reducing overhead.
"""

import re
from copy import deepcopy
from typing import Annotated, Any

from flask import request
from pydantic import TypeAdapter, ValidationError
from pydantic_core import PydanticUndefined
from werkzeug.datastructures import FileStorage, Headers, MultiDict

from flask_jeroboam.view_arguments._utils import (
    _extract_scalar,
    _extract_sequence,
    _extract_subfields,
)
from flask_jeroboam.view_arguments.arguments import ArgumentLocation, ViewArgument


class SolvedArgument:
    """Generic Solved Parameter.

    Created at route-registration time; reused on every request.
    Validates inbound data using a pydantic v2 TypeAdapter.
    """

    def __init__(
        self,
        *,
        name: str,
        annotation: type,
        required: bool = False,
        default: Any = PydanticUndefined,
        location: ArgumentLocation = ArgumentLocation.unknown,
        alias: str | None = None,
        embed: bool = False,
        include_in_schema: bool = True,
        field_info: ViewArgument | None = None,
    ):
        self.name = name
        self.annotation = annotation
        # Keep type_ as alias for OpenAPI compatibility until Phase 8
        self.type_ = annotation
        self.required = required
        self.default = default
        self.location = location
        self.alias = alias or name
        self.embed = embed
        self.include_in_schema = include_in_schema
        self.field_info = field_info  # the original ViewArgument

        # Build TypeAdapter once at registration time.
        # Wrap in Annotated so FieldInfo constraints (gt, lt, …) are applied.
        if field_info is not None:
            adapter_type: Any = Annotated[annotation, field_info]
        else:
            adapter_type = annotation
        self._type_adapter: TypeAdapter = TypeAdapter(adapter_type)

    @classmethod
    def specialize(
        cls,
        *,
        name: str,
        annotation: type,
        required: bool = False,
        view_param: ViewArgument | None = None,
        **_kwargs,
    ) -> "SolvedArgument":
        """Dispatch to the location-specific subclass."""
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

        default = getattr(view_param, "default", PydanticUndefined)
        if default is Ellipsis:
            default = PydanticUndefined

        return target_class(
            name=name,
            annotation=annotation,
            required=required,
            default=default,
            location=location,
            alias=getattr(view_param, "alias", None),
            embed=getattr(view_param, "embed", False),
            include_in_schema=getattr(view_param, "include_in_schema", True),
            field_info=view_param,
        )

    def validate_request(self) -> tuple[dict, list[dict]]:
        """Extract and validate the parameter from the current request."""
        values: dict = {}
        errors: list[dict] = []

        inbound_values = self._get_values()

        if inbound_values is None and self.required:
            errors.append(
                {
                    "loc": [self.location.value, self.alias],
                    "msg": "Field required",
                    "type": "missing",
                }
            )
            return values, errors

        if inbound_values is None:
            if self.default is not PydanticUndefined:
                values[self.name] = deepcopy(self.default)
            return values, errors

        try:
            values[self.name] = self._type_adapter.validate_python(inbound_values)
        except ValidationError as exc:
            for err in exc.errors(include_url=False):
                loc = [self.location.value, self.alias] + [
                    str(segment) for segment in err.get("loc", ())
                ]
                error_dict: dict = {
                    "loc": loc,
                    "msg": err["msg"],
                    "type": err["type"],
                }
                if "ctx" in err:
                    error_dict["ctx"] = {
                        k: str(v) if isinstance(v, Exception) else v
                        for k, v in err["ctx"].items()
                    }
                errors.append(error_dict)

        return values, errors

    def _get_values(
        self,
    ) -> FileStorage | MultiDict | dict | str | None | list[Any]:
        """The Value extraction method is specialised by location."""
        raise NotImplementedError


class SolvedPathArgument(SolvedArgument):
    """Solved Path parameter."""

    def _get_values(self) -> dict | str | None | list[Any]:
        source: dict = request.view_args or {}
        return _extract_scalar(source=source, alias=self.alias, name=self.name)


class SolvedHeaderArgument(SolvedArgument):
    """Solved Header parameter."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Compute the HTTP header name from the Python field name.
        # e.g. content_type → Content-Type
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


def _unwrap_optional(annotation: Any) -> Any:
    """Return the inner type if annotation is Optional[X], else return it unchanged.

    Handles both typing.Optional[X] (Union) and the X | None syntax (types.UnionType
    in Python 3.10+).
    """
    import types as _types
    from typing import Union, get_args, get_origin

    origin = get_origin(annotation)
    is_union = origin is Union
    if not is_union and hasattr(_types, "UnionType"):
        is_union = isinstance(annotation, _types.UnionType)

    if is_union:
        non_none = [a for a in get_args(annotation) if a is not type(None)]
        if len(non_none) == 1:
            return non_none[0]
    return annotation


class SolvedQueryArgument(SolvedArgument):
    """Solved Query parameter."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from typing import get_origin

        # Unwrap Optional[X] to find the inner type for extractor selection.
        inner = _unwrap_optional(self.annotation)
        if hasattr(inner, "model_fields") or hasattr(inner, "__fields__"):
            self.extractor = _extract_subfields
        elif get_origin(self.annotation) in (list, tuple, set, frozenset):
            self.extractor = _extract_sequence
        else:
            self.extractor = _extract_scalar

    def _get_values(self) -> dict | str | None | list[Any]:
        source: MultiDict = request.args
        inner = _unwrap_optional(self.annotation)
        fields = getattr(inner, "model_fields", None) or getattr(inner, "__fields__", {})
        return self.extractor(
            source=source,
            alias=self.alias,
            name=self.name,
            fields=fields,
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
