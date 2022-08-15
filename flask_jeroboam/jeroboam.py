"""The Flask Object with augmented functionality around route registration."""
from flask import Flask
from flask_jeroboam._route import route


class Jeroboam(Flask):
    """A replacement for Flask Object with augmented functionality around route registration."""

    route = route
