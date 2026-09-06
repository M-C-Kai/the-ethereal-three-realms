from __future__ import annotations

import json
from pathlib import Path

ROOT = Path('implementation_staging')


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{label}: expected exactly one match, got {count}')
    return text.replace(old, new, 1)


# ---------------------------------------------------------------------------
# 1) 独立资料库：暂不下发没有明确装备/外观逻辑的槽位。
#    旧 preview template_id 直接从当前目录读取，避免假定每个槽固定 10 个资源。
# ---------------------------------------------------------------------------
unsupported_slots = {
    12: ('coat', '外套', 120_001_001),
    13: ('accessory', '饰品', 130_001_001),
    14: ('talisman', '法宝', 140_001_001),
}
current_preview = json.loads(
    (ROOT / 'data/catalog/equipment_resource_preview_items.json').read_text(encoding='utf-8')
)['items']
preview_ids: list[int] = []
slot_rows: list[dict[str, object]] = []
for slot, (family, label, starter_template_id) in unsupported_slots.items():
    slot_preview_ids = sorted(
        int(item['template_id'])
        for item in current_preview
        if int(item.get('equipment_slot', 0)) == slot
    )
    if not slot_preview_ids:
        raise SystemExit(f'no existing preview items found for disabled slot {slot}')
    preview_ids.extend(slot_preview_ids)
    slot_rows.append({
        'equipment_slot': slot,
        'family': family,
        'label': label,
        'starter_template_id': starter_template_id,
        'deprecated_preview_template_ids': slot_preview_ids,
    })

unsupported_payload = {
    'version': 1,
    'kind': 'unsupported_equipment_slots',
    'status': 'temporarily_disabled_until_equipment_mapping_is_confirmed',
    'description': (
        '这些装备槽当前没有确认的人物装备/外观下发关系，因此兼容服暂时不自动下发。'
        '旧角色中此前自动发放的本地 starter/preview 实例会在加载时迁移删除。'
    ),
    'slots': slot_rows,
    'disabled_slots': sorted(unsupported_slots),
    'starter_template_ids': [row[2] for row in unsupported_slots.values()],
    'deprecated_preview_template_ids': sorted(preview_ids),
    'deprecated_template_ids': sorted(
        preview_ids + [row[2] for row in unsupported_slots.values()]
    ),
}
(ROOT / 'data/catalog/unsupported_equipment_slots.json').write_text(
    json.dumps(unsupported_payload, ensure_ascii=False, indent=2) + '\n',
    encoding='utf-8',
)

# ---------------------------------------------------------------------------
# 2) item_registry：只从资料库读取禁用槽和需要清理的旧模板 ID。
# ---------------------------------------------------------------------------
registry_path = ROOT / 'item_registry.py'
registry = registry_path.read_text(encoding='utf-8')
registry = replace_once(
    registry,
    "ARMOR_APPEARANCE_MAPPING_FILE = (\n    Path(__file__).resolve().parent / 'data' / 'catalog' / 'armor_appearance_mapping.json'\n)\n",
    "ARMOR_APPEARANCE_MAPPING_FILE = (\n    Path(__file__).resolve().parent / 'data' / 'catalog' / 'armor_appearance_mapping.json'\n)\nUNSUPPORTED_EQUIPMENT_FILE = (\n    Path(__file__).resolve().parent / 'data' / 'catalog' / 'unsupported_equipment_slots.json'\n)\n",
    'item_registry unsupported file constant',
)
registry = replace_once(
    registry,
    "def deprecated_armor_template_ids() -> frozenset[int]:\n    \"\"\"Return local armor templates that must be removed from saved inventories.\"\"\"\n    return _armor_appearance_catalog()[3]\n\n\ndef armor_property2_from_icon(icon_code: int) -> int | None:\n",
    "def deprecated_armor_template_ids() -> frozenset[int]:\n    \"\"\"Return local armor templates that must be removed from saved inventories.\"\"\"\n    return _armor_appearance_catalog()[3]\n\n\n@lru_cache(maxsize=1)\ndef _unsupported_equipment_catalog() -> tuple[frozenset[int], frozenset[int]]:\n    \"\"\"Load temporarily disabled equipment slots and their legacy local templates.\"\"\"\n    data = json.loads(UNSUPPORTED_EQUIPMENT_FILE.read_text(encoding='utf-8'))\n    if not isinstance(data, dict) or int(data.get('version', 0)) != 1:\n        raise ValueError(f'invalid unsupported equipment catalog: {UNSUPPORTED_EQUIPMENT_FILE}')\n    raw_slots = data.get('disabled_slots')\n    raw_templates = data.get('deprecated_template_ids')\n    if not isinstance(raw_slots, list) or not isinstance(raw_templates, list):\n        raise ValueError(f'invalid unsupported equipment payload: {UNSUPPORTED_EQUIPMENT_FILE}')\n    slots = frozenset(int(value) for value in raw_slots)\n    templates = frozenset(int(value) for value in raw_templates)\n    if slots != frozenset({12, 13, 14}):\n        raise ValueError(f'unexpected disabled equipment slots: {sorted(slots)}')\n    if not templates:\n        raise ValueError('unsupported equipment deprecated template list is empty')\n    return slots, templates\n\n\ndef unsupported_equipment_slots() -> frozenset[int]:\n    \"\"\"Return equipment slots that must not be auto-granted yet.\"\"\"\n    return _unsupported_equipment_catalog()[0]\n\n\ndef deprecated_unsupported_equipment_template_ids() -> frozenset[int]:\n    \"\"\"Return old local starter/preview templates removed from saved roles.\"\"\"\n    return _unsupported_equipment_catalog()[1]\n\n\ndef armor_property2_from_icon(icon_code: int) -> int | None:\n",
    'item_registry unsupported loader',
)
registry_path.write_text(registry, encoding='utf-8')

