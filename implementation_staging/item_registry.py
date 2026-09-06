from __future__ import annotations

import json
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable, Sequence


PREVIEW_QUALITY = 1
PREVIEW_SERIAL_COLLISION_OFFSET = 50_000

WEAPON_APPEARANCE_MAPPING_FILE = (
    Path(__file__).resolve().parent / 'data' / 'catalog' / 'weapon_appearance_mapping.json'
)
HELMET_APPEARANCE_MAPPING_FILE = (
    Path(__file__).resolve().parent / 'data' / 'catalog' / 'helmet_appearance_mapping.json'
)
ARMOR_APPEARANCE_MAPPING_FILE = (
    Path(__file__).resolve().parent / 'data' / 'catalog' / 'armor_appearance_mapping.json'
)
UNSUPPORTED_EQUIPMENT_FILE = (
    Path(__file__).resolve().parent / 'data' / 'catalog' / 'unsupported_equipment_slots.json'
)
MOUNT_APPEARANCE_MAPPING_FILE = (
    Path(__file__).resolve().parent / 'data' / 'catalog' / 'mount_appearance_mapping.json'
)


@lru_cache(maxsize=1)
def _weapon_icon_to_image_mapping() -> dict[int, int]:
    """Load the weapon appearance relation from the catalog data file."""
    data = json.loads(WEAPON_APPEARANCE_MAPPING_FILE.read_text(encoding='utf-8'))
    if not isinstance(data, dict) or int(data.get('version', 0)) != 1:
        raise ValueError(
            f'invalid weapon appearance mapping catalog: {WEAPON_APPEARANCE_MAPPING_FILE}'
        )
    raw_mapping = data.get('icon_to_weapon_image')
    if not isinstance(raw_mapping, dict) or not raw_mapping:
        raise ValueError(
            f'weapon appearance mapping is empty: {WEAPON_APPEARANCE_MAPPING_FILE}'
        )
    mapping: dict[int, int] = {}
    for raw_icon, raw_image in raw_mapping.items():
        icon_code = int(raw_icon)
        weapon_image = int(raw_image)
        if icon_code <= 0 or weapon_image <= 0:
            raise ValueError(
                f'invalid weapon appearance pair {raw_icon!r}->{raw_image!r}'
            )
        if icon_code in mapping:
            raise ValueError(f'duplicate weapon icon_code after normalization: {icon_code}')
        mapping[icon_code] = weapon_image
    return mapping


def weapon_icon_to_image_mapping() -> dict[int, int]:
    """Return a copy of the catalog-backed icon_code -> weapon image mapping."""
    return dict(_weapon_icon_to_image_mapping())


@lru_cache(maxsize=1)
def _helmet_icon_to_property20_mapping() -> dict[int, int]:
    """Load the evidence-backed helmet icon -> property20 mapping catalog."""
    data = json.loads(HELMET_APPEARANCE_MAPPING_FILE.read_text(encoding='utf-8'))
    if not isinstance(data, dict) or int(data.get('version', 0)) != 1:
        raise ValueError(f'invalid helmet appearance mapping catalog: {HELMET_APPEARANCE_MAPPING_FILE}')
    if int(data.get('property', 0)) != 20 or int(data.get('image_base', 0)) != 21000:
        raise ValueError(f'invalid helmet appearance property metadata: {HELMET_APPEARANCE_MAPPING_FILE}')
    raw_mapping = data.get('icon_to_property20')
    if not isinstance(raw_mapping, dict):
        raise ValueError(f'helmet appearance mapping must be a dict: {HELMET_APPEARANCE_MAPPING_FILE}')
    mapping: dict[int, int] = {}
    for raw_icon, raw_value in raw_mapping.items():
        icon_code = int(raw_icon)
        property_value = int(raw_value)
        if icon_code <= 0 or property_value <= 0:
            raise ValueError(f'invalid helmet appearance pair {raw_icon!r}->{raw_value!r}')
        if icon_code in mapping:
            raise ValueError(f'duplicate helmet icon_code after normalization: {icon_code}')
        mapping[icon_code] = property_value
    return mapping


def helmet_icon_to_property20_mapping() -> dict[int, int]:
    """Return a copy of the catalog-backed helmet appearance mapping."""
    return dict(_helmet_icon_to_property20_mapping())


def helmet_property20_from_icon(icon_code: int) -> int:
    """Resolve helmet property20 from the catalog; unresolved icons are not guessed."""
    return _helmet_icon_to_property20_mapping().get(int(icon_code), 0)


