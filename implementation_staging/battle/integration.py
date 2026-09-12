from __future__ import annotations

from types import ModuleType
from typing import Any

from . import encounter, engine, protocol, state


def _legacy_should_suppress_escape_retrigger(
    guard: dict[str, object] | None,
    map_id: int,
    monster_id: int,
) -> bool:
    return state.should_suppress_guard(guard, map_id, monster_id)


def _legacy_update_escape_guard_for_movement(
    battle_state: state.LocalBattleState,
    x: int,
    y: int,
) -> bool:
    return encounter.update_player_tile(battle_state, x, y)


def _legacy_battle_round_action_frames(
    battle_state: state.LocalBattleState,
    command_code: int,
    round_number: int | None = None,
    *,
    target_id: int | None = None,
) -> tuple[list[bytes], bool]:
    """Adapt the domain engine result to the server's existing frame API."""
    resolution = engine.resolve_round(
        battle_state,
        command_code,
        target_id=target_id,
    )
    if not resolution.accepted:
        return [], False

    action_round = battle_state.round if round_number is None else round_number
    frames: list[bytes] = []
    for action in resolution.actions:
        if action.kind == 'defend':
            frames.append(protocol.battle_defend_frame(battle_state, action_round))
            continue
        if action.kind == 'attack':
            frames.append(protocol.battle_action_frame(
                battle_state,
                action_round,
                actor_id=action.actor_id,
                target_id=action.target_id,
                damage=action.damage,
                label=action.label,
            ))
            continue
        raise ValueError(f'unsupported battle action kind {action.kind!r}')
    return frames, resolution.monster_defeated


def install(server_module: ModuleType | Any) -> None:
    """Install extracted battle components behind the legacy server API.

    This compatibility layer lets the active launcher use one authoritative
    battle implementation while the large ``server.py`` file is being reduced.
    Once server.py imports battle directly, this module can be deleted without
    changing battle behavior.
    """
    server_module.CombatStats = state.CombatStats
    server_module.LocalBattleState = state.LocalBattleState
    server_module.should_suppress_escape_retrigger = _legacy_should_suppress_escape_retrigger
    server_module.update_escape_guard_for_movement = _legacy_update_escape_guard_for_movement

    server_module.battle_command_target_id = engine.battle_command_target_id
    server_module.battle_round_action_frames = _legacy_battle_round_action_frames

    for name in (
        'battle_reset_frame',
        'battle_start_frame',
        'battle_actor_source_model_for_debug',
        'battle_actor_debug_snapshot',
        'format_battle_actor_1048_log',
        'battle_actor_frame',
        'battle_action_frame',
        'battle_defend_frame',
        'battle_move_frame',
        'battle_action_show_frame',
        'battle_escape_frame',
        'battle_escape_request_frames',
        'battle_end_frame',
        'battle_reward_popup',
        'is_player_escape_command',
    ):
        setattr(server_module, name, getattr(protocol, name))
