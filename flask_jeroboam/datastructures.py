"""DataStructures.

Credits: this module is essentially a for of FastAPI's datastructures.py module.
"""

from collections.abc import Callable, Iterable
from typing import Any

from werkzeug.datastructures import FileStorage


class UploadFile(FileStorage):
    """A wrapper around werkzeug.datastructures.FileStorage.

    Credits: Adaptation of FastAPI's UploadFile.
    """

    @classmethod
    def __get_validators__(cls: type["UploadFile"]) -> Iterable[Callable[..., Any]]:
        yield cls.validate

    @classmethod
    def validate(cls: type["FileStorage"], v: Any) -> Any:
        """Validate the value."""
        if not isinstance(v, FileStorage):
            raise ValueError(f"Expected FileStorage, received: {type(v)}")
        return v

    @classmethod
    def __modify_schema__(cls, field_schema: dict[str, Any]) -> None:
        field_schema.update({"type": "string", "format": "binary"})
