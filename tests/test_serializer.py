"""Testing for the Serilizer decorator factory."""
from unittest.mock import patch

import pytest
from flask import Response

from flask_jeroboam._serializer import _prepare_response
from flask_jeroboam._serializer import serializer
from flask_jeroboam.exceptions import ServerError


@patch("flask_jeroboam._serializer._prepare_response")
def test_serializer_init_response_object_from_dict(
    mock_prepare_response, reponse_model_test_class, dict_endpoint
):
    """GIVEN a decorated function with a serializer
    WHEN called
    THEN should call the _prepare_response function with
    the response_model as argument
    """
    decorator = serializer(response_model=reponse_model_test_class)
    decorator(dict_endpoint)()

    assert mock_prepare_response.is_called()
    assert mock_prepare_response.is_called_with(
        reponse_model_test_class(data_str="test", data_int=1)
    )


@patch("flask_jeroboam._serializer._prepare_response")
def test_serializer_pass_response_object(
    mock_prepare_response, reponse_model_test_class, model_endpoint
):
    """Decorated endpoint should return response_model Object when endpoint
    returns a valid dict.
    """
    decorator = serializer(response_model=reponse_model_test_class)
    decorator(model_endpoint)()

    assert mock_prepare_response.is_called()
    assert mock_prepare_response.is_called_with(
        reponse_model_test_class(data_str="test", data_int=1)
    )


@patch("flask_jeroboam._serializer._prepare_response")
def test_serializer_pass_flask_response(
    mock_prepare_response, reponse_model_test_class, response_endpoint
):
    """Decorated endpoint should pass a Response Object when
    endpoint returns one.
    """
    decorator = serializer(response_model=reponse_model_test_class)
    response = decorator(response_endpoint)()

    assert mock_prepare_response.is_not_called()
    assert isinstance(response, Response)
    assert isinstance(response_endpoint(), Response)
    assert str(response) == str(response_endpoint())


def test_prepare_response_with_valid_response(reponse_model_test_class):
    """Decorated endpoint should return response_model Object when
    endpoint returns a valid dict.
    """
    object = reponse_model_test_class(data_str="test", data_int=1)
    response = _prepare_response(object)

    assert isinstance(response, Response)
    assert response.status_code == 200
    assert response.mimetype == "application/json"
    assert response.data == b'{"data_str": "test", "data_int": 1}'


def test_prepare_response_with_invalid_response(reponse_model_test_class):
    """Decorated endpoint should return response_model Object when
    endpoint returns a valid dict.
    """
    object = {"test": 3}
    with pytest.raises(ServerError) as exc_info:
        _prepare_response(object)

    assert exc_info.type == ServerError
