import json
import sys
import tempfile
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from protocol import decode_frame, field_values
import server as server_module
from server import (
    BASE_CHARACTER_APPEARANCE,
    RoleStore,
    Settings,
    character_appearance,
    default_role,
    ensure_equipment_resource_preview_items,
    player_info,
)


class InventoryCapacityTests(unittest.TestCase):
    def test_new_role_player_info_reports_320_bag_slots(self):
        role = default_role(Settings())

        message_id, fields = decode_frame(player_info(Settings(), role))
        values = field_values(fields)

        self.assertEqual(message_id, 1006)
        self.assertEqual(values[63], 320)  # property 62: APK bag capacity

    def test_legacy_role_gains_persisted_320_slot_bag_without_losing_items(self):
        with tempfile.TemporaryDirectory() as directory:
            role_path = Path(directory) / 'roles.json'
            legacy_role = default_role(Settings())
            legacy_role.pop('bag_capacity')
            legacy_role['name'] = '旧档角色'
            original_item_ids = [item['id'] for item in legacy_role['items']]
            role_path.write_text(json.dumps({
                'next_role_id': 10002,
                'accounts': {'legacy': [legacy_role]},
            }, ensure_ascii=False), encoding='utf-8')

            migrated = RoleStore(Settings(role_data_file=str(role_path))).roles_for('legacy')[0]

            self.assertEqual(migrated.get('bag_capacity'), 320)
            self.assertEqual(migrated['name'], '旧档角色')
            self.assertEqual([item['id'] for item in migrated['items']], original_item_ids)
            persisted = json.loads(role_path.read_text(encoding='utf-8'))
            self.assertEqual(persisted['accounts']['legacy'][0].get('bag_capacity'), 320)

    def test_additional_created_role_starts_with_320_slot_bag(self):
        with tempfile.TemporaryDirectory() as directory:
            role_path = Path(directory) / 'roles.json'
            store = RoleStore(Settings(role_data_file=str(role_path)))
            created = store.create('tester', '第二角色', 6, 1)

            self.assertEqual(created.get('bag_capacity'), 320)
            reloaded = RoleStore(Settings(role_data_file=str(role_path))).find(
                'tester', int(created['id'])
            )
            self.assertIsNotNone(reloaded)
            self.assertEqual(reloaded.get('bag_capacity'), 320)

    def test_full_bag_rejects_unequip_without_moving_item(self):
        move_to_bag = getattr(server_module, 'try_move_item_to_bag', None)
        self.assertIsNotNone(move_to_bag, 'bag capacity transition helper is missing')
        if move_to_bag is None:
            return
        role = {
            'bag_capacity': 40,
            'items': [
                {'id': item_id, 'location': 'bag'}
                for item_id in range(1, 41)
            ],
        }
        equipped = {'id': 100, 'location': 'equipped'}
        role['items'].append(equipped)

        moved = move_to_bag(role, equipped)

        self.assertFalse(moved)
        self.assertEqual(equipped['location'], 'equipped')
        self.assertEqual(
            sum(item['location'] == 'bag' for item in role['items']),
            40,
        )

    def test_available_slot_allows_unequip_into_bag(self):
        role = {
            'bag_capacity': 40,
            'items': [
                {'id': item_id, 'location': 'bag'}
                for item_id in range(1, 40)
            ],
        }
        equipped = {'id': 100, 'location': 'equipped'}
        role['items'].append(equipped)

        moved = server_module.try_move_item_to_bag(role, equipped)

        self.assertTrue(moved)
        self.assertEqual(equipped['location'], 'bag')
        self.assertEqual(
            sum(item['location'] == 'bag' for item in role['items']),
            40,
        )

    def test_item_actions_require_the_apk_location_they_operate_on(self):
        valid_location = getattr(server_module, 'item_action_location_valid', None)
        self.assertIsNotNone(valid_location, 'item action location guard is missing')
        if valid_location is None:
            return
        bag = {'location': 'bag'}
        equipped = {'location': 'equipped'}
        warehouse = {'location': 'warehouse'}

        for action in (3, 4, 5):
            self.assertTrue(valid_location(action, bag))
            self.assertFalse(valid_location(action, equipped))
            self.assertFalse(valid_location(action, warehouse))
        self.assertTrue(valid_location(6, equipped))
        self.assertFalse(valid_location(6, bag))
        self.assertFalse(valid_location(6, warehouse))

    def test_full_bag_skips_new_battle_drop_but_keeps_experience_reward(self):
        role = default_role(Settings())
        capacity = int(role['bag_capacity'])
        role['items'] = [
            {
                'id': item_id,
                'template_id': 300_000_000 + item_id,
                'location': 'bag',
            }
            for item_id in range(1, capacity + 1)
        ]

        reward_item, level_up = server_module.apply_battle_rewards(role)

        self.assertIsNone(reward_item)
        self.assertFalse(level_up)
        self.assertEqual(role['experience'], 50)
        self.assertEqual(len(role['items']), capacity)


