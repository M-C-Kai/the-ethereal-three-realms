"""战斗系统协议帧：1040/1041/1042/1048/1049 战斗表现。"""
from __future__ import annotations

import logging
import struct
import time
from pathlib import Path

from protocol import (
    Field, TYPE_BYTE, TYPE_INT, TYPE_SHORT,
    binary, byte, decode_frame, encode_frame, field_debug_entries, field_values,
    integer, long_integer, short, string,
)
from systems.battle import registry as battle_registry
from systems.map.registry import MapActorDefinition, MapDefinition
from systems.battle.registry import (
    BATTLE_EMPTY_RESOURCE_IDS, PNG_QUERY_MAIN_CACHE, PNG_QUERY_ROLE_CACHE,
    _build_artifact_dirs, _signed_int32,
)
from systems.battle.service import LocalBattleState
from systems.inventory.protocol import item_frame
from systems.inventory.registry import is_strengthening_stone, normalized_strengthen_level
from systems.inventory.registry import default_item_registry
from systems.role.protocol import character_appearance
from systems.role.service import (
    combat_stats, effective_character_stats, equipped_weapon_battle_field2,
)

LOG = logging.getLogger('piaomiao-local')

def battle_reward_notice(experience: int, item: dict[str, object], level_up: bool = False) -> bytes:
    """Persist the deterministic result in the APK's notice cache.

    Protocol 1123 is not a visible notification: ``main/e.C`` only stores
    its version and text for the notice screen.  Keep it as a durable record,
    and use :func:`battle_reward_popup` for the immediate on-screen result.
    """
    level_text = '，升级了' if level_up else ''
    resolved = default_item_registry().resolve(item)
    name = resolved.get('name', '未知物品')
    text = f'战斗胜利{level_text}！获得经验 {experience}，获得 {name} x{item.get("quantity_gained", 1)}'
    # 1123/action 0 is the client's normal notice channel.  A timestamp-like
    # version makes each victory visible even when the previous notice was
    # already acknowledged locally.
    return encode_frame(1123, [byte(0), integer(int(time.time())), string(text)])


def battle_reward_popup(experience: int, item: dict[str, object], level_up: bool = False) -> bytes:
    """Open the APK's native top-of-map reward overlay (protocol 1049).

    ``main/e`` handles 1049/action 3 by passing the next five fields to the
    map screen's embedded ``e/bs`` overlay.  Its fixed layout is experience,
    pet experience, silver, cultivation and an item-count marker.  The
    overlay slides down from the top, remains visible for three seconds, and
    slides away; unlike protocol 1512 it does not open the centred ``br``
    prompt and therefore does not interrupt the map screen.

    The bundled client renders the length of the last string after ``获得``.
    Encode one marker character per awarded item so a single drop is shown as
    ``获得 1`` while the complete item instance is still delivered by 1008.
    """
    quantity = max(0, int(item.get('quantity_gained', 1)))
    item_count_marker = 'x' * quantity
    return encode_frame(1049, [
        byte(3),
        integer(max(0, int(experience))),
        integer(0),
        integer(0),
        integer(0),
        string(item_count_marker),
    ])

def battle_reset_frame() -> bytes:
    """Return the APK-verified 1040 action=0 battle reset frame.

    Action 0 is parsed by the client as the battle-state reset/open path.  It
    removes stale map/battle state and creates screen 20, which must precede
    the action=1 first-round payload on a fresh map session.
    """
    return encode_frame(1040, [byte(0)])


