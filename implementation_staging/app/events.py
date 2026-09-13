from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class SystemEvent:
    name: str
    payload: dict[str, Any]


EventHandler = Callable[[SystemEvent], Any]


class EventBus:
    """In-process event bus for cross-system side effects."""

    def __init__(self) -> None:
        self._subscribers: dict[str, list[EventHandler]] = defaultdict(list)

    def subscribe(self, event_name: str, handler: EventHandler) -> None:
        if not event_name:
            raise ValueError('event_name is required')
        self._subscribers[event_name].append(handler)

    def publish(self, event_name: str, **payload: Any) -> tuple[Any, ...]:
        event = SystemEvent(event_name, dict(payload))
        return tuple(handler(event) for handler in self._subscribers.get(event_name, ()))

