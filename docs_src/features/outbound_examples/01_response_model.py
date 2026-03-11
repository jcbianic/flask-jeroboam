"""Response model - Task example."""

from pydantic import BaseModel

from flask_jeroboam import Jeroboam

app = Jeroboam("Jeroboam Outbound Features App")
app.init_app()


class Task(BaseModel):
    id: int
    title: str
    description: str | None = None
    done: bool = False


@app.get("/tasks/<int:task_id>", response_model=Task)
def get_task(task_id: int):
    return {
        "id": task_id,
        "title": "Buy groceries",
        "description": "Milk, cheese, bread",
        "done": False,
    }


if __name__ == "__main__":
    app.run(host="localhost", port=5000)
