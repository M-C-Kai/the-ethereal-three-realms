"""帮派系统测试：协议布局、业务规则与帮派管理员 NPC。"""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from app.context import SystemContext
from app.router import SystemRouter
from protocol import (
    TYPE_BYTE,
    TYPE_INT,
    TYPE_SHORT,
    TYPE_STRING,
    Field,
    decode_frame,
)
from systems.gang import GangSystem, register_gang_routes
from systems.gang.registry import (
    GANG_ADMIN_CREATE_OPTION,
    GANG_ADMIN_DISBAND_CONFIRM_OPTION,
    GANG_ADMIN_DISBAND_OPTION,
    GANG_ADMIN_NPC_ID,
    GANG_ADMIN_SERVICE,
    GANG_CREATION_COST_SILVER,
    GANG_POSITION_LEADER,
    GANG_POSITION_MEMBER,
    GANG_POSITION_NONE,
    MAX_GANG_NAME_LENGTH,
)
from systems.map.handler import LocalNpcDialogueState
from systems.role.protocol import player_info
from systems.role.service import default_role

ROOT = Path(__file__).resolve().parent.parent


def _short(value: int) -> Field:
    return Field(TYPE_SHORT, value)


def _byte(value: int) -> Field:
    return Field(TYPE_BYTE, value)


def _int(value: int) -> Field:
    return Field(TYPE_INT, value)


def _string(value: str) -> Field:
    return Field(TYPE_STRING, value)


def _config_settings():
    import server

    return server.Settings.load(server.Path(ROOT) / 'config.json')


class GangSystemTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.store_path = root / 'gangs.json'
        self.settings = _config_settings()
        self.leader = default_role(self.settings)
        self.leader['id'] = 10001
        self.leader['name'] = '帮主甲'
        self.leader['level'] = 10
        self.member = default_role(self.settings)
        self.member['id'] = 10002
        self.member['name'] = '侠客乙'
        self.member['level'] = 5
        self.outsider = default_role(self.settings)
        self.outsider['id'] = 10003
        self.outsider['name'] = '路人丙'
        self.outsider['level'] = 3
        self.roles_by_id = {
            int(role['id']): role
            for role in (self.leader, self.member, self.outsider)
        }
        self.save_count = 0
        self.notifications: list[tuple[int, tuple[bytes, ...]]] = []
        self.system = GangSystem(
            self.store_path,
            self.save_roles,
            lambda role_id: self.roles_by_id.get(int(role_id)),
            online_check=lambda role_id: int(role_id) in (int(self.member['id']), int(self.outsider['id'])),
            notifier=lambda role_id, frames: self.notifications.append((role_id, frames)),
        )
        self.router = SystemRouter()
        register_gang_routes(self.router, self.system)

    def save_roles(self):
        self.save_count += 1

    def dispatch(self, message_id, fields, role):
        return self.router.dispatch(
            SystemContext(username='tester', active_role=role),
            message_id,
            fields,
        )

    # ------------------------------------------------------------------
    # catalog and list

    def test_seeds_gang_catalog_and_serves_1136_list(self):
        self.assertTrue(self.store_path.exists())
        result = self.dispatch(1136, [_byte(1), _byte(0), _byte(0)], self.outsider)
        self.assertTrue(result.handled)
        self.assertEqual(len(result.frames), 1)
        message_id, fields = decode_frame(result.frames[0])
        self.assertEqual(message_id, 1136)
        self.assertEqual(fields[0].value, 1)
        count = fields[2].value
        self.assertGreaterEqual(count, 1)
        stride = (len(fields) - 3) // count
        first = fields[3:3 + stride]
        self.assertEqual(first[1].type_id, TYPE_STRING)  # 帮派名

    def test_apply_to_leaderless_seed_becomes_leader(self):
        result = self.dispatch(1107, [_short(0x1B), _int(2001)], self.leader)
        self.assertTrue(result.handled)
        self.assertEqual(result.reason, 'joined_as_leader')
        self.assertEqual(self.system.service.role_position(self.leader), GANG_POSITION_LEADER)
        self.assertEqual(self.system.service.role_gang_id(self.leader), 2001)
        self.assertGreater(self.save_count, 0)
        # 1017 职位推送 + 帮派信息，两条都发给申请者自己的连接
        self.assertEqual(len(result.frames), 2)
        message_id, fields = decode_frame(result.frames[0])
        self.assertEqual(message_id, 1017)
        self.assertEqual([f.value for f in fields], [0, 10001, 1, 21, GANG_POSITION_LEADER])

    # ------------------------------------------------------------------
    # info layout consumed by e/ed fixed indexes

    def test_gang_info_frame_layout_matches_client_indexes(self):
        self.dispatch(1107, [_short(0x1B), _int(2001)], self.leader)
        result = self.dispatch(1107, [_short(0xB), _int(0)], self.leader)
        self.assertTrue(result.handled)
        message_id, fields = decode_frame(result.frames[0])
        self.assertEqual(message_id, 1107)
        self.assertEqual(fields[0].value, 0xB)
        self.assertEqual(fields[1].value, 2001)
        self.assertEqual(fields[2].value, '天罡盟')  # e/ed.V = 2 帮派名
        self.assertEqual(fields[3].value, 10001)  # e/ed.W = 3 帮主id
        self.assertEqual(fields[4].value, '帮主甲')  # e/ed.X = 4 帮主名
        self.assertEqual(fields[5].value, 1)  # e/ed.Y = 5 成员数
        self.assertEqual(fields[8].value, '替天行道，护佑苍生')  # e/ed.ab = 8 宗旨

    def test_gang_list_request_via_1107_sub_b_for_other_gang(self):
        result = self.dispatch(1107, [_short(0xB), _int(2002)], self.outsider)
        self.assertTrue(result.handled)
        message_id, fields = decode_frame(result.frames[0])
        self.assertEqual(message_id, 1107)
        self.assertEqual(fields[0].value, 0xB)
        self.assertEqual(fields[1].value, 2002)

    # ------------------------------------------------------------------
    # invite flow

    def test_invite_pushes_dialog_and_accept_adds_member(self):
        self.dispatch(1107, [_short(0x1B), _int(2001)], self.leader)
        result = self.dispatch(1107, [_short(0x1D), _int(10002)], self.leader)
        self.assertEqual(result.reason, 'invited')
        self.assertEqual(len(self.notifications), 1)
        target_id, frames = self.notifications[0]
        self.assertEqual(target_id, 10002)
        message_id, fields = decode_frame(frames[0])
        self.assertEqual(message_id, 1107)
        self.assertEqual(fields[0].value, 0x1D)  # 邀请弹窗
        self.assertEqual(fields[1].value, 10001)
        self.assertEqual(fields[2].value, '帮主甲')
        self.assertEqual(fields[3].value, '天罡盟')

        accept = self.system.service.handle_message(
            1107,
            [_short(0x1E), _int(10001)],
            self.member,
        )
        self.assertEqual(accept.reason, 'invite_accepted')
        self.assertEqual(self.system.service.role_position(self.member), GANG_POSITION_MEMBER)
        # joiner 的 1017 职位推送走自己的回复通道
        message_id, fields = decode_frame(accept.replies[0])
        self.assertEqual(message_id, 1017)
        self.assertEqual([f.value for f in fields], [0, 10002, 1, 21, GANG_POSITION_MEMBER])

    def test_reject_invite_clears_pending(self):
        self.dispatch(1107, [_short(0x1B), _int(2001)], self.leader)
        self.dispatch(1107, [_short(0x1D), _int(10002)], self.leader)
        result = self.system.service.handle_message(
            1107,
            [_short(0x19), _int(10001)],
            self.member,
        )
        self.assertEqual(result.reason, 'invite_rejected')
        self.assertNotIn(10002, self.system.service.store.pending_invites)

    # ------------------------------------------------------------------
    # application flow

    def test_application_flow_accept_and_reject(self):
        self.dispatch(1107, [_short(0x1B), _int(2001)], self.leader)
        applied = self.dispatch(1107, [_short(0x1B), _int(2001)], self.outsider)
        self.assertEqual(applied.reason, 'applied')

        listing = self.dispatch(1140, [_byte(1), _byte(0), _byte(0)], self.leader)
        message_id, fields = decode_frame(listing.frames[0])
        self.assertEqual(message_id, 1140)
        self.assertEqual(fields[0].value, 1)
        self.assertEqual(fields[2].value, 1)
        self.assertEqual(fields[3].value, 10003)
        self.assertEqual(fields[4].value, '路人丙')

        accepted = self.dispatch(1107, [_short(0x1C), _int(10003)], self.leader)
        self.assertEqual(accepted.reason, 'application_accepted')
        self.assertEqual(self.system.service.role_position(self.outsider), GANG_POSITION_MEMBER)

    def test_reject_application_refreshes_1140(self):
        self.dispatch(1107, [_short(0x1B), _int(2001)], self.leader)
        self.dispatch(1107, [_short(0x1B), _int(2001)], self.outsider)
        result = self.dispatch(1107, [_short(0x1A), _int(10003)], self.leader)
        self.assertEqual(result.reason, 'rejected')
        message_id, fields = decode_frame(result.frames[0])
        self.assertEqual(message_id, 1140)
        self.assertEqual(fields[2].value, 0)

    def test_application_list_requires_leader(self):
        self.dispatch(1107, [_short(0x1B), _int(2001)], self.leader)
        self.dispatch(1107, [_short(0x1B), _int(2001)], self.outsider)
        self.dispatch(1107, [_short(0x1C), _int(10003)], self.leader)
        result = self.dispatch(1140, [_byte(1), _byte(0), _byte(0)], self.outsider)
        self.assertTrue(result.handled)
        message_id, fields = decode_frame(result.frames[0])
        self.assertEqual(fields[2].value, 0)  # 空列表而非报错

    # ------------------------------------------------------------------
    # member list and detail

    def test_member_list_and_detail_layout(self):
        self.dispatch(1107, [_short(0x1B), _int(2001)], self.leader)
        self.dispatch(1107, [_short(0x1B), _int(2001)], self.outsider)
        self.dispatch(1107, [_short(0x1C), _int(10003)], self.leader)

        listing = self.dispatch(1137, [_byte(1), _byte(0), _byte(0)], self.leader)
        message_id, fields = decode_frame(listing.frames[0])
        self.assertEqual(message_id, 1137)
        self.assertEqual(fields[0].value, 1)
        self.assertEqual(fields[2].value, 2)
        # leader first (position 1000 sorts before 200)
        self.assertEqual(fields[3].value, 10001)
        self.assertEqual(fields[4].value, '帮主甲')
        self.assertEqual(fields[5].value, GANG_POSITION_LEADER)
        self.assertEqual(fields[6].value, '10')  # 等级以字符串下发
        self.assertEqual(fields[7].value, 0)  # leader 离线

        detail = self.dispatch(1137, [_byte(2), _int(10003)], self.leader)
        message_id, fields = decode_frame(detail.frames[0])
        self.assertEqual(message_id, 1137)
        self.assertEqual(fields[0].value, 2)
        self.assertEqual(fields[1].value, '路人丙')  # ee d[0] 名称
        self.assertGreater(fields[6].value, 20000101)  # ee d[5] 入帮时间 YYYYMMDD
        self.assertEqual(fields[7].value, GANG_POSITION_MEMBER)  # ee d[6] 职务
        self.assertEqual(fields[8].value, '0')  # ee d[7] 贡献

    # ------------------------------------------------------------------
    # leader mutations

    def test_kick_member_notifies_target(self):
        self.dispatch(1107, [_short(0x1B), _int(2001)], self.leader)
        self.dispatch(1107, [_short(0x1B), _int(2001)], self.outsider)
        self.dispatch(1107, [_short(0x1C), _int(10003)], self.leader)
        self.notifications.clear()  # 忽略入帮时的职位推送，聚焦踢人通知
        result = self.dispatch(
            1107,
            [_short(0x4), _byte(0), _byte(0), _int(10003)],
            self.leader,
        )
        self.assertEqual(result.reason, 'kicked')
        self.assertNotEqual(self.system.service.role_gang_id(self.outsider), 2001)
        self.assertEqual(len(self.notifications), 1)
        target_id, frames = self.notifications[0]
        self.assertEqual(target_id, 10003)
        message_id, fields = decode_frame(frames[1])
        self.assertEqual(message_id, 1107)
        self.assertEqual(fields[0].value, 0x4)  # 关闭帮派界面的推送

    def test_kick_requires_leader(self):
        self.dispatch(1107, [_short(0x1B), _int(2001)], self.leader)
        self.dispatch(1107, [_short(0x1B), _int(2001)], self.outsider)
        self.dispatch(1107, [_short(0x1C), _int(10003)], self.leader)
        result = self.dispatch(1107, [_short(0x4), _byte(0), _byte(0), _int(10001)], self.outsider)
        self.assertEqual(result.reason, 'not_leader')

    def test_abdicate_swaps_positions(self):
        self.dispatch(1107, [_short(0x1B), _int(2001)], self.leader)
        self.dispatch(1107, [_short(0x1B), _int(2001)], self.outsider)
        self.dispatch(1107, [_short(0x1C), _int(10003)], self.leader)
        result = self.dispatch(1107, [_short(0x10), _int(10003)], self.leader)
        self.assertEqual(result.reason, 'abdicated')
        self.assertEqual(self.system.service.role_position(self.leader), GANG_POSITION_MEMBER)
        self.assertEqual(self.system.service.role_position(self.outsider), GANG_POSITION_LEADER)
        # 原帮主的职位更新走自己的回复通道，继任者走 notifier 通知通道
        message_id, fields = decode_frame(result.frames[0])
        self.assertEqual(message_id, 1017)
        self.assertEqual(fields[4].value, GANG_POSITION_MEMBER)
        pushed_ids = {rid for rid, _ in self.notifications}
        self.assertEqual(pushed_ids, {10003})

    def test_modify_motto_leader_only(self):
        self.dispatch(1107, [_short(0x1B), _int(2001)], self.leader)
        result = self.dispatch(1107, [_short(0x1F), _string('  新的宗旨  ')], self.leader)
        self.assertEqual(result.reason, 'motto_changed')
        gang = self.system.service.store.gangs[2001]
        self.assertEqual(gang.motto, '新的宗旨')

    def test_leave_gang_resets_role_and_closes_screens(self):
        self.dispatch(1107, [_short(0x1B), _int(2001)], self.leader)
        self.dispatch(1107, [_short(0x1B), _int(2001)], self.outsider)
        self.dispatch(1107, [_short(0x1C), _int(10003)], self.leader)
        result = self.dispatch(1107, [_short(0x3)], self.outsider)
        self.assertEqual(result.reason, 'left')
        self.assertEqual(self.system.service.role_gang_id(self.outsider), 0)
        self.assertNotIn('gang_position', self.outsider)
        message_id, fields = decode_frame(result.frames[1])
        self.assertEqual(message_id, 1107)
        self.assertEqual(fields[0].value, 0x3)

    # ------------------------------------------------------------------
    # 1006 login table

    def test_player_info_publishes_gang_position_slot_21(self):
        self.leader['gang_position'] = GANG_POSITION_LEADER
        frame = player_info(self.settings, self.leader)
        message_id, fields = decode_frame(frame)
        self.assertEqual(message_id, 1006)
        self.assertEqual(fields[1 + 21].value, GANG_POSITION_LEADER)
        self.leader['gang_position'] = GANG_POSITION_NONE
        frame = player_info(self.settings, self.leader)
        _, fields = decode_frame(frame)
        self.assertEqual(fields[1 + 21].value, GANG_POSITION_NONE)

    # ------------------------------------------------------------------
    # dispatch hygiene

    def test_router_consumes_all_gang_message_ids_without_falling_through(self):
        for message_id in (1107, 1136, 1137, 1140):
            result = self.dispatch(message_id, [_byte(0)], self.leader)
            self.assertTrue(result.handled, message_id)

    def test_handle_requires_active_role(self):
        result = self.router.dispatch(
            SystemContext(username='tester', active_role=None),
            1136,
            [_byte(1), _byte(0), _byte(0)],
        )
        self.assertTrue(result.handled)
        self.assertEqual(result.reason, 'no_active_role')

    def test_persistence_roundtrip(self):
        self.dispatch(1107, [_short(0x1B), _int(2001)], self.leader)
        self.dispatch(1107, [_short(0x1F), _string(' Persisted ')], self.leader)
        rebuilt = GangSystem(
            self.store_path,
            self.save_roles,
            lambda role_id: self.roles_by_id.get(int(role_id)),
        )
        gang = rebuilt.service.store.gangs[2001]
        self.assertEqual(gang.motto, 'Persisted')
        self.assertIn(10001, gang.members)
        self.assertEqual(gang.members[10001].position, GANG_POSITION_LEADER)


