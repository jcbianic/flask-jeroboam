"""Testing Utils."""
from functools import partial

import pytest
from flask.testing import FlaskClient

from flask_jeroboam import Body
from flask_jeroboam.jeroboam import Jeroboam
from flask_jeroboam.utils import _rename_query_params_keys
from flask_jeroboam.view_params.solved import SolvedParameter
from tests.app_test.models.inbound import ModelWithListIn
from tests.app_test.models.outbound import ModelWithListOut


def test_pascal_case_in_and_out_snake_case(app: Jeroboam, client: FlaskClient):
    """GIVEN an endpoint with param typed with a Parser and response_model a Serializer
    WHEN payload is send in pascalCase
    THEN it lives in python in snake_case and send back in pascalCase
    """
    # We need to define the endpoint here to set the query_string_key_transformer first.
    app.query_string_key_transformer = partial(
        _rename_query_params_keys, pattern=r"(.*)\[(.+)\]$"
    )

    @app.get(
        "/query/special_pattern/after_configuration", response_model=ModelWithListOut
    )
    def read_items(payload: ModelWithListIn):
        return payload

    response = client.get(
        "/query/special_pattern/after_configuration?page=1&perPage=10&id[]=1&id[]=2&order[name]=asc&order[age]=desc"
    )

    assert response.status_code == 200
    assert response.json == {
        "page": 1,
        "perPage": 10,
        "ids": [1, 2],
        "order": [{"name": "asc"}, {"age": "desc"}],
    }


def test_pascal_case_in_and_out_snake_case_without_transformer(client: FlaskClient):
    """GIVEN an endpoint with param typed with a Parser and response_model a Serializer
    WHEN payload is send in pascalCase
    THEN it lives in python in snake_case and send back in pascalCase
    """
    response = client.get(
        "/query/special_pattern?page=1&perPage=10&id[]=1&id[]=2&order[name]=asc&order[age]=desc"
    )

    assert response.status_code == 400
    assert response.json == {
        "detail": [
            {
                "loc": ["query", "payload", "order[]"],
                "msg": "Order must have at least 1 value",
                "type": "value_error",
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
