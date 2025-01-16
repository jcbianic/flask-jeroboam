"""Code Example 01 for README.md."""

from typing import List
from typing import Optional

from pydantic.fields import Field

from docs_src.readme._crud import get_wines
from flask_jeroboam import InboundModel
from flask_jeroboam import Jeroboam
from flask_jeroboam import OutboundModel


app = Jeroboam(__name__)


class GenericPagination(InboundModel):
    page: int = Field(1, ge=1)
    per_page: int = Field(10, ge=1, le=100)

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.per_page


class WineOut(OutboundModel):
    cuvee: str
    appellation: str


@app.get("/ping")
def ping():
    return "pong"


@app.get("/wines", response_model=List[WineOut])
def read_wine_list(pagination: GenericPagination, search: Optional[str]):
    wines = get_wines(pagination, search)
    return wines


if __name__ == "__main__":
    app.run(port=5000)
