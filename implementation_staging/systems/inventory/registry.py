from __future__ import annotations

import json
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable, Sequence


PREVIEW_QUALITY = 1
PREVIEW_SERIAL_COLLISION_OFFSET = 50_000

WEAPON_APPEARANCE_MAPPING_FILE = (
    Path(__file__).resolve().parents[2] / 'data' / 'catalog' / 'weapon_appearance_mapping.json'
)
HELMET_APPEARANCE_MAPPING_FILE = (
    Path(__file__).resolve().parents[2] / 'data' / 'catalog' / 'helmet_appearance_mapping.json'
)
ARMOR_APPEARANCE_MAPPING_FILE = (
    Path(__file__).resolve().parents[2] / 'data' / 'catalog' / 'armor_appearance_mapping.json'
)
UNSUPPORTED_EQUIPMENT_FILE = (
    Path(__file__).resolve().parents[2] / 'data' / 'catalog' / 'unsupported_equipment_slots.json'
)
MOUNT_APPEARANCE_MAPPING_FILE = (
    Path(__file__).resolve().parents[2] / 'data' / 'catalog' / 'mount_appearance_mapping.json'
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
    """Return only explicitly deprecated mount templates.

    The earlier 54-template blanket removal was only for cleaning the
    accidentally granted starter atlas.  Legacy bags are now handled by
    the one-time role-bag migration, so real acquired mount instances
    must survive future logins.
    """
    data = json.loads(MOUNT_APPEARANCE_MAPPING_FILE.read_text(encoding='utf-8'))
    raw = data.get('deprecated_template_ids', [])
    if not isinstance(raw, list):
        raise ValueError('mount deprecated_template_ids must be a list')
    return frozenset(int(value) for value in raw)


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


def weapon_effect_selector_from_strengthen_level(strengthen_level: int) -> int:
    """Map server strengthening +0..+9 to the APK weapon effect selector.

    Confirmed compatibility rule for this project: +0..+3 have no external
    weapon effect; +4..+9 select the six bundled effect stages 1..6.
    """
    try:
        level = int(strengthen_level)
    except (TypeError, ValueError):
        return 0
    if not 0 <= level <= 9:
        return 0
    return 0 if level < 4 else level - 3


def weapon_appearance_field_from_icon_and_strengthen(
    icon_code: int,
    strengthen_level: int,
) -> int:
    """Build live map/battle weapon code from body image and strengthen glow."""
    image_id = battle_weapon_image_from_icon(icon_code)
    if image_id == 0:
        return 0
    return image_id * 10 + weapon_effect_selector_from_strengthen_level(strengthen_level)
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
    innate_attributes: tuple[int, ...] = (0, 0, 0, 0, 0)
    acquired_attributes: tuple[int, ...] = (0, 0, 0, 0, 0)
    extra_attributes: tuple[int, ...] = (0, 0, 0, 0, 0)
    strength: int = 0
    max_durability: int = 0
    socket_count: int = 0
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
            five_element_blocks: dict[str, tuple[int, ...]] = {}
            for attr_name in ('innate_attributes', 'acquired_attributes'):
                raw_values = raw.get(attr_name, [0, 0, 0, 0, 0])
                if not isinstance(raw_values, list) or len(raw_values) != 5:
                    raise ItemCatalogError(
                        f'{attr_name} must have 5 items for template_id={template_id}'
                    )
                values = tuple(int(x) for x in raw_values)
                if any(not 0 <= v <= 255 for v in values):
                    raise ItemCatalogError(
                        f'{attr_name} values must fit a byte for template_id={template_id}'
                    )
                five_element_blocks[attr_name] = values

            raw_extra = raw.get('extra_attributes', [0, 0, 0, 0, 0])
            if not isinstance(raw_extra, list) or len(raw_extra) != 5:
                raise ItemCatalogError(
                    f'extra_attributes must have 5 items for template_id={template_id}'
                )
            extra_attributes = tuple(int(x) for x in raw_extra)

            strength = int(raw.get('strength', template_id % 10 if is_equip else 0))
            if not 0 <= strength <= 9:
                raise ItemCatalogError(
                    f'strength must be 0..9 for template_id={template_id}'
                )

            max_durability = int(raw.get('max_durability', 200 if is_equip else 0))
            if not 0 <= max_durability <= 32767:
                raise ItemCatalogError(
                    f'max_durability must fit a positive short for template_id={template_id}'
                )

            socket_count = int(raw.get('socket_count', 0))
            if not 0 <= socket_count <= 5:
                raise ItemCatalogError(
                    f'socket_count must be 0..5 for template_id={template_id}'
                )

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
                innate_attributes=five_element_blocks['innate_attributes'],
                acquired_attributes=five_element_blocks['acquired_attributes'],
                extra_attributes=extra_attributes,
                strength=strength,
                max_durability=max_durability,
                socket_count=socket_count,
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
            'innate_attributes': list(definition.innate_attributes),
            'acquired_attributes': list(definition.acquired_attributes),
            'extra_attributes': list(definition.extra_attributes),
            'strength': definition.strength,
            'max_durability': definition.max_durability,
            'socket_count': definition.socket_count,
            'appearance_properties': dict(definition.appearance_properties),
            'item_flags': definition.item_flags,
            'action_flags': definition.action_flags,
            'heal': definition.heal,
            'mount_model': definition.mount_model,
        }
        for key in ('id', 'quantity', 'location', 'last_heal', 'expires_at',
                     'strengthen_level', 'base_equipment_attributes',
                     'equipment_attributes', 'innate_attributes',
                     'acquired_attributes', 'extra_attributes',
                     'durability', 'socket_count', 'state_flags'):
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


