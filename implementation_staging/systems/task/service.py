"""任务系统业务：状态流转、运行时与服务器侧奖励粘合。"""
from __future__ import annotations

"""Persistent task state machine independent from network protocol details."""

from dataclasses import dataclass
from datetime import date
from typing import Callable

from systems.task.registry import TaskDefinition, TaskRegistry


@dataclass(frozen=True)
class TaskActionResult:
    ok: bool
    changed: bool
    task_id: int
    status: str
    reason: str = ''


def _today(today: str | None) -> str:
    return str(today) if today is not None else date.today().isoformat()


def ensure_task_state(role: dict[str, object], *, today: str | None = None) -> bool:
    """Migrate/normalize the role task container without touching other fields."""
    current_day = _today(today)
    changed = False
    state = role.get('tasks')
    if not isinstance(state, dict):
        state = {}
        role['tasks'] = state
        changed = True
    if state.get('version') != 1:
        state['version'] = 1
        changed = True
    if not isinstance(state.get('active'), dict):
        state['active'] = {}
        changed = True
    if not isinstance(state.get('completed'), dict):
        state['completed'] = {}
        changed = True
    daily = state.get('daily')
    if not isinstance(daily, dict):
        daily = {'date': current_day, 'counts': {}}
        state['daily'] = daily
        changed = True
    if daily.get('date') != current_day:
        daily['date'] = current_day
        daily['counts'] = {}
        changed = True
    elif not isinstance(daily.get('counts'), dict):
        daily['counts'] = {}
        changed = True
    return changed


def _state(role: dict[str, object]) -> dict[str, object]:
    state = role['tasks']
    assert isinstance(state, dict)
    return state


def _active(role: dict[str, object]) -> dict[str, object]:
    active = _state(role)['active']
    assert isinstance(active, dict)
    return active


def _completed(role: dict[str, object]) -> dict[str, object]:
    completed = _state(role)['completed']
    assert isinstance(completed, dict)
    return completed


def _daily_counts(role: dict[str, object]) -> dict[str, object]:
    daily = _state(role)['daily']
    assert isinstance(daily, dict)
    counts = daily['counts']
    assert isinstance(counts, dict)
    return counts


def _completed_count(role: dict[str, object], task_id: int) -> int:
    raw = _completed(role).get(str(int(task_id)), 0)
    try:
        return max(0, int(raw))
    except (TypeError, ValueError):
        return 0


def _daily_count(role: dict[str, object], task_id: int) -> int:
    raw = _daily_counts(role).get(str(int(task_id)), 0)
    try:
        return max(0, int(raw))
    except (TypeError, ValueError):
        return 0


def _is_available(role: dict[str, object], task: TaskDefinition) -> bool:
    key = str(task.task_id)
    if key in _active(role):
        return False
    if int(role.get('level', 1)) < task.level_requirement:
        return False
    if any(_completed_count(role, prerequisite) < 1 for prerequisite in task.prerequisites):
        return False
    if task.repeat_policy == 'once' and _completed_count(role, task.task_id) > 0:
        return False
    if task.repeat_policy == 'daily' and _daily_count(role, task.task_id) >= task.daily_limit:
        return False
    return True


def available_tasks(
    role: dict[str, object],
    registry: TaskRegistry,
    *,
    today: str | None = None,
) -> tuple[TaskDefinition, ...]:
    ensure_task_state(role, today=today)
    return tuple(task for task in registry.all_tasks() if _is_available(role, task))


def accept_task(
    role: dict[str, object],
    registry: TaskRegistry,
    task_id: int,
    *,
    now: int | float = 0,
    today: str | None = None,
) -> TaskActionResult:
    ensure_task_state(role, today=today)
    task = registry.get(task_id)
    if task is None:
        return TaskActionResult(False, False, int(task_id), 'unavailable', 'unknown_task')
    if not _is_available(role, task):
        return TaskActionResult(False, False, task.task_id, 'unavailable', 'not_available')
    cycle_count = _completed_count(role, task.task_id)
    _active(role)[str(task.task_id)] = {
        'status': 'active',
        'progress': [0 for _ in task.objectives],
        'accepted_at': int(now),
        'completed_at': 0,
        'cycle_count': cycle_count,
    }
    return TaskActionResult(True, True, task.task_id, 'active')


def abandon_task(
    role: dict[str, object],
    registry: TaskRegistry,
    task_id: int,
    *,
    today: str | None = None,
) -> TaskActionResult:
    ensure_task_state(role, today=today)
    task = registry.get(task_id)
    if task is None:
        return TaskActionResult(False, False, int(task_id), 'missing', 'unknown_task')
    record = _active(role).get(str(task.task_id))
    if not isinstance(record, dict) or record.get('status') not in {'active', 'ready'}:
        return TaskActionResult(False, False, task.task_id, 'missing', 'not_active')
    del _active(role)[str(task.task_id)]
    return TaskActionResult(True, True, task.task_id, 'available')


