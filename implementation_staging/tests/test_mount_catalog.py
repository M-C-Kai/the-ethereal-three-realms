"""Regression tests for the APK-derived riding catalogue."""

import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from item_registry import default_item_registry
from server import Settings, default_role, mount_update_frame
from protocol import decode_frame, field_values


CATALOG = Path(__file__).resolve().parents[1] / 'data' / 'catalog' / 'mount_appearance_mapping.json'


class MountCatalogTests(unittest.TestCase):
    def setUp(self):
        self.catalog = json.loads(CATALOG.read_text(encoding='utf-8'))
        self.registry = default_item_registry()

    def test_catalog_contains_54_unique_riding_appearances(self):
        image_ids = [
            int(image_id)
            for family in self.catalog['families']
            for image_id in family['image_ids']
        ]
        self.assertEqual(len(image_ids), 54)
        self.assertEqual(len(set(image_ids)), 54)

    def test_every_catalog_entry_has_matching_mount_item(self):
        named = self.catalog.get('named_templates', {})
        for family in self.catalog['families']:
            role_model = int(family['role_model'])
            for image_id in family['image_ids']:
                image_id = int(image_id)
                ride_code = image_id - 40000
                expected_role_model = 101000 + ((ride_code % 10000) // 1000) * 1000
                self.assertEqual(role_model, expected_role_model)
                if str(image_id) in named:
                    template_id = int(named[str(image_id)]['template_id'])
                else:
                    template_id = 170900000 + ride_code
                definition = self.registry.require(template_id)
                self.assertEqual(definition.kind, 'mount')
                self.assertEqual(definition.equipment_slot, 17)
                self.assertEqual(definition.mount_model, ride_code)

    def test_new_role_receives_all_54_mounts(self):
        role = default_role(Settings())
        mount_items = []
        for item in role['items']:
            definition = self.registry.resolve(item)
            if definition.get('kind') == 'mount':
                mount_items.append(definition)
        self.assertEqual(len(mount_items), 54)
        self.assertEqual(len({int(item['mount_model']) for item in mount_items}), 54)

    def test_mount_update_writes_ride_code_to_character_property_22(self):
        role = {'id': 10001, 'mount_model': 1004}
        message_id, payload = decode_frame(mount_update_frame(role))
        self.assertEqual(message_id, 1017)
        values = field_values(payload)
        self.assertEqual(values[0], 10001)
        self.assertEqual(values[1], 1)
        self.assertEqual(values[2], 22)
        self.assertEqual(values[3], 1004)


if __name__ == '__main__':
    unittest.main()
