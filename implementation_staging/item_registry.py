from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Sequence


PREVIEW_QUALITY = 1
PREVIEW_SERIAL_COLLISION_OFFSET = 50_000
# Compatibility-preview pairing only. Not an official icon→appearance mapping.
PREVIEW_SLOT_APPEARANCE_PROPERTY = {
    1: 20,
    2: 16,
    3: 15,
    5: 14,
    7: 19,
    8: 17,
    9: 18,
}
PREVIEW_SLOTS_WITHOUT_APPEARANCE = frozenset({4, 6, 11, 12, 13, 14})
SLOT_FAMILY_LABELS = {
    'helmet': '头盔',
    'shoulder': '肩甲',
    'armor': '铠甲',
    'belt': '腰带',
    'leg_armor': '腿甲',
    'necklace': '项链',
    'cloak': '披风',
    'bracer': '护腕',
    'boots': '鞋子',
    'weapon': '武器',
    'ring': '戒指',
    'coat': '外套',
    'accessory': '饰品',
    'talisman': '法宝',
}


class ItemCatalogError(Exception):
    """Raised when item catalog or starter inventory is invalid."""


def preview_category_for_slot(equipment_slot: int) -> int:
    slot = int(equipment_slot)
    return 10 if slot == 10 else slot


def synthetic_preview_template_id(
    equipment_slot: int,
    resource_group: int,
    frame: int,
    reserved_ids: Iterable[int] = (),
) -> int:
    """Build a stable compatibility-preview template_id.

    These IDs are synthetic. They are not official equipment template IDs.
    Weapons keep weapon_type == 0 so property 63 bit0 can show 装备.
    """
    category = preview_category_for_slot(equipment_slot)
    base = category * 10_000_000
    preview_serial = int(resource_group) * 1000 + int(frame) * 10
    template_id = base + preview_serial + PREVIEW_QUALITY
    reserved = set(int(value) for value in reserved_ids)
    if template_id in reserved:
        template_id = base + PREVIEW_SERIAL_COLLISION_OFFSET + preview_serial + PREVIEW_QUALITY
    return template_id


def confirmed_weapon_preview_candidates(payload: dict[str, Any]) -> list[dict[str, Any]]:
    """Return APK-confirmed low4 weapon candidates, sorted by weapon_image_id."""
    rows = payload.get('candidates', [])
    confirmed = [
        row for row in rows
        if isinstance(row, dict)
        and bool(row.get('role_dat_exists'))
        and bool(row.get('weapon_image_exists'))
    ]
    confirmed.sort(key=lambda row: int(row['weapon_image_id']))
    return confirmed


def preview_weapon_property7(
    icon_code: int,
    preview_index_in_slot: int,
    candidates: Sequence[dict[str, Any]],
) -> int:
    """Compatibility preview pairing for map-character property 7.

    low4 comes from APK-confirmed resource candidates.
    The high digits use icon_group = icon_code // 100 as local preview construction.
    This is not an official icon_code → property7 mapping.
    """
    if not candidates:
        raise ItemCatalogError('weapon preview requires confirmed property7 candidates')
    candidate = candidates[int(preview_index_in_slot) % len(candidates)]
    icon_group = int(icon_code) // 100
    low4 = int(candidate['property7_low4_candidate'])
    return icon_group * 10_000 + low4


def preview_appearance_properties(
    equipment_slot: int,
    preview_index_in_slot: int,
    manifest: dict[str, Any],
    *,
    icon_code: int = 0,
    weapon_candidates: Sequence[dict[str, Any]] | None = None,
) -> dict[str, int]:
    """Pair one preview item to an APK-confirmed character-layer candidate.

    This is a compatibility preview pairing, not an official equipment mapping.
    """
    slot = int(equipment_slot)
    if slot == 10:
        return {
            '7': preview_weapon_property7(
                icon_code,
                preview_index_in_slot,
                weapon_candidates or (),
            )
        }
    if slot in PREVIEW_SLOTS_WITHOUT_APPEARANCE:
        return {}
    property_index = PREVIEW_SLOT_APPEARANCE_PROPERTY.get(slot)
    if property_index is None:
        return {}
    layer = manifest.get(str(property_index))
    if not isinstance(layer, dict):
        raise ItemCatalogError(f'missing appearance-layer audit for property {property_index}')
    candidates = layer.get('candidate_image_ids')
    if not isinstance(candidates, list) or not candidates:
        raise ItemCatalogError(f'empty candidate_image_ids for property {property_index}')
    group_base = int(layer['group_base'])
    image_id = int(candidates[int(preview_index_in_slot) % len(candidates)])
    return {str(property_index): image_id - group_base}


