"""Protocol 1083 wire helpers for the APK's native 仙晶交易所.

Reverse-engineered routing (APK ``pmsj/work/main/e.p(w)`` receive hook):

- action 0 / 3 / 4 / 5 / 6 -> screen 350 (``pmsj.work.e.ad``, order market)
- action 10 .. 17          -> screen 351 (``pmsj.work.e.ac``, order entry)

Client request points confirmed in smali:

- screen 350 ``y(I)``: ``[4, tab]`` tab captions, ``[5, tab]`` own order ids,
  ``[0, page, size, tab]`` order rows.
- screen 350 row menu 出售/购买 confirm: ``[3, order_id]`` (应单).
- screen 351 ``y(I)``: ``[10, mode]`` (mode 0 = 买入仙晶, 1 = 卖出仙晶).
- screen 351 fee button: ``[12, mode, num, price]`` (委托费用查询).
- screen 351 submit confirm: ``[15, num, price]`` (出售单) / ``[16, num, price]``
  (求购单); cancel menu 撤单: ``[13, order_id]``; pager: ``[11, page, size, mode]``.

The client parses concrete field types at fixed payload indexes, so every
builder below keeps BYTE/SHORT/INT/STRING types explicit.
"""

from __future__ import annotations

from typing import Iterable, Mapping, Sequence
from datetime import datetime, timezone, timedelta

from protocol import (
    TYPE_BYTE,
    TYPE_INT,
    TYPE_STRING,
    byte,
    encode_frame,
    integer,
    short,
    string,
)


EXCHANGE_MESSAGE_ID = 1083
EXCHANGE_MARKET_SCREEN_ID = 350
EXCHANGE_ENTRY_SCREEN_ID = 351
EXCHANGE_OPEN_ACTION = 69

EXCHANGE_TAB_BUY_ORDERS = 0
EXCHANGE_TAB_SELL_ORDERS = 1
EXCHANGE_TAB_NAMES = ('玩家求购单', '玩家出售单')
EXCHANGE_MODE_BUY = 0
EXCHANGE_MODE_SELL = 1

EXCHANGE_FOOTER = (
    '【玩家求购单】全服所有需要购入仙晶的订单(包括自己的求购单，'
    '但无法交易自己的订单)都显示在此处，您可以在此处应单，'
    '把自己的仙晶出售给订单发布者，以获取银两。'
    '【玩家出售单】全服所有想要卖出仙晶的订单(包括自己的出售单，'
    '但无法交易自己的订单)都显示在此处，您可以在此处应单，'
    '用银两购买到相应仙晶。'
)

# Field type layout of one row in the two order-list payloads.  The client
# reads field 0 with INT and renders fields 1..3 via Object.toString(), so the
# descriptive columns are transmitted as STRING fields.  Field order matters:
# screen 350's accept dialog reads field 1 as crystal amount and field 3 as
# the silver amount ("出售{1}个仙晶换取{3}银两？").
MARKET_ROW_TYPES = (TYPE_INT, TYPE_STRING, TYPE_STRING, TYPE_STRING)


EXCHANGE_ACTION_MARKET_ROWS = 0
EXCHANGE_ACTION_ACCEPT = 3
EXCHANGE_ACTION_TABS = 4
EXCHANGE_ACTION_MY_IDS = 5
EXCHANGE_ACTION_ROW_REMOVED = 6
EXCHANGE_ACTION_ENTRY_ROWS = 10
EXCHANGE_ACTION_MY_ORDERS = 11
EXCHANGE_ACTION_FEE = 12
EXCHANGE_ACTION_CANCEL = 13
EXCHANGE_ACTION_POST_BUY = 16
EXCHANGE_ACTION_POST_SELL = 15


def _exact(fields: list, types: tuple[int, ...], action: int) -> bool:
    return bool(
        len(fields) == len(types)
        and all(field.type_id == expected for field, expected in zip(fields, types))
        and int(fields[0].value) == int(action)
    )


def is_market_rows_request(fields: list) -> bool:
    """screen 350 pager: [0, page, size, tab]."""
    return _exact(fields, (TYPE_BYTE,) * 4, EXCHANGE_ACTION_MARKET_ROWS)


def is_accept_request(fields: list) -> bool:
    """screen 350 应单 confirm: [3, order_id]."""
    return _exact(fields, (TYPE_BYTE, TYPE_INT), EXCHANGE_ACTION_ACCEPT)


