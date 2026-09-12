from __future__ import annotations

import logging

from protocol import (
    Field,
    byte,
    encode_frame,
    field_debug_entries,
    integer,
    short,
    string,
)

from .state import LocalBattleState


LOG = logging.getLogger('piaomiao-local')


def battle_reset_frame() -> bytes:
    """APK 1040/action=0: clear stale state and open a fresh battle UI."""
    return encode_frame(1040, [byte(0)])


def battle_start_frame(role=None, settings=None) -> bytes:
    """APK 1040/action=1 first-round state frame.

    ``role`` and ``settings`` remain accepted for compatibility with the old
    server-level API; the confirmed wire payload does not consume either.
    """
    del role, settings
    return encode_frame(1040, [
        byte(1),
        integer(1),
        byte(0),
        integer(30),
        short(0),
        string(''),
        short(0),
        string(''),
        byte(1),
    ])


def battle_actor_source_model_for_debug(
    model: int,
    kind: int,
    model_is_battle_base: bool = False,
) -> int:
    return model if model_is_battle_base else (model * 10 if kind == 1 else model - 1)


def battle_actor_debug_snapshot(
    *,
    actor_id: int,
    model: int,
    name: str,
    kind: int,
    side_code: int,
    slot: int = 1,
    model_is_battle_base: bool = False,
    appearance: dict[int, int] | None = None,
    fields: list | None = None,
    trace_id: str = '',
) -> dict[str, object]:
    visible_layers = dict(appearance or {})
    return {
        'trace_id': trace_id,
        'actor_id': actor_id,
        'name': name,
        'role_model': model,
        'kind': kind,
        'side': side_code,
        'slot': slot,
        'appearance_preset': model if kind == 1 else 0,
        'model_is_battle_base': model_is_battle_base,
        'source_model': battle_actor_source_model_for_debug(model, kind, model_is_battle_base),
        'appearance': visible_layers,
        'visible_layers': visible_layers,
        'fields': field_debug_entries(fields or ()),
    }


def format_battle_actor_1048_log(snapshot: dict[str, object]) -> str:
    kind = int(snapshot['kind'])
    fields = snapshot.get('fields') or []
    field_lines = []
    if isinstance(fields, list):
        for entry in fields:
            if not isinstance(entry, dict):
                continue
            field_lines.append(
                f"  {{index: {entry['index']}, type: {entry['type']}, value: {entry['value']!r}}}"
            )
    fields_text = '[\n' + ',\n'.join(field_lines) + '\n]' if field_lines else '[]'
    trace = str(snapshot.get('trace_id') or '')
    trace_line = f'battle_trace={trace}\n' if trace else ''
    if kind == 1:
        return (
            'BATTLE_ACTOR_1048 PLAYER\n'
            f'{trace_line}'
            f"role_id={snapshot['actor_id']}\n"
            f"role_model={snapshot['role_model']}\n"
            f"source_model={snapshot['source_model']}\n"
            f"side={snapshot['side']}\n"
            f"kind={snapshot['kind']}\n"
            f"slot={snapshot['slot']}\n"
            f"appearance_preset={snapshot.get('appearance_preset', snapshot['role_model'])}\n"
            f"model_is_battle_base={snapshot['model_is_battle_base']}\n"
            f"appearance={snapshot['appearance']}\n"
            f"visible_layers={snapshot['visible_layers']}\n"
            f'fields={fields_text}'
        )
    return (
        'BATTLE_ACTOR_1048 MONSTER\n'
        f'{trace_line}'
        f"entity_id={snapshot['actor_id']}\n"
        f"model={snapshot['role_model']}\n"
        f"source_model={snapshot['source_model']}\n"
        f"kind={snapshot['kind']}\n"
        f"side={snapshot['side']}\n"
        f"slot={snapshot['slot']}\n"
        f'fields={fields_text}'
    )


