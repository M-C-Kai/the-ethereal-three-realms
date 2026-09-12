"""Persistent task state machine independent from network protocol details."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Callable

from task_registry import TaskDefinition, TaskRegistry


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
