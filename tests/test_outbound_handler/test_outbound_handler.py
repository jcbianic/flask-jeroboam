"""Testing Outbound Handler Use Cases.

The endpoints are defined in the app_test.apps.outbound.py module.
"""
from typing import Any
from typing import Dict

import pytest
from flask.testing import FlaskClient

from flask_jeroboam.jeroboam import Jeroboam
from tests.app_test.models.outbound import SimpleModelOut


valid_outbound_data = {"items": ["Apple", "Banana"], "total_count": 10}
valid_response_body = {"items": ["Apple", "Banana"], "totalCount": 10}
unsorted_reponse_body = {"total_count": 10, "items": ["Apple", "Banana"]}


@pytest.mark.parametrize(
    "url", ["/methods/explicit_options", "/methods/explicit_options_and_head"]
)
def test_register_route_with_additionnal_secondary_verb(
    url: str,
    client: FlaskClient,
):
    """GIVEN an endpoint with secondary methods defined
    WHEN configured with secondary verbs (OPTIONS, HEAD)
    THEN it register and keeps the main verb
    """
    response = client.get(url)

    assert response.json == valid_response_body
    assert response.status_code == 200


def test_register_route_with_two_main_verb_raise_a_warning(
    one_shot_app: Jeroboam,
    one_shot_client: FlaskClient,
):
    """GIVEN an endpoint configured with two main http verb
    WHEN it is registered
    THEN it raises a warning and keep the first one
    """
    with pytest.warns(UserWarning):

        @one_shot_app.route(
            "/endpoint_with_two_main_verb",
            methods=["GET", "POST"],
            response_model=SimpleModelOut,
        )
        def with_two_main_verb():
            return valid_outbound_data

    response = one_shot_client.get("/endpoint_with_two_main_verb")
    assert response.json == valid_response_body


def test_register_route_with_method_route_and_methods_option_raise_a_exception(
    one_shot_app: Jeroboam,
):
    """GIVEN an endpoint configured with the method_route
    WHEN it is registered with the methods option
    THEN it raises an Exception
    """
    with pytest.raises(TypeError):

        @one_shot_app.get(
            "/route_method_and_methods_option",
            methods=["GET"],
            response_model=SimpleModelOut,
        )
        def route_method_and_methods_option():
            return valid_outbound_data


def test_endpoint_without_response_model(
    client: FlaskClient,
):
    """GIVEN an endpoint with no response_model configured or return annotation
    WHEN hit
    THEN it behaves like a regular Flask endpoint
    """
    response = client.get("/response_model/no_response_model")
    assert response.status_code == 200
    assert response.data == b"Don't have a response model"


def test_endpoint_with_valid_return_annocation(
    client: FlaskClient,
):
    """GIVEN an endpoint without response_model but with a valid return annotation
    WHEN registered
    THEN the annotation is stored as response_model
    """
    response = client.get("/response_model/infered_from_return_annotation")
    assert response.status_code == 200
    assert response.json == valid_response_body


def test_invalid_response_model_raise_type_error_at_registration(
    one_shot_app: Jeroboam,
):
    """GIVEN an endpoint with invalid response_model
    WHEN registered
    THEN it raises a TypeError
    """
    with pytest.raises(TypeError):

        @one_shot_app.get("/invalid_return_annotation_and_no_response_model")
        def invalid_return_annotation() -> dict:
            return valid_outbound_data

    with pytest.raises(TypeError):

        @one_shot_app.get("/invalid_response_model", response_model=dict)
        def invalid_configuration():
            return valid_outbound_data


def test_configured_response_model_take_prescedence_over_return_annotation(
    one_shot_client: FlaskClient,
):
    """GIVEN an endpoint without a configured response_model and a return annotation
    WHEN registered
    THEN the configrued response_model take prescedence over the return annotation
    """
    response = one_shot_client.get("/response_model/configuration_over_inference")
    assert response.status_code == 200
    assert response.json == valid_response_body


def test_endpoint_can_turn_off_return_annocation(
    client: FlaskClient,
):
    """GIVEN an endpoint with a valid return annotation
    WHEN response_model is configured to be None
    THEN the response_model registration is turned off
    """
    with pytest.raises(TypeError):
        client.get("/response_model/turned_off")


@pytest.mark.parametrize(
    "type_,expected_response",
    [
        ("dict", valid_response_body),
        ("list", [unsorted_reponse_body, unsorted_reponse_body]),
        ("base_model", valid_response_body),
        ("response", valid_response_body),
        ("dataclass", valid_response_body),
    ],
)
def test_view_function_with_response_model_return_type(
    type_: str,
    expected_response: Any,
    client: FlaskClient,
):
    """GIVEN an endpoint with a response_model defined and dict return value
    WHEN hit
    THEN it serialize the dict using the response_model
    #TODO: find a case where it wouldn't pass without the response_model !!
    """
    response = client.get(f"/return_type/{type_}")

    assert response.status_code == 200
    assert response.json == expected_response


def test_wrong_dict_being_sent(
    one_shot_app: Jeroboam,
    one_shot_client: FlaskClient,
):
    """GIVEN an endpoint with a response_model defined and a dict return value
    WHEN hit and the return value is not valid
    THEN it raises a InternalServerError, 500
    """

    @one_shot_app.get("/invalid_return_value", response_model=SimpleModelOut)
    def ping():
        return {"total_count": "not_valid", "items": ["Apple", "Banana"]}

    response = one_shot_client.get("/invalid_return_value")

    assert response.status_code == 500
    assert response.data.startswith(b"InternalServerError")


@pytest.mark.parametrize(
    "shape,status_code,headers",
    [
        ("with_headers", 200, {"X-Test": "Test"}),
        ("with_status_code", 218, {}),
        ("with_headers_and_status_code", 218, {"X-Test": "Test"}),
    ],
)
def test_view_function_tuple_return_shape(
    shape: str,
    status_code: int,
    headers: Dict[str, str],
    client: FlaskClient,
):
    """GIVEN an endpoint with a response_model defined and a dict return value
    WHEN hit and the return value is not valid
    THEN it raises a InternalServerError, 500
    """
    response = client.get(f"/return_shape/{shape}")
    assert response.status_code == status_code
    assert response.headers.get("X-Test", "Empty") == headers.get("X-Test", "Empty")


def test_wrong_tuple_length_raise_error(
    client: FlaskClient,
):
    """GIVEN a viewfunction with the wrongly shaped tuple (>3)
    WHEN hit
    THEN it raises a TypeError (as in Flask) and return a code 500
    """
    with pytest.raises(TypeError):
        respone = client.get("/return_shape/wrong_tuple_length")

        assert respone.status_code == 500


def test_content_raise_an_error_if_anything_else(
    client: FlaskClient,
):
    """GIVEN an endpoint with an exotic HTTP verb and no status_code defined
    WHEN registered
    THEN a Value Warning is raised
    """
    with pytest.raises(ValueError):
        response = client.get("/return_type/not_valid")

        assert response.status_code == 500


def test_reponse_model_filters_outbound_data_even_when_subclassing(
    client: FlaskClient,
):
    """GIVEN an endpoint with an exotic HTTP verb and no status_code defined
    WHEN registered
    THEN a User Warning is raised
    """
    response = client.post(
        "/sensitive_data",
        json={"sensitive_data": {"username": "test", "password": "test"}},
    )

    assert response.json == {"username": "test"}
    assert response.status_code == 201
