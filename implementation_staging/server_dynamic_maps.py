from __future__ import annotations

import asyncio
import logging
from pathlib import Path

import server as _server
from consignment_protocol import consignment_category_frame, consignment_screen_frame
from dynamic_map_builder import (
    materialize_all_dynamic_maps,
    merge_dynamic_maps_into_registry_payload,
)
from protocol import binary, byte, decode_frame, encode_frame, field_values, integer, short, string


LOG = logging.getLogger('piaomiao-local')
MAP_REF_CHUNK_SIZE = 12_000
MAX_MAP_REF_TRANSFER_SIZE = 0x7FFF
BOSS_EFFECT_CARRIER_DAT_ID = 3_000_100
BOSS_EFFECT_RESOURCE_ID = 3_000_000
ROAMING_BOSS_MAP_ID = 58
ROAMING_BOSS_ID = 700_001
ROAMING_BOSS_MODEL_OFFSET = 2_100_000
ROAMING_BOSS_EFFECT_MASK = 0x800000
ROAMING_BOSS_EFFECT_REQUEST_IMAGE_ID = 70_600
ROAMING_BOSS_EFFECT_SOURCE_IMAGE_ID = 70_000
ROAMING_BOSS_MOVE_DELAY_SECONDS = 3.0
ROAMING_BOSS_TARGET_X = 12
ROAMING_BOSS_TARGET_Y = 28
CONSIGNMENT_MERCHANT_OPTION = 1
_ORIGINAL_MAP_ENTER_FRAMES = _server.map_enter_frames
_ORIGINAL_LOAD_MAP_REGISTRY = _server.load_map_registry
_ORIGINAL_MAP_NPC_FRAME = _server.map_npc_frame
_ORIGINAL_MAP_NPC_DIALOGUE_FRAMES = _server.map_npc_dialogue_frames
_ORIGINAL_NPC_DIALOGUE_OPTION_FRAMES = _server.npc_dialogue_option_frames
_ORIGINAL_BATTLE_IMAGE_RESOURCE = _server.battle_image_resource
_ORIGINAL_SEND = _server.LocalGameServer._send


def map_ref_path(map_id: int) -> Path:
    """Return the server-side map.ref path for one logical map id."""
    return Path(_server.__file__).resolve().parent / 'maps' / f'{int(map_id)}.map.ref'


def map_ref_transfer_frames(
    definition,
    *,
    chunk_size: int = MAP_REF_CHUNK_SIZE,
) -> list[bytes]:
    """Encode one server-side .map.ref as APK-native 1407/11+12 chunks.

    Reverse-engineered APK path:
      1407 subtype 11/12 -> pmsj.work.b.m.a(short total, short offset, byte[])
      -> m.z byte buffer -> m.C() map.ref parser.

    Wire fields are [byte subtype, short total_size, binary chunk, short offset].
    The first chunk uses subtype 11 and continuations use subtype 12. The APK
    stores total length and offset as signed Java shorts, so this compatibility
    path deliberately rejects resources above 32767 bytes rather than silently
    wrapping their offsets.
    """
    if chunk_size <= 0:
        raise ValueError('map.ref chunk size must be positive')

    path = map_ref_path(definition.id)
    if not path.is_file():
        return []

    data = path.read_bytes()
    total = len(data)
    if total <= 0:
        raise ValueError(f'map.ref is empty: {path}')
    if total > MAX_MAP_REF_TRANSFER_SIZE:
        raise ValueError(
            f'map.ref {path} is {total} bytes; APK 1407 map.ref transfer '
            f'uses signed short length/offset and supports at most {MAX_MAP_REF_TRANSFER_SIZE}'
        )

    frames: list[bytes] = []
    for offset in range(0, total, chunk_size):
        chunk = data[offset:offset + chunk_size]
        subtype = 11 if offset == 0 else 12
        frames.append(encode_frame(1407, [
            byte(subtype),
            short(total),
            binary(chunk),
            short(offset),
        ]))
    return frames