@lru_cache(maxsize=1)
def _armor_appearance_catalog() -> tuple[dict[int, int], dict[int, int], dict[int, int], frozenset[int]]:
    """Load confirmed armor resources plus explicit preview/deprecation metadata."""
    data = json.loads(ARMOR_APPEARANCE_MAPPING_FILE.read_text(encoding='utf-8'))
    if not isinstance(data, dict) or int(data.get('version', 0)) != 1:
        raise ValueError(f'invalid armor appearance mapping catalog: {ARMOR_APPEARANCE_MAPPING_FILE}')
    if int(data.get('property', -1)) != 2 or int(data.get('image_base', 0)) != 14000:
        raise ValueError(f'invalid armor appearance property metadata: {ARMOR_APPEARANCE_MAPPING_FILE}')

    raw_resources = data.get('property2_to_image')
    if not isinstance(raw_resources, dict) or len(raw_resources) != 31:
        raise ValueError(f'armor property2 resource table must contain 31 entries: {ARMOR_APPEARANCE_MAPPING_FILE}')
    property_to_image: dict[int, int] = {}
    for raw_property, raw_image in raw_resources.items():
        property_value = int(raw_property)
        image_id = int(raw_image)
        if not 0 <= property_value <= 30 or image_id != 14000 + property_value:
            raise ValueError(f'invalid armor property2 resource {raw_property!r}->{raw_image!r}')
        property_to_image[property_value] = image_id
    if set(property_to_image) != set(range(31)):
        raise ValueError(f'armor property2 resource range is incomplete: {ARMOR_APPEARANCE_MAPPING_FILE}')

    raw_mapping = data.get('icon_to_property2')
    if not isinstance(raw_mapping, dict):
        raise ValueError(f'armor icon mapping must be a dict: {ARMOR_APPEARANCE_MAPPING_FILE}')
    icon_mapping: dict[int, int] = {}
    for raw_icon, raw_value in raw_mapping.items():
        icon_code = int(raw_icon)
        property_value = int(raw_value)
        if icon_code <= 0 or property_value not in property_to_image or property_value == 0:
            raise ValueError(f'invalid armor appearance pair {raw_icon!r}->{raw_value!r}')
        if icon_code in icon_mapping:
            raise ValueError(f'duplicate armor icon_code after normalization: {icon_code}')
        icon_mapping[icon_code] = property_value
    if len(icon_mapping) != 30 or set(icon_mapping.values()) != set(range(1, 31)):
        raise ValueError(f'armor icon mapping must cover property2 1..30 exactly: {ARMOR_APPEARANCE_MAPPING_FILE}')

    preview = data.get('resource_preview', {})
    raw_template_mapping = preview.get('template_to_property2') if isinstance(preview, dict) else None
    if not isinstance(raw_template_mapping, dict) or len(raw_template_mapping) != 30:
        raise ValueError(f'armor resource preview template table must contain 30 entries: {ARMOR_APPEARANCE_MAPPING_FILE}')
    template_mapping: dict[int, int] = {}
    for raw_template, raw_value in raw_template_mapping.items():
        template_id = int(raw_template)
        property_value = int(raw_value)
        expected_template = 30_000_000 + (14_000 + property_value) * 10 + 1
        if property_value not in property_to_image or template_id != expected_template:
            raise ValueError(f'invalid armor preview template pair {raw_template!r}->{raw_value!r}')
        template_mapping[template_id] = property_value
    if set(template_mapping.values()) != set(range(1, 31)):
        raise ValueError(f'armor resource preview property range must be 1..30: {ARMOR_APPEARANCE_MAPPING_FILE}')

    raw_deprecated = data.get('deprecated_template_ids', [])
    if not isinstance(raw_deprecated, list):
        raise ValueError(f'armor deprecated_template_ids must be a list: {ARMOR_APPEARANCE_MAPPING_FILE}')
    deprecated = frozenset(int(value) for value in raw_deprecated)
    if 30_001_001 not in deprecated:
        raise ValueError('legacy starter armor 30001001 must remain deprecated')
    if 30_140_001 not in deprecated:
        raise ValueError('legacy property2=0 armor preview 30140001 must remain deprecated')
    return property_to_image, icon_mapping, template_mapping, deprecated


def armor_property2_to_image_mapping() -> dict[int, int]:
    """Return confirmed property2 -> armor image mapping (14000..14030)."""
    return dict(_armor_appearance_catalog()[0])


def armor_icon_to_property2_mapping() -> dict[int, int]:
    """Return only explicitly confirmed icon_code -> property2 armor pairs."""
    return dict(_armor_appearance_catalog()[1])


def armor_resource_preview_template_mapping() -> dict[int, int]:
    """Return resource-preview template_id -> property2 for the 30 equippable armor bodies."""
    return dict(_armor_appearance_catalog()[2])


def deprecated_armor_template_ids() -> frozenset[int]:
    """Return local armor templates that must be removed from saved inventories."""
    return _armor_appearance_catalog()[3]


