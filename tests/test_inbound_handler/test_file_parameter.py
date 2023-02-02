"""Test the FileParam.

The corresponding endpoints are defined in the test_app.apps.file.py module.
"""


from io import BytesIO

from flask.testing import FlaskClient


def test_valid_payload_in_files_is_injected(client: FlaskClient):
    """GIVEN a POST endpoint with FileParam
    WHEN hit with a valid files payload
    THEN the parsed input is injected into the view function.
    """
    data = {"file": (BytesIO(b"Hello World !!"), "hello.txt"), "type": "file"}

    response = client.post(
        "/file",
        data=data,
        headers={
            "enctype": "multipart/form-data",
        },
    )

    assert response.status_code == 201
    assert response.json == {"file_content": "b'Hello World !!'"}
