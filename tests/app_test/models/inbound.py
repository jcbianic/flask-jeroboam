"""Inbound Models for Testing."""

from pydantic import Field, validator

from flask_jeroboam import InboundModel


class SimpleModelIn(InboundModel):
    """Simple InboundModel for Testing Parsing Request."""

    page: int
    type: str


class QueryStringWithList(InboundModel):
    """A List of ids."""

    id: list[int] = Field(alias="id[]")


class OptionalModelIn(InboundModel):
    """a BaseModel with Optional Fields."""

    page: int | None = None
    per_page: int | None = None


class ModelWithListIn(InboundModel):
    """InboundModel with lists."""

    page: int
    per_page: int
    ids: list[int] = Field(alias="id[]")
    order: list[dict] = Field(alias="order[]")

    @validator("order")
    def order_validator(cls, value):  # noqa: B902,N805
        """Validate order."""
        if len(value) == 0:
            raise ValueError("Order must have at least 1 value")
        return value
