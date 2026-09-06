import tempfile
import unittest
from pathlib import Path

from server import (
    ROLE_BAG_PREVIEW_SUPPRESSION_VERSION,
    ROLE_BAG_RESET_VERSION,
    RoleStore,
    Settings,
    clear_role_bag_once,
    default_role,
    ensure_equipment_resource_preview_items,
    role_items,
)


class RoleBagResetTests(unittest.TestCase):
    def test_clear_role_bag_once_removes_only_bag_items(self):
        role = {
            'id': 10001,
            'items': [
                {'id': 1, 'template_id': 101, 'location': 'bag'},
                {'id': 2, 'template_id': 102, 'location': 'equipped'},
            ],
        }
        self.assertTrue(clear_role_bag_once(role))
        self.assertEqual(
            [(item['id'], item['location']) for item in role_items(role)],
            [(2, 'equipped')],
        )
        self.assertEqual(role['bag_reset_version'], ROLE_BAG_RESET_VERSION)
        self.assertEqual(
            role['bag_preview_suppression_version'],
            ROLE_BAG_PREVIEW_SUPPRESSION_VERSION,
        )

    def test_reset_is_one_time_and_does_not_delete_future_items(self):
        role = {
            'id': 10001,
            'items': [{'id': 1, 'template_id': 101, 'location': 'bag'}],
        }
        self.assertTrue(clear_role_bag_once(role))
        role_items(role).append({'id': 3, 'template_id': 103, 'location': 'bag'})
        self.assertFalse(clear_role_bag_once(role))
        self.assertEqual([item['id'] for item in role_items(role)], [3])

    def test_preview_catalog_does_not_refill_after_real_reset(self):
        settings = Settings()
        role = default_role(settings)
        role.pop('bag_reset_version', None)
        role.pop('bag_preview_suppression_version', None)
        self.assertTrue(any(item.get('location') == 'bag' for item in role_items(role)))
        self.assertTrue(clear_role_bag_once(role))
        self.assertFalse(any(item.get('location') == 'bag' for item in role_items(role)))
        ensure_equipment_resource_preview_items(role, settings.item_registry)
        self.assertFalse(any(item.get('location') == 'bag' for item in role_items(role)))

    def test_new_role_reset_marker_does_not_disable_preview_repair(self):
        settings = Settings()
        role = default_role(settings)
        self.assertEqual(role['bag_reset_version'], ROLE_BAG_RESET_VERSION)
        self.assertNotIn('bag_preview_suppression_version', role)
        preview_id = next(iter(settings.item_registry.preview_template_ids()))
        role['items'] = [
            item for item in role_items(role)
            if int(item.get('template_id', 0)) != int(preview_id)
        ]
        self.assertNotIn(preview_id, {int(item.get('template_id', 0)) for item in role_items(role)})
        self.assertTrue(ensure_equipment_resource_preview_items(role, settings.item_registry))
        self.assertIn(preview_id, {int(item.get('template_id', 0)) for item in role_items(role)})

    def test_roles_for_migrates_legacy_role_but_keeps_equipped(self):
        with tempfile.TemporaryDirectory() as tmp:
            settings = Settings(role_data_file=str(Path(tmp) / 'roles.json'))
            store = RoleStore(settings)
            role = default_role(settings)
            role.pop('bag_reset_version', None)
            role.pop('bag_preview_suppression_version', None)
            first = role_items(role)[0]
            first['location'] = 'equipped'
            equipped_id = int(first['id'])
            store.data['accounts'] = {'legacy': [role]}
            migrated = store.roles_for('legacy')[0]
            self.assertEqual(
                [int(item['id']) for item in role_items(migrated) if item.get('location') == 'equipped'],
                [equipped_id],
            )
            self.assertFalse(any(item.get('location') == 'bag' for item in role_items(migrated)))
            self.assertEqual(migrated['bag_reset_version'], ROLE_BAG_RESET_VERSION)
            self.assertEqual(
                migrated['bag_preview_suppression_version'],
                ROLE_BAG_PREVIEW_SUPPRESSION_VERSION,
            )

    def test_new_role_is_marked_current_and_keeps_starter_bag(self):
        with tempfile.TemporaryDirectory() as tmp:
            settings = Settings(role_data_file=str(Path(tmp) / 'roles.json'))
            store = RoleStore(settings)
            role = store.roles_for('new-user')[0]
            self.assertEqual(role['bag_reset_version'], ROLE_BAG_RESET_VERSION)
            self.assertNotIn('bag_preview_suppression_version', role)
            self.assertTrue(any(item.get('location') == 'bag' for item in role_items(role)))


if __name__ == '__main__':
    unittest.main()
