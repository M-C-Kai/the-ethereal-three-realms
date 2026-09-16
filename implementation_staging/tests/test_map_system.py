"""统一测试：地图系统（世界初始化、移动、进入帧、寻路、动态地图、巡逻 Boss、同图玩家互见）。"""
from __future__ import annotations

import unittest
from unittest import mock
from pathlib import Path

from app.context import SystemContext
from protocol import Field, TYPE_INT, decode_frame
from systems.map.handler import MapSystem
from systems.map.protocol import (
    ROAMING_BOSS_ID, dynamic_map_enter_frames, is_roaming_boss_definition,
    map_ref_transfer_frames, map_movement_final_tile,
)
from systems.map.service import settings_for_role, update_role_position


ROOT = Path(__file__).resolve().parent.parent


def make_game():
    import server

    settings = server.Settings.load(server.Path(ROOT) / 'config.json')
    return settings, server.LocalGameServer(settings)


class MapSystemHandlerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.settings, cls.game = make_game()
        cls.system = cls.game.map_system

    def _context(self, role=None, session=None):
        return SystemContext(username='tester', active_role=role, session=session if session is not None else {})

    def _fields(self, values, types):
        from protocol import Field, TYPE_INT, TYPE_SHORT
        builders = {4: TYPE_INT, 3: TYPE_SHORT, 2: TYPE_INT}
        fields = []
        for value, type_id in zip(values, types):
            fields.append(Field(type_id, value))
        return fields

    def test_world_init_frames(self):
        session = {}
        result = self.system.handle(self._context(session=session), 1123, [])
        self.assertTrue(result.handled)
        message_ids = [decode_frame(frame)[0] for frame in result.frames]
        self.assertEqual(message_ids, [1123, 1110])
        # 第二次进图前不重复下发（同一连接会话）
        result = self.system.handle(self._context(session=session), 1123, [])
        self.assertFalse(result.handled)

    def test_movement_updates_position(self):
        from systems.role.service import default_role
        role = default_role(self.settings)
        role['map_id'] = self.settings.default_map_id
        # C->S 1005 为 [x, y, ...] 移动请求
        fields = self._fields([60, 67], [4, 4])
        result = self.system.handle(self._context(role, {}), 1005, fields)
        self.assertTrue(result.handled)
        self.assertEqual((int(role['map_x']), int(role['map_y'])), (60, 67))

    def test_map_data_frames(self):
        role = None
        fields = self._fields([12], [4])
        result = self.system.handle(self._context(role), 1010, fields)
        decoded = [decode_frame(frame) for frame in result.frames]
        self.assertEqual([message_id for message_id, _ in decoded],
                         [1010, 1407, 1407, 1407, 1407, 1407, 1010])
        self.assertEqual([fields[0].value for message_id, fields in decoded
                          if message_id == 1407], [0, 1, 3, 5, 7])
        self.assertEqual(decoded[-1][1][4].value, 1)
        self.assertEqual(decoded[-1][1][5].value, 12)

    def test_auto_grind_request_returns_native_short_start_ack(self):
        # APK k menu sends 1010/SHORT 280; e's matching branch records
        # the local origin. Missing ack leaves client-side roaming inactive.
        from protocol import TYPE_SHORT
        role = {'id': 10001, 'map_id': 58, 'map_x': 60, 'map_y': 67}
        original = dict(role)
        context = self._context(role, {})
        for _ in range(2):
            result = self.system.handle(context, 1010, [Field(TYPE_SHORT, 280)])
            self.assertTrue(result.handled)
            self.assertEqual(len(result.frames), 1)
            message_id, fields = decode_frame(result.frames[0])
            self.assertEqual(message_id, 1010)
            self.assertEqual([(field.type_id, field.value) for field in fields],
                             [(TYPE_INT, 0), (TYPE_SHORT, 0), (TYPE_SHORT, 0),
                              (TYPE_INT, 0), (TYPE_INT, 0), (TYPE_SHORT, 280)])
        self.assertEqual(role, original)

    def test_pathfind_known_target(self):
        # 采集目标 6001 位于 58 号地图 (12,8)
        role = {'map_id': 58}
        fields = self._fields([0, 58, 12, 8], [2, 4, 2, 2])
        result = self.system.handle(self._context(role), 1145, fields)
        self.assertTrue(result.handled)
        self.assertTrue(result.frames)
        message_id, _ = decode_frame(result.frames[0])
        self.assertEqual(message_id, 1145)

    def test_enter_frames_replace_boss_with_native_q(self):
        definition = self.settings.map_registry.require(58)
        frames = dynamic_map_enter_frames(definition, 10001)
        message_ids = [decode_frame(frame)[0] for frame in frames]
        self.assertIn(1126, message_ids)
        self.assertIn(2028, message_ids)   # 巡逻 Boss 原生 q 角色
        spawn = next(
            (frame for frame, message_id in zip(frames, message_ids) if message_id == 2028),
            None,
        )
        _, fields = decode_frame(spawn)
        self.assertEqual(int(fields[0].value), ROAMING_BOSS_ID)

    def test_enter_frames_include_map_ref_transfer(self):
        definition = self.settings.map_registry.require(60010)
        frames = dynamic_map_enter_frames(definition, 10001)
        message_ids = [decode_frame(frame)[0] for frame in frames]
        self.assertIn(1407, message_ids)   # map.ref 分块

    def test_map_ref_transfer_for_dynamic_map(self):
        definition = self.settings.map_registry.require(60010)
        frames = map_ref_transfer_frames(definition)
        self.assertTrue(frames)

    def test_movement_final_tile(self):
        # C->S 1005 请求以 [x, y, ...] 开头
        self.assertEqual(map_movement_final_tile([61, 68, 0]), (61, 68))

    def test_update_role_position(self):
        role = {'map_id': 58, 'map_x': 0, 'map_y': 0}
        self.assertTrue(update_role_position(role, 12, 8))
        self.assertFalse(update_role_position(role, 12, 8))


