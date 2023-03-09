"""Flask-Jeroboam Blueprint.

Subclasses the Flask Blueprint.
Can be used as a drop in replacement of any Flask's Blueprint.
"""
from typing import Any
from typing import List
from typing import Optional

from flask.blueprints import Blueprint as FlaskBlueprint

from flask_jeroboam.scaffold import JeroboamScaffoldOverRide


class Blueprint(JeroboamScaffoldOverRide, FlaskBlueprint):  # type:ignore
    """Regular Blueprint with extra behavior on route definition."""

    def __init__(
        self,
        *args: Any,
        tags: Optional[List[str]] = None,
        include_in_openapi: bool = True,
        **kwargs: Any,
    ) -> None:
        """Init."""
        self.include_in_openapi = include_in_openapi
        self.tags = tags or []
        super().__init__(*args, **kwargs)
