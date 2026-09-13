"""福缘系统协议帧：1054 福缘页面与属性刷新帧。"""
from __future__ import annotations

from protocol import byte, encode_frame, integer, string
from systems.fuyuan.service import remaining_points, status_text, tier
from systems.inventory.service import bag_capacity
from systems.role.protocol import character_appearance_frame
from systems.role.service import combat_stats, normalized_currency_balance


def status_frame(role: dict, text: str = '', *, now: int | None = None) -> bytes:
    return encode_frame(1054, [byte(1), string(status_text(role, now=now) + ('_' + text if text else ''))])


def list_frame(rows: list, *, title: str = '福缘系统', page: int = 0, size: int = 20) -> bytes:
    # d/i.c() is a zero-based page cursor, d() is the requested page size.
    size = max(1, min(100, size))
    selected = rows[page * size:(page + 1) * size]
    fields = [byte(0), string(title), byte(len(rows)), byte(len(selected))]
    for row in selected:
        fields.extend([integer(row['id']), string(row['name']), integer(row['tier']),
                       string(row['menu']), string(row['description'])])
    return encode_frame(1054, fields)


def fuyuan_update_frame(role: dict[str, object]) -> bytes:
    """Refresh native property slots without restarting the 1006 login flow."""
    properties = {
        24: tier(role),
        40: combat_stats(role).max_hp,
        41: combat_stats(role).max_hp,
        50: normalized_currency_balance(role.get('currencies', {}).get('silver', 0)),
        62: bag_capacity(role),
    }
    return character_appearance_frame(int(role['id']), properties)