def is_tabs_request(fields: list) -> bool:
    """screen 350 open: [4, tab]."""
    return _exact(fields, (TYPE_BYTE, TYPE_BYTE), EXCHANGE_ACTION_TABS)


def is_my_ids_request(fields: list) -> bool:
    """screen 350 column-header request: [5, tab] (legacy function name)."""
    return _exact(fields, (TYPE_BYTE, TYPE_BYTE), EXCHANGE_ACTION_MY_IDS)


def is_entry_page_request(fields: list) -> bool:
    """screen 351 open/refresh: [10, mode]."""
    return _exact(fields, (TYPE_BYTE, TYPE_BYTE), EXCHANGE_ACTION_ENTRY_ROWS)


def is_my_orders_request(fields: list) -> bool:
    """screen 351 pager: [11, page, size, mode]."""
    return _exact(fields, (TYPE_BYTE,) * 4, EXCHANGE_ACTION_MY_ORDERS)


def is_fee_request(fields: list) -> bool:
    """screen 351 fee query: [12, mode, num, price]."""
    return _exact(fields, (TYPE_BYTE, TYPE_BYTE, TYPE_INT, TYPE_INT), EXCHANGE_ACTION_FEE)


def is_cancel_request(fields: list) -> bool:
    """screen 351 撤单: [13, order_id]."""
    return _exact(fields, (TYPE_BYTE, TYPE_INT), EXCHANGE_ACTION_CANCEL)


def is_post_buy_request(fields: list) -> bool:
    """screen 351 buy-order confirm (event 3): [16, num, price]."""
    return _exact(fields, (TYPE_BYTE, TYPE_INT, TYPE_INT), EXCHANGE_ACTION_POST_BUY)


def is_post_sell_request(fields: list) -> bool:
    """screen 351 sell-order confirm (event 4): [15, num, price]."""
    return _exact(fields, (TYPE_BYTE, TYPE_INT, TYPE_INT), EXCHANGE_ACTION_POST_SELL)


def market_row_fields(order: Mapping[str, object]) -> list:
    """One order row: [INT id, STRING crystals, STRING name, STRING silver]."""
    return [
        integer(int(order['order_id'])),
        string(str(int(order['crystals']))),
        string(str(order.get('poster_name', ''))),
        string(str(int(order['crystals']) * int(order['unit_price']))),
    ]


def my_order_row_fields(order: Mapping[str, object]) -> list:
    """screen 351 row: [INT id, STRING price, STRING crystals, STRING time].

    The renderer shows field 2 as the row caption, field 1 in the second
    column and field 3 on the right.
    """
    return [
        integer(int(order['order_id'])),
        string(str(int(order['unit_price']))),
        string(str(int(order['crystals']))),
        string(datetime.fromtimestamp(int(order.get('created_at', 0)),
                                     timezone(timedelta(hours=8))).strftime('%m-%d %H:%M')),
    ]


def exchange_market_frame(
    tab: int,
    orders: Sequence[Mapping[str, object]],
    total: int | None = None,
) -> bytes:
    """S->C action 0: one market page for ``tab`` (求购单/出售单).

    ``total`` is the full row count across pages; the client uses it for its
    pager while ``orders`` carries only the rows of the requested page.
    """
    rows = list(orders)
    fields: list = [
        byte(EXCHANGE_ACTION_MARKET_ROWS),
        short(len(rows) if total is None else max(0, int(total))),
        byte(len(rows)),
        byte(int(tab)),
    ]
    for order in rows:
        fields.extend(market_row_fields(order))
    return encode_frame(EXCHANGE_MESSAGE_ID, fields)


def exchange_tabs_frame() -> bytes:
    """S->C action 4: the two market tabs plus the help footer."""
    fields: list = [
        byte(EXCHANGE_ACTION_TABS),
        byte(len(EXCHANGE_TAB_NAMES)),
    ]
    fields.extend(string(name) for name in EXCHANGE_TAB_NAMES)
    fields.append(string(EXCHANGE_FOOTER))
    return encode_frame(EXCHANGE_MESSAGE_ID, fields)


def exchange_columns_frame(tab: int) -> bytes:
    """ad.a(w) action 5 stores one header vector [tab, left, middle, right]."""
    fields: list = [
        byte(EXCHANGE_ACTION_MY_IDS),
        byte(4),
        integer(int(tab)),
        string('仙晶数量'), string('发布者'), string('银两总额'),
    ]
    return encode_frame(EXCHANGE_MESSAGE_ID, fields)


