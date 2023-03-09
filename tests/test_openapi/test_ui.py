from flask_jeroboam.jeroboam import Jeroboam


def test_ui(client):
    """Test info endpoint."""
    response = client.get("/docs")
    assert response.status_code == 200
    assert response.data.startswith(b"<!DOCTYPE html>")


def test_opt_out_registering():
    """GIVEN a decorated view function
    WHEN it raises a ServerError
    THEN I get a 500 response with ServerError Message
    """
    app = Jeroboam(__name__)
    app.config["JEROBOAM_REGISTER_OPENAPI"] = False
    app.init_app()

    client = app.test_client()
    response = client.get("/docs")
    assert response.status_code == 404
