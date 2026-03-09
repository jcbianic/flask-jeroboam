"""Utility Functions for Flask-Jeroboam.

Credits: this is essentially a fork of FastAPI's own utils.py
Original Source Code at https://github.com/tiangolo/fastapi
"""

import inspect
import re
from collections.abc import Callable
from typing import Any, ForwardRef

from pydantic import BaseModel
from pydantic.fields import FieldInfo

from flask_jeroboam._compat import (
    SHAPE_FROZENSET,
    SHAPE_LIST,
    SHAPE_SEQUENCE,
    SHAPE_SET,
    SHAPE_TUPLE,
    SHAPE_TUPLE_ELLIPSIS,
    BaseConfig,
    ModelField,
)

from flask_jeroboam.view_arguments.arguments import ArgumentLocation, ViewArgument

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


def _evaluate_forwardref(ref: ForwardRef, globalns: dict, localns: dict) -> Any:
    """Evaluate a ForwardRef in the given namespaces (Python version-safe).

    Python 3.12 added type_params; 3.9+ made recursive_guard keyword-only.
    """
    try:
        # Python 3.12+: type_params required
        return ref._evaluate(globalns, localns, type_params=frozenset(), recursive_guard=frozenset())
    except TypeError:
        # Python 3.9–3.11: recursive_guard keyword-only, no type_params
        return ref._evaluate(globalns, localns, recursive_guard=frozenset())  # type: ignore[call-arg]


def _lenient_issubclass(cls: Any, class_or_tuple: Any) -> bool:
    """issubclass that returns False instead of raising TypeError."""
    try:
        return issubclass(cls, class_or_tuple)
    except TypeError:
        return False


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


def get_typed_annotation(annotation: Any, globalns: dict[str, Any]) -> Any:
    """Return a typed annotation."""
    if isinstance(annotation, str):
        annotation = ForwardRef(annotation)
        annotation = _evaluate_forwardref(annotation, globalns, globalns)
    return annotation


def get_typed_return_annotation(call: Callable[..., Any]) -> Any:  # pragma: no cover
    """Return a typed return annotation."""
    signature = inspect.signature(call)
    annotation = signature.return_annotation

    if annotation is inspect.Signature.empty:
        return None

    globalns = getattr(call, "__globals__", {})
    return get_typed_annotation(annotation, globalns)


def is_sequence_field(field) -> bool:
    """Check if a field is a sequence field."""
    # Handle pydantic v2 FieldInfo (no shape/type_ attributes)
    if not hasattr(field, "shape"):
        from typing import get_origin

        annotation = getattr(field, "annotation", None)
        if annotation is None:
            return False
        return get_origin(annotation) in (list, tuple, set, frozenset)
    # Pydantic v1 ModelField path (removed in Phase 6)
    if (field.shape in sequence_shapes) and not _lenient_issubclass(
        field.type_, BaseModel
    ):
        return True
    return bool(_lenient_issubclass(field.type_, sequence_types))


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
    type_: type[BaseModel],
    required: bool,
    alias: str | None = None,
    field_info: FieldInfo | None = None,
    class_validators: dict,
    model_config: type[BaseConfig] | None = None,
) -> ModelField | None:
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
    sparse_dict: dict[str, Any], keep: set | None = None
) -> dict[str, Any]:
    keep = keep or set()
    return {key: value for key, value in sparse_dict.items() if value or key in keep}


def _memoized_update_if_value(key: str, new_value: Any, orginal: dict[str, Any]):
    if new_value:
        orginal.setdefault(key, {}).update(new_value)


def _append_truthy(array: list, value: Any) -> None:
    """Append a value to an array if it's truthy.

    Mutates the orginal array.
    """
    if value:
        array.append(value)


def _set_nested_defaults(
    original_dict: dict, keys: list[str], last_key: str, new_value: Any
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
