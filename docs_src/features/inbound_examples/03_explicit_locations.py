"""Explicit locations - GET and POST with Query()."""

from flask_jeroboam import Jeroboam, Query

app = Jeroboam("Jeroboam Inbound Features App")
app.init_app()


@app.get("/implicit_location_is_query_string")
def get_implicit_argument(page: int):
    return f"Received Page Argument is : {page}"


@app.get("/explicit_location_is_query_string")
def get_explicit_argument(page: int = Query()):
    return f"Received Page Argument is : {page}"


@app.post("/implicit_location_is_body")
def post_implicit_argument(page: int):
    return f"Received Page Argument is : {page}"


@app.post("/explicit_location_is_body")
def post_explicit_argument(page: int = Query()):
    return f"Received Page Argument is : {page}"


if __name__ == "__main__":
    app.run(host="localhost", port=5000)
