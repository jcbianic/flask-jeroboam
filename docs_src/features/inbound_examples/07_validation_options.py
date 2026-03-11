"""Validation options with constraints."""

from flask_jeroboam import Jeroboam, Query

app = Jeroboam("Jeroboam Inbound Features App")
app.init_app()


@app.get("/argument_with_validation")
def get_validation_option(page: int = Query(ge=1)):
    return f"Received page argument is : {page}"


if __name__ == "__main__":
    app.run(host="localhost", port=5000)
