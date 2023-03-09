"""Testing Error Handling."""
from flask.testing import FlaskClient

from flask_jeroboam.jeroboam import Jeroboam


def test_invalid_request(
    client: FlaskClient,
):
    """GIVEN a view function
    WHEN it raises a ResponseValidationError
    THEN I get a 400 response with message details
    """
    response = client.get("/invalid_request")
    assert response.status_code == 400
    assert response.json == {
        "detail": [
            {
                "loc": ["query", "missing_param"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    }


def test_ressource_not_found(
    client: FlaskClient,
):
    """GIVEN a decorated view function
    WHEN it raises a Generic ResssourceNotFound
    THEN I get a 404 response with RessourceNotFound Generic Message
    """
    response = client.get("/ressource_not_found")
    assert response.status_code == 404
    assert response.data.startswith(b"RessourceNotFound: TestRessource not found :")


def test_generic_ressource_not_found_message(
    client: FlaskClient,
):
    """GIVEN a decorated view function
    WHEN it raises a ResssourceNotFound
    THEN I get a 404 response with RessourceNotFound Generic Message
    """
    response = client.get("/generic_ressource")
    assert response.status_code == 404
    assert response.data.startswith(b"RessourceNotFound: My Message")


def test_internal_server_error(
    client: FlaskClient,
):
    """GIVEN a decorated view function
    WHEN it raises a ServerError
    THEN I get a 500 response with ServerError Message
    """
    response = client.get("/server_error")
    assert response.status_code == 500
    assert response.data.startswith(b"InternalServerError: My Message")


def test_opt_out_registering():
    """GIVEN a decorated view function
    WHEN it raises a ServerError
    THEN I get a 500 response with ServerError Message
    """
    app = Jeroboam(__name__)
    app.config["JEROBOAM_REGISTER_ERROR_HANDLERS"] = False
    app.init_app()

    @app.route("/will_raise_an_error")
    def server_error(failing_argument: int):
        return {"message": "Will not Return"}

    client = app.test_client()
    response = client.get("/will_raise_an_error?failing_argument=not_an_int")
    assert response.status_code == 400
    assert response.data.startswith(
        b"<!doctype html>\n<html lang=en>\n<title>400 Bad Request"
    )
