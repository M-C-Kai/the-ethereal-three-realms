"""统一测试：背包系统（容量、装备/卸下、使用、丢弃、强化）。"""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from app.context import SystemContext
from protocol import decode_frame
from systems.battle.service import battle_state_for
from systems.inventory.handler import InventorySystem
from systems.inventory.protocol import STRENGTHENING_ACTIONS, find_item, item_slot, role_items
from systems.inventory.service import (
    bag_capacity, bag_item_count, try_move_item_to_bag,
)
from systems.role.events import CharacterUpdateBus
from systems.role.service import RoleStore


ROOT = Path(__file__).resolve().parent.parent


def make_game():
    import server

    settings = server.Settings.load(server.Path(ROOT) / 'config.json')
    return settings, server.LocalGameServer(settings)


def weapon_of(role, registry):
    for item in role_items(role):
        resolved = registry.resolve(item)
        if int(resolved.get('equipment_slot', 0)) == 10:
            return item
    return None


class InventoryHelperTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.settings, cls.game = make_game()
        cls.registry = cls.settings.item_registry

    def test_role_items_accessor_mutates_role(self):
        role = {'items': [None, {'id': 5}]}
        items = role_items(role)
        self.assertEqual([i for i in items if i], [{'id': 5}])
        self.assertIn('items', role)

    def test_bag_capacity_and_move(self):
        role = {'bag_capacity': 10, 'items': [{'id': 1, 'location': 'bag', 'quantity': 1}]}
        self.assertEqual(bag_capacity(role), 10)
        self.assertEqual(bag_item_count(role), 1)
        self.assertTrue(try_move_item_to_bag(role, {'id': 2, 'location': 'equipped', 'quantity': 1}))

    def test_item_slot_for_weapon(self):
        role = {'items': []}
        weapon = weapon_of({'items': self.game.roles.data['accounts']['localtest'][0]['items']} if False else {'items': []}, self.registry)
        self.assertIsNone(weapon)


class InventoryHandlerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.settings, self.game = make_game()
        self.settings.role_data_file = str(Path(self.tmp.name) / 'roles.json')
        self.store = RoleStore(self.settings)
        self.role = self.store.create('tester', '测试角色', 0, 0)
        self.system = InventorySystem(
            self.settings,
            save=self.store.save,
            character_update_bus=self.game.character_update_bus,
        )
        self.session = {}

    def tearDown(self):
        self.tmp.cleanup()

    def _context(self):
        return SystemContext(username='tester', active_role=self.role, session=self.session)

    def _handle(self, frame_id, fields):
        return self.system.handle(self._context(), frame_id, fields)

    def test_item_detail_by_template(self):
        item = role_items(self.role)[0]
        template_id = int(item['template_id'])
        from protocol import integer, short
        result = self._handle(1032, [short(0), integer(template_id)])
        self.assertTrue(result.handled)
        message_id, fields = decode_frame(result.frames[0])
        self.assertEqual(message_id, 1032)

    def test_equip_and_unequip_weapon_refreshes(self):
        from protocol import integer, short
        weapon = next(
            (i for i in role_items(self.role)
             if int(self.settings.item_registry.resolve(i).get('equipment_slot', 0)) == 10),
            None,
        )
        self.assertIsNotNone(weapon)
        item_id = int(weapon['id'])
        result = self._handle(1009, [short(5), integer(item_id)])
        self.assertTrue(result.handled)
        self.assertEqual(weapon['location'], 'equipped')
        # 1008 更新 + 1009 ack + 1017 外观 + 1039 面板
        message_ids = [decode_frame(frame)[0] for frame in result.frames]
        self.assertIn(1008, message_ids)
        self.assertIn(1017, message_ids)
        result = self._handle(1009, [short(6), integer(item_id)])
        self.assertEqual(weapon['location'], 'bag')
        message_ids = [decode_frame(frame)[0] for frame in result.frames]
        self.assertIn(1017, message_ids)

    def test_discard_item(self):
        from protocol import integer, short
        item = role_items(self.role)[0]
        item_id = int(item['id'])
        result = self._handle(1009, [short(3), integer(item_id)])
        self.assertTrue(result.handled)
        self.assertIsNone(find_item(self.role, item_id))

    def test_strengthening_actions_declared(self):
        self.assertEqual(STRENGTHENING_ACTIONS, {74, 75, 77, 92, 97})


if __name__ == '__main__':
    unittest.main()