def roaming_boss_image_resource(image_id: int):
    """Resolve q's native 40000 foot-ring image to the verified APK 70000 pixels.

    APK ``role/40000.dat`` is the native q-actor ground-ring resource selected
    by property-6 bit ``0x800000``.  Its three mirrored sprite bands are laid
    out for image 70600, but this thin APK does not index 70600 while bundled
    image 70000 has the exact 44x73 / 43x23 / 42x22 geometry already verified
    on-device through 3000000.dat.  Reply to a 70600 cache miss with the 70000
    payload while the outer 1501 frame keeps the requested id 70600.
    """
    source_id = (
        ROAMING_BOSS_EFFECT_SOURCE_IMAGE_ID
        if int(image_id) == ROAMING_BOSS_EFFECT_REQUEST_IMAGE_ID
        else int(image_id)
    )
    if source_id != int(image_id):
        LOG.info(
            'MAP_BOSS_EFFECT_IMAGE_ALIAS requested=%d source=%d',
            int(image_id),
            source_id,
        )
    return _ORIGINAL_BATTLE_IMAGE_RESOURCE(source_id)


def roaming_boss_spawn_frame(definition) -> bytes:
    """Create the map-58 Boss through APK-native 2028 / ``b/q``.

    The old 1126 path adds 2,100,000 to the configured raw model before
    creating ``b/n``.  Protocol 2028 creates ``b/q`` directly from field 3, so
    preserve the same visible resource by applying that offset server-side.
    Fields 1/2 are map coordinates; ``W(w)`` stores them as actor properties
    and immediately seeds the q actor position from those properties.

    q.p() reads property 4 as the actor display/interaction name. Keep it as a
    STRING: sending an INT placeholder leaves the roaming actor without the
    metadata used by the native map-object interaction path. Property 6 is the
    q effect mask; bit 0x800000 calls ``q.c(40000, true)`` so the ring remains
    attached to the moving actor itself.
    """
    monster = getattr(definition, 'monster', None)
    if monster is None:
        raise ValueError('roaming Boss requires a map monster definition')
    resource_id = int(monster.model) + ROAMING_BOSS_MODEL_OFFSET
    return encode_frame(2028, [
        integer(int(monster.id)),
        short(int(monster.x)),
        short(int(monster.y)),
        integer(resource_id),
        string(str(monster.name)),
        integer(0),
        integer(ROAMING_BOSS_EFFECT_MASK),
    ])


def roaming_boss_move_frame(
    actor_id: int,
    source_x: int,
    source_y: int,
    target_x: int,
    target_y: int,
) -> bytes:
    """Encode one native 1005 map movement update for a q actor.

    APK 1005 reads actor id from field 0 and target x/y from short fields 3/4.
    Fields 1/2 are retained as short source coordinates; the q branch does not
    read them, but keeping the coordinate-shaped five-field record mirrors the
    native movement packet without inventing a new protocol.
    """
    return encode_frame(1005, [
        integer(int(actor_id)),
        short(int(source_x)),
        short(int(source_y)),
        short(int(target_x)),
        short(int(target_y)),
    ])


def _replace_roaming_boss_spawn(definition, frames: list[bytes]) -> list[bytes]:
    """Replace only map 58's generic 1126 Boss record with native 2028/q."""
    monster = getattr(definition, 'monster', None)
    if int(getattr(definition, 'id', 0)) != ROAMING_BOSS_MAP_ID or monster is None:
        return frames
    if int(getattr(monster, 'id', 0)) != ROAMING_BOSS_ID:
        return frames

    result: list[bytes] = []
    replaced = False
    for frame in frames:
        try:
            message_id, fields = decode_frame(frame)
            values = field_values(fields)
        except Exception:
            result.append(frame)
            continue
        if (
            not replaced
            and message_id == 1126
            and len(values) >= 3
            and int(values[2]) == ROAMING_BOSS_ID
        ):
            result.append(roaming_boss_spawn_frame(definition))
            replaced = True
        else:
            result.append(frame)
    return result


def _roaming_boss_spawn_position(frames: tuple[bytes, ...]) -> tuple[int, int] | None:
    """Return source coordinates when this send batch contains the 2028 Boss spawn."""
    for frame in frames:
        try:
            message_id, fields = decode_frame(frame)
            values = field_values(fields)
        except Exception:
            continue
        if message_id == 2028 and len(values) >= 3 and int(values[0]) == ROAMING_BOSS_ID:
            return int(values[1]), int(values[2])
    return None


