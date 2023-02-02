import pytest


not_a_valid_int = {
    "detail": [
        {
            "loc": ["cookie", "cookie"],
            "msg": "value is not a valid integer",
            "type": "type_error.integer",
        }
    ]
}


def _valid(x):
    return {"cookie": x}


@pytest.mark.parametrize(
    "url,cookie_value,expected_status,expected_response",
    [
        ("/cookie/str", b"foobar", 200, _valid("foobar")),
        ("/cookie/int", b"123", 200, _valid(123)),
        ("/cookie/int", b"not_valid_int", 400, not_a_valid_int),
    ],
)
def test_get_cookie(client, url, cookie_value, expected_status, expected_response):
    """Test Cookie Parameter with GET method.


    TODO: Allow Configuration of the returned Status Code.
    """
    client.set_cookie("localhost", "cookie", cookie_value)
    response = client.get(url)
    assert response.status_code == expected_status
    assert response.json == expected_response
