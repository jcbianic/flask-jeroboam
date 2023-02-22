"""Utility Functions for Flask-Jeroboam.

Credits: this is essentially a fork of FastAPI's own utils.py
Original Source Code at https://github.com/tiangolo/fastapi
"""
import dataclasses
import inspect
import re
from typing import Any
from typing import Callable
from typing import Dict
from typing import ForwardRef
from typing import List
from typing import Optional
from typing import Type

from pydantic import BaseConfig
from pydantic import BaseModel
from pydantic.fields import SHAPE_FROZENSET
from pydantic.fields import SHAPE_LIST
from pydantic.fields import SHAPE_SEQUENCE
from pydantic.fields import SHAPE_SET
from pydantic.fields import SHAPE_SINGLETON
from pydantic.fields import SHAPE_TUPLE
from pydantic.fields import SHAPE_TUPLE_ELLIPSIS
from pydantic.fields import FieldInfo
from pydantic.fields import ModelField
from pydantic.typing import evaluate_forwardref
from pydantic.utils import lenient_issubclass

from flask_jeroboam.view_arguments.arguments import ArgumentLocation
from flask_jeroboam.view_arguments.arguments import ViewArgument


sequence_shapes = {
    SHAPE_LIST,
    SHAPE_SET,
    SHAPE_FROZENSET,
    SHAPE_TUPLE,
    SHAPE_SEQUENCE,
    SHAPE_TUPLE_ELLIPSIS,
}
sequence_types = (list, set, tuple)
body_locations = {ArgumentLocation.body, ArgumentLocation.form, ArgumentLocation.file}


def get_typed_signature(call: Callable[..., Any]) -> inspect.Signature:
    """Return a signature with the annotations evaluated."""
    signature = inspect.signature(call)
    globalns = getattr(call, "__globals__", {})
    typed_params = [
        inspect.Parameter(
            name=param.name,
            kind=param.kind,
            default=param.default,
            annotation=get_typed_annotation(param.annotation, globalns),
        )
        for param in signature.parameters.values()
    ]
    return inspect.Signature(typed_params)


def get_typed_annotation(annotation: Any, globalns: Dict[str, Any]) -> Any:
    """Return a typed annotation."""
    if isinstance(annotation, str):
        annotation = ForwardRef(annotation)
        annotation = evaluate_forwardref(annotation, globalns, globalns)
    return annotation


def get_typed_return_annotation(call: Callable[..., Any]) -> Any:  # pragma: no cover
    """Return a typed return annotation."""
    signature = inspect.signature(call)
    annotation = signature.return_annotation

    if annotation is inspect.Signature.empty:
        return None

    globalns = getattr(call, "__globals__", {})
    return get_typed_annotation(annotation, globalns)


def is_scalar_field(field: ModelField) -> bool:
    """Check if a field is a scalar field."""
    return (
        False
        if field.shape != SHAPE_SINGLETON
        or lenient_issubclass(field.type_, BaseModel)
        or lenient_issubclass(field.type_, sequence_types + (dict,))
        or dataclasses.is_dataclass(field.type_)
        or isinstance(field.field_info, ViewArgument)
        or getattr(field.field_info, "location", None) in body_locations
        else not field.sub_fields  # pragma: no cover
        or all(is_scalar_field(f) for f in field.sub_fields)
    )


def is_sequence_field(field: ModelField) -> bool:
    """Check if a field is a sequence field."""
    if (field.shape in sequence_shapes) and not lenient_issubclass(
        field.type_, BaseModel
    ):
        return True
    return bool(lenient_issubclass(field.type_, sequence_types))


def _rename_query_params_keys(self, inbound_dict: dict, pattern: str) -> dict:
    """Rename keys in a dictionary."""
    frozen_inbound_dict = inbound_dict.copy()
    for old_key, value in frozen_inbound_dict.items():
        match = re.match(pattern, old_key)
        if match is not None:
            new_key = f"{match[1]}[]"
            new_value = {match[2]: value}
            new_array = inbound_dict.get(new_key, [])
            new_array.append(new_value)
            inbound_dict[new_key] = new_array
            del inbound_dict[old_key]
    return inbound_dict


def create_field(
    *,
    name: str,
    type_: Type[BaseModel],
    required: bool,
    alias: Optional[str] = None,
    field_info: Optional[FieldInfo] = None,
    class_validators: dict,
    model_config: Optional[Type[BaseConfig]] = None,
) -> Optional[ModelField]:
    """Create a pydantic ModelField from a model class.

    Removed the partial-trcatch trick from FastAPI's original implementation.
    I didn't find a way to reproduce.
    """
    class_validators = class_validators or {}
    field_info = field_info or FieldInfo()
    model_config = model_config or getattr(type_, "__config__", BaseConfig)

    return ModelField(
        name=name,
        type_=type_,
        class_validators=class_validators,
        default=None,
        model_config=model_config,  # type: ignore
        alias=alias or name,
        required=required,
        field_info=field_info,
    )


def _throw_away_falthy_values(
    sparse_dict: Dict[str, Any], keep: Optional[set] = None
) -> Dict[str, Any]:
    keep = keep or set()
    return {key: value for key, value in sparse_dict.items() if value or key in keep}


def _memoized_update_if_value(key: str, new_value: Any, orginal: Dict[str, Any]):
    if new_value:
        orginal.setdefault(key, {}).update(new_value)


def _append_truthy(array: list, value: Any) -> None:
    """Append a value to an array if it's truthy.

    Mutates the orginal array.
    """
    if value:
        array.append(value)


def _set_nested_defaults(
    original_dict: dict, keys: List[str], last_key: str, new_value: Any
) -> None:
    """Create a nested dictionary from a list of keys.

    _set_nested_defaults(
        original_dict=operation,
        keys=["responses", status_code, "content", route_response_media_type],
        last_key="schema",
        new_value={"$ref": "#/components/schemas/ResponseModel"},
    )
    is equivalent to:
    (operation.setdefault("responses", {})
     .setdefault(status_code, {})
     .setdefault("content", {})
     .setdefault(route_response_media_type, {})
    )["schema"] = {"$ref": "#/components/schemas/ResponseModel"}
    """
    for key in keys:
        original_dict.setdefault(key, {})
        original_dict = original_dict[key]
    original_dict[last_key] = new_value
