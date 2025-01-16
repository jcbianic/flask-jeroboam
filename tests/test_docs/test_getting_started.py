"""Testing Examples from the Getting Started Page"""

from docs_src.getting_started_00 import app


def test_getting_started_00(app=app):
    """Test the first example from the Getting Started Page."""
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json == {"status": "Ok"}


def test_getting_started_01(app=app):
    """Test the second example from the Getting Started Page."""
    client = app.test_client()
    response = client.get("/query_string_arguments")
    assert response.status_code == 200
    assert response.json == {"page": 1, "per_page": 10}


def test_getting_started_02(app=app):
    """Test the third example from the Getting Started Page."""
    client = app.test_client()
    response = client.get("/query_string_arguments?page=2&per_page=50")
    assert response.status_code == 200
    assert response.json == {"page": 2, "per_page": 50}


def test_getting_started_03(app=app):
    """Test the fourth example from the Getting Started Page."""
    client = app.test_client()
    response = client.get("/query_string_arguments?page=not_a_int&per_page=50")
    assert response.status_code == 400
    assert response.json == {
        "detail": [
            {
                "loc": ["query", "page"],
                "msg": "value is not a valid integer",
                "type": "type_error.integer",
            }
        ]
    }


def test_getting_started_04(app=app):
    """Test the fifth example from the Getting Started Page."""
    client = app.test_client()
    response = client.get("/item")
    assert response.status_code == 200
    assert response.json == {"name": "Bottle", "price": 5.0, "count": 1}


def test_getting_started_05(app=app):
    """Test the sixth example from the Getting Started Page."""
    client = app.test_client()
    response = client.get("/docs")
    assert response.status_code == 200
    assert response.data.startswith(b"<!DOCTYPE html>")
