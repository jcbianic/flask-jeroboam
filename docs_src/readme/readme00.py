"""Code Example 00 for README.md."""
from flask_jeroboam import Jeroboam


app = Jeroboam(__name__)


@app.get("/ping")
def ping():
    return "pong"


if __name__ == "__main__":
    app.run(port=5000)
