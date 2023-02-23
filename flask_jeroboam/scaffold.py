"""The Scaffold Override.

It is used to override the route method of both Flask and Blueprints Object
in Jeroboam and jeroboam's Blueprints.
"""
from typing import Any
from typing import Callable

from flask.scaffold import setupmethod
from typing_extensions import TypeVar

from flask_jeroboam.typing import JeroboamRouteCallable
from flask_jeroboam.view import JeroboamView


R = TypeVar("R", bound=Any)


class JeroboamScaffoldOverRide:
    """Mixin to override the route method.

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
