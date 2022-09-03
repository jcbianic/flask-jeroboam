from flask-jeroboam import APIRouter
from flask-jeroboam import Body


router = APIRouter()


@router.post("/compute")
def compute(a: int = Body(), b: str = Body()):
    return {"a": a, "b": b}
