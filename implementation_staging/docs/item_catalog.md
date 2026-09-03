# Item Catalog

The Item Catalog separates item template data (names, icons, stats, appearance) from role instance data (quantities, locations, strengthen levels). This ensures `data/roles.json` only stores instance state.

## Architecture

```
data/catalog/items.json          ← 18 item templates (read-only)
data/catalog/starter_inventory.json  ← starter item list (read-only)
item_registry.py                 ← ItemRegistry, ItemDefinition, resolve()
server.py                        ← reads templates at runtime, never writes them to roles.json
```

## Data Flow

1. **New role**: `starter_instances(role_id)` → minimal `[{id, template_id, quantity, location}]`
2. **Load role**: `_ensure_items()` strips any leaked template fields, seeds weapon bases
3. **Display**: `item_frame()`, `character_appearance()` call `registry.resolve(item)` at encode time
4. **Save**: Only instance fields persist to `data/roles.json`

## Instance vs Template Fields

**Instance fields** (persisted to roles.json):
`id`, `template_id`, `quantity`, `location`, `last_heal`, `strengthen_level`, `base_equipment_attributes`, `equipment_attributes`, `state_flags`, `item_flags`

**Template fields** (resolved at read time, never persisted):
`name`, `description`, `max_quantity`, `price`, `level_required`, `icon_code`, `quality`, `sort_group`, `sort_order`, `equipment_slot`, `appearance_properties`, `action_flags`, `heal`, `mount_model`

## Key APIs

### `ItemRegistry`
- `require(template_id)` → `ItemDefinition` (raises `KeyError` if unknown)
- `resolve(instance)` → merged dict (template defaults + instance overrides, original not modified)
- `starter_instances(role_id)` → minimal item list

### `ItemDefinition` (frozen dataclass)
All template fields as attributes: `template_id`, `name`, `icon_code`, `equipment_slot`, `equipment_attributes`, `appearance_properties`, `max_quantity`, etc.

### `ensure_weapon_base_attributes(item, registry=None)`
Seeds `base_equipment_attributes` and `strengthen_level` for weapons that lack them. Used by tests and callers working with minimal instances.

## Migration Rules

`_ensure_items()` runs on every role load:
1. Strips template fields from all items (legacy cleanup)
2. Preserves `item_flags` for strengthening stones (instance state)
3. Merges starter defaults with existing items, stripping template fields from the merged result
4. Seeds `base_equipment_attributes` for weapons missing it
5. Runs `recalculate_equipment_attributes` on all weapons

## Catalog Files

### `items.json`
```json
{
  "version": 1,
  "items": [
    {
      "template_id": 100001001,
      "kind": "equipment",
      "name": "青锋剑",
      "equipment_slot": 10,
      "equipment_attributes": [3, 0, 0, 0],
      "icon_code": 101,
      "max_quantity": 1,
      ...
    }
  ]
}
```

### `starter_inventory.json`
```json
{
  "version": 1,
  "items": [
    { "template_id": 100001001, "instance_offset": 1, "quantity": 1, "location": "bag" },
    ...
  ]
}
```

`instance_offset` is stable across restarts. Instance ID = `role_id * 100 + offset`.

## Adding New Items

1. Add template to `data/catalog/items.json`
2. If it should be in starter inventory, add entry to `data/catalog/starter_inventory.json`
3. No code changes needed — `item_frame()`, `character_appearance()`, etc. resolve via registry automatically

## Tests

`tests/test_item_registry.py` contains 39 tests covering:
- Registry load/validate
- resolve() merge behavior
- starter_instances() minimal output
- Template field leak prevention (every template field checked for every item type)
- Instance state preservation
- Battle rewards minimal instances
- Weapon attack from instance state
- Item frame resolves from registry
- Character appearance from registry
