"""Function to declare the Type of Parameters.

This functions are used to declare the parameters of the view functions.
By annotating the return value with Any, we make sure that the code editor
don't complain about assigning a default value of type ViewParameter
to a parameter that have been annotated with a pydantic-compatible type...
They're primary purprose is to trick the code editor as they only delegate
to actual ViewParameter instantiers.
Their signature are defined in adjacent file functions.pyi.

Credits: This module is a fork of FlaskAPI params_function module.
"""

from typing import Any

from flask_jeroboam.view_arguments.arguments import BodyArgument
from flask_jeroboam.view_arguments.arguments import CookieArgument
from flask_jeroboam.view_arguments.arguments import FileArgument
from flask_jeroboam.view_arguments.arguments import FormArgument
from flask_jeroboam.view_arguments.arguments import HeaderArgument
from flask_jeroboam.view_arguments.arguments import PathArgument
from flask_jeroboam.view_arguments.arguments import QueryArgument


def Path(  # noqa:N802
    *args: Any,
    **kwargs: Any,
) -> Any:
    """Declare A Path parameter."""
    return PathArgument(
        *args,
        **kwargs,
    )


def Query(  # noqa:N802
    *args: Any,
    **kwargs: Any,
) -> Any:
    """Declare A Query parameter."""
    return QueryArgument(
        *args,
        **kwargs,
    )


def Header(  # noqa:N802
    *args: Any,
    **kwargs: Any,
) -> Any:
    """Declare A Header parameter."""
    return HeaderArgument(
        *args,
        **kwargs,
    )


def Cookie(  # noqa:N802
    *args: Any,
    **kwargs: Any,
) -> Any:
    """Declare A Cookie parameter."""
    return CookieArgument(
        *args,
        **kwargs,
    )


def Body(  # noqa:N802
    *args: Any,
    **kwargs: Any,
) -> Any:
    """Declare A Body parameter."""
    return BodyArgument(
        *args,
        **kwargs,
    )


def Form(  # noqa: N802
    *args: Any,
    **kwargs: Any,
) -> Any:
    """Declare A Form parameter."""
    return FormArgument(
        *args,
        **kwargs,
    )


def File(  # noqa: N802
    *args: Any,
    **kwargs: Any,
) -> Any:
    """Declare A File parameter."""
    return FileArgument(
        *args,
        **kwargs,
    )
