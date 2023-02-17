def test_ui(client):
    """Test info endpoint."""
    response = client.get("/docs")
    assert response.status_code == 200
    assert response.data.startswith(b"<!DOCTYPE html>")
