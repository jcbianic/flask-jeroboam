from flask.testing import FlaskClient


def test_valid_payload_in_data_is_injected(
    client: FlaskClient,
):
    """GIVEN a POST endpoint with a BaseModel FormParam
    WHEN hit with a valid json payload
    THEN the parsed input is injected into the view function.
    """
    response = client.post("/form/base_model", data={"page": 1, "type": "item"})

    assert response.json == {"page": 1, "type": "item"}
    assert response.status_code == 201
