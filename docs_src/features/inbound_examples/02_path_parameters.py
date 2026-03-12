"""Path parameters - GET and POST endpoints."""

from flask_jeroboam import Jeroboam

app = Jeroboam("Jeroboam Inbound Features App")
app.init_app()


@app.get("/item/<int:id>/implicit")
def get_path_parameter(id: int):
    return f"Received id Argument is : {id}"


@app.post("/item/<int:id>/implicit")
def post_path_parameter(id: int):
    return f"Received id Argument is : {id}"


if __name__ == "__main__":
    app.run(host="localhost", port=5000)
