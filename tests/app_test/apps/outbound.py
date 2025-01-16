"""A Test Blueprint for testing Outbound Behavior.

The corresponding test can be found in tests/test_outbound.py
"""

from typing import Any
from typing import Dict
from typing import List

from flask_jeroboam import Blueprint
from flask_jeroboam.responses import JSONResponse
from flask_jeroboam.view_arguments.functions import Body
from tests.app_test.models.outbound import MyDataClass
from tests.app_test.models.outbound import SimpleModelOut
from tests.app_test.models.outbound import UserIn
from tests.app_test.models.outbound import UserOut


router = Blueprint("outbound_router", __name__, tags=["Outbound"])

valid_outbound_data: Dict[str, Any] = {
    "total_count": 10,
    "items": ["Apple", "Banana"],
}


@router.route(
    "/methods/explicit_options",
    methods=["GET", "OPTIONS"],
    response_model=SimpleModelOut,
)
def get_with_explicit_verb_options():
    return valid_outbound_data


@router.route(
    "/methods/explicit_options_and_head",
    methods=["GET", "OPTIONS", "HEAD"],
    response_model=SimpleModelOut,
)
def get_with_explicit_verbs_options_and_head():
    return valid_outbound_data


@router.put("/verb/put/without_explicit_status_code", response_model=SimpleModelOut)
def put_http_verb():
    return valid_outbound_data


@router.patch("/verb/patch/without_explicit_status_code", response_model=SimpleModelOut)
def patch_http_verb():
    return valid_outbound_data


@router.get("/response_model/no_response_model")
def no_response_model():
    return "Don't have a response model"


@router.get("/response_model/infered_from_return_annotation")
def response_model_is_infered_from_return_annotation() -> SimpleModelOut:
    return SimpleModelOut(total_count=10, items=["Apple", "Banana"])


@router.get(
    "/response_model/configuration_over_inference", response_model=SimpleModelOut
)
def configuration_over_inference() -> dict:
    return valid_outbound_data


@router.get("/response_model/turned_off", response_model=None)
def response_model_inference_is_turned_off() -> SimpleModelOut:
    return SimpleModelOut(total_count=10, items=["Apple", "Banana"])


@router.get("/return_type/dict", response_model=SimpleModelOut)
def view_function_returns_a_dict() -> dict:
    return valid_outbound_data


@router.get("/return_type/list", response_model=List[SimpleModelOut])
def view_function_returns_a_list():
    return [valid_outbound_data, valid_outbound_data]


@router.get("/return_type/base_model", response_model=SimpleModelOut)
def view_function_returns_a_base_model():
    return SimpleModelOut(total_count=10, items=["Apple", "Banana"])


@router.get("/return_type/response", response_model=SimpleModelOut)
def view_function_returns_a_response():
    return JSONResponse(
        SimpleModelOut(total_count=10, items=["Apple", "Banana"]).json()
    )


@router.get("/return_type/dataclass", response_model=SimpleModelOut)
def view_function_returns_a_dataclass():
    return MyDataClass(**valid_outbound_data)


@router.get("/return_type/not_valid", response_model=SimpleModelOut)
def view_function_returns_unvalid():
    return "not a list"


@router.get("/return_shape/with_headers", response_model=SimpleModelOut)
def view_function_returns_dict_and_headers():
    return valid_outbound_data, {"X-Test": "Test"}


@router.get("/return_shape/with_headers_and_status_code", response_model=SimpleModelOut)
def view_function_returns_dict_status_code_and_headers():
    return valid_outbound_data, 218, {"X-Test": "Test"}


@router.get("/return_shape/with_status_code", response_model=SimpleModelOut)
def view_function_returns_dict_and_status_code():
    return valid_outbound_data, 218


@router.get("/return_shape/wrong_tuple_length", response_model=SimpleModelOut)
def view_function_returns_wrong_tuple_length():
    return valid_outbound_data, 200, {"X-Test": "Test"}, "extra"


@router.get("/status_code/204_has_no_body/as_returned")
def returned_status_code_204_has_no_body_returned():
    return "Some Content that will be ignored", 204


@router.get(
    "/status_code/204_has_no_body/as_configured",
    status_code=204,
)
def configured_status_code_204_has_no_body():
    return "Some Content that will be ignored"


@router.post("/sensitive_data", response_model=UserOut)
def reponse_model_filters_data(sensitive_data: UserIn = Body()):
    return sensitive_data
