from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Callable


class CharacterUpdateEvent(str, Enum):
    """会改变客户端人物可见状态的领域事件。"""

    EQUIPMENT_CHANGED = 'equipment.changed'
    EQUIPMENT_STRENGTHENED = 'equipment.strengthened'
    CHARACTER_LEVEL_CHANGED = 'character.level_changed'
    CHARACTER_STATS_CHANGED = 'character.stats_changed'
    CHARACTER_APPEARANCE_CHANGED = 'character.appearance_changed'


@dataclass(frozen=True)
class CharacterUpdateResult:
    """一次同步人物刷新需要下发的协议帧。"""

    event: CharacterUpdateEvent
    frames: tuple[bytes, ...]
    refresh_scope: tuple[str, ...]


class CharacterUpdateBus:
    """同步、进程内的人物状态更新总线。

    总线只决定事件需要刷新哪些范围；人物公式与协议编码通过回调注入，
    因此该模块不会反向依赖 server.py，也不会持有网络连接。
    """

    def __init__(
        self,
        build_full_refresh: Callable[[dict[str, object], object], tuple[bytes, ...]],
        build_appearance_refresh: Callable[[dict[str, object], object], tuple[bytes, ...]],
        is_item_equipped: Callable[[dict[str, object], int], bool],
    ) -> None:
        self._build_full_refresh = build_full_refresh
        self._build_appearance_refresh = build_appearance_refresh
        self._is_item_equipped = is_item_equipped

    def publish(
        self,
        event: CharacterUpdateEvent | str,
        *,
        role: dict[str, object],
        registry: object,
        item_id: int | None = None,
    ) -> CharacterUpdateResult:
        try:
            normalized = event if isinstance(event, CharacterUpdateEvent) else CharacterUpdateEvent(event)
        except ValueError as exc:
            raise ValueError(f'unsupported character update event: {event!r}') from exc

        if normalized is CharacterUpdateEvent.EQUIPMENT_STRENGTHENED:
            if item_id is None:
                raise ValueError('equipment.strengthened requires item_id')
            if not self._is_item_equipped(role, int(item_id)):
                return CharacterUpdateResult(normalized, (), ())
            return CharacterUpdateResult(
                normalized,
                tuple(self._build_full_refresh(role, registry)),
                ('appearance', 'attributes'),
            )

        if normalized in {
            CharacterUpdateEvent.EQUIPMENT_CHANGED,
            CharacterUpdateEvent.CHARACTER_LEVEL_CHANGED,
            CharacterUpdateEvent.CHARACTER_STATS_CHANGED,
        }:
            return CharacterUpdateResult(
                normalized,
                tuple(self._build_full_refresh(role, registry)),
                ('appearance', 'attributes'),
            )

        if normalized is CharacterUpdateEvent.CHARACTER_APPEARANCE_CHANGED:
            return CharacterUpdateResult(
                normalized,
                tuple(self._build_appearance_refresh(role, registry)),
                ('appearance',),
            )

        raise ValueError(f'unsupported character update event: {normalized!r}')
