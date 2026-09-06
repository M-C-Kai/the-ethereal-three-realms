import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from item_registry import (
    UNSUPPORTED_EQUIPMENT_FILE,
    deprecated_unsupported_equipment_template_ids,
    unsupported_equipment_slots,
)
from server import (
    DEFAULT_BAG_CAPACITY,
    RoleStore,
    Settings,
    default_role,
)


class InventoryCleanupV3Tests(unittest.TestCase):
    def test_bag_capacity_is_1000(self):
        self.assertEqual(DEFAULT_BAG_CAPACITY, 1000)
        settings = Settings()
        role = default_role(settings)
        self.assertEqual(role['bag_capacity'], 1000)

    def test_catalog_disables_only_coat_accessory_talisman(self):
        data = json.loads(UNSUPPORTED_EQUIPMENT_FILE.read_text(encoding='utf-8'))
        self.assertEqual(unsupported_equipment_slots(), frozenset({12, 13, 14}))
        self.assertEqual(data['disabled_slots'], [12, 13, 14])
        self.assertEqual(len(data['deprecated_preview_template_ids']), 22)
        self.assertEqual(len(deprecated_unsupported_equipment_template_ids()), 25)

    def test_new_starter_inventory_does_not_grant_disabled_slots(self):
        settings = Settings()
        role = default_role(settings)
        resolved_slots = {
            int(settings.item_registry.resolve(item).get('equipment_slot', 0))
            for item in role['items']
        }
        self.assertTrue({12, 13, 14}.isdisjoint(resolved_slots))

    def test_old_saved_instances_are_removed_and_not_regranted(self):
        settings = Settings()
        role = default_role(settings)
        role['bag_capacity'] = 320
        role['equipment_resource_preview_version'] = 2
        control = next(item for item in role['items'] if int(item.get('template_id', 0)) == 100_001_001)
        old_ids = sorted(deprecated_unsupported_equipment_template_ids())
        for offset, template_id in enumerate(old_ids, start=1):
            role['items'].append({
                'id': 9_000_000 + offset,
                'template_id': template_id,
                'quantity': 1,
                'location': 'equipped' if offset % 2 else 'bag',
            })
        changed = RoleStore(settings)._ensure_items(role)
        self.assertTrue(changed)
        remaining = {int(item.get('template_id', 0)) for item in role['items']}
        self.assertTrue(set(old_ids).isdisjoint(remaining))
        self.assertIn(int(control['template_id']), remaining)
        self.assertEqual(role['bag_capacity'], 1000)
        self.assertEqual(role['equipment_resource_preview_version'], 3)

    def test_generated_preview_catalog_has_no_disabled_slots(self):
        root = Path(__file__).resolve().parents[1]
        payload = json.loads(
            (root / 'data/catalog/equipment_resource_preview_items.json').read_text(encoding='utf-8')
        )
        slots = {int(item['equipment_slot']) for item in payload['items']}
        self.assertTrue({12, 13, 14}.isdisjoint(slots))
        self.assertEqual(len(payload['items']), 251)


if __name__ == '__main__':
    unittest.main()
