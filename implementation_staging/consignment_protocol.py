"""Protocol helpers for the APK's native consignment (寄售) UI.

Reverse-engineering notes for ``piaomiao_local_login.apk``:
- screen 613 -> pmsj/work/e/ev (寄售商人)
- message 1138 -> consignment protocol
- action 3 -> native category list on screen 613
- action 13 -> quality-count selector on screen 44 (pmsj/work/e/r)
- action 1 -> actual market records on screen 73 (pmsj/work/e/p)
- action 7/9 -> own-listing records on screen 70 (pmsj/work/e/t)
- action 12/16 -> remove a purchased row from screen 73
- action 14/15 -> remove an unlisted row from screen 70

This module owns only the wire contract. Business state lives in
``consignment_service.py``.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

from protocol import (
    TYPE_BYTE,
    TYPE_INT,
    TYPE_SHORT,
    Field,
    byte,
    encode_frame,
    integer,
    short,
    string,
)


CONSIGNMENT_MESSAGE_ID = 1138
CONSIGNMENT_SCREEN_ID = 613
CONSIGNMENT_OPEN_ACTION = 69

# Confirmed C->S/S->C actions.
CONSIGNMENT_ACTION_BROWSE_LIST = 1
CONSIGNMENT_ACTION_UNLIST = 2
CONSIGNMENT_ACTION_REFRESH_MERCHANT = 3
CONSIGNMENT_ACTION_BUY = 4
CONSIGNMENT_ACTION_MY_LISTINGS = 7
CONSIGNMENT_ACTION_LIST = 9
CONSIGNMENT_ACTION_PURCHASE_REMOVED = 12
CONSIGNMENT_ACTION_QUALITY_COUNTS = 13
CONSIGNMENT_ACTION_UNLISTED = 14

# Compatibility alias retained for the earlier category implementation.
CONSIGNMENT_ACTION_BROWSE = CONSIGNMENT_ACTION_QUALITY_COUNTS

CONSIGNMENT_OBJECT_ITEM = 1
CONSIGNMENT_OBJECT_PET = 3

# APK pmsj/work/a/n.<clinit> contains the native 28-entry item-consignment
# category table. Screen 613/ev renders action-3 records as [id, name] and
# sends the selected id back through 1138 [BYTE 13, BYTE category_id].
CONSIGNMENT_ITEM_CATEGORIES = (
    '所有武器', '长枪', '折扇', '环器', '棍杖', '双刃', '爪刺', '剑', '刀', '笔',
    '长斧', '灯枪', '半月', '双斧', '头盔', '肩甲', '铠甲', '腰带', '腿甲', '项链',
    '披风', '护腕', '鞋子', '戒指', '坐骑', '外套', '道具', '材料',
)


@dataclass(frozen=True)
class ConsignmentRequest:
    action: int
    item_instance_id: int = 0
    object_type: int = 0
    role_id: int = 0
    quantity: int = 0
    unit_price: int = 0
    category_id: int = -1
    mode: int = 0
    page: int = 0
    page_size: int = 0


def _typed(field: Field, type_id: int) -> bool:
    return field.type_id == type_id


def parse_consignment_request(fields: list[Field]) -> ConsignmentRequest:
    """Parse only APK-confirmed 1138 client request shapes.

    Raises ``ValueError`` for malformed or currently unsupported shapes rather
    than guessing missing fields.
    """
    if not fields or not _typed(fields[0], TYPE_BYTE):
        raise ValueError('寄售请求缺少 BYTE action')
    action = int(fields[0].value)

    if action == CONSIGNMENT_ACTION_LIST:
        if not (
            len(fields) == 6
            and _typed(fields[1], TYPE_INT)
            and _typed(fields[2], TYPE_BYTE)
            and _typed(fields[3], TYPE_INT)
            and _typed(fields[4], TYPE_BYTE)
            and _typed(fields[5], TYPE_INT)
        ):
            raise ValueError('寄售上架请求格式非法')
        return ConsignmentRequest(
            action=action,
            item_instance_id=int(fields[1].value),
            object_type=int(fields[2].value),
            role_id=int(fields[3].value),
            quantity=int(fields[4].value),
            unit_price=int(fields[5].value),
        )

    if action == CONSIGNMENT_ACTION_QUALITY_COUNTS:
        if not (
            len(fields) == 2
            and _typed(fields[1], TYPE_BYTE)
            and 0 <= int(fields[1].value) < len(CONSIGNMENT_ITEM_CATEGORIES)
        ):
            raise ValueError('寄售分类请求格式非法')
        return ConsignmentRequest(action=action, category_id=int(fields[1].value))

    if action == CONSIGNMENT_ACTION_BROWSE_LIST:
        if not (
            len(fields) == 5
            and _typed(fields[1], TYPE_INT)
            and _typed(fields[2], TYPE_INT)
            and _typed(fields[3], TYPE_SHORT)
            and _typed(fields[4], TYPE_BYTE)
        ):
            raise ValueError('寄售列表请求格式非法')
        return ConsignmentRequest(
            action=action,
            role_id=int(fields[1].value),
            mode=int(fields[2].value),
            page=int(fields[3].value),
            page_size=int(fields[4].value),
        )

    if action == CONSIGNMENT_ACTION_MY_LISTINGS:
        if not (len(fields) == 2 and _typed(fields[1], TYPE_INT)):
            raise ValueError('我的寄售请求格式非法')
        return ConsignmentRequest(action=action, role_id=int(fields[1].value))

    if action == CONSIGNMENT_ACTION_UNLIST:
        if not (
            len(fields) == 4
            and _typed(fields[1], TYPE_INT)
            and _typed(fields[2], TYPE_BYTE)
            and _typed(fields[3], TYPE_INT)
        ):
            raise ValueError('寄售下架请求格式非法')
        return ConsignmentRequest(
            action=action,
            item_instance_id=int(fields[1].value),
            object_type=int(fields[2].value),
            role_id=int(fields[3].value),
        )

    if action == CONSIGNMENT_ACTION_BUY:
        if not (
            len(fields) == 3
            and _typed(fields[1], TYPE_INT)
            and _typed(fields[2], TYPE_INT)
        ):
            raise ValueError('寄售购买请求格式非法')
        return ConsignmentRequest(
            action=action,
            item_instance_id=int(fields[1].value),
            role_id=int(fields[2].value),
        )

    if action == CONSIGNMENT_ACTION_REFRESH_MERCHANT and len(fields) == 1:
        return ConsignmentRequest(action=action)

    raise ValueError(f'未支持的寄售 action={action}')


def consignment_category_frame() -> bytes:
    """S->C 1138/action 3: native screen-613 item category list."""
    fields = [byte(CONSIGNMENT_ACTION_REFRESH_MERCHANT), byte(len(CONSIGNMENT_ITEM_CATEGORIES))]
    for category_id, name in enumerate(CONSIGNMENT_ITEM_CATEGORIES):
        fields.extend((byte(category_id), string(name)))
    return encode_frame(CONSIGNMENT_MESSAGE_ID, fields)


def is_consignment_category_request(fields: list[Field]) -> bool:
    """C->S 1138 [BYTE 3] emitted by the native merchant category view."""
    try:
        request = parse_consignment_request(fields)
    except ValueError:
        return False
    return request.action == CONSIGNMENT_ACTION_REFRESH_MERCHANT


def is_consignment_browse_request(fields: list[Field]) -> bool:
    """Compatibility predicate for C->S action13 category selection."""
    try:
        request = parse_consignment_request(fields)
    except ValueError:
        return False
    return request.action == CONSIGNMENT_ACTION_QUALITY_COUNTS


def consignment_quality_counts_frame(counts: Iterable[int]) -> bytes:
    """S->C action13 consumed by screen44.

    The first count is “全部品质”, followed by the five native quality rows.
    """
    values = [max(0, int(value)) for value in counts]
    if len(values) > 255:
        raise ValueError('寄售品质计数过多')
    return encode_frame(
        CONSIGNMENT_MESSAGE_ID,
        [byte(CONSIGNMENT_ACTION_QUALITY_COUNTS), byte(len(values)), *(integer(v) for v in values)],
    )


def _listing_values(listing: dict[str, Any], registry: Any) -> tuple[int, int, int, int, int, str, int, str]:
    item = listing.get('item')
    if not isinstance(item, dict):
        # Historical rows may clear escrow after completion; active wire rows
        # must still carry the persisted template/id metadata.
        item = {
            'id': int(listing.get('item_instance_id', 0)),
            'template_id': int(listing.get('template_id', 0)),
            'quantity': int(listing.get('quantity', 1)),
        }
    resolved = registry.resolve(item)
    quantity = max(1, int(listing.get('quantity', item.get('quantity', 1))))
    total_price = max(0, int(listing.get('unit_price', 0))) * quantity
    seller_name = str(listing.get('seller_name', ''))
    return (
        int(listing.get('object_type', CONSIGNMENT_OBJECT_ITEM)),
        int(listing.get('item_instance_id', item.get('id', 0))),
        int(listing.get('template_id', item.get('template_id', 0))),
        quantity,
        total_price,
        seller_name,
        int(resolved.get('icon_code', resolved.get('quality', 0))),
        seller_name,
    )


def consignment_browse_frame(
    listings: Iterable[dict[str, Any]],
    registry: Any,
    *,
    total: int | None = None,
    page_start: int = 0,
) -> bytes:
    """S->C action1: actual market records consumed by screen73.

    Header fields are action, total-count, page/start metadata, batch-count.
    Every record is exactly eight fields, matching ``pmsj/work/e/p.a(w)``.
    """
    rows = list(listings)
    fields: list[Field] = [
        byte(CONSIGNMENT_ACTION_BROWSE_LIST),
        integer(len(rows) if total is None else max(0, int(total))),
        integer(max(0, int(page_start))),
        integer(len(rows)),
    ]
    for listing in rows:
        object_type, item_id, template_id, quantity, price, owner, icon, seller = _listing_values(listing, registry)
        fields.extend((
            integer(object_type),
            integer(item_id),
            integer(template_id),
            integer(quantity),
            integer(price),
            string(owner),
            integer(icon),
            string(seller),
        ))
    return encode_frame(CONSIGNMENT_MESSAGE_ID, fields)


def _own_listing_fields(listing: dict[str, Any], registry: Any) -> tuple[Field, ...]:
    object_type, item_id, template_id, quantity, price, owner, icon, _seller = _listing_values(listing, registry)
    return (
        integer(object_type),
        integer(item_id),
        integer(template_id),
        integer(quantity),
        integer(price),
        string(owner),
        integer(icon),
    )


def consignment_my_listings_frame(listings: Iterable[dict[str, Any]], registry: Any) -> bytes:
    """S->C action7: current role's active consignment records."""
    rows = list(listings)
    if len(rows) > 255:
        rows = rows[:255]
    fields: list[Field] = [byte(CONSIGNMENT_ACTION_MY_LISTINGS), byte(len(rows))]
    for listing in rows:
        fields.extend(_own_listing_fields(listing, registry))
    return encode_frame(CONSIGNMENT_MESSAGE_ID, fields)


