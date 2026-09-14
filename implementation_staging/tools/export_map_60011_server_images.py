"""Mirror the APK's 60011 packed images for native 1502 resource responses."""
from __future__ import annotations

import argparse
import struct
import zipfile
from pathlib import Path


IMAGE_IDS = range(60011000, 60011040)


def export_images(apk: Path, destination: Path) -> None:
    with zipfile.ZipFile(apk) as archive:
        index = archive.read('assets/res/images/images.o')
        size = struct.unpack_from('>H', index)[0]
        source_records = {
            image_id: (container, offset)
            for image_id, container, offset in
            (struct.unpack_from('>IBH', index, position)
             for position in range(2, 2 + size, 7))
        }
        missing = sorted(set(IMAGE_IDS) - source_records.keys())
        if missing:
            raise ValueError(f'APK has no 60011 images: {missing}')
        destination.mkdir(parents=True, exist_ok=True)
        records = bytearray()
        for local_container, image_id in enumerate(IMAGE_IDS):
            source_container, offset = source_records[image_id]
            if offset != 0:
                raise ValueError(f'60011 image {image_id} has unexpected offset {offset}')
            blob = archive.read(f'assets/res/images/png{source_container}.p')
            if len(blob) < 24:
                raise ValueError(f'60011 image {image_id} is truncated')
            (destination / f'png{local_container}.p').write_bytes(blob)
            records.extend(struct.pack('>IBH', image_id, local_container, 0))
        (destination / 'images.o').write_bytes(struct.pack('>H', len(records)) + records)


def sync_runtime_cache(apk: Path, destination: Path) -> None:
    """Update the extracted image cache read by an already-running local server."""
    index_path = destination / 'images.o'
    index = index_path.read_bytes()
    size = struct.unpack_from('>H', index)[0]
    records = index[2:2 + size]
    existing_ids = {struct.unpack_from('>I', records, offset)[0]
                    for offset in range(0, len(records), 7)}
    if existing_ids.intersection(IMAGE_IDS):
        if set(IMAGE_IDS).issubset(existing_ids):
            return
        raise ValueError('runtime cache contains a partial 60011 image set')
    containers = [int(path.stem[3:]) for path in destination.glob('png*.p')]
    first_container = max(containers, default=-1) + 1
    if first_container + len(IMAGE_IDS) - 1 > 255:
        raise ValueError('runtime image container numbers exceed one-byte index')
    with zipfile.ZipFile(apk) as archive:
        apk_index = archive.read('assets/res/images/images.o')
        apk_size = struct.unpack_from('>H', apk_index)[0]
        source_records = {
            image_id: (container, offset)
            for image_id, container, offset in
            (struct.unpack_from('>IBH', apk_index, position)
             for position in range(2, 2 + apk_size, 7))
        }
        additions = bytearray()
        for local_index, image_id in enumerate(IMAGE_IDS):
            container, offset = source_records[image_id]
            if offset != 0:
                raise ValueError(f'60011 image {image_id} has unexpected offset {offset}')
            (destination / f'png{first_container + local_index}.p').write_bytes(
                archive.read(f'assets/res/images/png{container}.p'))
            additions.extend(struct.pack('>IBH', image_id, first_container + local_index, 0))
    new_records = records + additions
    index_path.write_bytes(struct.pack('>H', len(new_records)) + new_records + index[2 + size:])


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
