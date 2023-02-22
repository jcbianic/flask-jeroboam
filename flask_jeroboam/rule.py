"""Augmented Rule for Flask-Jeroboam."""
import re
from typing import Any
from typing import Optional

from werkzeug.routing import Rule as FlaskRule


pattern = re.compile(r"<(\w*):")


class JeroboamRule(FlaskRule):
    """Subclass of werkzeug.routing.Rule."""

    def __init__(
        self, rule: str, endpoint: Optional[str] = None, **options: Any
    ) -> None:
        """Initialize a JeroRule."""
        self.include_in_openapi = endpoint != "static" and options.pop(
            "include_in_openapi", True
        )
        self.tags = options.pop("tags", [])

        # TODO: Maybe a smarter way to extract options...
        self.description = options.pop("description", None)
        self._summary = options.pop("summary", None)
        self.operation_id = options.pop("operation_id", None)
        self.deprecated = options.pop("deprecated", False)
        self.openapi_extra: dict = options.pop("openapi_extra", {})
        main_method = options.pop("main_method", "get")
        super().__init__(rule, endpoint=endpoint, **options)
        self.unique_id = options.pop(
            "unique_id", _generate_unique_id(self, main_method)
        )

    @property
    def openapi_path(self) -> str:
        """Return a formatted path."""
        rule = pattern.sub("<", self.rule)
        return rule.replace("<", "{").replace(">", "}")

    @property
    def summary(self) -> str:
        """Generate summary for the Rule.

        # TODO: Choper la description/summary dans la docstring de la view_function
        """
        return self._summary or self.endpoint.replace("_", " ").title().split(".")[-1]


def _generate_unique_id(rule: "JeroboamRule", main_method: str) -> str:
    def _split(my_string: str):
        return re.sub(r"[\W]+", "_", my_string).split("_")

    view_function_name = rule.endpoint.split(".")[-1]
    blueprints = ".".join(rule.endpoint.split(".")[:-1])
    http_verb = f"{main_method.lower()}"
    words = (
        _split(blueprints)
        + [None if http_verb in view_function_name else http_verb]
        + _split(view_function_name)
    )
    return "_".join([word for word in words if word])
