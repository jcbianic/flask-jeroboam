"""A Test Blueprint for testing Path Params.

The corresponding test can be found in tests/test_inbound/test_path
"""

from flask_jeroboam import JeroboamBlueprint
from flask_jeroboam import Path


router = JeroboamBlueprint("path_params_router", __name__, tags=["Path"])


@router.get("/path/<item_id>")
def get_id(item_id):
    return {"item_id": item_id}


@router.get("/path/str/<item_id>")
def get_str_id(item_id: str):
    return {"item_id": item_id}


@router.get("/path/int/<item_id>")
def get_int_id(item_id: int):
    return {"item_id": item_id}


@router.get("/path/float/<item_id>")
def get_float_id(item_id: float):
    return {"item_id": item_id}


@router.get("/path/bool/<item_id>")
def get_bool_id(item_id: bool):
    return {"item_id": item_id}


@router.get("/path/param/<item_id>")
def get_path_param_id(item_id: str = Path()):
    return {"item_id": item_id}


@router.get("/path/param-required/<item_id>")
def get_path_param_required_id(item_id: str = Path()):
    return {"item_id": item_id}


@router.get("/path/param-minlength/<item_id>")
def get_path_param_min_length(item_id: str = Path(min_length=3)):
    return {"item_id": item_id}


@router.get("/path/param-maxlength/<item_id>")
def get_path_param_max_length(item_id: str = Path(max_length=3)):
    return {"item_id": item_id}


@router.get("/path/param-min_maxlength/<item_id>")
def get_path_param_min_max_length(item_id: str = Path(max_length=3, min_length=2)):
    return {"item_id": item_id}


@router.get("/path/param-gt/<item_id>")
def get_path_param_gt(item_id: float = Path(gt=3)):
    return {"item_id": item_id}


@router.get("/path/param-gt0/<item_id>")
def get_path_param_gt0(item_id: float = Path(gt=0)):
    return {"item_id": item_id}


@router.get("/path/param-ge/<item_id>")
def get_path_param_ge(item_id: float = Path(ge=3)):
    return {"item_id": item_id}


@router.get("/path/param-lt/<item_id>")
def get_path_param_lt(item_id: float = Path(lt=3)):
    return {"item_id": item_id}


@router.get("/path/param-lt0/<item_id>")
def get_path_param_lt0(item_id: float = Path(lt=0)):
    return {"item_id": item_id}


@router.get("/path/param-le/<item_id>")
def get_path_param_le(item_id: float = Path(le=3)):
    return {"item_id": item_id}


@router.get("/path/param-lt-gt/<item_id>")
def get_path_param_lt_gt(item_id: float = Path(lt=3, gt=1)):
    return {"item_id": item_id}


@router.get("/path/param-le-ge/<item_id>")
def get_path_param_le_ge(item_id: float = Path(le=3, ge=1)):
    return {"item_id": item_id}


@router.get("/path/param-lt-int/<item_id>")
def get_path_param_lt_int(item_id: int = Path(lt=3)):
    return {"item_id": item_id}


@router.get("/path/param-gt-int/<item_id>")
def get_path_param_gt_int(item_id: int = Path(gt=3)):
    return {"item_id": item_id}


@router.get("/path/param-le-int/<item_id>")
def get_path_param_le_int(item_id: int = Path(le=3)):
    return {"item_id": item_id}


@router.get("/path/param-ge-int/<item_id>")
def get_path_param_ge_int(item_id: int = Path(ge=3)):
    return {"item_id": item_id}


@router.get("/path/param-lt-gt-int/<item_id>")
def get_path_param_lt_gt_int(item_id: int = Path(lt=3, gt=1)):
    return {"item_id": item_id}


@router.get("/path/param-le-ge-int/<item_id>")
def get_path_param_le_ge_int(item_id: int = Path(le=3, ge=1)):
    return {"item_id": item_id}


@router.get("/path/with_converter/<item_id>")
def get_with_preproc_id(item_id):
    return {"item_id": item_id}


