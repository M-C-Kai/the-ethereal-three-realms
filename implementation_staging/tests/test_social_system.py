"""统一测试：social 系统（点击玩家菜单：查看/私聊/交易/赠送/加友/切磋/PK/组队）。

协议下标全部对应 APK 反编译证据（docs/protocol/15-玩家交互协议.md）。
"""
from __future__ import annotations

import unittest

from app.context import SystemContext
from protocol import byte, decode_frame, integer, short, string
from systems.map.protocol import player_actor_object_id
from systems.role.service import default_role
from systems.social.handler import SocialSystem

import server as server_module
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load_settings():
    settings = server_module.Settings.load(server_module.Path(ROOT) / 'config.json')
    settings.role_data_file = '/nonexistent/roles.json'
    return settings


def make_role(role_id: int, name: str) -> dict:
    role = default_role(load_settings())
    role['id'] = role_id
    role['name'] = name
    role['level'] = 10
    # default_role 以 10001 号位的初始装备实例构造物品；为不同角色重编
    # 物品实例 id，保证跨角色赠送/交易的实例 id 全局唯一（与线上数据一致）。
    offset = (role_id - 10001) * 100000
    for item in role['items']:
        item['id'] = int(item['id']) + offset
    return role


class _StubBattleSystem:
    """记录 start_duel 调用的战斗系统替身。"""

    def __init__(self):
        self.calls: list[tuple[int, int, str]] = []
        self.frames = (object(),)

    def start_duel(self, challenger, defender, kind: str = '切磋'):
        self.calls.append((int(challenger['id']), int(defender['id']), kind))
        return self.frames


