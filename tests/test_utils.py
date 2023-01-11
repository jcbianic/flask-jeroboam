"""Testing Utils."""
from typing import List

from flask.testing import FlaskClient
from pydantic import Field

from flask_jeroboam.jeroboam import Jeroboam
from flask_jeroboam.models import Parser
from flask_jeroboam.models import Serializer


def test_pascal_case_in_and_out_snake_case(app: Jeroboam, client: FlaskClient):
    """GIVEN an endpoint with param typed with a Parser and response_model a Serializer
    WHEN payload is send in pascalCase
    THEN it lives in python in snake_case and send back in pascalCase
    """

    class OutboundModel(Serializer):
        page: int
        per_page: int
        ids: List[int]

    class InboundModel(Parser):
        page: int
        per_page: int
        ids: List[int] = Field(alias="id[]")

    @app.get("/web_boundaries", response_model=OutboundModel)
    def read_items(payload: InboundModel):
        return {"page": payload.page, "per_page": payload.per_page, "ids": payload.ids}

    r = client.get("web_boundaries?page=1&perPage=10&id[]=1&id[]=2")

    assert r.status_code == 200
    assert r.data == b'{"page": 1, "perPage": 10, "ids": [1, 2]}'
