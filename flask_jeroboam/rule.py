"""Augmented Rule for Flask-Jeroboam."""
import re
from typing import Any
from typing import Optional
from typing import Type

from flask.wrappers import Response
from werkzeug.routing import Rule

from flask_jeroboam.datastructures import DefaultPlaceholder


pattern = re.compile(r"<(\w*):")


class JeroRule(Rule):
    """Subclass of werkzeug.routing.Rule."""

    def __init__(
        self, rule: str, endpoint: Optional[str] = None, **options: Any
    ) -> None:
        """Initialize a JeroRule."""
        self.include_in_openapi = options.pop(
            "include_in_openapi", "static" not in rule
        )
        self.tags = options.pop("tags", [])
        # TODO: Choper la description dans la docstring
        self.description = options.pop("description", None)
        self.summary = options.pop("summary", None)
        self.operation_id = options.pop("operation_id", None)
        self.deprecated = options.pop("deprecated", False)
        self.openapi_extra = options.pop("deprecated", False)
        super().__init__(rule, endpoint=endpoint, **options)
        self.unique_id = options.pop("unique_id", _generate_unique_id(self))

    @property
    def path_format(self) -> str:
        """Return a formatted path."""
        rule = pattern.sub("<", self.rule)
        return rule.replace("<", "{").replace(">", "}")

    @property
    def current_response_class(self) -> Type[Response]:
        """Return the current response class."""
        attached_response_class = getattr(self, "response_class", Response)
        if isinstance(attached_response_class, DefaultPlaceholder):
            current: Type[Response] = attached_response_class.value
        else:
            current = attached_response_class
        return current


def _generate_unique_id(rule: "JeroRule") -> str:
    operation_id = rule.endpoint + rule.path_format
    operation_id = re.sub(r"\W", "_", operation_id)
    operation_id = operation_id + "_" + list(rule.methods or [])[0].lower()
    return operation_id
