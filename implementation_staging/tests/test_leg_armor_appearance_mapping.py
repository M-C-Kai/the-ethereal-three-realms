import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MAPPING_FILE = ROOT / 'data' / 'catalog' / 'leg_armor_appearance_mapping.json'
ITEMS_FILE = ROOT / 'data' / 'catalog' / 'items.json'

EXPECTED_MAPPING = {
    '500': 0,
    '501': 25,
    '502': 27,
    '503': 3,
    '504': 4,
    '505': 5,
    '506': 2,
    '507': 7,
    '508': 8,
    '509': 9,
}


class LegArmorAppearanceMappingTests(unittest.TestCase):
    def test_catalog_records_confirmed_apk_visual_mapping(self):
        payload = json.loads(MAPPING_FILE.read_text(encoding='utf-8'))
        self.assertEqual(payload['version'], 1)
        self.assertEqual(payload['kind'], 'leg_armor_appearance_mapping')
        self.assertEqual(payload['property'], 14)
        self.assertEqual(payload['image_base'], 15000)
        self.assertEqual(payload['icon_resource']['image_id'], 3052424)
        self.assertEqual(payload['icon_to_property14'], EXPECTED_MAPPING)
        self.assertEqual(payload['unresolved_icon_codes'], [])

    def test_catalog_image_ids_follow_property14_rule(self):
        payload = json.loads(MAPPING_FILE.read_text(encoding='utf-8'))
        recovered = payload['recovered_mappings']
        by_icon = {str(row['icon_code']): row for row in recovered}
        self.assertEqual(set(by_icon), set(EXPECTED_MAPPING))
        for icon_code, property14 in EXPECTED_MAPPING.items():
            self.assertEqual(by_icon[icon_code]['property14'], property14)
            self.assertEqual(by_icon[icon_code]['image_id'], 15000 + property14)

    def test_qingwen_leg_armor_uses_0505_property14_5(self):
        items = json.loads(ITEMS_FILE.read_text(encoding='utf-8'))['items']
        item = next(row for row in items if int(row['template_id']) == 50001001)
        self.assertEqual(int(item['icon_code']), 505)
        self.assertEqual(item['appearance_properties'], {'14': 5})


if __name__ == '__main__':
    unittest.main()
