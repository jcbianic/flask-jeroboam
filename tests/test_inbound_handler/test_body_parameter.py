from typing import List

import pytest

from flask_jeroboam.models import InboundModel
from flask_jeroboam.view_params.functions import Body


response_not_valid_int = {
    "detail": [
        {
            "loc": ["body", "payload"],
            "msg": "value is not a valid integer",
            "type": "type_error.integer",
        }
    ]
}


def _valid(value) -> dict:
    """Valid function."""
    return {"payload": value}


@pytest.mark.parametrize(
    "url,body_value,expected_status,expected_response",
    [
        ("/body/str", {"payload": "foobar"}, 201, _valid("foobar")),
        ("/body/int", {"payload": 123}, 201, _valid(123)),
        ("/body/int", {"payload": "not_a_valid_int"}, 400, response_not_valid_int),
        (
            "/body/base_model",
            {"page": 1, "type": "item"},
            201,
            {"page": 1, "type": "item"},
        ),
    ],
)
def test_post_body_operations(
    client, url, body_value, expected_status, expected_response
):
    """Testing Various GET operations with query parameters.

    GIVEN a GET endpoint configiured with query parameters
    WHEN a request is made to the endpoint
    THEN the request is parsed and validated accordingly
    """
    response = client.post(url, json=body_value)
    assert response.json == expected_response
    assert response.status_code == expected_status


def test_post_body_list_of_base_model(app, client):
    """Test Body Parameter with POST method."""

    class InBound(InboundModel):
        """Inbound model."""

        item: str
        count: int

    @app.post("/body/list_non_scalar", response_model=List[InBound])
    def post_body_list_non_scalar(payload: List[InBound] = Body(embed=False)):
        return payload

    response = client.post(
        "/body/list_non_scalar",
        json=[{"item": "foobar", "count": 1}, {"item": "bar", "count": 3}],
    )
    assert response.json == [
        {"item": "foobar", "count": 1},
        {"item": "bar", "count": 3},
    ]
    assert response.status_code == 201
