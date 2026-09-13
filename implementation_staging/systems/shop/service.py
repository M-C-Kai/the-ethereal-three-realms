from __future__ import annotations

import copy
from dataclasses import dataclass
from typing import Callable

from protocol import byte, encode_frame, integer, short
from systems.shop.registry import MAX_SHOP_PURCHASE_QUANTITY, ShopDefinition
from systems.shop.protocol import ShopProtocol, shop_purchase_ack_frame

MAX_CURRENCY_BALANCE = 2_147_483_647
DEFAULT_BAG_CAPACITY = 1000


@dataclass(frozen=True)
class ShopPurchaseResult:
    frames: tuple[bytes, ...]
    changed: bool
    reason: str = ''


def _role_items(role):
    items = role.get('items')
    if not isinstance(items, list):
        items = []
        role['items'] = items
    return items


def _balance(value):
    try:
        return max(0, min(MAX_CURRENCY_BALANCE, int(value)))
    except (TypeError, ValueError):
        return 0


def _allocate_item_instance_id(role):
    used = set()
    for item in _role_items(role):
        try:
            item_id = int(item.get('id', 0))
        except (TypeError, ValueError):
            continue
        if item_id > 0:
            used.add(item_id)
    candidate = max(1, int(role.get('id', 0)) * 10_000)
    while candidate in used:
        candidate += 1
    return candidate


def _currency_frame(role_id, property_id, value):
    return encode_frame(1017, [byte(0), integer(role_id), integer(1), byte(property_id), integer(value)])


def _minimal_item_frame(item, item_registry):
    definition = item_registry.require(int(item['template_id']))
    return encode_frame(1008, [byte(3), integer(int(item['id'])), short(int(item.get('quantity', 1))), short(int(definition.max_quantity))])


def shop_purchase_result(role, shop: ShopDefinition, category_id, template_id, quantity, item_registry=None, *, bag_capacity=None, item_frame_factory=None):
    if item_registry is None:
        from systems.inventory.registry import default_item_registry
        item_registry = default_item_registry()
    category = shop.category(int(category_id))
    if category is None:
        return ShopPurchaseResult((), False, '商城分类不存在')
    goods = shop.find_goods(int(category_id), int(template_id))
    if goods is None:
        return ShopPurchaseResult((), False, '商品不存在')
    if type(quantity) is not int or quantity <= 0:
        return ShopPurchaseResult((), False, '购买数量非法')
    if quantity > MAX_SHOP_PURCHASE_QUANTITY:
        return ShopPurchaseResult((), False, '购买数量超出上限')
    total = goods.price * quantity
    if total > MAX_CURRENCY_BALANCE:
        return ShopPurchaseResult((), False, '订单金额超出上限')
    currencies = role.get('currencies')
    if not isinstance(currencies, dict):
        currencies = {}
        role['currencies'] = currencies
    balance = _balance(currencies.get(shop.currency_name))
    if balance < total:
        return ShopPurchaseResult((), False, '货币不足')
    definition = item_registry.require(int(template_id))
    max_quantity = int(definition.max_quantity)
    stack = next((item for item in _role_items(role) if int(item.get('template_id', 0)) == int(template_id) and item.get('location', 'bag') == 'bag'), None) if max_quantity > 1 else None
    if stack is not None and int(stack.get('quantity', 1)) + quantity > max_quantity:
        return ShopPurchaseResult((), False, '超出物品堆叠上限')
    capacity = bag_capacity(role) if bag_capacity else int(role.get('bag_capacity', DEFAULT_BAG_CAPACITY))
    if stack is None and sum(1 for item in _role_items(role) if item.get('location', 'bag') == 'bag') >= capacity:
        return ShopPurchaseResult((), False, '背包已满')
    balance_after = balance - total
    currencies[shop.currency_name] = balance_after
    if stack is not None:
        stack['quantity'] = int(stack.get('quantity', 1)) + quantity
        purchased = stack
    else:
        purchased = {'id': _allocate_item_instance_id(role), 'template_id': int(template_id), 'quantity': quantity, 'location': 'bag'}
        _role_items(role).append(purchased)
    frame_factory = item_frame_factory or _minimal_item_frame
    return ShopPurchaseResult((
        _currency_frame(int(role.get('id', 0)), shop.currency_property, balance_after),
        frame_factory(purchased, item_registry),
        shop_purchase_ack_frame(),
    ), True)


class ShopService:
    """商店购买规则、持久化和失败回滚。"""

    def __init__(self, shop_registry, item_registry, save: Callable[[], None], bag_capacity=None, item_frame_factory=None):
        self.shop_registry = shop_registry
        self.item_registry = item_registry
        self.save = save
        self.bag_capacity = bag_capacity
        self.item_frame_factory = item_frame_factory

    def purchase(self, role, fields, *, mode=0, category_id=0):
        if not ShopProtocol.is_shop_purchase_request(fields):
            return ShopPurchaseResult((), False, '购买请求格式非法')
        shop = self.shop_registry.by_mode(mode)
        if shop is None:
            return ShopPurchaseResult((), False, '当前不在商城')
        if int(fields[0].value) != shop.shop_id:
            return ShopPurchaseResult((), False, '商店与当前商城不匹配')
        snapshot = copy.deepcopy(role)
        try:
            result = shop_purchase_result(
                role, shop, category_id, int(fields[2].value), int(fields[3].value),
                item_registry=self.item_registry,
                bag_capacity=self.bag_capacity,
                item_frame_factory=self.item_frame_factory,
            )
            if result.changed:
                self.save()
            return result
        except Exception:
            role.clear()
            role.update(snapshot)
            raise
