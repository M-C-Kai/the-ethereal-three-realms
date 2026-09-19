"""背包系统协议帧：物品下发、说明、详情与强化界面帧。"""
from __future__ import annotations

import logging

from protocol import (
    Field, TYPE_BYTE, TYPE_INT, TYPE_SHORT,
    binary, byte, encode_frame, integer, long_integer, short, string,
)
from systems.inventory.registry import is_strengthening_stone, normalized_strengthen_level
from systems.inventory.registry import (
    STACKABLE_ITEM_FLAG, ItemRegistry, armor_property2_from_equipment,
    armor_property2_from_icon, battle_weapon_field2_from_icon,
    battle_weapon_image_from_icon, default_item_registry,
    deprecated_mount_template_ids, helmet_property20_from_icon,
    rate_for, stone_definition_for,
    weapon_appearance_field_from_icon_and_strengthen,
    weapon_icon_to_image_mapping,
)

LOG = logging.getLogger('piaomiao-local')

# Protocol 1008 field 12 is not the equipment quality.  The original client
# turns this short into a 24x24 atlas lookup via ``a.c.x.f(int)``:
#
#   image id = 3_002_424 + (icon_code // 100 % 100) * 10_000
#   frame    = icon_code % 100
#
# These codes point at atlases already bundled in the APK.  The icon code is
# independent from the template id and from the equipment location byte.
# ``pmsj.work.e.af`` names the original equipment locations 1..14 exactly as
# listed below.  Groups 1..13 are matching armour/accessory icon atlases;
# groups 21..33 contain the different weapon families.
def find_item(role: dict[str, object], item_id: int) -> dict[str, object] | None:
    return next((item for item in role_items(role) if int(item.get('id', 0)) == item_id), None)


