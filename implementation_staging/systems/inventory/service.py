"""背包系统业务：容量、装备、使用、丢弃与强化事务。"""
from __future__ import annotations

import logging
import random
from dataclasses import dataclass

from protocol import (
    Field, TYPE_BYTE, TYPE_INT, TYPE_SHORT,
    binary, byte, encode_frame, integer, long_integer, short, string,
)
from systems.inventory.registry import (
    ItemRegistry, default_item_registry, deprecated_armor_template_ids,
    deprecated_mount_template_ids, deprecated_unsupported_equipment_template_ids,
    chaos_socket_rate, chaos_stone_definition_for, is_chaos_stone,
    is_strengthening_stone, normalized_strengthen_level,
)
from systems.inventory.protocol import (
    SOCKET_OPENING_ACTIONS, STRENGTHENING_ACTIONS, find_item, is_equipment,
    is_strengthenable_weapon, item_display_description, item_display_name,
    item_frame, item_slot, native_socket_slots, role_items,
    socket_opening_open_frame, strengthening_equipment_error_frame,
    strengthening_equipment_frame,
    strengthening_open_frame, strengthening_rate_error_frame,
    strengthening_rate_frame, strengthening_reset_frame,
    strengthening_stone_selection_frame,
)
from systems.fuyuan import service as fuyuan
from systems.role.registry import (
    construct_mount_state, create_mount_item_instance, load_mount_catalog,
)
from systems.inventory.socket import (
    ensure_socket_state, first_unopened_socket, roll_socket_type, socket_types,
)
from systems.inventory.registry import (
    INITIAL_STRENGTHEN_STONE_TEMPLATE_ID,
    MIDDLE_STRENGTHEN_STONE_TEMPLATE_ID,
    STRENGTHENING_ATTACK_BONUSES, rate_for, recalculate_equipment_attributes,
    stone_definition_for, strengthening_failure_level, strengthening_success,
    total_strengthening_rate,
)
from app.notify import top_message_frame

LOG = logging.getLogger('piaomiao-local')

# ---------------------------------------------------------------------------
def allocate_item_instance_id(role: dict[str, object]) -> int:
    """Allocate a free positive item instance id unique within this role.

    Starter inventory still uses role_id * 100 + offset. New allocations use
    role_id * 10_000 so 252 preview items cannot collide with adjacent roles'
    starter offsets or the old 1..99 block.
    """
    used: set[int] = set()
    for item in role_items(role):
        try:
            item_id = int(item.get('id', 0))
        except (TypeError, ValueError):
            continue
        if item_id > 0:
            used.add(item_id)
    try:
        role_id = int(role.get('id', 0))
    except (TypeError, ValueError):
        role_id = 0
    candidate = max(1, role_id * 10_000)
    while candidate in used:
        candidate += 1
    return candidate
DEFAULT_BAG_CAPACITY = 1000
EQUIPMENT_RESOURCE_PREVIEW_VERSION = 4
ROLE_BAG_RESET_VERSION = 1
ROLE_BAG_PREVIEW_SUPPRESSION_VERSION = 1
def starter_items(
    role_id: int,
    registry: ItemRegistry | None = None,
) -> list[dict[str, object]]:
    """Return the starter inventory understood by the original client."""
    if registry is None:
        registry = default_item_registry()
    return registry.starter_instances(role_id)


