from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class SystemContext:
    """Per-dispatch state shared by protocol systems."""

    username: str = ''
    active_role: dict[str, Any] | None = None
    session: dict[str, Any] = field(default_factory=dict)

