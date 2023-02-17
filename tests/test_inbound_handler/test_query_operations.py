import pytest
from flask.testing import FlaskClient

from tests.app_test.models.inbound import OptionalModelIn


response_missing = {
    "detail": [
        {
            "loc": ["query", "query"],
            "msg": "field required",
            "type": "value_error.missing",
        }
    ]
}

response_not_valid_int = {
    "detail": [
        {
            "loc": ["query", "query"],
            "msg": "value is not a valid integer",
            "type": "type_error.integer",
        }
    ]
}


def _valid(value) -> dict:
    """Valid function."""
    return {"query": value}


@pytest.mark.parametrize(
    "url,expected_status,expected_response",
    [
        ("/query", 400, response_missing),
        ("/query?query=baz", 200, _valid("baz")),
        ("/query?not_declared=baz", 400, response_missing),
        ("/query/optional", 200, _valid(None)),
        ("/query/optional?query=baz", 200, _valid("baz")),
        ("/query/optional?not_declared=baz", 200, _valid(None)),
        ("/query/int", 400, response_missing),
        ("/query/int?query=42", 200, _valid(42)),
        ("/query/int?query=42.5", 400, response_not_valid_int),
        ("/query/int?query=baz", 400, response_not_valid_int),
        ("/query/int?not_declared=baz", 400, response_missing),
        ("/query/int/optional", 200, _valid(None)),
        ("/query/int/optional?query=50", 200, _valid(50)),
        ("/query/int/optional?query=foo", 400, response_not_valid_int),
        ("/query/int/default", 200, _valid(10)),
        ("/query/int/default?query=50", 200, _valid(50)),
        ("/query/int/default?query=foo", 400, response_not_valid_int),
        ("/query/param", 200, _valid(None)),
        ("/query/param?query=50", 200, _valid("50")),
        ("/query/param-required", 400, response_missing),
        ("/query/param-required?query=50", 200, _valid("50")),
        ("/query/param-required/int", 400, response_missing),
        ("/query/param-required/int?query=50", 200, _valid(50)),
        ("/query/param-required/int?query=foo", 400, response_not_valid_int),
        ("/query/frozenset?query=1&query=1&query=2", 200, _valid("1,2")),
    ],
)
def test_get_query_operations(client, url, expected_status, expected_response):
    """Testing Various GET operations with query parameters.

    GIVEN a GET endpoint configiured with query parameters
    WHEN a request is made to the endpoint
    THEN the request is parsed and validated accordingly
    """
    response = client.get(url)
    assert response.json == expected_response
    assert response.status_code == expected_status


def test_valid_base_model_as_query_parameter(
    client: FlaskClient,
):
    """GIVEN a GET endpoint with a BaseModel as QueryParam
    WHEN hit with a valid query string
    THEN the parsed input is injected into the view function.
    """
    response = client.get("/query/base_model?page=1&type=item")
    assert response.status_code == 200
    assert response.json == {"page": 1, "type": "item"}


def test_valid_base_model_as_forwarded_query_parameter(
    client: FlaskClient,
):
    """GIVEN a GET endpoint with a BaseModel as Forward Ref QueryParam
    WHEN hit with a valid query string
    THEN the parsed input is injected into the view function.
    """
    response = client.get("/query/base_model/forward_ref?page=1&type=item")
    assert response.status_code == 200
    assert response.json == {"page": 1, "type": "item"}


def test_invalid_query_string_raise_400(
    client: FlaskClient,
):
    """GIVEN a GET endpoint with properly annotated argument
    WHEN hit with invalid queryString
    THEN the endpoint raise a 400 InvalidRequest Error
    """
    response = client.get("/query/base_model?page=not_a_valid_param")
    assert response.status_code == 400
    assert response.json == {
        "detail": [
            {
                "loc": ["query", "payload", "page"],
                "msg": "value is not a valid integer",
                "type": "type_error.integer",
            },
            {
                "loc": ["query", "payload", "type"],
                "msg": "none is not an allowed value",
                "type": "type_error.none.not_allowed",
            },
        ]
    }


def test_query_string_for_list_arguments(
    client: FlaskClient,
):
    """GIVEN a GET endpoint with list arguments
    WHEN hit with proper formatted queryString
    THEN the arguments get injected into a Array
    """
    response = client.get("/query/list_of_strings?id[]=1&id[]=2")
    assert response.json == {"id": [1, 2]}
    assert response.status_code == 200


def test_query_optionnal_base_model(
    client: FlaskClient,
):
    """GIVEN an endpoint with Optionnal typed argument with Optional fields
    WHEN hit with an empty querystring
    THEN the endpoint is properly executed
    """
    response = client.get("/query/optional_model")
    assert response.status_code == 200
    assert response.json == OptionalModelIn(**{}).dict()
