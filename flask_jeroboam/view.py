"""The Route Class."""
from typing import Any
from typing import Dict
from typing import Optional
from typing import Type
from typing import TypeVar

from typing_extensions import ParamSpec

from ._inboundhandler import InboundHandler
from ._outboundhandler import OutboundHandler
from .responses import JSONResponse
from .typing import JeroboamRouteCallable


P = ParamSpec("P")
R = TypeVar("R")


class JeroboamView:
    """Adds flask-jeroboam features to a regular flask view function.

    The InboundHandler and OutboundHandler are configured here.
    The as_view property returns an augmented view function ready to be used by Flask,
    adding inbound and outbound data handling behavior if needed.
    The resulting view function is a regular flask view function, and any overhead
    related to figuring out what needs to be done is spent at registration time.
    """

    def __init__(
        self,
        rule: str,
        original_view_func: JeroboamRouteCallable,
        options: Dict[str, Any],
        response_class: Optional[Type] = JSONResponse,
    ):
        """Initialize the JeroboamView.

        TODO: Is there a better way to set the default value of response_class?
        """
        assert response_class is not None  # noqa: S101
        self.endpoint = options.pop("endpoint", None)
        main_http_verb = self._solve_main_http_verb(options, original_view_func)
        configured_status_code: Optional[int] = options.pop("status_code", None)
        self.inbound_handler = InboundHandler(original_view_func, main_http_verb, rule)
        self.outbound_handler = OutboundHandler(
            original_view_func,
            configured_status_code,
            main_http_verb,
            options,
            response_class,
        )
        self.original_view_func = original_view_func

    @property
    def as_view(self) -> JeroboamRouteCallable:
        """Decorate the orinal view function with handlers..

        TODO: Deal with name, docs, before decorating
        """
        view_func = self.original_view_func
        name = view_func.__name__
        doc = view_func.__doc__

        if self.inbound_handler.is_valid:
            view_func = self.inbound_handler.add_inbound_handling_to(view_func)
        if self.outbound_handler.is_valid_handler():
            view_func = self.outbound_handler.add_outbound_handling_to(view_func)

        view_func.__name__ = name
        view_func.__doc__ = doc
        return view_func

    def _solve_main_http_verb(
        self, options: Dict[str, Any], original_view_func: JeroboamRouteCallable
    ) -> str:
        """Return the main HTTP verb of the Endpoint.

        Here we consider that the main verb is either OPTIONS if it's the only
        one present,
        or either GET, PUT, POST, DELETE, PATCH, HEAD when present with OPTIONS.
        The presence of more than one verb from the latter list will raise
        a UserWarning.
        Only the fist one will be considered as the main verb.
        Default to GET if no verb is present.
        """
        methods = options.get("methods", ["GET"])
        if len(methods) == 1:
            return methods[0]
        if "OPTIONS" in methods:
            methods.remove("OPTIONS")
        if "HEAD" in methods:
            methods.remove("HEAD")
        if len(methods) >= 2:
            import warnings

            main_verbs = ", ".join(methods)
            warnings.warn(
                f"More than two primary HTTP verbs ({main_verbs}) are present"
                "on the endpoint "
                f"'{original_view_func.__module__}:{original_view_func.__name__}'. "
                f"The main verb is not clear and only the first one ({methods[0]}) "
                "will be picked. If you thing this is a mistake, please open an issue.",
                UserWarning,
            )
        return methods[0]
