"""1083 仙晶交易所系统边界：原生 screen 350/351 请求编排与寄售商人对话。"""

from __future__ import annotations

import logging
from typing import Any, Callable

from app.context import SystemContext
from app.router import RouteResult, SystemRouter
from systems.exchange.protocol import (
    EXCHANGE_ENTRY_SCREEN_ID,  # noqa: F401  (re-exported for tests/docs)
    EXCHANGE_MARKET_SCREEN_ID,  # noqa: F401  (re-exported for tests/docs)
    EXCHANGE_MESSAGE_ID,
    EXCHANGE_MODE_BUY,
    EXCHANGE_MODE_SELL,
    EXCHANGE_TAB_BUY_ORDERS,
    EXCHANGE_TAB_SELL_ORDERS,
    exchange_cancelled_frame,
    exchange_entry_rows_frame,
    exchange_entry_screen_frame,
    exchange_fee_frame,
    exchange_market_frame,
    exchange_my_ids_frame,
    exchange_my_orders_frame,
    exchange_posted_frame,
    exchange_row_removed_frame,
    exchange_screen_frame,
    exchange_tabs_frame,
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
from systems.exchange.service import (
    ExchangeService,
    crystal_sync_properties,
)
from systems.role.protocol import character_appearance_frame


LOG = logging.getLogger('piaomiao-local')

EXCHANGE_MERCHANT_OPTION = 3
EXCHANGE_SELL_OPTION = 4
EXCHANGE_BUY_OPTION = 5


class ExchangeSystem:
    """仙晶交易所：1083 订单簿 + 赵公明对话“仙晶交易所”入口。"""

    system_name = 'exchange'

    def __init__(
        self,
        role_store: Any = None,
        data_file: str | None = None,
        fee_rate: float = 0.02,
        notifier: Callable[[int, tuple[bytes, ...]], None] | None = None,
    ) -> None:
        self.service = ExchangeService(role_store, data_file, fee_rate)
        self._notifier = notifier

    # ------------------------------------------------------------------
    def can_handle(self, _context: SystemContext, message_id: int, _fields: list) -> bool:
        return message_id == EXCHANGE_MESSAGE_ID

    def handle(self, context: SystemContext, message_id: int, fields: list) -> RouteResult:
        if not fields:
            return RouteResult.not_handled()
        role = context.active_role
        role_id = int(role.get('id', 0)) if role is not None else 0
        username = context.username

        if is_tabs_request(fields):
            LOG.info('EXCHANGE_TABS user=%r role_id=%d', username, role_id)
            return RouteResult.handled((exchange_tabs_frame(),))

        if is_market_rows_request(fields):
            page = int(fields[1].value)
            size = max(1, int(fields[2].value))
            tab = int(fields[3].value)
            orders = self.service.market_orders(tab)
            LOG.info(
                'EXCHANGE_MARKET_ROWS user=%r role_id=%d tab=%d page=%d total=%d',
                username, role_id, tab, page, len(orders),
            )
            return RouteResult.handled((
                exchange_market_frame(
                    tab, orders[page * size:(page + 1) * size], total=len(orders),
                ),
            ))

        if is_my_ids_request(fields):
            tab = int(fields[1].value)
            ids = self.service.my_order_ids(role_id, tab) if role is not None else []
            return RouteResult.handled((exchange_my_ids_frame(tab, ids),))

        if is_entry_page_request(fields):
            mode = int(fields[1].value)
            rows = self._entry_rows(role_id, mode)
            LOG.info(
                'EXCHANGE_ENTRY_PAGE user=%r role_id=%d mode=%d rows=%d',
                username, role_id, mode, len(rows),
            )
            return RouteResult.handled((exchange_entry_rows_frame(mode, rows),))

        if is_my_orders_request(fields):
            page = int(fields[1].value)
            size = max(1, int(fields[2].value))
            mode = int(fields[3].value)
            orders = self.service.my_orders(role_id, mode) if role is not None else []
            return RouteResult.handled((
                exchange_my_orders_frame(
                    mode, orders[page * size:(page + 1) * size], total=len(orders),
                ),
            ))

        if is_fee_request(fields):
            return self._handle_fee(context, fields)

        if is_post_buy_request(fields) or is_post_sell_request(fields):
            return self._handle_post(context, role, role_id, fields)

        if is_cancel_request(fields):
            return self._handle_cancel(context, role, role_id, fields)

        if is_accept_request(fields):
            return self._handle_accept(context, role, role_id, fields)

        LOG.info(
            'ignored exchange message=1083 field_types=%r values=%r',
            [field.type_id for field in fields],
            [field.value for field in fields],
        )
        return RouteResult.handled()

    # ------------------------------------------------------------------
    def _entry_rows(self, role_id: int, mode: int) -> list[str]:
        rows: list[str] = []
        if role_id:
            kind = 'buy' if int(mode) == EXCHANGE_MODE_BUY else 'sell'
            for order in self.service.my_orders(role_id):
                if order.get('kind') != kind:
                    continue
                rows.append(
                    f"#{order['order_id']} "
                    f"{'求购' if kind == 'buy' else '出售'}"
                    f"{order['crystals']}仙晶 单价{order['unit_price']}银两"
                )
        return rows

    def _handle_fee(self, context: SystemContext, fields: list) -> RouteResult:
        mode = int(fields[1].value)
        crystals = int(fields[2].value)
        unit_price = int(fields[3].value)
        result = self.service.fee_quote(crystals, unit_price)
        if not result.ok:
            return RouteResult.handled((exchange_fee_frame('无效数量或单价'),))
        total = crystals * unit_price
        LOG.info(
            'EXCHANGE_FEE user=%r mode=%d crystals=%d price=%d fee=%d',
            context.username, mode, crystals, unit_price, result.fee,
        )
        return RouteResult.handled((exchange_fee_frame(f'委托费用：{result.fee} 银两'),))

    def _handle_post(
        self,
        context: SystemContext,
        role,
        role_id: int,
        fields: list,
    ) -> RouteResult:
        buy = is_post_buy_request(fields)
        action = 15 if buy else 16
        if role is None:
            return RouteResult.handled()
        crystals = int(fields[1].value)
        unit_price = int(fields[2].value)
        kind = 'buy' if buy else 'sell'
        result = self.service.post_order(role, kind, crystals, unit_price)
        if not result.ok:
            LOG.info(
                'EXCHANGE_POST_REJECT user=%r role_id=%d kind=%s reason=%s',
                context.username, role_id, kind, result.reason,
            )
            from app.notify import top_message_frame
            reasons = {
                'insufficient_silver': '银两不足，无法托管',
                'insufficient_crystals': '仙晶不足，无法托管',
                'total_overflow': '订单金额超出上限',
                'invalid_input': '数量与单价必须大于 0',
            }
            return RouteResult.handled((
                top_message_frame('下单失败：' + reasons.get(result.reason, result.reason)),
            ))
        LOG.info(
            'EXCHANGE_POSTED user=%r role_id=%d order_id=%d kind=%s crystals=%d price=%d fee=%d',
            context.username, role_id, int(result.order['order_id']),
            kind, crystals, unit_price, result.fee,
        )
        return RouteResult.handled((
            exchange_posted_frame(action),
            character_appearance_frame(role_id, crystal_sync_properties(role)),
        ))

    def _handle_cancel(
        self,
        context: SystemContext,
        role,
        role_id: int,
        fields: list,
    ) -> RouteResult:
        order_id = int(fields[1].value)
        if role is None:
            return RouteResult.handled()
        result = self.service.cancel_order(role, order_id)
        if not result.ok:
            from app.notify import top_message_frame
            return RouteResult.handled((top_message_frame('撤单失败：订单不存在'),))
        LOG.info(
            'EXCHANGE_CANCELLED user=%r role_id=%d order_id=%d refund_total=%d',
            context.username, role_id, order_id, result.total,
        )
        return RouteResult.handled((
            exchange_cancelled_frame(result.total, order_id),
            character_appearance_frame(role_id, crystal_sync_properties(role)),
        ))

    def _handle_accept(
        self,
        context: SystemContext,
        role,
        role_id: int,
        fields: list,
    ) -> RouteResult:
        order_id = int(fields[1].value)
        if role is None:
            return RouteResult.handled()
        result = self.service.accept_order(role, order_id)
        if not result.ok:
            LOG.info(
                'EXCHANGE_ACCEPT_REJECT user=%r role_id=%d order_id=%d reason=%s',
                context.username, role_id, order_id, result.reason,
            )
            from app.notify import top_message_frame
            reasons = {
                'order_not_found': '订单已成交或已撤销',
                'poster_not_found': '订单发布者不存在',
                'self_trade': '无法应自己的订单',
                'insufficient_crystals': '仙晶不足',
                'insufficient_silver': '银两不足',
            }
            return RouteResult.handled((
                top_message_frame('应单失败：' + reasons.get(result.reason, result.reason)),
            ))

        order = result.order or {}
        tab = EXCHANGE_TAB_BUY_ORDERS if order.get('kind') == 'buy' else EXCHANGE_TAB_SELL_ORDERS
        remaining = len(self.service.market_orders(tab))
        LOG.info(
            'EXCHANGE_TRADE_COMPLETED transaction order_id=%d acceptor=%d poster=%d '
            'crystals=%d total=%d tab=%d',
            order_id,
            role_id,
            int(order.get('poster_role_id', 0)),
            int(order.get('crystals', 0)),
            result.total,
            tab,
        )
        self._notify_counterparty(int(order.get('poster_role_id', 0)), role_id)
        return RouteResult.handled((
            exchange_row_removed_frame(tab, order_id, remaining),
            character_appearance_frame(role_id, crystal_sync_properties(role)),
        ))

    def _notify_counterparty(self, poster_role_id: int, _acceptor_role_id: int) -> None:
        if self._notifier is None:
            return
        poster = self.service.find_role(poster_role_id)
        if poster is None:
            return
        try:
            self._notifier(
                poster_role_id,
                (character_appearance_frame(poster_role_id, crystal_sync_properties(poster)),),
            )
        except Exception:  # notifier failures must never break the trade
            LOG.debug('exchange counterparty notify failed', exc_info=True)

    # ------------------------------------------------------------------
    # 寄售商人对话（由地图系统的 2032 选项回调认领选项 3/4/5）
    # ------------------------------------------------------------------
    def npc_dialogue_option(self, settings, role, state, option_id: int, input_text: str = ''):
        """Open the native crystal-exchange screens from the NPC dialogue.

        The dialogue itself (including the option texts) is built by the
        consignment system; this hook claims option selection:

        - 3 仙晶交易所 -> screen 350 order market
        - 4 寄售仙晶   -> screen 351 卖出仙晶 order-entry page (mode 1)
        - 5 求购仙晶   -> screen 351 买入仙晶 order-entry page (mode 0)
        """
        from systems.map.protocol import (
            map_npc_for_object_id, map_object_interaction_ack_frame,
        )
        from systems.map.service import settings_for_role
        if role is None or int(option_id) not in (
            EXCHANGE_MERCHANT_OPTION,
            EXCHANGE_SELL_OPTION,
            EXCHANGE_BUY_OPTION,
        ):
            return None

        try:
            definition = settings_for_role(settings, role)
        except ValueError:
            return None

        if state.map_id != definition.id or state.npc_id is None:
            return None

        npc = map_npc_for_object_id(definition, state.npc_id)
        if npc is None or str(getattr(npc, 'service', '')) != 'consignment_merchant':
            return None

        if int(option_id) == EXCHANGE_MERCHANT_OPTION:
            frames = (exchange_screen_frame(),)
            LOG.info(
                'EXCHANGE_MERCHANT_OPEN role_id=%d npc_id=%d screen=%d',
                int(role.get('id', 0)),
                int(npc.id),
                EXCHANGE_MARKET_SCREEN_ID,
            )
        else:
            mode = EXCHANGE_MODE_SELL if int(option_id) == EXCHANGE_SELL_OPTION else EXCHANGE_MODE_BUY
            frames = (exchange_entry_screen_frame(mode=mode),)
            LOG.info(
                'EXCHANGE_ENTRY_OPEN role_id=%d npc_id=%d screen=%d mode=%d',
                int(role.get('id', 0)),
                int(npc.id),
                EXCHANGE_ENTRY_SCREEN_ID,
                mode,
            )
        try:
            return [map_object_interaction_ack_frame(0), *frames]
        finally:
            state.clear()


def register_exchange_routes(router: SystemRouter, system: ExchangeSystem) -> None:
    router.register(system.system_name, system.can_handle, system.handle)
