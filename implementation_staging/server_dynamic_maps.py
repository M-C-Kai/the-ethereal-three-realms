from __future__ import annotations

import logging
from pathlib import Path

import server as _server
from dynamic_map_builder import (
    materialize_all_dynamic_maps,
    merge_dynamic_maps_into_registry_payload,
)
from protocol import binary, byte, encode_frame, short


LOG = logging.getLogger('piaomiao-local')
MAP_REF_CHUNK_SIZE = 12_000
MAX_MAP_REF_TRANSFER_SIZE = 0x7FFF
_ORIGINAL_MAP_ENTER_FRAMES = _server.map_enter_frames
_ORIGINAL_LOAD_MAP_REGISTRY = _server.load_map_registry


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


def dynamic_map_enter_frames(definition, role_id: int | None = None) -> list[bytes]:
    """Prefer server-delivered map.ref while preserving native transition order."""
    original = list(_ORIGINAL_MAP_ENTER_FRAMES(definition, role_id))
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
    _server.map_enter_frames = dynamic_map_enter_frames
    _server.load_map_registry = dynamic_load_map_registry


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