async def _send_roaming_boss_probe(
    server,
    writer,
    source_x: int,
    source_y: int,
    *,
    cipher,
    lock,
) -> None:
    """After map entry, issue one movement target to prove native q walking."""
    try:
        await asyncio.sleep(ROAMING_BOSS_MOVE_DELAY_SECONDS)
        frame = roaming_boss_move_frame(
            ROAMING_BOSS_ID,
            source_x,
            source_y,
            ROAMING_BOSS_TARGET_X,
            ROAMING_BOSS_TARGET_Y,
        )
        await _ORIGINAL_SEND(server, writer, frame, cipher=cipher, lock=lock)
        LOG.info(
            'MAP_BOSS_NATIVE_MOVE actor=%d from=(%d,%d) to=(%d,%d) protocol=1005',
            ROAMING_BOSS_ID,
            source_x,
            source_y,
            ROAMING_BOSS_TARGET_X,
            ROAMING_BOSS_TARGET_Y,
        )
    except asyncio.CancelledError:
        raise
    except (ConnectionError, OSError):
        LOG.info('MAP_BOSS_NATIVE_MOVE skipped actor=%d connection_closed=1', ROAMING_BOSS_ID)


async def dynamic_send(server, writer, *frames: bytes, cipher=None, lock=None) -> None:
    """Preserve normal sends and schedule one delayed q movement after its spawn."""
    await _ORIGINAL_SEND(server, writer, *frames, cipher=cipher, lock=lock)
    source = _roaming_boss_spawn_position(tuple(frames))
    if source is not None:
        asyncio.create_task(_send_roaming_boss_probe(
            server,
            writer,
            source[0],
            source[1],
            cipher=cipher,
            lock=lock,
        ))


def map_npc_frame_with_effect(definition, npc) -> bytes:
    """Attach the verified 3000000 effect to the dedicated 3000100 carrier.

    APK ``main/e.X`` creates a native 2030 ``pmsj.work.b/t`` actor from the
    normal NPC record.  Integer field 5 is the built-in attached-display code:
    ``base = value // 100 * 100`` and ``index = value % 100`` before calling
    ``t.a(base, index, true)``.  Therefore 3000000 selects resource 3000000,
    animation index 0, while 3000100.dat remains an invisible carrier body.

    Field 7 bit 1 is also native behavior. ``m.a(t)`` routes such actors into
    the map manager's W vector. W is merged into the render list but omitted
    from ``m.l(x, y)`` hit-testing, so the effect stays visible without adding
    another clickable/selected NPC target over the Boss.
    """
    if int(getattr(npc, 'dat_id', 0)) != BOSS_EFFECT_CARRIER_DAT_ID:
        return _ORIGINAL_MAP_NPC_FRAME(definition, npc)

    return encode_frame(2030, [
        integer(npc.id),
        integer(npc.x),
        integer(npc.y),
        integer(npc.dat_id),
        integer(npc.direction),
        integer(BOSS_EFFECT_RESOURCE_ID),
        string(npc.name),
        integer(2),
        string(npc.label),
    ])


