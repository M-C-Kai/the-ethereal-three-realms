"""福缘系统业务：状态、结算与等阶规则。"""
from __future__ import annotations

import time

from systems.fuyuan.registry import CATALOG, MAX_POINTS


def _nonnegative(value: object, default: int = 0) -> int:
    try:
        return max(0, min(MAX_POINTS, int(value)))
    except (ValueError, TypeError, OverflowError):
        return default


def _now(now: int | None) -> int:
    return int(time.time()) if now is None else int(now)


def ensure_state(role: dict, *, now: int | None = None) -> bool:
    """One-time grant only when absent; malformed existing states get no grant."""
    timestamp = _now(now)
    absent = 'fuyuan' not in role
    state = role.get('fuyuan')
    if not isinstance(state, dict):
        state = {}
    normalized = dict(state)
    normalized.update(
        version=1,
        points=_nonnegative(state.get('points', CATALOG['initial_points'] if absent else 0)),
        settled_at=_nonnegative(state.get('settled_at'), timestamp),
        purchased_points=_nonnegative(state.get('purchased_points')),
        claims=state.get('claims') if isinstance(state.get('claims'), dict) else {},
    )
    if 'settled_at' not in state:
        normalized['settled_at'] = timestamp
    if absent or normalized != role.get('fuyuan'):
        role['fuyuan'] = normalized
        return True
    return False


def remaining_points(role: dict, *, now: int | None = None) -> int:
    state = role.get('fuyuan')
    if not isinstance(state, dict):
        return 0
    timestamp = _now(now)
    elapsed = max(0, timestamp - int(state.get('settled_at', timestamp))) // 60
    return max(0, _nonnegative(state.get('points')) - elapsed)


def tier_for_points(points: int) -> int:
    return 3 if points > 15000 else 2 if points > 5000 else 1 if points > 0 else 0


def tier(role: dict, *, now: int | None = None) -> int:
    return tier_for_points(remaining_points(role, now=now))


def settle(role: dict, *, now: int | None = None) -> bool:
    timestamp = _now(now)
    changed = ensure_state(role, now=timestamp)
    state = role['fuyuan']
    elapsed = max(0, timestamp - state['settled_at']) // 60
    if elapsed and state['points']:
        state['points'] = max(0, state['points'] - elapsed)
        state['settled_at'] += elapsed * 60
        return True
    return changed


def experience_reward(role: dict, base: int) -> int:
    base = max(0, int(base))
    return base * 105 // 100 if tier(role) >= 1 else base


def hp_limit(role: dict, base: int) -> int:
    return base * 120 // 100 if tier(role) >= 2 else base


def capacity_bonus(role: dict) -> int:
    return 20 if tier(role) >= 3 else 0


def status_text(role: dict, *, now: int | None = None) -> str:
    points = remaining_points(role, now=now)
    grade = tier_for_points(points)
    return f'福缘{grade}阶  剩余{points}点（约{points // 60}小时{points % 60}分）'
