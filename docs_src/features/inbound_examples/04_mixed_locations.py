"""Mixing implicit and explicit locations."""

from flask_jeroboam import Jeroboam, Cookie, Query

app = Jeroboam("Jeroboam Inbound Features App")
app.init_app()


@app.get("/explicit_location_is_query_string_and_cookie")
def get_explicit_arguments(page: int = Query(), username: str = Cookie()):
    return f"Received Page Argument is : {page}. Username is : {username}"


@app.get("/implicit_and_explicit")
def get_implicit_and_explicit_arguments(page: int, username: str = Cookie()):
    return f"Received Page Argument is : {page}. Username is : {username}"


if __name__ == "__main__":
    app.run(host="localhost", port=5000)
