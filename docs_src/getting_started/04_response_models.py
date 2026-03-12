"""Response models."""

from pydantic import BaseModel, Field

from flask_jeroboam import Jeroboam

app = Jeroboam("Jeroboam Getting Started App")
app.init_app()


class Item(BaseModel):
    name: str
    price: float
    count: int = Field(1)


@app.get("/item", response_model=Item)
def get_an_item():
    return {"name": "Bottle", "price": 5}


if __name__ == "__main__":
    app.run(host="localhost", port=5000)
