"""The Flask Object with augmented functionality around route registration."""
from flask import Blueprint as FlaskBlueprint
from flask import Flask

from flask_jeroboam.route import route_overide


class Jeroboam(Flask):
    """A Flask Object with extra functionalities.

    The route method is overriden by a custom flask_jeroboam
    route decorator.
    """

    route = route_overide  # type: ignore[assignment]


class Blueprint(FlaskBlueprint):
    """A Blueprint Object with extra functionalities.

    The route method is overriden by a custom flask_jeroboam
    route decorator.
    """

    route = route_overide  # type: ignore[assignment]
