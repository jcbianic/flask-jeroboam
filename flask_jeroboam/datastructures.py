"""Helper DataStructure."""

from typing import Any
from typing import Callable
from typing import Dict
from typing import Iterable
from typing import Type

from werkzeug.datastructures import FileStorage


class UploadFile(FileStorage):
    """A wrapper around werkzeug.datastructures.FileStorage."""

    @classmethod
    def __get_validators__(cls: Type["FileStorage"]) -> Iterable[Callable[..., Any]]:
        yield cls.validate

    @classmethod
    def validate(cls: Type["FileStorage"], v: Any) -> Any:
        if not isinstance(v, FileStorage):
            raise ValueError(f"Expected UploadFile, received: {type(v)}")
        return v

    @classmethod
    def __modify_schema__(cls, field_schema: Dict[str, Any]) -> None:
        field_schema.update({"type": "string", "format": "binary"})


class DefaultPlaceholder:
    """
    You shouldn't use this class directly.

    It's used internally to recognize when a default value has been overwritten, even
    if the overridden default value was truthy.
    """

    def __init__(self, value: Any):
        self.value = value

    def __bool__(self) -> bool:
        return bool(self.value)

    def __eq__(self, o: object) -> bool:
        return isinstance(o, DefaultPlaceholder) and o.value == self.value
