"""The Route Class."""
from typing import Any
from typing import Dict
from typing import TypeVar

from typing_extensions import ParamSpec

from ._inboundhandler import InboundHandler
from ._outboundhandler import OutboundHandler
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


class JeroboamView:
    """Adds flask-jeroboam features to a regular flask view function.

    The InboundHandler and OutboundHandler are configured here.
    The as_view property returns an augmented view function ready to be used by Flask,
    adding inbound and outbound data handling behavior if needed.
    The resulting view function is a regular flask view function, and any overhead
    related to figuring out what needs to be done is spent at registration time.
    """

    def __init__(
        self, rule: str, view_func: JeroboamRouteCallable, options: Dict[str, Any]
    ):
        """Initialize the Route Class."""
        self.endpoint = options.pop("endpoint", None)
        self.methods = options.get("methods", ["GET"])
        self.status_code = options.pop("status_code", 200)
        self.inbound_handler = InboundHandler(view_func, self.methods, rule)
        self.outbound_handler = OutboundHandler(view_func, options)
        self.view_func = view_func

    @property
    def as_view(self) -> JeroboamRouteCallable:
        """Return a view funcion."""
        view_func = self.view_func
        # TODO: Manip sur le nom, etc...
        if self.inbound_handler:
            view_func = self.inbound_handler(view_func)
        if self.outbound_handler:
            view_func = self.outbound_handler(view_func, self.status_code)
        return view_func
