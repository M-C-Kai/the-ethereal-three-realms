from __future__ import annotations

import json
from pathlib import Path

ROOT = Path('implementation_staging')
CATALOG = ROOT / 'data' / 'catalog'


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{label}: expected exactly one match, got {count}')
    return text.replace(old, new, 1)


# ---------------------------------------------------------------------------
# 1) Armor resource catalog: keep icon mapping unresolved, but add a dedicated
#    resource-preview template mapping for every confirmed 14000..14030 armor.
# ---------------------------------------------------------------------------
armor_path = CATALOG / 'armor_appearance_mapping.json'
armor = json.loads(armor_path.read_text(encoding='utf-8'))

old_preview_ids = [30_003_001 + frame * 10 for frame in range(10)]
deprecated_ids = [30_001_001, *old_preview_ids]
resource_preview = {
    'kind': 'apk_armor_resource_preview',
    'description': (
        'These are compatibility preview equipment templates for the confirmed APK '
        'armor body resources 14000..14030. The inventory icon is only a generic '
        'armor placeholder and is NOT an icon_code->property2 mapping.'
    ),
    'generic_icon_code': 300,
    'icon_is_placeholder': True,
    'template_id_formula': '30000000 + image_id * 10 + 1',
    'template_to_property2': {
        str(30_000_000 + (14_000 + value) * 10 + 1): value
        for value in range(31)
    },
}
armor['status'] = 'apk_resource_family_confirmed_resource_previews_ready_icon_mapping_unresolved'
armor['resource_preview'] = resource_preview
armor['deprecated_template_ids'] = deprecated_ids
notes = list(armor.get('notes', []))
for note in (
    'Legacy slot-3 preview templates 30003001..30003091 are deprecated and removed from role inventories.',
    'Legacy local starter armor template 30001001 is no longer auto-granted because its old appearance was incorrect.',
    '31 replacement armor preview templates are keyed directly by confirmed property2 values 0..30; their icon 0300 is only a neutral bag placeholder.',
):
    if note not in notes:
        notes.append(note)
