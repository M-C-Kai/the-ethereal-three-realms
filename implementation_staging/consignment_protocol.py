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

from protocol import byte, encode_frame, integer, short


CONSIGNMENT_MESSAGE_ID = 1138
CONSIGNMENT_SCREEN_ID = 613
CONSIGNMENT_OPEN_ACTION = 69

CONSIGNMENT_ACTION_BUY = 4
CONSIGNMENT_ACTION_UNLIST = 2
CONSIGNMENT_ACTION_REFRESH_MERCHANT = 3
CONSIGNMENT_ACTION_MY_LISTINGS = 7
CONSIGNMENT_ACTION_LIST = 9
CONSIGNMENT_ACTION_BROWSE = 13

CONSIGNMENT_OBJECT_ITEM = 1
CONSIGNMENT_OBJECT_PET = 3


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
    """Return an empty count-based result for APK list screens.

    The APK handlers for actions 3, 7, 9 and 13 read field[1] as a byte count.
    A zero count is therefore a safe empty response while the corresponding list
    contains no records.
    """
    return encode_frame(CONSIGNMENT_MESSAGE_ID, [byte(action), byte(0)])