_DEFAULT_ITEMS_FILE = Path(__file__).resolve().parents[2] / 'data' / 'catalog' / 'items.json'
_DEFAULT_STARTER_FILE = Path(__file__).resolve().parents[2] / 'data' / 'catalog' / 'starter_inventory.json'
_DEFAULT_PREVIEW_FILE = (
    Path(__file__).resolve().parents[2] / 'data' / 'catalog' / 'equipment_resource_preview_items.json'
)


def default_item_registry() -> ItemRegistry:
    extra = (_DEFAULT_PREVIEW_FILE,) if _DEFAULT_PREVIEW_FILE.is_file() else ()
    return ItemRegistry(_DEFAULT_ITEMS_FILE, _DEFAULT_STARTER_FILE, extra_items_files=extra)

STACKABLE_ITEM_FLAG = 0x40

# ---------------------------------------------------------------------------
# 装备强化静态规则（自 strengthening.py 收编）。
# ---------------------------------------------------------------------------
"""Pure rules for the APK-compatible local weapon-strengthening flow."""


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

# ---------------------------------------------------------------------------
# 装备开孔：APK e/ag + b/g 实证。
# g.b(j) 只接受 322250000..322250003 作为开孔材料。
# 官方帮助仅锁定“第一孔 100%，后四孔逐次降低，特殊混沌石除外”；
# 后四孔普通石的精确官方概率未找到，因此这里使用本地兼容概率。
# 322250001/2 的名称来自历史活动资料，但具体 ID→名称对应仍属本地映射。
# ---------------------------------------------------------------------------
CHAOS_STONE_TEMPLATE_MIN = 322_250_000
CHAOS_STONE_TEMPLATE_MAX = 322_250_003
CHAOS_STONE_TEMPLATE_ID = 322_250_000
TIANYUAN_CHAOS_STONE_TEMPLATE_ID = 322_250_001
SANCAI_CHAOS_STONE_TEMPLATE_ID = 322_250_002
SPECIAL_CHAOS_STONE_TEMPLATE_ID = 322_250_003
NORMAL_CHAOS_SOCKET_RATES = (10_000, 7_500, 5_000, 3_000, 1_500)


@dataclass(frozen=True)
class ChaosStoneDefinition:
    template_id: int
    name: str
    special: bool


CHAOS_STONE_DEFINITIONS = {
    CHAOS_STONE_TEMPLATE_ID: ChaosStoneDefinition(
        CHAOS_STONE_TEMPLATE_ID, '混沌石', False,
    ),
    TIANYUAN_CHAOS_STONE_TEMPLATE_ID: ChaosStoneDefinition(
        TIANYUAN_CHAOS_STONE_TEMPLATE_ID, '天元混沌石', True,
    ),
    SANCAI_CHAOS_STONE_TEMPLATE_ID: ChaosStoneDefinition(
        SANCAI_CHAOS_STONE_TEMPLATE_ID, '三才混沌石', True,
    ),
    SPECIAL_CHAOS_STONE_TEMPLATE_ID: ChaosStoneDefinition(
        SPECIAL_CHAOS_STONE_TEMPLATE_ID, '特殊混沌石', True,
    ),
}


def chaos_stone_definition_for(item: Mapping[str, object] | None) -> Optional[ChaosStoneDefinition]:
    if item is None:
        return None
    template_id = _template_id(item)
    if template_id is None:
        return None
    return CHAOS_STONE_DEFINITIONS.get(template_id)


def is_chaos_stone(item: Mapping[str, object]) -> bool:
    template_id = _template_id(item)
    return (
        template_id is not None
        and CHAOS_STONE_TEMPLATE_MIN <= template_id <= CHAOS_STONE_TEMPLATE_MAX
    )


def chaos_socket_rate(stone: ChaosStoneDefinition, opened_count: int) -> int:
    if type(opened_count) is not int or not 0 <= opened_count < 5:
        raise ValueError('opened socket count must be 0..4')
    if stone.special:
        # APK 帮助明确“特殊混沌石除外”，本地兼容服按全孔 100% 处理。
        return 10_000
    return NORMAL_CHAOS_SOCKET_RATES[opened_count]


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
