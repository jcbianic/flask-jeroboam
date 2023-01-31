"""Configuration File for pytest."""
import os
from typing import FrozenSet
from typing import Optional

import pytest

from flask_jeroboam import Jeroboam
from flask_jeroboam import JeroboamBlueprint
from flask_jeroboam.exceptions import InvalidRequest
from flask_jeroboam.exceptions import ResponseValidationError
from flask_jeroboam.exceptions import RessourceNotFound
from flask_jeroboam.exceptions import ServerError
from flask_jeroboam.view_params import Body
from flask_jeroboam.view_params import Header
from flask_jeroboam.view_params import Path
from flask_jeroboam.view_params import Query
from flask_jeroboam.view_params.functions import Cookie


@pytest.fixture
def app() -> Jeroboam:
    """A Basic Jeroboam Test App."""
    app = Jeroboam("jeroboam_test", root_path=os.path.dirname(__file__))
    app.config.update(
        TESTING=True,
        SECRET_KEY="RandomSecretKey",
    )
    # TODO: Add it by default with CONFIG OPT-OUT

    def handle_404(e):
        return {"message": "Not Found"}, 404

    app.register_error_handler(InvalidRequest, InvalidRequest.handle)
    app.register_error_handler(RessourceNotFound, RessourceNotFound.handle)
    app.register_error_handler(ServerError, ServerError.handle)
    app.register_error_handler(ResponseValidationError, ResponseValidationError.handle)
    app.register_error_handler(404, handle_404)

    @app.route("/api_route")
    def non_operation():
        return {"message": "Hello World"}

    @app.get("/text")
    def get_text():
        return "Hello World"

    return app