@router.get("/path/with_converter/str/<string:item_id>")
def get_with_preproc_str_id(item_id: str):
    return {"item_id": item_id}


@router.get("/path/with_converter/int/<int:item_id>")
def get_with_preproc_int_id(item_id: int):
    return {"item_id": item_id}


@router.get("/path/with_converter/float/<float:item_id>")
def get_with_preproc_float_id(item_id: float):
    return {"item_id": item_id}


@router.get("/path/with_converter/param/<string:item_id>")
def get_with_preproc_path_param_id(item_id: str = Path()):
    return {"item_id": item_id}


@router.get("/path/with_converter/param-required/<string:item_id>")
def get_with_preproc_path_param_required_id(item_id: str = Path()):
    return {"item_id": item_id}


@router.get("/path/with_converter/param-minlength/<string:item_id>")
def get_with_preproc_path_param_min_length(item_id: str = Path(min_length=3)):
    return {"item_id": item_id}


@router.get("/path/with_converter/param-maxlength/<string:item_id>")
def get_with_preproc_path_param_max_length(item_id: str = Path(max_length=3)):
    return {"item_id": item_id}


@router.get("/path/with_converter/param-min_maxlength/<string:item_id>")
def get_with_preproc_path_param_min_max_length(
    item_id: str = Path(max_length=3, min_length=2)
):
    return {"item_id": item_id}


@router.get("/path/with_converter/param-gt/<float:item_id>")
def get_with_preproc_path_param_gt(item_id: float = Path(gt=3)):
    return {"item_id": item_id}


@router.get("/path/with_converter/param-gt0/<float:item_id>")
def get_with_preproc_path_param_gt0(item_id: float = Path(gt=0)):
    return {"item_id": item_id}


@router.get("/path/with_converter/param-ge/<float:item_id>")
def get_with_preproc_path_param_ge(item_id: float = Path(ge=3)):
    return {"item_id": item_id}


@router.get("/path/with_converter/param-lt/<float:item_id>")
def get_with_preproc_path_param_lt(item_id: float = Path(lt=3)):
    return {"item_id": item_id}


@router.get("/path/with_converter/param-lt0/<float(signed=True):item_id>")
def get_with_preproc_path_param_lt0(item_id: float = Path(lt=0)):
    return {"item_id": item_id}


@router.get("/path/with_converter/param-le/<float:item_id>")
def get_with_preproc_path_param_le(item_id: float = Path(le=3)):
    return {"item_id": item_id}


@router.get("/path/with_converter/param-lt-gt/<float:item_id>")
def get_with_preproc_path_param_lt_gt(item_id: float = Path(lt=3, gt=1)):
    return {"item_id": item_id}


@router.get("/path/with_converter/param-le-ge/<float:item_id>")
def get_with_preproc_path_param_le_ge(item_id: float = Path(le=3, ge=1)):
    return {"item_id": item_id}


@router.get("/path/with_converter/param-lt-int/<int:item_id>")
def get_with_preproc_path_param_lt_int(item_id: int = Path(lt=3)):
    return {"item_id": item_id}


@router.get("/path/with_converter/param-gt-int/<int:item_id>")
def get_with_preproc_path_param_gt_int(item_id: int = Path(gt=3)):
    return {"item_id": item_id}


@router.get("/path/with_converter/param-le-int/<int:item_id>")
def get_with_preproc_path_param_le_int(item_id: int = Path(le=3)):
    return {"item_id": item_id}


@router.get("/path/with_converter/param-ge-int/<int:item_id>")
def get_with_preproc_path_param_ge_int(item_id: int = Path(ge=3)):
    return {"item_id": item_id}


@router.get("/path/with_converter/param-lt-gt-int/<int:item_id>")
def get_with_preproc_path_param_lt_gt_int(item_id: int = Path(lt=3, gt=1)):
    return {"item_id": item_id}


@router.get("/path/with_converter/param-le-ge-int/<int:item_id>")
def get_with_preproc_path_param_le_ge_int(item_id: int = Path(le=3, ge=1)):
    return {"item_id": item_id}
