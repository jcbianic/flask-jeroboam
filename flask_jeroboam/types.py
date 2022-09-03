from typing import Any
from typing import Callable
from typing import TypeVar


DecoratedCallable = TypeVar("DecoratedCallable", bound=Callable[..., Any])
