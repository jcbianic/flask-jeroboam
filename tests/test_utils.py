"""Testing Utils."""
from functools import partial
from typing import List

import pytest
from flask.testing import FlaskClient
from pydantic import Field

from flask_jeroboam import Body
from flask_jeroboam.jeroboam import Jeroboam
from flask_jeroboam.models import Parser
from flask_jeroboam.models import Serializer
from flask_jeroboam.utils import _rename_query_params_keys
from flask_jeroboam.view_params.solved import SolvedParameter


def test_pascal_case_in_and_out_snake_case(app: Jeroboam, client: FlaskClient):
    """GIVEN an endpoint with param typed with a Parser and response_model a Serializer
    WHEN payload is send in pascalCase
    THEN it lives in python in snake_case and send back in pascalCase
    """

    class OutboundModel(Serializer):
        page: int
        per_page: int
        ids: List[int]
        order: List[dict]

    class InboundModel(Parser):
        page: int
        per_page: int
        ids: List[int] = Field(alias="id[]")
        order: List[dict] = Field(alias="order[]")

    app.query_string_key_transformer = partial(
        _rename_query_params_keys, pattern=r"(.*)\[(.+)\]$"
    )

    @app.get("/web_boundaries", response_model=OutboundModel)
    def read_items(payload: InboundModel):
        return payload

    r = client.get(
        "web_boundaries?page=1&perPage=10&id[]=1&id[]=2&order[name]=asc&order[age]=desc"
    )

    assert r.status_code == 200
    assert r.json == {
        "page": 1,
        "perPage": 10,
        "ids": [1, 2],
        "order": [{"name": "asc"}, {"age": "desc"}],
    }


def test_pascal_case_in_and_out_snake_case_without_transformer(
    app: Jeroboam, client: FlaskClient
):
    """GIVEN an endpoint with param typed with a Parser and response_model a Serializer
    WHEN payload is send in pascalCase
    THEN it lives in python in snake_case and send back in pascalCase
    """

    class OutboundModel(Serializer):
        page: int
        per_page: int
        ids: List[int]
        order: List[dict]

    class InboundModel(Parser):
        page: int
        per_page: int
        ids: List[int] = Field(alias="id[]")
        order: List[dict] = Field(alias="order[]")

    @app.get("/web_boundaries", response_model=OutboundModel)
    def read_items(payload: InboundModel):
        return payload

    r = client.get(
        "web_boundaries?page=1&perPage=10&id[]=1&id[]=2&order[name]=asc&order[age]=desc"
    )

    assert r.status_code == 400
    assert r.json == {
        "detail": [
            {
                "loc": ["query", "payload", "order[]"],
                "msg": "none is not an allowed value",
                "type": "type_error.none.not_allowed",
            }
        ]
    }


def test_view_param_str_repr():
    """Test an internal function of ViewParameter."""
    param = Body("MyDefautValue")
    assert param.__repr__() == "BodyParameter(MyDefautValue)"


def test_solved_param_erroring():
    """Test an internal function of SolvedParameter."""
    param = Body("MyDefautValue")
    param.location = None
    solved_param = SolvedParameter(
        name="FaultySolvedParam", type_=str, view_param=param
    )
    with pytest.raises(ValueError):
        solved_param._get_values()
