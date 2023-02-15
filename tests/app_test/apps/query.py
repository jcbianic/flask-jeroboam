"""A Test Blueprint for testing Query Params.

The corresponding test can be found in tests/test_inbound/test_query
"""
from typing import FrozenSet
from typing import Optional

from flask_jeroboam import JeroboamBlueprint
from flask_jeroboam import Query
from tests.app_test.models.inbound import ModelWithListIn
from tests.app_test.models.inbound import OptionalModelIn
from tests.app_test.models.inbound import QueryStringWithList
from tests.app_test.models.inbound import SimpleModelIn
from tests.app_test.models.outbound import ModelWithListOut


router = JeroboamBlueprint("query_params_router", __name__, tags=["Query"])


@router.get("/query/frozenset/")
def get_query_type_frozenset(query: FrozenSet[int] = Query(...)):
    return {"query": ",".join(map(str, sorted(query)))}


@router.get("/query")
def get_query(query):
    return {"query": query}


@router.get("/query/optional")
def get_query_optional(query=None):
    return {"query": query}


@router.get("/query/int")
def get_query_type(query: int):
    return {"query": query}


@router.get("/query/int/optional")
def get_query_type_optional(query: Optional[int] = None):
    return {"query": query}


@router.get("/query/int/default")
def get_query_type_int_default(query: int = 10):
    return {"query": query}


@router.get("/query/param")
def get_query_param(query=Query(default=None)):
    return {"query": query}


@router.get("/query/param-required")
def get_query_param_required(query=Query()):
    return {"query": query}


@router.get("/query/param-required/int")
def get_query_param_required_type(query: int = Query()):
    return {"query": query}


@router.get("/enum-status-code", status_code=201)
def get_enum_status_code():
    return {}


@router.get("/query/base_model")
def get_base_model(payload: SimpleModelIn):
    """Base Model as Query Param."""
    return payload.json()


@router.get("/query/base_model/forward_ref")
def get_base_model_as_forward_ref(payload: "SimpleModelIn"):
    return payload.json()


@router.get("/query/list_of_strings")
def get_list_of_strings(query_string: QueryStringWithList):
    return query_string.json()


@router.get("/query/optional_model")
def get_optional_param(payload: Optional[OptionalModelIn]):
    return payload.json() if payload else {}


@router.get("/query/special_pattern", response_model=ModelWithListOut)
def read_items(payload: ModelWithListIn):
    return payload.json()
