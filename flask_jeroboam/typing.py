"""Types used in the package."""
from typing import TYPE_CHECKING
from typing import Any
from typing import Awaitable
from typing import Callable
from typing import Dict
from typing import Iterator
from typing import List
from typing import Mapping
from typing import Optional
from typing import Protocol
from typing import Tuple
from typing import Type
from typing import TypeVar
from typing import Union

from flask.typing import HeadersValue
from pydantic import BaseModel


if TYPE_CHECKING:  # pragma: no cover
    from _typeshed.wsgi import WSGIApplication  # noqa: F401
    from werkzeug.datastructures import Headers  # noqa: F401
    from werkzeug.wrappers import Response


class DataclassProtocol(Protocol):
    """A Protiocol to type annotate dataclasses."""

    __dataclass_fields__: Dict
    __dataclass_params__: Dict
    __post_init__: Optional[Callable]


ResponseModel = Type[BaseModel]
TypedParams = Dict[str, Any]


DataClassType = TypeVar("DataClassType", bound=DataclassProtocol)


JeroboamBodyType = Union[
    "Response",
    DataClassType,
    BaseModel,
    str,
    bytes,
    List[Any],
    List[BaseModel],
    # Only dict is actually accepted, but Mapping allows for TypedDic
    Mapping[str, Any],
    Iterator[str],
    Iterator[bytes],
    DataclassProtocol,
]

JeroboamResponseWithStatusCode = Union[
    Tuple[JeroboamBodyType, int], Tuple[JeroboamBodyType, int, HeadersValue]
]

JeroboamResponseReturnValue = Union[
    JeroboamBodyType,
    Tuple[JeroboamBodyType, HeadersValue],
    Tuple[JeroboamBodyType, int],
    Tuple[JeroboamBodyType, int, HeadersValue],
    "WSGIApplication",
]

JeroboamReturnValue = Union[
    JeroboamResponseReturnValue, Awaitable[JeroboamResponseReturnValue]
]

JeroboamRouteCallable = Union[
    Callable[..., JeroboamResponseReturnValue],
    Callable[..., Awaitable[JeroboamResponseReturnValue]],
]
