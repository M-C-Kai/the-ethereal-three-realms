from __future__ import annotations

import json
from pathlib import Path

ROOT = Path('implementation_staging')


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{label}: expected one match, got {count}')
    return text.replace(old, new, 1)


# 30 confirmed armor item icons: 03xx + 12xx + 13xx.
# property2=0 / image14000 is the default body resource, not a bag item.
icon_to_property2: dict[int, int] = {}
for offset, base in enumerate((300, 1200, 1300)):
    for frame in range(10):
        icon_to_property2[base + frame] = offset * 10 + frame + 1
property2_to_icon = {value: icon for icon, value in icon_to_property2.items()}
assert set(property2_to_icon) == set(range(1, 31))

# 1) Reclassify APK icon atlas groups 12 and 13 as armor icon resources.
resources_path = ROOT / 'data/catalog/apk_equipment_resources.json'
resources_payload = json.loads(resources_path.read_text(encoding='utf-8'))
for row in resources_payload['resources']:
    icon = int(row.get('icon_code', 0))
    if 1200 <= icon <= 1309:
        row['equipment_slot'] = 3
        row['slot_family'] = 'armor'
resources_path.write_text(json.dumps(resources_payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

# 2) Record exact bag-icon <-> property2 mapping in the armor catalog.
armor_path = ROOT / 'data/catalog/armor_appearance_mapping.json'
armor = json.loads(armor_path.read_text(encoding='utf-8'))
armor['status'] = 'apk_resource_family_and_item_icons_aligned'
armor['description'] = (
    '铠甲人物主体使用 property2：image_id=14000+property2。14000/property2=0 是默认身体资源；'
    '真正可装备的 30 套铠甲为 property2=1..30，并与 APK 三组 24x24 物品图标按资源顺序一一对应：'
    '0300..0309 -> 1..10，1200..1209 -> 11..20，1300..1309 -> 21..30。'
)
armor['armor_icon_codes'] = list(icon_to_property2)
armor['icon_to_property2'] = {str(icon): value for icon, value in icon_to_property2.items()}
armor['unresolved_icon_codes'] = []
armor['notes'] = [
    '0014000_71x32.png through 0014030_71x32.png are the APK armor/body resource family.',
    'property2=0 selects image14000 and is kept as the default body/no-equipped-armor resource.',
    'The 30 equippable armor appearances are property2=1..30.',
    'APK inventory icon atlases align as 0300..0309 -> property2 1..10, 1200..1209 -> 11..20, 1300..1309 -> 21..30.',
    'Resource groups 12 and 13 were previously misclassified as coat/accessory previews; they are armor inventory icon atlases.',
    'Legacy placeholder armor preview for property2=0 and legacy slot-3 icon-only previews are removed from saved inventories.',
]
preview = armor.setdefault('resource_preview', {})
preview['kind'] = 'apk_armor_resource_preview'
preview['description'] = (
    'Compatibility preview equipment for the 30 equippable APK armor bodies 14001..14030. '
    'Each item now uses its aligned APK 24x24 inventory icon; 14000/property2=0 is the default body and is not granted as an item.'
)
preview.pop('generic_icon_code', None)
preview['icon_is_placeholder'] = False
preview['property2_to_icon_code'] = {str(value): icon for value, icon in property2_to_icon.items()}
preview['template_id_formula'] = '30000000 + image_id * 10 + 1'
preview['template_to_property2'] = {
    str(30_000_000 + (14_000 + value) * 10 + 1): value
    for value in range(1, 31)
}
deprecated = {int(v) for v in armor.get('deprecated_template_ids', [])}
deprecated.add(30_140_001)  # old property2=0 preview template
armor['deprecated_template_ids'] = sorted(deprecated)
armor_path.write_text(json.dumps(armor, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

# 3) Runtime validation: 31 body resources remain, but only 30 equippable icon-mapped previews.
registry_path = ROOT / 'item_registry.py'
registry = registry_path.read_text(encoding='utf-8')
registry = replace_once(
    registry,
    "    raw_mapping = data.get('icon_to_property2')\n    if not isinstance(raw_mapping, dict):\n        raise ValueError(f'armor icon mapping must be a dict: {ARMOR_APPEARANCE_MAPPING_FILE}')\n    icon_mapping: dict[int, int] = {}\n    for raw_icon, raw_value in raw_mapping.items():\n        icon_code = int(raw_icon)\n        property_value = int(raw_value)\n        if icon_code <= 0 or property_value not in property_to_image:\n            raise ValueError(f'invalid armor appearance pair {raw_icon!r}->{raw_value!r}')\n        if icon_code in icon_mapping:\n            raise ValueError(f'duplicate armor icon_code after normalization: {icon_code}')\n        icon_mapping[icon_code] = property_value\n\n    preview = data.get('resource_preview', {})\n    raw_template_mapping = preview.get('template_to_property2') if isinstance(preview, dict) else None\n    if not isinstance(raw_template_mapping, dict) or len(raw_template_mapping) != 31:\n        raise ValueError(f'armor resource preview template table must contain 31 entries: {ARMOR_APPEARANCE_MAPPING_FILE}')\n",
    "    raw_mapping = data.get('icon_to_property2')\n    if not isinstance(raw_mapping, dict):\n        raise ValueError(f'armor icon mapping must be a dict: {ARMOR_APPEARANCE_MAPPING_FILE}')\n    icon_mapping: dict[int, int] = {}\n    for raw_icon, raw_value in raw_mapping.items():\n        icon_code = int(raw_icon)\n        property_value = int(raw_value)\n        if icon_code <= 0 or property_value not in property_to_image or property_value == 0:\n            raise ValueError(f'invalid armor appearance pair {raw_icon!r}->{raw_value!r}')\n        if icon_code in icon_mapping:\n            raise ValueError(f'duplicate armor icon_code after normalization: {icon_code}')\n        icon_mapping[icon_code] = property_value\n    if len(icon_mapping) != 30 or set(icon_mapping.values()) != set(range(1, 31)):\n        raise ValueError(f'armor icon mapping must cover property2 1..30 exactly: {ARMOR_APPEARANCE_MAPPING_FILE}')\n\n    preview = data.get('resource_preview', {})\n    raw_template_mapping = preview.get('template_to_property2') if isinstance(preview, dict) else None\n    if not isinstance(raw_template_mapping, dict) or len(raw_template_mapping) != 30:\n        raise ValueError(f'armor resource preview template table must contain 30 entries: {ARMOR_APPEARANCE_MAPPING_FILE}')\n",
    'registry armor mapping count',
)
registry = replace_once(
    registry,
    "    if set(template_mapping.values()) != set(range(31)):\n        raise ValueError(f'armor resource preview property range is incomplete: {ARMOR_APPEARANCE_MAPPING_FILE}')\n",
    "    if set(template_mapping.values()) != set(range(1, 31)):\n        raise ValueError(f'armor resource preview property range must be 1..30: {ARMOR_APPEARANCE_MAPPING_FILE}')\n",
    'registry armor preview range',
)
registry = replace_once(
    registry,
    "    if 30_001_001 not in deprecated:\n        raise ValueError('legacy starter armor 30001001 must remain deprecated')\n",
    "    if 30_001_001 not in deprecated:\n        raise ValueError('legacy starter armor 30001001 must remain deprecated')\n    if 30_140_001 not in deprecated:\n        raise ValueError('legacy property2=0 armor preview 30140001 must remain deprecated')\n",
    'registry base armor deprecation',
)
registry = registry.replace(
    'Return resource-preview template_id -> property2 for all 31 armor bodies.',
    'Return resource-preview template_id -> property2 for the 30 equippable armor bodies.',
)
registry_path.write_text(registry, encoding='utf-8')

# 4) Generator: use the real icon attached to each property2; do not issue 14000.
generator_path = ROOT / 'tools/build_equipment_resource_preview_items.py'
generator = generator_path.read_text(encoding='utf-8')
generator = replace_once(
    generator,
    "    armor_preview = armor_catalog['resource_preview']\n    generic_armor_icon = int(armor_preview['generic_icon_code'])\n    template_to_property2 = {\n        int(template_id): int(value)\n        for template_id, value in armor_preview['template_to_property2'].items()\n    }\n",
    "    armor_preview = armor_catalog['resource_preview']\n    property2_to_icon = {\n        int(value): int(icon_code)\n        for value, icon_code in armor_preview['property2_to_icon_code'].items()\n    }\n    template_to_property2 = {\n        int(template_id): int(value)\n        for template_id, value in armor_preview['template_to_property2'].items()\n    }\n",
    'generator armor icon table',
)
generator = replace_once(
    generator,
    "        image_id = 14000 + property2\n        preview_items.append({\n",
    "        image_id = 14000 + property2\n        icon_code = property2_to_icon[property2]\n        preview_items.append({\n",
    'generator armor icon resolve',
)
generator = replace_once(
    generator,
    "            'description': (\n                f'APK确认人物铠甲主体资源 {image_id} / property2={property2}。'\n                '背包图标0300仅作铠甲类别占位，不代表官方图标与外观对应关系。'\n            ),\n",
    "            'description': (\n                f'APK铠甲主体资源 {image_id} / property2={property2}；'\n                f'物品图标 icon_code={icon_code:04d} 已按 APK 铠甲图标组对齐。'\n            ),\n",
    'generator armor description',
)
generator = replace_once(
    generator,
    "            'icon_code': generic_armor_icon,\n",
    "            'icon_code': icon_code,\n",
    'generator armor icon field',
)
generator = generator.replace(
    '铠甲旧0300..0309预览已废弃；现在下发31个14000..14030资源预览，槽3只使用property2。',
    '铠甲下发30件：0300..0309→14001..14010、1200..1209→14011..14020、1300..1309→14021..14030；14000是默认身体不作为装备下发。',
)
generator_path.write_text(generator, encoding='utf-8')

# 5) Existing roles must drop the old property2=0 preview and rebuild against v4.
server_path = ROOT / 'server.py'
server = server_path.read_text(encoding='utf-8')
server = replace_once(
    server,
    'EQUIPMENT_RESOURCE_PREVIEW_VERSION = 3',
    'EQUIPMENT_RESOURCE_PREVIEW_VERSION = 4',
    'server preview version',
)
server_path.write_text(server, encoding='utf-8')

# 6) Update focused tests.
test_path = ROOT / 'tests/test_armor_appearance_mapping.py'
test = test_path.read_text(encoding='utf-8')
start = test.index('    def test_icon_mapping_remains_unresolved_and_not_guessed(self):')
end = test.index('    def test_real_and_preview_armor_never_use_property15(self):')
replacement = '''    def test_icon_mapping_covers_30_equippable_armors(self):\n        expected = {}\n        for offset, base in enumerate((300, 1200, 1300)):\n            for frame in range(10):\n                expected[base + frame] = offset * 10 + frame + 1\n        self.assertEqual(armor_icon_to_property2_mapping(), expected)\n        for icon_code, property2 in expected.items():\n            self.assertEqual(armor_property2_from_icon(icon_code), property2)\n            self.assertEqual(\n                preview_appearance_properties(3, 0, {}, icon_code=icon_code),\n                {'2': property2},\n            )\n\n    def test_resource_preview_templates_cover_30_equippable_armors(self):\n        mapping = armor_resource_preview_template_mapping()\n        self.assertEqual(len(mapping), 30)\n        self.assertEqual(set(mapping.values()), set(range(1, 31)))\n        for template_id, property2 in mapping.items():\n            self.assertEqual(template_id, 30_000_000 + (14_000 + property2) * 10 + 1)\n            self.assertEqual(armor_property2_from_equipment(template_id, 0), property2)\n\n    def test_default_body_preview_is_deprecated(self):\n        self.assertIn(30_140_001, deprecated_armor_template_ids())\n\n'''
test = test[:start] + replacement + test[end:]
# legacy expected set now also includes old property2=0 preview; if the old method survived elsewhere, normalize it.
test = test.replace(
    "expected = {30_001_001, *[30_003_001 + frame * 10 for frame in range(10)]}",
    "expected = {30_001_001, 30_140_001, *[30_003_001 + frame * 10 for frame in range(10)]}",
)
test_path.write_text(test, encoding='utf-8')

migration_path = ROOT / 'tests/test_armor_inventory_migration.py'
migration = migration_path.read_text(encoding='utf-8')
migration = migration.replace('31_resource_armors_reissued', '30_equippable_armors_reissued')
migration = migration.replace(']), 31)', ']), 30)')
migration_path.write_text(migration, encoding='utf-8')

cleanup_path = ROOT / 'tests/test_inventory_cleanup_v3.py'
cleanup = cleanup_path.read_text(encoding='utf-8')
cleanup = cleanup.replace("role['equipment_resource_preview_version'] = 2", "role['equipment_resource_preview_version'] = 3")
cleanup = cleanup.replace("self.assertEqual(role['equipment_resource_preview_version'], 3)", "self.assertEqual(role['equipment_resource_preview_version'], 4)")
cleanup = cleanup.replace("self.assertEqual(len(payload['items']), 251)", "self.assertEqual(len(payload['items']), 250)")
cleanup_path.write_text(cleanup, encoding='utf-8')

registry_test_path = ROOT / 'tests/test_item_registry.py'
registry_test = registry_test_path.read_text(encoding='utf-8')
registry_test = registry_test.replace('self.assertEqual(len(items), 251)', 'self.assertEqual(len(items), 250)')
registry_test = registry_test.replace('self.assertEqual(len(preview_ids), 251)', 'self.assertEqual(len(preview_ids), 250)')
registry_test = registry_test.replace('self.assertEqual(len(armor_items), 31)', 'self.assertEqual(len(armor_items), 30)')
registry_test = registry_test.replace("self.assertTrue(all(int(item['icon_code']) == 300 for item in armor_items))", "self.assertEqual({int(item['icon_code']) for item in armor_items}, set(range(300,310)) | set(range(1200,1210)) | set(range(1300,1310)))")
registry_test_path.write_text(registry_test, encoding='utf-8')

# 7) Dedicated regression for the atlas/resource alignment.
alignment_test = ROOT / 'tests/test_armor_icon_alignment.py'
alignment_test.write_text('''import json\nimport sys\nimport unittest\nfrom pathlib import Path\n\nsys.path.insert(0, str(Path(__file__).resolve().parents[1]))\n\nfrom item_registry import ARMOR_APPEARANCE_MAPPING_FILE, armor_icon_to_property2_mapping\n\nROOT = Path(__file__).resolve().parents[1]\n\n\nclass ArmorIconAlignmentTests(unittest.TestCase):\n    def expected(self):\n        result = {}\n        for offset, base in enumerate((300, 1200, 1300)):\n            for frame in range(10):\n                result[base + frame] = offset * 10 + frame + 1\n        return result\n\n    def test_30_item_icons_align_to_property2_1_through_30(self):\n        self.assertEqual(armor_icon_to_property2_mapping(), self.expected())\n\n    def test_groups_3_12_13_are_catalogued_as_armor_icons(self):\n        payload = json.loads((ROOT / 'data/catalog/apk_equipment_resources.json').read_text(encoding='utf-8'))\n        rows = [row for row in payload['resources'] if int(row['icon_code']) in self.expected()]\n        self.assertEqual(len(rows), 30)\n        self.assertTrue(all(int(row['equipment_slot']) == 3 for row in rows))\n        self.assertTrue(all(row['slot_family'] == 'armor' for row in rows))\n\n    def test_preview_uses_distinct_real_icons_and_never_grants_14000(self):\n        payload = json.loads((ROOT / 'data/catalog/equipment_resource_preview_items.json').read_text(encoding='utf-8'))\n        armor = [row for row in payload['items'] if int(row['equipment_slot']) == 3]\n        self.assertEqual(len(armor), 30)\n        actual = {int(row['icon_code']): int(row['appearance_properties']['2']) for row in armor}\n        self.assertEqual(actual, self.expected())\n        self.assertNotIn(0, {int(row['appearance_properties']['2']) for row in armor})\n        self.assertNotIn(30_140_001, {int(row['template_id']) for row in armor})\n\n    def test_catalog_marks_14000_as_base_not_equipment_preview(self):\n        data = json.loads(ARMOR_APPEARANCE_MAPPING_FILE.read_text(encoding='utf-8'))\n        self.assertEqual(data['property2_to_image']['0'], 14000)\n        self.assertNotIn('0', data['resource_preview']['property2_to_icon_code'])\n        self.assertNotIn('30140001', data['resource_preview']['template_to_property2'])\n        self.assertIn(30_140_001, {int(v) for v in data['deprecated_template_ids']})\n\n\nif __name__ == '__main__':\n    unittest.main()\n''', encoding='utf-8')

print('armor icon alignment patch prepared')
