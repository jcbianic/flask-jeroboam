"""Testing Outbound Handler Use Cases.
We test for various return values (Response, Dict, ResponseModel),
configuration (response_model or not) and error handling.
"""
import json
import warnings
from dataclasses import dataclass
from typing import List
from unittest.mock import patch

import pytest
from flask import Response
from flask.testing import FlaskClient
from pydantic import BaseModel

from flask_jeroboam.jeroboam import Jeroboam


class OutBoundModel(BaseModel):
    """Base OutBoundModel for Testing."""

    total_count: int
    items: List[str]


valid_outbound_data = {"total_count": 10, "items": ["Apple", "Banana"]}
valid_response_body = b'{"total_count": 10, "items": ["Apple", "Banana"]}'


def test_register_route_with_additionnal_secondary_verb(
    app: Jeroboam,
    client: FlaskClient,
):
    """GIVEN an endpoint with only one main http verb
    WHEN configured with secondary verbs (OPTIONS, HEAD)
    THEN it register and keeps the main verb
    """

    @app.route(
        "/endpoint_with_options",
        methods=["GET", "OPTIONS"],
        response_model=OutBoundModel,
    )
    def with_one_secondary_verb():
        return valid_outbound_data

    @app.route(
        "/endpoint_with_options",
        methods=["GET", "OPTIONS", "HEAD"],
        response_model=OutBoundModel,
    )
    def with_two_secondary_verb():
        return valid_outbound_data

    r = client.get("/endpoint_with_options")
    assert r.data == valid_response_body
    assert app.url_map._rules_by_endpoint["with_one_secondary_verb"][0].methods == {
        "GET",
        "OPTIONS",
        "HEAD",
    }
    assert app.url_map._rules_by_endpoint["with_two_secondary_verb"][0].methods == {
        "GET",
        "OPTIONS",
        "HEAD",
    }


def test_register_route_with_two_main_verb_raise_a_warning(
    app: Jeroboam,
    client: FlaskClient,
):
    """GIVEN an endpoint configured with two main http verb
    WHEN it is registered
    THEN it raises a warning and keep the first one
    """
    with pytest.warns(UserWarning):

        @app.route(
            "/endpoint_with_stwo_main_verb",
            methods=["GET", "POST"],
            response_model=OutBoundModel,
        )
        def with_two_main_verb():
            return valid_outbound_data

    r = client.get("/endpoint_with_stwo_main_verb")
    assert r.data == valid_response_body


def test_register_route_with_method_route_and_methods_option_raise_a_exception(
    app: Jeroboam,
    client: FlaskClient,
):
    """GIVEN an endpoint configured with the method_route
    WHEN it is registered with the methods option
    THEN it raises an Exception
    """
    with pytest.raises(TypeError):

        @app.get(
            "/route_method_and_methods_option",
            methods=["GET"],
            response_model=OutBoundModel,
        )
        def route_method_and_methods_option():
            return valid_outbound_data


def test_endpoint_with_put(
    app: Jeroboam,
    client: FlaskClient,
):
    """GIVEN an endpoint registered wit put
    WHEN hit with a put request
    THEN it responds with a 201 status code
    """

    @app.put("/put_http_verb", response_model=OutBoundModel)
    def put_http_verb():
        return valid_outbound_data

    r = client.put("/put_http_verb")
    assert r.status_code == 201
    assert r.data == valid_response_body


def test_endpoint_with_patch(
    app: Jeroboam,
    client: FlaskClient,
):
    """GIVEN an endpoint registered wit put
    WHEN hit with a patch request
    THEN it responds with a 201 status code
    """

    @app.patch("/patch_http_verb", response_model=OutBoundModel)
    def patch_http_verb():
        return valid_outbound_data

    r = client.patch("/patch_http_verb")
    assert r.status_code == 200
    assert r.data == valid_response_body


def test_endpoint_without_response_model(
    app: Jeroboam,
    client: FlaskClient,
):
    """GIVEN an endpoint with no response_model configured or return annotation
    WHEN hit
    THEN it behaves like a regular Flask endpoint
    """

    @app.get("/no_response_model")
    def no_response_model():
        return "Don't have a response model"

    r = client.get("/no_response_model")
    assert r.status_code == 200
    assert r.data == b"Don't have a response model"


