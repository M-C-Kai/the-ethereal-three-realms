from __future__ import annotations

from dataclasses import dataclass

from .state import LocalBattleState


@dataclass(frozen=True)
class BattleAction:
    kind: str
    actor_id: int
    target_id: int
    damage: int = 0
    label: str = ''


@dataclass(frozen=True)
class RoundResolution:
    accepted: bool
    actions: tuple[BattleAction, ...]
    monster_defeated: bool
    player_defeated: bool
    reason: str


def battle_command_target_id(
    values: list[object],
    state: LocalBattleState,
) -> int | None:
    """Read the APK-confirmed 1041 attack target at field index four."""
    if len(values) <= 4:
        return None
    target_id = int(values[4])
    if target_id not in state.monster_ids or state.monster_hp_for(target_id) <= 0:
        return None
    return target_id


def resolve_round(
    state: LocalBattleState,
    command_code: int,
    *,
    target_id: int | None = None,
) -> RoundResolution:
    """Apply the current local combat formulas without encoding wire frames."""
    if not state.active:
        return RoundResolution(False, (), False, False, 'battle_inactive')

    if int(command_code) == 1:
        selected_target = state.monster_id if target_id is None else int(target_id)
        if (
            selected_target not in state.monster_ids
            or state.monster_hp_for(selected_target) <= 0
        ):
            return RoundResolution(False, (), False, False, 'invalid_target')

        player_damage = state.player_basic_attack_damage()
        monster_defeated = state.apply_basic_attack(
            player_damage,
            target_id=selected_target,
        )
        actions: list[BattleAction] = [BattleAction(
            'attack',
            state.player_id,
            selected_target,
            player_damage,
            '普通攻击',
        )]
        counterattacker = selected_target
        defending = False
    elif int(command_code) == 2:
        monster_defeated = False
        actions = [BattleAction(
            'defend',
            state.player_id,
            state.player_id,
            0,
            '防御',
        )]
        counterattacker = state.monster_id
        defending = True
    else:
        return RoundResolution(False, (), False, False, 'unsupported_command')

    if not monster_defeated and state.monster_hp_for(counterattacker) > 0:
        monster_damage = state.monster_basic_attack_damage(defending=defending)
        state.player_hp = max(0, state.player_hp - monster_damage)
        actions.append(BattleAction(
            'attack',
            counterattacker,
            state.player_id,
            monster_damage,
            '妖兽攻击',
        ))

    return RoundResolution(
        True,
        tuple(actions),
        monster_defeated,
        state.player_hp <= 0,
        'resolved',
    )
