"""Configuration File for pytest."""
import json
import os

import pytest
from flask import Response
from pydantic import BaseModel

from flask_jeroboam.jeroboam import Jeroboam


@pytest.fixture
def app() -> Jeroboam:
    """A Basic Jeroboam Test App."""
    app = Jeroboam("jeroboam_test", root_path=os.path.dirname(__file__))
    app.config.update(
        TESTING=True,
        SECRET_KEY="RandomSecretKey",
    )
    return app


@pytest.fixture
def app_ctx(app: Jeroboam):
    """Application Context from the Test App."""
    with app.app_context() as ctx:
        yield ctx


@pytest.fixture
def request_context(app: Jeroboam):
    """Request Context from the Test App."""
    with app.test_request_context() as ctx:
        yield ctx


@pytest.fixture
def client(app: Jeroboam):
    """Test Client from the Test App."""
    return app.test_client()


@pytest.fixture(scope="session")
def reponse_model_test_class():
    """Basic Response Model."""

    class TestResponseModel(BaseModel):
        data_str: str
        data_int: int

    return TestResponseModel


@pytest.fixture(scope="session")
def inbound_model_test_class():
    """Basic Response Model."""

    class InBoundModel(BaseModel):
        data_str: str
        data_int: int

    return InBoundModel


@pytest.fixture(scope="session")
def valid_inbound_dict():
    """Basic Inbound Dictionnary."""
    return {"data_str": "test", "data_int": 1}


@pytest.fixture(scope="session")
def dict_endpoint(valid_inbound_dict):
    """Endpoint-Like function returning a dict."""

    def endpoint():
        return valid_inbound_dict

    return endpoint


@pytest.fixture(scope="session")
def model_endpoint(reponse_model_test_class, valid_inbound_dict):
    """Endpoint-Like function returning a Pydantic Model."""

    def endpoint():
        return reponse_model_test_class(**valid_inbound_dict)

    return endpoint


@pytest.fixture(scope="session")
def response_endpoint():
    """Endpoint-Like function returning a Flask Response."""

    def endpoint():
        return Response(
            json.dumps({"emails": "test"}),
            mimetype="application/json",
            status=200,
        )

    return endpoint


@pytest.fixture(scope="session")
def endpoint_with_params(inbound_model_test_class):
    """Endpoint-Like function returning a Flask Response."""

    def endpoint(id: int, other_param: str, query: inbound_model_test_class):
        return query

    return endpoint


@pytest.fixture(scope="session")
def endpoint_with_simple_annotations(inbound_model_test_class):
    """Endpoint-Like function returning a Flask Response."""

    def endpoint(id: int, other_param: str):
        return {"id": id, "other_param": other_param}

    return endpoint
