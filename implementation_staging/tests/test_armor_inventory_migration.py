import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from item_registry import armor_resource_preview_template_mapping, deprecated_armor_template_ids
from server import EQUIPMENT_RESOURCE_PREVIEW_VERSION, RoleStore, Settings, default_role


class ArmorInventoryMigrationTests(unittest.TestCase):
    def test_old_armor_instances_are_deleted_and_30_equippable_armors_reissued(self):
        settings = Settings()
        role = default_role(settings)
        new_ids = set(armor_resource_preview_template_mapping())
        deprecated = set(deprecated_armor_template_ids())

        role['items'] = [
            item for item in role['items']
            if int(item.get('template_id', 0)) not in new_ids
        ]
        for index, template_id in enumerate(sorted(deprecated), start=1):
            role['items'].append({
                'id': 900_000 + index,
                'template_id': template_id,
                'quantity': 1,
                'location': 'equipped' if index == 1 else 'bag',
            })
        role['equipment_resource_preview_version'] = 1

        changed = RoleStore(settings)._ensure_items(role)
        self.assertTrue(changed)
        template_ids = [int(item.get('template_id', 0)) for item in role['items']]
        self.assertTrue(deprecated.isdisjoint(template_ids))
        self.assertEqual(set(template_ids) & new_ids, new_ids)
        self.assertEqual(len([tid for tid in template_ids if tid in new_ids]), 30)
        self.assertEqual(role['equipment_resource_preview_version'], EQUIPMENT_RESOURCE_PREVIEW_VERSION)

    def test_legacy_starter_armor_is_not_regranted(self):
        settings = Settings()
        role = default_role(settings)
        self.assertNotIn(30_001_001, {int(item.get('template_id', 0)) for item in role['items']})


if __name__ == '__main__':
    unittest.main()
