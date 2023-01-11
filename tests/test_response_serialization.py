"""Testing Response Serialisation Use Cases.
We test for various return values (Response, Dict, ResponseModel),
configuration (response_model or not) and error handling.
"""
from typing import List

from flask import Response
from flask.testing import FlaskClient
from pydantic import BaseModel

from flask_jeroboam.jeroboam import Jeroboam


class OutBoundModel(BaseModel):
    """Base OutBoundModel for Testing."""

    total_count: int
    items: List[str]


def test_endpoint_without_response_model(
    app: Jeroboam,
    client: FlaskClient,
):
    """GIVEN an endpoint without response_model defined
    WHEN hit
    THEN it behaves like a regular Flask endpoint
    """

    @app.get("/simple_endpoint")
    def ping():
        return "pong"

    r = client.get("/simple_endpoint")
    assert r.status_code == 200
    assert r.data == b"pong"


def test_endpoint_with_response_model_and_dict_as_return_value(
    app: Jeroboam,
    client: FlaskClient,
):
    """GIVEN an endpoint with a response_model defined and dict return value
    WHEN hit
    THEN it serialize the dict using the response_model
    #TODO: find a case where it wouldn't pass without the response_model !!
    """

    @app.get("/endpoint_returns_a_dict", response_model=OutBoundModel)
    def test():
        return {"total_count": 10, "items": ["Apple", "Banana"]}

    r = client.get("/endpoint_returns_a_dict")

    assert r.status_code == 200
    assert r.data == b'{"total_count": 10, "items": ["Apple", "Banana"]}'


def test_endpoint_with_response_model_and_response_model_as_return_value(
    app: Jeroboam,
    client: FlaskClient,
):
    """GIVEN an endpoint with a response_model defined and dict return value
    WHEN hit
    THEN it serialize the dict using the response_model
    #TODO: find a case where it wouldn't pass without the response_model !!
    """

    @app.get("/endpoint_returns_a_dict", response_model=OutBoundModel)
    def test():
        return OutBoundModel(total_count=10, items=["Apple", "Banana"])

    r = client.get("/endpoint_returns_a_dict")

    assert r.status_code == 200
    assert r.data == b'{"total_count": 10, "items": ["Apple", "Banana"]}'


def test_endpoint_with_response_model_and_response_as_return_value(
    app: Jeroboam,
    client: FlaskClient,
):
    """GIVEN an endpoint with a response_model defined and a Response return value
    WHEN hit
    THEN it sends the Response untouched
    """

    @app.get("/endpoint_returns_a_response", response_model=OutBoundModel)
    def test():
        return Response(OutBoundModel(total_count=10, items=["Apple", "Banana"]).json())

    r = client.get("/endpoint_returns_a_response")

    assert r.status_code == 200
    assert r.data == b'{"total_count": 10, "items": ["Apple", "Banana"]}'


def test_wrong_dict_being_sent(
    app: Jeroboam,
    client: FlaskClient,
):
    """GIVEN an endpoint with a response_model defined and a dict return value
    WHEN hit and the return value is not valid
    THEN it raises a InternalServerError, 500
    """

    @app.get("/invalid_return_value", response_model=OutBoundModel)
    def ping():
        return {"total_count": "not_valid", "items": ["Apple", "Banana"]}

    r = client.get("/invalid_return_value")

    assert r.status_code == 500
    assert r.data.startswith(b"InternalServerError")
