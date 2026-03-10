"""Utility Functions for Flask-Jeroboam.

Credits: this is essentially a fork of FastAPI's own utils.py
Original Source Code at https://github.com/tiangolo/fastapi
"""

import inspect
import re
import typing
from collections.abc import Callable
from typing import Any


def _lenient_issubclass(cls: Any, class_or_tuple: Any) -> bool:
    """issubclass that returns False instead of raising TypeError."""
    try:
        return issubclass(cls, class_or_tuple)
    except TypeError:
        return False


def get_typed_signature(call: Callable[..., Any]) -> inspect.Signature:
    """Return a signature with string annotations resolved via get_type_hints."""
    signature = inspect.signature(call)
    globalns = getattr(call, "__globals__", {})
    try:
        hints = typing.get_type_hints(call, globalns=globalns, include_extras=True)
    except Exception:  # pragma: no cover
        hints = {}
    typed_params = [
        inspect.Parameter(
            name=param.name,
            kind=param.kind,
            default=param.default,
            annotation=hints.get(param.name, param.annotation),
        )
        for param in signature.parameters.values()
    ]
    return inspect.Signature(typed_params)


def get_typed_return_annotation(call: Callable[..., Any]) -> Any:  # pragma: no cover
    """Return a typed return annotation."""
    try:
        hints = typing.get_type_hints(call, include_extras=True)
    except Exception:
        return None
    return hints.get("return", None)


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


def is_sequence_field(field) -> bool:
    """Check if a field is a sequence field."""
    from typing import get_origin

    annotation = getattr(field, "annotation", None)
    if annotation is None:
        return False
    return get_origin(annotation) in (list, tuple, set, frozenset)


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


def _throw_away_falthy_values(
    sparse_dict: dict[str, Any], keep: set | None = None
) -> dict[str, Any]:
    keep = keep or set()
    return {key: value for key, value in sparse_dict.items() if value or key in keep}


def _memoized_update_if_value(key: str, new_value: Any, orginal: dict[str, Any]):
    if new_value:
        orginal.setdefault(key, {}).update(new_value)


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