def record_event(
    role: dict[str, object],
    registry: TaskRegistry,
    kind: str,
    *,
    target_id: int = 0,
    amount: int = 1,
    now: int | float = 0,
    today: str | None = None,
) -> tuple[int, ...]:
    ensure_task_state(role, today=today)
    if int(amount) <= 0:
        return ()
    changed_ids: list[int] = []
    active = _active(role)
    for key, raw_record in list(active.items()):
        if not isinstance(raw_record, dict) or raw_record.get('status') != 'active':
            continue
        try:
            task_id = int(key)
        except (TypeError, ValueError):
            continue
        task = registry.get(task_id)
        if task is None:
            continue
        raw_progress = raw_record.get('progress')
        progress = list(raw_progress) if isinstance(raw_progress, list) else [0] * len(task.objectives)
        if len(progress) != len(task.objectives):
            progress = [0] * len(task.objectives)
        changed = False
        for index, objective in enumerate(task.objectives):
            if objective.kind != kind:
                continue
            if objective.target_id not in (0, int(target_id)):
                continue
            try:
                old_value = max(0, int(progress[index]))
            except (TypeError, ValueError):
                old_value = 0
            new_value = min(objective.required, old_value + int(amount))
            if new_value != old_value:
                progress[index] = new_value
                changed = True
        if not changed:
            continue
        raw_record['progress'] = progress
        if all(int(progress[index]) >= objective.required for index, objective in enumerate(task.objectives)):
            raw_record['status'] = 'ready'
            raw_record['completed_at'] = int(now)
        changed_ids.append(task.task_id)
    return tuple(changed_ids)


def claim_task(
    role: dict[str, object],
    registry: TaskRegistry,
    task_id: int,
    *,
    reward_applier: Callable[[dict[str, object], TaskDefinition], bool] | None = None,
    now: int | float = 0,
    today: str | None = None,
) -> TaskActionResult:
    ensure_task_state(role, today=today)
    task = registry.get(task_id)
    if task is None:
        return TaskActionResult(False, False, int(task_id), 'missing', 'unknown_task')
    key = str(task.task_id)
    record = _active(role).get(key)
    if not isinstance(record, dict) or record.get('status') != 'ready':
        return TaskActionResult(False, False, task.task_id, 'active', 'not_ready')
    if reward_applier is not None and not bool(reward_applier(role, task)):
        return TaskActionResult(False, False, task.task_id, 'ready', 'reward_rejected')

    completed = _completed(role)
    count = _completed_count(role, task.task_id) + 1
    completed[key] = count
    if task.repeat_policy == 'daily':
        counts = _daily_counts(role)
        counts[key] = _daily_count(role, task.task_id) + 1
    del _active(role)[key]
    return TaskActionResult(True, True, task.task_id, 'claimed')


"""Task-system orchestration shared by server routing and tests."""

from dataclasses import dataclass
from typing import Callable, Dict, Sequence

from protocol import Field
from systems.task.protocol import (
    active_task_list_frame,
    available_task_list_frame,
    detail_request_task_id,
    is_active_list_request,
    is_available_list_request,
    parse_task_1145_request,
    parse_task_accept_request,
    parse_task_operation_request,
    safe_detail_ack_frame,
)
from systems.task.registry import TaskDefinition, TaskRegistry
from systems.task.service import (
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
        """Return rows with the status numbers consumed by e/en and e/ca."""
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
        now: int | float = 0,
        today: str | None = None,
    ) -> TaskRuntimeResult:
        # Native acceptance must validate the role id before even migrating
        # state: a packet naming another player must have no side effects.
        accept_request = parse_task_accept_request(fields)
        if accept_request is not None:
            if accept_request.player_id != int(role.get('id', 0)):
                return TaskRuntimeResult(
                    (safe_detail_ack_frame(),),
                    False,
                    reason='player_mismatch',
                )
            migrated = ensure_task_state(role, today=today)
            action = accept_task(
                role,
                self.registry,
                accept_request.task_id,
                now=now,
                today=today,
            )
            return TaskRuntimeResult(
                self.snapshot_frames(role, today=today),
                migrated or action.changed,
                reason=action.reason,
            )

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

    def matches_path_target(self, map_id: int, x: int, y: int) -> bool:
        """Return whether native task navigation may walk to this coordinate.

        The APK's task list sends ordinary 1145/action-0 map path requests
        using the map/x/y stored in the 1403 task row.  Accept and submit NPC
        positions are therefore legitimate path targets alongside gathering
        targets handled by the main server.
        """
        needle = (int(map_id), int(x), int(y))
        for task in self.registry.all_tasks():
            route = task.client_route
            if needle == (route.accept_map_id, route.accept_x, route.accept_y):
                return route.accept_map_id > 0
            if needle == (route.submit_map_id, route.submit_x, route.submit_y):
                return route.submit_map_id > 0
        return False

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
        """Return True only when an ambiguous 1145 payload names a legacy task route."""
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
        """Keep older compatibility route handling without owning normal pathfinding."""
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


