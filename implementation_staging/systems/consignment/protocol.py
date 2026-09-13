"""Protocol 1138 helpers for the APK's native item-consignment UI.

Confirmed APK receive routing in ``pmsj/work/main/e.al(w)``:
- action 1 / 12 / 16 -> screen 73
- action 3 / 22 -> screen 613
- action 7 / 9 / 14 / 15 -> screen 70
- action 13 -> screen 44

The field encoders below keep BYTE/INT/STRING types explicit because the
client reads concrete TLV types at fixed positions.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping

from protocol import TYPE_BYTE, TYPE_INT, Field, byte, encode_frame, integer, short, string
from systems.consignment.registry import CONSIGNMENT_ITEM_CATEGORIES


CONSIGNMENT_MESSAGE_ID = 1138
CONSIGNMENT_SCREEN_ID = 613
# Screen 70 ("已寄售物品") is the native consignment hub: its 添加物品/添加宠物
# buttons open the bag/pet pickers whose per-item 寄售 action submits 1138
# action 9. Opening it from the NPC dialogue is therefore the native
# consignment path.
CONSIGNMENT_MY_SCREEN_ID = 70
CONSIGNMENT_OPEN_ACTION = 69
CONSIGNMENT_ITEM_MODE = 2809
CONSIGNMENT_PET_MODE = 2500

CONSIGNMENT_ACTION_MARKET_LIST = 1
CONSIGNMENT_ACTION_UNLIST = 2
CONSIGNMENT_ACTION_REFRESH_MERCHANT = 3
CONSIGNMENT_ACTION_BUY = 4
CONSIGNMENT_ACTION_MY_LISTINGS = 7
CONSIGNMENT_ACTION_LIST = 9
CONSIGNMENT_ACTION_BROWSE = 13
CONSIGNMENT_ACTION_REMOVE_OWN = 15
CONSIGNMENT_ACTION_REMOVE_MARKET = 16

# After screen 44 is opened by action 13, the native page requests the actual
# market rows with one of these request actions.  The response is action 1.
CONSIGNMENT_MARKET_REQUEST_ACTIONS = frozenset({0, 23})

CONSIGNMENT_OBJECT_ITEM = 1
CONSIGNMENT_OBJECT_PET = 3




@dataclass(frozen=True)
class ConsignmentWireRecord:
    """One APK-native item row used by the market and own-listing screens."""

    object_type: int
    item_instance_id: int
    template_id: int
    quantity: int
    price: int
    display_name: str
    seller_role_id: int
    seller_name: str = ''

    def own_fields(self) -> list[Field]:
        # screen 70 row: 7 fields
        return [
            byte(self.object_type),
            integer(self.item_instance_id),
            integer(self.template_id),
            integer(self.quantity),
            integer(self.price),
            string(self.display_name),
            integer(self.seller_role_id),
        ]

    def market_fields(self) -> list[Field]:
        # screen 73 row: own row + seller display name
        return [*self.own_fields(), string(self.seller_name)]


def wire_record_from_listing(listing: Mapping[str, object]) -> ConsignmentWireRecord:
    return ConsignmentWireRecord(
        object_type=CONSIGNMENT_OBJECT_ITEM,
        item_instance_id=int(listing['item_instance_id']),
        template_id=int(listing['template_id']),
        quantity=int(listing['quantity']),
        price=int(listing['unit_price']) * int(listing['quantity']),
        display_name=str(listing.get('display_name', '')),
        seller_role_id=int(listing['seller_role_id']),
        seller_name=str(listing.get('seller_name', '')),
    )


def _exact(fields: list[Field], types: tuple[int, ...], action: int) -> bool:
    return bool(
        len(fields) == len(types)
        and all(field.type_id == expected for field, expected in zip(fields, types))
        and int(fields[0].value) == int(action)
    )


def is_consignment_category_request(fields: list[Field]) -> bool:
    return _exact(fields, (TYPE_BYTE,), CONSIGNMENT_ACTION_REFRESH_MERCHANT)


def is_consignment_browse_request(fields: list[Field]) -> bool:
    return bool(
        _exact(fields, (TYPE_BYTE, TYPE_BYTE), CONSIGNMENT_ACTION_BROWSE)
        and 0 <= int(fields[1].value) < len(CONSIGNMENT_ITEM_CATEGORIES)
    )


def is_consignment_my_listings_request(fields: list[Field]) -> bool:
    return _exact(fields, (TYPE_BYTE, TYPE_INT), CONSIGNMENT_ACTION_MY_LISTINGS)


def is_consignment_list_item_request(fields: list[Field]) -> bool:
    return bool(
        _exact(
            fields,
            (TYPE_BYTE, TYPE_INT, TYPE_BYTE, TYPE_INT, TYPE_BYTE, TYPE_INT),
            CONSIGNMENT_ACTION_LIST,
        )
        and int(fields[4].value) > 0
        and int(fields[5].value) > 0
    )


def is_consignment_unlist_request(fields: list[Field]) -> bool:
    return _exact(
        fields,
        (TYPE_BYTE, TYPE_INT, TYPE_BYTE, TYPE_INT),
        CONSIGNMENT_ACTION_UNLIST,
    )


def is_consignment_buy_request(fields: list[Field]) -> bool:
    return _exact(fields, (TYPE_BYTE, TYPE_INT, TYPE_INT), CONSIGNMENT_ACTION_BUY)


def is_consignment_market_list_request(fields: list[Field]) -> bool:
    return bool(
        fields
        and len(fields) == 1
        and fields[0].type_id == TYPE_BYTE
        and int(fields[0].value) in CONSIGNMENT_MARKET_REQUEST_ACTIONS
    )


def consignment_category_frame() -> bytes:
    """S->C action 3: screen 613's 28 native item categories."""
    fields: list[Field] = [
        byte(CONSIGNMENT_ACTION_REFRESH_MERCHANT),
        byte(len(CONSIGNMENT_ITEM_CATEGORIES)),
    ]
    for category_id, name in enumerate(CONSIGNMENT_ITEM_CATEGORIES):
        fields.extend((byte(category_id), string(name)))
    return encode_frame(CONSIGNMENT_MESSAGE_ID, fields)


