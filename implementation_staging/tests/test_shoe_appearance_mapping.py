import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MAPPING_FILE = ROOT / 'data' / 'catalog' / 'shoe_appearance_mapping.json'
ITEMS_FILE = ROOT / 'data' / 'catalog' / 'items.json'

EXPECTED_MAPPING = {
    '900': 20,
    '901': 2,
    '902': 6,
    '903': 2,
    '904': 46,
    '905': 2,
    '906': 10,
    '907': 38,
    '908': 31,
    '909': 40,
}


class ShoeAppearanceMappingTests(unittest.TestCase):
    def test_catalog_records_confirmed_apk_visual_mapping(self):
        payload = json.loads(MAPPING_FILE.read_text(encoding='utf-8'))
        self.assertEqual(payload['version'], 1)
        self.assertEqual(payload['kind'], 'shoe_appearance_mapping')
        self.assertEqual(payload['property'], 18)
        self.assertEqual(payload['image_base'], 19000)
        self.assertEqual(payload['character_layer'], 8)
        self.assertEqual(payload['icon_resource']['image_id'], 3092424)
        self.assertEqual(payload['icon_to_property18'], EXPECTED_MAPPING)
        self.assertEqual(payload['unresolved_icon_codes'], [])

    def test_catalog_image_ids_follow_property18_rule(self):
        payload = json.loads(MAPPING_FILE.read_text(encoding='utf-8'))
        recovered = payload['recovered_mappings']
        by_icon = {str(row['icon_code']): row for row in recovered}
        self.assertEqual(set(by_icon), set(EXPECTED_MAPPING))
        for icon_code, property18 in EXPECTED_MAPPING.items():
            self.assertGreater(property18, 0)
            self.assertEqual(by_icon[icon_code]['property18'], property18)
            self.assertEqual(by_icon[icon_code]['image_id'], 19000 + property18)

    def test_qingwen_boots_uses_0907_property18_38(self):
        items = json.loads(ITEMS_FILE.read_text(encoding='utf-8'))['items']
        item = next(row for row in items if int(row['template_id']) == 90001001)
        self.assertEqual(int(item['icon_code']), 907)
        self.assertEqual(item['appearance_properties'], {'18': 38})


if __name__ == '__main__':
    unittest.main()
