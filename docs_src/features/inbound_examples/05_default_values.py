"""Assigning default values."""

from flask_jeroboam import Jeroboam, Query

app = Jeroboam("Jeroboam Inbound Features App")
app.init_app()


@app.get("/implicit_location_with_default_value")
def get_implicit_argument_with_default(page: int = 1):
    return f"Received Page Argument is : {page}"


@app.get("/explicit_location_with_default_value")
def get_explicit_argument_with_default(page: int = Query(1)):
    return f"Received Page Argument is : {page}"


if __name__ == "__main__":
    app.run(host="localhost", port=5000)
