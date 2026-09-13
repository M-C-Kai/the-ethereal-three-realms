from __future__ import annotations

from typing import Callable

from app.context import SystemContext
from app.router import RouteResult, SystemRouter
from systems.inventory.registry import ItemRegistry
from protocol import Field
from systems.task.service import TaskRuntimeResult
from systems.task.service import TaskServerSupport, default_task_server_support


SaveRoles = Callable[[], None]


class TaskSystem:
    """任务系统边界：负责协议入口、任务运行时和持久化策略的组合。"""

    system_name = 'task'

    def __init__(self, item_registry: ItemRegistry, save_roles: SaveRoles) -> None:
        self.support: TaskServerSupport = default_task_server_support(item_registry)
        self.runtime = self.support.runtime
        self._save_roles = save_roles

    def _persist_changed_result(self, result: TaskRuntimeResult) -> tuple[bytes, ...]:
        if result.changed:
            self._save_roles()
        return result.frames

    def handle_1403(
        self,
        role: dict[str, object],
        fields: list[Field],
        *,
        now: int | float = 0,
        today: str | None = None,
    ) -> tuple[bytes, ...]:
        result = self.runtime.handle_1403(role, fields, now=now, today=today)
        return self._persist_changed_result(result)

    def handle_1145(
        self,
        role: dict[str, object],
        fields: list[Field],
        *,
        now: int | float = 0,
        today: str | None = None,
    ) -> tuple[bytes, ...] | None:
        result = self.runtime.handle_1145(
            role,
            fields,
            reward_applier=self.support.apply_rewards,
            now=now,
            today=today,
        )
        if result is None:
            return None
        return self._persist_changed_result(result)

    def record_event(
        self,
        role: dict[str, object],
        kind: str,
        *,
        target_id: int = 0,
        amount: int = 1,
        now: int | float = 0,
        today: str | None = None,
    ) -> tuple[bytes, ...]:
        result = self.runtime.record_event(
            role,
            kind,
            target_id=target_id,
            amount=amount,
            now=now,
            today=today,
        )
        return self._persist_changed_result(result)

    def matches_1145(self, fields: list[Field]) -> bool:
        return self.runtime.matches_1145(fields)

    def matches_path_target(self, map_id: int, x: int, y: int) -> bool:
        return self.runtime.matches_path_target(map_id, x, y)

    def route_1403(
        self,
        context: SystemContext,
        _message_id: int,
        fields: list[Field],
    ) -> RouteResult:
        if context.active_role is None:
            return RouteResult.not_handled('missing active role')
        frames = self.handle_1403(
            context.active_role,
            fields,
            now=context.session.get('now', 0),
            today=context.session.get('today'),
        )
        return RouteResult.handled(frames)

    def route_1145(
        self,
        context: SystemContext,
        _message_id: int,
        fields: list[Field],
    ) -> RouteResult:
        if context.active_role is None:
            return RouteResult.not_handled('missing active role')
        frames = self.handle_1145(
            context.active_role,
            fields,
            now=context.session.get('now', 0),
            today=context.session.get('today'),
        )
        if frames is None:
            return RouteResult.not_handled('not a task 1145 payload')
        return RouteResult.handled(frames)


def register_task_routes(router: SystemRouter, task_system: TaskSystem) -> None:
    router.register(
        'task.1403',
        lambda context, message_id, _fields: message_id == 1403 and context.active_role is not None,
        task_system.route_1403,
    )
    router.register(
        'task.1145',
        lambda context, message_id, fields: (
            message_id == 1145
            and context.active_role is not None
            and task_system.matches_1145(fields)
        ),
        task_system.route_1145,
    )
