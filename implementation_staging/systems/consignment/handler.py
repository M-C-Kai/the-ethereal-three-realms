from __future__ import annotations

import logging

from app.context import SystemContext
from app.router import RouteResult, SystemRouter
from app.notify import top_message_frame
from protocol import encode_frame, integer, short
from systems.consignment.protocol import (
    CONSIGNMENT_ACTION_LIST, CONSIGNMENT_ITEM_CATEGORIES, CONSIGNMENT_OBJECT_ITEM,
    CONSIGNMENT_OBJECT_PET, consignment_category_counts_frame,
    consignment_category_frame, consignment_market_category, consignment_market_list_frame,
    consignment_my_listings_frame, consignment_my_screen_frame,
    consignment_remove_market_frame,
    consignment_remove_owned_frame, consignment_screen_frame,
    is_consignment_browse_request, is_consignment_buy_request,
    is_consignment_category_request, is_consignment_list_item_request,
    is_consignment_market_list_request, is_consignment_my_listings_request,
    is_consignment_unlist_request, wire_record_from_listing,
)
from systems.consignment.service import ConsignmentService
from systems.inventory.protocol import item_frame
from systems.role.protocol import character_appearance_frame  # noqa: F401


LOG = logging.getLogger('piaomiao-local')

CONSIGNMENT_MERCHANT_OPTION = 1
# Screen 6 dialogue option ids for the consignment merchant NPC. Option 2 is
# the native consignment path (screen 70 with 添加物品/添加宠物); options 3/4/5
# are claimed by the exchange system (仙晶交易所 screen 350 and the screen 351
# 卖出/买入 order-entry pages).
CONSIGNMENT_MY_LISTINGS_OPTION = 2
EXCHANGE_MERCHANT_DIALOGUE_OPTION = 3
EXCHANGE_SELL_DIALOGUE_OPTION = 4
EXCHANGE_BUY_DIALOGUE_OPTION = 5


