def test_text_get(client):
    """Test GET /text"""
    response = client.get("/text")
    assert response.status_code == 200, response.text
    assert response.data == b"Hello World"


def test_nonexistent(client):
    """Test GET /nonexistent"""
    response = client.get("/nonexistent")
    assert response.status_code == 404, response.text
    assert response.json == {"message": "Not Found"}
