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

from flask_jeroboam.view_params.parameters import BodyParameter
from flask_jeroboam.view_params.parameters import CookieParameter
from flask_jeroboam.view_params.parameters import FileParameter
from flask_jeroboam.view_params.parameters import FormParameter
from flask_jeroboam.view_params.parameters import HeaderParameter
from flask_jeroboam.view_params.parameters import PathParameter
from flask_jeroboam.view_params.parameters import QueryParameter


def Path(  # noqa:N802
    *args: Any,
    **kwargs: Any,
) -> Any:
    """Declare A Path parameter."""
    return PathParameter(
        *args,
        **kwargs,
    )


def Query(  # noqa:N802
    *args: Any,
    **kwargs: Any,
) -> Any:
    """Declare A Query parameter."""
    return QueryParameter(
        *args,
        **kwargs,
    )


def Header(  # noqa:N802
    *args: Any,
    **kwargs: Any,
) -> Any:
    """Declare A Header parameter."""
    return HeaderParameter(
        *args,
        **kwargs,
    )


def Cookie(  # noqa:N802
    *args: Any,
    **kwargs: Any,
) -> Any:
    """Declare A Cookie parameter."""
    return CookieParameter(
        *args,
        **kwargs,
    )


def Body(  # noqa:N802
    *args: Any,
    **kwargs: Any,
) -> Any:
    """Declare A Body parameter."""
    return BodyParameter(
        *args,
        **kwargs,
    )


def Form(  # noqa: N802
    *args: Any,
    **kwargs: Any,
) -> Any:
    """Declare A Form parameter."""
    return FormParameter(
        *args,
        **kwargs,
    )


def File(  # noqa: N802
    *args: Any,
    **kwargs: Any,
) -> Any:
    """Declare A File parameter."""
    return FileParameter(
        *args,
        **kwargs,
    )
