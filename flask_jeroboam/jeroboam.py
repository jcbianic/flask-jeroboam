"""The Flask Object with augmented functionality around route registration.

Here we overide the route method of the Flask object to use our custom implementation.
This allow us to introduce new functionality to the route registration process.

TODO: A probably better way to override it is to override the url_rule_class
with a custom JeroboamRule Object
"""
from typing import Any
from typing import Callable
from typing import Optional

from flask import Flask
from flask.blueprints import Blueprint
from flask.scaffold import setupmethod
from typing_extensions import TypeVar

from ._config import JeroboamConfig
from .responses import JSONResponse
from .typing import JeroboamRouteCallable
from .view import JeroboamView


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

        def decorator(func: JeroboamRouteCallable) -> JeroboamRouteCallable:
            route = JeroboamView(rule, func, options)
            self.add_url_rule(  # type: ignore
                rule, route.endpoint, route.as_view, **options
            )
            return func

        return decorator

    def _method_route(
        self,
        method: str,
        rule: str,
        options: dict,
    ) -> Callable[[JeroboamRouteCallable], JeroboamRouteCallable]:
        if "methods" in options:
            raise TypeError("Use the 'route' decorator to use the 'methods' argument.")

        return self.route(rule, methods=[method], **options)

    @setupmethod
    def get(
        self, rule: str, **options: Any
    ) -> Callable[[JeroboamRouteCallable], JeroboamRouteCallable]:
        """Shortcut for :meth:`route` with ``methods=["GET"]``."""
        return self._method_route("GET", rule, options)

    @setupmethod
    def post(
        self, rule: str, **options: Any
    ) -> Callable[[JeroboamRouteCallable], JeroboamRouteCallable]:
        """Shortcut for :meth:`route` with ``methods=["POST"]``."""
        return self._method_route("POST", rule, options)

    @setupmethod
    def put(
        self, rule: str, **options: Any
    ) -> Callable[[JeroboamRouteCallable], JeroboamRouteCallable]:
        """Shortcut for :meth:`route` with ``methods=["PUT"]``."""
        return self._method_route("PUT", rule, options)

    @setupmethod
    def delete(
        self, rule: str, **options: Any
    ) -> Callable[[JeroboamRouteCallable], JeroboamRouteCallable]:
        """Shortcut for :meth:`route` with ``methods=["DELETE"]``."""
        return self._method_route("DELETE", rule, options)

    @setupmethod
    def patch(
        self, rule: str, **options: Any
    ) -> Callable[[JeroboamRouteCallable], JeroboamRouteCallable]:
        """Shortcut for :meth:`route` with ``methods=["PATCH"]``."""
        return self._method_route("PATCH", rule, options)


class Jeroboam(JeroboamScaffoldOverRide, Flask):  # type:ignore
    """A Flask Object with extra functionalities.

    The route method is overriden by a custom flask_jeroboam
    route decorator.
    """

    response_class = JSONResponse

    query_string_key_transformer: Optional[Callable] = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Init."""
        super().__init__(*args, **kwargs)
        self.config.update(JeroboamConfig().dict())


class JeroboamBlueprint(JeroboamScaffoldOverRide, Blueprint):  # type:ignore
    """Regular Blueprint with extra behavior on route definition."""

    def __init__(
        self,
        *args: Any,
        tags: List[str] = empty_list,
        include_in_openapi: bool = True,
        **kwargs: Any
    ) -> None:
        """Init."""
        self.include_in_openapi = include_in_openapi
        self.tags = tags
        super().__init__(*args, **kwargs)
