"""Register a view function."""

from flask_jeroboam import Jeroboam

app = Jeroboam("Jeroboam Getting Started App")
app.init_app()


@app.get("/health")
def get_health():
    return {"status": "Ok"}


if __name__ == "__main__":
    app.run(host="localhost", port=5000)
