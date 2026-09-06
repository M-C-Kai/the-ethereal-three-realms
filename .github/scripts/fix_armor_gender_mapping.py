from __future__ import annotations

import json
from pathlib import Path

ROOT = Path('implementation_staging')
CATALOG = ROOT / 'data/catalog/armor_appearance_mapping.json'
TEST = ROOT / 'tests/test_armor_appearance_mapping.py'
GENERATOR = ROOT / 'tools/build_equipment_resource_preview_items.py'


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{label}: expected 1 match, got {count}')
    return text.replace(old, new, 1)


# 1) 资料库：3122424 是男装，3132424 是女装。
data = json.loads(CATALOG.read_text(encoding='utf-8'))

data['status'] = 'apk_resource_family_and_gendered_item_icons_aligned'
data['source'] = 'direct APK resource extraction + pmsj/work/b/v.smali + user-confirmed atlas gender'
data['description'] = (
    '铠甲人物主体使用 property2：image_id=14000+property2。14000/property2=0 是默认身体资源；'
    '0300..0309 对应 property2 1..10；APK 物品图标图 3122424（1200..1209）经用户确认是男装，'
    '对应 property2 21..30；3132424（1300..1309）是女装，对应 property2 11..20。'
)

icon_to_property2: dict[str, int] = {}
for frame in range(10):
    icon_to_property2[str(300 + frame)] = 1 + frame
    # 男装图标组 3122424 / 1200..1209 对应男装主体 14021..14030。
    icon_to_property2[str(1200 + frame)] = 21 + frame
    # 女装图标组 3132424 / 1300..1309 对应女装主体 14011..14020。
    icon_to_property2[str(1300 + frame)] = 11 + frame

data['icon_to_property2'] = icon_to_property2

data['gendered_icon_groups'] = [
    {
        'atlas_image_id': 3122424,
        'resource_group': 12,
        'icon_range': [1200, 1209],
        'gender': 'male',
        'property2_range': [21, 30],
        'image_range': [14021, 14030],
        'evidence': 'user_confirmed_from_original_game_item_art',
    },
    {
        'atlas_image_id': 3132424,
        'resource_group': 13,
        'icon_range': [1300, 1309],
        'gender': 'female',
        'property2_range': [11, 20],
        'image_range': [14011, 14020],
        'evidence': 'user_confirmed_from_original_game_item_art',
    },
]

preview = data['resource_preview']
property2_to_icon: dict[str, int] = {}
for frame in range(10):
    property2_to_icon[str(1 + frame)] = 300 + frame
    property2_to_icon[str(11 + frame)] = 1300 + frame
    property2_to_icon[str(21 + frame)] = 1200 + frame
preview['property2_to_icon_code'] = property2_to_icon
preview['description'] = (
    'Compatibility preview equipment for the 30 equippable APK armor bodies 14001..14030. '
    '0300..0309 stay paired to 14001..14010; 3132424 female icons 1300..1309 pair to 14011..14020; '
    '3122424 male icons 1200..1209 pair to 14021..14030. 14000/property2=0 is the default body.'
)

data['notes'] = [
    '0014000_71x32.png through 0014030_71x32.png are the APK armor/body resource family.',
    'property2=0 selects image14000 and is kept as the default body/no-equipped-armor resource.',
    '0300..0309 remain paired to property2 1..10.',
    '3122424 is the male armor item atlas: icon 1200..1209 -> property2 21..30 -> image 14021..14030.',
    '3132424 is the female armor item atlas: icon 1300..1309 -> property2 11..20 -> image 14011..14020.',
    'The previous 12xx->11..20 / 13xx->21..30 pairing was gender-reversed and is deprecated.',
    'Legacy property2=0 armor preview and old slot-3 icon-only previews remain deprecated.',
]

CATALOG.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

# 2) 生成器说明同步，具体 icon_code 从资料库反向表读取。
generator = GENERATOR.read_text(encoding='utf-8')
generator = replace_once(
    generator,
    "'铠甲下发30件：0300..0309→14001..14010、1200..1209→14011..14020、1300..1309→14021..14030；14000是默认身体不作为装备下发。'",
    "'铠甲下发30件：0300..0309→14001..14010；女装3132424/1300..1309→14011..14020；男装3122424/1200..1209→14021..14030；14000是默认身体不作为装备下发。'",
    'generator armor note',
)
GENERATOR.write_text(generator, encoding='utf-8')

# 3) 回归：锁定男女图标组，防止再次调反。
test = TEST.read_text(encoding='utf-8')
old = """    def test_icon_mapping_covers_30_equippable_armors(self):
        expected = {}
        for offset, base in enumerate((300, 1200, 1300)):
            for frame in range(10):
                expected[base + frame] = offset * 10 + frame + 1
        self.assertEqual(armor_icon_to_property2_mapping(), expected)
        for icon_code, property2 in expected.items():
            self.assertEqual(armor_property2_from_icon(icon_code), property2)
            self.assertEqual(
                preview_appearance_properties(3, 0, {}, icon_code=icon_code),
                {'2': property2},
            )
"""
new = """    def test_icon_mapping_covers_30_equippable_armors_with_correct_gender_groups(self):
        expected = {}
        for frame in range(10):
            expected[300 + frame] = 1 + frame
            expected[1300 + frame] = 11 + frame  # 3132424 女装
            expected[1200 + frame] = 21 + frame  # 3122424 男装
        self.assertEqual(armor_icon_to_property2_mapping(), expected)
        for icon_code, property2 in expected.items():
            self.assertEqual(armor_property2_from_icon(icon_code), property2)
            self.assertEqual(
                preview_appearance_properties(3, 0, {}, icon_code=icon_code),
                {'2': property2},
            )

    def test_gendered_icon_atlases_are_not_reversed(self):
        data = json.loads(ARMOR_APPEARANCE_MAPPING_FILE.read_text(encoding='utf-8'))
        groups = {int(row['atlas_image_id']): row for row in data['gendered_icon_groups']}
        self.assertEqual(groups[3122424]['gender'], 'male')
        self.assertEqual(groups[3122424]['icon_range'], [1200, 1209])
        self.assertEqual(groups[3122424]['property2_range'], [21, 30])
        self.assertEqual(groups[3132424]['gender'], 'female')
        self.assertEqual(groups[3132424]['icon_range'], [1300, 1309])
        self.assertEqual(groups[3132424]['property2_range'], [11, 20])
"""
test = replace_once(test, old, new, 'gender mapping test')
TEST.write_text(test, encoding='utf-8')

print('armor gender mapping correction prepared')
