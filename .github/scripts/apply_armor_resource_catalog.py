from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STAGING = ROOT / 'implementation_staging'
CATALOG = STAGING / 'data' / 'catalog'

# 1) APK-confirmed armor resource family: property2 -> image 14000..14030.
resources = [
    {
        'property2': value,
        'image_id': 14000 + value,
        'file': f'{14000 + value:07d}_71x32.png',
        'width': 71,
        'height': 32,
    }
    for value in range(31)
]
armor_mapping = {
    'version': 1,
    'kind': 'armor_appearance_mapping',
    'status': 'apk_resource_family_confirmed_icon_mapping_unresolved',
    'source': 'direct APK resource extraction + pmsj/work/b/v.smali',
    'description': (
        '铠甲人物外观只使用 property2。客户端将 property2 写入人物 layer3，'
        '实际资源为 image_id=14000+property2。APK 内 14000..14030 共 31 张，'
        '全部为 71x32。当前未恢复 icon_code 0300..0309 到 property2 的官方对应表，'
        '因此程序不得循环、按尾号或按颜色自动猜测。'
    ),
    'property': 2,
    'image_slot': 3,
    'image_base': 14000,
    'property_range': [0, 30],
    'image_range': [14000, 14030],
    'dimensions': [71, 32],
    'resources': resources,
    'property2_to_image': {str(value): 14000 + value for value in range(31)},
    'armor_icon_codes': list(range(300, 310)),
    'icon_to_property2': {},
    'unresolved_icon_codes': list(range(300, 310)),
    'notes': [
        '0014000_71x32.png through 0014030_71x32.png are the APK armor appearance resource family.',
        'v.r() routes property 2 to the character armor/body layer handler.',
        'The handler writes image 14000 + property2 into character layer 3.',
        'property2 value 0 is valid and selects image 14000; unresolved must therefore be represented as null/None, not 0.',
        'No icon_code -> property2 pair is stored until supported by original-server evidence or a confirmed visual match.',
    ],
}
(CATALOG / 'armor_appearance_mapping.json').write_text(
    json.dumps(armor_mapping, ensure_ascii=False, indent=2) + '\n', encoding='utf-8'
)

# 2) Program reads armor catalog; remove wrong slot3 -> property15 preview rule.
registry_path = STAGING / 'item_registry.py'
text = registry_path.read_text(encoding='utf-8')

constant_anchor = "HELMET_APPEARANCE_MAPPING_FILE = (\n    Path(__file__).resolve().parent / 'data' / 'catalog' / 'helmet_appearance_mapping.json'\n)\n"
if 'ARMOR_APPEARANCE_MAPPING_FILE' not in text:
    assert constant_anchor in text
    text = text.replace(
        constant_anchor,
        constant_anchor + "ARMOR_APPEARANCE_MAPPING_FILE = (\n    Path(__file__).resolve().parent / 'data' / 'catalog' / 'armor_appearance_mapping.json'\n)\n",
        1,
    )