armor['notes'] = notes
armor_path.write_text(json.dumps(armor, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

# ---------------------------------------------------------------------------
# 2) Stop granting the legacy starter armor.
# ---------------------------------------------------------------------------
starter_path = CATALOG / 'starter_inventory.json'
starter = json.loads(starter_path.read_text(encoding='utf-8'))
before = len(starter['items'])
starter['items'] = [
    row for row in starter['items']
    if int(row.get('template_id', 0)) != 30_001_001
]
if len(starter['items']) != before - 1:
    raise SystemExit('starter_inventory: expected exactly one legacy armor entry')
starter_path.write_text(json.dumps(starter, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

# ---------------------------------------------------------------------------
# 3) Runtime catalog reader: add resource-preview template lookup and
#    deprecated-template lookup.  icon_code mapping remains unresolved.
# ---------------------------------------------------------------------------
registry_path = ROOT / 'item_registry.py'
registry_text = registry_path.read_text(encoding='utf-8')
start = registry_text.index('@lru_cache(maxsize=1)\ndef _armor_appearance_catalog()')
end = registry_text.index('\ndef battle_weapon_image_from_icon', start)
new_armor_runtime = '''@lru_cache(maxsize=1)
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
        if icon_code <= 0 or property_value not in property_to_image:
            raise ValueError(f'invalid armor appearance pair {raw_icon!r}->{raw_value!r}')
        if icon_code in icon_mapping:
            raise ValueError(f'duplicate armor icon_code after normalization: {icon_code}')
        icon_mapping[icon_code] = property_value

    preview = data.get('resource_preview', {})
    raw_template_mapping = preview.get('template_to_property2') if isinstance(preview, dict) else None
    if not isinstance(raw_template_mapping, dict) or len(raw_template_mapping) != 31:
        raise ValueError(f'armor resource preview template table must contain 31 entries: {ARMOR_APPEARANCE_MAPPING_FILE}')
    template_mapping: dict[int, int] = {}
    for raw_template, raw_value in raw_template_mapping.items():
        template_id = int(raw_template)
        property_value = int(raw_value)
        expected_template = 30_000_000 + (14_000 + property_value) * 10 + 1
        if property_value not in property_to_image or template_id != expected_template:
            raise ValueError(f'invalid armor preview template pair {raw_template!r}->{raw_value!r}')
        template_mapping[template_id] = property_value
    if set(template_mapping.values()) != set(range(31)):
        raise ValueError(f'armor resource preview property range is incomplete: {ARMOR_APPEARANCE_MAPPING_FILE}')

    raw_deprecated = data.get('deprecated_template_ids', [])
    if not isinstance(raw_deprecated, list):
        raise ValueError(f'armor deprecated_template_ids must be a list: {ARMOR_APPEARANCE_MAPPING_FILE}')
    deprecated = frozenset(int(value) for value in raw_deprecated)
    if 30_001_001 not in deprecated:
        raise ValueError('legacy starter armor 30001001 must remain deprecated')
    return property_to_image, icon_mapping, template_mapping, deprecated


def armor_property2_to_image_mapping() -> dict[int, int]:
    """Return confirmed property2 -> armor image mapping (14000..14030)."""
    return dict(_armor_appearance_catalog()[0])


def armor_icon_to_property2_mapping() -> dict[int, int]:
    """Return only explicitly confirmed icon_code -> property2 armor pairs."""
    return dict(_armor_appearance_catalog()[1])


def armor_resource_preview_template_mapping() -> dict[int, int]:
    """Return resource-preview template_id -> property2 for all 31 armor bodies."""
    return dict(_armor_appearance_catalog()[2])


def deprecated_armor_template_ids() -> frozenset[int]:
    """Return local armor templates that must be removed from saved inventories."""
    return _armor_appearance_catalog()[3]


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

'''
registry_text = registry_text[:start] + new_armor_runtime + registry_text[end + 1:]
registry_path.write_text(registry_text, encoding='utf-8')

# ---------------------------------------------------------------------------
# 4) Generate preview inventory: drop the old 10 icon-only armor previews and
#    replace them with 31 direct 14000..14030 resource previews.
# ---------------------------------------------------------------------------
generator_path = ROOT / 'tools' / 'build_equipment_resource_preview_items.py'
g = generator_path.read_text(encoding='utf-8')
g = replace_once(
    g,
    "from item_registry import (\n    SLOT_FAMILY_LABELS,\n    preview_appearance_properties,\n    synthetic_preview_template_id,\n)",
    "from item_registry import (\n    ARMOR_APPEARANCE_MAPPING_FILE,\n    SLOT_FAMILY_LABELS,\n    preview_appearance_properties,\n    synthetic_preview_template_id,\n)",
    'generator imports',
)
g = replace_once(
    g,
    "    resources = json.loads(RESOURCES_FILE.read_text(encoding='utf-8'))['resources']\n    official_items = json.loads(ITEMS_FILE.read_text(encoding='utf-8'))['items']",
    "    resources = json.loads(RESOURCES_FILE.read_text(encoding='utf-8'))['resources']\n    armor_catalog = json.loads(ARMOR_APPEARANCE_MAPPING_FILE.read_text(encoding='utf-8'))\n    official_items = json.loads(ITEMS_FILE.read_text(encoding='utf-8'))['items']",
    'generator load armor catalog',
)
g = replace_once(
    g,
    "    for index, resource in enumerate(resources, start=1):\n        template_id = synthetic_preview_template_id(",
    "    for index, resource in enumerate(resources, start=1):\n        if int(resource['equipment_slot']) == 3:\n            # Old 0300..0309 icon-only armor previews are deprecated.\n            continue\n        template_id = synthetic_preview_template_id(",
    'generator skip old armor previews',
)
needle = "    by_slot: dict[int, list[dict]] = {}\n"
if needle not in g:
    raise SystemExit('generator armor insertion point not found')
armor_insert = '''    armor_preview = armor_catalog['resource_preview']
    generic_armor_icon = int(armor_preview['generic_icon_code'])
    template_to_property2 = {
        int(template_id): int(value)
        for template_id, value in armor_preview['template_to_property2'].items()
    }
    for template_id, property2 in sorted(template_to_property2.items(), key=lambda row: row[1]):
        image_id = 14000 + property2
        preview_items.append({
            'template_id': template_id,
            'kind': 'equipment',
            'name': f'APK铠甲资源-{image_id}',
            'description': (
                f'APK确认人物铠甲主体资源 {image_id} / property2={property2}。'
                '背包图标0300仅作铠甲类别占位，不代表官方图标与外观对应关系。'
            ),
            'max_quantity': 1,
            'equipment_slot': 3,
            'price': 0,
            'level_required': 1,
            'icon_code': generic_armor_icon,
            'quality': 1,
            'sort_group': 100,
            'sort_order': 0,
            'equipment_attributes': [0, 0, 0, 0],
            'appearance_properties': {'2': property2},
        })

    preview_items.sort(key=lambda item: (
        int(item['equipment_slot']),
        int(item['appearance_properties'].get('2', 999)) if int(item['equipment_slot']) == 3 else int(item['sort_order']),
        int(item['template_id']),
    ))
    for sort_order, item in enumerate(preview_items, start=1):
        item['sort_order'] = sort_order

'''
g = g.replace(needle, armor_insert + needle, 1)
g = replace_once(
    g,
    "        for preview_index, item in enumerate(slot_items):\n            item['appearance_properties'] = preview_appearance_properties(",
    "        for preview_index, item in enumerate(slot_items):\n            if slot == 3:\n                # Dedicated armor previews already carry the confirmed property2.\n                continue\n            item['appearance_properties'] = preview_appearance_properties(",
    'generator preserve armor property2',
)
g = g.replace(
    "                '铠甲只读取 armor_appearance_mapping.json，并使用 property2 / 14000..14030；严禁再使用 property15。'",
    "                '铠甲旧0300..0309预览已废弃；现在下发31个14000..14030资源预览，槽3只使用property2。'",
    1,
)
generator_path.write_text(g, encoding='utf-8')

# ---------------------------------------------------------------------------
# 5) Runtime migration and downlink: remove legacy armor instances from saved
#    roles, grant the new preview catalog, and resolve slot3 via template map.
# ---------------------------------------------------------------------------
server_path = ROOT / 'server.py'
s = server_path.read_text(encoding='utf-8')
s = replace_once(
    s,
    "from item_registry import (\n    ItemRegistry,\n    armor_property2_from_icon,\n    battle_weapon_field2_from_icon,\n    default_item_registry,\n)",
    "from item_registry import (\n    ItemRegistry,\n    armor_property2_from_equipment,\n    battle_weapon_field2_from_icon,\n    default_item_registry,\n    deprecated_armor_template_ids,\n)",
    'server armor imports',
)
s = replace_once(
    s,
    'EQUIPMENT_RESOURCE_PREVIEW_VERSION = 1',
    'EQUIPMENT_RESOURCE_PREVIEW_VERSION = 2',
    'preview version',
)
s = replace_once(
    s,
    "            armor_value = armor_property2_from_icon(int(resolved.get('icon_code', 0)))",
    "            armor_value = armor_property2_from_equipment(\n                int(resolved.get('template_id', 0)),\n                int(resolved.get('icon_code', 0)),\n            )",
    'armor downlink resolver',
)
cleanup_needle = "    items = role_items(role)\n    present = {\n"
if cleanup_needle not in s:
    raise SystemExit('ensure preview cleanup insertion point not found')
cleanup = '''    items = role_items(role)
    deprecated_armor = deprecated_armor_template_ids()
    kept_items: list[dict[str, object]] = []
    removed_legacy_armor = False
    for item in items:
        if not isinstance(item, dict):
            continue
        try:
            template_id = int(item.get('template_id', 0))
        except (TypeError, ValueError):
            template_id = 0
        if template_id in deprecated_armor:
            removed_legacy_armor = True
            continue
        kept_items.append(item)
    if removed_legacy_armor:
        role['items'] = kept_items
        items = role_items(role)
        changed = True
    present = {
'''
s = s.replace(cleanup_needle, cleanup, 1)
server_path.write_text(s, encoding='utf-8')

# ---------------------------------------------------------------------------
# 6) Focused tests for resource mapping, migration, and downlink.
# ---------------------------------------------------------------------------
armor_test = ROOT / 'tests' / 'test_armor_appearance_mapping.py'
armor_test.write_text('''import json\nimport sys\nimport unittest\nfrom pathlib import Path\n\nsys.path.insert(0, str(Path(__file__).resolve().parents[1]))\n\nfrom item_registry import (\n    ARMOR_APPEARANCE_MAPPING_FILE,\n    armor_icon_to_property2_mapping,\n    armor_property2_from_equipment,\n    armor_property2_from_icon,\n    armor_property2_to_image_mapping,\n    armor_resource_preview_template_mapping,\n    deprecated_armor_template_ids,\n    preview_appearance_properties,\n)\n\n\nclass ArmorAppearanceMappingTests(unittest.TestCase):\n    def test_apk_armor_resource_family_is_exact_14000_to_14030(self):\n        data = json.loads(ARMOR_APPEARANCE_MAPPING_FILE.read_text(encoding='utf-8'))\n        self.assertEqual(data['property'], 2)\n        self.assertEqual(data['image_slot'], 3)\n        self.assertEqual(data['image_base'], 14000)\n        self.assertEqual(data['property_range'], [0, 30])\n        self.assertEqual(data['image_range'], [14000, 14030])\n        self.assertEqual(data['dimensions'], [71, 32])\n        self.assertEqual(len(data['resources']), 31)\n        self.assertEqual(\n            [(row['property2'], row['image_id']) for row in data['resources']],\n            [(value, 14000 + value) for value in range(31)],\n        )\n\n    def test_runtime_reads_property2_resource_table_from_catalog(self):\n        self.assertEqual(\n            armor_property2_to_image_mapping(),\n            {value: 14000 + value for value in range(31)},\n        )\n\n    def test_icon_mapping_remains_unresolved_and_not_guessed(self):\n        self.assertEqual(armor_icon_to_property2_mapping(), {})\n        for icon_code in range(300, 310):\n            self.assertIsNone(armor_property2_from_icon(icon_code), icon_code)\n            self.assertEqual(\n                preview_appearance_properties(3, icon_code - 300, {}, icon_code=icon_code),\n                {},\n            )\n\n    def test_resource_preview_templates_cover_all_31_armors(self):\n        mapping = armor_resource_preview_template_mapping()\n        self.assertEqual(len(mapping), 31)\n        self.assertEqual(set(mapping.values()), set(range(31)))\n        for template_id, property2 in mapping.items():\n            self.assertEqual(template_id, 30_000_000 + (14_000 + property2) * 10 + 1)\n            self.assertEqual(armor_property2_from_equipment(template_id, 300), property2)\n\n    def test_legacy_armor_templates_are_deprecated(self):\n        expected = {30_001_001, *[30_003_001 + frame * 10 for frame in range(10)]}\n        self.assertEqual(set(deprecated_armor_template_ids()), expected)\n\n    def test_real_and_preview_armor_never_use_property15(self):\n        root = Path(__file__).resolve().parents[1]\n        for relative in ('data/catalog/items.json', 'data/catalog/equipment_resource_preview_items.json'):\n            payload = json.loads((root / relative).read_text(encoding='utf-8'))\n            armor = [item for item in payload['items'] if int(item.get('equipment_slot', 0)) == 3]\n            for item in armor:\n                self.assertNotIn('15', item.get('appearance_properties', {}))\n\n\nif __name__ == '__main__':\n    unittest.main()\n''', encoding='utf-8')

inventory_test = ROOT / 'tests' / 'test_armor_inventory_migration.py'
inventory_test.write_text('''import sys\nimport unittest\nfrom pathlib import Path\n\nsys.path.insert(0, str(Path(__file__).resolve().parents[1]))\n\nfrom item_registry import armor_resource_preview_template_mapping, deprecated_armor_template_ids\nfrom server import EQUIPMENT_RESOURCE_PREVIEW_VERSION, RoleStore, Settings, default_role\n\n\nclass ArmorInventoryMigrationTests(unittest.TestCase):\n    def test_old_armor_instances_are_deleted_and_31_resource_armors_reissued(self):\n        settings = Settings()\n        role = default_role(settings)\n        new_ids = set(armor_resource_preview_template_mapping())\n        deprecated = set(deprecated_armor_template_ids())\n\n        role['items'] = [\n            item for item in role['items']\n            if int(item.get('template_id', 0)) not in new_ids\n        ]\n        for index, template_id in enumerate(sorted(deprecated), start=1):\n            role['items'].append({\n                'id': 900_000 + index,\n                'template_id': template_id,\n                'quantity': 1,\n                'location': 'equipped' if index == 1 else 'bag',\n            })\n        role['equipment_resource_preview_version'] = 1\n\n        changed = RoleStore(settings)._ensure_items(role)\n        self.assertTrue(changed)\n        template_ids = [int(item.get('template_id', 0)) for item in role['items']]\n        self.assertTrue(deprecated.isdisjoint(template_ids))\n        self.assertEqual(set(template_ids) & new_ids, new_ids)\n        self.assertEqual(len([tid for tid in template_ids if tid in new_ids]), 31)\n        self.assertEqual(role['equipment_resource_preview_version'], EQUIPMENT_RESOURCE_PREVIEW_VERSION)\n\n    def test_legacy_starter_armor_is_not_regranted(self):\n        settings = Settings()\n        role = default_role(settings)\n        self.assertNotIn(30_001_001, {int(item.get('template_id', 0)) for item in role['items']})\n\n\nif __name__ == '__main__':\n    unittest.main()\n''', encoding='utf-8')

armor_downlink = ROOT / 'tests' / 'test_armor_downlink.py'
armor_downlink.write_text('''import sys\nimport unittest\nfrom pathlib import Path\nfrom unittest.mock import patch\n\nsys.path.insert(0, str(Path(__file__).resolve().parents[1]))\n\nfrom item_registry import armor_resource_preview_template_mapping\nfrom server import BASE_CHARACTER_APPEARANCE, Settings, character_appearance, default_role, role_items\n\n\nclass ArmorDownlinkTests(unittest.TestCase):\n    def _role_with_property2_equipped(self, property2: int):\n        settings = Settings()\n        role = default_role(settings)\n        target_template = next(\n            template_id for template_id, value in armor_resource_preview_template_mapping().items()\n            if value == property2\n        )\n        armor = None\n        for item in role_items(role):\n            item['location'] = 'bag'\n            if int(item.get('template_id', 0)) == target_template:\n                armor = item\n        self.assertIsNotNone(armor)\n        armor['location'] = 'equipped'\n        return settings, role, armor\n\n    def test_base_snapshot_clears_legacy_property15(self):\n        self.assertEqual(BASE_CHARACTER_APPEARANCE[2], 0)\n        self.assertEqual(BASE_CHARACTER_APPEARANCE[15], 0)\n\n    def test_resource_preview_armor_downlinks_exact_property2(self):\n        settings, role, _ = self._role_with_property2_equipped(12)\n        appearance = character_appearance(role, settings.item_registry)\n        self.assertEqual(appearance[2], 12)\n        self.assertEqual(appearance[15], 0)\n\n    def test_stale_template_property15_cannot_override_resource_mapping(self):\n        settings, role, _ = self._role_with_property2_equipped(7)\n        real_resolve = settings.item_registry.resolve\n\n        def stale_resolve(item):\n            resolved = real_resolve(item)\n            if int(resolved.get('equipment_slot', 0)) == 3:\n                resolved['appearance_properties'] = {'15': 34, '2': 30}\n            return resolved\n\n        with patch.object(settings.item_registry, 'resolve', side_effect=stale_resolve):\n            appearance = character_appearance(role, settings.item_registry)\n        self.assertEqual(appearance[2], 7)\n        self.assertEqual(appearance[15], 0)\n\n\nif __name__ == '__main__':\n    unittest.main()\n''', encoding='utf-8')

# Patch existing registry tests for the new preview inventory shape.
test_registry_path = ROOT / 'tests' / 'test_item_registry.py'
t = test_registry_path.read_text(encoding='utf-8')
t = replace_once(
    t,
    "    battle_weapon_field2_from_icon,\n    default_item_registry,",
    "    armor_resource_preview_template_mapping,\n    deprecated_armor_template_ids,\n    battle_weapon_field2_from_icon,\n    default_item_registry,",
    'test registry imports',
)
old_armour_test = '''    def test_armour_item_has_no_template_fields(self):
        keys = self._get_item_keys(ARMOUR_TEMPLATE_ID)
        for field in TEMPLATE_FIELDS:
            self.assertNotIn(field, keys, f'armour item should not have template field {field!r}')

'''
new_armour_test = '''    def test_deprecated_starter_armour_is_not_granted(self):
        settings = Settings()
        role = default_role(settings)
        self.assertNotIn(ARMOUR_TEMPLATE_ID, {int(item.get('template_id', 0)) for item in role['items']})

'''
t = replace_once(t, old_armour_test, new_armour_test, 'legacy armour starter test')
class_start = t.index('class EquipmentResourcePreviewCatalogTests(unittest.TestCase):')
main_start = t.index("if __name__ == '__main__':", class_start)
new_preview_class = '''class EquipmentResourcePreviewCatalogTests(unittest.TestCase):
    def test_preview_catalog_replaces_old_armor_items_with_31_resource_items(self):
        root = Path(__file__).resolve().parents[1]
        resources = json.loads(
            (root / 'data' / 'catalog' / 'apk_equipment_resources.json').read_text(encoding='utf-8')
        )['resources']
        preview = json.loads(
            (root / 'data' / 'catalog' / 'equipment_resource_preview_items.json').read_text(encoding='utf-8')
        )
        items = preview['items']
        self.assertEqual(len(resources), 252)
        self.assertEqual(len(items), 273)
        self.assertEqual(preview.get('status'), 'compatibility_preview')
        self.assertEqual(len({int(item['template_id']) for item in items}), 273)

        armor_items = [item for item in items if int(item['equipment_slot']) == 3]
        self.assertEqual(len(armor_items), 31)
        expected_mapping = armor_resource_preview_template_mapping()
        self.assertEqual(
            {int(item['template_id']): int(item['appearance_properties']['2']) for item in armor_items},
            expected_mapping,
        )
        self.assertTrue(all(int(item['icon_code']) == 300 for item in armor_items))
        self.assertTrue(
            set(deprecated_armor_template_ids()).isdisjoint(
                {int(item['template_id']) for item in items}
            )
        )

        nonarmor_resources = [r for r in resources if int(r['equipment_slot']) != 3]
        nonarmor_items = [i for i in items if int(i['equipment_slot']) != 3]
        self.assertEqual(len(nonarmor_resources), 242)
        self.assertEqual(len(nonarmor_items), 242)
        expected_by_icon = {int(r['icon_code']): int(r['equipment_slot']) for r in nonarmor_resources}
        actual_by_icon = {int(i['icon_code']): int(i['equipment_slot']) for i in nonarmor_items}
        self.assertEqual(actual_by_icon, expected_by_icon)

    def test_registry_loads_every_preview_template(self):
        registry = default_item_registry()
        preview_ids = registry.preview_template_ids()
        self.assertEqual(len(preview_ids), 273)
        for template_id in preview_ids:
            registry.require(template_id)


'''
t = t[:class_start] + new_preview_class + t[main_start:]
test_registry_path.write_text(t, encoding='utf-8')

# ---------------------------------------------------------------------------
# 7) Protocol lock note.
# ---------------------------------------------------------------------------
lock_path = ROOT / 'PROTOCOL_LOCK.md'
p = lock_path.read_text(encoding='utf-8')
marker = '## 铠甲背包资源迁移 v2'
if marker not in p:
    p += '''\n\n## 铠甲背包资源迁移 v2\n\n旧版本曾自动向每个角色背包发放槽3的 `0300..0309` 十个兼容预览铠甲，并额外通过 `starter_inventory.json` 发放本地构造的 `30001001/青纹铠甲`。这些物品建立在错误的铠甲外观路径上，现全部列为废弃模板。角色加载时必须从持久化 `items` 中删除这 11 个模板实例，即使其中某件处于已装备状态也要删除。\n\n替代下发为 APK 已确认的 31 个铠甲主体资源：`property2=0..30`，对应 `14000..14030`。兼容预览模板 ID 固定按 `30000000 + image_id*10 + 1` 生成，运行时通过 `armor_appearance_mapping.json/resource_preview/template_to_property2` 读取，不从背包图标推断外观。为了让 APK 背包可显示，这 31 个预览暂统一使用图标 `0300` 作为“铠甲类别占位图标”；这不是官方 `icon_code -> property2` 映射。\n\n`equipment_resource_preview_version` 升为 `2`。旧角色下一次加载时会删除旧铠甲并幂等补发 31 个新铠甲资源预览；新角色直接收到新预览，不再收到 `30001001`。\n'''
lock_path.write_text(p, encoding='utf-8')

print('armor inventory v2 patch prepared')
