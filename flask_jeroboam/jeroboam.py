"""The Flask Object with augmented functionality around route registration.

Here we overide the route method of the Flask object to use our custom implementation.
This allow us to introduce new functionality to the route registration process.

TODO: A probably better way to override it is to override the url_rule_class
with a custom JeroboamRule Object
"""
from typing import Any
from typing import Callable
from typing import List
from typing import Optional

from flask import Flask
from flask import current_app  # noqa: F401
from flask.blueprints import Blueprint as FlaskBlueprint
from flask.scaffold import setupmethod
from typing_extensions import TypeVar

from flask_jeroboam._config import JeroboamConfig
from flask_jeroboam.openapi.builder import build_openapi
from flask_jeroboam.openapi.models.openapi import OpenAPI
from flask_jeroboam.responses import JSONResponse
from flask_jeroboam.rule import JeroboamRule
from flask_jeroboam.typing import JeroboamRouteCallable
from flask_jeroboam.view import JeroboamView


R = TypeVar("R", bound=Any)


class JeroboamScaffoldOverRide:
    """A Flask Object with extra functionalities.

    The route method is overriden by a custom flask_jeroboam
    route decorator.
    """

    @setupmethod
    def route(
        self, rule: str, **options: Any
    ) -> Callable[[JeroboamRouteCallable], JeroboamRouteCallable]:
        """View function decorator to register a route.

        Decorate a view function to register it with the given URL
        rule and options. Calls :meth:`add_url_rule`, which has more
        details about the implementation.

        .. code-block:: python

            @app.route("/")
            def index():
                return "Hello, World!"

        See :ref:`url-route-registrations`.

        The endpoint name for the route defaults to the name of the view
        function if the ``endpoint`` parameter isn't passed.

        The ``methods`` parameter defaults to ``["GET"]``. ``HEAD`` and
        ``OPTIONS`` are added automatically.

        :param rule: The URL rule string.
        :param options: Extra options passed to the
            :class:`~werkzeug.routing.Rule` object.
        """

        def decorator(view_func: JeroboamRouteCallable) -> JeroboamRouteCallable:
            options.setdefault("tags", []).extend(getattr(self, "tags", []))
            blueprint_option = getattr(self, "include_in_openapi", None)
            view = JeroboamView(rule, view_func, options) if view_func else None
            options["main_method"] = getattr(view, "main_http_verb", None)
            if blueprint_option is not None:
                options["include_in_openapi"] = blueprint_option
            self.add_url_rule(  # type: ignore
                rule, view.endpoint, view.as_view, **options  # type: ignore
            )
            return view_func

        return decorator


class Jeroboam(JeroboamScaffoldOverRide, Flask):  # type:ignore
    """A Flask Object with extra functionalities.

    The route method is overriden by a custom flask_jeroboam
    route decorator.
    """

    response_class = JSONResponse

    url_rule_class = JeroboamRule

    query_string_key_transformer: Optional[Callable] = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Init."""
        super().__init__(*args, **kwargs)
        self.config.update(JeroboamConfig.load().dict())
        self._openapi: Optional[OpenAPI] = None

    @property
    def openapi(self) -> OpenAPI:
        """Get the OpenApi object."""
        if self._openapi is None:
            self._openapi = build_openapi(
                app=self,  # type: ignore
                rules=list(self.url_map.iter_rules()),  # type: ignore
                tags=[],
            )
        return self._openapi


class Blueprint(JeroboamScaffoldOverRide, FlaskBlueprint):  # type:ignore
    """Regular Blueprint with extra behavior on route definition."""

    def __init__(
        self,
        *args: Any,
        tags: Optional[List[str]] = None,
        include_in_openapi: bool = True,
        **kwargs: Any,
    ) -> None:
        """Init."""
        self.include_in_openapi = include_in_openapi
        self.tags = tags or []
        super().__init__(*args, **kwargs)
