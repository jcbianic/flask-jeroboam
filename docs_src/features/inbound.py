"""Code Sample for Inbound Features Documentation."""

from typing import List

from pydantic import BaseModel

from flask_jeroboam import Body
from flask_jeroboam import Cookie
from flask_jeroboam import Jeroboam
from flask_jeroboam import Path
from flask_jeroboam import Query


app = Jeroboam("Jeroboam Inbound Features App")
app.init_app()


@app.get("/implicit_location_is_query_string")
def get_implicit_argument(page: int):
    return f"Received Page Argument is : {page}"


@app.get("/explicit_location_is_query_string")
def get_explicit_argument(page: int = Query()):
    return f"Received Page Argument is : {page}"


@app.get("/explicit_location_is_query_string_and_cookie")
def get_explicit_arguments(page: int = Query(), username: str = Cookie()):
    return f"Received Page Argument is : {page}. Username is : {username}"


@app.get("/implicit_and_explicit")
def get_implicit_and_explicit_arguments(page: int, username: str = Cookie()):
    return f"Received Page Argument is : {page}. Username is : {username}"


@app.post("/implicit_location_is_body")
def post_implicit_argument(page: int):
    return f"Received Page Argument is : {page}"


@app.post("/explicit_location_is_body")
def post_explicit_argument(page: int = Body()):
    return f"Received Page Argument is : {page}"


@app.get("/item/<int:id>/implicit")
def get_path_parameter(id: int):
    return f"Received id Argument is : {id}"


@app.post("/item/<int:id>/implicit")
def post_path_parameter(id: int):
    return f"Received id Argument is : {id}"


@app.post("/item/<int:id>/explicit")
def get_explicit_path_parameter(id: int = Path()):
    return f"Received id Argument is : {id}"


@app.get("/implicit_location_with_default_value")
def get_implicit_argument_with_default(page: int = 1):
    return f"Received Page Argument is : {page}"


@app.get("/explicit_location_with_default_value")
def get_explicit_argument_with_default(page: int = Query(1)):
    return f"Received Page Argument is : {page}"


class Item(BaseModel):
    name: str
    count: int


@app.get("/defining_type_with_type_hints")
def get_type_hints(page: int, search: List[str], item: Item, price=Query(float)):
    return (
        f"Received arguments are :\n"
        f"page : {page}\n"
        f"search : {search}\n"
        f"price : {price}\n"
        f"item : {item}"
    )


@app.get("/argument_with_validation")
def get_validation_option(page: int = Query(ge=1)):
    return f"Received page argument is : {page}"


if __name__ == "__main__":
    app.run(host="localhost", port=5000)
