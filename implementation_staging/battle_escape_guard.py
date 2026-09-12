from __future__ import annotations

import time


CONTACT_RADIUS_TILES = 1
RETRIGGER_TIMEOUT_SECONDS = 2.0
_CREATED_AT_KEY = 'created_at'


def stamp_guard(
    guard: dict[str, object] | None,
    *,
    now: float | None = None,
) -> dict[str, object] | None:
    """Stamp a freshly-created battle escape guard with monotonic time."""
    if guard is None:
        return None
    guard[_CREATED_AT_KEY] = time.monotonic() if now is None else float(now)
    return guard


def _matches(
    guard: dict[str, object] | None,
    map_id: int,
    monster_id: int,
) -> bool:
    if not guard:
        return False
    return (
        int(guard.get('map_id', -1)) == int(map_id)
        and int(guard.get('monster_id', -1)) == int(monster_id)
    )


def timed_out(
    guard: dict[str, object] | None,
    *,
    now: float | None = None,
    timeout_seconds: float = RETRIGGER_TIMEOUT_SECONDS,
) -> bool:
    """Return whether a stamped guard has reached its retrigger timeout."""
    if not guard:
        return False
    created_at = guard.get(_CREATED_AT_KEY)
    if created_at is None:
        # Legacy guards created before this policy stay movement-gated rather
        # than being treated as already expired.
        return False
    current = time.monotonic() if now is None else float(now)
    return current - float(created_at) >= float(timeout_seconds)


def should_suppress(
    guard: dict[str, object] | None,
    map_id: int,
    monster_id: int,
    *,
    now: float | None = None,
) -> bool:
    """Suppress the same encounter only until the two-second timeout expires."""
    if not _matches(guard, map_id, monster_id):
        return False
    return not timed_out(guard, now=now)


def movement_outside_guard_radius(
    guard: dict[str, object] | None,
    x: int,
    y: int,
    *,
    radius: int = CONTACT_RADIUS_TILES,
) -> bool:
    """Return whether movement leaves the one-tile escape contact radius."""
    if not guard:
        return False
    origin = guard.get('origin')
    if origin is None:
        return False
    origin_x, origin_y = int(origin[0]), int(origin[1])
    return max(abs(int(x) - origin_x), abs(int(y) - origin_y)) > int(radius)
