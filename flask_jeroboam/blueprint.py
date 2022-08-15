"""Blueprint overriding Flask's default routing."""
from flask.blueprints import Blueprint

from ._route import route


class APIBlueprint(Blueprint):
    """Regular Blueprint with extra behavior on route definition."""

    route = route
