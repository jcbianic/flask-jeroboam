"""Testing the outbound feature page of our Documentation."""
import pytest

from docs_src.features.outbound import app


@pytest.fixture()
def client():
    """A Test Client for the app."""
    return app.test_client()


def test_explicit_response_model(client):
    """Test the implicit location GET example."""
    response = client.get("/tasks/42")

    assert response.status_code == 200
    assert response.json == {
        "id": 42,
        "name": "Find the answer.",
        "description": "Just here to make a point.",
    }


def test_dictionnary(client):
    """Test the implicit location GET example."""
    response = client.get("/tasks/42/no_response_model")

    assert response.status_code == 200
    assert response.json == {"id": 42, "name": "I'm from the dictionary."}


def test_implicit_response_model(client):
    """Test the implicit location GET example."""
    response = client.get("/tasks/42/implicit_from_annotation")

    assert response.status_code == 200
    assert response.json == {
        "id": 42,
        "name": "Implicit from Annotation",
        "description": "Just here to make a point.",
    }


def test_implicit_response_model_no_annotation(client):
    """Test the implicit location GET example."""
    response = client.get("/tasks/42/implicit_no_annotation")

    assert response.status_code == 500
    assert response.json == {
        "message": "Internal Error",
    }


def test_response_model_turned_off(client):
    """Test the implicit location GET example."""
    response = client.get("/tasks/42/response_model_off")

    assert response.status_code == 200
    assert response.json == {"id": 42, "name": "Response Model is off."}
