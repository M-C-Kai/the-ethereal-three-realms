"""Pure rules for the APK-compatible local weapon-strengthening flow."""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Mapping, MutableMapping, Optional, Tuple


INITIAL_STRENGTHEN_STONE_TEMPLATE_ID = 322_260_000
MIDDLE_STRENGTHEN_STONE_TEMPLATE_ID = 322_261_000
STRENGTHENING_STONE_TEMPLATE_MIN = 322_260_000
STRENGTHENING_STONE_TEMPLATE_MAX = 322_261_002
MAX_STRENGTHEN_LEVEL = 9
MAX_STRENGTHEN_STONE_COUNT = 5
WEAPON_STRENGTHEN_ATTACK_BONUSES = (0, 1, 2, 3, 5, 7, 10, 14, 19, 25)

# Backward-compatible aliases for the initial local implementation names.
STRENGTHEN_STONE_TEMPLATE_ID_MIN = STRENGTHENING_STONE_TEMPLATE_MIN
STRENGTHEN_STONE_TEMPLATE_ID_MAX = STRENGTHENING_STONE_TEMPLATE_MAX
MAX_STRENGTHEN_COUNT = MAX_STRENGTHEN_STONE_COUNT
STRENGTHENING_ATTACK_BONUSES = WEAPON_STRENGTHEN_ATTACK_BONUSES


@dataclass(frozen=True)
class StrengtheningStoneDefinition:
    template_id: int
    name: str
    grade: str
    success_rates: Tuple[int, ...]


# These IDs are a local mapping inside the item range accepted by the APK.
# Their relationship to official server item definitions has not been confirmed.
STRENGTHENING_STONE_DEFINITIONS = {
    INITIAL_STRENGTHEN_STONE_TEMPLATE_ID: StrengtheningStoneDefinition(
        INITIAL_STRENGTHEN_STONE_TEMPLATE_ID,
        "初级强化石",
        "initial",
        (2000, 1800, 1600, 1400, 1200, 1000, 800, 600, 400),
    ),
    MIDDLE_STRENGTHEN_STONE_TEMPLATE_ID: StrengtheningStoneDefinition(
        MIDDLE_STRENGTHEN_STONE_TEMPLATE_ID,
        "中级强化石",
        "middle",
        (2500, 2200, 2000, 1800, 1600, 1400, 1200, 900, 600),
    ),
}
STRENGTHENING_STONES = STRENGTHENING_STONE_DEFINITIONS


def _template_id(item: Mapping[str, object]) -> Optional[int]:
    value = item.get("template_id")
    if type(value) is not int:
        return None
    return value


def stone_definition_for(
    item: Mapping[str, object],
) -> Optional[StrengtheningStoneDefinition]:
    template_id = _template_id(item)
    if template_id is None:
        return None
    if not STRENGTHEN_STONE_TEMPLATE_ID_MIN <= template_id <= STRENGTHEN_STONE_TEMPLATE_ID_MAX:
        return None
    return STRENGTHENING_STONE_DEFINITIONS.get(template_id)


def is_strengthening_stone(item: Mapping[str, object]) -> bool:
    return stone_definition_for(item) is not None


def rate_for(stone: StrengtheningStoneDefinition, level: int) -> int:
    if type(level) is not int or not 0 <= level < MAX_STRENGTHEN_LEVEL:
        raise ValueError("strengthening rate only exists for levels 0 through 8")
    return stone.success_rates[level]


def total_strengthening_rate(single_stone_rate: int, count: int) -> int:
    # The APK exposes a one-to-five stone selector and one aggregate rate. Treating
    # their contribution as additive is a strong UI inference, not an official rule.
    return min(10000, max(0, int(single_stone_rate)) * max(0, int(count)))


def normalized_strengthen_level(item: Mapping[str, object]) -> int:
    level = item.get("strengthen_level", 0)
    if type(level) is not int or not 0 <= level <= MAX_STRENGTHEN_LEVEL:
        return 0
    return level


def strengthening_failure_level(level: int) -> int:
    if type(level) is not int or not 0 <= level <= MAX_STRENGTHEN_LEVEL:
        raise ValueError("strengthening level must be between 0 and 9")
    if level <= 2:
        return level
    if level <= 5:
        return 3
    if level <= 8:
        return 6
    return 9


def _four_attributes(value: object) -> list[int]:
    source = value if isinstance(value, (list, tuple)) else ()
    attributes = []
    for index in range(4):
        current = source[index] if index < len(source) else 0
        attributes.append(current if type(current) is int and current >= 0 else 0)
    return attributes


def recalculate_equipment_attributes(item: MutableMapping[str, object]) -> list[int]:
    if "base_equipment_attributes" in item:
        base_attributes = _four_attributes(item.get("base_equipment_attributes"))
    else:
        base_attributes = _four_attributes(item.get("equipment_attributes"))
    item["base_equipment_attributes"] = list(base_attributes)

    effective_attributes = list(base_attributes)
    level = normalized_strengthen_level(item)
    effective_attributes[0] += STRENGTHENING_ATTACK_BONUSES[level]
    item["equipment_attributes"] = effective_attributes
    return effective_attributes


def strengthening_success(
    stone: StrengtheningStoneDefinition,
    level: int,
    count: int,
    rng=random,
) -> bool:
    total_rate = total_strengthening_rate(rate_for(stone, level), count)
    return rng.randrange(10000) < total_rate


# TODO: APK help confirms lucky socket creation during strengthening, but socket field/probability are not yet protocol-locked.
