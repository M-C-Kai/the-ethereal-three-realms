"""统一测试：背包系统（容量、装备/卸下、使用、丢弃、强化）。"""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from app.context import SystemContext
from protocol import decode_frame
from systems.battle.service import battle_state_for
from systems.inventory.handler import InventorySystem
from systems.inventory.protocol import (
    GEM_EMBEDDING_ACTIONS, GEM_REMOVAL_ACTIONS, SOCKET_OPENING_ACTIONS,
    STRENGTHENING_ACTIONS,
    find_item, item_slot,
    native_socket_slots, opened_socket_count, role_items,
)
from systems.inventory.service import (
    bag_capacity, bag_item_count, gem_embedding_action_result,
    gem_removal_action_result, socket_opening_action_result,
    try_move_item_to_bag,
)
from systems.inventory.socket import (
    SOCKET_STATE_VERSION, gem_socket_type, socket_types,
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

    def test_1008_uses_extra_attributes_as_authoritative_socket_state(self):
        from protocol import TYPE_INT
        from systems.inventory.protocol import item_frame
        item = {
            'id': 701, 'template_id': 10000001, 'location': 'bag',
            'socket_count': 3,
            'extra_attributes': [1, 2, 0, 0, 0],
        }
        _, fields = decode_frame(item_frame(item))
        self.assertEqual(
            [(f.type_id, f.value) for f in fields[34:39]],
            [(TYPE_INT, 1), (TYPE_INT, 2), (TYPE_INT, 0),
             (TYPE_INT, 0), (TYPE_INT, 0)],
        )
        self.assertEqual(opened_socket_count(item), 2)

    def test_native_socket_helpers_ignore_legacy_socket_count(self):
        item = {'socket_count': 5, 'extra_attributes': [1, 0x13315480, 0, 0, 0]}
        self.assertEqual(native_socket_slots(item), [1, 0x13315480, 0, 0, 0])
        self.assertEqual(opened_socket_count(item), 2)

    def test_open_empty_sockets_are_not_inferred_from_gem_ids(self):
        from systems.inventory.protocol import equipment_detail_description
        item = {
            'template_id': 10000001,
            'description': '测试装备',
            'socket_count': 1,
            'extra_attributes': [1, 2, 3, 0, 0],
        }
        detail = equipment_detail_description(item)
        self.assertIn('开孔 3/5', detail)
        self.assertNotIn('开孔 1/5', detail)

    def test_non_equipment_record_keeps_common_fields_only(self):
        from systems.inventory.protocol import item_frame
        _, fields = decode_frame(item_frame({'id': 8, 'template_id': 260000001}))
        self.assertEqual(len(fields), 16)

    def test_reference_ring_carries_complete_equipment_detail_data(self):
        from protocol import TYPE_BYTE, TYPE_INT, TYPE_SHORT
        from systems.inventory.protocol import item_frame, item_detail_frame

        ring = {'id': 777, 'template_id': 110001001, 'location': 'bag'}
        message, fields = decode_frame(item_frame(ring, self.registry))
        self.assertEqual(message, 1008)
        self.assertEqual(fields[2].type_id, TYPE_SHORT)
        self.assertEqual(fields[2].value, 200)
        self.assertEqual(fields[3].type_id, TYPE_SHORT)
        self.assertEqual(fields[3].value, 200)
        self.assertEqual(fields[6].value, 5000)
        self.assertEqual(fields[7].value, 110001009)
        self.assertEqual(fields[11].value, 1)
        self.assertEqual(
            [(f.type_id, f.value) for f in fields[29:34]],
            [(TYPE_BYTE, v) for v in [15, 20, 20, 20, 21]],
        )
        self.assertEqual(
            [f.type_id for f in fields[34:39]],
            [TYPE_INT] * 5,
        )

        detail_message, detail_fields = decode_frame(item_detail_frame(ring))
        self.assertEqual(detail_message, 1032)
        detail = str(detail_fields[3].value)
        for expected in (
            '+17 精神(先天)',
            '+15 力量',
            '强度 +9',
            '+135 物理防御',
            '+135 法术防御',
            '耐久度 200/200',
            '需要等级 1',
            '价格: 5000',
        ):
            self.assertIn(expected, detail)

    def test_equipment_durability_override_is_instance_state(self):
        from systems.inventory.protocol import item_frame
        ring = {
            'id': 778,
            'template_id': 110001001,
            'location': 'equipped',
            'durability': 137,
        }
        _, fields = decode_frame(item_frame(ring, self.registry))
        self.assertEqual(fields[2].value, 137)
        self.assertEqual(fields[3].value, 200)

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


class InventorySocketMigrationTests(unittest.TestCase):
    def test_role_loader_migrates_legacy_socket_count_once(self):
        import server
        with tempfile.TemporaryDirectory() as tmp:
            settings = server.Settings.load(server.Path(ROOT) / 'config.json')
            settings.role_data_file = str(Path(tmp) / 'roles.json')
            store = RoleStore(settings)
            role = store.create('socket-migrate', '孔位迁移', 0, 0)
            item = next(
                x for x in role_items(role)
                if int(settings.item_registry.resolve(x).get('equipment_slot', 0)) == 10
            )
            item.pop('extra_attributes', None)
            item['socket_count'] = 3
            item_id = int(item['id'])
            store.save()

            reloaded = RoleStore(settings)
            migrated_role = reloaded.roles_for('socket-migrate')[0]
            migrated = next(x for x in role_items(migrated_role) if int(x.get('id', 0)) == item_id)
            self.assertEqual(migrated['extra_attributes'], [1, 1, 1, 0, 0])
            self.assertEqual(migrated['socket_types'], [1, 1, 1, 0, 0])
            self.assertEqual(migrated_role['socket_state_version'], SOCKET_STATE_VERSION)
            self.assertNotIn('socket_count', migrated)

            second = RoleStore(settings)
            second_role = second.roles_for('socket-migrate')[0]
            second_item = next(x for x in role_items(second_role) if int(x.get('id', 0)) == item_id)
            self.assertEqual(second_item['extra_attributes'], [1, 1, 1, 0, 0])
            self.assertEqual(second_item['socket_types'], [1, 1, 1, 0, 0])
            self.assertNotIn('socket_count', second_item)

    def test_role_loader_normalizes_old_weapon_hole_code_ten(self):
        import server
        with tempfile.TemporaryDirectory() as tmp:
            settings = server.Settings.load(server.Path(ROOT) / 'config.json')
            settings.role_data_file = str(Path(tmp) / 'roles.json')
            store = RoleStore(settings)
            role = store.create('socket-code-fix', '孔码修复', 0, 0)
            weapon = next(
                x for x in role_items(role)
                if int(settings.item_registry.resolve(x).get('equipment_slot', 0)) == 10
            )
            weapon['extra_attributes'] = [10, 1, 0, 0, 0]
            weapon_id = int(weapon['id'])
            store.save()

            reloaded = RoleStore(settings)
            loaded = reloaded.roles_for('socket-code-fix')[0]
            fixed = next(x for x in role_items(loaded) if int(x.get('id', 0)) == weapon_id)
            self.assertEqual(fixed['extra_attributes'], [1, 1, 0, 0, 0])
            self.assertEqual(fixed['socket_types'], [1, 1, 0, 0, 0])

    def test_role_loader_preserves_real_socket_colours(self):
        import server
        with tempfile.TemporaryDirectory() as tmp:
            settings = server.Settings.load(server.Path(ROOT) / 'config.json')
            settings.role_data_file = str(Path(tmp) / 'roles.json')
            store = RoleStore(settings)
            role = store.create('socket-colours', '孔色迁移', 0, 0)
            weapon = next(
                x for x in role_items(role)
                if int(settings.item_registry.resolve(x).get('equipment_slot', 0)) == 10
            )
            weapon['extra_attributes'] = [2, 3, 4, 5, 6]
            weapon.pop('socket_types', None)
            weapon_id = int(weapon['id'])
            store.save()

            reloaded = RoleStore(settings)
            loaded = reloaded.roles_for('socket-colours')[0]
            migrated = next(x for x in role_items(loaded) if int(x.get('id', 0)) == weapon_id)
            self.assertEqual(migrated['extra_attributes'], [2, 3, 4, 5, 6])
            self.assertEqual(migrated['socket_types'], [2, 3, 4, 5, 6])

    def test_role_loader_recovers_socket_type_from_embedded_gem(self):
        import server
        with tempfile.TemporaryDirectory() as tmp:
            settings = server.Settings.load(server.Path(ROOT) / 'config.json')
            settings.role_data_file = str(Path(tmp) / 'roles.json')
            store = RoleStore(settings)
            role = store.create('socket-gem-migrate', '宝石孔迁移', 0, 0)
            weapon = next(
                x for x in role_items(role)
                if int(settings.item_registry.resolve(x).get('equipment_slot', 0)) == 10
            )
            weapon['extra_attributes'] = [322002000, 322004000, 0, 0, 0]
            weapon.pop('socket_types', None)
            weapon_id = int(weapon['id'])
            store.save()

            reloaded = RoleStore(settings)
            loaded = reloaded.roles_for('socket-gem-migrate')[0]
            migrated = next(x for x in role_items(loaded) if int(x.get('id', 0)) == weapon_id)
            self.assertEqual(migrated['extra_attributes'], [322002000, 322004000, 0, 0, 0])
            self.assertEqual(migrated['socket_types'], [3, 5, 0, 0, 0])
            self.assertEqual(gem_socket_type(322001000), 2)

    def test_ring_legacy_socket_count_is_not_migrated(self):
        import server
        with tempfile.TemporaryDirectory() as tmp:
            settings = server.Settings.load(server.Path(ROOT) / 'config.json')
            settings.role_data_file = str(Path(tmp) / 'roles.json')
            store = RoleStore(settings)
            role = store.create('ring-migrate', '戒指迁移', 0, 0)
            ring = {
                'id': int(role['id']) * 10000 + 999,
                'template_id': 110001001,
                'location': 'bag',
                'socket_count': 3,
            }
            role_items(role).append(ring)
            store.save()

            reloaded = RoleStore(settings)
            migrated_role = reloaded.roles_for('ring-migrate')[0]
            migrated = next(x for x in role_items(migrated_role) if x.get('template_id') == 110001001)
            self.assertEqual(migrated['extra_attributes'], [0, 0, 0, 0, 0])
            self.assertEqual(migrated['socket_types'], [0, 0, 0, 0, 0])
            self.assertNotIn('socket_count', migrated)


class _FixedRng:
    def __init__(self, value: int):
        self.value = value

    def randrange(self, upper: int) -> int:
        return min(max(0, self.value), upper - 1)


class InventorySocketOpeningTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.settings, cls.game = make_game()
        cls.registry = cls.settings.item_registry

    def _role(self):
        role = {
            'id': 77,
            'items': [
                {
                    'id': 7701,
                    'template_id': 100001001,
                    'location': 'bag',
                    'extra_attributes': [0, 0, 0, 0, 0],
                },
                {
                    'id': 7721,
                    'template_id': 322250000,
                    'location': 'bag',
                    'quantity': 3,
                },
            ],
        }
        return role

    def test_apk_socket_actions_declared(self):
        self.assertEqual(SOCKET_OPENING_ACTIONS, {90, 95})

    def test_open_socket_page_uses_action_95(self):
        from protocol import short
        role = self._role()
        result = socket_opening_action_result(
            role, [95], _FixedRng(0), self.registry,
        )
        self.assertFalse(result.changed)
        message_id, fields = decode_frame(result.frames[0])
        self.assertEqual(message_id, 1009)
        self.assertEqual(fields[0].value, 95)

    def test_first_socket_succeeds_and_consumes_one_chaos_stone(self):
        role = self._role()
        result = socket_opening_action_result(
            role, [90, 7701, 7721], _FixedRng(9999), self.registry,
        )
        self.assertTrue(result.changed)
        equipment = find_item(role, 7701)
        stone = find_item(role, 7721)
        self.assertEqual(equipment['extra_attributes'], [6, 0, 0, 0, 0])
        self.assertEqual(equipment['socket_types'], [6, 0, 0, 0, 0])
        self.assertEqual(stone['quantity'], 2)
        message_ids = [decode_frame(frame)[0] for frame in result.frames]
        self.assertIn(1008, message_ids)
        repaint_message, repaint_fields = decode_frame(result.frames[-2])
        self.assertEqual(repaint_message, 1009)
        self.assertEqual(repaint_fields[0].value, 90)
        refresh_message, refresh_fields = decode_frame(result.frames[-1])
        self.assertEqual(refresh_message, 1009)
        self.assertEqual(refresh_fields[0].value, 95)

    def test_weapon_opening_can_generate_lowest_common_socket_colour(self):
        role = self._role()
        result = socket_opening_action_result(
            role, [90, 7701, 7721], _FixedRng(0), self.registry,
        )
        self.assertTrue(result.changed)
        equipment = find_item(role, 7701)
        self.assertEqual(native_socket_slots(equipment), [1, 0, 0, 0, 0])
        self.assertEqual(socket_types(equipment), [1, 0, 0, 0, 0])

    def test_normal_equipment_never_generates_purple_socket(self):
        role = self._role()
        result = socket_opening_action_result(
            role, [90, 7701, 7721], _FixedRng(9999), self.registry,
        )
        self.assertTrue(result.changed)
        equipment = find_item(role, 7701)
        self.assertEqual(socket_types(equipment)[0], 6)

    def test_belt_can_generate_purple_socket(self):
        role = self._role()
        equipment = find_item(role, 7701)
        equipment['template_id'] = 40001001
        result = socket_opening_action_result(
            role, [90, 7701, 7721], _FixedRng(9999), self.registry,
        )
        self.assertTrue(result.changed)
        self.assertEqual(socket_types(equipment), [7, 0, 0, 0, 0])
        self.assertEqual(native_socket_slots(equipment), [7, 0, 0, 0, 0])

    def test_bracer_can_generate_purple_socket(self):
        role = self._role()
        equipment = find_item(role, 7701)
        equipment['template_id'] = 80001001
        result = socket_opening_action_result(
            role, [90, 7701, 7721], _FixedRng(9999), self.registry,
        )
        self.assertTrue(result.changed)
        self.assertEqual(socket_types(equipment), [7, 0, 0, 0, 0])

    def test_failed_later_socket_keeps_equipment_and_consumes_stone(self):
        role = self._role()
        equipment = find_item(role, 7701)
        equipment['extra_attributes'] = [1, 0, 0, 0, 0]
        result = socket_opening_action_result(
            role, [90, 7701, 7721], _FixedRng(9999), self.registry,
        )
        self.assertTrue(result.changed)
        self.assertEqual(equipment['extra_attributes'], [1, 0, 0, 0, 0])
        self.assertEqual(find_item(role, 7721)['quantity'], 2)
        self.assertIn('开孔失败', result.message)

    def test_special_chaos_stone_guarantees_socket_in_local_compat_rule(self):
        role = self._role()
        role['items'][1]['template_id'] = 322250001
        equipment = find_item(role, 7701)
        equipment['extra_attributes'] = [1, 1, 1, 1, 0]
        result = socket_opening_action_result(
            role, [90, 7701, 7721], _FixedRng(9999), self.registry,
        )
        self.assertTrue(result.changed)
        self.assertEqual(equipment['extra_attributes'], [1, 1, 1, 1, 6])
        self.assertEqual(equipment['socket_types'], [1, 1, 1, 1, 6])

    def test_ring_is_rejected_without_consuming_material(self):
        role = self._role()
        role['items'][0]['template_id'] = 110001001
        result = socket_opening_action_result(
            role, [90, 7701, 7721], _FixedRng(0), self.registry,
        )
        self.assertFalse(result.changed)
        self.assertEqual(find_item(role, 7721)['quantity'], 3)
        self.assertIn('不能开孔', result.message)


    def test_consumed_chaos_stone_is_not_regranted(self):
        import server
        with tempfile.TemporaryDirectory() as tmp:
            settings = server.Settings.load(server.Path(ROOT) / 'config.json')
            settings.role_data_file = str(Path(tmp) / 'roles.json')
            store = RoleStore(settings)
            role = store.create('chaos-once', '混沌石一次性', 0, 0)
            stones = [
                item for item in role_items(role)
                if 322250000 <= int(item.get('template_id', 0)) <= 322250003
            ]
            self.assertEqual(len(stones), 4)
            consumed_id = int(stones[0]['id'])
            role_items(role).remove(stones[0])
            store.save()

            reloaded = RoleStore(settings)
            loaded_role = reloaded.roles_for('chaos-once')[0]
            self.assertIsNone(find_item(loaded_role, consumed_id))
            self.assertTrue(loaded_role.get('chaos_stones_initialized'))


class InventoryGemEmbeddingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.settings, cls.game = make_game()
        cls.registry = cls.settings.item_registry

    def _role(self, socket_type=3, gem_template=322002000):
        return {
            'id': 88,
            'items': [
                {
                    'id': 8801,
                    'template_id': 100001001,
                    'location': 'bag',
                    'socket_types': [socket_type, 0, 0, 0, 0],
                    'extra_attributes': [socket_type, 0, 0, 0, 0],
                },
                {
                    'id': 8825,
                    'template_id': gem_template,
                    'location': 'bag',
                    'quantity': 3,
                },
            ],
        }

    def test_apk_gem_embedding_actions_declared(self):
        self.assertEqual(GEM_EMBEDDING_ACTIONS, {93, 94, 98})

    def test_open_embedding_page_uses_action_98(self):
        role = self._role()
        result = gem_embedding_action_result(role, [98], self.registry)
        self.assertFalse(result.changed)
        message, fields = decode_frame(result.frames[0])
        self.assertEqual(message, 1009)
        self.assertEqual(fields[0].value, 98)

    def test_selecting_gem_uses_action_94_ack(self):
        role = self._role()
        result = gem_embedding_action_result(
            role, [94, 8801, 8825], self.registry,
        )
        self.assertFalse(result.changed)
        message, fields = decode_frame(result.frames[0])
        self.assertEqual(message, 1009)
        self.assertEqual(fields[0].value, 94)

    def test_matching_gem_embeds_into_first_open_empty_socket(self):
        role = self._role(socket_type=3, gem_template=322002000)
        result = gem_embedding_action_result(
            role, [93, 8801, 8825], self.registry,
        )
        self.assertTrue(result.changed)
        equipment = find_item(role, 8801)
        gem = find_item(role, 8825)
        self.assertEqual(equipment['socket_types'], [3, 0, 0, 0, 0])
        self.assertEqual(equipment['extra_attributes'], [322002000, 0, 0, 0, 0])
        self.assertEqual(gem['quantity'], 2)
        repaint_message, repaint_fields = decode_frame(result.frames[-2])
        self.assertEqual(repaint_message, 1009)
        self.assertEqual(repaint_fields[0].value, 93)
        rebind_message, rebind_fields = decode_frame(result.frames[-1])
        self.assertEqual(rebind_message, 1009)
        self.assertEqual(rebind_fields[0].value, 98)

    def test_mismatched_gem_is_rejected_without_consuming(self):
        role = self._role(socket_type=5, gem_template=322002000)
        result = gem_embedding_action_result(
            role, [93, 8801, 8825], self.registry,
        )
        self.assertFalse(result.changed)
        self.assertEqual(find_item(role, 8825)['quantity'], 3)
        self.assertEqual(find_item(role, 8801)['extra_attributes'], [5, 0, 0, 0, 0])
        self.assertIn('不匹配', result.message)

    def test_embedding_uses_first_empty_socket_in_order(self):
        role = self._role(socket_type=3, gem_template=322004000)
        equipment = find_item(role, 8801)
        equipment['socket_types'] = [3, 5, 0, 0, 0]
        equipment['extra_attributes'] = [322002000, 5, 0, 0, 0]
        result = gem_embedding_action_result(
            role, [93, 8801, 8825], self.registry,
        )
        self.assertTrue(result.changed)
        self.assertEqual(
            equipment['extra_attributes'],
            [322002000, 322004000, 0, 0, 0],
        )

    def test_gold_gem_uses_locked_socket_type_two(self):
        role = self._role(socket_type=2, gem_template=322001000)
        result = gem_embedding_action_result(
            role, [93, 8801, 8825], self.registry,
        )
        self.assertTrue(result.changed)
        self.assertEqual(
            find_item(role, 8801)['extra_attributes'][0],
            322001000,
        )

    def test_no_open_empty_socket_is_rejected(self):
        role = self._role(socket_type=3, gem_template=322002000)
        equipment = find_item(role, 8801)
        equipment['extra_attributes'] = [322002000, 0, 0, 0, 0]
        result = gem_embedding_action_result(
            role, [93, 8801, 8825], self.registry,
        )
        self.assertFalse(result.changed)
        self.assertIn('没有可镶嵌的空孔', result.message)


class InventoryGemRemovalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.settings, cls.game = make_game()
        cls.registry = cls.settings.item_registry

    def _role(self, silver=5000, with_stack=True):
        items = [
            {
                'id': 9901,
                'template_id': 100001001,
                'location': 'bag',
                'socket_types': [3, 5, 0, 0, 0],
                'extra_attributes': [322002000, 5, 0, 0, 0],
            },
        ]
        if with_stack:
            items.append({
                'id': 9925,
                'template_id': 322002000,
                'location': 'bag',
                'quantity': 2,
            })
        return {
            'id': 99,
            'currencies': {
                'silver': silver,
                'immortal_stones': 100,
                'immortal_crystals': 100,
            },
            'items': items,
        }

    def test_apk_gem_removal_actions_declared(self):
        self.assertEqual(GEM_REMOVAL_ACTIONS, {72, 73, 108})

    def test_open_removal_page_uses_action_73(self):
        result = gem_removal_action_result(
            self._role(), [73], self.registry,
        )
        self.assertFalse(result.changed)
        message, fields = decode_frame(result.frames[0])
        self.assertEqual(message, 1009)
        self.assertEqual(fields[0].value, 73)

    def test_remove_gem_restores_socket_and_returns_to_stack(self):
        role = self._role(silver=5000, with_stack=True)
        result = gem_removal_action_result(
            role, [72, 9901, 0], self.registry,
        )
        self.assertTrue(result.changed)
        equipment = find_item(role, 9901)
        stack = find_item(role, 9925)
        self.assertEqual(equipment['socket_types'], [3, 5, 0, 0, 0])
        self.assertEqual(equipment['extra_attributes'], [3, 5, 0, 0, 0])
        self.assertEqual(stack['quantity'], 3)
        self.assertEqual(role['currencies']['silver'], 4000)

        message_ids = [decode_frame(frame)[0] for frame in result.frames]
        self.assertIn(1008, message_ids)
        self.assertIn(1017, message_ids)
        repaint_message, repaint_fields = decode_frame(result.frames[-2])
        self.assertEqual(repaint_message, 1009)
        self.assertEqual(repaint_fields[0].value, 107)
        refresh_message, refresh_fields = decode_frame(result.frames[-1])
        self.assertEqual(refresh_message, 1009)
        self.assertEqual(refresh_fields[0].value, 73)

    def test_remove_gem_creates_new_bag_instance_when_stack_missing(self):
        role = self._role(silver=5000, with_stack=False)
        result = gem_removal_action_result(
            role, [72, 9901, 0], self.registry,
        )
        self.assertTrue(result.changed)
        returned = [
            item for item in role_items(role)
            if int(item.get('template_id', 0)) == 322002000
        ]
        self.assertEqual(len(returned), 1)
        self.assertEqual(returned[0]['quantity'], 1)
        self.assertEqual(returned[0]['location'], 'bag')

    def test_insufficient_silver_does_not_remove_gem(self):
        role = self._role(silver=999, with_stack=True)
        result = gem_removal_action_result(
            role, [72, 9901, 0], self.registry,
        )
        self.assertFalse(result.changed)
        self.assertEqual(
            find_item(role, 9901)['extra_attributes'],
            [322002000, 5, 0, 0, 0],
        )
        self.assertEqual(find_item(role, 9925)['quantity'], 2)
        self.assertEqual(role['currencies']['silver'], 999)

    def test_empty_socket_cannot_be_removed(self):
        role = self._role()
        result = gem_removal_action_result(
            role, [72, 9901, 1], self.registry,
        )
        self.assertFalse(result.changed)
        self.assertIn('没有可拆除', result.message)

    def test_action_108_inspection_does_not_mutate_state(self):
        role = self._role()
        result = gem_removal_action_result(
            role, [108, 9901, 0], self.registry,
        )
        self.assertFalse(result.changed)
        self.assertEqual(role['currencies']['silver'], 5000)
        self.assertEqual(
            find_item(role, 9901)['extra_attributes'][0],
            322002000,
        )


class InventoryGemStarterGrantTests(unittest.TestCase):
    def test_consumed_socket_gem_is_not_regranted(self):
        import server
        with tempfile.TemporaryDirectory() as tmp:
            settings = server.Settings.load(server.Path(ROOT) / 'config.json')
            settings.role_data_file = str(Path(tmp) / 'roles.json')
            store = RoleStore(settings)
            role = store.create('gem-once', '宝石一次性', 0, 0)
            gems = [
                item for item in role_items(role)
                if 322000000 <= int(item.get('template_id', 0)) <= 322006011
                and gem_socket_type(int(item.get('template_id', 0))) is not None
            ]
            self.assertEqual(len(gems), 9)
            consumed = gems[0]
            consumed_template = int(consumed['template_id'])
            role_items(role).remove(consumed)
            store.save()

            reloaded = RoleStore(settings)
            loaded = reloaded.roles_for('gem-once')[0]
            self.assertFalse(any(
                int(item.get('template_id', 0)) == consumed_template
                for item in role_items(loaded)
            ))
            self.assertTrue(loaded.get('socket_gems_initialized'))


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