# ---------------------------------------------------------------------------
# 3) 生成器：外套/饰品/法宝不再进入自动下发 preview catalog。
# ---------------------------------------------------------------------------
generator_path = ROOT / 'tools/build_equipment_resource_preview_items.py'
generator = generator_path.read_text(encoding='utf-8')
generator = replace_once(
    generator,
    "    preview_appearance_properties,\n    synthetic_preview_template_id,\n)",
    "    preview_appearance_properties,\n    synthetic_preview_template_id,\n    unsupported_equipment_slots,\n)",
    'generator import unsupported slots',
)
generator = replace_once(
    generator,
    "    resources = json.loads(RESOURCES_FILE.read_text(encoding='utf-8'))['resources']\n    armor_catalog = json.loads(ARMOR_APPEARANCE_MAPPING_FILE.read_text(encoding='utf-8'))",
    "    resources = json.loads(RESOURCES_FILE.read_text(encoding='utf-8'))['resources']\n    disabled_slots = unsupported_equipment_slots()\n    armor_catalog = json.loads(ARMOR_APPEARANCE_MAPPING_FILE.read_text(encoding='utf-8'))",
    'generator load disabled slots',
)
generator = replace_once(
    generator,
    "    for index, resource in enumerate(resources, start=1):\n        if int(resource['equipment_slot']) == 3:\n            # Old 0300..0309 icon-only armor previews are deprecated.\n            continue\n        template_id = synthetic_preview_template_id(",
    "    for index, resource in enumerate(resources, start=1):\n        slot = int(resource['equipment_slot'])\n        if slot == 3:\n            # Old 0300..0309 icon-only armor previews are deprecated.\n            continue\n        if slot in disabled_slots:\n            # 外套/饰品/法宝尚无确认装备关系，暂不进入角色背包。\n            continue\n        template_id = synthetic_preview_template_id(",
    'generator skip disabled slots',
)
generator = replace_once(
    generator,
    "                '铠甲旧0300..0309预览已废弃；现在下发31个14000..14030资源预览，槽3只使用property2。'\n                '其他防具 appearance_properties 仍引用 appearance-layer-audit 人物图层候选。'",
    "                '铠甲旧0300..0309预览已废弃；现在下发31个14000..14030资源预览，槽3只使用property2。'\n                '外套(slot12)、饰品(slot13)、法宝(slot14)因没有明确装备关系暂时不下发。'\n                '其他防具 appearance_properties 仍引用 appearance-layer-audit 人物图层候选。'",
    'generator metadata note',
)
generator_path.write_text(generator, encoding='utf-8')

