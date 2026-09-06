from __future__ import annotations

import logging
from pathlib import Path

import server as _server
from protocol import binary, byte, encode_frame, short


LOG = logging.getLogger('piaomiao-local')
MAP_REF_CHUNK_SIZE = 12_000
MAX_MAP_REF_TRANSFER_SIZE = 0x7FFF
_ORIGINAL_MAP_ENTER_FRAMES = _server.map_enter_frames


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
    The first chunk uses subtype 11 and continuations use subtype 12.  The APK
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
    """Prefer server-delivered map.ref, otherwise preserve the old APK-local path."""
    original = list(_ORIGINAL_MAP_ENTER_FRAMES(definition, role_id))
    transfer = map_ref_transfer_frames(definition)
    if not transfer:
        return original

    # The old first frame is 1010/action=13.  Replace it with status=1 so the
    # client does not reopen assets/res/map/{mapId}.map.ref after m.z has just
    # been filled and parsed by the 1407 transfer.
    if not original:
        raise ValueError(f'map {definition.id} produced no enter frames')
    original[0] = _server.map_action(
        definition,
        13,
        status=1,
        role_id=role_id,
    )
    LOG.info(
        'MAP_REF_STREAM map=%d path=%s bytes=%d chunks=%d protocol=1407/11+12',
        int(definition.id),
        map_ref_path(definition.id),
        map_ref_path(definition.id).stat().st_size,
        len(transfer),
    )
    return [*transfer, *original]


# Patch only the narrow map-reference entry point.  All existing server
# dispatch, battle, NPC, inventory and persistence code remains unchanged.
_server.map_enter_frames = dynamic_map_enter_frames


def main() -> None:
    _server.main()


if __name__ == '__main__':
    main()