@pytest.fixture
def app_with_path_operations(app) -> Jeroboam:  # noqa: C901
    """App with reigistered path operations."""

    @app.get("/path/<item_id>")
    def get_id(item_id):
        return {"item_id": item_id}

    @app.get("/path/str/<item_id>")
    def get_str_id(item_id: str):
        return {"item_id": item_id}

    @app.get("/path/int/<item_id>")
    def get_int_id(item_id: int):
        return {"item_id": item_id}

    @app.get("/path/float/<item_id>")
    def get_float_id(item_id: float):
        return {"item_id": item_id}

    @app.get("/path/bool/<item_id>")
    def get_bool_id(item_id: bool):
        return {"item_id": item_id}

    @app.get("/path/param/<item_id>")
    def get_path_param_id(item_id: str = Path()):
        return {"item_id": item_id}

    @app.get("/path/param-required/<item_id>")
    def get_path_param_required_id(item_id: str = Path()):
        return {"item_id": item_id}

    @app.get("/path/param-minlength/<item_id>")
    def get_path_param_min_length(item_id: str = Path(min_length=3)):
        return {"item_id": item_id}

    @app.get("/path/param-maxlength/<item_id>")
    def get_path_param_max_length(item_id: str = Path(max_length=3)):
        return {"item_id": item_id}

    @app.get("/path/param-min_maxlength/<item_id>")
    def get_path_param_min_max_length(item_id: str = Path(max_length=3, min_length=2)):
        return {"item_id": item_id}

    @app.get("/path/param-gt/<item_id>")
    def get_path_param_gt(item_id: float = Path(gt=3)):
        return {"item_id": item_id}

    @app.get("/path/param-gt0/<item_id>")
    def get_path_param_gt0(item_id: float = Path(gt=0)):
        return {"item_id": item_id}

    @app.get("/path/param-ge/<item_id>")
    def get_path_param_ge(item_id: float = Path(ge=3)):
        return {"item_id": item_id}

    @app.get("/path/param-lt/<item_id>")
    def get_path_param_lt(item_id: float = Path(lt=3)):
        return {"item_id": item_id}

    @app.get("/path/param-lt0/<item_id>")
    def get_path_param_lt0(item_id: float = Path(lt=0)):
        return {"item_id": item_id}

    @app.get("/path/param-le/<item_id>")
    def get_path_param_le(item_id: float = Path(le=3)):
        return {"item_id": item_id}

    @app.get("/path/param-lt-gt/<item_id>")
    def get_path_param_lt_gt(item_id: float = Path(lt=3, gt=1)):
        return {"item_id": item_id}

    @app.get("/path/param-le-ge/<item_id>")
    def get_path_param_le_ge(item_id: float = Path(le=3, ge=1)):
        return {"item_id": item_id}

    @app.get("/path/param-lt-int/<item_id>")
    def get_path_param_lt_int(item_id: int = Path(lt=3)):
        return {"item_id": item_id}

    @app.get("/path/param-gt-int/<item_id>")
    def get_path_param_gt_int(item_id: int = Path(gt=3)):
        return {"item_id": item_id}

    @app.get("/path/param-le-int/<item_id>")
    def get_path_param_le_int(item_id: int = Path(le=3)):
        return {"item_id": item_id}

    @app.get("/path/param-ge-int/<item_id>")
    def get_path_param_ge_int(item_id: int = Path(ge=3)):
        return {"item_id": item_id}

    @app.get("/path/param-lt-gt-int/<item_id>")
    def get_path_param_lt_gt_int(item_id: int = Path(lt=3, gt=1)):
        return {"item_id": item_id}

    @app.get("/path/param-le-ge-int/<item_id>")
    def get_path_param_le_ge_int(item_id: int = Path(le=3, ge=1)):
        return {"item_id": item_id}

    @app.get("/path/with_converter/<item_id>")
    def get_with_preproc_id(item_id):
        return {"item_id": item_id}

    @app.get("/path/with_converter/str/<string:item_id>")
    def get_with_preproc_str_id(item_id: str):
        return {"item_id": item_id}

    @app.get("/path/with_converter/int/<int:item_id>")
    def get_with_preproc_int_id(item_id: int):
        return {"item_id": item_id}

    @app.get("/path/with_converter/float/<float:item_id>")
    def get_with_preproc_float_id(item_id: float):
        return {"item_id": item_id}

    @app.get("/path/with_converter/param/<string:item_id>")
    def get_with_preproc_path_param_id(item_id: str = Path()):
        return {"item_id": item_id}

    @app.get("/path/with_converter/param-required/<string:item_id>")
    def get_with_preproc_path_param_required_id(item_id: str = Path()):
        return {"item_id": item_id}

    @app.get("/path/with_converter/param-minlength/<string:item_id>")
    def get_with_preproc_path_param_min_length(item_id: str = Path(min_length=3)):
        return {"item_id": item_id}

    @app.get("/path/with_converter/param-maxlength/<string:item_id>")
    def get_with_preproc_path_param_max_length(item_id: str = Path(max_length=3)):
        return {"item_id": item_id}

    @app.get("/path/with_converter/param-min_maxlength/<string:item_id>")
    def get_with_preproc_path_param_min_max_length(
        item_id: str = Path(max_length=3, min_length=2)
    ):
        return {"item_id": item_id}

    @app.get("/path/with_converter/param-gt/<float:item_id>")
    def get_with_preproc_path_param_gt(item_id: float = Path(gt=3)):
        return {"item_id": item_id}

    @app.get("/path/with_converter/param-gt0/<float:item_id>")
    def get_with_preproc_path_param_gt0(item_id: float = Path(gt=0)):
        return {"item_id": item_id}

    @app.get("/path/with_converter/param-ge/<float:item_id>")
    def get_with_preproc_path_param_ge(item_id: float = Path(ge=3)):
        return {"item_id": item_id}

    @app.get("/path/with_converter/param-lt/<float:item_id>")
    def get_with_preproc_path_param_lt(item_id: float = Path(lt=3)):
        return {"item_id": item_id}

    @app.get("/path/with_converter/param-lt0/<float(signed=True):item_id>")
    def get_with_preproc_path_param_lt0(item_id: float = Path(lt=0)):
        return {"item_id": item_id}

    @app.get("/path/with_converter/param-le/<float:item_id>")
    def get_with_preproc_path_param_le(item_id: float = Path(le=3)):
        return {"item_id": item_id}

    @app.get("/path/with_converter/param-lt-gt/<float:item_id>")
    def get_with_preproc_path_param_lt_gt(item_id: float = Path(lt=3, gt=1)):
        return {"item_id": item_id}

    @app.get("/path/with_converter/param-le-ge/<float:item_id>")
    def get_with_preproc_path_param_le_ge(item_id: float = Path(le=3, ge=1)):
        return {"item_id": item_id}

    @app.get("/path/with_converter/param-lt-int/<int:item_id>")
    def get_with_preproc_path_param_lt_int(item_id: int = Path(lt=3)):
        return {"item_id": item_id}

    @app.get("/path/with_converter/param-gt-int/<int:item_id>")
    def get_with_preproc_path_param_gt_int(item_id: int = Path(gt=3)):
        return {"item_id": item_id}

    @app.get("/path/with_converter/param-le-int/<int:item_id>")
    def get_with_preproc_path_param_le_int(item_id: int = Path(le=3)):
        return {"item_id": item_id}

    @app.get("/path/with_converter/param-ge-int/<int:item_id>")
    def get_with_preproc_path_param_ge_int(item_id: int = Path(ge=3)):
        return {"item_id": item_id}

    @app.get("/path/with_converter/param-lt-gt-int/<int:item_id>")
    def get_with_preproc_path_param_lt_gt_int(item_id: int = Path(lt=3, gt=1)):
        return {"item_id": item_id}

    @app.get("/path/with_converter/param-le-ge-int/<int:item_id>")
    def get_with_preproc_path_param_le_ge_int(item_id: int = Path(le=3, ge=1)):
        return {"item_id": item_id}

    return app


