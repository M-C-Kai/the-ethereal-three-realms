from __future__ import annotations

import logging
from dataclasses import dataclass

from app.context import SystemContext
from app.router import RouteResult, SystemRouter
from systems.shop.protocol import (
    MALL_TAB_TO_DP_MODE,
    ShopProtocol,
    mall_category_list_frame,
    mall_title_frame,
    shop_goods_list_frame,
    shop_screen_bridge_frame,
)
from systems.shop.service import ShopService


LOG = logging.getLogger('piaomiao-local')


@dataclass
class ShopSession:
    mode: int = 0
    category_id: int = 0


@dataclass(frozen=True)
class ShopHandleResult:
    handled: bool
    frames: tuple[bytes, ...] = ()
    reason: str = ''


class ShopSystem:
    """shop 系统边界。"""

    system_name = 'shop'
    protocol = ShopProtocol()

    def __init__(self, shop_registry=None, item_registry=None, save=None, bag_capacity=None, item_frame_factory=None) -> None:
        self.service = None
        if shop_registry is not None:
            self.service = ShopService(shop_registry, item_registry, save, bag_capacity, item_frame_factory)

    def can_handle(self, _context: SystemContext, message_id: int, _fields: list[object]) -> bool:
        return message_id in (1033, 1067)

    def handle(self, context: SystemContext, message_id: int, fields: list[object]) -> RouteResult:
        """Full 1033/1067 shop entry: connection mall state lives in the session."""
        session = context.session
        shop_session = session.get('shop')
        if not isinstance(shop_session, ShopSession):
            shop_session = ShopSession()
            session['shop'] = shop_session
        result = self.handle_message(message_id, fields, context.active_role, shop_session)
        if result.frames:
            return RouteResult.handled(result.frames)
        LOG.info(
            'ignored shop message=%d role=%r reason=%r',
            message_id,
            (context.active_role or {}).get('id') if context.active_role else None,
            result.reason,
        )
        return RouteResult.not_handled(reason=result.reason)

    def handle_purchase(
        self,
        role: dict[str, object],
        fields: list[object],
        *,
        mode: int = 0,
        category_id: int = 0,
    ) -> object:
        if self.service is None:
            raise RuntimeError('shop service is not configured')
        return self.service.purchase(role, fields, mode=mode, category_id=category_id)

    def handle_message(self, message_id, fields, role, session: ShopSession) -> ShopHandleResult:
        if self.service is None:
            raise RuntimeError('shop service is not configured')
        protocol = self.protocol
        if message_id == 1067 and (protocol.is_mall_category_request(fields) or protocol.is_mall_title_request(fields)):
            tab_mode = int(fields[2].value)
            shop = self.service.shop_registry.find_bk_mode(tab_mode)
            if shop is None:
                return ShopHandleResult(True, reason='unknown_mall_mode')
            session.mode = MALL_TAB_TO_DP_MODE[tab_mode]
            session.category_id = 0
            frame = mall_category_list_frame(shop.categories) if protocol.is_mall_category_request(fields) else mall_title_frame(shop.name)
            return ShopHandleResult(True, (frame,))
        if message_id == 1067 and protocol.is_mall_open_category_request(fields):
            shop = self.service.shop_registry.by_mode(session.mode)
            category_id = int(fields[2].value)
            if shop is None or shop.category(category_id) is None:
                return ShopHandleResult(True, reason='unknown_category')
            session.category_id = category_id
            return ShopHandleResult(True, (shop_screen_bridge_frame(session.mode),))
        if message_id == 1033 and protocol.is_shop_list_request(fields):
            shop = self.service.shop_registry.by_mode(session.mode)
            category = shop.category(session.category_id) if shop is not None else None
            if role is None or shop is None or category is None:
                return ShopHandleResult(True, reason='no_mall_session')
            if int(fields[0].value) != shop.shop_id:
                return ShopHandleResult(True, reason='shop_mismatch')
            return ShopHandleResult(True, (shop_goods_list_frame(shop, category, self.service.item_registry),))
        if message_id == 1033 and protocol.is_shop_purchase_request(fields):
            if role is None:
                return ShopHandleResult(True, reason='no_active_role')
            result = self.service.purchase(role, fields, mode=session.mode, category_id=session.category_id)
            return ShopHandleResult(True, result.frames, result.reason)
        return ShopHandleResult(False)


def register_shop_routes(router: SystemRouter, system: ShopSystem) -> None:
    router.register(system.system_name, system.can_handle, system.handle)
