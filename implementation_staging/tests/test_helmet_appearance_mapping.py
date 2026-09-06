import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from item_registry import (
    HELMET_APPEARANCE_MAPPING_FILE,
    helmet_icon_to_property20_mapping,
    helmet_property20_from_icon,
)


class HelmetAppearanceMappingTests(unittest.TestCase):
    def test_catalog_records_0102_as_only_visible_helmet(self):
        payload = json.loads(HELMET_APPEARANCE_MAPPING_FILE.read_text(encoding='utf-8'))
        self.assertEqual(payload['property'], 20)
        self.assertEqual(payload['image_base'], 21000)
        self.assertEqual(payload['candidate_property20_values'], [3])
        self.assertEqual(payload['candidate_image_ids'], [21003])
        self.assertEqual(payload['icon_to_property20'], {'102': 3})
        self.assertEqual(payload['no_appearance_icon_codes'], [100, 101, 103, 104, 105, 106, 107, 108, 109])
        self.assertEqual(payload['unresolved_icon_codes'], [])

    def test_runtime_reads_only_catalog_mapping(self):
        self.assertEqual(helmet_icon_to_property20_mapping(), {102: 3})
        self.assertEqual(helmet_property20_from_icon(102), 3)
        for icon_code in [100, 101, 103, 104, 105, 106, 107, 108, 109, 9999]:
            self.assertEqual(helmet_property20_from_icon(icon_code), 0, icon_code)

    def test_preview_catalog_applies_only_0102_helmet_layer(self):
        root = Path(__file__).resolve().parents[1]
        preview = json.loads((root / 'data/catalog/equipment_resource_preview_items.json').read_text(encoding='utf-8'))['items']
        helmets = {int(item['icon_code']): item['appearance_properties'] for item in preview if int(item.get('equipment_slot', 0)) == 1}
        self.assertEqual(sorted(helmets), list(range(100, 110)))
        self.assertEqual(helmets[102], {'20': 3})
        for icon_code in [100, 101, 103, 104, 105, 106, 107, 108, 109]:
            self.assertEqual(helmets[icon_code], {}, icon_code)


if __name__ == '__main__':
    unittest.main()
