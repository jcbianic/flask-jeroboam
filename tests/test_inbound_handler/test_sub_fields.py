from typing import Optional

from flask.testing import FlaskClient
from pydantic import BaseModel
from pydantic import validator

from flask_jeroboam.jeroboam import Jeroboam


class ModelB(BaseModel):
    username: str


class ModelC(ModelB):
    password: str


class ModelA(BaseModel):
    name: str
    description: Optional[str] = None
    model_b: ModelB

    @validator("name")
    def lower_username(cls, name: str, values):  # noqa: B902, N805
        """Validate that the name ends in A."""
        if not name.endswith("A"):
            raise ValueError("name must end in A")
        return name


def test_get_query_operations(one_shot_app: Jeroboam, one_shot_client: FlaskClient):
    """Testing Various GET operations with query parameters.

    GIVEN a GET endpoint configiured with query parameters
    WHEN a request is made to the endpoint
    THEN the request is parsed and validated accordingly
    """

    @one_shot_app.post("/sub_model", response_model=ModelA)
    def post_sub_model(model: ModelA):
        return model

    response = one_shot_client.post(
        "/sub_model", json={"name": "fooA", "model_b": {"username": "bar"}}
    )
    assert response.status_code == 201
    assert response.json == {
        "name": "fooA",
        "model_b": {"username": "bar"},
        "description": None,
    }
