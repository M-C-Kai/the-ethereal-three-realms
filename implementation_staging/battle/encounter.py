from __future__ import annotations

from dataclasses import dataclass

from .state import CombatStats, LocalBattleState


ENCOUNTER_SOURCES = frozenset({
    'map_interaction',
    'q_action',
    'proximity',
})


@dataclass(frozen=True)
class EncounterRequest:
    map_id: int
    monster_id: int
    player_id: int
    player_tile: tuple[int, int] | None
    monster_tile: tuple[int, int] | None
    source: str


@dataclass(frozen=True)
class EncounterDecision:
    start: bool
    suppressed: bool
    reason: str


def request_encounter(
    state: LocalBattleState,
    request: EncounterRequest,
    *,
    player_stats: CombatStats | None = None,
    monster_ids: tuple[int, ...] | list[int] | None = None,
    now: float | None = None,
) -> EncounterDecision:
    """Apply one authoritative admission decision for every battle entry path."""
    if request.source not in ENCOUNTER_SOURCES:
        raise ValueError(f'unsupported encounter source {request.source!r}')

    if state.active:
        return EncounterDecision(False, True, 'battle_active')

    # ``monster_defeated`` means the current map encounter has already been
    # settled. The legacy server suppressed every stale monster tap until the
    # map-entry boundary reset this flag; preserve that behavior during split.
    if state.monster_defeated:
        return EncounterDecision(False, True, 'monster_defeated')

    if state.should_suppress_retrigger(
        request.map_id,
        request.monster_id,
        now=now,
    ):
        return EncounterDecision(False, True, 'escape_guard')

    state.map_id = int(request.map_id)
    state.contact_tile = (
        (int(request.monster_tile[0]), int(request.monster_tile[1]))
        if request.monster_tile is not None
        else None
    )
    state.player_tile = (
        (int(request.player_tile[0]), int(request.player_tile[1]))
        if request.player_tile is not None
        else None
    )
    state.begin(
        int(request.player_id),
        int(request.monster_id),
        player_stats,
        monster_ids=monster_ids,
    )
    return EncounterDecision(True, False, 'started')


def update_player_tile(
    state: LocalBattleState,
    x: int,
    y: int,
    *,
    now: float | None = None,
) -> bool:
    """Route map movement into the battle-owned escape-release policy."""
    return state.update_player_tile(x, y, now=now)
