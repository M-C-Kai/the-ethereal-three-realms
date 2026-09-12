from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Protocol

import fuyuan
from item_registry import ItemRegistry, default_item_registry


BATTLE_EXP_REWARD = 50
BATTLE_DROP_TEMPLATE_ID = 260_000_001


class RoleItemsFn(Protocol):
    def __call__(self, role: dict[str, object]) -> list[dict[str, object]]: ...


@dataclass(frozen=True)
class RewardServices:
    """Generic role/inventory services required by battle settlement.

    Keeping these dependencies explicit prevents the battle package from
    importing the network server module while preserving the existing role
    schema and inventory-capacity rules.
    """

    role_items: RoleItemsFn
    bag_item_count: Callable[[dict[str, object]], int]
    bag_capacity: Callable[[dict[str, object]], int]
    apply_one_level: Callable[[dict[str, object]], bool]
    max_role_level: int = 99


def apply_battle_rewards(
    role: dict[str, object],
    services: RewardServices,
    experience: int = BATTLE_EXP_REWARD,
    registry: ItemRegistry | None = None,
) -> tuple[dict[str, object] | None, bool]:
    """Apply the existing deterministic local victory reward.

    This function intentionally owns only battle settlement. Generic role
    leveling and bag-capacity rules are supplied by ``RewardServices`` so they
    remain shared with the rest of the server instead of being copied here.
    """
    old_level = max(1, int(role.get('level', 1)))
    role['experience'] = (
        max(0, int(role.get('experience', 0)))
        + fuyuan.experience_reward(role, int(experience))
    )
    if bool(role.get('auto_level', True)):
        while (
            int(role.get('level', 1)) < int(services.max_role_level)
            and services.apply_one_level(role)
        ):
            pass

    if registry is None:
        registry = default_item_registry()
    items = services.role_items(role)
    item = next(
        (
            candidate
            for candidate in items
            if int(candidate.get('template_id', 0)) == BATTLE_DROP_TEMPLATE_ID
            and str(candidate.get('location', 'bag')) == 'bag'
        ),
        None,
    )
    level_up = int(role.get('level', 1)) > old_level

    if item is None:
        if services.bag_item_count(role) >= services.bag_capacity(role):
            return None, level_up
        registry.require(BATTLE_DROP_TEMPLATE_ID)
        item = {
            'id': (int(role.get('id', 0)) * 100) + 17,
            'template_id': BATTLE_DROP_TEMPLATE_ID,
            'quantity': 1,
            'location': 'bag',
        }
        items.append(item)
    else:
        definition = registry.require(BATTLE_DROP_TEMPLATE_ID)
        item['quantity'] = min(
            definition.max_quantity,
            int(item.get('quantity', 0)) + 1,
        )
    return item, level_up