# ---------------------------------------------------------------------------
# 4) Starter inventory：新角色也不再收到这三类旧本地装备。
# ---------------------------------------------------------------------------
starter_path = ROOT / 'data/catalog/starter_inventory.json'
starter = json.loads(starter_path.read_text(encoding='utf-8'))
blocked_starter_ids = set(unsupported_payload['starter_template_ids'])
starter['items'] = [
    row for row in starter['items']
    if int(row.get('template_id', 0)) not in blocked_starter_ids
]
starter_path.write_text(
    json.dumps(starter, ensure_ascii=False, separators=(',', ':')) + '\n',
    encoding='utf-8',
)

# ---------------------------------------------------------------------------
# 5) server：背包 1000；版本 3；加载旧角色时删除旧实例。
# ---------------------------------------------------------------------------
server_path = ROOT / 'server.py'
server = server_path.read_text(encoding='utf-8')
server = replace_once(
    server,
    "    default_item_registry,\n    deprecated_armor_template_ids,\n)",
    "    default_item_registry,\n    deprecated_armor_template_ids,\n    deprecated_unsupported_equipment_template_ids,\n)",
    'server import deprecated unsupported ids',
)
server = replace_once(
    server,
    'DEFAULT_BAG_CAPACITY = 320\nEQUIPMENT_RESOURCE_PREVIEW_VERSION = 2',
    'DEFAULT_BAG_CAPACITY = 1000\nEQUIPMENT_RESOURCE_PREVIEW_VERSION = 3',
    'server bag/version constants',
)
server = replace_once(
    server,
    "    \"\"\"Idempotently grant every APK equipment-resource preview item into the bag.\n\n    Preview items are compatibility constructs, not official equipment templates.\n    Existing items, equipped slots and appearance are left unchanged.\n    \"\"\"",
    "    \"\"\"Migrate deprecated local previews, then grant the supported APK preview set.\n\n    Preview items are compatibility constructs, not official equipment templates.\n    Unsupported local starter/preview templates are removed from old roles before\n    the current supported preview catalog is re-granted.\n    \"\"\"",
    'server preview migration docstring',
)
server = replace_once(
    server,
    "    items = role_items(role)\n    deprecated_armor = deprecated_armor_template_ids()\n    kept_items: list[dict[str, object]] = []\n    removed_legacy_armor = False\n    for item in items:\n        if not isinstance(item, dict):\n            continue\n        try:\n            template_id = int(item.get('template_id', 0))\n        except (TypeError, ValueError):\n            template_id = 0\n        if template_id in deprecated_armor:\n            removed_legacy_armor = True\n            continue\n        kept_items.append(item)\n    if removed_legacy_armor:\n        role['items'] = kept_items\n        items = role_items(role)\n        changed = True",
    "    items = role_items(role)\n    deprecated_templates = (\n        deprecated_armor_template_ids()\n        | deprecated_unsupported_equipment_template_ids()\n    )\n    kept_items: list[dict[str, object]] = []\n    removed_deprecated = False\n    for item in items:\n        if not isinstance(item, dict):\n            continue\n        try:\n            template_id = int(item.get('template_id', 0))\n        except (TypeError, ValueError):\n            template_id = 0\n        if template_id in deprecated_templates:\n            removed_deprecated = True\n            continue\n        kept_items.append(item)\n    if removed_deprecated:\n        role['items'] = kept_items\n        items = role_items(role)\n        changed = True",
    'server remove deprecated inventory instances',
)
server_path.write_text(server, encoding='utf-8')

# ---------------------------------------------------------------------------
# 6) 调整旧回归测试期望，并新增迁移测试。
# ---------------------------------------------------------------------------
test_registry_path = ROOT / 'tests/test_item_registry.py'
test_registry = test_registry_path.read_text(encoding='utf-8')
test_registry = test_registry.replace('self.assertEqual(len(items), 273)', 'self.assertEqual(len(items), 251)')
test_registry = test_registry.replace("self.assertEqual(len({int(item['template_id']) for item in items}), 273)", "self.assertEqual(len({int(item['template_id']) for item in items}), 251)")
test_registry = replace_once(
    test_registry,
    "        nonarmor_resources = [r for r in resources if int(r['equipment_slot']) != 3]\n        nonarmor_items = [i for i in items if int(i['equipment_slot']) != 3]\n        self.assertEqual(len(nonarmor_resources), 242)\n        self.assertEqual(len(nonarmor_items), 242)",
    "        nonarmor_resources = [\n            r for r in resources\n            if int(r['equipment_slot']) not in {3, 12, 13, 14}\n        ]\n        nonarmor_items = [i for i in items if int(i['equipment_slot']) != 3]\n        self.assertEqual(len(nonarmor_resources), 220)\n        self.assertEqual(len(nonarmor_items), 220)\n        self.assertTrue(all(int(i['equipment_slot']) not in {12, 13, 14} for i in items))",
    'test_item_registry unsupported preview expectations',
)
test_registry = test_registry.replace('self.assertEqual(len(preview_ids), 273)', 'self.assertEqual(len(preview_ids), 251)')
test_registry_path.write_text(test_registry, encoding='utf-8')

