from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable, List

from app.context import SystemContext


@dataclass(frozen=True)
class RouteResult:
    handled: bool
    frames: tuple[bytes, ...] = ()
    changed: bool = False
    reason: str = ''

    @classmethod
    def handled(
        cls,
        frames: Iterable[bytes] = (),
        *,
        changed: bool = False,
        reason: str = '',
    ) -> 'RouteResult':
        return cls(True, tuple(frames), changed, reason)

    @classmethod
    def not_handled(cls, *, reason: str = '') -> 'RouteResult':
        return cls(False, (), False, reason)


RoutePredicate = Callable[[SystemContext, int, List[object]], bool]
RouteHandler = Callable[[SystemContext, int, List[object]], RouteResult]


@dataclass(frozen=True)
class SystemRoute:
    name: str
    predicate: RoutePredicate
    handler: RouteHandler


class SystemRouter:
    """Ordered protocol router for independent game systems."""

    def __init__(self) -> None:
        self._routes: list[SystemRoute] = []
        self._names: set[str] = set()

    def register(self, name: str, predicate: RoutePredicate, handler: RouteHandler) -> None:
        if not name:
            raise ValueError('system route name is required')
        if name in self._names:
            raise ValueError(f'duplicate system route: {name}')
        self._routes.append(SystemRoute(name, predicate, handler))
        self._names.add(name)

    def dispatch(self, context: SystemContext, message_id: int, values: list[object]) -> RouteResult:
        for route in self._routes:
            if route.predicate(context, message_id, values):
                return route.handler(context, message_id, values)
        return RouteResult.not_handled()

    @property
    def routes(self) -> tuple[SystemRoute, ...]:
        return tuple(self._routes)