def consignment_listed_frame(listing: dict[str, Any], registry: Any) -> bytes:
    """S->C action9: append one successfully listed item to screen70."""
    return encode_frame(
        CONSIGNMENT_MESSAGE_ID,
        [byte(CONSIGNMENT_ACTION_LIST), byte(1), *_own_listing_fields(listing, registry)],
    )


def consignment_purchase_removed_frame(item_instance_id: int) -> bytes:
    """S->C action12: remove a purchased row from screen73."""
    return encode_frame(
        CONSIGNMENT_MESSAGE_ID,
        [byte(CONSIGNMENT_ACTION_PURCHASE_REMOVED), integer(int(item_instance_id))],
    )


def consignment_unlisted_frame(item_instance_id: int) -> bytes:
    """S->C action14: remove one unlisted row from screen70."""
    return encode_frame(
        CONSIGNMENT_MESSAGE_ID,
        [byte(CONSIGNMENT_ACTION_UNLISTED), integer(int(item_instance_id))],
    )


def consignment_failure_frame(action: int) -> bytes:
    """Return the smallest structurally safe response for a failed operation."""
    if action == CONSIGNMENT_ACTION_BROWSE_LIST:
        return encode_frame(CONSIGNMENT_MESSAGE_ID, [byte(action), integer(0), integer(0), integer(0)])
    if action in {
        CONSIGNMENT_ACTION_REFRESH_MERCHANT,
        CONSIGNMENT_ACTION_MY_LISTINGS,
        CONSIGNMENT_ACTION_LIST,
        CONSIGNMENT_ACTION_QUALITY_COUNTS,
    }:
        return encode_frame(CONSIGNMENT_MESSAGE_ID, [byte(action), byte(0)])
    return encode_frame(CONSIGNMENT_MESSAGE_ID, [byte(action)])


def consignment_screen_frame(*, mode: int = 0) -> bytes:
    """Open the APK's original screen 613 (pmsj.work.e.ev / 寄售商人)."""
    return encode_frame(
        1010,
        [
            integer(0),
            short(0),
            short(0),
            integer(mode),
            integer(CONSIGNMENT_SCREEN_ID),
            short(CONSIGNMENT_OPEN_ACTION),
        ],
    )


def empty_consignment_result_frame(action: int) -> bytes:
    """Compatibility wrapper for older callers returning an empty result."""
    return consignment_failure_frame(int(action))
