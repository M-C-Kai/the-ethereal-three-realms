from __future__ import annotations

import logging
import struct
from pathlib import Path

from protocol import binary, byte, encode_frame, integer, short


LOG = logging.getLogger('piaomiao-local')
# battle/ is nested directly under implementation_staging; resource paths are
# still rooted at implementation_staging just as they were before extraction.
PROJECT_DIR = Path(__file__).resolve().parent.parent

BATTLE_RESOURCE_MODEL_OFFSET = 0x200B20
BATTLE_RESOURCE_ALIASES = {
    6: 100_000,
}
BATTLE_EMPTY_RESOURCE_IDS = {0}
PNG_QUERY_MAIN_CACHE = 0
PNG_QUERY_ROLE_CACHE = 2


def _battle_role_resource_candidates(model_id: int) -> list[tuple[str, int, Path]]:
    role_dirs = (
        PROJECT_DIR / 'data' / 'role',
        PROJECT_DIR / 'build' / 'weapon-apk-extracted' / 'assets' / 'res' / 'role',
    )
    alias = BATTLE_RESOURCE_ALIASES.get(model_id)
    mapped = model_id + BATTLE_RESOURCE_MODEL_OFFSET
    ids: list[tuple[str, int]] = [('direct', model_id)]
    if alias is not None:
        ids.append(('alias', alias))
    if mapped != model_id:
        ids.append(('offset', mapped))
    return [
        (branch, resolved_id, role_dir / f'{resolved_id}.dat')
        for branch, resolved_id in ids
        for role_dir in role_dirs
    ]


def battle_resource_resolution(model_id: int) -> dict[str, object]:
    """Describe the role-DAT branch used by a 1502/action=1 query."""
    alias = BATTLE_RESOURCE_ALIASES.get(model_id)
    mapped = model_id + BATTLE_RESOURCE_MODEL_OFFSET
    for branch, resolved_id, path in _battle_role_resource_candidates(model_id):
        if path.is_file():
            return {
                'requested_id': model_id,
                'alias': alias,
                'offset_id': mapped if mapped != model_id else None,
                'branch': branch,
                'resolved_id': resolved_id,
                'resolved_path': str(path),
                'empty': False,
                'missing': False,
            }
    empty = model_id in BATTLE_EMPTY_RESOURCE_IDS
    return {
        'requested_id': model_id,
        'alias': alias,
        'offset_id': mapped if mapped != model_id else None,
        'branch': 'empty' if empty else 'missing',
        'resolved_id': None,
        'resolved_path': None,
        'empty': empty,
        'missing': not empty,
    }


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
    trace = f'battle_trace={trace_id}\n' if trace_id else ''
    return (
        'BATTLE_RESOURCE_QUERY\n'
        f'{trace}'
        f'user={username!r}\n'
        f'action={query_action}\n'
        f'ids={resource_ids}\n'
        f'battle_active={battle_active}\n'
        f'round={round_number}\n'
        f'resource_id={resource_id}\n'
        f"alias={resolution.get('alias')!r}\n"
        f"branch={resolution.get('branch')!r}\n"
        f"offset_id={resolution.get('offset_id')!r}\n"
        f"jar_fallback={resolution.get('jar_fallback', False)}\n"
        f"resolved_id={resolution.get('resolved_id')!r}\n"
        f"resolved_path={resolution.get('resolved_path')!r}\n"
        f'response_type={response_type}\n'
        f'chunks={chunks}'
    )


def battle_resource_path(model_id: int) -> Path | None:
    """Resolve a logical model to a local override or bundled APK role DAT."""
    for _branch, _resolved_id, candidate in _battle_role_resource_candidates(model_id):
        if candidate.is_file():
            return candidate
    return None


def battle_resource_frames(model_id: int) -> list[bytes]:
    """Return the two 1503 chunks expected by the APK role-resource loader."""
    path = battle_resource_path(model_id)
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
    fields = [integer(model_id), short(len(data)), short(len(data)), binary(data)]
    finish_fields = [integer(model_id), short(len(data)), short(0), binary(b'')]
    return [
        encode_frame(1503, [byte(0), *fields]),
        encode_frame(1503, [byte(2), *finish_fields]),
    ]


