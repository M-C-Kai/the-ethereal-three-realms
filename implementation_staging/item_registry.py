from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


class ItemCatalogError(Exception):
    """Raised when item catalog or starter inventory is invalid."""


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

    def __init__(self, items_file: Path, starter_inventory_file: Path) -> None:
        self._items: dict[int, ItemDefinition] = {}
        self._starter_items: list[StarterItemDefinition] = []
        self._load_items(items_file)
        self._load_starter_inventory(starter_inventory_file)

    def _load_items(self, path: Path) -> None:
        data = json.loads(path.read_text(encoding='utf-8'))
        if not isinstance(data, dict) or 'items' not in data:
            raise ItemCatalogError(f'items.json missing "items" key: {path}')
        raw_items = data['items']
        if not isinstance(raw_items, list):
            raise ItemCatalogError(f'items.json "items" must be a list: {path}')
        seen_ids: set[int] = set()
        items: dict[int, ItemDefinition] = {}
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


def default_item_registry() -> ItemRegistry:
    return ItemRegistry(_DEFAULT_ITEMS_FILE, _DEFAULT_STARTER_FILE)
