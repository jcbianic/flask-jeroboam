"""Testing for the Parser decorator factory."""
from unittest.mock import create_autospec
from unittest.mock import patch

import pytest
from flask.testing import FlaskClient
from pydantic import BaseModel

from flask_jeroboam._parser import _parse_input
from flask_jeroboam.exceptions import InvalidRequest
from flask_jeroboam.jeroboam import Jeroboam


def test_parser_parse_valid_object(inbound_model_test_class, valid_inbound_dict):
    """Parser should be able to parse a valid dictionnary."""
    parsed_input = _parse_input(inbound_model_test_class, **valid_inbound_dict)

    assert isinstance(parsed_input, inbound_model_test_class)
    assert parsed_input.data_str == valid_inbound_dict["data_str"]
    assert parsed_input.data_int == valid_inbound_dict["data_int"]


def test_parser_raise_exception_on_invalid_object(inbound_model_test_class):
    """Parser should raise and exception when parsing an invalid object."""
    with pytest.raises(InvalidRequest) as _:
        _parse_input(inbound_model_test_class, **{"other_thing": "test"})


def test_decorator_parse_query_string_and_inject_into_view(
    app, client, valid_inbound_dict
):
    """Parser Decorator injects the parsed input into the view function."""

    class InBoundModel(BaseModel):
        data_str: str
        data_int: int

    @app.get("/<int:_id>")
    def _endpoint(_id: int, query: InBoundModel):
        return query.json()

    data = client.get("/1", query_string=valid_inbound_dict).data

    assert data == b'{"data_str": "test", "data_int": 1}'


def test_decorator_parse_data_payload_and_inject_into_view(
    app: Jeroboam,
    client: FlaskClient,
    valid_inbound_dict,
):
    """GIVEN a post endpoint with an argument annotated as Pydantic Model
    WHEN Called with a valid data payload
    THEN the parsed input is injected into the view function.
    """

    class InBoundModel(BaseModel):
        data_str: str
        data_int: int

    @app.post("/<int:_id>")
    def _endpoint(_id: int, payload: InBoundModel):
        return payload.json()

    data = client.post("/1", data=valid_inbound_dict).data

    assert data == b'{"data_str": "test", "data_int": 1}'


def test_decorator_parse_json_payload_and_inject_into_view(
    app: Jeroboam,
    client: FlaskClient,
    valid_inbound_dict,
):
    """GIVEN a post endpoint with an argument annotated as Pydantic Model
    WHEN Called with a valid json payload
    THEN the parsed input is injected into the view function.
    """

    class InBoundModel(BaseModel):
        data_str: str
        data_int: int

    @app.post("/<int:_id>")
    def _endpoint(_id: int, payload: InBoundModel):
        return payload.json()

    assert (
        client.post("/1", json=valid_inbound_dict, content_type="application/json").data
        == b'{"data_str": "test", "data_int": 1}'
    )


def test_decorator_parse_with_unsupported_method(
    valid_inbound_dict, endpoint_with_params
):
    """Parser Decorator injects the parsed input into the view function."""
    mock_endpoint = create_autospec(
        endpoint_with_params, return_value=valid_inbound_dict
    )
    mock_endpoint.__annotations__ = endpoint_with_params.__annotations__


def test_decorator_parse_with_unsuported_annotation(
    app: Jeroboam, client: FlaskClient, request_context
):
    """GIVEN a post endpoint without any argument annotated as Pydantic Model
    WHEN Called
    THEN the request object is not parsed whatsoever.
    """

    @app.get("/<int:_id>/<other_param>")
    def _endpoint(_id: int, other_param: str):
        return {"id_": _id, "other_param": other_param}

    with request_context:
        mock_request = patch("flask_jeroboam._parser.request").start()

    assert client.get("/1/test").data == b'{"id_":1,"other_param":"test"}\n'
    mock_request.assert_not_called()
