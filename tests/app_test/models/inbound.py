"""Inbound Models for Testing."""
from typing import List
from typing import Optional

from pydantic import Field

from flask_jeroboam import InboundModel


class SimpleModelIn(InboundModel):
    """Simple InboundModel for Testing Parsing Request."""

    page: int
    type: str


class QueryStringWithList(InboundModel):
    """A List of ids."""

    id: List[int] = Field(alias="id[]")


class OptionalModelIn(InboundModel):
    """a BaseModel with Optional Fields."""

    page: Optional[int]
    per_page: Optional[int]


class ModelWithListIn(InboundModel):
    """InboundModel with lists."""

    page: int
    per_page: int
    ids: List[int] = Field(alias="id[]")
    order: List[dict] = Field(alias="order[]")
