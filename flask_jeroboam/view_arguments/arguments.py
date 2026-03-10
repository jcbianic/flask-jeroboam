"""View Parameters.

Subclasses of pydantic.fields.FieldInfo that are used to define
localised fields with some extra information.
"""

from enum import Enum
from typing import Any

from pydantic.fields import FieldInfo
from pydantic_core import PydanticUndefined


class ArgumentLocation(Enum):
    """Enum for the possible source location of a view_function parameter."""

    query = "query"
    header = "header"
    path = "path"
    cookie = "cookie"
    body = "body"
    form = "form"
    file = "file"
    unknown = "unknown"


class ViewArgument(FieldInfo):  # type: ignore[misc]
    """Base class for all View parameters.

    Inherits from pydantic v2 FieldInfo so that constraints (gt, lt,
    min_length, …) are stored natively and can be applied via
    TypeAdapter(Annotated[annotation, view_arg_instance]).
    """

    location: ArgumentLocation

    def __init__(
        self,
        default: Any = PydanticUndefined,
        **kwargs: Any,
    ):
        # Normalise Ellipsis (used as "required" marker in pydantic v1 style)
        if default is Ellipsis:
            default = PydanticUndefined
        self.embed = kwargs.pop("embed", False)
        self.include_in_schema = kwargs.pop("include_in_schema", True)
        self.example = kwargs.pop("example", PydanticUndefined)
        self.examples = kwargs.pop("examples", None)
        super().__init__(default=default, **kwargs)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.default})"

    @property
    def in_body(self):
        """Is the parameter located in the body?"""
        return self.location in {
            ArgumentLocation.body,
            ArgumentLocation.form,
            ArgumentLocation.file,
        }


class ParameterArgument(ViewArgument):  # type: ignore[misc]
    """A Parameter that is not located in the body."""

    def __init__(
        self,
        default: Any = PydanticUndefined,
        **kwargs: Any,
    ):
        self.deprecated = kwargs.pop("deprecated", None)
        super().__init__(
            default,
            **kwargs,
        )


class QueryArgument(ParameterArgument):  # type: ignore[misc]
    """A Parameter found in the Query String."""

    location = ArgumentLocation.query


class PathArgument(ParameterArgument):  # type: ignore[misc]
    """A Parameter found in Path."""

    location = ArgumentLocation.path

    def __init__(
        self,
        *args: Any,
        **kwargs: Any,
    ):
        # Path params are always required — ignore any supplied default
        super().__init__(
            PydanticUndefined,
            **kwargs,
        )


class HeaderArgument(ParameterArgument):  # type: ignore[misc]
    """A Header parameter."""

    location = ArgumentLocation.header

    def __init__(
        self,
        default: Any = PydanticUndefined,
        **kwargs: Any,
    ):
        self.convert_underscores = kwargs.pop("convert_underscores", True)
        super().__init__(
            default,
            **kwargs,
        )


class CookieArgument(ParameterArgument):  # type: ignore[misc]
    """A Parameter located in Cookies."""

    location = ArgumentLocation.cookie


class BodyArgument(ViewArgument):  # type: ignore[misc]
    """A Parameter located in Body.

    Body Parameters can be embedded. which means that they must
    be accessed by their name at the root of the body.
    They also have a Media/Type that varies between body, form and file.
    """

    location = ArgumentLocation.body

    def __init__(
        self,
        default: Any = PydanticUndefined,
        **kwargs: Any,
    ):
        self.media_type = kwargs.pop("media_type", "application/json")
        super().__init__(
            default,
            **kwargs,
        )


class FormArgument(BodyArgument):  # type: ignore[misc]
    """A Parameter located in Body."""

    location = ArgumentLocation.form

    def __init__(
        self,
        default: Any = PydanticUndefined,
        **kwargs: Any,
    ):
        embed = kwargs.pop("embed", True)
        kwargs.setdefault("media_type", "application/x-www-form-urlencoded")
        super().__init__(
            default,
            embed=embed,
            **kwargs,
        )


class FileArgument(FormArgument):  # type: ignore[misc]
    """A Parameter located in Body."""

    location = ArgumentLocation.file

    def __init__(
        self,
        default: Any = PydanticUndefined,
        **kwargs: Any,
    ):
        embed = kwargs.pop("embed", False)
        kwargs.setdefault("media_type", "multipart/form-data")
        super().__init__(
            default,
            embed=embed,
            **kwargs,
        )


def get_argument_class(location: ArgumentLocation) -> type[ViewArgument]:
    """Get the Parameter class for a given location."""
    return {
        ArgumentLocation.query: QueryArgument,
        ArgumentLocation.header: HeaderArgument,
        ArgumentLocation.path: PathArgument,
        ArgumentLocation.cookie: CookieArgument,
        ArgumentLocation.body: BodyArgument,
        ArgumentLocation.form: FormArgument,
        ArgumentLocation.file: FileArgument,
    }[location]