def ensure_equipment_resource_preview_items(
    role: dict[str, object],
    item_registry: ItemRegistry | None = None,
) -> bool:
    """Migrate deprecated local previews, then grant the supported APK preview set.

    Preview items are compatibility constructs, not official equipment templates.
    Unsupported local starter/preview templates are removed from old roles before
    the current supported preview catalog is re-granted.
    """
    if item_registry is None:
        item_registry = default_item_registry()
    changed = False
    try:
        existing_capacity = int(role.get('bag_capacity', 0))
    except (TypeError, ValueError):
        existing_capacity = 0
    new_capacity = max(existing_capacity, DEFAULT_BAG_CAPACITY)
    if role.get('bag_capacity') != new_capacity:
        role['bag_capacity'] = new_capacity
        changed = True
    items = role_items(role)
    deprecated_mounts = deprecated_mount_template_ids()
    deprecated_templates = (
        deprecated_armor_template_ids()
        | deprecated_unsupported_equipment_template_ids()
        | deprecated_mounts
    )
    kept_items: list[dict[str, object]] = []
    removed_deprecated = False
    removed_deprecated_mount = False
    for item in items:
        if not isinstance(item, dict):
            continue
        try:
            template_id = int(item.get('template_id', 0))
        except (TypeError, ValueError):
            template_id = 0
        if template_id in deprecated_templates:
            removed_deprecated = True
            if template_id in deprecated_mounts:
                removed_deprecated_mount = True
            continue
        kept_items.append(item)
    if removed_deprecated:
        role['items'] = kept_items
        items = role_items(role)
        changed = True
    if removed_deprecated_mount and int(role.get('mount_model', 0)) != 0:
        role['mount_model'] = 0
        changed = True
    # 只有真正执行过一次性背包清空的旧角色才禁止重新补回历史 APK 预览物品。
    # 新角色虽然 bag_reset_version 已是最新，但没有 suppression 标记，仍可正常修复预览目录。
    if int(role.get('bag_preview_suppression_version', 0) or 0) >= ROLE_BAG_PREVIEW_SUPPRESSION_VERSION:
        if role.get('equipment_resource_preview_version') != EQUIPMENT_RESOURCE_PREVIEW_VERSION:
            role['equipment_resource_preview_version'] = EQUIPMENT_RESOURCE_PREVIEW_VERSION
            changed = True
        return changed
    present = {
        int(item.get('template_id', 0))
        for item in items
        if isinstance(item, dict)
    }
    for template_id in item_registry.preview_template_ids():
        if template_id in present:
            continue
        items.append({
            'id': allocate_item_instance_id(role),
            'template_id': int(template_id),
            'quantity': 1,
            'location': 'bag',
        })
        present.add(int(template_id))
        changed = True
    if role.get('equipment_resource_preview_version') != EQUIPMENT_RESOURCE_PREVIEW_VERSION:
        role['equipment_resource_preview_version'] = EQUIPMENT_RESOURCE_PREVIEW_VERSION
        changed = True
    return changed
def ensure_all_mount_series_items(
    role: dict[str, object],
    item_registry: ItemRegistry,
) -> bool:
    """Ensure the role owns one real bag item for every known mount series.

    This is intentionally idempotent. Existing mount instances are resolved
    through the constructor (including legacy appearance-projection items),
    so reconnecting never duplicates a series the role already owns. New
    grants are normal item instances with authoritative per-instance
    ``mount_state`` and start at the normal logical stage in the bag.
    """
    catalog = load_mount_catalog()
    items = role_items(role)
    owned_series: set[int] = set()
    for item in items:
        if not isinstance(item, dict):
            continue
        try:
            state = construct_mount_state(item, item_registry, catalog)
        except (KeyError, TypeError, ValueError):
            continue
        if state is not None:
            owned_series.add(int(state.series_id))

    changed = False
    for series_id in sorted(catalog.series):
        if series_id in owned_series:
            continue
        template_id = catalog.template_id_for_image(
            catalog.resolve_appearance(series_id, 0)
        )
        try:
            item_registry.require(template_id)
        except KeyError:
            continue
        items.append(create_mount_item_instance(
            instance_id=allocate_item_instance_id(role),
            series_id=series_id,
            stage=0,
            grade=1,
            growth=0,
            location='bag',
            catalog=catalog,
        ))
        owned_series.add(series_id)
        changed = True
    return changed



def clear_role_bag_once(role: dict[str, object]) -> bool:
    """一次性清空旧角色背包，只删除 location=bag 的物品实例。

    已装备物品保留；迁移后写入 reset 与 preview-suppression 版本。
    reset 确保之后新获得的物品不会再次被清空；suppression 防止旧预览物品自动补回。
    """
    try:
        current_version = int(role.get('bag_reset_version', 0) or 0)
    except (TypeError, ValueError):
        current_version = 0
    if current_version >= ROLE_BAG_RESET_VERSION:
        return False

    items = role_items(role)
    kept_items = [
        item for item in items
        if not (isinstance(item, dict) and item.get('location') == 'bag')
    ]
    if len(kept_items) != len(items):
        role['items'] = kept_items
    role['bag_reset_version'] = ROLE_BAG_RESET_VERSION
    role['bag_preview_suppression_version'] = ROLE_BAG_PREVIEW_SUPPRESSION_VERSION
    return True


