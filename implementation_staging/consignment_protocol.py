"""Protocol helpers for the APK's native consignment (寄售) UI.

Reverse-engineering notes for piaomiao_local_login.apk:
- screen 613 -> pmsj/work/e/ev (寄售商人)
- message 1138 -> consignment protocol
- response action 3/22 routes back to screen 613
- response action 13 routes to screen 44 (consignment category/search)
- response action 7/9 routes to screen 70 (已寄售物品)
- response action 1/12/16 routes to screen 73 (寄售购买)

Keep the screen bridge and wire-level constants here so NPC code does not hardcode
APK implementation details throughout server.py.
"""

from __future__ import annotations

from protocol import TYPE_BYTE, Field, byte, encode_frame, integer, short, string


CONSIGNMENT_MESSAGE_ID = 1138
CONSIGNMENT_SCREEN_ID = 613
CONSIGNMENT_OPEN_ACTION = 69

# APK pmsj/work/e/ev.c() installs exactly these two tab modes in M[]:
#   2809 -> 购买物品
#   2500 -> 购买宠物
# ev.y(mode) only sends C->S 1138/action=3 when mode == 2809. Opening screen
# 613 with mode=0 therefore builds the chrome/tabs but leaves the item list
# uninitialised, which appears on-device as one empty highlighted row.
CONSIGNMENT_ITEM_MODE = 2809
CONSIGNMENT_PET_MODE = 2500

CONSIGNMENT_ACTION_BUY = 4
CONSIGNMENT_ACTION_UNLIST = 2
CONSIGNMENT_ACTION_REFRESH_MERCHANT = 3
CONSIGNMENT_ACTION_MY_LISTINGS = 7
CONSIGNMENT_ACTION_LIST = 9
CONSIGNMENT_ACTION_BROWSE = 13

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


def consignment_category_frame() -> bytes:
    """S->C 1138/action 3: native screen-613 item category list."""
    fields = [byte(CONSIGNMENT_ACTION_REFRESH_MERCHANT), byte(len(CONSIGNMENT_ITEM_CATEGORIES))]
    for category_id, name in enumerate(CONSIGNMENT_ITEM_CATEGORIES):
        fields.extend((byte(category_id), string(name)))
    return encode_frame(CONSIGNMENT_MESSAGE_ID, fields)


def is_consignment_category_request(fields: list[Field]) -> bool:
    """C->S 1138 [BYTE 3] emitted by the native merchant category view."""
    return bool(
        len(fields) == 1
        and fields[0].type_id == TYPE_BYTE
        and fields[0].value == CONSIGNMENT_ACTION_REFRESH_MERCHANT
    )


def is_consignment_browse_request(fields: list[Field]) -> bool:
    """C->S 1138 [BYTE 13, BYTE category_id] emitted after a category tap."""
    return bool(
        len(fields) == 2
        and fields[0].type_id == TYPE_BYTE
        and fields[0].value == CONSIGNMENT_ACTION_BROWSE
        and fields[1].type_id == TYPE_BYTE
        and 0 <= int(fields[1].value) < len(CONSIGNMENT_ITEM_CATEGORIES)
    )


def consignment_screen_frame(*, mode: int = CONSIGNMENT_ITEM_MODE) -> bytes:
    """Open screen 613 directly in the APK's native 购买物品 mode."""
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
    """Return an empty count-based result for APK list screens.

    The APK handlers for actions 3, 7, 9 and 13 read field[1] as a byte count.
    A zero count is therefore a safe empty response while the corresponding list
    contains no records.
    """
    return encode_frame(CONSIGNMENT_MESSAGE_ID, [byte(action), byte(0)])
