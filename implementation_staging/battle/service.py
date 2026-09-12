from __future__ import annotations

from .engine import resolve_round
from .protocol import battle_action_frame, battle_defend_frame
from .state import LocalBattleState


def battle_round_action_frames(
    state: LocalBattleState,
    command_code: int,
    round_number: int | None = None,
    *,
    target_id: int | None = None,
) -> tuple[list[bytes], bool]:
    """Resolve one battle command, then encode the resulting native 1042 queue."""
    resolution = resolve_round(
        state,
        command_code,
        target_id=target_id,
    )
    if not resolution.accepted:
        return [], False

    action_round = state.round if round_number is None else int(round_number)
    frames: list[bytes] = []
    for action in resolution.actions:
        if action.kind == 'defend':
            frames.append(battle_defend_frame(state, action_round))
            continue
        if action.kind == 'attack':
            frames.append(battle_action_frame(
                state,
                action_round,
                actor_id=action.actor_id,
                target_id=action.target_id,
                damage=action.damage,
                label=action.label,
            ))
            continue
        raise ValueError(f'unsupported battle action kind {action.kind!r}')
    return frames, resolution.monster_defeated
