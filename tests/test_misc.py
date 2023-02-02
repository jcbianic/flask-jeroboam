"""Misc Testing for Flask-Jeroboam."""

from flask.testing import FlaskClient


def test_delete_method(client: FlaskClient):
    """GIIVEN an endpoint with a different verb than GET or POST
    WHEN hit
    THEN it works like a regular endpoint
    """
    response = client.delete("/delete")
    assert response.status_code == 204
    assert response.data == b""
