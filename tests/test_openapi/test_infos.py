"""Test OpenAPI infos."""


def test_info(client):
    """Test info endpoint."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json["info"] == {
        "contact": {
            "email": "jc.bianic@gmail.com",
            "name": "Jean-Christophe Bianic",
        },
        "description": "This application is here to test Jeroboam OpenAPI features.",
        "license": {"name": "MIT", "url": "http://opensource.org/licenses/MIT"},
        "termsOfService": "http://example.com/terms/",
        "title": "Jeroboam Test App",
        "version": "0.1.0",
    }
