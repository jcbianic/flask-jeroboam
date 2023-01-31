import pytest


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
        ("/query/frozenset/?query=1&query=1&query=2", 200, _valid("1,2")),
    ],
)
def test_get_query_operations(query_client, url, expected_status, expected_response):
    """Testing Various GET operations with query parameters.

    GIVEN a GET endpoint configiured with query parameters
    WHEN a request is made to the endpoint
    THEN the request is parsed and validated accordingly
    """
    response = query_client.get(url)
    assert response.status_code == expected_status
    assert response.json == expected_response
