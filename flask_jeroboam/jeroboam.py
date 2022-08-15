"""The Flask Object with augmented functionality around route registration."""
from flask import Flask

from flask_jeroboam._route import route


class Jeroboam(Flask):
    """A Flask Object with extra functionalities.

    The route method is overriden by a custom flask_jeroboam
    route decorator.
    """

    route = route
