import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from item_registry import ARMOR_APPEARANCE_MAPPING_FILE, armor_icon_to_property2_mapping

ROOT = Path(__file__).resolve().parents[1]


class ArmorIconAlignmentTests(unittest.TestCase):
    def expected(self):
        result = {}
        for offset, base in enumerate((300, 1200, 1300)):
            for frame in range(10):
                result[base + frame] = offset * 10 + frame + 1
        return result

    def test_30_item_icons_align_to_property2_1_through_30(self):
        self.assertEqual(armor_icon_to_property2_mapping(), self.expected())

    def test_groups_3_12_13_are_catalogued_as_armor_icons(self):
        payload = json.loads((ROOT / 'data/catalog/apk_equipment_resources.json').read_text(encoding='utf-8'))
        rows = [row for row in payload['resources'] if int(row['icon_code']) in self.expected()]
        self.assertEqual(len(rows), 30)
        self.assertTrue(all(int(row['equipment_slot']) == 3 for row in rows))
        self.assertTrue(all(row['slot_family'] == 'armor' for row in rows))

    def test_preview_uses_distinct_real_icons_and_never_grants_14000(self):
        payload = json.loads((ROOT / 'data/catalog/equipment_resource_preview_items.json').read_text(encoding='utf-8'))
        armor = [row for row in payload['items'] if int(row['equipment_slot']) == 3]
        self.assertEqual(len(armor), 30)
        actual = {int(row['icon_code']): int(row['appearance_properties']['2']) for row in armor}
        self.assertEqual(actual, self.expected())
        self.assertNotIn(0, {int(row['appearance_properties']['2']) for row in armor})
        self.assertNotIn(30_140_001, {int(row['template_id']) for row in armor})

    def test_catalog_marks_14000_as_base_not_equipment_preview(self):
        data = json.loads(ARMOR_APPEARANCE_MAPPING_FILE.read_text(encoding='utf-8'))
        self.assertEqual(data['property2_to_image']['0'], 14000)
        self.assertNotIn('0', data['resource_preview']['property2_to_icon_code'])
        self.assertNotIn('30140001', data['resource_preview']['template_to_property2'])
        self.assertIn(30_140_001, {int(v) for v in data['deprecated_template_ids']})


if __name__ == '__main__':
    unittest.main()