class SocialSystemTests(unittest.TestCase):
    def setUp(self):
        self.settings = load_settings()
        self.alice = make_role(10001, '甲')
        self.bob = make_role(10002, '乙')
        self.roles = {10001: self.alice, 10002: self.bob}
        self.online = {10001, 10002}
        self.pushed: dict[int, list] = {}
        self.saved: list = []
        self.battle_system = _StubBattleSystem()
        self.system = SocialSystem(
            self.settings,
            save=lambda: self.saved.append(True),
            find_role=lambda role_id: self.roles.get(int(role_id)),
            online_role_ids=lambda: set(self.online),
            push_to_role=self._push,
            battle_system=self.battle_system,
        )

    def _push(self, role_id, frames):
        self.pushed.setdefault(int(role_id), []).extend(frames)

    def _context(self, role):
        return SystemContext(username=str(role.get('name')), active_role=role, session={})

    def _handle(self, role, message_id, fields):
        return self.system.handle(self._context(role), message_id, fields)

    def _decode(self, frame):
        return decode_frame(frame)

    def _pushed_ids(self, role_id):
        return [self._decode(frame)[0] for frame in self.pushed.get(role_id, [])]

    # ------------------------------------------------------------------
    # 查看（1303）：action=1 更新地图上已有的 b/v（e/ey pswitch_11）
    # ------------------------------------------------------------------
    def test_view_updates_live_actor_with_panel_fields(self):
        result = self._handle(self.alice, 1303, [byte(2), integer(player_actor_object_id(10002))])
        self.assertTrue(result.handled)
        self.assertEqual(len(result.frames), 2)  # 1303 面板数据 + 1089 空附加行
        message_id, fields = self._decode(result.frames[0])
        self.assertEqual(message_id, 1303)
        self.assertEqual(int(fields[0].value), 1)          # action=1
        self.assertEqual(int(fields[1].value), player_actor_object_id(10002))
        self.assertEqual(str(fields[2].value), '无')        # prop54 配偶
        equip_count = int(fields[4].value)
        self.assertGreaterEqual(equip_count, 0)
        tail = 5 + equip_count * 6
        self.assertEqual(str(fields[tail].value), '无')     # prop79 师傅
        self.assertEqual(int(fields[tail + 1].value), 0)    # prop84 斗法排名
        second_id, second_fields = self._decode(result.frames[1])
        self.assertEqual(second_id, 1089)
        self.assertEqual(int(second_fields[0].value), 2)
        self.assertEqual(int(second_fields[2].value), 0)    # 0 行

    def test_view_by_name_variant(self):
        result = self._handle(self.alice, 1303, [byte(2), integer(0), string('乙')])
        message_id, fields = self._decode(result.frames[0])
        self.assertEqual(message_id, 1303)
        self.assertEqual(int(fields[0].value), 1)
        self.assertEqual(int(fields[1].value), player_actor_object_id(10002))

    def test_view_offline_target_reports(self):
        self.online.discard(10002)
        result = self._handle(self.alice, 1303, [byte(2), integer(999999)])
        message_id, fields = self._decode(result.frames[0])
        self.assertEqual(message_id, 1049)  # 顶部提示

    # ------------------------------------------------------------------
    # 1089/action=2 附加列编码（e/ey.b(w) + k()，B 级）
    # ------------------------------------------------------------------
    def test_character_view_rows_default_is_empty_table(self):
        from systems.social.protocol import character_view_rows_frame
        message_id, fields = self._decode(character_view_rows_frame())
        self.assertEqual(message_id, 1089)
        self.assertEqual(int(fields[0].value), 2)   # action=2
        self.assertEqual(int(fields[1].value), 0)   # field1 占位 int
        self.assertEqual(int(fields[2].value), 0)   # 0 列
        self.assertEqual(len(fields), 3)            # 总数 3+2*0

    def test_character_view_rows_with_columns(self):
        from systems.social.protocol import character_view_rows_frame
        columns = [(1001, 250), (-7, 88)]
        message_id, fields = self._decode(character_view_rows_frame(columns))
        self.assertEqual(message_id, 1089)
        self.assertEqual(int(fields[0].value), 2)
        self.assertEqual(int(fields[1].value), 0)
        self.assertEqual(int(fields[2].value), 2)   # 列数 N=2
        self.assertEqual(len(fields), 3 + 2 * 2)    # 总数 3+2N
        self.assertEqual(int(fields[3].value), 1001)  # 列0 图标下标
        self.assertEqual(int(fields[4].value), 250)   # 列0 数值
        self.assertEqual(int(fields[5].value), -7)    # 列1 图标下标
        self.assertEqual(int(fields[6].value), 88)    # 列1 数值

    def test_character_view_rows_rejects_wrong_column_shape(self):
        from systems.social.protocol import character_view_rows_frame
        with self.assertRaises(ValueError):
            character_view_rows_frame([(1,)])  # 非法列（须为 (图标, 数值)）

    # ------------------------------------------------------------------
    # 加友（1019）
    # ------------------------------------------------------------------
    def test_friend_request_prompt_and_accept(self):
        result = self._handle(self.alice, 1019, [
            byte(10), integer(player_actor_object_id(10002)), string('乙'),
        ])
        self.assertTrue(result.handled)
        self.assertIn(1019, self._pushed_ids(10002))
        prompt_id, prompt = self._decode(self.pushed[10002][0])
        self.assertEqual(prompt_id, 1019)
        self.assertEqual(int(prompt[0].value), 10)
        self.assertEqual(int(prompt[1].value), 10001)
        self.assertEqual(str(prompt[2].value), '甲')

        accept = self._handle(self.bob, 1019, [byte(11), integer(10001), string('甲')])
        message_id, fields = self._decode(accept.frames[0])
        self.assertEqual(message_id, 1019)
        self.assertEqual(int(fields[0].value), 15)  # 好友列表
        self.assertEqual(int(fields[1].value), 1)   # 1 位好友
        self.assertEqual(int(fields[2].value), 10001)
        self.assertIn(1019, self._pushed_ids(10001))
        self.assertEqual(self.alice['friends'], [{'id': 10002, 'name': '乙'}])
        self.assertEqual(self.bob['friends'], [{'id': 10001, 'name': '甲'}])
        self.assertTrue(self.saved)

    def test_friend_reject_notifies_requester(self):
        self._handle(self.alice, 1019, [byte(10), integer(player_actor_object_id(10002)), string('乙')])
        self.pushed.clear()
        self._handle(self.bob, 1019, [byte(20), integer(10001), string('甲')])
        self.assertIn(1049, self._pushed_ids(10001))

    def test_friend_request_to_self_rejected(self):
        result = self._handle(self.alice, 1019, [byte(10), integer(player_actor_object_id(10001)), string('甲')])
        message_id, fields = self._decode(result.frames[0])
        self.assertEqual(message_id, 1049)

    # ------------------------------------------------------------------
    # 交易（1056）：锁定(20) → 对方开确认钮(10) → 双方确认后结算
    # ------------------------------------------------------------------
    def _bag_item(self, role, item_id):
        for item in role['items']:
            if item.get('id') == item_id and item.get('location') == 'bag':
                return item
        return None

    def registry_trade(self):
        self.system.registry.open_trade(10001, 10002)
        self.pushed.clear()

    def test_trade_handshake_opens_window_on_both_sides(self):
        self._handle(self.alice, 1056, [byte(1), integer(player_actor_object_id(10002))])
        self.assertIn(1056, self._pushed_ids(10002))
        prompt_id, prompt = self._decode(self.pushed[10002][0])
        self.assertEqual(int(prompt[0].value), 1)
        self.assertEqual(int(prompt[1].value), player_actor_object_id(10001))
        self.assertEqual(str(prompt[3].value), '甲')  # 名字在字段 3

        self.pushed.clear()
        accept_result = self._handle(self.bob, 1056, [byte(2), integer(player_actor_object_id(10001))])
        # 接受方（乙）应答里直接收到打开窗口帧；发起方（甲）收到定向推送。
        open_id, opened = self._decode(accept_result.frames[0])
        self.assertEqual(open_id, 1056)
        self.assertEqual(int(opened[0].value), 5)
        self.assertEqual(int(opened[1].value), player_actor_object_id(10001))
        self.assertIn(1056, self._pushed_ids(10001))

    def test_trade_lock_enables_peer_confirm_button(self):
        item_a = self._bag_item(self.alice, self.alice['items'][0]['id'])
        self.registry_trade()
        self._handle(self.alice, 1056, [byte(20), integer(100), integer(1), integer(item_a['id']), integer(0)])
        pushed_actions = [
            self._decode(frame)[1][0].value
            for frame in self.pushed.get(10002, [])
            if self._decode(frame)[0] == 1056
        ]
        self.assertEqual(pushed_actions, [8, 6, 10])  # 物品行、金额、启用确认钮

    def test_trade_settlement_swaps_items_and_silver(self):
        item_a = self._bag_item(self.alice, self.alice['items'][0]['id'])
        item_b = self._bag_item(self.bob, self.bob['items'][0]['id'])
        self.registry_trade()
        alice_silver_before = self.alice['currencies']['silver']
        bob_silver_before = self.bob['currencies']['silver']

        # 阶段一：双方锁定（确认按钮在锁定后才启用）
        self._handle(self.alice, 1056, [byte(20), integer(100), integer(1), integer(item_a['id']), integer(0)])
        self._handle(self.bob, 1056, [byte(20), integer(0), integer(1), integer(item_b['id']), integer(0)])
        # 阶段二：双方点击确认（1056/10）
        self._handle(self.alice, 1056, [byte(10), integer(player_actor_object_id(10002))])
        result = self._handle(self.bob, 1056, [byte(10), integer(player_actor_object_id(10001))])

        message_ids = [self._decode(frame)[0] for frame in result.frames]
        self.assertIn(1056, message_ids)   # 20 完成 + 11/12 关闭窗口
        self.assertIn(1008, message_ids)   # 收到物品
        self.assertIn(1009, message_ids)   # 移除物品
        self.assertIn(1017, message_ids)   # 银两刷新
        self.assertIn(1049, message_ids)   # 交易完成提示
        self.assertIsNone(self._bag_item(self.alice, item_a['id']))
        self.assertIsNone(self._bag_item(self.bob, item_b['id']))
        self.assertIsNotNone(self._bag_item(self.alice, item_b['id']))
        self.assertIsNotNone(self._bag_item(self.bob, item_a['id']))
        self.assertEqual(self.alice['currencies']['silver'], alice_silver_before - 100)
        self.assertEqual(self.bob['currencies']['silver'], bob_silver_before + 100)
        self.assertTrue(self.saved)

    def test_single_confirm_does_not_settle(self):
        item_a = self._bag_item(self.alice, self.alice['items'][0]['id'])
        self.registry_trade()
        result = self._handle(self.alice, 1056, [byte(20), integer(0), integer(1), integer(item_a['id']), integer(0)])
        message_id, _ = self._decode(result.frames[0])
        self.assertEqual(message_id, 1049)  # 锁定等待
        result = self._handle(self.alice, 1056, [byte(10), integer(player_actor_object_id(10002))])
        message_id, _ = self._decode(result.frames[0])
        self.assertEqual(message_id, 1049)  # 已确认，等待对方
        # 物品未转移，会话未关闭
        self.assertIsNotNone(self._bag_item(self.alice, item_a['id']))
        self.assertEqual(self.system.registry.active_trades, {10001: 10002, 10002: 10001})

    def test_trade_failure_when_item_missing(self):
        item_a = self._bag_item(self.alice, self.alice['items'][0]['id'])
        item_b = self._bag_item(self.bob, self.bob['items'][0]['id'])
        self.registry_trade()
        self._handle(self.alice, 1056, [byte(20), integer(0), integer(1), integer(item_a['id']), integer(0)])
        self._handle(self.bob, 1056, [byte(20), integer(0), integer(1), integer(item_b['id']), integer(0)])
        self._handle(self.alice, 1056, [byte(10), integer(player_actor_object_id(10002))])
        self.alice['items'].remove(item_a)  # 交易期间物品消失
        result = self._handle(self.bob, 1056, [byte(10), integer(player_actor_object_id(10001))])
        message_id, fields = self._decode(result.frames[0])
        self.assertEqual(message_id, 1049)
        self.assertIn('交易失败', str(fields[1].value))
        self.assertIsNotNone(self._bag_item(self.bob, item_b['id']))
        self.assertNotIn(10001, self.system.registry.active_trades)

    def test_trade_close_notifies_peer(self):
        self.registry_trade()
        self._handle(self.alice, 1056, [byte(4), integer(player_actor_object_id(10002))])
        self.assertIn(1049, self._pushed_ids(10002))
        self.assertEqual(self.system.registry.active_trades, {})

    # ------------------------------------------------------------------
    # 赠送（1009/81）
    # ------------------------------------------------------------------
    def test_gift_moves_item_to_target(self):
        item = self._bag_item(self.alice, self.alice['items'][0]['id'])
        result = self._handle(self.alice, 1009, [
            short(81), integer(item['id']), integer(player_actor_object_id(10002)),
        ])
        message_ids = [self._decode(frame)[0] for frame in result.frames]
        self.assertIn(1009, message_ids)  # 移除帧
        self.assertIn(1049, message_ids)
        self.assertIn(1008, self._pushed_ids(10002))
        self.assertIn(1049, self._pushed_ids(10002))
        self.assertIsNone(self._bag_item(self.alice, item['id']))
        self.assertIsNotNone(self._bag_item(self.bob, item['id']))
        self.assertTrue(self.saved)

    def test_gift_to_self_rejected(self):
        item = self._bag_item(self.alice, self.alice['items'][0]['id'])
        result = self._handle(self.alice, 1009, [
            short(81), integer(item['id']), integer(player_actor_object_id(10001)),
        ])
        message_id, fields = self._decode(result.frames[0])
        self.assertEqual(message_id, 1049)

    # ------------------------------------------------------------------
    # 切磋（1157）/ PK（1158）：双方确认后进入战斗系统对决
    # ------------------------------------------------------------------
    def test_spar_request_and_auto_ack_starts_duel(self):
        result = self._handle(self.alice, 1157, [byte(2), integer(10001), integer(player_actor_object_id(10002))])
        message_id, _ = self._decode(result.frames[0])
        self.assertEqual(message_id, 1049)
        ack_id, ack = self._decode(self.pushed[10002][0])
        self.assertEqual(ack_id, 1157)
        self.assertEqual(int(ack[0].value), 1)
        self.assertEqual(int(ack[1].value), player_actor_object_id(10001))

        self.pushed.clear()
        result = self._handle(self.bob, 1157, [
            byte(4), integer(player_actor_object_id(10001)), integer(player_actor_object_id(10002)),
        ])
        self.assertEqual(result.frames, self.battle_system.frames)  # 乙的进入帧
        self.assertEqual(self.battle_system.calls, [(10001, 10002, '切磋')])

    def test_pk_request_prompt_and_confirm_starts_duel(self):
        result = self._handle(self.alice, 1158, [byte(2), integer(10001), integer(player_actor_object_id(10002))])
        message_id, _ = self._decode(result.frames[0])
        self.assertEqual(message_id, 1049)
        prompt_id, prompt = self._decode(self.pushed[10002][0])
        self.assertEqual(prompt_id, 1158)
        self.assertEqual(int(prompt[2].value), player_actor_object_id(10001))

        self.pushed.clear()
        result = self._handle(self.bob, 1158, [
            byte(6), integer(10002), integer(player_actor_object_id(10001)),
        ])
        self.assertEqual(result.frames, self.battle_system.frames)
        self.assertEqual(self.battle_system.calls, [(10001, 10002, 'PK')])

    # ------------------------------------------------------------------
    # 私聊（1004）
    # ------------------------------------------------------------------
    def test_private_chat_relayed_to_target(self):
        result = self._handle(self.alice, 1004, [
            integer(0), short(2014), short(0), integer(0),
            string('乙'), string('甲'), string('你好'),
        ])
        self.assertTrue(result.handled)
        relay_id, relay = self._decode(self.pushed[10002][0])
        self.assertEqual(relay_id, 1004)
        self.assertEqual(int(relay[1].value), 2014)
        self.assertEqual(str(relay[4].value), '甲')   # 说话人
        self.assertEqual(str(relay[5].value), '乙')   # 对象
        self.assertEqual(str(relay[6].value), '你好')

    def test_private_chat_offline_reports(self):
        self.online.discard(10002)
        result = self._handle(self.alice, 1004, [
            integer(0), short(2014), short(0), integer(0),
            string('乙'), string('甲'), string('你好'),
        ])
        message_id, _ = self._decode(result.frames[0])
        self.assertEqual(message_id, 1049)

    # ------------------------------------------------------------------
    # 路由剥离：role/inventory 的消息不被 social 抢走
    # ------------------------------------------------------------------
    def test_can_handle_does_not_claim_role_or_inventory_messages(self):
        context = self._context(self.alice)
        self.assertFalse(self.system.can_handle(context, 1023, [short(0), integer(10001)]))
        self.assertFalse(self.system.can_handle(context, 1023, [short(11)]))
        self.assertFalse(self.system.can_handle(context, 1089, [byte(0), byte(0)]))
        self.assertFalse(self.system.can_handle(context, 1009, [short(3), integer(1)]))
        self.assertFalse(self.system.can_handle(context, 1039, [byte(1)]))
        self.assertFalse(self.system.can_handle(context, 1023, [short(2), integer(1)]))
        self.assertFalse(self.system.can_handle(context, 1023, [short(18)]))
        self.assertTrue(self.system.can_handle(context, 1089, [byte(2), integer(1)]))
        self.assertTrue(self.system.can_handle(context, 1009, [short(81), integer(1), integer(1)]))


if __name__ == '__main__':
    unittest.main()
