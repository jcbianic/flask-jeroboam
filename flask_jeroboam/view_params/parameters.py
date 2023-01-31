"""View Parameters.

Subclasses of pydantic.fields.FieldInfo that are used to define
localised fields with some extra information.
"""

from enum import Enum
from typing import Any
from typing import Type

from pydantic.fields import FieldInfo
from pydantic.fields import Undefined


class ParamLocation(Enum):
    """Enum for the possible source location of a view_function parameter."""

    query = "query"
    header = "header"
    path = "path"
    cookie = "cookie"
    body = "body"
    form = "form"
    file = "file"


class ViewParameter(FieldInfo):
    """Base class for all View parameters."""

    location: ParamLocation

    def __init__(
        self,
        default: Any = Undefined,
        **kwargs: Any,
    ):
        self.example = kwargs.pop("example", Undefined)
        self.examples = kwargs.pop("examples", None)
        self.embed = kwargs.pop("embed", False)
        super().__init__(
            default=default,
            **kwargs,
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.default})"

    @property
    def in_body(self):
        """Is the parameter located in the body?"""
        return self.location in {
            ParamLocation.body,
            ParamLocation.form,
            ParamLocation.file,
        }


class NonBodyParameter(ViewParameter):
    """A Parameter that is not located in the body."""

    def __init__(
        self,
        default: Any = Undefined,
        **kwargs: Any,
    ):
        self.deprecated = kwargs.pop("deprecated", None)
        self.include_in_schema = kwargs.pop("include_in_schema", True)
        super().__init__(
            default=default,
            **kwargs,
        )


class QueryParameter(NonBodyParameter):
    """A Parameter found in the Query String."""

    location = ParamLocation.query


class PathParameter(NonBodyParameter):
    """A Parameter found in Path."""

    location = ParamLocation.path

    def __init__(
        self,
        default: Any = Undefined,
        **kwargs: Any,
    ):
        self.required = True
        super().__init__(
            default=...,
            **kwargs,
        )


class HeaderParameter(NonBodyParameter):
    """A Header parameter."""

    location = ParamLocation.header

    def __init__(
        self,
        default: Any = Undefined,
        **kwargs: Any,
    ):
        self.convert_underscores = kwargs.pop("convert_underscores", True)
        super().__init__(
            default=default,
            **kwargs,
        )


class CookieParameter(NonBodyParameter):
    """A Parameter located in Cookies."""

    location = ParamLocation.cookie


class BodyParameter(ViewParameter):
    """A Parameter located in Body.

    Body Parameters can be embedded. which means that they must
    be accessed by their name at the root of the body.
    They also have a Media/Type that varies between body, form and file.
    """

    location = ParamLocation.body

    def __init__(
        self,
        default: Any = Undefined,
        **kwargs: Any,
    ):
        self.embed = kwargs.get("embed", False)
        self.media_type = kwargs.pop("media_type", "application/json")
        super().__init__(
            default=default,
            **kwargs,
        )


class FormParameter(BodyParameter):
    """A Parameter located in Body."""

    location = ParamLocation.form

    def __init__(
        self,
        default: Any = Undefined,
        **kwargs: Any,
    ):
        self.media_type = kwargs.pop("media_type", "application/x-www-form-urlencoded")
        embed = kwargs.pop("embed", True)
        super().__init__(
            default=default,
            embed=embed,
            **kwargs,
        )


class FileParameter(FormParameter):
    """A Parameter located in Body."""

    location = ParamLocation.file

    def __init__(
        self,
        default: Any = Undefined,
        **kwargs: Any,
    ):
        self.media_type = kwargs.pop("media_type", "multipart/form-data")
        embed = kwargs.pop("embed", False)
        super().__init__(
            default=default,
            embed=embed,
            **kwargs,
        )


def get_parameter_class(location: ParamLocation) -> Type[ViewParameter]:
    """Get the Parameter class for a given location."""
    return {
        ParamLocation.query: QueryParameter,
        ParamLocation.header: HeaderParameter,
        ParamLocation.path: PathParameter,
        ParamLocation.cookie: CookieParameter,
        ParamLocation.body: BodyParameter,
        ParamLocation.form: FormParameter,
        ParamLocation.file: FileParameter,
    }[location]
