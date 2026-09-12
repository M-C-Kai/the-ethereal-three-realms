"""Validated task catalog for the local compatibility server."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Callable


CATEGORY_WIRE_IDS = {
    'main': 1,
    'side': 2,
    'cycle': 3,
    'daily': 4,
    'divine': 6,
}
OBJECTIVE_KINDS = {
    'monster_killed',
    'item_gained',
    'npc_talked',
    'map_entered',
    'battle_won',
    'item_submitted',
}
REWARD_KINDS = {'experience', 'silver', 'item'}
REPEAT_POLICIES = {'once', 'repeat', 'daily'}


class TaskCatalogError(ValueError):
    """Raised when the task catalog is malformed or inconsistent."""


@dataclass(frozen=True)
class TaskObjectiveDefinition:
    kind: str
    target_id: int
    required: int


@dataclass(frozen=True)
class TaskRewardDefinition:
    kind: str
    amount: int = 0
    template_id: int = 0
    quantity: int = 0


@dataclass(frozen=True)
class TaskClientRoute:
    """Client-visible NPC coordinates used by the native task screens.

    ``route_id``/``route_kind`` are retained for the older compatibility
    route experiments.  The APK-confirmed 1403 list records use the explicit
    accept/submit map, tile and actor fields below.
    """

    route_id: int
    route_kind: int
    accept_map_id: int = 0
    accept_x: int = 0
    accept_y: int = 0
    accept_actor_id: int = 0
    submit_map_id: int = 0
    submit_x: int = 0
    submit_y: int = 0
    submit_actor_id: int = 0


@dataclass(frozen=True)
class TaskDefinition:
    task_id: int
    category: str
    name: str
    description: str
    level_requirement: int
    prerequisites: tuple[int, ...]
    objectives: tuple[TaskObjectiveDefinition, ...]
    rewards: tuple[TaskRewardDefinition, ...]
    repeat_policy: str
    daily_limit: int
    client_route: TaskClientRoute

    @property
    def category_wire_id(self) -> int:
        return CATEGORY_WIRE_IDS[self.category]


class TaskRegistry:
    """Load immutable task definitions and reject bad cross references."""

    def __init__(self, catalog_file: Path, item_exists: Callable[[int], bool]) -> None:
        self._tasks: dict[int, TaskDefinition] = {}
        self._item_exists = item_exists
        self._load(Path(catalog_file))

    def _load(self, path: Path) -> None:
        try:
            raw = json.loads(path.read_text(encoding='utf-8'))
        except (OSError, json.JSONDecodeError) as exc:
            raise TaskCatalogError(f'cannot load task catalog: {path}') from exc
        if not isinstance(raw, dict):
            raise TaskCatalogError('task catalog must be an object')
        if int(raw.get('version', 0)) != 1:
            raise TaskCatalogError('unsupported task catalog version')
        tasks = raw.get('tasks')
        if not isinstance(tasks, list):
            raise TaskCatalogError('task catalog tasks must be a list')
        for entry in tasks:
            task = self._parse_task(entry)
            if task.task_id in self._tasks:
                raise TaskCatalogError(f'duplicate task_id {task.task_id}')
            self._tasks[task.task_id] = task
        for task in self._tasks.values():
            for prerequisite in task.prerequisites:
                if prerequisite not in self._tasks:
                    raise TaskCatalogError(
                        f'task {task.task_id} references unknown prerequisite {prerequisite}'
                    )

    def _parse_task(self, raw: object) -> TaskDefinition:
        if not isinstance(raw, dict):
            raise TaskCatalogError('each task must be an object')
        task_id = int(raw.get('task_id', 0))
        if task_id <= 0:
            raise TaskCatalogError('task_id must be positive')
        category = str(raw.get('category', ''))
        if category not in CATEGORY_WIRE_IDS:
            raise TaskCatalogError(f'invalid category {category!r} for task {task_id}')
        name = str(raw.get('name', '')).strip()
        if not name:
            raise TaskCatalogError(f'task {task_id} needs a name')
        level_requirement = int(raw.get('level_requirement', 1))
        if level_requirement < 1:
            raise TaskCatalogError(f'task {task_id} level_requirement must be >= 1')
        prerequisites_raw = raw.get('prerequisites', [])
        if not isinstance(prerequisites_raw, list):
            raise TaskCatalogError(f'task {task_id} prerequisites must be a list')
        prerequisites = tuple(int(value) for value in prerequisites_raw)

        objectives_raw = raw.get('objectives', [])
        if not isinstance(objectives_raw, list) or not objectives_raw:
            raise TaskCatalogError(f'task {task_id} needs objectives')
        objectives: list[TaskObjectiveDefinition] = []
        for objective_raw in objectives_raw:
            if not isinstance(objective_raw, dict):
                raise TaskCatalogError(f'task {task_id} objective must be an object')
            kind = str(objective_raw.get('kind', ''))
            if kind not in OBJECTIVE_KINDS:
                raise TaskCatalogError(f'task {task_id} invalid objective kind {kind!r}')
            required = int(objective_raw.get('required', 0))
            if required <= 0:
                raise TaskCatalogError(f'task {task_id} objective required must be positive')
            objectives.append(TaskObjectiveDefinition(
                kind=kind,
                target_id=int(objective_raw.get('target_id', 0)),
                required=required,
            ))

        rewards_raw = raw.get('rewards', [])
        if not isinstance(rewards_raw, list):
            raise TaskCatalogError(f'task {task_id} rewards must be a list')
        rewards: list[TaskRewardDefinition] = []
        for reward_raw in rewards_raw:
            if not isinstance(reward_raw, dict):
                raise TaskCatalogError(f'task {task_id} reward must be an object')
            kind = str(reward_raw.get('kind', ''))
            if kind not in REWARD_KINDS:
                raise TaskCatalogError(f'task {task_id} invalid reward kind {kind!r}')
            if kind == 'item':
                template_id = int(reward_raw.get('template_id', 0))
                quantity = int(reward_raw.get('quantity', 0))
                if template_id <= 0 or quantity <= 0:
                    raise TaskCatalogError(f'task {task_id} item reward is invalid')
                if not self._item_exists(template_id):
                    raise TaskCatalogError(f'unknown item template {template_id}')
                rewards.append(TaskRewardDefinition(
                    kind=kind,
                    template_id=template_id,
                    quantity=quantity,
                ))
            else:
                amount = int(reward_raw.get('amount', 0))
                if amount < 0:
                    raise TaskCatalogError(f'task {task_id} reward amount must be >= 0')
                rewards.append(TaskRewardDefinition(kind=kind, amount=amount))

        repeat_policy = str(raw.get('repeat_policy', 'once'))
        if repeat_policy not in REPEAT_POLICIES:
            raise TaskCatalogError(f'task {task_id} invalid repeat_policy {repeat_policy!r}')
        daily_limit = int(raw.get('daily_limit', 0))
        if daily_limit < 0:
            raise TaskCatalogError(f'task {task_id} daily_limit must be >= 0')
        if repeat_policy == 'daily' and daily_limit < 1:
            raise TaskCatalogError(f'task {task_id} daily task needs daily_limit >= 1')

        route_raw = raw.get('client_route', {})
        if not isinstance(route_raw, dict):
            raise TaskCatalogError(f'task {task_id} client_route must be an object')
        route = TaskClientRoute(
            route_id=int(route_raw.get('route_id', task_id)),
            route_kind=int(route_raw.get('route_kind', 1)),
            accept_map_id=int(route_raw.get('accept_map_id', 0)),
            accept_x=int(route_raw.get('accept_x', 0)),
            accept_y=int(route_raw.get('accept_y', 0)),
            accept_actor_id=int(route_raw.get('accept_actor_id', 0)),
            submit_map_id=int(route_raw.get('submit_map_id', route_raw.get('accept_map_id', 0))),
            submit_x=int(route_raw.get('submit_x', route_raw.get('accept_x', 0))),
            submit_y=int(route_raw.get('submit_y', route_raw.get('accept_y', 0))),
            submit_actor_id=int(route_raw.get('submit_actor_id', route_raw.get('accept_actor_id', 0))),
        )
        return TaskDefinition(
            task_id=task_id,
            category=category,
            name=name,
            description=str(raw.get('description', '')),
            level_requirement=level_requirement,
            prerequisites=prerequisites,
            objectives=tuple(objectives),
            rewards=tuple(rewards),
            repeat_policy=repeat_policy,
            daily_limit=daily_limit,
            client_route=route,
        )

    def all_tasks(self) -> tuple[TaskDefinition, ...]:
        return tuple(self._tasks[task_id] for task_id in sorted(self._tasks))

    def require(self, task_id: int) -> TaskDefinition:
        try:
            return self._tasks[int(task_id)]
        except KeyError as exc:
            raise KeyError(f'unknown task {int(task_id)}') from exc

    def get(self, task_id: int) -> TaskDefinition | None:
        return self._tasks.get(int(task_id))