def _image_dirs() -> tuple[Path, Path]:
    build_dir = PROJECT_DIR / 'build'
    return (
        build_dir / 'weapon-apk-extracted' / 'assets' / 'res' / 'images',
        build_dir / 'jar-images' / 'res' / 'images',
    )


def _find_image_record(image_id: int) -> tuple[int, Path, tuple[int, int]] | None:
    """Return source id, directory and (container, offset) for one image."""
    for candidate_id in (image_id, image_id - 100):
        if candidate_id < 0:
            continue
        for candidate_dir in _image_dirs():
            index_path = candidate_dir / 'images.o'
            if not index_path.is_file():
                continue
            index = index_path.read_bytes()
            if len(index) < 2:
                continue
            index_size = struct.unpack_from('>H', index, 0)[0]
            records = index[2:2 + index_size]
            for offset in range(0, len(records) - 6, 7):
                record_id, container_number, data_offset = struct.unpack_from('>IBH', records, offset)
                if record_id != candidate_id:
                    continue
                container_path = candidate_dir / f'png{container_number}.p'
                if not container_path.is_file():
                    # Some JAR index records reuse a container bundled by APK.
                    fallback = next(
                        (
                            directory / f'png{container_number}.p'
                            for directory in _image_dirs()
                            if (directory / f'png{container_number}.p').is_file()
                        ),
                        None,
                    )
                    if fallback is None:
                        continue
                return candidate_id, candidate_dir, (container_number, data_offset)
    return None


def _signed_int32(value: int) -> int:
    value &= 0xFFFFFFFF
    return value - 0x100000000 if value >= 0x80000000 else value


def battle_image_resource(
    image_id: int,
) -> tuple[int, int, int, int, int, int, int, int, int, bytes] | None:
    """Read one proprietary image record from the APK/JAR image sets."""
    found = _find_image_record(image_id)
    if found is None:
        return None
    source_id, image_dir, record = found
    container_number, data_offset = record
    container_path = image_dir / f'png{container_number}.p'
    if not container_path.is_file():
        fallback = next(
            (
                directory / f'png{container_number}.p'
                for directory in _image_dirs()
                if (directory / f'png{container_number}.p').is_file()
            ),
            None,
        )
        if fallback is None:
            return None
        container_path = fallback

    container = container_path.read_bytes()
    if data_offset + 24 > len(container):
        return None

    position = data_offset
    group_count, group_index = container[position], container[position + 1]
    position += 2
    if group_count:
        position += (group_count - group_index - 1) * 2
    if position + 22 > len(container):
        return None
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
    ) = struct.unpack_from('>HHBBIIIHH', container, position)
    position += 22

    if group_count:
        position += group_index * palette_length
        palette = container[position:position + palette_length]
        position += palette_length
        position += (group_count - group_index - 1) * palette_length
    else:
        palette = container[position:position + palette_length]
        position += palette_length
    idat = container[position:position + idat_length]
    if len(palette) != palette_length or len(idat) != idat_length:
        return None

    if source_id != image_id:
        LOG.info('battle image alias requested=%d source=%d', image_id, source_id)
    if 'jar-images' in image_dir.parts:
        LOG.info('battle image JAR fallback image=%d source=%d', image_id, source_id)
    return (
        width,
        height,
        bit_depth,
        transparent_index,
        palette_crc,
        transparency_crc,
        header_crc,
        palette_length,
        idat_length,
        palette + idat,
    )


def battle_image_resolve_debug(image_id: int) -> dict[str, object]:
    """Describe which image lookup branch would be used without encoding."""
    found = _find_image_record(image_id)
    if found is None:
        return {
            'requested_id': image_id,
            'alias': None,
            'resolved_id': None,
            'resolved_path': None,
            'branch': 'missing',
            'jar_fallback': False,
            'missing': True,
        }
    candidate_id, candidate_dir, record = found
    container_number, _data_offset = record
    container_path = candidate_dir / f'png{container_number}.p'
    if not container_path.is_file():
        container_path = next(
            (
                directory / f'png{container_number}.p'
                for directory in _image_dirs()
                if (directory / f'png{container_number}.p').is_file()
            ),
            container_path,
        )
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


def battle_image_frames(query_action: int, image_id: int) -> list[bytes]:
    """Return 1501 image chunks followed by the client's 1502 redraw signal."""
    resource = battle_image_resource(image_id)
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

    return [frame(0, data), frame(2, b''), encode_frame(1502)]
