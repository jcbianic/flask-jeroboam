"""Testing for status code configuration.

Endpoints are defined in the app_test.apps.outbound.py module.
"""
import warnings
from unittest.mock import patch

import pytest
from flask.testing import FlaskClient

from flask_jeroboam.jeroboam import Jeroboam
from tests.app_test.models.outbound import SimpleModelOut


valid_outbound_data = {"items": ["Apple", "Banana"], "total_count": 10}
valid_response_body = {"items": ["Apple", "Banana"], "totalCount": 10}
unsorted_reponse_body = {"total_count": 10, "items": ["Apple", "Banana"]}


def test_endpoint_with_put(
    client: FlaskClient,
):
    """GIVEN an endpoint registered wit put
    WHEN hit with a put request
    THEN it responds with a 201 status code
    """
    response = client.put("/verb/put/without_explicit_status_code")
    assert response.status_code == 201
    assert response.json == valid_response_body


def test_endpoint_with_patch(
    client: FlaskClient,
):
    """GIVEN an endpoint registered wit put
    WHEN hit with a patch request
    THEN it responds with a 201 status code
    """
    response = client.patch("/verb/patch/without_explicit_status_code")
    assert response.status_code == 200
    assert response.json == valid_response_body


@pytest.mark.parametrize("variant", ["as_returned", "as_configured"])
def test_status_code_204_has_no_body(
    variant: str,
    client: FlaskClient,
):
    """GIVEN a 204 Status Code
    WHEN building the response
    THEN the response has no body
    """
    response = client.get(f"/status_code/204_has_no_body/{variant}")
    assert response.status_code == 204
    assert response.data == b""


@patch("flask_jeroboam._outboundhandler.METHODS_DEFAULT_STATUS_CODE", {"POST": 201})
def test_exotic_http_verb_raise_a_warning_when_no_status_code_is_set(
    one_shot_app: Jeroboam,
    one_shot_client: FlaskClient,
):
    """GIVEN an endpoint with an exotic HTTP verb and no status_code defined
    WHEN registered
    THEN a User Warning is raised
    """
    with pytest.warns(UserWarning):

        @one_shot_app.get(
            "/exotic_http_verb_raise_a_warning",
            response_model=SimpleModelOut,
        )
        def exotic_http_verb():
            return valid_outbound_data

    response = one_shot_client.get("/exotic_http_verb_raise_a_warning")

    assert response.status_code == 200


@patch("flask_jeroboam._outboundhandler.METHODS_DEFAULT_STATUS_CODE", {"POST": 201})
def test_exotic_http_verb_dont_raise_a_warning_when_status_code_is_set(
    one_shot_app: Jeroboam,
    one_shot_client: FlaskClient,
):
    """GIVEN an endpoint with an exotic HTTP verb and no status_code defined
    WHEN registered
    THEN no User Warning is raised
    """
    with warnings.catch_warnings():
        warnings.simplefilter("error")

        @one_shot_app.get(
            "/exotic_http_verb_dont_raise_a_warning",
            response_model=SimpleModelOut,
            status_code=200,
        )
        def exotic_http_verb():
            return valid_outbound_data

    response = one_shot_client.get("/exotic_http_verb_dont_raise_a_warning")

    assert response.status_code == 200
