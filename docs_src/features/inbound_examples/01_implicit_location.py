"""Implicit location - GET and POST endpoints."""

from flask_jeroboam import Jeroboam

app = Jeroboam("Jeroboam Inbound Features App")
app.init_app()


@app.get("/implicit_location_is_query_string")
def get_implicit_argument(page: int):
    return f"Received Page Argument is : {page}"


@app.post("/implicit_location_is_body")
def post_implicit_argument(page: int):
    return f"Received Page Argument is : {page}"


if __name__ == "__main__":
    app.run(host="localhost", port=5000)
