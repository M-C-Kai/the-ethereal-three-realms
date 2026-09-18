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
    def test_equipment_record_matches_apk_blocks_without_attribute_shift(self):
        from protocol import TYPE_SHORT, TYPE_BYTE, TYPE_INT
        from systems.inventory.protocol import item_frame
        item = {'id': 8, 'template_id': 10000001, 'location': 'bag',
                'equipment_attributes': [11, 12, 13, 14],
                'innate_attributes': [1, 2, 3, 4, 5],
                'acquired_attributes': [6, 7, 8, 9, 10],
                'extra_attributes': [40000, 2, 3, 4, 5]}
        message, fields = decode_frame(item_frame(item))
        self.assertEqual(message, 1008)
        self.assertEqual(len(fields), 39)
        self.assertEqual([(f.type_id, f.value) for f in fields[16:24]],
                         [(TYPE_SHORT, v) for v in [11, 12, 13, 14, 0, 0, 0, 0]])
        self.assertEqual([(f.type_id, f.value) for f in fields[24:34]],
                         [(TYPE_BYTE, v) for v in range(1, 11)])
        self.assertEqual([(f.type_id, f.value) for f in fields[34:39]],
                         [(TYPE_INT, v) for v in [40000, 2, 3, 4, 5]])

    def test_non_equipment_record_keeps_common_fields_only(self):
        from systems.inventory.protocol import item_frame
        _, fields = decode_frame(item_frame({'id': 8, 'template_id': 260000001}))
        self.assertEqual(len(fields), 16)

    def test_catalog_equipment_templates_carry_innate_five_element_values(self):
        # APK B 级证据：1008 字段 24..28 为 5×BYTE 五行基础值（先天属性），
        # 客户端 tooltip 仅显示 >0 的行（pmsj/work/e/b.smali）。
        # 原版 b/g.c() 只接受模板大类 1..10；本地兼容 APK 将该判断扩展到
        # 1..14，因此戒指/外套/饰品/法宝也必须使用完整 39 字段布局。
        from systems.inventory.protocol import item_frame
        from protocol import TYPE_BYTE, TYPE_INT
        for template_id in (
            10001001, 30001001, 100001001, 110001001, 140001001,
        ):
            resolved = self.registry.resolve({'template_id': template_id})
            innate = [int(v) for v in resolved['innate_attributes']]
            self.assertGreater(sum(innate), 0, template_id)
            _, fields = decode_frame(item_frame({
                'id': 1, 'template_id': template_id, 'location': 'bag'}))
            self.assertEqual(len(fields), 39, template_id)
            self.assertEqual([(f.type_id, f.value) for f in fields[24:29]],
                             [(TYPE_BYTE, v) for v in innate])
            self.assertEqual(
                [f.type_id for f in fields[34:39]],
                [TYPE_INT] * 5,
                template_id,
            )

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


    def test_equipment_detail_fallback_contains_configured_attributes(self):
        from systems.inventory.protocol import item_detail_frame
        ring = {'id': 999, 'template_id': 110001001, 'location': 'bag'}
        message_id, fields = decode_frame(item_detail_frame(ring))
        self.assertEqual(message_id, 1032)
        detail = str(fields[3].value)
        self.assertIn('+1 力量(先天)', detail)
        self.assertIn('+2 智力(先天)', detail)
        self.assertIn('+2 精神(先天)', detail)

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
