"""Mirror the APK's 60011 packed images for native 1502 resource responses."""
from __future__ import annotations

import argparse
import struct
import zipfile
from pathlib import Path


IMAGE_IDS = range(60011000, 60011126)


def read_records(index: bytes) -> tuple[list[tuple[int, int, int]], bytes]:
    size = struct.unpack_from('>H', index)[0]
    return ([struct.unpack_from('>IBH', index, position)
             for position in range(2, 2 + size, 7)], index[2 + size:])


def export_images(apk: Path, destination: Path) -> None:
    with zipfile.ZipFile(apk) as archive:
        index = archive.read('assets/res/images/images.o')
        parsed, _suffix = read_records(index)
        source_records = {
            image_id: (container, offset)
            for image_id, container, offset in parsed
        }
        missing = sorted(set(IMAGE_IDS) - source_records.keys())
        if missing:
            raise ValueError(f'APK has no 60011 images: {missing}')
        destination.mkdir(parents=True, exist_ok=True)
        for old in destination.glob('png*.p'):
            old.unlink()
        source_containers = sorted({source_records[image_id][0] for image_id in IMAGE_IDS})
        container_map = {source: local for local, source in enumerate(source_containers)}
        for source_container, local_container in container_map.items():
            blob = archive.read(f'assets/res/images/png{source_container}.p')
            if len(blob) < 24:
                raise ValueError(f'60011 container {source_container} is truncated')
            (destination / f'png{local_container}.p').write_bytes(blob)
        records = bytearray()
        for image_id in IMAGE_IDS:
            source_container, offset = source_records[image_id]
            records.extend(struct.pack('>IBH', image_id, container_map[source_container], offset))
        (destination / 'images.o').write_bytes(struct.pack('>H', len(records)) + records)


def sync_runtime_cache(apk: Path, destination: Path) -> None:
    """Update the extracted image cache read by an already-running local server."""
    index_path = destination / 'images.o'
    index = index_path.read_bytes()
    parsed, suffix = read_records(index)
    kept = [record for record in parsed if record[0] not in IMAGE_IDS]
    used = {container for _image_id, container, _offset in kept}
    with zipfile.ZipFile(apk) as archive:
        apk_index = archive.read('assets/res/images/images.o')
        apk_parsed, _apk_suffix = read_records(apk_index)
        source_records = {
            image_id: (container, offset)
            for image_id, container, offset in apk_parsed
        }
        missing = sorted(set(IMAGE_IDS) - source_records.keys())
        if missing:
            raise ValueError(f'APK has no 60011 images: {missing}')
        source_containers = sorted({source_records[image_id][0] for image_id in IMAGE_IDS})
        available = [container for container in range(256) if container not in used]
        if len(available) < len(source_containers):
            raise ValueError('runtime image container numbers exceed one-byte index')
        container_map = dict(zip(source_containers, available))
        for source_container, local_container in container_map.items():
            (destination / f'png{local_container}.p').write_bytes(
                archive.read(f'assets/res/images/png{source_container}.p'))
        additions = bytearray()
        for image_id in IMAGE_IDS:
            container, offset = source_records[image_id]
            additions.extend(struct.pack('>IBH', image_id, container_map[container], offset))
    kept_bytes = b''.join(struct.pack('>IBH', *record) for record in kept)
    new_records = kept_bytes + additions
    index_path.write_bytes(struct.pack('>H', len(new_records)) + new_records + suffix)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('apk', type=Path)
    parser.add_argument('destination', type=Path)
    parser.add_argument('--runtime-cache', type=Path,
                        help='also update the extracted cache used by a running server')
    args = parser.parse_args()
    export_images(args.apk, args.destination)
    if args.runtime_cache is not None:
        sync_runtime_cache(args.apk, args.runtime_cache)
