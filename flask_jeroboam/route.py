"""The Routing Object glue Parser, Serializer and OpenApi Together."""
import typing as t
from typing import Callable
from typing import TypeVar

from flask.scaffold import Scaffold
from typing_extensions import ParamSpec

from flask_jeroboam.exceptions import InvalidRequest

from ._parser import Parser
from ._serializer import Serializer


F = TypeVar("F", bound=t.Callable[..., t.Any])
P = ParamSpec("P")


class Route:
    """Base Model for adding Behaviors to Flask Views functions."""

    def __init__(self, view_function: Callable, options: dict):
        self.view_function = view_function
        self.options = options
        self.parser = Parser(view_function, options)
        self.serializer = Serializer(view_function, options)

    def get_open_api(self):
        """Return the OpenAPI specification for the Route."""
        if self.spec is None:
            self.spec = self.build_open_api()
        return self.spec

    def build_open_api(self):
        """Build the OpenAPI specification for the Route."""
        raise NotImplementedError

    @property
    def __name__(self):
        """Return the name of the view function."""
        return self.view_function.__name__

    def __call__(self, *_args: P.args, **_kwargs: P.kwargs):
        """In the end a route is just a callable."""
        values, errors = self.parser()
        if errors:
            raise InvalidRequest(errors)
        raw_result = self.view_function(**values)
        response = self.serializer(raw_result)
        return response


def route_overide(
    self: Scaffold, rule: str, **options: t.Any
) -> t.Callable[[F], Route]:  # type: ignore[override]
    """Override the route decorator defined in Scaffold."""

    def register_route(f: F) -> Route:
        endpoint = options.pop("endpoint", None)
        route = Route(f, options)
        self.add_url_rule(rule, endpoint, route, **options)
        return route

    return register_route
