"""Testing Request Parsing Use Cases.
We test for various payload location (QueryString, Data, Json, Files),
verbs (GET, POST, DELETE) and configuration (Lists or Plain)...
"""
from io import BytesIO
from typing import Dict
from typing import List
from typing import Optional

from flask.testing import FlaskClient
from pydantic import BaseModel
from pydantic import Field
from werkzeug.datastructures import FileStorage

from flask_jeroboam.jeroboam import Jeroboam
from flask_jeroboam.models import Parser


class InBoundModel(BaseModel):
    """Base InboundModel for Testing Parsing Request."""

    page: int
    type: str


def test_valid_payload_in_query_string_is_injected(
    app: Jeroboam,
    client: FlaskClient,
):
    """GIVEN a GET endpoint with properly annotated argument
    WHEN hit with a valid query string
    THEN the parsed input is injected into the view function.
    """

    @app.get("/payload_in_query_string")
    def read_test(payload: InBoundModel):
        return payload.json()

    r = client.get("/payload_in_query_string?page=1&type=item")

    assert r.status_code == 200
    assert r.data == b'{"page": 1, "type": "item"}'


def test_forward_ref_in_query_string_is_injected(
    app: Jeroboam,
    client: FlaskClient,
):
    """GIVEN a GET endpoint with properly annotated  as forward ref
    WHEN hit with a valid query string
    THEN the parsed input is injected into the view function.
    """

    @app.get("/payload_in_query_string")
    def read_test(payload: "InBoundModel"):
        return payload.json()

    r = client.get("/payload_in_query_string?page=1&type=item")

    assert r.status_code == 200
    assert r.data == b'{"page": 1, "type": "item"}'


def test_valid_payload_in_json_is_injected(
    app: Jeroboam,
    client: FlaskClient,
):
    """GIVEN a POST endpoint with properly annotated argument
    WHEN hit with a valid json payload
    THEN the parsed input is injected into the view function.
    """

    @app.post("/payload_in_json")
    def read_test(payload: InBoundModel):
        return payload.json()

    r = client.post("/payload_in_json", json={"page": 1, "type": "item"})

    assert r.status_code == 200
    assert r.data == b'{"page": 1, "type": "item"}'


def test_valid_payload_in_data_is_injected(
    app: Jeroboam,
    client: FlaskClient,
):
    """GIVEN a POST endpoint with properly annotated argument
    WHEN hit with a valid data payload
    THEN the parsed input is injected into the view function.
    """

    @app.post("/payload_in_json")
    def read_test(payload: InBoundModel):
        return payload.json()

    r = client.post("/payload_in_json", data={"page": 1, "type": "item"})

    assert r.status_code == 200
    assert r.data == b'{"page": 1, "type": "item"}'


def test_valid_payload_in_files_is_injected(app: Jeroboam, client: FlaskClient):
    """GIVEN a POST endpoint with properly annotated argument
    WHEN hit with a valid files payload
    THEN the parsed input is injected into the view function.
    """

    class InBoundModelWithFile(BaseModel):
        type: str
        file: FileStorage

        class Config:
            arbitrary_types_allowed: bool = True

    @app.post("/payload_in_file")
    def ping(payload: InBoundModelWithFile):
        return {"type": payload.type, "file_content": str(payload.file.read())}

    data = {"file": (BytesIO(b"Hello World !!"), "hello.txt"), "type": "file"}

    r = client.post(
        "payload_in_file",
        data=data,
        headers={
            "enctype": "multipart/form-data",
        },
    )

    assert r.status_code == 200
    assert r.data == b'{"file_content":"b\'Hello World !!\'","type":"file"}\n'


def test_invalid_query_string_raise_400(
    app: Jeroboam,
    client: FlaskClient,
):
    """GIVEN a GET endpoint with properly annotated argument
    WHEN hit with invalid queryString
    THEN the endpoint raise a 400 InvalidRequest Error
    """

    @app.get("/strict_endpoint")
    def read_test(payload: InBoundModel):
        return payload.json()

    r = client.get("/strict_endpoint?page=not_a_valid_param")

    assert r.status_code == 400
    assert r.data.startswith(b"BadRequest")


def test_invalid_simple_param_raise_400(
    app: Jeroboam,
    client: FlaskClient,
):
    """GIVEN an endpoint that native-type-annotated argument
    WHEN hit with a wrong parameters
    THEN the endpoint raise a 400 InvalidRequest Error
    """

    @app.get("/query_string_as_int")
    def ping(simple_param: int):
        return {}

    r = client.get("query_string_as_int?simple_param=imparsable")

    assert r.status_code == 400
    assert r.data.startswith(b"BadRequest:")


def test_query_string_for_list_arguments(
    app: Jeroboam,
    client: FlaskClient,
):
    """GIVEN a GET endpoint with list arguments
    WHEN hit with proper formatted queryString
    THEN the arguments get injected into a Array
    """

    class QueryStringWithList(Parser):
        id: List[int] = Field(alias="id[]")
        order: List[Dict[str, str]] = Field(alias="order[]")

    @app.get("/query_string_with_list")
    def ping(query_string: QueryStringWithList):
        return ",".join([str(id) for id in query_string.id])

    r = client.get(
        "/query_string_with_list?order[name]=asc&order[group]=desc&id[]=1&id[]=2"
    )
    assert r.data == b"1,2"


def test_optionnal_param(
    app: Jeroboam,
    client: FlaskClient,
):
    """GIVEN an endpoint with Optionnal typed argument with Optional params
    WHEN hit with an empty payload
    THEN the endpoint is properly executed
    """

    class InBoundModel(BaseModel):
        page: Optional[int]
        per_page: Optional[int]

    @app.get("/optionnal_param")
    def ping(payload: Optional[InBoundModel]):
        return payload.json() if payload else {}

    r = client.get("/optionnal_param")

    assert r.status_code == 200
    assert r.data == b'{"page": null, "per_page": null}'


def test_other_methods(app: Jeroboam, client: FlaskClient):
    """GVIEN an endpoint with a different verb than GET or POST
    WHEN hit
    THEN it works like a regular endpoint
    """

    @app.delete("/other_verb")
    def ping():
        return {}, 201

    r = client.delete("/other_verb")

    assert r.status_code == 201
    assert r.data == b"{}\n"
