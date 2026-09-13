"""Small, pure helpers for the team protocol."""
from __future__ import annotations

import time

from systems.map.protocol import PLAYER_ACTOR_ID_BASE


def now() -> float:
    return time.monotonic()


def role_id_from_actor(actor_id: int) -> int:
    value = int(actor_id) - PLAYER_ACTOR_ID_BASE
    return value if value > 0 else 0
