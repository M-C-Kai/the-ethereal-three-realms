"""仙晶交易所（1083）与寄售商人对话补全的回归测试。

APK 逆向依据（references/smali + apktool 全量反编译确认）：
- 1083 响应路由 main/e.p：action 0/3/4/5/6 -> screen 350；10..17 -> screen 351。
- screen 350 打开时发送 [4,tab] [5,tab] [0,page,size,tab]；应单确认 [3,order_id]。
- screen 351 打开时发送 [10,mode]；费用查询 [12,mode,num,price]；
  提交确认 [15/16,num,price]；撤单 [13,order_id]；分页 [11,page,size,mode]。
- 寄售途径：screen 70（已寄售物品）的 添加物品/添加宠物 按钮 -> 背包/宠物
  选择菜单 [寄售] -> 输入售价 -> 1138 action 9（服务端已实现）。
"""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from app.context import SystemContext
from app.router import SystemRouter
from protocol import Field, TYPE_BYTE, TYPE_INT, TYPE_STRING, decode_frame
from systems.consignment.handler import (
    CONSIGNMENT_MERCHANT_OPTION,
    EXCHANGE_MERCHANT_DIALOGUE_OPTION,
    EXCHANGE_SELL_DIALOGUE_OPTION,
    EXCHANGE_BUY_DIALOGUE_OPTION,
    ConsignmentSystem,
)
from systems.exchange.handler import (
    EXCHANGE_BUY_OPTION,
    EXCHANGE_MERCHANT_OPTION,
    EXCHANGE_SELL_OPTION,
    ExchangeSystem,
)
from systems.exchange.service import ExchangeService
from systems.exchange.protocol import (
    EXCHANGE_ACTION_CANCEL,
    EXCHANGE_ACTION_FEE,
    EXCHANGE_ACTION_MARKET_ROWS,
    EXCHANGE_ACTION_MY_ORDERS,
    EXCHANGE_ACTION_POST_BUY,
    EXCHANGE_ACTION_POST_SELL,
    EXCHANGE_ACTION_ROW_REMOVED,
    EXCHANGE_ACTION_TABS,
    exchange_entry_screen_frame,
    exchange_screen_frame,
    is_accept_request,
    is_cancel_request,
    is_entry_page_request,
    is_fee_request,
    is_market_rows_request,
    is_my_ids_request,
    is_my_orders_request,
    is_post_buy_request,
    is_post_sell_request,
    is_tabs_request,
)
from systems.map.handler import LocalNpcDialogueState


ROOT = Path(__file__).resolve().parent.parent
FEE_RATE = 0.02


def make_settings():
    import server

    return server.Settings.load(server.Path(ROOT) / 'config.json')


def fields(values, type_ids):
    return [Field(type_id, value) for value, type_id in zip(values, type_ids)]


def make_role(role_id: int, name: str, silver: int = 1_000_000, crystals: int = 1000):
    return {
        'id': role_id,
        'name': name,
        'map_id': 58,
        'bag_capacity': 1000,
        'currencies': {'silver': silver, 'immortal_stones': 0, 'immortal_crystals': crystals},
        'items': [],
    }


class _Store:
    def __init__(self, accounts=None):
        self.data = {'accounts': accounts or {}}

    def save(self):
        pass


class _BrokenStore(_Store):
    def save(self):
        raise OSError('disk full')


class ExchangeServiceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.data_file = Path(self.tmp.name) / 'exchange_orders.json'
        self.store = _Store({'a': [make_role(101, '卖家')], 'b': [make_role(202, '买家')]})
        self.service = ExchangeService(self.store, self.data_file, fee_rate=FEE_RATE)

    def test_fee_quote_uses_rate_and_minimum(self):
        result = self.service.fee_quote(100, 500)
        self.assertTrue(result.ok)
        self.assertEqual(result.fee, 1000)  # 2% of 50000
        result = self.service.fee_quote(1, 10)
        self.assertEqual(result.fee, 1)  # 最小费用
        self.assertFalse(self.service.fee_quote(0, 10).ok)

    def test_post_buy_order_escrows_silver_and_fee(self):
        role = self.store.data['accounts']['a'][0]
        result = self.service.post_order(role, 'buy', 100, 500)
        self.assertTrue(result.ok)
        self.assertEqual(role['currencies']['silver'], 1_000_000 - 50_000 - 1000)
        self.assertEqual(len(self.service.market_orders(0)), 1)
        self.assertTrue(self.data_file.exists())

    def test_post_sell_order_escrows_crystals_and_fee(self):
        role = self.store.data['accounts']['a'][0]
        result = self.service.post_order(role, 'sell', 100, 500)
        self.assertTrue(result.ok)
        self.assertEqual(role['currencies']['immortal_crystals'], 900)
        self.assertEqual(role['currencies']['silver'], 1_000_000 - 1000)

    def test_post_order_rejects_insufficient_funds(self):
        role = self.store.data['accounts']['a'][0]
        role['currencies']['silver'] = 10
        self.assertEqual(self.service.post_order(role, 'buy', 1, 500).reason, 'insufficient_silver')
        role['currencies']['immortal_crystals'] = 1
        self.assertEqual(
            self.service.post_order(role, 'sell', 100, 500).reason,
            'insufficient_crystals',
        )

    def test_market_orders_split_by_tab(self):
        role = self.store.data['accounts']['a'][0]
        self.service.post_order(role, 'buy', 10, 100)
        self.service.post_order(role, 'sell', 20, 200)
        self.assertEqual([row['kind'] for row in self.service.market_orders(0)], ['buy'])
        self.assertEqual([row['kind'] for row in self.service.market_orders(1)], ['sell'])

    def test_my_orders_and_ids_filter_by_kind(self):
        role = self.store.data['accounts']['a'][0]
        buy = self.service.post_order(role, 'buy', 10, 100).order
        sell = self.service.post_order(role, 'sell', 20, 200).order
        self.assertEqual(len(self.service.my_orders(101)), 2)
        self.assertEqual(self.service.my_order_ids(101, 0), [int(buy['order_id'])])
        self.assertEqual(self.service.my_order_ids(101, 1), [int(sell['order_id'])])

    def test_cancel_buy_order_refunds_silver_not_fee(self):
        role = self.store.data['accounts']['a'][0]
        order = self.service.post_order(role, 'buy', 100, 500).order
        result = self.service.cancel_order(role, int(order['order_id']))
        self.assertTrue(result.ok)
        self.assertEqual(role['currencies']['silver'], 1_000_000 - 1000)  # 费用不退
        self.assertEqual(self.service.market_orders(0), [])

    def test_cancel_sell_order_refunds_crystals(self):
        role = self.store.data['accounts']['a'][0]
        order = self.service.post_order(role, 'sell', 100, 500).order
        self.assertTrue(self.service.cancel_order(role, int(order['order_id'])).ok)
        self.assertEqual(role['currencies']['immortal_crystals'], 1000)

    def test_cancel_rejects_foreign_or_missing_order(self):
        role = self.store.data['accounts']['a'][0]
        other = self.store.data['accounts']['b'][0]
        order = self.service.post_order(role, 'buy', 10, 100).order
        self.assertEqual(self.service.cancel_order(other, int(order['order_id'])).reason, 'order_not_found')
        self.assertEqual(self.service.cancel_order(role, 999999).reason, 'order_not_found')

    def test_accept_buy_order_transfers_crystals_for_escrowed_silver(self):
        poster = self.store.data['accounts']['a'][0]
        acceptor = self.store.data['accounts']['b'][0]
        order = self.service.post_order(poster, 'buy', 100, 500).order
        result = self.service.accept_order(acceptor, int(order['order_id']))
        self.assertTrue(result.ok)
        self.assertEqual(acceptor['currencies']['immortal_crystals'], 900)
        self.assertEqual(acceptor['currencies']['silver'], 1_000_000 + 50_000)
        self.assertEqual(poster['currencies']['immortal_crystals'], 1100)
        self.assertEqual(poster['currencies']['silver'], 1_000_000 - 50_000 - 1000)

    def test_accept_sell_order_transfers_silver_for_escrowed_crystals(self):
        poster = self.store.data['accounts']['a'][0]
        acceptor = self.store.data['accounts']['b'][0]
        order = self.service.post_order(poster, 'sell', 100, 500).order
        result = self.service.accept_order(acceptor, int(order['order_id']))
        self.assertTrue(result.ok)
        self.assertEqual(acceptor['currencies']['immortal_crystals'], 1100)
        self.assertEqual(acceptor['currencies']['silver'], 1_000_000 - 50_000)
        self.assertEqual(poster['currencies']['silver'], 1_000_000 - 1000 + 50_000)

    def test_accept_rejects_self_trade_and_double_fill(self):
        role = self.store.data['accounts']['a'][0]
        order = self.service.post_order(role, 'buy', 10, 100).order
        self.assertEqual(self.service.accept_order(role, int(order['order_id'])).reason, 'self_trade')
        acceptor = self.store.data['accounts']['b'][0]
        self.assertTrue(self.service.accept_order(acceptor, int(order['order_id'])).ok)
        self.assertEqual(self.service.accept_order(acceptor, int(order['order_id'])).reason, 'order_not_found')

    def test_accept_rejects_insufficient_crystals(self):
        poster = self.store.data['accounts']['a'][0]
        acceptor = self.store.data['accounts']['b'][0]
        acceptor['currencies']['immortal_crystals'] = 1
        order = self.service.post_order(poster, 'buy', 100, 500).order
        self.assertEqual(
            self.service.accept_order(acceptor, int(order['order_id'])).reason,
            'insufficient_crystals',
        )

    def test_state_survives_reload(self):
        role = self.store.data['accounts']['a'][0]
        order = self.service.post_order(role, 'buy', 10, 100).order
        revived = ExchangeService(self.store, self.data_file, fee_rate=FEE_RATE)
        self.assertEqual(len(revived.market_orders(0)), 1)
        self.assertEqual(revived.market_orders(0)[0]['order_id'], int(order['order_id']))

    def test_save_failure_rolls_back(self):
        broken = _BrokenStore({'a': [make_role(101, '卖家')]})
        service = ExchangeService(broken, self.data_file, fee_rate=FEE_RATE)
        role = broken.data['accounts']['a'][0]
        with self.assertRaises(OSError):
            service.post_order(role, 'buy', 100, 500)
        self.assertEqual(role['currencies']['silver'], 1_000_000)
        self.assertEqual(service.market_orders(0), [])


class ExchangeHandlerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.data_file = Path(self.tmp.name) / 'exchange_orders.json'
        self.store = _Store({'a': [make_role(101, '卖家')], 'b': [make_role(202, '买家')]})
        self.pushed: list[tuple[int, tuple[bytes, ...]]] = []
        self.system = ExchangeSystem(
            self.store,
            self.data_file,
            fee_rate=FEE_RATE,
            notifier=lambda role_id, frames: self.pushed.append((role_id, frames)),
        )
        self.role = self.store.data['accounts']['b'][0]
        self.context = SystemContext(username='buyer', active_role=self.role, session={})

    def handle(self, values, type_ids, context=None):
        return self.system.handle(context or self.context, 1083, fields(values, type_ids))

    def test_request_detectors_are_type_exact(self):
        self.assertTrue(is_tabs_request(fields([4, 0], [TYPE_BYTE, TYPE_BYTE])))
        self.assertFalse(is_tabs_request(fields([4], [TYPE_BYTE])))
        self.assertTrue(is_market_rows_request(fields([0, 0, 20, 1], [TYPE_BYTE] * 4)))
        self.assertTrue(is_my_ids_request(fields([5, 1], [TYPE_BYTE, TYPE_BYTE])))
        self.assertTrue(is_entry_page_request(fields([10, 1], [TYPE_BYTE, TYPE_BYTE])))
        self.assertTrue(is_my_orders_request(fields([11, 0, 20, 0], [TYPE_BYTE] * 4)))
        self.assertTrue(is_fee_request(fields([12, 1, 100, 500], [TYPE_BYTE, TYPE_BYTE, TYPE_INT, TYPE_INT])))
        self.assertTrue(is_cancel_request(fields([13, 7], [TYPE_BYTE, TYPE_INT])))
        self.assertTrue(is_post_buy_request(fields([16, 100, 500], [TYPE_BYTE, TYPE_INT, TYPE_INT])))
        self.assertTrue(is_post_sell_request(fields([15, 100, 500], [TYPE_BYTE, TYPE_INT, TYPE_INT])))
        self.assertTrue(is_accept_request(fields([3, 7], [TYPE_BYTE, TYPE_INT])))

    def test_tabs_request_returns_native_tabs(self):
        result = self.handle([4, 0], [TYPE_BYTE, TYPE_BYTE])
        message_id, payload = decode_frame(result.frames[0])
        self.assertEqual(message_id, 1083)
        self.assertEqual(int(payload[0].value), EXCHANGE_ACTION_TABS)
        self.assertEqual(int(payload[1].value), 2)
        self.assertIn('玩家求购单', [payload[2].value, payload[3].value])

    def test_market_rows_request_returns_active_orders(self):
        self.store.data['accounts']['a'][0]
        self.system.service.post_order(self.store.data['accounts']['a'][0], 'buy', 100, 500)
        result = self.handle([0, 0, 20, 0], [TYPE_BYTE] * 4)
        message_id, payload = decode_frame(result.frames[0])
        self.assertEqual(int(payload[0].value), EXCHANGE_ACTION_MARKET_ROWS)
        self.assertEqual(int(payload[1].value), 1)  # total SHORT
        self.assertEqual(int(payload[2].value), 1)  # row count, ad.a(w) index 2
        self.assertEqual(int(payload[3].value), 0)  # tab, ad.a(w) index 3
        row = payload[4:]
        self.assertEqual([f.value for f in row], [1, '100', '卖家', '50000'])

    def test_entry_page_and_my_orders(self):
        self.system.service.post_order(self.role, 'sell', 50, 200)
        result = self.handle([10, 1], [TYPE_BYTE, TYPE_BYTE])
        _, payload = decode_frame(result.frames[0])
        self.assertEqual(int(payload[0].value), 10)
        self.assertEqual(int(payload[1].value), 2)  # 下单/我的订单页签，不是摘要行
        result = self.handle([11, 0, 20, 1], [TYPE_BYTE] * 4)
        _, payload = decode_frame(result.frames[0])
        self.assertEqual(int(payload[0].value), EXCHANGE_ACTION_MY_ORDERS)
        self.assertEqual(int(payload[1].value), 1)
        self.assertEqual(int(payload[2].value), 1)
        row = payload[3:]
        self.assertEqual([f.value for f in row[:3]], [1, '200', '50'])
        self.assertTrue(row[3].value)

    def test_empty_entry_initializes_two_tabs_in_both_modes(self):
        for mode in (0, 1):
            with self.subTest(mode=mode):
                result = self.handle([10, mode], [TYPE_BYTE, TYPE_BYTE])
                message_id, payload = decode_frame(result.frames[0])
                self.assertEqual(message_id, 1083)
                self.assertEqual([f.type_id for f in payload],
                                 [TYPE_BYTE, TYPE_BYTE, TYPE_STRING, TYPE_STRING, TYPE_STRING])
                self.assertEqual(int(payload[1].value), 2)
                self.assertTrue(payload[2].value)
                self.assertTrue(payload[3].value)

    def test_fee_request_returns_commission(self):
        result = self.handle([12, 1, 100, 500], [TYPE_BYTE, TYPE_BYTE, TYPE_INT, TYPE_INT])
        message_id, payload = decode_frame(result.frames[0])
        self.assertEqual(message_id, 1083)
        self.assertEqual(int(payload[0].value), EXCHANGE_ACTION_FEE)
        self.assertIn('1000', payload[1].value)

    def test_post_sell_order_clears_inputs_and_syncs_currency(self):
        result = self.handle([15, 50, 200], [TYPE_BYTE, TYPE_INT, TYPE_INT])
        self.assertEqual(len(result.frames), 3)
        self.assertEqual(self.system.service.my_orders(self.role['id'], 1)[0]['kind'], 'sell')
        refresh_id, refresh = decode_frame(result.frames[2])
        self.assertEqual(refresh_id, 1083)
        self.assertEqual([f.type_id for f in refresh],
                         [TYPE_BYTE, 3, TYPE_INT, TYPE_STRING, TYPE_STRING, TYPE_STRING])
        self.assertEqual([f.value for f in refresh[:5]], [17, 1, 1, '200', '50'])
        self.assertTrue(refresh[5].value)

        message_id, payload = decode_frame(result.frames[0])
        self.assertEqual(message_id, 1083)
        self.assertEqual(int(payload[0].value), EXCHANGE_ACTION_POST_SELL)
        # 1017 货币同步：property 50 银两 / 52 仙晶
        sync_id, sync = decode_frame(result.frames[1])
        self.assertEqual(sync_id, 1017)
        self.assertEqual([f.value for f in sync], [
            0, 202, 2, 50, 1_000_000 - 200, 52, 950,
        ])
        self.assertEqual(self.role['currencies']['immortal_crystals'], 950)

    def test_market_column_header_is_not_own_order_ids(self):
        result = self.handle([5, 1], [TYPE_BYTE, TYPE_BYTE])
        _, payload = decode_frame(result.frames[0])
        self.assertEqual([f.value for f in payload],
                         [5, 4, 1, '仙晶数量', '发布者', '银两总额'])

    def test_post_buy_order_with_insufficient_silver_is_rejected(self):
        self.role['currencies']['silver'] = 10
        result = self.handle([16, 100, 500], [TYPE_BYTE, TYPE_INT, TYPE_INT])
        message_id, payload = decode_frame(result.frames[0])
        self.assertEqual(message_id, 1049)  # 顶部提示
        self.assertIn('银两不足', payload[1].value)

    def test_self_trade_closes_wait_before_hint_without_asset_changes(self):
        import copy
        for kind in ('buy', 'sell'):
            with self.subTest(kind=kind):
                order = self.system.service.post_order(self.role, kind, 11, 1).order
                snapshot = copy.deepcopy(self.role)
                result = self.handle([3, int(order['order_id'])], [TYPE_BYTE, TYPE_INT])
                self.assertEqual(len(result.frames), 2)
                ack_id, ack = decode_frame(result.frames[0])
                self.assertEqual(ack_id, 1083)
                self.assertEqual([(f.type_id, f.value) for f in ack], [(TYPE_BYTE, 3)])
                hint_id, hint = decode_frame(result.frames[1])
                self.assertEqual(hint_id, 1049)
                self.assertIn('自己的订单', hint[1].value)
                self.assertEqual(self.role, snapshot)
                self.assertEqual(self.system.service.my_orders(self.role['id'])[-1]['status'], 'active')

    def test_cancel_order_refunds_and_removes_row(self):
        order = self.system.service.post_order(self.role, 'sell', 50, 200).order
        result = self.handle([13, int(order['order_id'])], [TYPE_BYTE, TYPE_INT])
        message_id, payload = decode_frame(result.frames[0])
        self.assertEqual(int(payload[0].value), EXCHANGE_ACTION_CANCEL)
        self.assertEqual(int(payload[1].value), 10000)  # total SHORT
        self.assertEqual(int(payload[2].value), int(order['order_id']))
        self.assertEqual(self.role['currencies']['immortal_crystals'], 1000)

    def test_accept_order_updates_both_parties_and_notifies_poster(self):
        poster = self.store.data['accounts']['a'][0]
        order = self.system.service.post_order(poster, 'buy', 100, 500).order
        result = self.handle([3, int(order['order_id'])], [TYPE_BYTE, TYPE_INT])
        message_id, payload = decode_frame(result.frames[0])
        self.assertEqual(int(payload[0].value), EXCHANGE_ACTION_ROW_REMOVED)
        self.assertEqual(int(payload[1].value), 0)  # 求购单 tab
        self.assertEqual(int(payload[2].value), int(order['order_id']))
        sync_id, _ = decode_frame(result.frames[1])
        self.assertEqual(sync_id, 1017)
        self.assertEqual(self.role['currencies']['immortal_crystals'], 900)
        self.assertEqual(self.role['currencies']['silver'], 1_000_000 + 50_000)
        self.assertEqual([role_id for role_id, _ in self.pushed], [101])

    def test_exchange_claims_1083_on_router(self):
        router = SystemRouter()
        from systems.exchange.handler import register_exchange_routes

        register_exchange_routes(router, self.system)
        result = router.dispatch(
            self.context,
            1083,
            fields([4, 0], [TYPE_BYTE, TYPE_BYTE]),
        )
        self.assertTrue(result.handled)
        self.assertTrue(result.frames)


class ConsignmentMerchantDialogueTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.settings = make_settings()
        self.store = _Store({'a': [make_role(101, '卖家')]})
        self.consignment = ConsignmentSystem(
            self.store,
            self.settings.item_registry,
            Path(self.tmp.name) / 'consignment.json',
        )
        self.exchange = ExchangeSystem(self.store, Path(self.tmp.name) / 'exchange.json')
        self.role = self.store.data['accounts']['a'][0]
        definition = self.settings.map_registry.require(58)
        self.npc = next(
            npc for npc in definition.npcs if npc.service == 'consignment_merchant'
        )

    def test_dialogue_offers_all_options(self):
        frames = self.consignment.npc_dialogue_frames(self.npc, self.role, self.settings)
        message_id, payload = decode_frame(frames[0])
        self.assertEqual(message_id, 2032)
        self.assertEqual(int(payload[1].value), 8)  # 介绍 + 5 选项 + 结束对话 + 布局帧
        values = [field.value for field in payload[2:]]
        option_ids = [values[start + 4] for start in range(0, len(values), 8)]
        texts = [values[start + 6] for start in range(0, len(values), 8)]
        # 记录顺序：介绍(0) + 5 个选项 + 结束对话(0) + 布局帧(100)
        self.assertEqual(option_ids[1:6], [1, 2, 3, 4, 5])
        self.assertEqual(
            texts[1:6], ['寄售商场', '我的寄售', '仙晶交易所', '寄售仙晶', '求购仙晶'],
        )

    def test_market_option_opens_native_screen_613(self):
        state = LocalNpcDialogueState()
        state.select(58, self.npc.id)
        frames = self.consignment.npc_dialogue_option(
            self.settings, self.role, state, CONSIGNMENT_MERCHANT_OPTION,
        )
        # ack + 1010 开屏 613 + 1138 分类帧
        self.assertEqual([decode_frame(frame)[0] for frame in frames], [1010, 1010, 1138])
        _, payload = decode_frame(frames[1])
        self.assertEqual([f.value for f in payload], [0, 0, 0, 2809, 613, 69])
        self.assertIsNone(state.npc_id)

    def test_my_listings_option_opens_native_screen_70(self):
        state = LocalNpcDialogueState()
        state.select(58, self.npc.id)
        frames = self.consignment.npc_dialogue_option(
            self.settings, self.role, state, 2,
        )
        self.assertIsNotNone(frames)
        # ack(1010/action=7) + 1010 开屏 screen 70
        self.assertEqual([decode_frame(frame)[0] for frame in frames], [1010, 1010])
        _, payload = decode_frame(frames[1])
        self.assertEqual([f.value for f in payload], [0, 0, 0, 0, 70, 69])
        self.assertIsNone(state.npc_id)

    def test_exchange_options_open_market_and_entry_screens(self):
        # 选项 3：仙晶交易所行情（screen 350）
        state = LocalNpcDialogueState()
        state.select(58, self.npc.id)
        self.assertIsNone(
            self.consignment.npc_dialogue_option(
                self.settings, self.role, state, EXCHANGE_MERCHANT_DIALOGUE_OPTION,
            )
        )
        state.select(58, self.npc.id)
        frames = self.exchange.npc_dialogue_option(
            self.settings, self.role, state, EXCHANGE_MERCHANT_OPTION,
        )
        self.assertEqual([decode_frame(frame)[0] for frame in frames], [1010, 1010])
        _, payload = decode_frame(frames[1])
        self.assertEqual([f.value for f in payload], [0, 0, 0, 0, 350, 69])
        self.assertIsNone(state.npc_id)

        # 选项 4：寄售仙晶 -> screen 351 卖出页（mode 1）
        state = LocalNpcDialogueState()
        state.select(58, self.npc.id)
        frames = self.exchange.npc_dialogue_option(
            self.settings, self.role, state, EXCHANGE_SELL_OPTION,
        )
        _, payload = decode_frame(frames[1])
        self.assertEqual([f.value for f in payload], [0, 0, 0, 1, 351, 69])

        # 选项 5：求购仙晶 -> screen 351 买入页（mode 0）
        state = LocalNpcDialogueState()
        state.select(58, self.npc.id)
        frames = self.exchange.npc_dialogue_option(
            self.settings, self.role, state, EXCHANGE_BUY_OPTION,
        )
        _, payload = decode_frame(frames[1])
        self.assertEqual([f.value for f in payload], [0, 0, 0, 0, 351, 69])
        self.assertIsNone(state.npc_id)

    def test_exchange_option_ignored_for_other_services(self):
        definition = self.settings.map_registry.require(58)
        other = next(npc for npc in definition.npcs if npc.service != 'consignment_merchant')
        state = LocalNpcDialogueState()
        state.select(58, other.id)
        self.assertIsNone(
            self.exchange.npc_dialogue_option(self.settings, self.role, state, EXCHANGE_MERCHANT_OPTION)
        )


