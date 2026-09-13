"""social 系统业务：好友关系存取、交易结算与切磋/PK 裁决。

帧构造在 protocol.py；本模块只做数据操作与合法性校验，输出
``RouteResult`` 所需的 frames 元组和落盘标记。
"""
from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field

from protocol import byte, encode_frame, integer
from systems.inventory.protocol import find_item, role_items
from systems.inventory.service import bag_capacity, bag_item_count

LOG = logging.getLogger('piaomiao-local')

_DEFAULT_TRADE_CAPACITY = 1000


def friends_of(role: dict[str, object]) -> list[dict[str, object]]:
    """Return the role's live friend list, migrating non-list values in place.

    必须返回角色数据中的同一个 list 对象：增删好友的直接修改才能随
    ``RoleStore.save()`` 一起落盘。
    """
    friends = role.get('friends')
    if not isinstance(friends, list):
        friends = []
        role['friends'] = friends
    friends[:] = [row for row in friends if isinstance(row, dict)]
    return friends


def add_friend(role: dict[str, object], friend_id: int, friend_name: str) -> bool:
    """Insert one friendship row; returns False when already present."""
    friends = friends_of(role)
    if any(int(row.get('id', 0)) == int(friend_id) for row in friends):
        return False
    friends.append({'id': int(friend_id), 'name': str(friend_name)})
    return True


def remove_friend(role: dict[str, object], friend_id: int) -> bool:
    friends = friends_of(role)
    remaining = [row for row in friends if int(row.get('id', 0)) != int(friend_id)]
    if len(remaining) == len(friends):
        return False
    role['friends'] = remaining
    return True


def currency_balance(role: dict[str, object], name: str) -> int:
    currencies = role.get('currencies')
    if not isinstance(currencies, dict):
        return 0
    try:
        return max(0, int(currencies.get(name, 0) or 0))
    except (TypeError, ValueError):
        return 0


def set_currency_balance(role: dict[str, object], name: str, value: int) -> None:
    currencies = role.get('currencies')
    if not isinstance(currencies, dict):
        currencies = {}
        role['currencies'] = currencies
    currencies[name] = max(0, int(value))


def currency_frame(role_id: int, property_id: int, value: int) -> bytes:
    """1017 增量属性帧：刷新一个货币属性（50=银两）。"""
    return encode_frame(1017, [
        byte(0), integer(int(role_id)), integer(1),
        byte(int(property_id)), integer(int(value)),
    ])


def _capacity_of(role: dict[str, object]) -> int:
    """背包容量上限：复用背包系统的标准口径（默认 1000 + 福缘加成）。"""
    try:
        return bag_capacity(role)
    except Exception:
        return _DEFAULT_TRADE_CAPACITY


def _offer_parts(offer: dict[str, object]) -> tuple[int, list[int]]:
    money = offer.get('money', 0)
    try:
        money = max(0, int(money or 0))
    except (TypeError, ValueError):
        money = 0
    item_ids: list[int] = []
    for raw in offer.get('item_ids', []) or []:
        try:
            item_ids.append(int(raw))
        except (TypeError, ValueError):
            continue
    return money, item_ids


@dataclass
class TradeSettlement:
    """一次双方确认后的交易结算结果。

    ``sides``: role_id -> (移出的物品, 收到的物品, 银两增量)。
    """

    ok: bool
    reason: str = ''
    sides: dict[int, tuple[list[dict[str, object]], list[dict[str, object]], int]] = field(
        default_factory=dict,
    )


def settle_trade(
    left: dict[str, object],
    right: dict[str, object],
    left_offer: dict[str, object],
    right_offer: dict[str, object],
) -> TradeSettlement:
    """原子交换双方锁定的物品与银两；任一校验失败则整体放弃。

    ``*_offer`` 为 ``{"money": int, "item_ids": [int]}``，来自各自 1056/20
    确认帧。物品实例只做归属转移（保持实例 id 不变），银两使用 ``silver``；
    先完成全部校验（余额、物品在背包、背包容量、重复提交），再统一落账。
    """
    left_id = int(left['id'])
    right_id = int(right['id'])
    sides = {left_id: left, right_id: right}
    peer_of = {left_id: right_id, right_id: left_id}
    offers = {left_id: left_offer, right_id: right_offer}

    moved_map: dict[int, list[dict[str, object]]] = {}
    money_map: dict[int, int] = {}
    claimed: set[tuple[int, int]] = set()
    for giver_id, giver in sides.items():
        money, item_ids = _offer_parts(offers[giver_id])
        if currency_balance(giver, 'silver') < money:
            return TradeSettlement(False, '银两不足')
        moved: list[dict[str, object]] = []
        for item_id in item_ids:
            if (giver_id, item_id) in claimed:
                return TradeSettlement(False, '物品重复提交')
            item = find_item(giver, item_id)
            if item is None or item.get('location', 'bag') != 'bag':
                return TradeSettlement(False, '物品已不在背包中')
            claimed.add((giver_id, item_id))
            moved.append(item)
        moved_map[giver_id] = moved
        money_map[giver_id] = money

    for giver_id, moved in moved_map.items():
        receiver = sides[peer_of[giver_id]]
        if bag_item_count(receiver) + len(moved) > _capacity_of(receiver):
            return TradeSettlement(False, '对方背包空间不足')

    result: dict[int, tuple[list[dict[str, object]], list[dict[str, object]], int]] = {
        role_id: ([], [], 0) for role_id in sides
    }
    for giver_id, moved in moved_map.items():
        receiver_id = peer_of[giver_id]
        money = money_map[giver_id]
        giver = sides[giver_id]
        receiver = sides[receiver_id]
        items = role_items(giver)
        for item in moved:
            if item in items:
                items.remove(item)
        role_items(receiver).extend(moved)
        if money:
            set_currency_balance(giver, 'silver', currency_balance(giver, 'silver') - money)
            set_currency_balance(receiver, 'silver', currency_balance(receiver, 'silver') + money)
        given, received, delta = result[giver_id]
        result[giver_id] = (given + moved, received, delta - money)
        given, received, delta = result[receiver_id]
        result[receiver_id] = (given, received + moved, delta + money)
    return TradeSettlement(True, '交易完成', result)


def now() -> float:
    return time.time()