@pytest.fixture
def app_with_query_operations(app: Jeroboam) -> Jeroboam:  # noqa: C901
    """App with reigistered query operations."""

    @app.get("/query/frozenset/")
    def get_query_type_frozenset(query: FrozenSet[int] = Query(...)):
        return {"query": ",".join(map(str, sorted(query)))}

    @app.get("/query")
    def get_query(query):
        return {"query": query}

    @app.get("/query/optional")
    def get_query_optional(query=None):
        return {"query": query}

    @app.get("/query/int")
    def get_query_type(query: int):
        return {"query": query}

    @app.get("/query/int/optional")
    def get_query_type_optional(query: Optional[int] = None):
        return {"query": query}

    @app.get("/query/int/default")
    def get_query_type_int_default(query: int = 10):
        return {"query": query}

    @app.get("/query/param")
    def get_query_param(query=Query(default=None)):
        return {"query": query}

    @app.get("/query/param-required")
    def get_query_param_required(query=Query()):
        return {"query": query}

    @app.get("/query/param-required/int")
    def get_query_param_required_type(query: int = Query()):
        return {"query": query}

    @app.get("/enum-status-code", status_code=201)
    def get_enum_status_code():
        return {}

    return app


@pytest.fixture
def app_with_cookie_parameters(app: Jeroboam) -> Jeroboam:
    """App with reigistered cookie parameters."""

    @app.get("/cookie/int")
    def get_cookie_as_int(cookie: int = Cookie()):
        return {"cookie": cookie}

    @app.get("/cookie/str")
    def get_cookie_as_str(cookie: str = Cookie()):
        return {"cookie": cookie}

    return app


@pytest.fixture
def app_with_header_parameters(app: Jeroboam) -> Jeroboam:
    """App with reigistered cookie parameters."""

    @app.get("/headers/int")
    def get_header_as_int(test_header: int = Header()):
        return {"header": test_header}

    @app.get("/headers/str")
    def get_header_as_str(test_header: str = Header()):
        return {"header": test_header}

    return app


@pytest.fixture
def app_with_body_parameters(app: Jeroboam) -> Jeroboam:
    """App with reigistered cookie parameters."""

    @app.post("/body/int")
    def post_body_as_int(payload: int = Body()):
        return {"payload": payload}

    @app.post("/body/str")
    def post_body_as_str(payload: str = Body()):
        return {"payload": payload}

    return app


@pytest.fixture
def blueprint() -> JeroboamBlueprint:
    """A Basic Jeroboam Test App."""
    return JeroboamBlueprint("TestBluePrint", __name__)


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


@pytest.fixture
def query_client(app_with_query_operations: Jeroboam):
    """Test Client from the Test App."""
    return app_with_query_operations.test_client()


@pytest.fixture
def path_client(app_with_path_operations: Jeroboam):
    """Test Client from the Test App."""
    return app_with_path_operations.test_client()


@pytest.fixture
def cookie_client(app_with_cookie_parameters: Jeroboam):
    """Test Client from the Test App."""
    return app_with_cookie_parameters.test_client()


@pytest.fixture
def header_client(app_with_header_parameters: Jeroboam):
    """Test Client from the Test App."""
    return app_with_header_parameters.test_client()


@pytest.fixture
def body_client(app_with_body_parameters: Jeroboam):
    """Test Client from the Test App."""
    return app_with_body_parameters.test_client()