def consignment_category_counts_frame(counts: Iterable[int]) -> bytes:
    """S->C action 13: count/filter vector consumed by native screen 44."""
    values = [max(0, int(value)) for value in counts]
    return encode_frame(
        CONSIGNMENT_MESSAGE_ID,
        [
            byte(CONSIGNMENT_ACTION_BROWSE),
            byte(len(values)),
            *(integer(value) for value in values),
        ],
    )


def consignment_market_list_frame(records: Iterable[ConsignmentWireRecord]) -> bytes:
    """S->C action 1: market rows consumed by native screen 73."""
    rows = list(records)
    fields: list[Field] = [
        byte(CONSIGNMENT_ACTION_MARKET_LIST),
        integer(len(rows)),
        integer(0),
        integer(len(rows)),
    ]
    for row in rows:
        fields.extend(row.market_fields())
    return encode_frame(CONSIGNMENT_MESSAGE_ID, fields)


def consignment_my_listings_frame(
    records: Iterable[ConsignmentWireRecord],
    *,
    action: int = CONSIGNMENT_ACTION_MY_LISTINGS,
) -> bytes:
    """S->C action 7/9: own-listing rows consumed by native screen 70."""
    rows = list(records)
    fields: list[Field] = [byte(action), byte(len(rows))]
    for row in rows:
        fields.extend(row.own_fields())
    return encode_frame(CONSIGNMENT_MESSAGE_ID, fields)


def consignment_remove_owned_frame(item_instance_id: int) -> bytes:
    return encode_frame(
        CONSIGNMENT_MESSAGE_ID,
        [byte(CONSIGNMENT_ACTION_REMOVE_OWN), integer(item_instance_id)],
    )


def consignment_remove_market_frame(item_instance_id: int) -> bytes:
    return encode_frame(
        CONSIGNMENT_MESSAGE_ID,
        [byte(CONSIGNMENT_ACTION_REMOVE_MARKET), integer(item_instance_id)],
    )


def consignment_screen_frame(*, mode: int = CONSIGNMENT_ITEM_MODE) -> bytes:
    """Open screen 613 directly in the native 购买物品 mode."""
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


def consignment_my_screen_frame(*, mode: int = 0) -> bytes:
    """Open the native 已寄售物品 screen 70 (my listings + 添加物品/宠物)."""
    return encode_frame(
        1010,
        [
            integer(0),
            short(0),
            short(0),
            integer(mode),
            integer(CONSIGNMENT_MY_SCREEN_ID),
            short(CONSIGNMENT_OPEN_ACTION),
        ],
    )


def empty_consignment_result_frame(action: int) -> bytes:
    """Compatibility helper for count-based empty responses."""
    return encode_frame(CONSIGNMENT_MESSAGE_ID, [byte(action), byte(0)])