def consignment_map_npc_dialogue_frames(npc, role, settings) -> list[bytes]:
    """Expose the APK's original consignment page from a consignment NPC.

    Screen 6 (2032) remains the native NPC dialogue overlay.  Selecting the
    single 寄售 option is handled by ``consignment_npc_dialogue_option_frames``
    and opens screen 613 / ``pmsj.work.e.ev``.
    """
    if str(getattr(npc, 'service', '')) != 'consignment_merchant':
        return _ORIGINAL_MAP_NPC_DIALOGUE_FRAMES(npc, role, settings)

    def dialogue_record(kind: int, *, option_id: int = 0, text: str = '', icon: int = 0):
        return [
            integer(0),
            integer(0),
            integer(0),
            short(0),
            integer(option_id),
            byte(kind),
            string(text),
            integer(icon),
        ]

    introduction = str(getattr(npc, 'introduction', '') or getattr(npc, 'label', '') or getattr(npc, 'name', ''))
    records = [*dialogue_record(1, text=introduction)]
    records.extend(dialogue_record(
        2,
        option_id=CONSIGNMENT_MERCHANT_OPTION,
        text='寄售',
    ))
    records.extend(dialogue_record(2, option_id=0, text='结束对话'))
    records.extend(dialogue_record(100))
    return [encode_frame(2032, [
        integer(int(npc.id)),
        byte(len(records) // 8),
        *records,
    ])]


def consignment_npc_dialogue_option_frames(settings, role, state, option_id: int) -> list[bytes]:
    """Open native consignment screen 613 and bootstrap native item categories."""
    if role is None or int(option_id) != CONSIGNMENT_MERCHANT_OPTION:
        return _ORIGINAL_NPC_DIALOGUE_OPTION_FRAMES(settings, role, state, option_id)

    try:
        definition = _server.settings_for_role(settings, role)
    except ValueError:
        return _ORIGINAL_NPC_DIALOGUE_OPTION_FRAMES(settings, role, state, option_id)

    if state.map_id != definition.id or state.npc_id is None:
        return _ORIGINAL_NPC_DIALOGUE_OPTION_FRAMES(settings, role, state, option_id)

    npc = _server.map_npc_for_object_id(definition, state.npc_id)
    if npc is None or str(getattr(npc, 'service', '')) != 'consignment_merchant':
        return _ORIGINAL_NPC_DIALOGUE_OPTION_FRAMES(settings, role, state, option_id)

    try:
        LOG.info(
            'CONSIGNMENT_MERCHANT_OPEN role_id=%d npc_id=%d screen=613 protocol=1138 categories=28',
            int(role.get('id', 0)),
            int(npc.id),
        )
        return [
            _server.map_object_interaction_ack_frame(0),
            consignment_screen_frame(),
            consignment_category_frame(),
        ]
    finally:
        state.clear()


def dynamic_map_enter_frames(definition, role_id: int | None = None) -> list[bytes]:
    """Prefer server-delivered map.ref and use native q actor for the map-58 Boss."""
    original = _replace_roaming_boss_spawn(
        definition,
        list(_ORIGINAL_MAP_ENTER_FRAMES(definition, role_id)),
    )
    transfer = map_ref_transfer_frames(definition)
    if not transfer:
        return original

    if not original:
        raise ValueError(f'map {definition.id} produced no enter frames')

    # Phone-verified order: action 13 must establish the native transition
    # state before 1407/11+12 causes m.C() to parse the target map.ref.
    transition_start = _server.map_action(
        definition,
        13,
        status=1,
        role_id=role_id,
    )
    continuation = original[1:]
    LOG.info(
        'MAP_REF_STREAM map=%d path=%s bytes=%d chunks=%d '
        'protocol=1010/13->1407/11+12->1010/14+105',
        int(definition.id),
        map_ref_path(definition.id),
        map_ref_path(definition.id).stat().st_size,
        len(transfer),
    )
    return [transition_start, *transfer, *continuation]


def dynamic_load_map_registry(payload, npc_catalog=None, appearance_catalog=None):
    """Inject maps/<id>/map.json registry metadata before typed validation."""
    merged = merge_dynamic_maps_into_registry_payload(payload)
    return _ORIGINAL_LOAD_MAP_REGISTRY(
        merged,
        npc_catalog=npc_catalog,
        appearance_catalog=appearance_catalog,
    )


def install_dynamic_map_support() -> None:
    """Install launcher-only hooks without polluting modules that merely import us."""
    _server.LocalGameServer._send = dynamic_send
    _server.battle_image_resource = roaming_boss_image_resource
    _server.map_npc_frame = map_npc_frame_with_effect
    _server.map_enter_frames = dynamic_map_enter_frames
    _server.load_map_registry = dynamic_load_map_registry
    _server.map_npc_dialogue_frames = consignment_map_npc_dialogue_frames
    _server.npc_dialogue_option_frames = consignment_npc_dialogue_option_frames


def main() -> None:
    built_maps = materialize_all_dynamic_maps()
    for built in built_maps:
        LOG.info(
            'DYNAMIC_MAP_READY map=%d ref=%s ref_bytes=%d map_o=%s map_o_bytes=%d',
            built.map_id,
            built.map_ref_path,
            built.map_ref_bytes,
            built.map_o_path,
            built.map_o_bytes,
        )
    LOG.info('DYNAMIC_MAP_SCAN count=%d', len(built_maps))
    install_dynamic_map_support()
    _server.main()


if __name__ == '__main__':
    main()