def test_endpoint_with_valid_return_annocation(
    app: Jeroboam,
    client: FlaskClient,
):
    """GIVEN an endpoint without response_model but with a valid return annotation
    WHEN registered
    THEN the annotation is stored as response_model
    """

    @app.get("/valid_return_annotation")
    def valid_return_annotation() -> OutBoundModel:
        return OutBoundModel(**valid_outbound_data)

    r = client.get("/valid_return_annotation")

    assert r.status_code == 200
    assert r.data == valid_response_body


def test_invalid_response_model_raise_type_error_at_registration(
    app: Jeroboam,
    client: FlaskClient,
):
    """GIVEN an endpoint with invladidly typed response_model
    WHEN registered
    THEN it raises a TypeError
    """
    with pytest.raises(TypeError):

        @app.get("/invalid_return_annotation")
        def invalid_return_annotation() -> dict:
            return valid_outbound_data

    with pytest.raises(TypeError):

        @app.get("/invalid_configuration", response_model=dict)
        def invalid_configuration():
            return valid_outbound_data


def test_configured_response_model_take_prescedence_over_return_annotation(
    app: Jeroboam,
    client: FlaskClient,
):
    """GIVEN an endpoint without a configured response_model and a return annotation
    WHEN registered
    THEN configrued response_model take prescedence over return annotation
    """

    @app.get("/configured_reponse_model_take_prescedence", response_model=OutBoundModel)
    def test() -> dict:
        return {"total_count": 10, "items": ["Apple", "Banana"]}

    r = client.get("/configured_reponse_model_take_prescedence")

    assert r.status_code == 200
    assert r.data == valid_response_body


def test_endpoint_can_turn_off_return_annocation(
    app: Jeroboam,
    client: FlaskClient,
):
    """GIVEN an endpoint with a valid return annotation
    WHEN response_model is configured to be None
    THEN the response_model registration is turned off
    """

    @app.get("/with_return_annotation_turned_off", response_model=None)
    def test() -> OutBoundModel:
        return OutBoundModel(**{"total_count": 10, "items": ["Apple", "Banana"]})

    with pytest.raises(TypeError):
        client.get("/with_return_annotation_turned_off")


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
    def endpoint_returns_a_dict() -> dict:
        return valid_outbound_data

    r = client.get("/endpoint_returns_a_dict")

    assert r.status_code == 200
    assert r.data == valid_response_body


def test_endpoint_with_list_as_return_value(
    app: Jeroboam,
    client: FlaskClient,
):
    """GIVEN an endpoint with a response_model as a List
    WHEN hit
    THEN it serialize the list using the response_model
    """

    @app.get("/endpoint_returns_a_list", response_model=List[OutBoundModel])
    def test():
        return [valid_outbound_data, valid_outbound_data]

    r = client.get("/endpoint_returns_a_list")

    assert r.status_code == 200
    assert (
        r.data == b'[{"total_count": 10, "items": ["Apple", "Banana"]}, '
        b'{"total_count": 10, "items": ["Apple", "Banana"]}]'
    )


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


def test_status_code_204_has_no_body(
    app: Jeroboam,
    client: FlaskClient,
):
    """GIVEN an endpoint with a response_model defined and a dict return value
    WHEN hit and the return value is not valid
    THEN it raises a InternalServerError, 500
    """

    @app.get("/status_code_204_has_no_body", response_model=OutBoundModel)
    def status_code_204_has_no_body():
        return "Some Content that will be ignored", 204

    r = client.get("/status_code_204_has_no_body")

    assert r.status_code == 204
    assert r.data == b""


def test_can_pass_headers_values(
    app: Jeroboam,
    client: FlaskClient,
):
    """GIVEN an endpoint with a response_model defined and a dict return value
    WHEN hit and the return value is not valid
    THEN it raises a InternalServerError, 500
    """

    @app.get("/returned_headers_are_sent", response_model=OutBoundModel)
    def returned_headers_are_sent():
        return valid_outbound_data, {"X-Test": "Test"}

    r = client.get("/returned_headers_are_sent")

    assert r.status_code == 200
    assert r.headers["X-Test"] == "Test"