class ConsignmentSystem:
    """consignment 系统边界：1138 寄售行协议与寄售商人对话。"""

    system_name = 'consignment'

    def __init__(self, role_store=None, item_registry=None, data_file=None) -> None:
        # 寄售服务在每次操作前重新从磁盘加载，跨连接共享一个实例即可。
        self.service = ConsignmentService(role_store, item_registry, data_file)
        self._item_registry = item_registry

    def can_handle(self, _context: SystemContext, message_id: int, _fields: list[object]) -> bool:
        return message_id == 1138

    def handle(self, context: SystemContext, message_id: int, fields: list[object]) -> RouteResult:
        if not fields:
            return RouteResult.not_handled()
        role = context.active_role
        session = context.session
        role_id = int(role.get('id', 0)) if role is not None else 0
        username = context.username

        if is_consignment_category_request(fields):
            LOG.info(
                'CONSIGNMENT_CATEGORIES user=%r role_id=%d count=%d',
                username,
                role_id,
                len(CONSIGNMENT_ITEM_CATEGORIES),
            )
            return RouteResult.handled((consignment_category_frame(),))

        if is_consignment_browse_request(fields):
            category_id = int(fields[1].value)
            session['consignment.category'] = category_id
            total = self.service.category_count(category_id)
            LOG.info(
                'CONSIGNMENT_BROWSE user=%r role_id=%d category_id=%d category=%r active=%d',
                username,
                role_id,
                category_id,
                CONSIGNMENT_ITEM_CATEGORIES[category_id],
                total,
            )
            # APK main/e.al routes action 13 to screen 44. That page
            # consumes a count/filter vector, then asks for actual
            # market rows through action 0/23. Even an empty category
            # therefore needs [13, 1, 0], not the old generic [13, 0].
            return RouteResult.handled((consignment_category_counts_frame([total]),))

        if is_consignment_market_list_request(fields):
            requested_category = consignment_market_category(fields)
            if requested_category is not None:
                session['consignment.category'] = requested_category
            category_id = int(session.get('consignment.category', 0))
            rows = self.service.search(category_id)
            records = [wire_record_from_listing(row, self._item_registry) for row in rows]
            LOG.info(
                'CONSIGNMENT_MARKET_LIST user=%r role_id=%d category=%d count=%d request_action=%d',
                username,
                role_id,
                category_id,
                len(records),
                int(fields[0].value),
            )
            return RouteResult.handled((consignment_market_list_frame(records),))

        if is_consignment_my_listings_request(fields):
            requested_role = int(fields[1].value)
            if role is None:
                LOG.warning(
                    'CONSIGNMENT_MY_REJECT user=%r role_id=%d requested=%d',
                    username, role_id, requested_role,
                )
                return RouteResult.handled((top_message_frame('寄售角色信息已失效'),))
            rows = self.service.my_listings(role_id)
            return RouteResult.handled((
                consignment_my_listings_frame(
                    [wire_record_from_listing(row, self._item_registry) for row in rows]
                ),
            ))

        if is_consignment_list_item_request(fields):
            return self._handle_list_item(context, role, role_id, fields)

        if is_consignment_unlist_request(fields):
            return self._handle_unlist(context, role, role_id, fields)

        if is_consignment_buy_request(fields):
            return self._handle_buy(context, role, role_id, fields)

        LOG.info(
            'ignored consignment message=1138 field_types=%r values=%r',
            [field.type_id for field in fields],
            [field.value for field in fields],
        )
        return RouteResult.handled()

    # ------------------------------------------------------------------
    # 上架
    # ------------------------------------------------------------------
    def _handle_list_item(self, context: SystemContext, role, role_id: int, fields) -> RouteResult:
        username = context.username
        item_id = int(fields[1].value)
        object_type = int(fields[2].value)
        requested_role = int(fields[3].value)
        quantity = int(fields[4].value)
        unit_price = int(fields[5].value)
        if role is None:
            return RouteResult.handled((top_message_frame('寄售角色信息已失效'),))
        if object_type == CONSIGNMENT_OBJECT_PET:
            return RouteResult.handled((top_message_frame('宠物寄售暂未开放'),))
        if object_type != CONSIGNMENT_OBJECT_ITEM:
            return RouteResult.handled((top_message_frame('该对象暂不支持寄售'),))
        result = self.service.list_item(role, item_id, quantity, unit_price)
        if not result.ok:
            LOG.info(
                'CONSIGNMENT_LIST_REJECT user=%r role_id=%d item_id=%d reason=%s',
                username, role_id, item_id, result.reason,
            )
            return RouteResult.handled((top_message_frame('寄售失败：' + result.reason),))
        updates: list[bytes] = []
        if result.removed_from_bag:
            # Same native removal notification used by
            # the normal bag discard path.
            updates.append(encode_frame(1009, [short(3), integer(item_id)]))
        elif result.source_item is not None:
            updates.append(item_frame(
                result.source_item,
                self._item_registry,
                operation=3,
            ))
        own = self.service.my_listings(role_id)
        updates.append(consignment_my_listings_frame(
            [wire_record_from_listing(row, self._item_registry) for row in own],
            action=CONSIGNMENT_ACTION_LIST,
        ))
        LOG.info(
            'CONSIGNMENT_LIST_SUCCESS user=%r role_id=%d item_id=%d quantity=%d unit_price=%d',
            username, role_id,
            int(result.listing['item_instance_id']),
            quantity, unit_price,
        )
        return RouteResult.handled(tuple(updates))

    # ------------------------------------------------------------------
    # 下架
    # ------------------------------------------------------------------
    def _handle_unlist(self, context: SystemContext, role, role_id: int, fields) -> RouteResult:
        item_id = int(fields[1].value)
        object_type = int(fields[2].value)
        requested_role = int(fields[3].value)
        if (
            role is None
            or object_type != CONSIGNMENT_OBJECT_ITEM
        ):
            return RouteResult.handled((top_message_frame('下架请求无效'),))
        result = self.service.unlist(role, item_id)
        if not result.ok:
            return RouteResult.handled((top_message_frame('下架失败：' + result.reason),))
        return RouteResult.handled((
            consignment_remove_owned_frame(item_id),
            item_frame(result.item, self._item_registry, operation=3),
        ))

    # ------------------------------------------------------------------
    # 购买
    # ------------------------------------------------------------------
    def _handle_buy(self, context: SystemContext, role, role_id: int, fields) -> RouteResult:
        username = context.username
        item_id = int(fields[1].value)
        requested_buyer = int(fields[2].value)
        if role is None:
            return RouteResult.handled((top_message_frame('购买请求无效'),))
        result = self.service.buy(role, item_id)
        if not result.ok:
            return RouteResult.handled((top_message_frame('购买失败：' + result.reason),))
        silver = int(role.get('currencies', {}).get('silver', 0))
        frames = (
            consignment_remove_market_frame(item_id),
            item_frame(result.item, self._item_registry, operation=3),
            character_appearance_frame(role_id, {50: silver}),
        )
        transaction_id = int((result.transaction or {}).get('transaction_id', 0))
        LOG.info(
            'TRADE_COMPLETED transaction_id=%d user=%r buyer_role_id=%d item_id=%d total=%d silver=%d',
            transaction_id, username, role_id, item_id,
            result.total_price, silver,
        )
        return RouteResult.handled(frames)

    # ------------------------------------------------------------------
    # 寄售商人对话（由地图系统的 2031/2032 交互回调）
    # ------------------------------------------------------------------
    def npc_dialogue_frames(self, npc, role, settings) -> list[bytes]:
        """Build the APK's native consignment-merchant dialogue (screen 6).

        Screen 6 (2032) remains the native NPC dialogue overlay. The options
        cover the full consignment feature set:

        - 寄售商场    -> screen 613 购买物品 mode (market browse + buy)
        - 我的寄售    -> screen 70 已寄售物品 (native 添加物品/添加宠物 -> 1138
                        action 9 上架、下架、取回)
        - 仙晶交易所  -> claimed by the exchange system (screen 350, 1083)
        - 寄售仙晶    -> exchange system: screen 351 卖出仙晶下单页 (1083)
        - 求购仙晶    -> exchange system: screen 351 买入仙晶下单页 (1083)
        """
        from protocol import byte, encode_frame, integer, short, string
        if str(getattr(npc, 'service', '')) != 'consignment_merchant':
            return None

        def dialogue_record(kind: int, *, option_id: int = 0, text: str = '', icon: int = 0):
            return [
                integer(0),
                integer(0),
                integer(0),
                short(0),
                integer(option_id),
                byte(kind),
                string(text),
                integer(icon),
            ]

        introduction = str(
            getattr(npc, 'introduction', '') or getattr(npc, 'label', '') or getattr(npc, 'name', '')
        )
        records = [*dialogue_record(1, text=introduction)]
        for option_id, text in (
            (CONSIGNMENT_MERCHANT_OPTION, '寄售商场'),
            (CONSIGNMENT_MY_LISTINGS_OPTION, '我的寄售'),
            (EXCHANGE_MERCHANT_DIALOGUE_OPTION, '仙晶交易所'),
            (EXCHANGE_SELL_DIALOGUE_OPTION, '寄售仙晶'),
            (EXCHANGE_BUY_DIALOGUE_OPTION, '求购仙晶'),
        ):
            records.extend(dialogue_record(2, option_id=option_id, text=text))
        records.extend(dialogue_record(2, option_id=0, text='结束对话'))
        records.extend(dialogue_record(100))
        return [encode_frame(2032, [
            integer(int(npc.id)),
            byte(len(records) // 8),
            *records,
        ])]

    def npc_dialogue_option(self, settings, role, state, option_id: int, input_text: str = '') -> list[bytes]:
        """Route the consignment merchant's dialogue options.

        Option 1 opens the native market (screen 613 购买物品 mode); option 2
        opens the native 已寄售物品 screen 70 whose 添加物品/添加宠物 buttons
        expose the native consignment path (bag/pet picker -> price input ->
        1138 action 9). Option 3 (仙晶交易所) is left to the exchange system's
        hook.
        """
        from systems.map.protocol import (
            map_npc_for_object_id, map_object_interaction_ack_frame,
        )
        from systems.map.service import settings_for_role
        if role is None or int(option_id) not in (
            CONSIGNMENT_MERCHANT_OPTION,
            CONSIGNMENT_MY_LISTINGS_OPTION,
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

        try:
            if int(option_id) == CONSIGNMENT_MY_LISTINGS_OPTION:
                LOG.info(
                    'CONSIGNMENT_MY_LISTINGS_OPEN role_id=%d npc_id=%d screen=70 protocol=1138',
                    int(role.get('id', 0)),
                    int(npc.id),
                )
                return [
                    map_object_interaction_ack_frame(0),
                    consignment_my_screen_frame(),
                ]
            LOG.info(
                'CONSIGNMENT_MERCHANT_OPEN role_id=%d npc_id=%d screen=613 protocol=1138 categories=28',
                int(role.get('id', 0)),
                int(npc.id),
            )
            return [
                map_object_interaction_ack_frame(0),
                consignment_screen_frame(),
                consignment_category_frame(),
            ]
        finally:
            state.clear()


def register_consignment_routes(router: SystemRouter, system: ConsignmentSystem) -> None:
    router.register(system.system_name, system.can_handle, system.handle)
