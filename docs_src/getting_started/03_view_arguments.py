"""Adding view arguments."""

from flask_jeroboam import Jeroboam

app = Jeroboam("Jeroboam Getting Started App")
app.init_app()


@app.get("/query_string_arguments")
def get_query_string_arguments(page: int = 1, per_page: int = 10):
    return {"page": page, "per_page": per_page}


if __name__ == "__main__":
    app.run(host="localhost", port=5000)