helmet_anchor = "def helmet_property20_from_icon(icon_code: int) -> int:\n    \"\"\"Resolve helmet property20 from the catalog; unresolved icons are not guessed.\"\"\"\n    return _helmet_icon_to_property20_mapping().get(int(icon_code), 0)\n\n\n"
if 'def armor_property2_from_icon' not in text:
    assert helmet_anchor in text
    armor_loader = '''@lru_cache(maxsize=1)\ndef _armor_appearance_catalog() -> tuple[dict[int, int], dict[int, int]]:\n    \"\"\"Load APK-confirmed armor resources and explicit icon mappings from catalog.\"\"\"\n    data = json.loads(ARMOR_APPEARANCE_MAPPING_FILE.read_text(encoding='utf-8'))\n    if not isinstance(data, dict) or int(data.get('version', 0)) != 1:\n        raise ValueError(f'invalid armor appearance mapping catalog: {ARMOR_APPEARANCE_MAPPING_FILE}')\n    if int(data.get('property', -1)) != 2 or int(data.get('image_base', 0)) != 14000:\n        raise ValueError(f'invalid armor appearance property metadata: {ARMOR_APPEARANCE_MAPPING_FILE}')\n\n    raw_resources = data.get('property2_to_image')\n    if not isinstance(raw_resources, dict) or len(raw_resources) != 31:\n        raise ValueError(f'armor property2 resource table must contain 31 entries: {ARMOR_APPEARANCE_MAPPING_FILE}')\n    property_to_image: dict[int, int] = {}\n    for raw_property, raw_image in raw_resources.items():\n        property_value = int(raw_property)\n        image_id = int(raw_image)\n        if not 0 <= property_value <= 30 or image_id != 14000 + property_value:\n            raise ValueError(f'invalid armor property2 resource {raw_property!r}->{raw_image!r}')\n        property_to_image[property_value] = image_id\n    if set(property_to_image) != set(range(31)):\n        raise ValueError(f'armor property2 resource range is incomplete: {ARMOR_APPEARANCE_MAPPING_FILE}')\n\n    raw_mapping = data.get('icon_to_property2')\n    if not isinstance(raw_mapping, dict):\n        raise ValueError(f'armor icon mapping must be a dict: {ARMOR_APPEARANCE_MAPPING_FILE}')\n    icon_mapping: dict[int, int] = {}\n    for raw_icon, raw_value in raw_mapping.items():\n        icon_code = int(raw_icon)\n        property_value = int(raw_value)\n        if icon_code <= 0 or property_value not in property_to_image:\n            raise ValueError(f'invalid armor appearance pair {raw_icon!r}->{raw_value!r}')\n        if icon_code in icon_mapping:\n            raise ValueError(f'duplicate armor icon_code after normalization: {icon_code}')\n        icon_mapping[icon_code] = property_value\n    return property_to_image, icon_mapping\n\n\ndef armor_property2_to_image_mapping() -> dict[int, int]:\n    \"\"\"Return APK-confirmed property2 -> armor image mapping (14000..14030).\"\"\"\n    return dict(_armor_appearance_catalog()[0])\n\n\ndef armor_icon_to_property2_mapping() -> dict[int, int]:\n    \"\"\"Return only explicitly confirmed icon_code -> property2 armor pairs.\"\"\"\n    return dict(_armor_appearance_catalog()[1])\n\n\ndef armor_property2_from_icon(icon_code: int) -> int | None:\n    \"\"\"Resolve armor property2 from catalog; unresolved icons return None, never guessed.\"\"\"\n    return _armor_appearance_catalog()[1].get(int(icon_code))\n\n\n'''
    text = text.replace(helmet_anchor, helmet_anchor + armor_loader, 1)

text = text.replace('    3: 15,\n', '')

slot1_anchor = "    if slot == 1:\n        value = helmet_property20_from_icon(icon_code)\n        return {'20': value} if value > 0 else {}\n"
if "if slot == 3:\n        value = armor_property2_from_icon(icon_code)" not in text:
    assert slot1_anchor in text
    text = text.replace(
        slot1_anchor,
        slot1_anchor + "    if slot == 3:\n        value = armor_property2_from_icon(icon_code)\n        return {'2': value} if value is not None else {}\n",
        1,
    )
registry_path.write_text(text, encoding='utf-8')

# 3) Remove the previously wrong property15 from real slot-3 item templates.
items_path = CATALOG / 'items.json'
items_payload = json.loads(items_path.read_text(encoding='utf-8'))
changed_items = []
for item in items_payload['items']:
    if int(item.get('equipment_slot', 0)) != 3:
        continue
    appearance = item.get('appearance_properties')
    if isinstance(appearance, dict) and '15' in appearance:
        removed = appearance.pop('15')
        changed_items.append((int(item['template_id']), int(item.get('icon_code', 0)), removed))
        if not appearance:
            item.pop('appearance_properties', None)