def bag_capacity(role: dict[str, object]) -> int:
    """Return the persisted personal-inventory slot limit."""
    try:
        return max(0, int(role.get('bag_capacity', DEFAULT_BAG_CAPACITY))) + fuyuan.capacity_bonus(role)
    except (TypeError, ValueError):
        return DEFAULT_BAG_CAPACITY + fuyuan.capacity_bonus(role)


def bag_item_count(role: dict[str, object]) -> int:
    """Count occupied bag slots; stack quantity does not consume extra slots."""
    return sum(item.get('location', 'bag') == 'bag' for item in role_items(role))


def try_move_item_to_bag(role: dict[str, object], item: dict[str, object]) -> bool:
    """Move one owned item into the bag only when a slot is available."""
    if item.get('location', 'bag') == 'bag':
        return True
    if bag_item_count(role) >= bag_capacity(role):
        return False
    item['location'] = 'bag'
    return True


def item_action_location_valid(action: int, item: dict[str, object]) -> bool:
    """Match 1009 bag/equipment actions to the APK's item containers."""
    location = str(item.get('location', 'bag'))
    if int(action) in {3, 4, 5}:
        return location == 'bag'
    if int(action) == 6:
        return location == 'equipped'
    return True

def ensure_weapon_base_attributes(
    item: dict[str, object],
    registry: ItemRegistry | None = None,
) -> None:
    """Ensure a weapon item has base_equipment_attributes and strengthen_level.

    This is used when tests or callers work with minimal item instances that
    may not have gone through RoleStore._ensure_items() yet.
    """
    if not is_strengthenable_weapon(item):
        return
    if registry is None:
        registry = default_item_registry()
    resolved = registry.resolve(item)
    if 'base_equipment_attributes' not in item:
        # Use the template's equipment_attributes as the base.
        current_attributes = list(resolved.get('equipment_attributes', [0, 0, 0, 0]))
        base_attributes = [
            (
                current_attributes[index]
                if index < len(current_attributes)
                and type(current_attributes[index]) is int
                and current_attributes[index] >= 0
                else 0
            )
            for index in range(4)
        ]
        raw_level = item.get('strengthen_level', 0)
        level = normalized_strengthen_level(item)
        if type(raw_level) is int and 0 < raw_level <= 9:
            base_attributes[0] = max(
                0,
                base_attributes[0] - STRENGTHENING_ATTACK_BONUSES[level],
            )
        item['base_equipment_attributes'] = base_attributes
    if 'strengthen_level' not in item:
        item['strengthen_level'] = 0
    recalculate_equipment_attributes(item)

@dataclass
class SocketOpeningActionResult:
    frames: tuple[bytes, ...]
    changed: bool
    message: str = ''


def _invalid_socket_opening_result(message: str) -> SocketOpeningActionResult:
    return SocketOpeningActionResult((top_message_frame(message),), False, message)


