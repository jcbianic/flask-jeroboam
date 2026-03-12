"""Code Sample for OpenAPI Features Documentation."""

from pydantic import BaseModel

from flask_jeroboam import Blueprint, Jeroboam

app = Jeroboam("Jeroboam Inbound Features App")
app.init_app()


class TaskIn(BaseModel):
    name: str
    description: str | None = None


class TaskOut(TaskIn):
    id: int


@app.get("/health")
def get_health():
    return {"status": "Ok"}


blueprint = Blueprint("tasks", __name__, tags=["tasks"])


@blueprint.get("/tasks", response_model=list[TaskOut])
def get_tasks(page: int = 1, per_page: int = 10, search: str | None = None):
    return [{"id": 1, "name": "Task 1"}, {"id": 2, "name": "Task 2"}]


@blueprint.get("/tasks/<int:item_id>", response_model=TaskOut)
def get_task(item_id: int):
    return {"id": 1, "name": "Task 1"}


@blueprint.put("/tasks", status_code=202, tags=["sensitive"])
def create_task(task: TaskIn):
    return {}


@blueprint.post("/tasks/<int:item_id>", tags=["sensitive"])
def edit_task(item_id: int, task: TaskIn):
    return {}


app.register_blueprint(blueprint)

if __name__ == "__main__":
    app.run(host="localhost", port=5000)
