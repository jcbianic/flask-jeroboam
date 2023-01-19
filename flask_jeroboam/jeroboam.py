"""The Flask Object with augmented functionality around route registration.

Here we overide the route method of the Flask object to use our custom implementation.
This allow us to introduce new functionality to the route registration process.
"""
from typing import Any
from typing import Callable

from flask import Flask
from flask.blueprints import Blueprint
from flask.scaffold import Scaffold
from typing_extensions import TypeVar

from .typing import JeroboamRouteCallable
from .view import JeroboamView


R = TypeVar("R", bound=Any)


def route_override(
    self: Scaffold, rule: str, **options: Any
) -> Callable[[JeroboamRouteCallable], JeroboamRouteCallable]:
    """Route Registration Override."""

    def decorator(func: JeroboamRouteCallable) -> JeroboamRouteCallable:
        route = JeroboamView(rule, func, options)

        self.add_url_rule(
            rule, route.endpoint, route.as_view, **options  # type: ignore
        )
        return func

    return decorator


class Jeroboam(Flask):
    """A Flask Object with extra functionalities.

    The route method is overriden by a custom flask_jeroboam
    route decorator.
    """

    route = route_override  # type: ignore[assignment]


class JeroboamBlueprint(Blueprint):
    """Regular Blueprint with extra behavior on route definition."""

    route = route_override  # type: ignore[assignment]