items_path.write_text(json.dumps(items_payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('removed wrong armor property15:', changed_items)

# 4) Document the corrected APK rule in the protocol lock.
lock_path = STAGING / 'PROTOCOL_LOCK.md'
lock_text = lock_path.read_text(encoding='utf-8')
marker = '## 铠甲外观资源（property 2 / 14000）'
if marker not in lock_text:
    lock_text += '''\n\n## 铠甲外观资源（property 2 / 14000）\n\nAPK 与 `pmsj/work/b/v.smali` 已确认：\n\n- 铠甲主体外观使用人物 `property 2`，不是 `property 15`。\n- `property 2` 写入人物复合模型的 image slot/layer 3。\n- 资源编号固定为 `14000 + property2`。\n- 当前 APK 包内连续存在 `0014000_71x32.png` 到 `0014030_71x32.png`，即 `property2=0..30` 共 31 个铠甲外观资源。\n- `property2=0` 是有效值，对应 `image 14000`，不能拿 0 表示“未解析”。\n- 当前尚未恢复 `icon_code 0300..0309 -> property2` 的官方表；没有证据时不得循环候选、按尾号、按颜色或跨 `15000/16000/...` 资源族猜测。\n- 服务器资料库以 `data/catalog/armor_appearance_mapping.json` 为唯一铠甲外观资源来源；程序只读取该表。\n'''
    lock_path.write_text(lock_text, encoding='utf-8')

# 5) Add regression tests locking down the resource family and no-guess behavior.
test_path = STAGING / 'tests' / 'test_armor_appearance_mapping.py'
test_path.write_text('''import json\nimport sys\nimport unittest\nfrom pathlib import Path\n\nsys.path.insert(0, str(Path(__file__).resolve().parents[1]))\n\nfrom item_registry import (\n    ARMOR_APPEARANCE_MAPPING_FILE,\n    armor_icon_to_property2_mapping,\n    armor_property2_from_icon,\n    armor_property2_to_image_mapping,\n    preview_appearance_properties,\n)\n\n\nclass ArmorAppearanceMappingTests(unittest.TestCase):\n    def test_apk_armor_resource_family_is_exact_14000_to_14030(self):\n        data = json.loads(ARMOR_APPEARANCE_MAPPING_FILE.read_text(encoding='utf-8'))\n        self.assertEqual(data['property'], 2)\n        self.assertEqual(data['image_slot'], 3)\n        self.assertEqual(data['image_base'], 14000)\n        self.assertEqual(data['property_range'], [0, 30])\n        self.assertEqual(data['image_range'], [14000, 14030])\n        self.assertEqual(data['dimensions'], [71, 32])\n        self.assertEqual(len(data['resources']), 31)\n        self.assertEqual(\n            [(row['property2'], row['image_id']) for row in data['resources']],\n            [(value, 14000 + value) for value in range(31)],\n        )\n        self.assertTrue(all(row['file'] == f\"{row['image_id']:07d}_71x32.png\" for row in data['resources']))\n\n    def test_runtime_reads_property2_resource_table_from_catalog(self):\n        self.assertEqual(\n            armor_property2_to_image_mapping(),\n            {value: 14000 + value for value in range(31)},\n        )\n\n    def test_icon_mapping_is_unresolved_and_not_guessed(self):\n        self.assertEqual(armor_icon_to_property2_mapping(), {})\n        for icon_code in range(300, 310):\n            self.assertIsNone(armor_property2_from_icon(icon_code), icon_code)\n            self.assertEqual(\n                preview_appearance_properties(3, icon_code - 300, {}, icon_code=icon_code),\n                {},\n            )\n\n    def test_real_and_preview_armor_no_longer_use_property15(self):\n        root = Path(__file__).resolve().parents[1]\n        for relative in ('data/catalog/items.json', 'data/catalog/equipment_resource_preview_items.json'):\n            payload = json.loads((root / relative).read_text(encoding='utf-8'))\n            armor = [item for item in payload['items'] if int(item.get('equipment_slot', 0)) == 3]\n            self.assertTrue(armor, relative)\n            for item in armor:\n                appearance = item.get('appearance_properties', {})\n                self.assertNotIn('15', appearance, (relative, item.get('icon_code')))\n\n\nif __name__ == '__main__':\n    unittest.main()\n''', encoding='utf-8')
