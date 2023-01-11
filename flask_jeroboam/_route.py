import typing as t
from typing import Optional
from typing import Type

from flask.scaffold import Scaffold
from pydantic import BaseModel

from flask_jeroboam._parser import parser
from flask_jeroboam._serializer import serializer


R = t.TypeVar("R", bound=t.Any)


def route(
    self: Scaffold, rule: str, **options: t.Any
) -> t.Callable[[t.Callable[..., R]], t.Callable[..., R]]:
    """Route Registration Override."""

    def decorator(f: t.Callable[..., R]) -> t.Callable[..., R]:
        endpoint = options.pop("endpoint", None)
        reponse_model: Optional[Type[BaseModel]] = options.pop("response_model", None)
        method = options.get("methods", ["GET"])[0]
        options["methods"] = [method]
        status_code = options.pop("status_code", 200)
        if reponse_model is not None:
            f = serializer(reponse_model, status_code)(f)  # type: ignore
        f = parser(method=method, rule=rule)(f)
        self.add_url_rule(rule, endpoint, f, **options)
        return f

    return decorator