class EquipmentResourcePreviewGrantTests(unittest.TestCase):
    def test_preview_grant_is_idempotent_and_uses_unique_instance_ids(self):
        settings = Settings()
        registry = settings.item_registry
        preview_ids = registry.preview_template_ids()
        self.assertEqual(len(preview_ids), 252)
        role = {
            'id': 10001,
            'bag_capacity': 40,
            'items': [
                {
                    'id': 1000104,
                    'template_id': 10001001,
                    'quantity': 1,
                    'location': 'equipped',
                }
            ],
        }
        first = ensure_equipment_resource_preview_items(role, registry)
        self.assertTrue(first)
        after_first = len(role['items'])
        self.assertEqual(after_first, 1 + 252)
        self.assertEqual(role['bag_capacity'], 320)
        self.assertEqual(role['items'][0]['location'], 'equipped')
        second = ensure_equipment_resource_preview_items(role, registry)
        self.assertFalse(second)
        self.assertEqual(len(role['items']), after_first)
        by_template = {}
        instance_ids = []
        for item in role['items']:
            instance_ids.append(item['id'])
            template_id = item['template_id']
            by_template.setdefault(template_id, 0)
            by_template[template_id] += 1
        self.assertEqual(len(set(instance_ids)), len(instance_ids))
        for template_id in preview_ids:
            self.assertEqual(by_template[template_id], 1)
        preview_items = [
            item for item in role['items'] if item['template_id'] in set(preview_ids)
        ]
        self.assertTrue(all(item['location'] == 'bag' for item in preview_items))
        self.assertTrue(all(item['quantity'] == 1 for item in preview_items))

    def test_login_grant_does_not_change_character_appearance(self):
        settings = Settings()
        registry = settings.item_registry
        role = {
            'id': 10001,
            'bag_capacity': 40,
            'items': [
                {
                    'id': 1000104,
                    'template_id': 10001001,
                    'quantity': 1,
                    'location': 'equipped',
                }
            ],
        }
        before = character_appearance(role, registry)
        ensure_equipment_resource_preview_items(role, registry)
        after = character_appearance(role, registry)
        self.assertEqual(after, before)
        self.assertTrue(
            all(
                item['location'] == 'bag'
                for item in role['items']
                if item['template_id'] in set(registry.preview_template_ids())
            )
        )

    def _preview_item_changing_property(self, registry, slot, property_index, current):
        candidates = [
            definition
            for definition in (
                registry.require(template_id)
                for template_id in registry.preview_template_ids()
            )
            if definition.equipment_slot == slot
            and int(definition.appearance_properties.get(str(property_index), current)) != current
        ]
        self.assertTrue(candidates, f'no preview item for slot {slot} changes property {property_index}')
        return candidates[0]

    def test_equipping_preview_shoulder_changes_property16(self):
        settings = Settings()
        registry = settings.item_registry
        role = {'id': 10001, 'items': []}
        before = character_appearance(role, registry)
        definition = self._preview_item_changing_property(registry, 2, 16, before[16])
        role['items'] = [{
            'id': 1,
            'template_id': definition.template_id,
            'quantity': 1,
            'location': 'equipped',
        }]
        after = character_appearance(role, registry)
        self.assertEqual(after[16], definition.appearance_properties['16'])
        self.assertNotEqual(after[16], before[16])

    def test_equipping_preview_armor_changes_property15(self):
        settings = Settings()
        registry = settings.item_registry
        role = {'id': 10001, 'items': []}
        before = character_appearance(role, registry)
        definition = self._preview_item_changing_property(registry, 3, 15, before[15])
        role['items'] = [{
            'id': 1,
            'template_id': definition.template_id,
            'quantity': 1,
            'location': 'equipped',
        }]
        after = character_appearance(role, registry)
        self.assertEqual(after[15], definition.appearance_properties['15'])
        self.assertNotEqual(after[15], before[15])

    def test_unequipping_preview_restores_base_or_remaining_equipped(self):
        settings = Settings()
        registry = settings.item_registry
        role = {'id': 10001, 'items': []}
        shoulder = self._preview_item_changing_property(registry, 2, 16, 0)
        armor = self._preview_item_changing_property(registry, 3, 15, 0)
        role['items'] = [
            {
                'id': 1,
                'template_id': shoulder.template_id,
                'quantity': 1,
                'location': 'equipped',
            },
            {
                'id': 2,
                'template_id': armor.template_id,
                'quantity': 1,
                'location': 'equipped',
            },
        ]
        equipped = character_appearance(role, registry)
        self.assertEqual(equipped[16], shoulder.appearance_properties['16'])
        self.assertEqual(equipped[15], armor.appearance_properties['15'])
        role['items'][0]['location'] = 'bag'
        after_unequip = character_appearance(role, registry)
        self.assertEqual(after_unequip[16], BASE_CHARACTER_APPEARANCE[16])
        self.assertEqual(after_unequip[15], armor.appearance_properties['15'])
        role['items'][1]['location'] = 'bag'
        after_all = character_appearance(role, registry)
        self.assertEqual(after_all, dict(BASE_CHARACTER_APPEARANCE))


if __name__ == '__main__':
    unittest.main()
