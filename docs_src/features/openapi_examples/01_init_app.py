"""OpenAPI auto-documentation - initializing Jeroboam app."""

from flask_jeroboam import Jeroboam

app = Jeroboam(__name__)
app.init_app()


if __name__ == "__main__":
    app.run(host="localhost", port=5000)
