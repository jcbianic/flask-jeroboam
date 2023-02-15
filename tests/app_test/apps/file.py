"""A Test Blueprint for testing File Params.

The corresponding test can be found in tests/test_inbound/test_file
"""
from flask_jeroboam import File
from flask_jeroboam import JeroboamBlueprint
from flask_jeroboam.datastructures import UploadFile


router = JeroboamBlueprint("file_params_router", __name__, tags=["File"])


@router.post("/file")
def ping(file: UploadFile = File(embed=True)):
    return {"file_content": str(file.read())}
