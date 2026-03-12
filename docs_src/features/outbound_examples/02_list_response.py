"""List response - returning multiple items."""

from pydantic import BaseModel

from flask_jeroboam import Jeroboam

app = Jeroboam("Jeroboam Outbound Features App")
app.init_app()


class Task(BaseModel):
    id: int
    title: str
    done: bool = False


@app.get("/tasks", response_model=list[Task])
def list_tasks():
    return [
        {"id": 1, "title": "Buy groceries", "done": False},
        {"id": 2, "title": "Write docs", "done": True},
        {"id": 3, "title": "Review PR", "done": False},
    ]


if __name__ == "__main__":
    app.run(host="localhost", port=5000)
