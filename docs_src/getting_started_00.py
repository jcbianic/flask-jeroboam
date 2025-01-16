"""Code Sample for Getting Started with Flask-Jeroboam."""

from pydantic import BaseModel
from pydantic import Field

from flask_jeroboam import Jeroboam


app = Jeroboam("Jeroboam Getting Started App")
app.init_app()


@app.get("/health")
def get_health():
    return {"status": "Ok"}


@app.get("/query_string_arguments")
def get_query_string_arguments(page: int = 1, per_page: int = 10):
    return {"page": page, "per_page": per_page}


class Item(BaseModel):
    name: str
    price: float
    count: int = Field(1)


@app.get("/item", response_model=Item)
def get_an_item():
    return {"name": "Bottle", "price": 5}


if __name__ == "__main__":
    app.run(host="localhost", port=5000)
