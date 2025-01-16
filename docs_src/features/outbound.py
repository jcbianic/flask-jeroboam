"""Code Sample for Outbound Features Documentation."""

from typing import Optional

from pydantic import BaseModel
from pydantic import Field

from flask_jeroboam import Jeroboam


app = Jeroboam("Jeroboam Outbound Features App")
app.init_app()


class Task(BaseModel):
    id: int
    name: str
    description: Optional[str] = Field("Just here to make a point.")


class TaskIn(BaseModel):
    name: str
    description: Optional[str] = None


class TaskOut(TaskIn):
    id: int


@app.get("/tasks/<int:task_id>", response_model=Task)
def read_explicit_task(task_id: int):
    return {"id": task_id, "name": "Find the answer."}


@app.get("/tasks/<int:task_id>/no_response_model")
def read_task_dictionnary_without_response_mode(task_id: int):
    return {"id": task_id, "name": "I'm from the dictionary."}


@app.get("/tasks/<int:task_id>/implicit_from_annotation")
def read_implicit_task(task_id: int) -> Task:
    return Task.parse_obj({"id": task_id, "name": "Implicit from Annotation"})


@app.get("/tasks/<int:task_id>/implicit_no_annotation")
def read_implicit_no_annotation(task_id: int):
    return Task.parse_obj({"id": task_id, "name": "Implicit from Annotation"})


@app.get("/tasks/<int:task_id>/response_model_off", response_model=None)
def read_response_model_off(task_id: int):
    return {"id": task_id, "name": "Response Model is off."}


@app.put("/tasks", response_model=TaskOut)
def create_task(task: TaskIn):
    return {"task_id": 1, "name": task.name, "description": task.description}


if __name__ == "__main__":
    app.run(host="localhost", port=5000)