def socket_opening_action_result(
    role: dict[str, object],
    values: list[object],
    rng=random,
    registry: ItemRegistry | None = None,
) -> SocketOpeningActionResult:
    """Apply APK native 1009/action 95(open) and 90(confirm socket opening)."""
    if registry is None:
        registry = default_item_registry()
    if not values:
        return _invalid_socket_opening_result('开孔请求缺少操作类型')
    try:
        action = int(values[0])
    except (TypeError, ValueError):
        return _invalid_socket_opening_result('开孔请求格式错误')

    if action == 95:
        return SocketOpeningActionResult((socket_opening_open_frame(),), False)
    if action not in SOCKET_OPENING_ACTIONS:
        return SocketOpeningActionResult((), False)

    try:
        equipment_id = int(values[1])
        material_id = int(values[2])
    except (IndexError, TypeError, ValueError):
        return _invalid_socket_opening_result('请选择需要开孔的装备和混沌石')

    equipment = find_item(role, equipment_id)
    material = find_item(role, material_id)
    if equipment is None or not is_equipment(equipment):
        return _invalid_socket_opening_result('开孔装备无效')
    slot = item_slot(equipment, registry)
    if not 1 <= slot <= 10:
        # 原 APK 开孔属性块只覆盖原生 1..10；戒指 11 明确不参与开孔。
        return _invalid_socket_opening_result('该部位装备不能开孔')
    if str(equipment.get('location', 'bag')) not in {'bag', 'equipped'}:
        return _invalid_socket_opening_result('只能对背包或已装备的装备开孔')

    # Phase 2: ensure the instance owns a persistent original-hole array.
    # Minimal test/caller items may not have passed RoleStore migration yet.
    ensure_socket_state(equipment, socketable=True)
    types = socket_types(equipment)
    slots = native_socket_slots(equipment)
    opened = sum(1 for value in types if value != 0)
    index = first_unopened_socket(equipment)
    if opened >= 5 or index is None:
        return _invalid_socket_opening_result('该装备已经开满5个孔')

    definition = chaos_stone_definition_for(material)
    valid_material = (
        material is not None
        and definition is not None
        and is_chaos_stone(material)
        and str(material.get('location', 'bag')) == 'bag'
        and type(material.get('quantity')) is int
        and int(material.get('quantity', 0)) > 0
    )
    if not valid_material or material is None or definition is None:
        return _invalid_socket_opening_result('请放入有效的混沌石')

    # 帮助明确：无论成功失败，每次都消耗 1 颗混沌石。
    quantity = int(material['quantity'])
    material['quantity'] = quantity - 1

    rate = chaos_socket_rate(definition, opened)
    succeeded = rng.randrange(10_000) < rate
    if succeeded:
        socket_type = roll_socket_type(
            equipment,
            equipment_slot=slot,
            rng=rng,
        )
        if socket_type == 0:
            return _invalid_socket_opening_result('该部位装备不能开孔')
        types[index] = socket_type
        slots[index] = socket_type
        equipment['socket_types'] = types
        equipment['extra_attributes'] = slots

    frames: list[bytes] = []
    if succeeded:
        frames.append(item_frame(equipment, registry, operation=3))
    frames.append(item_frame(material, registry, operation=3))
    if int(material['quantity']) == 0:
        role_items(role).remove(material)
        frames.append(encode_frame(1009, [short(3), integer(material_id)]))

    if succeeded:
        message = f'开孔成功，第{opened + 1}孔已开启'
    else:
        message = f'开孔失败，成功率{rate / 100:.0f}%，混沌石已消耗'
    frames.append(top_message_frame(message))
    if succeeded:
        # 1008 updates the authoritative item object, but the already-open
        # e/ag socket page keeps its selected controls cached. Re-send the
        # native action-95 page-init response after the item update so the
        # page rebinds/repaints from the refreshed g.x[0..4] state.
        frames.append(socket_opening_open_frame())
    return SocketOpeningActionResult(tuple(frames), True, message)


@dataclass
class StrengtheningActionResult:
    frames: tuple[bytes, ...]
    changed: bool
    message: str = ''


def _invalid_strengthening_result(message: str) -> StrengtheningActionResult:
    return StrengtheningActionResult(
        (top_message_frame(message), strengthening_reset_frame()),
        False,
        message,
    )