migration_test = ROOT / 'tests/test_inventory_cleanup_v3.py'
migration_test.write_text('''import json\nimport sys\nimport unittest\nfrom pathlib import Path\n\nsys.path.insert(0, str(Path(__file__).resolve().parents[1]))\n\nfrom item_registry import (\n    UNSUPPORTED_EQUIPMENT_FILE,\n    deprecated_unsupported_equipment_template_ids,\n    unsupported_equipment_slots,\n)\nfrom server import (\n    DEFAULT_BAG_CAPACITY,\n    RoleStore,\n    Settings,\n    default_role,\n)\n\n\nclass InventoryCleanupV3Tests(unittest.TestCase):\n    def test_bag_capacity_is_1000(self):\n        self.assertEqual(DEFAULT_BAG_CAPACITY, 1000)\n        settings = Settings()\n        role = default_role(settings)\n        self.assertEqual(role['bag_capacity'], 1000)\n\n    def test_catalog_disables_only_coat_accessory_talisman(self):\n        data = json.loads(UNSUPPORTED_EQUIPMENT_FILE.read_text(encoding='utf-8'))\n        self.assertEqual(unsupported_equipment_slots(), frozenset({12, 13, 14}))\n        self.assertEqual(data['disabled_slots'], [12, 13, 14])\n        self.assertEqual(len(data['deprecated_preview_template_ids']), 22)\n        self.assertEqual(len(deprecated_unsupported_equipment_template_ids()), 25)\n\n    def test_new_starter_inventory_does_not_grant_disabled_slots(self):\n        settings = Settings()\n        role = default_role(settings)\n        resolved_slots = {\n            int(settings.item_registry.resolve(item).get('equipment_slot', 0))\n            for item in role['items']\n        }\n        self.assertTrue({12, 13, 14}.isdisjoint(resolved_slots))\n\n    def test_old_saved_instances_are_removed_and_not_regranted(self):\n        settings = Settings()\n        role = default_role(settings)\n        role['bag_capacity'] = 320\n        role['equipment_resource_preview_version'] = 2\n        control = next(item for item in role['items'] if int(item.get('template_id', 0)) == 100_001_001)\n        old_ids = sorted(deprecated_unsupported_equipment_template_ids())\n        for offset, template_id in enumerate(old_ids, start=1):\n            role['items'].append({\n                'id': 9_000_000 + offset,\n                'template_id': template_id,\n                'quantity': 1,\n                'location': 'equipped' if offset % 2 else 'bag',\n            })\n        changed = RoleStore(settings)._ensure_items(role)\n        self.assertTrue(changed)\n        remaining = {int(item.get('template_id', 0)) for item in role['items']}\n        self.assertTrue(set(old_ids).isdisjoint(remaining))\n        self.assertIn(int(control['template_id']), remaining)\n        self.assertEqual(role['bag_capacity'], 1000)\n        self.assertEqual(role['equipment_resource_preview_version'], 3)\n\n    def test_generated_preview_catalog_has_no_disabled_slots(self):\n        root = Path(__file__).resolve().parents[1]\n        payload = json.loads(\n            (root / 'data/catalog/equipment_resource_preview_items.json').read_text(encoding='utf-8')\n        )\n        slots = {int(item['equipment_slot']) for item in payload['items']}\n        self.assertTrue({12, 13, 14}.isdisjoint(slots))\n        self.assertEqual(len(payload['items']), 251)\n\n\nif __name__ == '__main__':\n    unittest.main()\n''', encoding='utf-8')

print('inventory cleanup v3 patch prepared')
