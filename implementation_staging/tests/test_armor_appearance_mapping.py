import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from item_registry import (
    ARMOR_APPEARANCE_MAPPING_FILE,
    armor_icon_to_property2_mapping,
    armor_property2_from_equipment,
    armor_property2_from_icon,
    armor_property2_to_image_mapping,
    armor_resource_preview_template_mapping,
    deprecated_armor_template_ids,
    preview_appearance_properties,
)


class ArmorAppearanceMappingTests(unittest.TestCase):
    def test_apk_armor_resource_family_is_exact_14000_to_14030(self):
        data = json.loads(ARMOR_APPEARANCE_MAPPING_FILE.read_text(encoding='utf-8'))
        self.assertEqual(data['property'], 2)
        self.assertEqual(data['image_slot'], 3)
        self.assertEqual(data['image_base'], 14000)
        self.assertEqual(data['property_range'], [0, 30])
        self.assertEqual(data['image_range'], [14000, 14030])
        self.assertEqual(data['dimensions'], [71, 32])
        self.assertEqual(len(data['resources']), 31)
        self.assertEqual(
            [(row['property2'], row['image_id']) for row in data['resources']],
            [(value, 14000 + value) for value in range(31)],
        )

    def test_runtime_reads_property2_resource_table_from_catalog(self):
        self.assertEqual(
            armor_property2_to_image_mapping(),
            {value: 14000 + value for value in range(31)},
        )

    def test_icon_mapping_covers_30_equippable_armors_with_correct_gender_groups(self):
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

    def test_resource_preview_templates_cover_30_equippable_armors(self):
        mapping = armor_resource_preview_template_mapping()
        self.assertEqual(len(mapping), 30)
        self.assertEqual(set(mapping.values()), set(range(1, 31)))
        for template_id, property2 in mapping.items():
            self.assertEqual(template_id, 30_000_000 + (14_000 + property2) * 10 + 1)
            self.assertEqual(armor_property2_from_equipment(template_id, 0), property2)

    def test_default_body_preview_is_deprecated(self):
        self.assertIn(30_140_001, deprecated_armor_template_ids())

    def test_real_and_preview_armor_never_use_property15(self):
        root = Path(__file__).resolve().parents[1]
        for relative in ('data/catalog/items.json', 'data/catalog/equipment_resource_preview_items.json'):
            payload = json.loads((root / relative).read_text(encoding='utf-8'))
            armor = [item for item in payload['items'] if int(item.get('equipment_slot', 0)) == 3]
            for item in armor:
                self.assertNotIn('15', item.get('appearance_properties', {}))


if __name__ == '__main__':
    unittest.main()
