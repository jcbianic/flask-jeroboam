"""Type patterns with Pydantic models."""

from pydantic import BaseModel

from flask_jeroboam import Jeroboam, Query

app = Jeroboam("Jeroboam Inbound Features App")
app.init_app()


class Item(BaseModel):
    name: str
    count: int


@app.get("/defining_type_with_type_hints")
def get_type_hints(page: int, search: list[str], item: Item, price=Query(float)):
    return (
        f"Received arguments are :\n"
        f"page : {page}\n"
        f"search : {search}\n"
        f"price : {price}\n"
        f"item : {item}"
    )


if __name__ == "__main__":
    app.run(host="localhost", port=5000)