class ConsignmentRoleBindingTests(unittest.TestCase):
    """客户端 b/m.h() 在本构建中恒为 0：请求角色 id 只能作提示性校验。"""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.settings = make_settings()
        self.store = _Store({'a': [make_role(101, '卖家')]})
        self.system = ConsignmentSystem(
            self.store,
            self.settings.item_registry,
            Path(self.tmp.name) / 'consignment.json',
        )
        self.role = self.store.data['accounts']['a'][0]
        self.role['items'].append(
            {'id': 9001, 'template_id': 260000001, 'quantity': 5, 'location': 'bag'},
        )
        self.context = SystemContext(username='t', active_role=self.role, session={})

    def test_my_listings_accepts_zero_client_role_id(self):
        result = self.system.handle(self.context, 1138, fields([7, 0], [TYPE_BYTE, TYPE_INT]))
        message_id, payload = decode_frame(result.frames[0])
        self.assertEqual(message_id, 1138)
        self.assertEqual(int(payload[0].value), 7)
        self.assertEqual(int(payload[1].value), 0)  # 空列表而非拒绝提示

    def test_my_listings_ignores_merchant_id_in_client_role_slot(self):
        result = self.system.handle(self.context, 1138, fields([7, 1900004], [TYPE_BYTE, TYPE_INT]))
        message_id, payload = decode_frame(result.frames[0])
        self.assertEqual(message_id, 1138)
        self.assertEqual(int(payload[0].value), 7)

    def test_list_item_accepts_zero_client_role_id(self):
        result = self.system.handle(self.context, 1138, fields(
            [9, 9001, 1, 0, 5, 100],
            [TYPE_BYTE, TYPE_INT, TYPE_BYTE, TYPE_INT, TYPE_BYTE, TYPE_INT],
        ))
        message_id, _ = decode_frame(result.frames[-1])
        self.assertEqual(message_id, 1138)
        self.assertEqual(len(self.system.service.my_listings(101)), 1)

    def test_list_item_ignores_positive_client_role_hint(self):
        result = self.system.handle(self.context, 1138, fields(
            [9, 9001, 1, 202, 5, 100],
            [TYPE_BYTE, TYPE_INT, TYPE_BYTE, TYPE_INT, TYPE_BYTE, TYPE_INT],
        ))
        message_id, _ = decode_frame(result.frames[-1])
        self.assertEqual(message_id, 1138)
        self.assertEqual(len(self.system.service.my_listings(101)), 1)


if __name__ == '__main__':
    unittest.main()
