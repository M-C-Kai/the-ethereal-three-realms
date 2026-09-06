"""Regression tests for the APK-derived riding catalogue."""

import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from item_registry import default_item_registry
from mount_protocol import (
    MOUNT_ATLAS_ACTION,
    MOUNT_MESSAGE_ID,
    is_mount_atlas_request,
    load_mount_atlas_entries,
    mount_atlas_frame,
)
from server import Settings, default_role, mount_update_frame
from protocol import TYPE_BYTE, byte, decode_frame, field_values


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

    def test_new_role_receives_no_mounts_by_default(self):
        role = default_role(Settings())
        mount_items = []
        for item in role['items']:
            definition = self.registry.resolve(item)
            if definition.get('kind') == 'mount':
                mount_items.append(definition)
        self.assertEqual(mount_items, [])
        self.assertEqual(int(role.get('mount_model', 0)), 0)

    def test_mount_update_writes_ride_code_to_character_property_22(self):
        role = {'id': 10001, 'mount_model': 1004}
        message_id, payload = decode_frame(mount_update_frame(role))
        self.assertEqual(message_id, 1017)
        values = field_values(payload)
        self.assertEqual(values[0], 10001)
        self.assertEqual(values[1], 1)
        self.assertEqual(values[2], 22)
        self.assertEqual(values[3], 1004)

    def test_mount_atlas_entries_are_generated_from_resource_catalog(self):
        entries = load_mount_atlas_entries(CATALOG)
        self.assertEqual(len(entries), 54)
        self.assertEqual(len({entry.ride_code for entry in entries}), 54)
        bixie = next(entry for entry in entries if entry.ride_code == 1004)
        self.assertEqual(bixie.catalog_id, 1004)
        self.assertEqual(bixie.name, '辟邪')
        self.assertEqual(bixie.mount_type, 0)

    def test_mount_atlas_request_requires_byte_action_30(self):
        self.assertTrue(is_mount_atlas_request([byte(MOUNT_ATLAS_ACTION)]))
        self.assertFalse(is_mount_atlas_request([]))

    def test_mount_atlas_frame_uses_protocol_1024_action_30(self):
        entries = load_mount_atlas_entries(CATALOG)
        message_id, payload = decode_frame(mount_atlas_frame(entries))
        self.assertEqual(message_id, MOUNT_MESSAGE_ID)
        values = field_values(payload)
        self.assertEqual(values[0], MOUNT_ATLAS_ACTION)
        self.assertEqual(values[1], 54)
        # First record: catalog_id, name, ride_code, mount_type.
        self.assertEqual(values[2], entries[0].catalog_id)
        self.assertEqual(values[3], entries[0].name)
        self.assertEqual(values[4], entries[0].ride_code)
        self.assertEqual(values[5], entries[0].mount_type)


if __name__ == '__main__':
    unittest.main()
