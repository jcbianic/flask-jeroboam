"""Types used in the package."""
from typing import TYPE_CHECKING
from typing import Any
from typing import Awaitable
from typing import Callable
from typing import Dict
from typing import Iterator
from typing import List
from typing import Mapping
from typing import Tuple
from typing import Type
from typing import Union

from flask.typing import HeadersValue
from pydantic import BaseModel


if TYPE_CHECKING:  # pragma: no cover
    from _typeshed.wsgi import WSGIApplication  # noqa: F401
    from werkzeug.datastructures import Headers  # noqa: F401
    from werkzeug.wrappers import Response


ResponseModel = Type[BaseModel]
TypedParams = Dict[str, Any]

JeroboamResponseValue = Union[
    "Response",
    BaseModel,
    str,
    bytes,
    List[Any],
    # Only dict is actually accepted, but Mapping allows for TypedDic
    Mapping[str, Any],
    Iterator[str],
    Iterator[bytes],
]

JeroboamResponseReturnValue = Union[
    JeroboamResponseValue,
    Tuple[JeroboamResponseValue, HeadersValue],
    Tuple[JeroboamResponseValue, int],
    Tuple[JeroboamResponseValue, int, HeadersValue],
    "WSGIApplication",
]

JeroboamReturnValue = Union[
    JeroboamResponseReturnValue, Awaitable[JeroboamResponseReturnValue]
]

JeroboamRouteCallable = Union[
    Callable[..., JeroboamResponseReturnValue],
    Callable[..., Awaitable[JeroboamResponseReturnValue]],
]
