import pytest


"""Testing the inbound feature doc Page."""
from docs_src.features.inbound import app


@pytest.fixture()
def client():
    """A Test Client for the app."""
    return app.test_client()


def test_implicit_location_on_get(client):
    """Test the implicit location GET example."""
    response = client.get("/implicit_location_is_query_string?page=42")
    assert response.data == b"Received Page Argument is : 42"
    assert response.status_code == 200


def test_implicit_location_on_post(client):
    """Test the implicit location POTS example."""
    response = client.post("/implicit_location_is_body", json={"page": 42})
    assert response.data == b"Received Page Argument is : 42"

    assert response.status_code == 201


def test_implicit_path_parameter(client):
    """Test the implicit path parameter example."""
    response = client.get("/item/42/implicit")
    assert response.data == b"Received id Argument is : 42"
    assert response.status_code == 200


def test_implicit_post_path_parameter(client):
    """Test the implicit path parameter example."""
    response = client.post("/item/42/implicit")
    assert response.data == b"Received id Argument is : 42"
    assert response.status_code == 201


def test_explicit_location_on_get(client):
    """Test the explicit location GET example."""
    response = client.get("/explicit_location_is_query_string?page=42")
    assert response.data == b"Received Page Argument is : 42"
    assert response.status_code == 200


def test_explicit_location_on_post(client):
    """Test the explicit location GET example."""
    response = client.post("/explicit_location_is_body", json={"page": 42})
    assert response.data == b"Received Page Argument is : 42"
    assert response.status_code == 201


def test_explicit_cookie_location_with_other_explicit(client):
    """Test the explicit location GET example."""
    client.set_cookie("username", "john")
    response = client.get(
        "/explicit_location_is_query_string_and_cookie?page=42",
    )
    assert response.data == b"Received Page Argument is : 42. Username is : john"
    assert response.status_code == 200


def test_explicit_cookie_location_with_other_implicit(client):
    """Test the explicit location GET example."""
    client.set_cookie("username", "john")
    response = client.get(
        "/implicit_and_explicit?page=42",
    )
    assert response.data == b"Received Page Argument is : 42. Username is : john"
    assert response.status_code == 200


def test_argument_is_required(client):
    """Test the explicit location GET example."""
    client.set_cookie("username", "john")
    response = client.get(
        "implicit_location_is_query_string",
    )
    assert response.json == {
        "detail": [
            {
                "loc": ["query", "page"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    }
    assert response.status_code == 400


def test_implicit_default_values(client):
    """Test default values with implicit-location."""
    response = client.get(
        "implicit_location_with_default_value",
    )
    assert response.data == b"Received Page Argument is : 1"
    assert response.status_code == 200


def test_explicit_default_values(client):
    """Test default values with implicit-location."""
    response = client.get(
        "explicit_location_with_default_value",
    )
    assert response.data == b"Received Page Argument is : 1"
    assert response.status_code == 200


def test_implicit_default_values_get_injected(client):
    """Test default values with implicit-location."""
    response = client.get(
        "implicit_location_with_default_value?page=42",
    )
    assert response.data == b"Received Page Argument is : 42"
    assert response.status_code == 200


def test_explicit_default_values_get_injected(client):
    """Test default values with implicit-location."""
    response = client.get(
        "explicit_location_with_default_value?page=42",
    )
    assert response.data == b"Received Page Argument is : 42"
    assert response.status_code == 200


def test_various_type_definition(client):
    """Test default values with implicit-location."""
    response = client.get(
        "defining_type_with_type_hints?page=42&search=foo&search=bar&price=42.42&name=test&count=3",
    )
    assert response.data == (
        b"Received arguments are :\n"
        b"page : 42\n"
        b"search : ['foo', 'bar']\n"
        b"price : 42.42\n"
        b"item : name='test' count=3"
    )
    assert response.status_code == 200


def test_validation_option(client):
    """Test default values with implicit-location."""
    response = client.get("argument_with_validation?page=0")
    assert response.json == {
        "detail": [
            {
                "ctx": {"limit_value": 1},
                "loc": ["query", "page"],
                "msg": "ensure this value is greater than or equal to 1",
                "type": "value_error.number.not_ge",
            }
        ]
    }
    assert response.status_code == 400
