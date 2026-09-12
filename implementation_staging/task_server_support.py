"""Server-side glue for the task runtime and authoritative rewards.

This module deliberately does not import ``server`` so task state/reward logic
stays reusable and the large TCP dispatcher only needs thin delegation hooks.
"""
from __future__ import annotations

from pathlib import Path

from item_registry import ItemRegistry
from task_registry import TaskDefinition, TaskRegistry
from task_runtime import TaskRuntime


MAX_CURRENCY_BALANCE = 2_147_483_647
DEFAULT_BAG_CAPACITY = 1000
_DEFAULT_TASK_CATALOG = Path(__file__).resolve().parent / 'data' / 'catalog' / 'tasks.json'


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
