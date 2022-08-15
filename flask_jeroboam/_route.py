import typing as t

from flask.scaffold import Scaffold

from flask_jeroboam._parser import parser
from flask_jeroboam._serializer import serializer


F = t.TypeVar("F", bound=t.Callable[..., t.Any])


def route(self: Scaffold, rule: str, **options: t.Any) -> t.Callable[[F], F]:
    """Route Registration Override."""

    def decorator(f: F) -> F:
        endpoint = options.pop("endpoint", None)
        reponse_model = options.pop("response_model", None)
        method = options.get("methods", ["GET"])[0]
        status_code = options.pop("status_code", 200)
        if reponse_model is not None:
            f = serializer(reponse_model, status_code)(f)
        f = parser(method=method)(f)
        self.add_url_rule(rule, endpoint, f, **options)
        return f

    return decorator