def battle_start_frame(role: dict[str, object], settings: Settings) -> bytes:
    """Build the APK-confirmed 1040/action=1 battle-state frame.

    ``main/e`` reads the following fixed types for action 1:
    byte(action), int(round), byte(reserved), int(timer), short(menu-state),
    string(reserved), short(target-state), string(reserved), byte(ready).
    The two strings and the reserved byte are intentionally empty/zero because
    the client parser only consumes them in this action; no server semantics
    are inferred from their names.
    """
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
    """Read-only copy of the 1048 source_model formula for diagnostic logs.

    The encoder in ``battle_actor_frame`` keeps its own identical expression
    and does not call this helper.  Do not use this return value to decide
    protocol output.
    """
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
    """Return a read-only 1048 diagnostic snapshot.  Not used for encoding."""
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
    """Format a PLAYER or MONSTER 1048 diagnostic block."""
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
    trace_line = f"battle_trace={trace}\n" if trace else ''
    if kind == 1:
        return (
            "BATTLE_ACTOR_1048 PLAYER\n"
            f"{trace_line}"
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
            f"fields={fields_text}"
        )
    return (
        "BATTLE_ACTOR_1048 MONSTER\n"
        f"{trace_line}"
        f"entity_id={snapshot['actor_id']}\n"
        f"model={snapshot['role_model']}\n"
        f"source_model={snapshot['source_model']}\n"
        f"kind={snapshot['kind']}\n"
        f"side={snapshot['side']}\n"
        f"slot={snapshot['slot']}\n"
        f"fields={fields_text}"
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
    """Build the APK's 1048 actor record used to populate battle slots.

    ``main/e.af`` constructs ``work/b/h`` from field 7 (kind), field 9 (id),
    field 2 (battle weapon image/quality for kind=1), field 0 (model source),
    field 5 (side/category), and field 8 (battle
    station).  Field 21 is the face/body appearance preset: kind=1 reads it as
    the constructor's fourth argument and ``h.r()`` applies ``y(f(21))`` /
    ``M(f(21))``.  The remaining numeric fields are the zero/default stat
    block; keeping them present is important because the renderer reads the
    sparse record by index.
    """
    # kind=2: APK e.af does field[0]+1. Keep signed model-1 so negative
    # map models such as -2004250 round-trip; do not clamp to 0.
    source_model = model if model_is_battle_base else (model * 10 if kind == 1 else model - 1)
    visible_layers = appearance or {}
    # kind=1: APK h.r() uses Vector[21] as the same selector map v.r() reads
    # from property 6.  Monsters keep the previous zero unless a caller
    # supplies appearance 21.
    appearance_preset = int(model) if kind == 1 else int(visible_layers.get(21, 0))
    fields: list[Field] = [
        integer(source_model),  # 0: flags/model source
        integer(0),              # 1
        integer(max(0, int(weapon_field2)) if kind == 1 else 0),  # 2: battle weapon image*10 + quality
        integer(max(0, current_hp)),  # 3: current hp/status (used by h.d())
        integer(0),              # 4
        integer(side_code),      # 5: side/category
        string(name),            # 6: battle name
        short(kind),              # 7: actor kind
        integer(slot),            # 8: one-based battle station
        integer(actor_id),        # 9: actor id
        integer(max(0, current_hp)),  # 10: current hp
        integer(max(1, max_hp)),      # 11: max hp
        integer(100),             # 12: current mp
        integer(100),             # 13: max mp/status
        integer(int(visible_layers.get(14, 0))),  # 14: trousers layer
        short(int(visible_layers.get(15, 0))),     # 15: armour/base layer
        integer(int(visible_layers.get(16, 0))),   # 16: shoulder layer
        integer(int(visible_layers.get(17, 0))),   # 17: wrist layer
        integer(int(visible_layers.get(18, 0))),   # 18: boot layer
        integer(int(visible_layers.get(19, 0))),   # 19: cape layer
        integer(int(visible_layers.get(20, 0))),   # 20: helmet layer
        # kind=1: short face/body selector.  e.af reads w.b(21) into h.<init>
        # p4; h.r() then calls y(f(21)) and M(f(21)).  Not a battle station.
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


def battle_actor_frames(
    role: dict[str, object],
    settings: Settings | MapDefinition,
    trace_id: str = '',
    state: LocalBattleState | None = None,
) -> list[bytes]:
    """Return one player and every configured monster for the local battle."""
    if isinstance(settings, MapDefinition):
        monsters = settings.monsters
        if not monsters:
            raise ValueError(f'map {settings.id} has no battle monster')
        default_role_model = 2000
        default_role_name = '本地侠客'
    else:
        monsters = (MapActorDefinition(
            id=int(settings.monster_id),
            name=str(settings.monster_name),
            model=int(settings.monster_model),
            x=int(settings.monster_x),
            y=int(settings.monster_y),
            direction=int(settings.monster_direction),
        ),)
        default_role_model = settings.role_model
        default_role_name = settings.role_name
    frames = [
        battle_actor_frame(
            actor_id=int(role['id']),
            model=int(role.get('model', default_role_model)),
            name=str(role.get('name', default_role_name)),
            kind=1,
            # main/b.h.e() treats the local fighter's side as grid 0. Side 3
            # is a special non-grid list and cannot be resolved by normal
            # attack actions, so the player must use the ordinary side 2.
            side_code=2,
            slot=1,
            appearance=character_appearance(role, getattr(settings, 'item_registry', None)),
            weapon_field2=equipped_weapon_battle_field2(role, getattr(settings, 'item_registry', None)),
            current_hp=state.player_hp if state is not None else 100,
            max_hp=state.player_max_hp if state is not None else 100,
            trace_id=trace_id,
        )
    ]
    frames.extend(
        battle_actor_frame(
            actor_id=monster.id,
            model=monster.model,
            name=monster.name,
            kind=2,
            side_code=1,
            slot=slot,
            current_hp=state.monster_hp_for(monster.id) if state is not None else 100,
            max_hp=state.monster_max_hp if state is not None else 100,
            trace_id=trace_id,
        )
        for slot, monster in enumerate(monsters, start=1)
    )
    return frames


def battle_actor_update_frame(
    role: dict[str, object],
    settings: Settings,
    state: LocalBattleState,
    actor_id: int,
) -> bytes:
    """Re-send one 1048 record with the actor's current HP.

    The 1042 action packet drives animation and damage numbers, but the APK's
    visible life bar is read from actor field 3 (and the current/max stat pair
    at fields 10/11).  A small 1048 state refresh keeps those values in sync.
    """
    if actor_id == state.player_id:
        return battle_actor_frame(
            actor_id=state.player_id,
            model=int(role.get('model', settings.role_model)),
            name=str(role.get('name', settings.role_name)),
            kind=1,
            side_code=2,
            slot=1,
            appearance=character_appearance(role, getattr(settings, 'item_registry', None)),
            weapon_field2=equipped_weapon_battle_field2(role, getattr(settings, 'item_registry', None)),
            current_hp=state.player_hp,
            max_hp=state.player_max_hp,
            trace_id=state.trace_id,
        )
    return battle_actor_frame(
        actor_id=state.monster_id,
        model=int(settings.monster_model),
        name=str(settings.monster_name),
        kind=2,
        side_code=1,
        slot=1,
        current_hp=state.monster_hp,
        max_hp=state.monster_max_hp,
        trace_id=state.trace_id,
    )

def format_battle_resource_query_log(
    *,
    username: str,
    query_action: int,
    resource_ids: list[int],
    battle_active: bool,
    round_number: int,
    trace_id: str,
    resource_id: int,
    resolution: dict[str, object],
    response_type: int | None,
    chunks: int,
) -> str:
    """Format the BATTLE_RESOURCE_QUERY diagnostic block."""
    trace = f"battle_trace={trace_id}\n" if trace_id else ''
    return (
        "BATTLE_RESOURCE_QUERY\n"
        f"{trace}"
        f"user={username!r}\n"
        f"action={query_action}\n"
        f"ids={resource_ids}\n"
        f"battle_active={battle_active}\n"
        f"round={round_number}\n"
        f"resource_id={resource_id}\n"
        f"alias={resolution.get('alias')!r}\n"
        f"branch={resolution.get('branch')!r}\n"
        f"offset_id={resolution.get('offset_id')!r}\n"
        f"jar_fallback={resolution.get('jar_fallback', False)}\n"
        f"resolved_id={resolution.get('resolved_id')!r}\n"
        f"resolved_path={resolution.get('resolved_path')!r}\n"
        f"response_type={response_type}\n"
        f"chunks={chunks}"
    )

def battle_resource_frames(model_id: int) -> list[bytes]:
    """Return the two 1503 chunks expected by ``main/e.ao`` for a .dat query."""
    path = battle_registry.battle_resource_path(model_id)
    if path is None:
        if model_id in BATTLE_EMPTY_RESOURCE_IDS:
            LOG.info('battle resource empty model=%d', model_id)
            empty = [integer(model_id), short(0), short(0), binary(b'')]
            return [
                encode_frame(1503, [byte(0), *empty]),
                encode_frame(1503, [byte(2), *empty]),
            ]
        LOG.warning('battle resource missing model=%d', model_id)
        return []
    data = path.read_bytes()
    if len(data) > 0xFFFF:
        LOG.warning('battle resource too large model=%d bytes=%d', model_id, len(data))
        return []
    # status 0 allocates and copies the first chunk.  The APK's status-2
    # handler also appends its declared chunk before finalising the cache;
    # repeating ``data`` there would overflow the client's fixed buffer.
    fields = [integer(model_id), short(len(data)), short(len(data)), binary(data)]
    finish_fields = [integer(model_id), short(len(data)), short(0), binary(b'')]
    return [
        encode_frame(1503, [byte(0), *fields]),
        encode_frame(1503, [byte(2), *finish_fields]),
    ]

def battle_image_resolve_debug(image_id: int) -> dict[str, object]:
    """Describe which 1502 action=0/2 image lookup branch would be used.

    Read-only locate of the images.o record.  It does not encode 1501/1502
    and is not used by ``battle_image_resource`` to choose a payload.
    """
    image_dirs = (
        Path(__file__).resolve().parents[2] / 'maps' / '60011' / 'images',
        *(
            build_dir / resource_set / 'res' / 'images'
            for build_dir in _build_artifact_dirs()
            for resource_set in ('weapon-apk-extracted/assets', 'jar-images')
        ),
    )
    for candidate_id in (image_id, image_id - 100):
        if candidate_id < 0:
            continue
        for candidate_dir in image_dirs:
            index_path = candidate_dir / 'images.o'
            if not index_path.is_file():
                continue
            index = index_path.read_bytes()
            if len(index) < 2:
                continue
            index_size = struct.unpack_from('>H', index, 0)[0]
            records = index[2:2 + index_size]
            for offset in range(0, len(records) - 6, 7):
                record_id, container_number, _data_offset = struct.unpack_from('>IBH', records, offset)
                if record_id != candidate_id:
                    continue
                container_path = candidate_dir / f'png{container_number}.p'
                if not container_path.is_file():
                    continue
                jar_fallback = 'jar-images' in candidate_dir.parts
                aliased = candidate_id != image_id
                if aliased and jar_fallback:
                    branch = 'alias_jar'
                elif aliased:
                    branch = 'alias'
                elif jar_fallback:
                    branch = 'jar_fallback'
                else:
                    branch = 'direct'
                return {
                    'requested_id': image_id,
                    'alias': candidate_id if aliased else None,
                    'resolved_id': candidate_id,
                    'resolved_path': str(container_path),
                    'branch': branch,
                    'jar_fallback': jar_fallback,
                    'missing': False,
                }
    return {
        'requested_id': image_id,
        'alias': None,
        'resolved_id': None,
        'resolved_path': None,
        'branch': 'missing',
        'jar_fallback': False,
        'missing': True,
    }


def battle_image_frames(query_action: int, image_id: int) -> list[bytes]:
    """Return 1501 image chunks followed by the client's 1502 redraw signal."""
    resource = battle_registry.battle_image_resource(image_id)
    if resource is None:
        LOG.warning('battle image resource missing image=%d action=%d', image_id, query_action)
        return []
    (
        width,
        height,
        bit_depth,
        transparent_index,
        palette_crc,
        transparency_crc,
        header_crc,
        palette_length,
        idat_length,
        data,
    ) = resource

    # Action 2 originates from a/a/a's role-image cache. main/e.ap selects
    # that cache with response field 0 == 1; batched action 0 uses cache 0.
    cache_selector = 1 if query_action == PNG_QUERY_ROLE_CACHE else 0
    if palette_length + idat_length != len(data) or len(data) > 0xFFFF:
        LOG.warning('battle image resource invalid image=%d bytes=%d', image_id, len(data))
        return []

    def frame(status: int, chunk: bytes) -> bytes:
        return encode_frame(1501, [
            integer(cache_selector),
            integer(len(data)),
            byte(0),
            byte(status),
            integer(image_id),
            short(width),
            short(height),
            byte(bit_depth),
            byte(transparent_index),
            short(palette_length),
            short(idat_length),
            integer(_signed_int32(palette_crc)),
            integer(_signed_int32(transparency_crc)),
            integer(_signed_int32(header_crc)),
            short(len(chunk)),
            binary(chunk),
        ])

    # As with 1503, status 0 allocates and copies the complete payload while
    # status 2 finalises with an empty chunk, avoiding a client buffer overflow.
    # main/e.ap stores action-2 resources in the role cache without invalidating
    # the current canvas. Server protocol 1502 is the separate processPngQuery
    # completion signal which forces the map/battle scene to redraw.
    return [frame(0, data), frame(2, b''), encode_frame(1502)]

def battle_action_frame(
    state: LocalBattleState,
    round_number: int | None = None,
    *,
    actor_id: int | None = None,
    target_id: int | None = None,
    damage: int = 10,
    label: str = '普通攻击',
) -> bytes:
    """Queue one native APK basic attack, including its damage effect.

    The decompiled ``pmsj.work.main.b`` controller identifies action type 1
    as ``ACTION_ATTACK``. It moves the sender to ``target.g()``, waits for
    arrival, switches to the attack pose, applies the embedded BattleEffect,
    and only then queues the sender's return movement. Effect type 22 calls
    ``target.a(delta, flags)`` and updates HP immediately.

    Types 7 and 8 are summon/call-back actions. Using type 8 as an attack was
    the reason HP changed after the return animation and could strand actors.
    """
    sender_id = state.player_id if actor_id is None else actor_id
    victim_id = state.monster_id if target_id is None else target_id
    return encode_frame(1042, [
        integer(state.round if round_number is None else round_number),
        integer(sender_id),
        integer(victim_id),
        byte(1),                 # ACTION_ATTACK
        byte(1),                 # one hit
        byte(0),
        integer(0),              # sender visual effect id
        integer(0),              # target visual effect id
        string(label),
        integer(1),              # BattleEffect count
        integer(victim_id),      # effect target
        integer(0),              # normal hit reaction and damage number
        integer(22),             # HP delta effect
        integer(-max(1, damage)),
        string(''),
    ])


def battle_defend_frame(
    state: LocalBattleState,
    round_number: int | None = None,
) -> bytes:
    """Queue the native defence action without applying an HP effect."""
    return encode_frame(1042, [
        integer(state.round if round_number is None else round_number),
        integer(state.player_id),
        integer(state.player_id),
        byte(2),                 # ACTION_DEFEND
        byte(1),
        byte(0),
        integer(0),
        integer(0),
        string('防御'),
        integer(0),              # no BattleEffect
    ])


def battle_round_action_frames(
    state: LocalBattleState,
    command_code: int,
    round_number: int | None = None,
    *,
    target_id: int | None = None,
) -> tuple[list[bytes], bool]:
    """Resolve one supported player command and keep wire HP effects in sync."""
    action_round = state.round if round_number is None else round_number
    from systems.battle.service import ordered_combatants
    selected_target = state.monster_id if target_id is None else int(target_id)
    if command_code not in (1, 2):
        return [], False
    if command_code == 1 and (selected_target not in state.monster_ids
                             or state.monster_hp_for(selected_target) <= 0):
        return [], False
    frames = []
    defending = False
    for actor in ordered_combatants(
        (state.player_id, *state.monster_ids), state.initiative, state.player_id,
    ):
        if state.player_hp <= 0 or state.all_monsters_defeated():
            break
        if actor == state.player_id:
            if command_code == 2:
                defending = True
                frames.append(battle_defend_frame(state, action_round))
            else:
                damage = state.player_basic_attack_damage()
                state.apply_basic_attack(damage, target_id=selected_target)
                frames.append(battle_action_frame(
                    state, action_round, target_id=selected_target, damage=damage,
                ))
        elif state.monster_hp_for(actor) > 0:
            damage = state.monster_basic_attack_damage(defending=defending)
            state.player_hp = max(0, state.player_hp - damage)
            frames.append(battle_action_frame(
                state, action_round, actor_id=actor, target_id=state.player_id,
                damage=damage, label='妖兽攻击',
            ))
    return frames, state.all_monsters_defeated()


def battle_move_frame(
    state: LocalBattleState,
    round_number: int | None = None,
    *,
    actor_id: int | None = None,
    target_id: int | None = None,
) -> bytes:
    """Build a raw effect-free ACTION_ATTACK record for diagnostics.

    Gameplay uses :func:`battle_action_frame`; this record approaches and
    returns but intentionally performs no damage.
    """
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


def battle_action_show_frame(state: LocalBattleState, round_number: int | None = None) -> bytes:
    """Advance the APK battle UI (1040/action=2) for a specific round.

    The client sends its completion acknowledgement only after it has
    finished the action animation.  The server may already have advanced its
    internal HP/turn state by then, so the frame must carry the round that the
    client just executed rather than blindly using the post-action counter.
    """
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
    """Start the APK's dedicated smooth escape-and-close transition.

    S->C 1041/10 calls ``pmsj.work.e.j.escapeStart()``. The client moves the
    local fighter to its off-screen escape point over 1300 ms, blocks further
    battle input during that movement, and closes the battle as soon as the
    fighter reports ``escapeDone()``.
    """
    return encode_frame(1041, [integer(10), integer(player_id)])


def battle_escape_request_frames(
    state: LocalBattleState,
    round_number: int | None = None,
) -> list[bytes]:
    """Settle escape once and immediately start the client's native transition."""
    del round_number  # Escape protocol 1041 has no round field.
    player_id = state.player_id
    if not state.escape():
        return []
    return [battle_escape_frame(player_id)]


def battle_end_frame() -> bytes:
    """End the local battle through the APK's verified action=4 branch."""
    return encode_frame(1040, [byte(4)])


# ---------------------------------------------------------------------------
# 双人即时对决（切磋 1157 / PK 1158）
# ---------------------------------------------------------------------------
def duel_start_frames(
    viewer: dict[str, object],
    opponent: dict[str, object],
    duel,
    settings,
) -> tuple[bytes, ...]:
    """Build one viewer's battle entry frames against the opposing player.

    与 PVE 相同的进入序列：1040/0 复位建屏 → 1048 参与者 → 1040/1 首回合。
    本方固定为 kind=1/side=2；对手以 kind=2/side=1 出现在对方站位，
    source_model = 玩家模型-1（客户端 +1 还原），因此对战画面中对手
    仍以玩家造型出现，仅站在怪物格。
    """
    own_stats = duel.stats[int(viewer['id'])]
    opponent_id = int(opponent['id'])
    return (
        battle_reset_frame(),
        battle_actor_frame(
            actor_id=int(viewer['id']),
            model=int(viewer.get('model', settings.role_model)),
            name=str(viewer.get('name', settings.role_name)),
            kind=1,
            side_code=2,
            slot=1,
            appearance=character_appearance(viewer, settings.item_registry),
            weapon_field2=equipped_weapon_battle_field2(viewer, settings.item_registry),
            current_hp=duel.hp[int(viewer['id'])],
            max_hp=own_stats.max_hp,
            trace_id=duel.trace_id,
        ),
        battle_actor_frame(
            actor_id=opponent_id,
            model=int(opponent.get('model', settings.role_model)),
            name=str(opponent.get('name', '')),
            kind=2,
            side_code=1,
            slot=1,
            current_hp=duel.hp[opponent_id],
            max_hp=duel.stats[opponent_id].max_hp,
            trace_id=duel.trace_id,
        ),
        battle_start_frame(viewer, settings),
    )


def duel_hp_refresh_frames(viewer: dict[str, object], opponent: dict[str, object], duel, settings) -> list[bytes]:
    """Re-send both 1048 records so both clients' HP bars stay in sync."""
    opponent_id = int(opponent['id'])
    own_stats = duel.stats[int(viewer['id'])]
    return [
        battle_actor_frame(
            actor_id=int(viewer['id']),
            model=int(viewer.get('model', settings.role_model)),
            name=str(viewer.get('name', settings.role_name)),
            kind=1,
            side_code=2,
            slot=1,
            appearance=character_appearance(viewer, settings.item_registry),
            weapon_field2=equipped_weapon_battle_field2(viewer, settings.item_registry),
            current_hp=duel.hp[int(viewer['id'])],
            max_hp=own_stats.max_hp,
            trace_id=duel.trace_id,
        ),
        battle_actor_frame(
            actor_id=opponent_id,
            model=int(opponent.get('model', settings.role_model)),
            name=str(opponent.get('name', '')),
            kind=2,
            side_code=1,
            slot=1,
            current_hp=duel.hp[opponent_id],
            max_hp=duel.stats[opponent_id].max_hp,
            trace_id=duel.trace_id,
        ),
    ]


def duel_action_frame(
    duel,
    round_number: int,
    *,
    actor_id: int,
    target_id: int,
    damage: int,
    label: str = '普通攻击',
) -> bytes:
    """One native ACTION_ATTACK 1042 record between the two duel actors.

    与 PVE 的 battle_action_frame 同构，但回合号取对决共享轮次，
    攻守双方都是真实玩家 actor id（两个客户端各有一份同 id 参与者），
    因此同一批 1042 可以直接广播给双方。
    """
    return encode_frame(1042, [
        integer(round_number),
        integer(int(actor_id)),
        integer(int(target_id)),
        byte(1),                 # ACTION_ATTACK
        byte(1),                 # one hit
        byte(0),
        integer(0),              # sender visual effect id
        integer(0),              # target visual effect id
        string(label),
        integer(1),              # BattleEffect count
        integer(int(target_id)),  # effect target
        integer(0),              # normal hit reaction and damage number
        integer(22),             # HP delta effect
        integer(-max(1, damage)),
        string(''),
    ])


def duel_defend_frame(duel, round_number: int, *, actor_id: int) -> bytes:
    """One native ACTION_DEFEND 1042 record without an HP effect."""
    return encode_frame(1042, [
        integer(round_number),
        integer(int(actor_id)),
        integer(int(actor_id)),
        byte(2),                 # ACTION_DEFEND
        byte(1),
        byte(0),
        integer(0),
        integer(0),
        string('防御'),
        integer(0),              # no BattleEffect
    ])


