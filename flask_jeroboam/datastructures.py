"""DataStructures.

Credits: this module is essentially a for of FastAPI's datastructures.py module.
"""

from typing import Any
from typing import Callable
from typing import Dict
from typing import Iterable
from typing import Type

from werkzeug.datastructures import FileStorage


class UploadFile(FileStorage):
    """A wrapper around werkzeug.datastructures.FileStorage.

    Credits: Adaptation of FastAPI's UploadFile.
    """

    @classmethod
    def __get_validators__(cls: Type["UploadFile"]) -> Iterable[Callable[..., Any]]:
        yield cls.validate

    @classmethod
    def validate(cls: Type["FileStorage"], v: Any) -> Any:
        """Validate the value."""
        if not isinstance(v, FileStorage):
            raise ValueError(f"Expected FileStorage, received: {type(v)}")
        return v

    @classmethod
    def __modify_schema__(cls, field_schema: Dict[str, Any]) -> None:
        field_schema.update({"type": "string", "format": "binary"})
