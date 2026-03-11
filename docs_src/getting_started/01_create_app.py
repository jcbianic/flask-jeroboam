"""Create a Jeroboam app."""

from flask_jeroboam import Jeroboam

app = Jeroboam("Jeroboam Getting Started App")
app.init_app()


if __name__ == "__main__":
    app.run(host="localhost", port=5000)
