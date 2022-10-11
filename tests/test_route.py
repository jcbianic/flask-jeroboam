"""Testing Base Class from Flask-Jeroboam."""
from unittest import mock

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


@mock.patch("flask_jeroboam._route.serializer")
def test_route_without_response_model(mock_serializer, app, client):
    """Test Route Decorator"""

    @app.route("/test")
    def test():
        return "test"

    assert mock_serializer.is_not_called()
    assert client.get("/test").data == b"test"


@mock.patch("flask_jeroboam._route.serializer")
def test_route_with_response_model(mock_serializer, app, client):
    """GIVEN a route decorator
    WHEN Called given a response_model
    THEN it generate a serializer
    """

    class InBoundModel(BaseModel):
        data_str: str
        data_int: int

    @app.route("/test", response_model=InBoundModel)
    def test():
        return "test"

    mock_serializer.return_value = lambda c: c

    assert mock_serializer.is_called_with(InBoundModel, 200)
