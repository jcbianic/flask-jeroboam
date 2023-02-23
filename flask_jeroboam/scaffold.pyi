from typing import Any
from typing import Callable

from flask_jeroboam.typing import JeroboamRouteCallable

class JeroboamScaffoldOverRide:
    def route(
        self, rule: str, **options: Any
    ) -> Callable[[JeroboamRouteCallable], JeroboamRouteCallable]: ...
    def get(
        self, rule: str, **options: Any
    ) -> Callable[[JeroboamRouteCallable], JeroboamRouteCallable]: ...
    def post(
        self, rule: str, **options: Any
    ) -> Callable[[JeroboamRouteCallable], JeroboamRouteCallable]: ...
    def put(
        self, rule: str, **options: Any
    ) -> Callable[[JeroboamRouteCallable], JeroboamRouteCallable]: ...
    def delete(
        self, rule: str, **options: Any
    ) -> Callable[[JeroboamRouteCallable], JeroboamRouteCallable]: ...
    def patch(
        self, rule: str, **options: Any
    ) -> Callable[[JeroboamRouteCallable], JeroboamRouteCallable]: ...
    def _method_route(
        self,
        method: str,
        rule: str,
        options: dict,
    ) -> Callable[[JeroboamRouteCallable], JeroboamRouteCallable]: ...