class SameMapVisibilityTests(unittest.TestCase):
    """同图在线玩家互见：1014 出现 / 1005 走路 / 1010+18 移除（20 格流式）。

    对应 APK 接收端：pmsj.work.main.e.T（1014，属性表直拷进 b/v，
    H(field22) 选精灵族）、原生 1005 的 b/v 分支（m.n 查找 + 逐轴 20 格
    邻近判定）、1010/action=18 的 id>=1_000_000 b/m.p(U) 移除。
    """

    @classmethod
    def setUpClass(cls):
        cls.settings, cls.game = make_game()
        cls.system = cls.game.map_system

    def setUp(self):
        self.pushed: dict[int, list[bytes]] = {}
        self.online: list[dict] = []
        self.system._online_roles_hook = lambda: list(self.online)
        self.system._push_to_role = self._push
        self.system._visible_roles.clear()
        # 58 号图进图会为巡逻 Boss 安排 asyncio 探针任务；单测无事件循环，
        # 统一关闭该分支。
        patcher = mock.patch(
            'systems.map.handler.is_roaming_boss_definition',
            return_value=False,
        )
        patcher.start()
        self.addCleanup(patcher.stop)

    def _push(self, role_id, frames):
        self.pushed.setdefault(int(role_id), []).extend(frames)

    @staticmethod
    def _observer(role_id, name, map_id=58, x=65, y=70, model=2000):
        return {
            'id': role_id,
            'name': name,
            'model': model,
            'map_id': map_id,
            'map_x': x,
            'map_y': y,
        }

    def _entering_role(self, **overrides):
        from systems.role.service import default_role
        role = default_role(self.settings)
        role.update(overrides)
        return role

    def _enter_map(self, role, session):
        fields = [Field(TYPE_INT, 13)]
        return self.system.handle(
            SystemContext(username='tester', active_role=role, session=session),
            1010,
            fields,
        )

    def _move(self, role, x, y):
        fields = [Field(TYPE_INT, x), Field(TYPE_INT, y), Field(TYPE_INT, 0)]
        return self.system.handle(
            SystemContext(username='tester', active_role=role, session={}),
            1005,
            fields,
        )

    def _frames_for(self, frames, message_id):
        decoded = []
        for frame in frames:
            mid, flds = decode_frame(frame)
            if mid == message_id:
                decoded.append(flds)
        return decoded

    def _appear_frames_for(self, frames, actor_id):
        """1014 字段即属性槽：field1=actor id, field3=名字, field4/5=坐标。"""
        return [
            flds for flds in self._frames_for(frames, 1014)
            if int(flds[1].value) == actor_id
        ]

    def test_enter_spawns_nearby_players_to_both_sides(self):
        me = self._entering_role(name='甲', map_x=60, map_y=67)
        other = self._observer(10002, '乙', x=65, y=70)
        self.online.extend([me, other])
        # 甲先进图（乙尚未进图，无帧），乙再进图后双向建立可见性。
        self._enter_map(me, {})
        self.assertEqual(self.pushed.get(10002, []), [])

        self._enter_map(other, {})

        # 乙进图后收到甲的 1014 出现帧（属性槽 1=id, 3=名字, 4/5=坐标, 6=模型）。
        b_view = self._appear_frames_for(self.pushed.get(10002, []), 1_000_000 + 10001)
        self.assertTrue(b_view)
        appear = b_view[0]
        self.assertEqual(str(appear[3].value), '甲')
        self.assertEqual(int(appear[4].value), 60)
        self.assertEqual(int(appear[5].value), 67)
        self.assertEqual(int(appear[6].value), 2000)
        # 甲同样收到乙的 1014 出现帧，且双方视野集合互相登记。
        my_view = self._appear_frames_for(self.pushed.get(10001, []), 1_000_000 + 10002)
        self.assertTrue(my_view)
        self.assertEqual(str(my_view[0][3].value), '乙')
        self.assertEqual(int(my_view[0][4].value), 65)
        self.assertEqual(int(my_view[0][5].value), 70)
        self.assertIn(1_000_000 + 10002, self.system._visible_roles[10001])
        self.assertIn(1_000_000 + 10001, self.system._visible_roles[10002])
        self.assertTrue(self.system.can_players_see_each_other(10001, 10002))

    def test_far_players_do_not_spawn_until_in_range(self):
        me = self._entering_role(name='甲', map_x=60, map_y=67)
        # 乙在 (95,95)：与甲逐轴差 35 > 20，进图后仍不互见。
        far = self._observer(10002, '乙', x=95, y=95)
        self.online.extend([me, far])

        self._enter_map(me, {})
        self._enter_map(far, {})
        self.assertFalse(self.system.can_players_see_each_other(10001, 10002))
        self.assertEqual(self.pushed.get(10002, []), [])
        self.assertEqual(self.pushed.get(10001, []), [])
        self.assertEqual(self.system._visible_roles[10001], set())

        # 甲移动到 (80,80)：与乙逐轴差 15，双向进入视野 → 1014 出现。
        self._move(me, 80, 80)
        self.assertTrue(self._appear_frames_for(self.pushed.get(10002, []), 1_000_000 + 10001))
        self.assertTrue(self._appear_frames_for(self.pushed.get(10001, []), 1_000_000 + 10002))

        # 格内继续移动 → 原生 1005 走路帧。
        self._move(me, 81, 80)
        walks = [
            flds for flds in self._frames_for(self.pushed.get(10002, []), 1005)
            if int(flds[0].value) == 1_000_000 + 10001
        ]
        self.assertTrue(walks)
        self.assertEqual((int(walks[-1][3].value), int(walks[-1][4].value)), (81, 80))

        # 移回远处 → 1010/action=18 移除，视野集合清空。
        self._move(me, 60, 67)
        removals = [
            flds for flds in self._frames_for(self.pushed.get(10002, []), 1010)
            if int(flds[0].value) == 1_000_000 + 10001 and int(flds[5].value) == 18
        ]
        self.assertTrue(removals)
        self.assertNotIn(1_000_000 + 10001, self.system._visible_roles[10002])
        self.assertNotIn(1_000_000 + 10002, self.system._visible_roles[10001])

    def test_movement_broadcasts_native_1005_walk(self):
        me = self._entering_role(name='甲', map_x=60, map_y=67)
        other = self._observer(10002, '乙', x=65, y=70)
        self.online.extend([me, other])
        # 双方进图建立邻近视野，再移动验证走路帧。
        self._enter_map(me, {})
        self._enter_map(other, {})
        self._move(me, 61, 68)

        walks = [
            flds for flds in self._frames_for(self.pushed.get(10002, []), 1005)
            if int(flds[0].value) == 1_000_000 + 10001
        ]
        self.assertTrue(walks)
        walk = walks[-1]
        self.assertEqual(int(walk[3].value), 61)
        self.assertEqual(int(walk[4].value), 68)
        self.assertEqual((int(me['map_x']), int(me['map_y'])), (61, 68))

    def test_following_member_receives_chain_instead_of_leader_walk(self):
        from systems.team.protocol import follow_chain_frame
        me = self._entering_role(name='甲', map_x=60, map_y=67)
        other = self._observer(10002, '乙', x=65, y=70)
        self.online.extend([me, other])
        self._enter_map(me, {})
        self._enter_map(other, {})
        original_hook = self.system._team_movement_frame_hook
        self.addCleanup(setattr, self.system, '_team_movement_frame_hook', original_hook)
        self.system._team_movement_frame_hook = (
            lambda leader, member, x, y: follow_chain_frame(leader, member, [member], x, y)
        )
        self._move(me, 61, 68)
        self.assertEqual(self._frames_for(self.pushed[10002], 1005), [])
        # 跟随链帧 = S→C 1038（e.ai）；1028 在 APK 主分发表中不存在。
        chains = self._frames_for(self.pushed[10002], 1038)
        self.assertEqual(len(chains), 1)
        self.assertEqual([int(field.value) for field in chains[0]],
                         [1_010_001, 0, 0, 61, 68, 1, 10002])

    def test_movement_ignores_receivers_that_never_entered(self):
        me = self._entering_role(name='甲', map_x=60, map_y=67)
        # 乙在线但从未进图（不在 _visible_roles），不向其发送任何可见性帧。
        self.online.append(self._observer(10002, '乙', x=65, y=70))
        self._move(me, 61, 68)
        self.assertEqual(self.pushed.get(10002, []), [])

    def test_departure_broadcasts_action18_removal(self):
        me = self._entering_role(name='甲', map_x=60, map_y=67)
        other = self._observer(10002, '乙', x=65, y=70)
        self.online.extend([me, other])
        self._enter_map(me, {})
        self._enter_map(other, {})

        session = {'map.visible_map_id': 58, 'active_role': me}
        self.system.depart_map(session)

        removals = self._frames_for(self.pushed.get(10002, []), 1010)
        self.assertTrue(removals)
        removal = removals[0]
        self.assertEqual(int(removal[0].value), 1_000_000 + 10001)
        self.assertEqual(int(removal[5].value), 18)
        self.assertNotIn('map.visible_map_id', session)
        self.assertNotIn(10001, self.system._visible_roles)
        self.assertNotIn(1_000_000 + 10001, self.system._visible_roles[10002])

    def test_map_change_removes_from_old_map_and_announces_new(self):
        me = self._entering_role(name='甲', map_x=60, map_y=67)
        old_mapper = self._observer(10002, '乙', map_id=60010, x=60, y=67)
        new_mapper = self._observer(10003, '丙', map_id=58, x=65, y=70)
        self.online.extend([old_mapper, new_mapper])
        # 预置三方均已进图：甲在 60010 看着乙（即将换图），丙已在 58 号图。
        self.system._visible_roles[10001] = {1_000_000 + 10002}
        self.system._visible_roles[10002] = {1_000_000 + 10001}
        self.system._visible_roles[10003] = set()

        # 甲上次公告在 60010（传送/换图前的旧图），本次进 58 号图。
        session = {'map.visible_map_id': 60010}
        result = self._enter_map(me, session)

        self.assertTrue(result.handled)
        removals = [
            flds for flds in self._frames_for(self.pushed.get(10002, []), 1010)
            if int(flds[0].value) == 1_000_000 + 10001 and int(flds[5].value) == 18
        ]
        self.assertTrue(removals)
        arrivals = self._appear_frames_for(self.pushed.get(10003, []), 1_000_000 + 10001)
        self.assertTrue(arrivals)
        my_view = self._appear_frames_for(self.pushed.get(10001, []), 1_000_000 + 10003)
        self.assertTrue(my_view)
        self.assertEqual(session['map.visible_map_id'], 58)
        # 旧图乙的视野集合已剔除甲；甲的新视野只含新图的丙。
        self.assertNotIn(1_000_000 + 10001, self.system._visible_roles[10002])
        self.assertEqual(self.system._visible_roles[10001], {1_000_000 + 10003})

    def test_equipment_change_broadcasts_targeted_1017(self):
        me = self._entering_role(name='甲', map_x=60, map_y=67)
        other = self._observer(10002, '乙', x=65, y=70)
        self.online.extend([me, other])
        self._enter_map(me, {})
        self._enter_map(other, {})
        self.pushed.clear()

        self.system.broadcast_player_appearance(me)

        # 乙收到以甲的地图对象 id 为目标的 1017 外观刷新帧。
        refreshes = [
            flds for flds in self._frames_for(self.pushed.get(10002, []), 1017)
            if int(flds[1].value) == 1_000_000 + 10001
        ]
        self.assertTrue(refreshes)
        refresh = refreshes[0]
        self.assertEqual(int(refresh[0].value), 0)  # 更新子类型
        pair_count = int(refresh[2].value)
        self.assertEqual((len(refresh) - 3) // 2, pair_count)
        # 甲自身不再收到以自己 actor id 为目标的 1017（自身刷新走原总线）。
        self.assertEqual([
            flds for flds in self._frames_for(self.pushed.get(10001, []), 1017)
            if int(flds[1].value) == 1_000_000 + 10001
        ], [])

    def test_appearance_broadcast_skips_out_of_view_clients(self):
        me = self._entering_role(name='甲', map_x=60, map_y=67)
        near = self._observer(10002, '乙', x=65, y=70)
        far = self._observer(10003, '丙', x=95, y=95)
        self.online.extend([me, near, far])
        self._enter_map(me, {})
        self._enter_map(near, {})
        self._enter_map(far, {})
        self.pushed.clear()

        self.system.broadcast_player_appearance(me)

        self.assertTrue([
            flds for flds in self._frames_for(self.pushed.get(10002, []), 1017)
            if int(flds[1].value) == 1_000_000 + 10001
        ])
        # 丙视野里没有甲（超出 20 格），不收帧。
        self.assertEqual([
            flds for flds in self._frames_for(self.pushed.get(10003, []), 1017)
            if int(flds[1].value) == 1_000_000 + 10001
        ], [])

    def test_bus_publish_triggers_appearance_broadcast(self):
        from systems.role.events import CharacterUpdateEvent
        me = self._entering_role(name='甲', map_x=60, map_y=67)
        other = self._observer(10002, '乙', x=65, y=70)
        self.online.extend([me, other])
        self._enter_map(me, {})
        self._enter_map(other, {})
        self.pushed.clear()

        result = self.game.character_update_bus.publish(
            CharacterUpdateEvent.EQUIPMENT_CHANGED,
            role=me,
            registry=self.settings.item_registry,
        )
        self.assertTrue(result.frames)

        refreshes = [
            flds for flds in self._frames_for(self.pushed.get(10002, []), 1017)
            if int(flds[1].value) == 1_000_000 + 10001
        ]
        self.assertTrue(refreshes)


    def test_character_appearance_includes_helmet_property20(self):
        from systems.role.protocol import character_appearance
        role = self._entering_role(name='甲')
        registry = self.settings.item_registry
        self.assertEqual(character_appearance(role, registry).get(20, 0), 0)

        # 穿上 icon 102 的头盔（helmet_appearance_mapping: 102 -> 3）。
        role['items'].append({
            'id': 999001,
            'template_id': 10001021,
            'icon_code': 102,
            'location': 'equipped',
            'equipment_slot': 1,
        })
        self.assertEqual(character_appearance(role, registry).get(20), 3)

    def test_appearance_broadcast_includes_mount_property22(self):
        me = self._entering_role(name='甲', map_x=60, map_y=67)
        other = self._observer(10002, '乙', x=65, y=70)
        self.online.extend([me, other])
        self._enter_map(me, {})
        self._enter_map(other, {})
        self.pushed.clear()

        with mock.patch(
            'systems.map.handler.mount_ride_code_for_role',
            return_value=12345,
        ):
            self.system.broadcast_player_appearance(me)

        refreshes = [
            flds for flds in self._frames_for(self.pushed.get(10002, []), 1017)
            if int(flds[1].value) == 1_000_000 + 10001
        ]
        self.assertTrue(refreshes)
        refresh = refreshes[0]
        pairs = {
            int(refresh[3 + i * 2].value): int(refresh[4 + i * 2].value)
            for i in range(int(refresh[2].value))
        }
        self.assertEqual(pairs.get(22), 12345)


if __name__ == '__main__':
    unittest.main()