def test_can_pass_headers_values_and_status_code(
    app: Jeroboam,
    client: FlaskClient,
):
    """GIVEN an endpoint that returns a content, a status code and headers
    WHEN hit
    THEN the response has the status code and headers
    """

    @app.get("/returned_headers_and_status_code_are_sent", response_model=OutBoundModel)
    def returned_headers_are_sent():
        return valid_outbound_data, 201, {"X-Test": "Test"}

    r = client.get("/returned_headers_and_status_code_are_sent")

    assert r.status_code == 201
    assert r.headers["X-Test"] == "Test"


@patch("flask_jeroboam._outboundhandler.METHODS_DEFAULT_STATUS_CODE", {"POST": 201})
def test_exotic_http_verb_raise_a_warning_when_no_status_code_is_set(
    app: Jeroboam,
    client: FlaskClient,
):
    """GIVEN an endpoint with an exotic HTTP verb and no status_code defined
    WHEN registered
    THEN a User Warning is raised
    """
    with pytest.warns(UserWarning):

        @app.get(
            "/exotic_http_verb_raise_a_warning",
            response_model=OutBoundModel,
        )
        def exotic_http_verb():
            return valid_outbound_data

    r = client.get("/exotic_http_verb_raise_a_warning")

    assert r.status_code == 200


@patch("flask_jeroboam._outboundhandler.METHODS_DEFAULT_STATUS_CODE", {"POST": 201})
def test_exotic_http_verb_dont_raise_a_warning_when_status_code_is_set(
    app: Jeroboam,
    client: FlaskClient,
):
    """GIVEN an endpoint with an exotic HTTP verb and no status_code defined
    WHEN registered
    THEN a User Warning is raised
    """
    with warnings.catch_warnings():
        warnings.simplefilter("error")

        @app.get(
            "/exotic_http_verb_dont_raise_a_warning",
            response_model=OutBoundModel,
            status_code=200,
        )
        def exotic_http_verb():
            return valid_outbound_data

    r = client.get("/exotic_http_verb_dont_raise_a_warning")

    assert r.status_code == 200


def test_content_can_be_a_dataclass(
    app: Jeroboam,
    client: FlaskClient,
):
    """GIVEN an endpoint with an exotic HTTP verb and no status_code defined
    WHEN registered
    THEN a User Warning is raised
    """

    @dataclass
    class MyDataClass:
        total_count: int
        items: List[str]

    @app.get("/response_value_as_dataclass", response_model=OutBoundModel)
    def response_value_as_list():
        return MyDataClass(**valid_outbound_data)

    r = client.get("/response_value_as_dataclass")

    assert r.status_code == 200
    assert r.data == valid_response_body


def test_content_raise_an_error_if_anything_else(
    app: Jeroboam,
    client: FlaskClient,
):
    """GIVEN an endpoint with an exotic HTTP verb and no status_code defined
    WHEN registered
    THEN a User Warning is raised
    """
    with pytest.raises(ValueError):

        @app.get("/response_value_is_not_valid_format", response_model=OutBoundModel)
        def response_value_as_list():
            return "not a list"

        r = client.get("/response_value_is_not_valid_format")

        assert r.status_code == 500


def test_reponse_model_filters_outbound_data_even_when_subclassing(
    app: Jeroboam,
    client: FlaskClient,
):
    """GIVEN an endpoint with an exotic HTTP verb and no status_code defined
    WHEN registered
    THEN a User Warning is raised
    """

    class SecureOutBoundUser(BaseModel):
        username: str

    class InBoundUser(SecureOutBoundUser):
        password: str

    @app.post("/filters_data", response_model=SecureOutBoundUser)
    def filters_data(sensitive_data: InBoundUser):
        return sensitive_data

    r = client.post(
        "/filters_data", data=json.dumps({"username": "test", "password": "test"})
    )

    assert r.status_code == 201
    assert r.data == json.dumps({"username": "test"}).encode()


def test_wrong_tuple_length_raise_error(
    app: Jeroboam,
    client: FlaskClient,
):
    """GIVEN an endpoint with an exotic HTTP verb and no status_code defined
    WHEN registered
    THEN a User Warning is raised
    """

    @app.get("/wrong_tuple_length", response_model=OutBoundModel)
    def wrong_tuple_length():
        return valid_outbound_data, 200, {"X-Test": "Test"}, "extra"

    with pytest.raises(TypeError):
        r = client.get("/wrong_tuple_length")

        assert r.status_code == 500
