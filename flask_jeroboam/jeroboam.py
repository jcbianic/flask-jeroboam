"""The Flask Object with augmented functionality around route registration.

Here we overide the route method of the Flask object to use our custom implementation.
This allow us to introduce new functionality to the route registration process.
"""
from typing import Any
from typing import Callable

from flask import Flask
from flask.blueprints import Blueprint
from flask.scaffold import T_route
from flask.scaffold import setupmethod
from typing_extensions import TypeVar

from .view import JeroboamView


R = TypeVar("R", bound=Any)


class JeroboamScaffold:
    """A Flask Object with extra functionalities.

    The route method is overriden by a custom flask_jeroboam
    route decorator.
    """

    @setupmethod
    def route(self, rule: str, **options: Any) -> Callable[[T_route], T_route]:
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

        def decorator(func: T_route) -> T_route:
            route = JeroboamView(rule, func, options)
            self.add_url_rule(  # type: ignore
                rule, route.endpoint, route.as_view, **options
            )
            return func

        return decorator


class Jeroboam(JeroboamScaffold, Flask):
    """A Flask Object with extra functionalities.

    The route method is overriden by a custom flask_jeroboam
    route decorator.
    """

    pass


class JeroboamBlueprint(JeroboamScaffold, Blueprint):
    """Regular Blueprint with extra behavior on route definition."""

    pass