def exchange_row_removed_frame(tab: int, order_id: int, total: int) -> bytes:
    """S->C action 6: drop one accepted market row on screen 350."""
    return encode_frame(EXCHANGE_MESSAGE_ID, [
        byte(EXCHANGE_ACTION_ROW_REMOVED),
        byte(int(tab)),
        integer(int(order_id)),
        short(max(0, int(total))),
    ])


def exchange_entry_rows_frame(mode: int) -> bytes:
    """S->C action 10: two screen 351 tabs, NOT order summaries.

    ac.a(w) divides the tab control width by this count.  Zero causes an
    exception before main/t.a(false,false) can dismiss the loading overlay.
    Tab 0 is the entry form; tab 1 requests actual order rows via action 11.
    Captions are local compatibility labels for the APK-confirmed tabs.
    """
    tabs = ('买入仙晶', '我的求购') if int(mode) == EXCHANGE_MODE_BUY else ('卖出仙晶', '我的挂售')
    fields: list = [
        byte(EXCHANGE_ACTION_ENTRY_ROWS),
        byte(len(tabs)),
        *(string(tab) for tab in tabs),
        string(EXCHANGE_FOOTER),
    ]
    return encode_frame(EXCHANGE_MESSAGE_ID, fields)


def exchange_my_orders_frame(
    mode: int,
    orders: Sequence[Mapping[str, object]],
    total: int | None = None,
) -> bytes:
    """S->C action 11: paged own-order rows for screen 351."""
    rows = list(orders)
    fields: list = [
        byte(EXCHANGE_ACTION_MY_ORDERS),
        short(len(rows) if total is None else max(0, int(total))),
        byte(len(rows)),
    ]
    for order in rows:
        fields.extend(my_order_row_fields(order))
    return encode_frame(EXCHANGE_MESSAGE_ID, fields)


def exchange_fee_frame(fee_text: str) -> bytes:
    """S->C action 12: 委托费用 answer consumed by screen 351."""
    return encode_frame(EXCHANGE_MESSAGE_ID, [
        byte(EXCHANGE_ACTION_FEE),
        string(fee_text),
    ])


def exchange_accept_rejected_frame() -> bytes:
    """main/e.p -> ad.a(w): action 3 only dismisses the wait overlay."""
    return encode_frame(EXCHANGE_MESSAGE_ID, [byte(EXCHANGE_ACTION_ACCEPT)])


def exchange_cancelled_frame(total: int, order_id: int) -> bytes:
    """S->C action 13: 撤单 ack; the client drops the matching row.

    Field order follows the smali reader: SHORT total at index 1, INT order
    id at index 2.
    """
    return encode_frame(EXCHANGE_MESSAGE_ID, [
        byte(EXCHANGE_ACTION_CANCEL),
        short(max(0, int(total))),
        integer(int(order_id)),
    ])


def exchange_posted_frame(action: int) -> bytes:
    """S->C action 15/16: order accepted; screen 351 clears the inputs."""
    return encode_frame(EXCHANGE_MESSAGE_ID, [byte(int(action))])


def exchange_order_refresh_frame(order: Mapping[str, object], total: int) -> bytes:
    """ac.a(w), action 17: insert a row even when own-order cache is loaded."""
    return encode_frame(EXCHANGE_MESSAGE_ID, [
        byte(17), short(max(0, int(total))), *my_order_row_fields(order),
    ])


def exchange_screen_frame(*, mode: int = EXCHANGE_MODE_BUY) -> bytes:
    """Open the native order market (screen 350) with the given initial tab."""
    return encode_frame(1010, [
        integer(0),
        short(0),
        short(0),
        integer(int(mode)),
        integer(EXCHANGE_MARKET_SCREEN_ID),
        short(EXCHANGE_OPEN_ACTION),
    ])


def exchange_entry_screen_frame(*, mode: int = EXCHANGE_MODE_SELL) -> bytes:
    """Open the native order-entry page (screen 351).

    mode 1 (default) is the 卖出仙晶 page posting sell orders; mode 0 is the
    买入仙晶 page posting buy orders. Screen 351's ``y(I)`` immediately
    requests ``[10, mode]`` which the server answers with caption rows.
    """
    return encode_frame(1010, [
        integer(0),
        short(0),
        short(0),
        integer(int(mode)),
        integer(EXCHANGE_ENTRY_SCREEN_ID),
        short(EXCHANGE_OPEN_ACTION),
    ])
