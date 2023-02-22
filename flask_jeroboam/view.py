"""The Route Class."""
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Type
from typing import TypeVar

from typing_extensions import ParamSpec

from flask_jeroboam._inboundhandler import InboundHandler
from flask_jeroboam._outboundhandler import OutboundHandler
from flask_jeroboam.responses import JSONResponse
from flask_jeroboam.typing import JeroboamRouteCallable
from flask_jeroboam.view_arguments.solved import SolvedArgument


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
        self.main_http_verb = self._solve_main_http_verb(options, original_view_func)
        configured_status_code: Optional[int] = options.pop("status_code", None)
        self.inbound_handler = InboundHandler(
            original_view_func, self.main_http_verb, rule
        )
        self.outbound_handler = OutboundHandler(
            original_view_func,
            configured_status_code,
            self.main_http_verb,
            options,
            response_class,
        )
        self.original_view_func = original_view_func
        self.include_in_openapi = options.pop("include_in_openapi", True)
        self.has_request_body = self.inbound_handler.has_request_body
        self.rule = rule

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
        view_func = self.outbound_handler.add_outbound_handling_to(view_func)

        view_func.__name__ = name
        view_func.__doc__ = doc
        # TODO voir comment passer l'objet lui-même.
        view_func.__jeroboam_view__ = self  # type: ignore
        return view_func

    @property
    def main_method(self) -> str:
        """Return the main HTTP verb of the Endpoint."""
        return self.main_http_verb.lower()

    @property
    def parameters(self) -> List[SolvedArgument]:
        """Return the main HTTP verb of the Endpoint."""
        return self.inbound_handler.parameters

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
                stacklevel=2,
            )
        return methods[0]