class GangAdminNpcTests(unittest.TestCase):
    """帮派管理员 NPC（长安 12,68，外观 96020，service=gang_admin）。"""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.settings = _config_settings()
        self.role = default_role(self.settings)
        self.role['map_id'] = 58
        self.roles_by_id = {int(self.role['id']): self.role}
        self.online_ids: set[int] = set()
        self.pushed: list[tuple[int, tuple[bytes, ...]]] = []
        self.system = GangSystem(
            root / 'gangs.json',
            lambda: None,
            lambda role_id: self.roles_by_id.get(int(role_id)),
            online_check=lambda role_id: int(role_id) in self.online_ids,
            notifier=lambda role_id, frames: self.pushed.append((role_id, frames)),
        )

    def _admin_npc(self):
        definition = self.settings.map_registry.require(58)
        npcs = [npc for npc in definition.npcs if npc.service == GANG_ADMIN_SERVICE]
        self.assertEqual(len(npcs), 1)
        return npcs[0]

    def test_map_58_declares_gang_admin_npc(self):
        npc = self._admin_npc()
        self.assertEqual(npc.id, GANG_ADMIN_NPC_ID)
        self.assertEqual(npc.name, '帮派管理员')
        self.assertEqual(npc.dat_id, 96020)
        self.assertEqual((npc.x, npc.y), (12, 68))

    def test_dialogue_offers_create_option_for_gangless_player(self):
        npc = self._admin_npc()
        frames = self.system.npc_dialogue_frames(npc, self.role, self.settings)
        self.assertIsNotNone(frames)
        message_id, fields = decode_frame(frames[0])
        self.assertEqual(message_id, 2032)
        self.assertEqual(fields[0].value, GANG_ADMIN_NPC_ID)
        record_count = fields[1].value
        self.assertEqual(record_count, 4)  # 介绍 + 创建选项 + 结束对话 + 100布局帧
        values = [field.value for field in fields[2:]]
        stride = 8
        option_rows = [
            values[start:start + stride]
            for start in range(0, len(values), stride)
        ]
        create_row = option_rows[1]
        # kind 3 记录：客户端原生输入框，short 字段 = 名称最大长度
        self.assertEqual(create_row[5], 3)
        self.assertEqual(create_row[3], MAX_GANG_NAME_LENGTH)
        self.assertEqual(create_row[4], GANG_ADMIN_CREATE_OPTION)  # option id
        self.assertIn('创建帮派', create_row[6])

    def test_dialogue_offers_disband_option_for_leader(self):
        npc = self._admin_npc()
        self.role['gang_id'] = 2001
        self.role['gang_position'] = GANG_POSITION_LEADER
        frames = self.system.npc_dialogue_frames(npc, self.role, self.settings)
        _, fields = decode_frame(frames[0])
        values = [field.value for field in fields[2:]]
        rows = [values[start:start + 8] for start in range(0, len(values), 8)]
        disband_row = rows[1]
        self.assertEqual(disband_row[5], 2)  # kind 2 普通选项（无输入框）
        self.assertEqual(disband_row[4], GANG_ADMIN_DISBAND_OPTION)
        self.assertIn('解散帮派', disband_row[6])
        option_ids = [row[4] for row in rows]
        self.assertNotIn(GANG_ADMIN_CREATE_OPTION, option_ids)

    def test_dialogue_hides_create_option_for_gang_member(self):
        npc = self._admin_npc()
        self.role['gang_id'] = 2001
        self.role['gang_position'] = GANG_POSITION_MEMBER
        frames = self.system.npc_dialogue_frames(npc, self.role, self.settings)
        message_id, fields = decode_frame(frames[0])
        self.assertEqual(fields[1].value, 3)  # 介绍 + 结束对话 + 100布局帧
        values = [field.value for field in fields[2:]]
        option_ids = [values[start + 4] for start in range(0, len(values), 8)]
        self.assertNotIn(GANG_ADMIN_CREATE_OPTION, option_ids)
        self.assertNotIn(GANG_ADMIN_DISBAND_OPTION, option_ids)

    def test_dialogue_returns_none_for_other_services(self):
        definition = self.settings.map_registry.require(58)
        other = next(npc for npc in definition.npcs if npc.service != GANG_ADMIN_SERVICE)
        self.assertIsNone(self.system.npc_dialogue_frames(other, self.role, self.settings))

    def test_create_gang_via_npc_option(self):
        npc = self._admin_npc()
        state = LocalNpcDialogueState()
        state.select(58, npc.id)
        silver_before = int(self.role['currencies']['silver'])
        frames = self.system.npc_dialogue_option(
            self.settings, self.role, state, GANG_ADMIN_CREATE_OPTION, input_text='傲世盟',
        )
        self.assertIsNotNone(frames)
        self.assertIsNone(state.npc_id)  # 对话状态已消费
        self.assertEqual([decode_frame(frame)[0] for frame in frames], [1010, 1049, 1017])
        # ack + 顶部提示 + 1017 职位/银两更新
        self.assertEqual(len(frames), 3)
        top_id, top_fields = decode_frame(frames[1])
        self.assertEqual(top_id, 1049)
        self.assertIn('创建成功', top_fields[1].value)
        prop_id, prop_fields = decode_frame(frames[2])
        self.assertEqual(prop_id, 1017)
        self.assertEqual([f.value for f in prop_fields], [
            0, int(self.role['id']), 2, 21, GANG_POSITION_LEADER, 50, silver_before - GANG_CREATION_COST_SILVER,
        ])
        self.assertEqual(self.system.service.role_position(self.role), GANG_POSITION_LEADER)
        gang_id = self.system.service.role_gang_id(self.role)
        gang = self.system.service.store.gangs[gang_id]
        self.assertEqual(gang.name, '傲世盟')  # 使用玩家输入的名称
        self.assertEqual(gang.funds, GANG_CREATION_COST_SILVER)

    def test_create_gang_requires_name_input(self):
        npc = self._admin_npc()
        state = LocalNpcDialogueState()
        state.select(58, npc.id)
        frames = self.system.npc_dialogue_option(
            self.settings, self.role, state, GANG_ADMIN_CREATE_OPTION, input_text='   ',
        )
        self.assertEqual(len(frames), 2)
        _, top_fields = decode_frame(frames[1])
        self.assertIn('帮派名称', top_fields[1].value)
        self.assertNotIn('gang_position', self.role)
        self.assertIsNone(state.npc_id)

    def test_create_gang_name_too_long(self):
        npc = self._admin_npc()
        state = LocalNpcDialogueState()
        state.select(58, npc.id)
        frames = self.system.npc_dialogue_option(
            self.settings, self.role, state, GANG_ADMIN_CREATE_OPTION, input_text='这个帮派名字实在是太长了呀',
        )
        _, top_fields = decode_frame(frames[1])
        self.assertIn('1-12', top_fields[1].value)
        self.assertNotIn('gang_position', self.role)

    def test_create_gang_insufficient_silver(self):
        npc = self._admin_npc()
        self.role['currencies']['silver'] = GANG_CREATION_COST_SILVER - 1
        state = LocalNpcDialogueState()
        state.select(58, npc.id)
        next_gang_id_before = self.system.service.store.next_gang_id
        frames = self.system.npc_dialogue_option(
            self.settings, self.role, state, GANG_ADMIN_CREATE_OPTION, input_text='散财盟',
        )
        self.assertEqual(len(frames), 2)
        _, top_fields = decode_frame(frames[1])
        self.assertIn('银两不足', top_fields[1].value)
        self.assertNotIn('gang_position', self.role)
        self.assertEqual(self.system.service.store.next_gang_id, next_gang_id_before)  # 无新帮派

    def test_create_gang_rejects_existing_member(self):
        npc = self._admin_npc()
        self.role['gang_id'] = 2001
        self.role['gang_position'] = GANG_POSITION_MEMBER
        state = LocalNpcDialogueState()
        state.select(58, npc.id)
        frames = self.system.npc_dialogue_option(
            self.settings, self.role, state, GANG_ADMIN_CREATE_OPTION, input_text='再建一帮',
        )
        _, top_fields = decode_frame(frames[1])
        self.assertIn('已有帮派', top_fields[1].value)

    def test_create_gang_rejects_duplicate_name(self):
        result = self.system.service.create_gang(self.role, name='天罡盟')
        self.assertEqual(result.reason, 'name_taken')

    def test_option_passthrough_for_other_options_and_npcs(self):
        npc = self._admin_npc()
        state = LocalNpcDialogueState()
        state.select(58, npc.id)
        # 0 = 结束对话：交回地图默认 ACK
        self.assertIsNone(
            self.system.npc_dialogue_option(self.settings, self.role, state, 0)
        )
        self.assertEqual(state.npc_id, npc.id)  # 未消费

    # ------------------------------------------------------------------
    # 解散帮派（两步确认）

    def _make_leader_with_gang(self):
        """帮主经创建流程拿到一个真实帮派，外加一名在线帮众成员。"""
        npc = self._admin_npc()
        state = LocalNpcDialogueState()
        state.select(58, npc.id)
        self.system.npc_dialogue_option(
            self.settings, self.role, state, GANG_ADMIN_CREATE_OPTION, input_text='傲世盟',
        )
        member = default_role(self.settings)
        member['id'] = 20002
        member['name'] = '帮众丁'
        self.roles_by_id[int(member['id'])] = member
        self.online_ids.add(int(member['id']))
        self.system.service._join(
            member,
            self.system.service.store.gangs[self.system.service.role_gang_id(self.role)],
            GANG_POSITION_MEMBER,
            'invite_accepted',
        )
        self.pushed.clear()  # 忽略建帮/入帮推送，聚焦解散通知
        return member

    def test_disband_offers_confirm_dialogue(self):
        self._make_leader_with_gang()
        npc = self._admin_npc()
        state = LocalNpcDialogueState()
        state.select(58, npc.id)
        frames = self.system.npc_dialogue_option(
            self.settings, self.role, state, GANG_ADMIN_DISBAND_OPTION,
        )
        # ack + 重新打开的确认对话（2032）
        self.assertEqual([decode_frame(frame)[0] for frame in frames], [1010, 2032])
        self.assertIsNotNone(state.npc_id)  # 确认期间对话状态保持选中
        _, fields = decode_frame(frames[1])
        values = [field.value for field in fields[2:]]
        rows = [values[start:start + 8] for start in range(0, len(values), 8)]
        self.assertIn('确定要解散帮派', rows[0][6])
        self.assertIn('傲世盟', rows[0][6])
        self.assertEqual(rows[1][4], GANG_ADMIN_DISBAND_CONFIRM_OPTION)
        confirm_row_text = rows[1][6]
        self.assertIn('确认解散', confirm_row_text)
        option_ids = [row[4] for row in rows]
        self.assertIn(0, option_ids)  # 再想想

    def test_disband_confirm_removes_gang_and_cleans_members(self):
        member = self._make_leader_with_gang()
        npc = self._admin_npc()
        state = LocalNpcDialogueState()
        state.select(58, npc.id)
        self.system.npc_dialogue_option(self.settings, self.role, state, GANG_ADMIN_DISBAND_OPTION)
        frames = self.system.npc_dialogue_option(
            self.settings, self.role, state, GANG_ADMIN_DISBAND_CONFIRM_OPTION,
        )
        self.assertIsNone(state.npc_id)
        self.assertEqual([decode_frame(frame)[0] for frame in frames], [1010, 1049, 1017])
        _, top_fields = decode_frame(frames[1])
        self.assertIn('帮派已解散', top_fields[1].value)
        prop_id, prop_fields = decode_frame(frames[2])
        self.assertEqual(prop_id, 1017)
        self.assertEqual([f.value for f in prop_fields], [0, int(self.role['id']), 1, 21, GANG_POSITION_NONE])
        # 帮派已从目录移除，帮主与帮众的角色状态全部清理
        self.assertEqual(self.system.service.role_gang_id(self.role), 0)
        self.assertNotIn('gang_position', self.role)
        self.assertEqual(self.system.service.role_gang_id(member), 0)
        self.assertNotIn('gang_position', member)
        self.assertTrue(all(gang.name != '傲世盟' for gang in self.system.service.store.gangs.values()))
        # 在线帮众收到职位重置与界面关闭推送
        self.assertEqual(len(self.pushed), 1)
        target_id, pushed = self.pushed[0]
        self.assertEqual(target_id, int(member['id']))
        self.assertEqual([decode_frame(frame)[0] for frame in pushed], [1017, 1107])

    def test_disband_requires_leader(self):
        member = self._make_leader_with_gang()
        npc = self._admin_npc()
        state = LocalNpcDialogueState()
        state.select(58, npc.id)
        frames = self.system.npc_dialogue_option(
            self.settings, member, state, GANG_ADMIN_DISBAND_OPTION,
        )
        # 帮众的对话里没有解散选项（handler 直接回 ACK+提示）
        self.assertEqual([decode_frame(frame)[0] for frame in frames], [1010, 1049])
        _, top_fields = decode_frame(frames[1])
        self.assertIn('只有帮主', top_fields[1].value)
        gang_id = self.system.service.role_gang_id(self.role)
        self.assertIn(gang_id, self.system.service.store.gangs)  # 帮派未受影响

    def test_disband_cancel_keeps_gang(self):
        self._make_leader_with_gang()
        npc = self._admin_npc()
        state = LocalNpcDialogueState()
        state.select(58, npc.id)
        self.system.npc_dialogue_option(self.settings, self.role, state, GANG_ADMIN_DISBAND_OPTION)
        # 取消：option 0 走默认 ACK 分支，帮派保留
        self.assertIsNone(
            self.system.npc_dialogue_option(self.settings, self.role, state, 0)
        )
        gang_id = self.system.service.role_gang_id(self.role)
        self.assertIn(gang_id, self.system.service.store.gangs)
        self.assertEqual(self.system.service.role_position(self.role), GANG_POSITION_LEADER)


if __name__ == '__main__':
    unittest.main()