def battle_actor_frame(
    *,
    actor_id: int,
    model: int,
    name: str,
    kind: int,
    side_code: int,
    slot: int = 1,
    model_is_battle_base: bool = False,
    appearance: dict[int, int] | None = None,
    weapon_field2: int = 0,
    current_hp: int = 100,
    max_hp: int = 100,
    trace_id: str = '',
) -> bytes:
    """Build the confirmed 1048 fighter record without server/map dependencies."""
    source_model = model if model_is_battle_base else (model * 10 if kind == 1 else model - 1)
    visible_layers = appearance or {}
    appearance_preset = int(model) if kind == 1 else int(visible_layers.get(21, 0))
    fields: list[Field] = [
        integer(source_model),
        integer(0),
        integer(max(0, int(weapon_field2)) if kind == 1 else 0),
        integer(max(0, current_hp)),
        integer(0),
        integer(side_code),
        string(name),
        short(kind),
        integer(slot),
        integer(actor_id),
        integer(max(0, current_hp)),
        integer(max(1, max_hp)),
        integer(100),
        integer(100),
        integer(int(visible_layers.get(14, 0))),
        short(int(visible_layers.get(15, 0))),
        integer(int(visible_layers.get(16, 0))),
        integer(int(visible_layers.get(17, 0))),
        integer(int(visible_layers.get(18, 0))),
        integer(int(visible_layers.get(19, 0))),
        integer(int(visible_layers.get(20, 0))),
        short(appearance_preset),
    ]
    LOG.info(
        '%s',
        format_battle_actor_1048_log(
            battle_actor_debug_snapshot(
                actor_id=actor_id,
                model=model,
                name=name,
                kind=kind,
                side_code=side_code,
                slot=slot,
                model_is_battle_base=model_is_battle_base,
                appearance=dict(visible_layers),
                fields=fields,
                trace_id=trace_id,
            )
        ),
    )
    return encode_frame(1048, fields)


def battle_action_frame(
    state: LocalBattleState,
    round_number: int | None = None,
    *,
    actor_id: int | None = None,
    target_id: int | None = None,
    damage: int = 10,
    label: str = '普通攻击',
) -> bytes:
    sender_id = state.player_id if actor_id is None else actor_id
    victim_id = state.monster_id if target_id is None else target_id
    return encode_frame(1042, [
        integer(state.round if round_number is None else round_number),
        integer(sender_id),
        integer(victim_id),
        byte(1),
        byte(1),
        byte(0),
        integer(0),
        integer(0),
        string(label),
        integer(1),
        integer(victim_id),
        integer(0),
        integer(22),
        integer(-max(1, damage)),
        string(''),
    ])


def battle_defend_frame(
    state: LocalBattleState,
    round_number: int | None = None,
) -> bytes:
    return encode_frame(1042, [
        integer(state.round if round_number is None else round_number),
        integer(state.player_id),
        integer(state.player_id),
        byte(2),
        byte(1),
        byte(0),
        integer(0),
        integer(0),
        string('防御'),
        integer(0),
    ])


def battle_move_frame(
    state: LocalBattleState,
    round_number: int | None = None,
    *,
    actor_id: int | None = None,
    target_id: int | None = None,
) -> bytes:
    return encode_frame(1042, [
        integer(state.round if round_number is None else round_number),
        integer(state.player_id if actor_id is None else actor_id),
        integer(state.monster_id if target_id is None else target_id),
        byte(1),
        byte(0),
        byte(0),
        integer(0),
        integer(0),
        string(''),
        integer(0),
    ])


def battle_action_show_frame(
    state: LocalBattleState,
    round_number: int | None = None,
) -> bytes:
    shown_round = state.round if round_number is None else round_number
    return encode_frame(1040, [
        byte(2),
        integer(shown_round),
        byte(0),
        integer(0),
        short(0),
        string(''),
        short(0),
        string(''),
        byte(1),
    ])


def battle_escape_frame(player_id: int) -> bytes:
    return encode_frame(1041, [integer(10), integer(player_id)])


def battle_escape_request_frames(
    state: LocalBattleState,
    round_number: int | None = None,
) -> list[bytes]:
    del round_number
    player_id = state.player_id
    if not state.escape():
        return []
    return [battle_escape_frame(player_id)]


def battle_end_frame() -> bytes:
    return encode_frame(1040, [byte(4)])


def battle_reward_popup(
    experience: int,
    item: dict[str, object],
    level_up: bool = False,
) -> bytes:
    del level_up
    quantity = max(0, int(item.get('quantity_gained', 1)))
    return encode_frame(1049, [
        byte(3),
        integer(max(0, int(experience))),
        integer(0),
        integer(0),
        integer(0),
        string('x' * quantity),
    ])


def is_player_escape_command(command_code: int) -> bool:
    """C->S 1041 command 6 is escape; command 10 is quit-spectator."""
    return int(command_code) == 6
