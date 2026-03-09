"""Types used in the package."""

from collections.abc import Awaitable, Callable, Iterator, Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    Protocol,
    TypeVar,
    Union,
)

from flask.typing import HeadersValue
from pydantic import BaseModel

if TYPE_CHECKING:  # pragma: no cover
    from _typeshed.wsgi import WSGIApplication  # noqa: F401
    from werkzeug.datastructures import Headers  # noqa: F401
    from werkzeug.wrappers import Response


class DataclassProtocol(Protocol):
    """A Protiocol to type annotate dataclasses."""

    __dataclass_fields__: dict
    __dataclass_params__: dict
    __post_init__: Callable | None


ResponseModel = type[BaseModel]
TypedParams = dict[str, Any]


DataClassType = TypeVar("DataClassType", bound=DataclassProtocol)


JeroboamBodyType = Union[
    "Response",
    DataClassType,
    BaseModel,
    str,
    bytes,
    list[Any],
    list[BaseModel],
    # Only dict is actually accepted, but Mapping allows for TypedDic
    Mapping[str, Any],
    Iterator[str],
    Iterator[bytes],
    DataclassProtocol,
]

JeroboamResponseWithStatusCode = (
    tuple[JeroboamBodyType, int] | tuple[JeroboamBodyType, int, HeadersValue]
)

JeroboamResponseReturnValue = Union[
    JeroboamBodyType,
    tuple[JeroboamBodyType, HeadersValue],
    tuple[JeroboamBodyType, int],
    tuple[JeroboamBodyType, int, HeadersValue],
    "WSGIApplication",
]

JeroboamReturnValue = (
    JeroboamResponseReturnValue | Awaitable[JeroboamResponseReturnValue]
)

JeroboamRouteCallable = (
    Callable[..., JeroboamResponseReturnValue]
    | Callable[..., Awaitable[JeroboamResponseReturnValue]]
)
