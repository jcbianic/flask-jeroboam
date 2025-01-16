"""Outbound Models for Testing."""

from dataclasses import dataclass
from typing import List

from flask_jeroboam import OutboundModel


class SimpleModelOut(OutboundModel):
    """Base OutBoundModel for Testing."""

    total_count: int
    items: List[str]


@dataclass
class MyDataClass:
    """A Simple DataClass for Testing."""

    total_count: int
    items: List[str]


class UserOut(OutboundModel):
    """Only the username must be returned."""

    username: str


class UserIn(UserOut):
    """Inbound contains the password."""

    password: str


class ModelWithListOut(OutboundModel):
    """OutboundModel with lists."""

    page: int
    per_page: int
    ids: List[int]
    order: List[dict]
