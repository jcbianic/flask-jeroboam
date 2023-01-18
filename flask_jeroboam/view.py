"""The Route Class."""
from typing import Any
from typing import Dict
from typing import TypeVar

from typing_extensions import ParamSpec

from ._parser import Parser
from ._serializer import Serializer
from .typing import JeroboamRouteCallable


P = ParamSpec("P")
R = TypeVar("R")

METHODS_DEFAULT_CODE = {
    "GET": 200,
    "POST": 201,
    "PUT": 200,
    "PATCH": 200,
    "DELETE": 204,
    "HEAD": 200,
    "OPTIONS": 200,
}


class JeroboamViewFunction:
    """A View Class for Flask-Jeroboam."""

    def __init__(self, rule: str, func: JeroboamRouteCallable, options: Dict[str, Any]):
        """Initialize the Route Class."""
        self.endpoint = options.pop("endpoint", None)
        self.serializer = Serializer(func, options)
        self.methods = options.get("methods", ["GET"])
        self.parser = Parser(func, self.methods, rule)
        self.status_code = options.pop("status_code", 200)
        self.func = func

    @property
    def as_view(self) -> JeroboamRouteCallable:
        """Return a view funcion."""
        func = self.func
        # TODO: Manip sur le nom, etc...
        if self.parser:
            func = self.parser(func)
        if self.serializer:
            func = self.serializer(func, self.status_code)
        return func