@lru_cache(maxsize=1)
def _unsupported_equipment_catalog() -> tuple[frozenset[int], frozenset[int]]:
    """Load temporarily disabled equipment slots and their legacy local templates."""
    data = json.loads(UNSUPPORTED_EQUIPMENT_FILE.read_text(encoding='utf-8'))
    if not isinstance(data, dict) or int(data.get('version', 0)) != 1:
        raise ValueError(f'invalid unsupported equipment catalog: {UNSUPPORTED_EQUIPMENT_FILE}')
    raw_slots = data.get('disabled_slots')
    raw_templates = data.get('deprecated_template_ids')
    if not isinstance(raw_slots, list) or not isinstance(raw_templates, list):
        raise ValueError(f'invalid unsupported equipment payload: {UNSUPPORTED_EQUIPMENT_FILE}')
    slots = frozenset(int(value) for value in raw_slots)
    templates = frozenset(int(value) for value in raw_templates)
    if slots != frozenset({12, 13, 14}):
        raise ValueError(f'unexpected disabled equipment slots: {sorted(slots)}')
    if not templates:
        raise ValueError('unsupported equipment deprecated template list is empty')
    return slots, templates


def unsupported_equipment_slots() -> frozenset[int]:
    """Return equipment slots that must not be auto-granted yet."""
    return _unsupported_equipment_catalog()[0]


def deprecated_unsupported_equipment_template_ids() -> frozenset[int]:
    """Return old local starter/preview templates removed from saved roles."""
    return _unsupported_equipment_catalog()[1]


@lru_cache(maxsize=1)
def deprecated_mount_template_ids() -> frozenset[int]:
    """Return all mount templates that must not be auto-owned by roles."""
    data = json.loads(MOUNT_APPEARANCE_MAPPING_FILE.read_text(encoding='utf-8'))
    image_base = int(data.get('image_base', 40000))
    projection = data.get('item_projection', {})
    template_base = int(projection.get('template_base', 170900000))
    named = data.get('named_templates', {})
    template_ids: set[int] = set()
    for family in data.get('families', []):
        for raw_image_id in family.get('image_ids', []):
            image_id = int(raw_image_id)
            ride_code = image_id - image_base
            override = named.get(str(image_id), {})
            template_ids.add(int(override.get('template_id', template_base + ride_code)))
    expected = int(data.get('count', len(template_ids)))
    if len(template_ids) != expected:
        raise ValueError(f'mount deprecated template count mismatch: expected={expected} actual={len(template_ids)}')
    return frozenset(template_ids)


def armor_property2_from_icon(icon_code: int) -> int | None:
    """Resolve armor property2 from a confirmed icon mapping; unresolved icons stay None."""
    return _armor_appearance_catalog()[1].get(int(icon_code))


def armor_property2_from_equipment(template_id: int, icon_code: int) -> int | None:
    """Resolve armor appearance from catalog data only.

    Dedicated 14000..14030 preview equipment is keyed by template_id. Ordinary
    armor still requires an explicit icon_code mapping and is never guessed.
    """
    catalog = _armor_appearance_catalog()
    preview_value = catalog[2].get(int(template_id))
    if preview_value is not None:
        return preview_value
    return catalog[1].get(int(icon_code))

def battle_weapon_image_from_icon(icon_code: int) -> int:
    """Resolve one weapon image from the catalog; unknown icons are not guessed."""
    return _weapon_icon_to_image_mapping().get(int(icon_code), 0)


def battle_weapon_field2_from_icon(icon_code: int, quality: int) -> int:
    """Build APK 1048 field[2]: battle image * 10 + quality selector."""
    image_id = battle_weapon_image_from_icon(icon_code)
    quality_value = int(quality)
    if image_id == 0 or not 0 <= quality_value <= 9:
        return 0
    return image_id * 10 + quality_value
# Compatibility-preview pairing only. Not an official icon→appearance mapping.
PREVIEW_SLOT_APPEARANCE_PROPERTY = {
    2: 16,
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
    quality: int = PREVIEW_QUALITY,
) -> int:
    """Return the complete map weapon code for character property 7.

    APK v.r() routes property 7 to v.e(I). v.e(I) decodes this value
    exactly like battle 1048 field[2]: value//10 is the weapon image
    and value%10 is the quality overlay selector.
    """
    value = battle_weapon_field2_from_icon(icon_code, quality)
    if value == 0:
        raise ItemCatalogError(f'unknown weapon appearance icon_code={icon_code}')
    return value


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
    if slot == 1:
        value = helmet_property20_from_icon(icon_code)
        return {'20': value} if value > 0 else {}
    if slot == 3:
        value = armor_property2_from_icon(icon_code)
        return {'2': value} if value is not None else {}
    if slot == 10:
        return {
            '7': preview_weapon_property7(icon_code)
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
