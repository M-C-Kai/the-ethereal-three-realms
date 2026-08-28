from __future__ import annotations

import argparse
import json
import struct
import zipfile
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class MapWorldEntry:
    x: int
    y: int
    icon: int
    map_ids: tuple[int, ...]
    label: str


def parse_mapworld(data: bytes) -> tuple[list[MapWorldEntry], list[tuple[int, int]]]:
    offset = 0
    entries: list[MapWorldEntry] = []
    markers: list[tuple[int, int]] = []
    while offset < len(data):
        if offset + 5 > len(data):
            raise ValueError(f'truncated mapworld record at byte {offset}')
        record_type = data[offset]
        x, y = struct.unpack_from('>hh', data, offset + 1)
        offset += 5
        if record_type == 2:
            markers.append((x + 5, y + 5))
            continue
        if record_type != 1:
            raise ValueError(f'unknown mapworld record type {record_type} at byte {offset - 5}')
        if offset + 2 > len(data):
            raise ValueError('truncated mapworld map group header')
        icon = data[offset]
        map_count = data[offset + 1]
        offset += 2
        ids_size = map_count * 4
        if offset + ids_size + 2 > len(data):
            raise ValueError('truncated mapworld map id list')
        map_ids = struct.unpack_from(f'>{map_count}I', data, offset)
        offset += ids_size
        text_length = struct.unpack_from('>H', data, offset)[0]
        offset += 2
        if offset + text_length > len(data):
            raise ValueError('truncated mapworld UTF-8 label')
        label = data[offset:offset + text_length].decode('utf-8')
        offset += text_length
        entries.append(MapWorldEntry(x, y, icon, map_ids, label))
    return entries, markers


def main() -> None:
    parser = argparse.ArgumentParser(description='Inspect map IDs and labels from assets/res/mapworld.o')
    parser.add_argument('--apk', type=Path, required=True)
    parser.add_argument('--map-id', type=int)
    parser.add_argument('--name')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()

    with zipfile.ZipFile(args.apk) as archive:
        entries, markers = parse_mapworld(archive.read('assets/res/mapworld.o'))
    selected = [
        entry for entry in entries
        if (args.map_id is None or args.map_id in entry.map_ids)
        and (args.name is None or args.name in entry.label)
    ]
    if args.json:
        print(json.dumps({
            'entries': [asdict(entry) for entry in selected],
            'entry_count': len(entries),
            'marker_count': len(markers),
        }, ensure_ascii=False, indent=2))
        return
    for entry in selected:
        title, _, description = entry.label.partition('_')
        print(
            f'{title}: map_ids={list(entry.map_ids)} world=({entry.x},{entry.y}) '
            f'icon={entry.icon}'
        )
        if description:
            print(f'  {description.replace("_", " / ")}')
    print(f'matched {len(selected)} of {len(entries)} map groups; {len(markers)} world markers')


if __name__ == '__main__':
    main()
