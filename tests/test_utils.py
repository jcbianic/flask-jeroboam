"""Testing Utils."""

from functools import partial
from typing import Optional, Union

import pytest
from flask.testing import FlaskClient
from pydantic import BaseModel, ValidationError
from pydantic_core import PydanticUndefined

from flask_jeroboam import Body
from flask_jeroboam._outboundhandler import OutboundHandler
from flask_jeroboam._utils import _rename_query_params_keys, is_sequence_field
from flask_jeroboam.datastructures import UploadFile
from flask_jeroboam.jeroboam import Jeroboam
from flask_jeroboam._utils import _unwrap_optional as _unwrap_optional_annotation
from flask_jeroboam.view_arguments.arguments import (
    ArgumentLocation,
    BodyArgument,
    FormArgument,
    QueryArgument,
)
from flask_jeroboam.view_arguments.solved import SolvedArgument, _unwrap_optional
from tests.app_test.models.inbound import ModelWithListIn
from tests.app_test.models.outbound import ModelWithListOut


def test_pascal_case_in_and_out_snake_case(
    one_shot_app: Jeroboam, one_shot_client: FlaskClient
):
    """GIVEN an endpoint with param typed with a Parser and response_model a Serializer
    WHEN payload is send in pascalCase
    THEN it lives in python in snake_case and send back in pascalCase
    """
    # We need to define the endpoint here to set the query_string_key_transformer first.
    one_shot_app.query_string_key_transformer = partial(
        _rename_query_params_keys, pattern=r"(.*)\[(.+)\]$"
    )

    @one_shot_app.get(
        "/query/special_pattern/after_configuration", response_model=ModelWithListOut
    )
    def read_items(payload: ModelWithListIn):
        return payload

    response = one_shot_client.get(
        "/query/special_pattern/after_configuration?page=1&perPage=10&id[]=1&id[]=2&order[name]=asc&order[age]=desc"
    )

    assert response.status_code == 200
    assert response.json == {
        "page": 1,
        "perPage": 10,
        "ids": [1, 2],
        "order": [{"name": "asc"}, {"age": "desc"}],
    }


def test_pascal_case_in_and_out_snake_case_without_transformer(
    one_shot_app: Jeroboam, one_shot_client: FlaskClient
):
    """GIVEN an endpoint with param typed with a Parser and response_model a Serializer
    WHEN payload is send in pascalCase
    THEN it lives in python in snake_case and send back in pascalCase
    """

    @one_shot_app.get(
        "/query/special_pattern/after_configuration", response_model=ModelWithListOut
    )
    def read_items(payload: ModelWithListIn):
        return payload

    response = one_shot_client.get(
        "/query/special_pattern?page=1&perPage=10&id[]=1&id[]=2&order[name]=asc&order[age]=desc"
    )

    assert response.status_code == 400
    errors = response.json.get("detail", [])
    assert len(errors) == 1
    # loc may use field name "order" (v2) or alias "order[]" (v1)
    assert any("order" in str(e.get("loc", "")) for e in errors)
    # msg may have "Value error, " prefix in v2
    assert any("Order must have at least 1 value" in e.get("msg", "") for e in errors)


def test_view_param_str_repr():
    """Test an internal function of ViewParameter."""
    param = Body("MyDefautValue")
    assert param.__repr__() == "BodyArgument(MyDefautValue)"


def test_solved_param_erroring():
    """Test an internal function of SolvedParameter."""
    param = Body("MyDefautValue")
    param.location = None
    solved_param = SolvedArgument(
        name="FaultySolvedParam", annotation=str, field_info=param
    )
    with pytest.raises(NotImplementedError):
        solved_param._get_values()


def test_file_upload():
    """Test UploadFile DataStructure raise an error if not a FileStorage."""

    class TestModel(BaseModel):
        file: UploadFile

    with pytest.raises(ValidationError):
        TestModel(file="BytesIO(b'Hello World !!')")  # type: ignore


def test_warn_on_two_identical_operation_id(one_shot_app: Jeroboam):
    """Test that a warning is raised when two identical operation_id are found."""
    app = Jeroboam(__name__)
    app.init_app()

    @app.get("/test")
    def test():
        pass

    @app.get("/test")
    def get_test():
        pass

    with pytest.warns(UserWarning):
        app.openapi  # type: ignore


# --- is_sequence_field ---


def test_is_sequence_field_with_no_annotation():
    """is_sequence_field returns False when the field has no annotation attribute."""
    from types import SimpleNamespace

    field = SimpleNamespace()  # no .annotation attribute
    assert is_sequence_field(field) is False


# --- ViewArgument.in_body ---


def test_in_body_true_for_body_argument():
    """BodyArgument.in_body is True."""
    assert BodyArgument().in_body is True


def test_in_body_true_for_form_argument():
    """FormArgument.in_body is True."""
    assert FormArgument().in_body is True


def test_in_body_false_for_query_argument():
    """QueryArgument.in_body is False."""
    assert QueryArgument().in_body is False


# --- SolvedArgument without field_info ---


def test_solved_argument_without_field_info():
    """SolvedArgument with field_info=None uses annotation directly (no Annotated wrapper)."""
    solved = SolvedArgument(name="x", annotation=str)
    assert solved.field_info is None
    # TypeAdapter should still work — no constraints to apply
    assert solved._type_adapter.validate_python("hello") == "hello"


# --- SolvedArgument.specialize with Ellipsis default ---


def test_specialize_normalises_ellipsis_default():
    """specialize() converts Ellipsis default to PydanticUndefined."""
    from types import SimpleNamespace

    view_param = SimpleNamespace(
        default=Ellipsis,
        location=ArgumentLocation.query,
        alias=None,
        embed=False,
        include_in_schema=True,
    )
    solved = SolvedArgument.specialize(name="x", annotation=str, view_param=view_param)
    assert solved.default is PydanticUndefined


# --- _unwrap_optional in solved.py ---


def test_unwrap_optional_with_typing_optional():
    """Optional[int] (= Union[int, None]) unwraps to int via the typing.Union path."""
    assert _unwrap_optional(Optional[int]) is int  # noqa: UP045


def test_unwrap_optional_with_multi_union():
    """Union[int, str, None] has two non-None members; returned unchanged."""
    result = _unwrap_optional(Union[int, str, None])  # noqa: UP007
    assert result == Union[int, str, None]  # noqa: UP007


def test_unwrap_optional_non_union():
    """Plain int is returned unchanged."""
    assert _unwrap_optional(int) is int


# --- _unwrap_optional in _utils.py ---


def test_unwrap_optional_annotation_with_typing_optional():
    """Optional[str] unwraps to str."""
    assert _unwrap_optional_annotation(Optional[str]) is str  # noqa: UP045


def test_unwrap_optional_annotation_with_multi_union():
    """Union[str, int, None] is returned unchanged (two non-None members)."""
    result = _unwrap_optional_annotation(Union[str, int, None])  # noqa: UP007
    assert result == Union[str, int, None]  # noqa: UP007


# --- OutboundHandler._adapt_datastructure_of with list ---


def test_adapt_datastructure_of_list():
    """A list of BaseModel instances is recursively adapted to a list of dicts."""

    class Item(BaseModel):
        name: str

    def view():
        pass

    handler = OutboundHandler(view, None, "GET", {})
    result = handler._adapt_datastructure_of([Item(name="a"), Item(name="b")])
    assert result == [{"name": "a"}, {"name": "b"}]
