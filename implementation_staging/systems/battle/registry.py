"""战斗系统静态资源目录：1502/1503 战斗资源与 1501 图片解析。"""
from __future__ import annotations

import logging
import struct
from pathlib import Path

from protocol import (
    Field, TYPE_BYTE, TYPE_INT, TYPE_SHORT,
    binary, byte, encode_frame, integer, long_integer, short, string,
)

LOG = logging.getLogger('piaomiao-local')

# Protocol 1502 multiplexes two different resource requests. Action 1 asks for
# a role .dat and is answered by 1503; actions 0/2 ask for an image and must be
# answered by 1501. The battle actors use logical model ids while the bundled
# role directory keeps the monster sprite after the same 0x200b20 offset used
# by map actors.
BATTLE_RESOURCE_MODEL_OFFSET = 0x200B20
BATTLE_RESOURCE_ALIASES = {
    # A normal kind-1 fighter is constructed with logical model 6. The thin
    # APK does not bundle role/6.dat; its preloaded composite-player layout is
    # role/100000.dat, which is the matching server-delivered template.
    6: 100_000,
}
# The APK requests role/0.dat for the built-in basic-attack animation.  This
# is an optional empty effect definition in the original client; completing
# the 1503 transfer with zero bytes lets the animation queue advance while
# the accompanying image atlas is still loaded normally.
BATTLE_EMPTY_RESOURCE_IDS = {0}
PNG_QUERY_MAIN_CACHE = 0
PNG_QUERY_ROLE_CACHE = 2
def _build_artifact_dirs() -> tuple[Path, ...]:
    project_dir = Path(__file__).resolve().parents[2]
    return (
        project_dir / 'build_artifacts' / 'build',
        project_dir / 'build',
    )


def _battle_role_resource_candidates(model_id: int) -> list[tuple[str, int, Path]]:
    build_dirs = _build_artifact_dirs()
    role_dirs = (
        Path(__file__).resolve().parents[2] / 'data' / 'role',
        *(
            build_dir / 'weapon-apk-extracted' / 'assets' / 'res' / 'role'
            for build_dir in build_dirs
        ),
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
    """Describe which 1502 action=1 lookup branch would be used.

    Read-only: this function does not encode 1503 and is not consulted by
    ``battle_resource_path`` when building a response.
    """
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

def battle_resource_path(model_id: int) -> Path | None:
    """Resolve a logical model to a local override or bundled APK role .dat."""
    for _branch, _resolved_id, candidate in _battle_role_resource_candidates(model_id):
        if candidate.is_file():
            return candidate
    return None

def _signed_int32(value: int) -> int:
    """Return an unsigned APK integer in Java's signed-int representation."""
    value &= 0xFFFFFFFF
    return value - 0x100000000 if value >= 0x80000000 else value


def battle_image_resource(image_id: int) -> tuple[int, int, int, int, int, int, int, int, int, bytes] | None:
    """Read one proprietary image record from the APK/JAR image sets.

    The client reconstructs a regular indexed PNG from the RGB565 palette and
    the stored IDAT bytes. Some role layers request a direction/variant id 100
    above the base atlas id; the bundled index only stores that base id. The
    APK is a thin client and omits some player images which remain available
    in the original client JAR, so that extracted set is used as a fallback.
    """
    image_dirs = (
        *(
            build_dir / resource_set / 'res' / 'images'
            for build_dir in _build_artifact_dirs()
            for resource_set in ('weapon-apk-extracted/assets', 'jar-images')
        ),
    )

    source_id = image_id
    image_dir: Path | None = None
    record: tuple[int, int] | None = None
    # Prefer an exact id from either resource set before trying the directional
    # id alias. This prevents an APK alias from masking an exact JAR resource.
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
                record_id, container_number, data_offset = struct.unpack_from('>IBH', records, offset)
                if record_id != candidate_id:
                    continue
                container_path = candidate_dir / f'png{container_number}.p'
                if not container_path.is_file():
                    continue
                source_id = candidate_id
                image_dir = candidate_dir
                record = (container_number, data_offset)
                break
            if record is not None:
                break
        if record is not None:
            break
    if record is None or image_dir is None:
        return None

    container_number, data_offset = record
    container_path = image_dir / f'png{container_number}.p'
    if not container_path.is_file():
        # The original JAR index contains a few combat-effect records that
        # reuse container numbers shipped by the APK.  Keep the JAR index
        # metadata (including the correct record offset), but transparently
        # source the matching container from the APK when the JAR omitted it.
        for candidate_dir in image_dirs:
            candidate_path = candidate_dir / f'png{container_number}.p'
            if candidate_path.is_file():
                container_path = candidate_path
                break
        else:
            return None
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


