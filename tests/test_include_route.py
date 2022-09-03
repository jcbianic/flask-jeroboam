from flask-jeroboam import APIRouter
from flask-jeroboam import FastAPI
from flask-jeroboam import Request
from flask-jeroboam.responses import JSONResponse
from flask-jeroboam.testclient import TestClient


app = FastAPI()
router = APIRouter()


@router.route("/items/")
def read_items(request: Request):
    return JSONResponse({"hello": "world"})


app.include_router(router)

client = TestClient(app)


def test_sub_router():
    response = client.get("/items/")
    assert response.status_code == 200, response.text
    assert response.json() == {"hello": "world"}
