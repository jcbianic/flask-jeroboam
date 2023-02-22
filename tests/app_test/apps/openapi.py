"""A Test Blueprint for testing OpenApi Specials.

The corresponding test can be found in tests/test_openapi/*
"""
from flask_jeroboam import Blueprint
from flask_jeroboam.view_arguments.functions import Query


router = Blueprint("openapi_args_router", __name__, tags=["OpenApi"])


@router.get("/query/dont_include_in_schema")
def read_argument_not_included_in_schema(
    not_included: int = Query(include_in_schema=False),
):
    return {"not_included": not_included}


@router.get(
    "/query/openapi_extra",
    openapi_extra={"example": {"testA": 1}, "examples": [{"test": 1}]},
)
def read_openapi_extra(
    with_openapi_extra: int = Query(
        include_in_schema=False,
    )
):
    return {"with_openapi_extra": with_openapi_extra}


@router.get("/openapi/no_body_status_code", status_code=205)
def get_that_returns_a_empty_body(payload: str):
    return None


@router.get("/openapi/no_response_model", response_model=None)
def get_without_a_reponse_model(payload: str):
    return None