def strengthening_action_result(
    role: dict[str, object],
    values: list[object],
    rng=random,
) -> StrengtheningActionResult:
    """Apply one confirmed protocol-1009 strengthening action atomically."""
    if not values:
        return _invalid_strengthening_result('强化请求缺少操作类型')
    try:
        action = int(values[0])
    except (TypeError, ValueError):
        return _invalid_strengthening_result('强化请求格式错误')

    if action == 97:
        return StrengtheningActionResult((strengthening_open_frame(),), False)
    if action not in STRENGTHENING_ACTIONS:
        return StrengtheningActionResult((), False)

    try:
        weapon_id = int(values[1])
    except (IndexError, TypeError, ValueError):
        if action == 75:
            return StrengtheningActionResult(
                (strengthening_equipment_error_frame('请选择需要强化的武器'),),
                False,
                '请选择需要强化的武器',
            )
        if action == 74:
            return StrengtheningActionResult(
                (strengthening_rate_error_frame('请选择需要强化的武器'),),
                False,
                '请选择需要强化的武器',
            )
        return _invalid_strengthening_result('请选择需要强化的武器')
    weapon = find_item(role, weapon_id)
    valid_weapon = (
        weapon is not None
        and is_strengthenable_weapon(weapon)
        and str(weapon.get('location', 'bag')) in {'bag', 'equipped'}
    )
    if not valid_weapon or weapon is None:
        if action == 75:
            return StrengtheningActionResult(
                (strengthening_equipment_error_frame('只能强化背包或已装备的武器'),),
                False,
                '只能强化背包或已装备的武器',
            )
        if action == 74:
            return StrengtheningActionResult(
                (strengthening_rate_error_frame('只能强化背包或已装备的武器'),),
                False,
                '只能强化背包或已装备的武器',
            )
        return _invalid_strengthening_result('只能强化背包或已装备的武器')
    if action == 75:
        return StrengtheningActionResult((strengthening_equipment_frame(weapon),), False)

    try:
        stone_id = int(values[2])
    except (IndexError, TypeError, ValueError):
        if action == 77:
            return StrengtheningActionResult(
                (strengthening_stone_selection_frame(False),),
                False,
                '请选择强化石',
            )
        if action == 74:
            return StrengtheningActionResult(
                (strengthening_rate_error_frame('请选择强化石'),),
                False,
                '请选择强化石',
            )
        return _invalid_strengthening_result('请选择强化石')
    stone = find_item(role, stone_id)
    definition = stone_definition_for(stone) if stone is not None else None
    valid_stone = (
        stone is not None
        and definition is not None
        and is_strengthening_stone(stone)
        and str(stone.get('location', 'bag')) == 'bag'
        and type(stone.get('quantity')) is int
        and int(stone.get('quantity', 0)) > 0
    )
    if action == 77:
        if valid_stone:
            # The APK sends action 77 immediately before action 74. Its S→C
            # action-77/status=1 branch calls bw.n(), which clears both chosen
            # item slots; a valid selection must therefore be acknowledged by
            # the following action-74 rate frame only. Status 0 remains the
            # native directive for rejecting and clearing an invalid stone.
            return StrengtheningActionResult((), False)
        return StrengtheningActionResult(
            (strengthening_stone_selection_frame(False),),
            False,
            '强化石无效',
        )
    if not valid_stone or stone is None or definition is None:
        if action == 74:
            return StrengtheningActionResult(
                (strengthening_rate_error_frame('强化石无效或数量不足'),),
                False,
                '强化石无效或数量不足',
            )
        return _invalid_strengthening_result('强化石无效或数量不足')
    if action == 74:
        return StrengtheningActionResult(
            (strengthening_rate_frame(weapon, stone),),
            False,
        )

    try:
        count = int(values[3])
    except (IndexError, TypeError, ValueError):
        return _invalid_strengthening_result('强化石数量无效')
    level = normalized_strengthen_level(weapon)
    quantity = int(stone['quantity'])
    if type(values[3]) is bool or not 1 <= count <= 5 or count > quantity:
        return _invalid_strengthening_result('每次需投入 1 至 5 颗强化石，且不能超过持有数量')
    if level >= 9:
        return _invalid_strengthening_result('武器已达到最高强化等级 +9')

    succeeded = strengthening_success(definition, level, count, rng)
    next_level = level + 1 if succeeded else strengthening_failure_level(level)
    weapon['strengthen_level'] = next_level
    recalculate_equipment_attributes(weapon)
    remaining = quantity - count
    stone['quantity'] = remaining

    frames = [item_frame(weapon, operation=3), item_frame(stone, operation=3)]
    if remaining == 0:
        role_items(role).remove(stone)
        frames.append(encode_frame(1009, [short(3), integer(stone_id)]))
    resolved_weapon = default_item_registry().resolve(weapon)
    if succeeded:
        message = f'强化成功，{item_display_name(resolved_weapon)}'
    elif next_level == level:
        message = f'强化失败，等级保持 +{level}'
    else:
        message = f'强化失败，等级降至 +{next_level}'
    frames.extend((top_message_frame(message), strengthening_reset_frame()))
    return StrengtheningActionResult(tuple(frames), True, message)

def is_role_item_equipped(role: dict[str, object], item_id: int) -> bool:
    """Return whether one concrete item instance is currently equipped."""
    for item in role_items(role):
        try:
            current_id = int(item.get('id', 0))
        except (TypeError, ValueError):
            continue
        if current_id == int(item_id) and item.get('location') == 'equipped':
            return True
    return False


