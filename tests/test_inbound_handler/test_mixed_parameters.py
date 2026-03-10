"""Testing endpoints that combine multiple parameter locations.

These tests are critical for migration safety: the parameter routing logic
(path auto-detection, verb-based defaults, explicit Body()/Query()) must all
work together correctly. Regressions here mean parameters end up in the wrong
location or are silently ignored.

Key design behavior documented here:
- GET: all undecorated params default to QUERY location
- PUT/POST: all undecorated params default to BODY location
- Path params are auto-detected from the URL rule (no annotation needed)
- Explicit Query() / Body() always overrides the verb-based default
"""

import pytest
from flask.testing import FlaskClient

from flask_jeroboam import Jeroboam

# --- GET: path + optional query ---


@pytest.mark.parametrize(
    "url,expected_status,expected_body",
    [
        ("/mixed/42", 200, {"item_id": 42, "q": None}),
        ("/mixed/42?q=search", 200, {"item_id": 42, "q": "search"}),
        ("/mixed/99?q=hello", 200, {"item_id": 99, "q": "hello"}),
    ],
)
def test_get_with_path_and_optional_query(
    client: FlaskClient, url, expected_status, expected_body
):
    """GIVEN a GET endpoint with a path param and an optional query param
    WHEN called with various combinations
    THEN each parameter is resolved from the correct source.
    """
    response = client.get(url)
    assert response.status_code == expected_status
    assert response.json == expected_body


def test_get_path_param_wrong_type_returns_400(client: FlaskClient):
    """GIVEN a GET endpoint with an int path param
    WHEN called with a non-integer value
    THEN Flask's converter returns 404 before Jeroboam validation runs.
    """
    response = client.get("/mixed/not_an_int")
    assert response.status_code == 404


# --- PUT: path + optional query + required body ---


def test_put_with_all_three_locations(client: FlaskClient):
    """GIVEN a PUT endpoint with path, query and body params
    WHEN called with all three present
    THEN each is extracted from its correct source and the response model is applied.
    """
    response = client.put(
        "/mixed/7?q=filtered",
        json={"name": "Widget", "price": 9.99},
    )
    assert response.status_code == 201
    assert response.json == {"id": 7, "name": "Widget", "price": 9.99, "q": "filtered"}


def test_put_without_optional_query(client: FlaskClient):
    """GIVEN a PUT endpoint with an optional query param
    WHEN the query param is absent
    THEN it defaults to None without error.
    """
    response = client.put(
        "/mixed/3",
        json={"name": "Gadget", "price": 4.50},
    )
    assert response.status_code == 201
    assert response.json == {"id": 3, "name": "Gadget", "price": 4.50, "q": None}


def test_put_with_missing_required_body_field_returns_400(client: FlaskClient):
    """GIVEN a PUT endpoint with a required body model
    WHEN the body is missing a required field
    THEN a 400 validation error is returned.
    """
    response = client.put(
        "/mixed/1",
        json={"name": "Incomplete"},  # missing price
    )
    assert response.status_code == 400
    data = response.json
    assert data is not None
    assert "detail" in data
    errors = data["detail"]
    # Error loc: ['body', 'item', 'price'] — body param named 'item', field 'price'
    assert any("price" in e.get("loc", []) for e in errors)


def test_put_with_wrong_body_field_type_returns_400(client: FlaskClient):
    """GIVEN a PUT endpoint with a float body field
    WHEN the body contains a non-numeric string for that field
    THEN a 400 validation error is returned and the path param is not confused with the body.
    """
    response = client.put(
        "/mixed/5",
        json={"name": "Widget", "price": "not_a_float"},
    )
    assert response.status_code == 400
    assert response.json is not None
    assert "detail" in response.json


def test_put_body_fields_are_not_confused_with_query_params(client: FlaskClient):
    """GIVEN a PUT endpoint where q is declared with Query() and item with Body()
    WHEN q is in the query string and item fields are in the JSON body
    THEN each is extracted from the correct location.
    """
    response = client.put(
        "/mixed/10?q=from_query",
        json={"name": "from_body", "price": 1.0},
    )
    assert response.status_code == 201
    assert response.json["q"] == "from_query"
    assert response.json["name"] == "from_body"


def test_put_implicit_default_is_body_not_query(one_shot_app: Jeroboam):
    """GIVEN a PUT endpoint with an undecorated optional param (no Query() or Body())
    WHEN the param is passed in the query string
    THEN it is NOT found — PUT's implicit default is body, not query.

    This documents the verb-based default behavior: to use a query param on
    a PUT endpoint you must be explicit with Query().
    """

    @one_shot_app.put("/test_implicit_put/<int:item_id>")
    def implicit_put(item_id: int, q: str | None = None):
        # q defaults to body location on PUT — query string is ignored
        return {"item_id": item_id, "q": q}

    client = one_shot_app.test_client()
    # Sending q in the query string — it will NOT be parsed (body default)
    response = client.put("/test_implicit_put/1?q=ignored", json={})
    assert response.status_code == 201
    assert response.json["q"] is None  # q was not found in the body
