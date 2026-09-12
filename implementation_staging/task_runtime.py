"""Task-system orchestration shared by server routing and tests."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, Sequence

from protocol import Field
from task_protocol import (
    active_task_list_frame,
    available_task_list_frame,
    detail_request_task_id,
    is_active_list_request,
    is_available_list_request,
    parse_task_1145_request,
    parse_task_operation_request,
    safe_detail_ack_frame,
)
from task_registry import TaskDefinition, TaskRegistry
from task_service import (
    abandon_task,
    accept_task,
    available_tasks,
    claim_task,
    ensure_task_state,
    record_event as update_task_progress,
)


@dataclass(frozen=True)
class TaskRuntimeResult:
    frames: tuple[bytes, ...]
    changed: bool
    handled: bool = True
    reason: str = ''


RewardApplier = Callable[[Dict[str, object], TaskDefinition], bool]


class TaskRuntime:
    """Bridge pure task state and the APK's task protocol without persistence."""

    def __init__(self, registry: TaskRegistry) -> None:
        self.registry = registry

    def migrate_role(self, role: dict[str, object], *, today: str | None = None) -> bool:
        return ensure_task_state(role, today=today)

    def _active_entries(self, role: dict[str, object], category_wire_id: int):
        state = role.get('tasks')
        active = state.get('active') if isinstance(state, dict) else None
        active = active if isinstance(active, dict) else {}
        entries: list[tuple[TaskDefinition, str]] = []
        for task in self.registry.all_tasks():
            if task.category_wire_id != int(category_wire_id):
                continue
            record = active.get(str(task.task_id))
            if not isinstance(record, dict):
                continue
            status = str(record.get('status', 'active'))
            if status not in {'active', 'ready'}:
                continue
            entries.append((task, status))
        return tuple(entries)

    def _available_list_entries(
        self,
        role: dict[str, object],
        *,
        today: str | None = None,
    ) -> tuple[tuple[TaskDefinition, int], ...]:
        """Return rows with the status numbers consumed by e/en and e/ca.

        APK meanings are 0=locked, 1=claimable, 2=active, 3=ready to submit,
        4=delivered. Repeatable tasks become claimable again after a claim, so
        availability takes precedence over historical completion.
        """
        ensure_task_state(role, today=today)
        state = role.get('tasks')
        assert isinstance(state, dict)
        active = state.get('active')
        active = active if isinstance(active, dict) else {}
        completed = state.get('completed')
        completed = completed if isinstance(completed, dict) else {}
        available_ids = {
            task.task_id
            for task in available_tasks(role, self.registry, today=today)
        }
        rows: list[tuple[TaskDefinition, int]] = []
        for task in self.registry.all_tasks():
            record = active.get(str(task.task_id))
            if isinstance(record, dict):
                status = 3 if record.get('status') == 'ready' else 2
            elif task.task_id in available_ids:
                status = 1
            else:
                try:
                    completed_count = max(0, int(completed.get(str(task.task_id), 0)))
                except (TypeError, ValueError):
                    completed_count = 0
                status = 4 if completed_count > 0 else 0
            rows.append((task, status))
        return tuple(rows)

    def active_snapshot_frames(self, role: dict[str, object]) -> tuple[bytes, ...]:
        return tuple(
            active_task_list_frame(wire_id, self._active_entries(role, wire_id))
            for wire_id in (1, 2, 3, 4, 6)
        )

    def snapshot_frames(self, role: dict[str, object], *, today: str | None = None) -> tuple[bytes, ...]:
        ensure_task_state(role, today=today)
        return (
            available_task_list_frame(self._available_list_entries(role, today=today)),
            *self.active_snapshot_frames(role),
        )

    def handle_1403(
        self,
        role: dict[str, object],
        fields: Sequence[Field],
        *,
        today: str | None = None,
    ) -> TaskRuntimeResult:
        migrated = ensure_task_state(role, today=today)
        if is_available_list_request(fields):
            return TaskRuntimeResult(
                (available_task_list_frame(self._available_list_entries(role, today=today)),),
                migrated,
            )
        if is_active_list_request(fields):
            return TaskRuntimeResult(self.active_snapshot_frames(role), migrated)
        if detail_request_task_id(fields) is not None:
            return TaskRuntimeResult((safe_detail_ack_frame(),), migrated, reason='detail_layout_untraced')
        if parse_task_operation_request(fields) is not None:
            return TaskRuntimeResult((safe_detail_ack_frame(),), migrated, reason='operation_1403_untraced')
        return TaskRuntimeResult((safe_detail_ack_frame(),), migrated, reason='unknown_1403_action')

    def _route_task(self, route_id: int, category: int, route_kind: int | None = None) -> TaskDefinition | None:
        for task in self.registry.all_tasks():
            if task.client_route.route_id != int(route_id):
                continue
            if task.category_wire_id != int(category):
                continue
            if route_kind is not None and task.client_route.route_kind != int(route_kind):
                continue
            return task
        return None

    def matches_1145(self, fields: Sequence[Field]) -> bool:
        """Return True only when an ambiguous 1145 payload names a real task route.

        Gathering pathfinding uses the same four TLV types as the historical
        compatibility task route. Wire shape alone therefore cannot own the
        message; route/category values must resolve against this catalog.
        """
        request = parse_task_1145_request(fields)
        if request is None:
            return False
        if request.variant == 'available':
            return self._route_task(
                request.route_id, request.category, request.route_kind
            ) is not None
        task = self.registry.get(request.task_id)
        return bool(
            task is not None
            and task.client_route.route_id == request.route_id
            and task.category_wire_id == request.category
        )

    def handle_1145(
        self,
        role: dict[str, object],
        fields: Sequence[Field],
        *,
        reward_applier: RewardApplier | None = None,
        now: int | float = 0,
        today: str | None = None,
    ) -> TaskRuntimeResult | None:
        request = parse_task_1145_request(fields)
        if request is None or not self.matches_1145(fields):
            return None
        migrated = ensure_task_state(role, today=today)
        if request.variant == 'available':
            task = self._route_task(request.route_id, request.category, request.route_kind)
            assert task is not None
            action = accept_task(role, self.registry, task.task_id, now=now, today=today)
            return TaskRuntimeResult(
                self.snapshot_frames(role, today=today),
                migrated or action.changed,
                reason=action.reason,
            )

        task = self.registry.get(request.task_id)
        assert task is not None
        if request.operation == 4:
            action = abandon_task(role, self.registry, task.task_id, today=today)
        elif request.operation == 2:
            action = claim_task(
                role,
                self.registry,
                task.task_id,
                reward_applier=reward_applier,
                now=now,
                today=today,
            )
        else:
            return TaskRuntimeResult(self.snapshot_frames(role, today=today), migrated, reason='unsupported_operation')
        return TaskRuntimeResult(
            self.snapshot_frames(role, today=today),
            migrated or action.changed,
            reason=action.reason,
        )

    def record_event(
        self,
        role: dict[str, object],
        kind: str,
        *,
        target_id: int = 0,
        amount: int = 1,
        now: int | float = 0,
        today: str | None = None,
    ) -> TaskRuntimeResult:
        migrated = ensure_task_state(role, today=today)
        changed_ids = update_task_progress(
            role,
            self.registry,
            kind,
            target_id=target_id,
            amount=amount,
            now=now,
            today=today,
        )
        changed = migrated or bool(changed_ids)
        return TaskRuntimeResult(
            self.snapshot_frames(role, today=today) if changed_ids else (),
            changed,
            reason=','.join(str(task_id) for task_id in changed_ids),
        )