"""Server-side glue for the task runtime and authoritative rewards.

This module deliberately does not import ``server`` so task state/reward logic
stays reusable and the large TCP dispatcher only needs thin delegation hooks.
"""

from pathlib import Path

from systems.inventory.registry import ItemRegistry
from systems.task.registry import TaskDefinition, TaskRegistry
from systems.task.service import TaskRuntime


MAX_CURRENCY_BALANCE = 2_147_483_647
DEFAULT_BAG_CAPACITY = 1000
_DEFAULT_TASK_CATALOG = Path(__file__).resolve().parents[2] / 'data' / 'catalog' / 'tasks.json'


def _item_exists(registry: ItemRegistry, template_id: int) -> bool:
    try:
        registry.require(int(template_id))
    except KeyError:
        return False
    return True


def default_task_registry(item_registry: ItemRegistry) -> TaskRegistry:
    return TaskRegistry(
        _DEFAULT_TASK_CATALOG,
        item_exists=lambda template_id: _item_exists(item_registry, template_id),
    )


def _role_items(role: dict[str, object]) -> list[dict[str, object]]:
    items = role.get('items')
    if not isinstance(items, list):
        items = []
        role['items'] = items
    return [item for item in items if isinstance(item, dict)]


def _next_item_id(role: dict[str, object]) -> int:
    used = {
        int(item.get('id', 0))
        for item in _role_items(role)
        if type(item.get('id')) is int and int(item.get('id', 0)) > 0
    }
    base = max(1, int(role.get('id', 0)) * 10_000)
    while base in used:
        base += 1
    return base


class TaskServerSupport:
    """Own the validated catalog, runtime, and reward application policy."""

    def __init__(self, item_registry: ItemRegistry) -> None:
        self.item_registry = item_registry
        self.registry = default_task_registry(item_registry)
        self.runtime = TaskRuntime(self.registry)

    def _can_add_items(self, role: dict[str, object], task: TaskDefinition) -> bool:
        items = _role_items(role)
        bag_items = [item for item in items if item.get('location', 'bag') == 'bag']
        try:
            capacity = max(0, int(role.get('bag_capacity', DEFAULT_BAG_CAPACITY)))
        except (TypeError, ValueError):
            capacity = DEFAULT_BAG_CAPACITY
        free_slots = max(0, capacity - len(bag_items))
        new_stacks = 0

        for reward in task.rewards:
            if reward.kind != 'item':
                continue
            definition = self.item_registry.require(reward.template_id)
            remaining = int(reward.quantity)
            for item in bag_items:
                if int(item.get('template_id', 0)) != reward.template_id:
                    continue
                current = max(0, int(item.get('quantity', 0)))
                remaining -= max(0, int(definition.max_quantity) - current)
                if remaining <= 0:
                    break
            if remaining > 0:
                max_quantity = max(1, int(definition.max_quantity))
                new_stacks += (remaining + max_quantity - 1) // max_quantity
        return new_stacks <= free_slots

    def apply_rewards(self, role: dict[str, object], task: TaskDefinition) -> bool:
        """Apply one task reward set atomically after capacity validation."""
        if not self._can_add_items(role, task):
            return False

        for reward in task.rewards:
            if reward.kind == 'experience':
                role['experience'] = max(0, int(role.get('experience', 0))) + max(0, int(reward.amount))
                continue
            if reward.kind == 'silver':
                currencies = role.get('currencies')
                if not isinstance(currencies, dict):
                    currencies = {}
                    role['currencies'] = currencies
                current = max(0, int(currencies.get('silver', 0)))
                currencies['silver'] = min(MAX_CURRENCY_BALANCE, current + max(0, int(reward.amount)))
                continue
            if reward.kind != 'item':
                continue

            definition = self.item_registry.require(reward.template_id)
            remaining = max(0, int(reward.quantity))
            items = _role_items(role)
            for item in items:
                if remaining <= 0:
                    break
                if item.get('location', 'bag') != 'bag':
                    continue
                if int(item.get('template_id', 0)) != reward.template_id:
                    continue
                current = max(0, int(item.get('quantity', 0)))
                space = max(0, int(definition.max_quantity) - current)
                if space <= 0:
                    continue
                gained = min(space, remaining)
                item['quantity'] = current + gained
                remaining -= gained
            while remaining > 0:
                gained = min(max(1, int(definition.max_quantity)), remaining)
                items.append({
                    'id': _next_item_id(role),
                    'template_id': int(reward.template_id),
                    'quantity': gained,
                    'location': 'bag',
                })
                remaining -= gained
        return True


def default_task_server_support(item_registry: ItemRegistry) -> TaskServerSupport:
    return TaskServerSupport(item_registry)
