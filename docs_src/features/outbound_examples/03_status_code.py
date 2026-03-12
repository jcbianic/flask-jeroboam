"""Response with custom status code."""

from pydantic import BaseModel

from flask_jeroboam import Jeroboam

app = Jeroboam("Jeroboam Outbound Features App")
app.init_app()


class Task(BaseModel):
    id: int
    title: str


@app.post("/tasks", response_model=Task, status_code=201)
def create_task(title: str):
    return {"id": 1, "title": title}


if __name__ == "__main__":
    app.run(host="localhost", port=5000)