def item_slot(item: dict[str, object], registry: ItemRegistry | None = None) -> int:
    if 'equipment_slot' in item:
        return int(item['equipment_slot'])
    if registry is not None:
        resolved = registry.resolve(item)
        if 'equipment_slot' in resolved:
            return int(resolved['equipment_slot'])
    category = (int(item.get('template_id', 0)) // 10_000_000) % 100
    return category if 1 <= category <= 14 else 0


def is_equipment(item: dict[str, object]) -> bool:
    category = (int(item.get('template_id', 0)) // 10_000_000) % 100
    return 1 <= category <= 21


def is_strengthenable_weapon(item: dict[str, object]) -> bool:
    return is_equipment(item) and item_slot(item) == 10


def equipment_strength(item: dict[str, object]) -> int:
    """Return the native client equipment-strength index (template low digit)."""
    raw = item.get('strength')
    if type(raw) is int and 0 <= raw <= 9:
        return raw
    return int(item.get('template_id', 0)) % 10


def client_template_id(item: dict[str, object]) -> int:
    """Encode local strength into the template low digit expected by b/g.h()."""
    template_id = int(item.get('template_id', 0))
    if not is_equipment(item):
        return template_id
    return template_id - (template_id % 10) + equipment_strength(item)


def item_display_name(item: dict[str, object]) -> str:
    name = str(item.get('name', '未命名物品'))
    level = normalized_strengthen_level(item) if is_strengthenable_weapon(item) else 0
    return f'{name} +{level}' if level > 0 else name


def item_display_description(item: dict[str, object]) -> str:
    description = str(item.get('description', item.get('name', '物品')))
    if not is_strengthenable_weapon(item):
        return description
    level = normalized_strengthen_level(item)
    attributes = list(item.get('equipment_attributes', [0, 0, 0, 0]))
    attack = int(attributes[0]) if attributes else 0
    return f'{description}_强化：+{level}_当前攻击：{attack}'


def equipment_detail_description(item: dict[str, object]) -> str:
    """Text fallback for clients that still open the legacy 1032 detail panel."""
    description = str(item.get('description', item.get('name', '物品')))
    if not is_equipment(item):
        return description

    lines: list[str] = []
    innate_names = ('力量', '耐力', '敏捷', '智力', '精神')
    acquired_names = ('力量', '耐力', '敏捷', '智力', '精神')
    base_names = ('物理攻击', '物理防御', '法术攻击', '法术防御')

    innate = list(item.get('innate_attributes', [0, 0, 0, 0, 0]))
    for name, raw in zip(innate_names, innate):
        value = int(raw)
        if value:
            lines.append(f'+{value} {name}(先天)' if value > 0 else f'{value} {name}(先天)')

    acquired = list(item.get('acquired_attributes', [0, 0, 0, 0, 0]))
    for name, raw in zip(acquired_names, acquired):
        value = int(raw)
        if value:
            lines.append(f'+{value} {name}' if value > 0 else f'{value} {name}')

    strength = equipment_strength(item)
    if strength > 0:
        lines.append(f'强度 +{strength}')

    base = list(item.get('equipment_attributes', [0, 0, 0, 0]))
    for name, raw in zip(base_names, base):
        value = int(raw)
        if value:
            lines.append(f'+{value} {name}' if value > 0 else f'{value} {name}')

    extra = list(item.get('extra_attributes', [0, 0, 0, 0, 0]))
    # 1008 fields[34..38] are the five native socket slots (g.x[0..4]).
    # A zero value is an empty/open socket; a non-zero value is the embedded
    # spirit-stone instance/resource id.  Do not infer socket count from
    # non-zero values: that would count gems rather than opened holes.
    socket_count = max(0, min(5, int(item.get('socket_count', 0))))
    if socket_count > 0:
        lines.append(f'开孔 {socket_count}/5')

    max_durability = max(0, int(item.get('max_durability', 0)))
    if max_durability > 0:
        durability = max(0, min(max_durability, int(item.get('durability', max_durability))))
        lines.append(f'耐久度 {durability}/{max_durability}')

    level_required = max(0, int(item.get('level_required', 0)))
    if level_required > 0:
        lines.append(f'需要等级 {level_required}')

    price = max(0, int(item.get('price', 0)))
    lines.append(f'价格: {price}')

    return '_'.join([description, *lines])


def strengthening_open_frame() -> bytes:
    return encode_frame(1009, [
        short(97),
        string('请选择需要强化的装备和强化宝石。'),
    ])


def strengthening_equipment_frame(item: dict[str, object]) -> bytes:
    registry = default_item_registry()
    resolved = registry.resolve(item)
    attributes = list(resolved.get('equipment_attributes', [0, 0, 0, 0]))
    attack = int(attributes[0]) if attributes else 0
    level = normalized_strengthen_level(item)
    summary = f'{item_display_name(resolved)}_强化 +{level}，当前攻击：{attack}'
    return encode_frame(1009, [short(75), string(summary)])


def strengthening_equipment_error_frame(message: str) -> bytes:
    return encode_frame(1009, [short(75), string(message)])


def strengthening_rate_frame(
    item: dict[str, object],
    stone: dict[str, object],
) -> bytes:
    definition = stone_definition_for(stone)
    level = normalized_strengthen_level(item)
    rate = 0
    if definition is not None and level < 9:
        rate = rate_for(definition, level)
    text = f'单颗成功率：{rate / 100:.2f}%'
    return encode_frame(1009, [short(74), short(rate), string(text)])


def strengthening_rate_error_frame(message: str) -> bytes:
    return encode_frame(1009, [short(74), short(0), string(message)])


def strengthening_stone_selection_frame(valid: bool) -> bytes:
    fields = [short(77), byte(1 if valid else 0)]
    if valid:
        fields.append(byte(1))
    return encode_frame(1009, fields)


def strengthening_reset_frame() -> bytes:
    return encode_frame(1009, [short(78)])


STRENGTHENING_ACTIONS = {74, 75, 77, 92, 97}


def item_frame(
    item: dict[str, object],
    registry: ItemRegistry | None = None,
    operation: int = 1,
) -> bytes:
    """Encode the original client's complete 1008 item-instance record.

    The local protocol uses operation ``3`` for an equipment state update.
    This is the operation already understood by the bundled APK for both
    equip and unequip; changing it to another operation breaks the item's
    equip action menu.
    """
    if registry is None:
        registry = default_item_registry()
    resolved = registry.resolve(item)
    location = str(item.get('location', 'bag'))
    location_code = {'bag': 50, 'warehouse': 51}.get(location, item_slot(item, registry))
    equipment = is_equipment(resolved)
    if equipment:
        max_durability = max(1, int(resolved.get('max_durability', 200)))
        current_durability = max(
            0,
            min(max_durability, int(resolved.get('durability', max_durability))),
        )
        stack_or_durability = current_durability
        max_stack_or_durability = max_durability
    else:
        stack_or_durability = int(item.get('quantity', 1))
        max_stack_or_durability = int(resolved.get('max_quantity', 1))
    fields = [
        byte(operation),
        integer(int(item['id'])),
        short(stack_or_durability),
        short(max_stack_or_durability),
        byte(location_code),
        integer(int(item.get('state_flags', 0))),
        integer(int(resolved.get('price', 0))),
        integer(client_template_id(resolved)),
        string(item_display_name(resolved)),
        short(int(resolved.get('item_flags', 0))),
        short(int(resolved.get('action_flags', 0))),
        byte(int(resolved.get('level_required', 1))),
        short(int(resolved.get('icon_code', resolved.get('quality', 0)))),
        integer(int(item.get('expires_at', -1))),
        short(int(resolved.get('sort_group', 0))),
        short(int(resolved.get('sort_order', 0))),
    ]
    if is_equipment(item):
        base_attributes = list(resolved.get('equipment_attributes', [0, 0, 0, 0]))
        innate_attributes = list(item.get('innate_attributes', resolved.get('innate_attributes', [0, 0, 0, 0, 0])))
        acquired_attributes = list(item.get('acquired_attributes', resolved.get('acquired_attributes', [0, 0, 0, 0, 0])))
        extra_attributes = list(item.get('extra_attributes', resolved.get('extra_attributes', [0, 0, 0, 0, 0])))
        category = (int(item['template_id']) // 10_000_000) % 100
        # The stock APK's b/g.c() only accepts categories 1..10. The local
        # compatibility APK patches that predicate to 1..14 so ring/coat/
        # accessory/talisman slots can use the same complete attribute block.
        # The additional short slots remain unknown and must stay zero.
        native_equipment = 1 <= category <= 14
        short_count = 8 if native_equipment else 4
        fields.extend(short(int(value)) for value in (base_attributes + [0] * short_count)[:short_count])
        fields.extend(byte(int(value)) for value in (innate_attributes + [0] * 5)[:5])
        fields.extend(byte(int(value)) for value in (acquired_attributes + [0] * 5)[:5])
        extra_encoder = integer if native_equipment else short
        fields.extend(extra_encoder(int(value)) for value in (extra_attributes + [0] * 5)[:5])
    return encode_frame(1008, fields)


def item_description_frame(item: dict[str, object]) -> bytes:
    registry = default_item_registry()
    resolved = registry.resolve(item)
    return encode_frame(1009, [
        short(82),
        integer(int(item['id'])),
        string(equipment_detail_description(resolved)),
    ])


def item_detail_frame(item: dict[str, object]) -> bytes:
    registry = default_item_registry()
    resolved = registry.resolve(item)
    return encode_frame(1032, [
        byte(1),
        integer(client_template_id(resolved)),
        short(int(resolved.get('icon_code', resolved.get('quality', 0)))),
        string(equipment_detail_description(resolved)),
    ])


def role_items(role: dict[str, object]) -> list[dict[str, object]]:
    items = role.get('items', [])
    if not isinstance(items, list):
        return []
    # Keep the original list object: discard/use operations must also mutate the
    # list held by the role before RoleStore.save() serializes it.
    if any(not isinstance(item, dict) for item in items):
        items = [item for item in items if isinstance(item, dict)]
        role['items'] = items
    return items  # type: ignore[return-value]
