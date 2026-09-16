"""The team router owns every 1023 action and keeps both clients in sync."""
from __future__ import annotations

import unittest

from app.context import SystemContext
from protocol import decode_frame, integer, short
from systems.map.protocol import player_actor_object_id
from systems.role.service import default_role

import server


class TeamSystemTests(unittest.TestCase):
    def setUp(self):
        self.settings = server.Settings.load(server.Path(__file__).resolve().parent.parent / 'config.json')
        self.alice = default_role(self.settings)
        self.bob = default_role(self.settings)
        self.alice.update(id=10001, name='甲')
        self.bob.update(id=10002, name='乙')
        self.roles = {10001: self.alice, 10002: self.bob}
        self.online = {10001, 10002}
        self.pushed = {10001: [], 10002: []}
        from systems.team.handler import TeamSystem
        self.team = TeamSystem(
            self.settings,
            find_role=self.roles.get,
            online_role_ids=lambda: set(self.online),
            push_to_role=lambda role_id, frames: self.pushed[role_id].extend(frames),
            can_follow=lambda leader_id, member_id: True,
        )

    def send(self, role, action, peer=None):
        fields = [short(action)]
        if peer is not None:
            fields.append(integer(peer))
        return self.team.handle(SystemContext(str(role['name']), role, {}), 1023, fields)

    def decoded(self, role_id):
        return [decode_frame(frame) for frame in self.pushed[role_id]]

    def test_invite_accept_syncs_both_rosters_without_map_ui_frames(self):
        created = self.send(self.alice, 0, 10001)
        from systems.role.protocol import role_property_fields
        props = role_property_fields(self.settings, self.alice)
        roster = [fields for mid, fields in (decode_frame(frame) for frame in created.frames)
                  if mid == 1026][0]
        # e.aj 把 fields[2:] 作为 aa.a 一行：
        # [名字, id, mp当前, hp当前, 门派, 等级, mp上限, hp上限, 标志]
        row = roster[2:]
        self.assertEqual(str(row[0].value), '甲')
        self.assertEqual(int(row[1].value), 10001)
        self.assertEqual([field.value for field in row[2:4]],
                         [props[42].value, props[40].value])
        self.assertEqual([field.value for field in row[4:6]],
                         [props[12].value, props[11].value])
        self.assertEqual([field.value for field in row[6:8]],
                         [props[42].value, props[40].value])
        self.assertEqual(int(row[8].value), 0)
        self.send(self.alice, 2, player_actor_object_id(10002))
        self.pushed = {10001: [], 10002: []}
        self.send(self.bob, 3, 10001)
        self.assertEqual(self.team.registry.team_of(10002).members, [10001, 10002])
        for role_id, peer_id in ((10001, 10002), (10002, 10001)):
            frames = self.decoded(role_id)
            self.assertFalse(any(message_id == 1023 and fields[0].value == 6
                                 for message_id, fields in frames))
            # 行 id 按 b/m.o 语义定制：他人行 = actor id，自己行 = raw id
            entry = player_actor_object_id(peer_id) if peer_id != role_id else peer_id
            self.assertTrue(any(message_id == 1026 and int(fields[3].value) == entry
                                for message_id, fields in frames))
        member_ids = [message_id for message_id, _ in self.decoded(10002)]
        # 跟随链帧 = S→C 1038（e.ai）；1028 在 APK 主分发表中不存在。
        self.assertEqual(member_ids.count(1038), 1)
        self.assertLess(max(i for i, message_id in enumerate(member_ids) if message_id == 1026),
                        member_ids.index(1038))
        # 队长客户端同样收到链帧（拖拽本地队员形象）
        self.assertIn(1038, [message_id for message_id, _ in self.decoded(10001)])

    def test_disband_and_disconnect_release_membership(self):
        self.send(self.alice, 0, 10001)
        self.send(self.alice, 2, player_actor_object_id(10002))
        self.send(self.bob, 3, 10001)
        self.team.on_disconnect(10002)
        self.assertIsNone(self.team.registry.team_of(10002))
        self.send(self.alice, 11)
        self.assertIsNone(self.team.registry.team_of(10001))

    def test_member_leave_updates_server_and_both_clients(self):
        self.send(self.alice, 0, 10001)
        self.send(self.alice, 2, player_actor_object_id(10002))
        self.send(self.bob, 3, 10001)
        self.pushed = {10001: [], 10002: []}
        self.send(self.bob, 1, 10002)
        self.assertIsNone(self.team.registry.team_of(10002))
        self.assertEqual(self.team.registry.team_of(10001).members, [10001])
        self.assertTrue(any(message_id == 1023 and fields[0].value == 1
                            for message_id, fields in self.decoded(10001)))

    def test_leader_kick_updates_own_roster_and_target(self):
        self.send(self.alice, 0, 10001)
        self.send(self.alice, 2, player_actor_object_id(10002))
        self.send(self.bob, 3, 10001)
        self.pushed = {10001: [], 10002: []}
        result = self.send(self.alice, 1, 10002)
        self.assertIsNone(self.team.registry.team_of(10002))
        self.assertEqual(self.team.registry.team_of(10001).members, [10001])
        self.assertTrue(any(mid == 1023 and fields[0].value == 1 and fields[1].value == 10002
                            for mid, fields in (decode_frame(frame) for frame in result.frames)))
        self.assertTrue(any(mid == 1023 and fields[0].value == 11
                            for mid, fields in self.decoded(10002)))

    def test_follow_movement_uses_chain_only_for_active_member(self):
        self.send(self.alice, 0, 10001)
        self.send(self.alice, 2, player_actor_object_id(10002))
        self.send(self.bob, 3, 10001)
        frame = self.team.follow_movement_frame(10001, 10002, 30, 35)
        message_id, fields = decode_frame(frame)
        self.assertEqual(message_id, 1038)
        # id 按 b/m.o 语义对接收方定制：链头(队长)=actor id，链员(自己)=raw id
        self.assertEqual([int(field.value) for field in fields],
                         [player_actor_object_id(10001), 0, 0, 30, 35, 1, 10002])
        self.send(self.bob, 18)
        self.assertIsNone(self.team.follow_movement_frame(10001, 10002, 31, 35))
        self.assertIsNone(self.team.follow_movement_frame(10002, 10001, 31, 35))

    def test_leader_promote_reorders_rosters_and_flags(self):
        self.send(self.alice, 0, 10001)
        self.send(self.alice, 2, player_actor_object_id(10002))
        self.pushed = {10001: [], 10002: []}
        self.send(self.bob, 3, 10001)
        self.pushed = {10001: [], 10002: []}
        result = self.send(self.alice, 20, 10002)
        team = self.team.registry.team_of(10002)
        self.assertEqual(team.leader_id, 10002)
        self.assertEqual(team.members, [10002, 10001])
        # 双方都收到 1023/20 重排 + 新旧队长旗
        for role_id in (10001, 10002):
            frames = self.decoded(role_id)
            entry = player_actor_object_id(10002) if role_id != 10002 else 10002
            self.assertTrue(any(mid == 1023 and fields[0].value == 20
                                and int(fields[1].value) == entry
                                for mid, fields in frames))
            flags = [fields for mid, fields in frames if mid == 1017]
            # 新队长旗 prop0=0x40、旧队长旗 prop0=0 都送达每个客户端
            self.assertEqual(len(flags), 2)
        # 新队长的客户端 Z() 旗来源 = 1017 {0:0x40} 指向自己
        self.assertTrue(any(message_id == 1049 for message_id, _ in self.decoded(10002)))

    def test_leader_kick_uses_action_12(self):
        self.send(self.alice, 0, 10001)
        self.send(self.alice, 2, player_actor_object_id(10002))
        self.send(self.bob, 3, 10001)
        self.pushed = {10001: [], 10002: []}
        result = self.send(self.alice, 12, 10002)
        self.assertIsNone(self.team.registry.team_of(10002))
        # 被踢者收 1023/11 清自身状态，留存者收 1023/1 移除行
        self.assertTrue(any(mid == 1023 and fields[0].value == 11
                            for mid, fields in self.decoded(10002)))
        self.assertTrue(any(mid == 1023 and fields[0].value == 1
                            and int(fields[1].value) == player_actor_object_id(10002)
                            for mid, fields in self.decoded(10001)))

    def test_summon_only_targets_away_members(self):
        self.send(self.alice, 0, 10001)
        self.send(self.alice, 2, player_actor_object_id(10002))
        self.send(self.bob, 3, 10001)
        # 未暂离：客户端原生不发，这里直接断言服务端拒绝
        result = self.send(self.alice, 19, 10002)
        self.assertIn('并未暂离', str(decode_frame(result.frames[0])[1][1].value))
        # 暂离后召集 → 状态复位 + 全队链重发
        self.send(self.bob, 18)
        self.pushed = {10001: [], 10002: []}
        result = self.send(self.alice, 19, 10002)
        self.assertNotIn(10002, self.team.registry.team_of(10002).away)
        self.assertTrue(any(mid == 1023 and fields[0].value == 17
                            and int(fields[1].value) == 10002
                            for mid, fields in self.decoded(10002)))
        self.assertTrue(any(mid == 1038 for mid, _ in self.decoded(10002)))

    def test_self_leave_clears_member_flag_and_roster(self):
        self.send(self.alice, 0, 10001)
        self.send(self.alice, 2, player_actor_object_id(10002))
        self.send(self.bob, 3, 10001)
        # 乙已带 0x200000 队员位；离队后应答必须把它清零
        result = self.send(self.bob, 1, 10002)
        flags = [fields for mid, fields in (decode_frame(frame) for frame in result.frames)
                 if mid == 1017]
        self.assertTrue(flags and int(flags[0][4].value) == 0)
        self.assertTrue(any(mid == 1023 and fields[0].value == 11
                            for mid, fields in (decode_frame(frame) for frame in result.frames)))
        self.assertIsNone(self.team.registry.team_of(10002))

    def test_kicked_member_gets_flag_cleared(self):
        self.send(self.alice, 0, 10001)
        self.send(self.alice, 2, player_actor_object_id(10002))
        self.send(self.bob, 3, 10001)
        self.pushed = {10001: [], 10002: []}
        # et 菜单发的是行内条目 id（他人 = actor id）
        self.send(self.alice, 12, player_actor_object_id(10002))
        flags = [fields for mid, fields in self.decoded(10002) if mid == 1017]
        self.assertTrue(flags and int(flags[0][4].value) == 0)
        self.assertTrue(any(mid == 1023 and fields[0].value == 11
                            for mid, fields in self.decoded(10002)))
        # 留存者（队长）收到按其视角定制的移除行（他人=actor id）
        self.assertTrue(any(mid == 1023 and fields[0].value == 1
                            and int(fields[1].value) == player_actor_object_id(10002)
                            for mid, fields in self.decoded(10001)))

    def test_promote_by_actor_id_input_reorders_and_reflags(self):
        self.send(self.alice, 0, 10001)
        self.send(self.alice, 2, player_actor_object_id(10002))
        self.send(self.bob, 3, 10001)
        self.pushed = {10001: [], 10002: []}
        # et 行内条目 id（乙在甲端 = actor id）
        result = self.send(self.alice, 20, player_actor_object_id(10002))
        team = self.team.registry.team_of(10002)
        self.assertEqual(team.leader_id, 10002)
        self.assertEqual(team.members, [10002, 10001])
        for role_id in (10001, 10002):
            frames = self.decoded(role_id)
            entry = player_actor_object_id(10002) if role_id != 10002 else 10002
            self.assertTrue(any(mid == 1023 and fields[0].value == 20
                                and int(fields[1].value) == entry
                                for mid, fields in frames))
            # 新队长旗(0x40)+旧队长降为队员位(0x200000) 都按接收方定制
            flags = [fields for mid, fields in frames if mid == 1017]
            self.assertEqual(len(flags), 2)
            values = {(int(f[1].value), int(f[4].value)) for f in flags}
            new_leader_entry = player_actor_object_id(10002) if role_id != 10002 else 10002
            old_leader_entry = player_actor_object_id(10001) if role_id != 10001 else 10001
            self.assertIn((new_leader_entry, 0x40), values)
            self.assertIn((old_leader_entry, 0x200000), values)

    def test_member_disconnect_removes_roster_row_on_leader(self):
        self.send(self.alice, 0, 10001)
        self.send(self.alice, 2, player_actor_object_id(10002))
        self.send(self.bob, 3, 10001)
        self.pushed = {10001: [], 10002: []}
        self.team.on_disconnect(10002)
        self.assertIsNone(self.team.registry.team_of(10002))
        # 队长收到 1023/1，目标 = 乙的 actor id（甲端行内条目 id）
        self.assertTrue(any(mid == 1023 and fields[0].value == 1
                            and int(fields[1].value) == player_actor_object_id(10002)
                            for mid, fields in self.decoded(10001)))
        # 仅剩队长一人时无跟随者，无需 1038；1023/1 的原生 aa.h()
        # 分支会在队长客户端清掉指向已移除成员的旧链。

    def test_leader_disconnect_disbands_and_clears_member_flags(self):
        self.send(self.alice, 0, 10001)
        self.send(self.alice, 2, player_actor_object_id(10002))
        self.send(self.bob, 3, 10001)
        self.pushed = {10001: [], 10002: []}
        self.team.on_disconnect(10001)
        # 全队解散，乙的 prop0 位被清零
        self.assertIsNone(self.team.registry.team_of(10002))
        frames = self.decoded(10002)
        self.assertTrue(any(mid == 1023 and fields[0].value == 11
                            for mid, fields in frames))
        flags = [fields for mid, fields in frames if mid == 1017]
        self.assertTrue(flags and int(flags[0][4].value) == 0)

    def test_router_has_single_team_owner(self):
        game = server.LocalGameServer(self.settings)
        self.assertEqual(
            sum(1 for route in game.system_router.routes
                if route.predicate(SystemContext('甲', self.alice, {}), 1023, [short(2), integer(10002)])),
            1,
        )
