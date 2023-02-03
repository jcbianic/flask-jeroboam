"""A Test Blueprint for testing Body Params.

The corresponding test can be found in tests/test_inbound/test_body
"""
from flask_jeroboam import Body
from flask_jeroboam import JeroboamBlueprint
from tests.app_test.models.inbound import SimpleModelIn


router = JeroboamBlueprint("body_params_router", __name__)


@router.post("/body/int")
def post_body_as_int(payload: int = Body(embed=True)):
    """Body Param as plain int."""
    return {"payload": payload}


@router.post("/body/str")
def post_body_as_str(payload: str = Body(embed=True)):
    """Body Param as plain str."""
    return {"payload": payload}


@router.post("/body/base_model")
def post_base_model_in_form(payload: SimpleModelIn = Body(embed=False)):
    """POST Form Parameter as pydantic BaseModel."""
    return payload.json()
