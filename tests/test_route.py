"""Testing Base Class from Flask-Jeroboam."""

from flask import Blueprint as FlaskBlueprint
from flask import Flask
from pydantic import BaseModel

from flask_jeroboam.jeroboam import Blueprint
from flask_jeroboam.jeroboam import Jeroboam


def test_blueprint(
    inbound_model_test_class,
    reponse_model_test_class,
):
    """Test BluePrint Initialisation"""
    blueprint = Blueprint("test", __name__)

    assert issubclass(blueprint.__class__, FlaskBlueprint)


def test_jeroboam(
    inbound_model_test_class,
    reponse_model_test_class,
):
    """Test Jeroboam Initialisation"""
    app = Jeroboam("test")

    assert issubclass(app.__class__, Flask)


def test_route_without_response_model(app, client):
    """Test Route Decorator"""

    @app.route("/test")
    def test():
        return "test"

    data = client.get("/test").data

    assert data == b"test"


def test_route_with_response_model(app, client):
    """GIVEN a route decorator
    WHEN Called given a response_model
    THEN it generate a serializer
    """

    class OutBoundModel(BaseModel):
        data_str: str
        data_int: int

    @app.get("/test", response_model=OutBoundModel)
    def test():
        return OutBoundModel(**{"data_str": "test", "data_int": 1})

    data = client.get("/test").data

    assert data == OutBoundModel(data_str="test", data_int=1).json()
