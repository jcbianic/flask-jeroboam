"""A Test Blueprint for testing File Params.

The corresponding test can be found in tests/test_inbound/test_file
"""
from werkzeug.datastructures import FileStorage

from flask_jeroboam import File
from flask_jeroboam import JeroboamBlueprint


router = JeroboamBlueprint("file_params_router", __name__)


@router.post("/file")
def ping(file: FileStorage = File(...)):
    return {"file_content": str(file.read())}