@dataclass(frozen=True)
class ItemDefinition:
    template_id: int
    kind: str
    name: str
    description: str
    max_quantity: int
    equipment_slot: int = 0
    price: int = 0
    level_required: int = 1
    icon_code: int = 0
    quality: int = 0
    sort_group: int = 0
    sort_order: int = 0
    equipment_attributes: tuple[int, ...] = (0, 0, 0, 0)
    appearance_properties: dict[str, int] = field(default_factory=dict)
    item_flags: int = 0
    action_flags: int = 0
    heal: int = 0
    mount_model: int = 0


@dataclass(frozen=True)
class StarterItemDefinition:
    template_id: int
    instance_offset: int
    quantity: int
    location: str


class ItemRegistry:
    """Load and validate item templates from catalog JSON files."""

    def __init__(
        self,
        items_file: Path,
        starter_inventory_file: Path,
        extra_items_files: Sequence[Path] | None = None,
    ) -> None:
        self._items: dict[int, ItemDefinition] = {}
        self._preview_template_ids: tuple[int, ...] = ()
        self._starter_items: list[StarterItemDefinition] = []
        self._load_items(items_file, preview=False)
        preview_ids: list[int] = []
        for extra_path in extra_items_files or ():
            before = set(self._items)
            self._load_items(extra_path, preview=True)
            preview_ids.extend(sorted(set(self._items) - before))
        self._preview_template_ids = tuple(preview_ids)
        self._load_starter_inventory(starter_inventory_file)

    def preview_template_ids(self) -> tuple[int, ...]:
        return self._preview_template_ids

    def _load_items(self, path: Path, *, preview: bool = False) -> None:
        data = json.loads(path.read_text(encoding='utf-8'))
        if not isinstance(data, dict) or 'items' not in data:
            raise ItemCatalogError(f'catalog missing "items" key: {path}')
        raw_items = data['items']
        if not isinstance(raw_items, list):
            raise ItemCatalogError(f'catalog "items" must be a list: {path}')
        if preview:
            status = str(data.get('status') or data.get('kind') or '')
            if status and status != 'compatibility_preview':
                raise ItemCatalogError(
                    f'preview catalog status must be compatibility_preview: {path}'
                )
        items = self._items
        seen_ids = set(items)
        for raw in raw_items:
            if not isinstance(raw, dict):
                raise ItemCatalogError(f'each item must be a dict: {path}')
            template_id = int(raw['template_id'])
            if template_id <= 0:
                raise ItemCatalogError(f'template_id must be > 0: {template_id}')
            if template_id in seen_ids:
                raise ItemCatalogError(f'duplicate template_id: {template_id}')
            seen_ids.add(template_id)
            name = str(raw.get('name', ''))
            if not name:
                raise ItemCatalogError(f'name required for template_id={template_id}')
            icon_code = int(raw.get('icon_code', 0))
            max_quantity = int(raw.get('max_quantity', 1))
            if max_quantity < 1:
                raise ItemCatalogError(f'max_quantity must be >= 1 for template_id={template_id}')
            sort_group = int(raw.get('sort_group', 0))
            if sort_group not in {0, 100, 150, 160, 170}:
                raise ItemCatalogError(f'invalid sort_group {sort_group} for template_id={template_id}')
            category = (template_id // 10_000_000) % 100
            is_equip = 1 <= category <= 21
            equipment_slot = int(raw.get('equipment_slot', 0))
            raw_attrs = raw.get('equipment_attributes', [0, 0, 0, 0])
            if is_equip:
                if equipment_slot == 0:
                    raise ItemCatalogError(f'equipment slot required for equipment template_id={template_id}')
                if not isinstance(raw_attrs, list) or len(raw_attrs) != 4:
                    raise ItemCatalogError(f'equipment_attributes must have 4 items for template_id={template_id}')
            raw_appearance = raw.get('appearance_properties', {})
            if not isinstance(raw_appearance, dict):
                raise ItemCatalogError(f'appearance_properties must be a dict for template_id={template_id}')
            appearance: dict[str, int] = {}
            for k, v in raw_appearance.items():
                appearance[str(k)] = int(v)
            equipment_attributes = tuple(int(x) for x in raw_attrs) if isinstance(raw_attrs, list) else (0, 0, 0, 0)
            definition = ItemDefinition(
                template_id=template_id,
                kind=str(raw.get('kind', 'consumable')),
                name=name,
                description=str(raw.get('description', '')),
                max_quantity=max_quantity,
                equipment_slot=equipment_slot,
                price=int(raw.get('price', 0)),
                level_required=int(raw.get('level_required', 1)),
                icon_code=icon_code,
                quality=int(raw.get('quality', 0)),
                sort_group=sort_group,
                sort_order=int(raw.get('sort_order', 0)),
                equipment_attributes=equipment_attributes,
                appearance_properties=appearance,
                item_flags=int(raw.get('item_flags', 0)),
                action_flags=int(raw.get('action_flags', 0)),
                heal=int(raw.get('heal', 0)),
                mount_model=int(raw.get('mount_model', 0)),
            )
            items[template_id] = definition
        self._items = items

    def _load_starter_inventory(self, path: Path) -> None:
        data = json.loads(path.read_text(encoding='utf-8'))
        if not isinstance(data, dict) or 'items' not in data:
            raise ItemCatalogError(f'starter_inventory.json missing "items" key: {path}')
        raw_items = data['items']
        if not isinstance(raw_items, list):
            raise ItemCatalogError(f'starter_inventory.json "items" must be a list: {path}')
        seen_offsets: set[int] = set()
        starter_items: list[StarterItemDefinition] = []
        for raw in raw_items:
            if not isinstance(raw, dict):
                raise ItemCatalogError(f'each starter item must be a dict: {path}')
            template_id = int(raw['template_id'])
            if template_id not in self._items:
                raise ItemCatalogError(f'starter item references unknown template_id={template_id}')
            instance_offset = int(raw['instance_offset'])
            if instance_offset in seen_offsets:
                raise ItemCatalogError(f'duplicate instance_offset: {instance_offset}')
            seen_offsets.add(instance_offset)
            starter_items.append(StarterItemDefinition(
                template_id=template_id,
                instance_offset=instance_offset,
                quantity=int(raw.get('quantity', 1)),
                location=str(raw.get('location', 'bag')),
            ))
        self._starter_items = starter_items

    def require(self, template_id: int) -> ItemDefinition:
        try:
            return self._items[template_id]
        except KeyError:
            raise KeyError(f'unknown template_id: {template_id}')

    def resolve(self, instance: dict[str, Any]) -> dict[str, Any]:
        """Merge template definition with instance data.

        Returns a new dict.  Template fields are defaults; instance state
        overrides where present.  The original instance dict is not modified.
        """
        template_id = int(instance.get('template_id', 0))
        definition = self._items.get(template_id)
        if definition is None:
            return dict(instance)
        resolved: dict[str, Any] = {
            'template_id': template_id,
            'kind': definition.kind,
            'name': definition.name,
            'description': definition.description,
            'max_quantity': definition.max_quantity,
            'equipment_slot': definition.equipment_slot,
            'price': definition.price,
            'level_required': definition.level_required,
            'icon_code': definition.icon_code,
            'quality': definition.quality,
            'sort_group': definition.sort_group,
            'sort_order': definition.sort_order,
            'equipment_attributes': list(definition.equipment_attributes),
            'appearance_properties': dict(definition.appearance_properties),
            'item_flags': definition.item_flags,
            'action_flags': definition.action_flags,
            'heal': definition.heal,
            'mount_model': definition.mount_model,
        }
        for key in ('id', 'quantity', 'location', 'last_heal', 'expires_at',
                     'strengthen_level', 'base_equipment_attributes',
                     'equipment_attributes', 'state_flags'):
            if key in instance:
                resolved[key] = instance[key]
        return resolved

    def starter_instances(self, role_id: int) -> list[dict[str, Any]]:
        """Generate minimal instance records for a new character's starter items."""
        item_base = role_id * 100
        result: list[dict[str, Any]] = []
        for si in self._starter_items:
            result.append({
                'id': item_base + si.instance_offset,
                'template_id': si.template_id,
                'quantity': si.quantity,
                'location': si.location,
            })
        return result


_DEFAULT_ITEMS_FILE = Path(__file__).resolve().parent / 'data' / 'catalog' / 'items.json'
_DEFAULT_STARTER_FILE = Path(__file__).resolve().parent / 'data' / 'catalog' / 'starter_inventory.json'
_DEFAULT_PREVIEW_FILE = (
    Path(__file__).resolve().parent / 'data' / 'catalog' / 'equipment_resource_preview_items.json'
)


def default_item_registry() -> ItemRegistry:
    extra = (_DEFAULT_PREVIEW_FILE,) if _DEFAULT_PREVIEW_FILE.is_file() else ()
    return ItemRegistry(_DEFAULT_ITEMS_FILE, _DEFAULT_STARTER_FILE, extra_items_files=extra)
