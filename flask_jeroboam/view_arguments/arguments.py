"""View Parameters.

Subclasses of pydantic.fields.FieldInfo that are used to define
localised fields with some extra information.
"""

from enum import Enum
from typing import Any
from typing import Type

from pydantic.fields import FieldInfo
from pydantic.fields import Undefined


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


class ViewArgument(FieldInfo):
    """Base class for all View parameters."""

    location: ArgumentLocation

    def __init__(
        self,
        default: Any = Undefined,
        **kwargs: Any,
    ):
        self.example = kwargs.pop("example", Undefined)
        self.examples = kwargs.pop("examples", None)
        self.embed = kwargs.pop("embed", False)
        self.include_in_schema = kwargs.get("include_in_schema", True)
        super().__init__(
            default,
            **kwargs,
        )

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


class ParameterArgument(ViewArgument):
    """A Parameter that is not located in the body."""

    def __init__(
        self,
        default: Any = Undefined,
        **kwargs: Any,
    ):
        self.deprecated = kwargs.pop("deprecated", None)
        super().__init__(
            default,
            **kwargs,
        )


class QueryArgument(ParameterArgument):
    """A Parameter found in the Query String."""

    location = ArgumentLocation.query


class PathArgument(ParameterArgument):
    """A Parameter found in Path."""

    location = ArgumentLocation.path

    def __init__(
        self,
        *args: Any,
        **kwargs: Any,
    ):
        super().__init__(
            ...,
            **kwargs,
        )
        self.required = True


class HeaderArgument(ParameterArgument):
    """A Header parameter."""

    location = ArgumentLocation.header

    def __init__(
        self,
        default: Any = Undefined,
        **kwargs: Any,
    ):
        self.convert_underscores = kwargs.pop("convert_underscores", True)
        super().__init__(
            default,
            **kwargs,
        )


class CookieArgument(ParameterArgument):
    """A Parameter located in Cookies."""

    location = ArgumentLocation.cookie


class BodyArgument(ViewArgument):
    """A Parameter located in Body.

    Body Parameters can be embedded. which means that they must
    be accessed by their name at the root of the body.
    They also have a Media/Type that varies between body, form and file.
    """

    location = ArgumentLocation.body

    def __init__(
        self,
        default: Any = Undefined,
        **kwargs: Any,
    ):
        self.embed = kwargs.get("embed", False)
        self.media_type = kwargs.pop("media_type", "application/json")
        super().__init__(
            default,
            **kwargs,
        )


class FormArgument(BodyArgument):
    """A Parameter located in Body."""

    location = ArgumentLocation.form

    def __init__(
        self,
        default: Any = Undefined,
        **kwargs: Any,
    ):
        embed = kwargs.pop("embed", True)
        kwargs.setdefault("media_type", "application/x-www-form-urlencoded")
        super().__init__(
            default,
            embed=embed,
            **kwargs,
        )


class FileArgument(FormArgument):
    """A Parameter located in Body."""

    location = ArgumentLocation.file

    def __init__(
        self,
        default: Any = Undefined,
        **kwargs: Any,
    ):
        embed = kwargs.pop("embed", False)
        kwargs.setdefault("media_type", "multipart/form-data")
        super().__init__(
            default,
            embed=embed,
            **kwargs,
        )


def get_argument_class(location: ArgumentLocation) -> Type[ViewArgument]:
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
