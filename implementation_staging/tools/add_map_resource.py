from __future__ import annotations

import argparse
import zipfile
from pathlib import Path


def clone_info(info: zipfile.ZipInfo) -> zipfile.ZipInfo:
    cloned = zipfile.ZipInfo(info.filename, info.date_time)
    cloned.compress_type = info.compress_type
    cloned.comment = info.comment
    cloned.extra = info.extra
    cloned.internal_attr = info.internal_attr
    cloned.external_attr = info.external_attr
    cloned.create_system = info.create_system
    cloned.flag_bits = info.flag_bits
    return cloned


def add_map_resources(source: Path, destination: Path, reference: Path, tile_map: Path, map_id: int) -> None:
    ref_name = f'assets/res/map/{map_id}.map.ref'
    tile_name = f'assets/res/map/{map_id}.map.o'
    replacement = {
        ref_name: reference.read_bytes(),
        tile_name: tile_map.read_bytes(),
    }
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(source, 'r') as src, zipfile.ZipFile(destination, 'w', allowZip64=True) as dst:
        names = set(src.namelist())
        for info in src.infolist():
            # The APK is re-signed after this step.
            if info.filename.upper().startswith('META-INF/'):
                continue
            if info.filename in replacement:
                continue
            dst.writestr(clone_info(info), src.read(info.filename))
        for name, data in replacement.items():
            dst.writestr(name, data, compress_type=zipfile.ZIP_DEFLATED)
    print(f'added {ref_name} and {tile_name} to {destination}')


def main() -> None:
    parser = argparse.ArgumentParser(description='Add a local map resource alias to an unsigned APK')
    parser.add_argument('source', type=Path)
    parser.add_argument('destination', type=Path)
    parser.add_argument('--reference', type=Path, required=True)
    parser.add_argument('--tile-map', type=Path, required=True)
    parser.add_argument('--map-id', type=int, default=50000)
    args = parser.parse_args()
    add_map_resources(args.source, args.destination, args.reference, args.tile_map, args.map_id)


if __name__ == '__main__':
    main()
