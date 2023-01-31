"""Testing Error Handling.
We test for both Exception Initialisation and Error Handling.
"""
from flask.testing import FlaskClient

from flask_jeroboam.exceptions import RessourceNotFound
from flask_jeroboam.exceptions import ServerError
from flask_jeroboam.jeroboam import Jeroboam


def test_invalid_request(
    app: Jeroboam,
    client: FlaskClient,
):
    """GIVEN an endpoint
    WHEN it raises a InvalidRequest
    THEN I get a 404 with InvalidRequest Message
    """

    @app.get("/invalid_request")
    def ping(missing_param: int):
        return {}

    r = client.get("invalid_request")

    assert r.status_code == 400
    assert r.json == {
        "detail": [
            {
                "loc": ["query", "missing_param"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    }


def test_ressource_not_found_named_ressource(
    app: Jeroboam,
    client: FlaskClient,
):
    """GIVEN an endpoint
    WHEN it raises a ResssourceNotFound
    THEN I get a 404 with RessourceNotFound Message
    """

    @app.get("/ressource_not_found")
    def ping():
        raise RessourceNotFound(ressource_name="TestRessource", context=f"with id {id}")

    r = client.get("/ressource_not_found")

    assert r.status_code == 404
    assert r.data.startswith(b"RessourceNotFound: TestRessource not found :")


def test_ressource_not_found_generic_message(
    app: Jeroboam,
    client: FlaskClient,
):
    """GIVEN an endpoint
    WHEN it raises a ResssourceNotFound
    THEN I get a 404 with RessourceNotFound Generic Message
    """

    @app.get("/generic_ressource")
    def generic_ressource():
        raise RessourceNotFound(msg="My Message")

    r = client.get("/generic_ressource")

    assert r.status_code == 404
    assert r.data.startswith(b"RessourceNotFound: My Message")


def test_internal_server_error(
    app: Jeroboam,
    client: FlaskClient,
):
    """GIVEN an endpoint
    WHEN it raises a InternalServerError
    THEN I get a 500 with RessourceNotFound Generic Message
    """

    @app.get("/server_error")
    def ping():
        raise ServerError(msg="My Message", error=Exception(), trace="FakeTrace")

    r = client.get("/server_error")

    assert r.status_code == 500
    assert r.data.startswith(b"InternalServerError: My Message")
