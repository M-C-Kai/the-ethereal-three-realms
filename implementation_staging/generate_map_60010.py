from __future__ import annotations

import hashlib
import json
from pathlib import Path

from map_o import MapO
from tools.map_ref_generator import from_spec, serialize_map_ref


MAP_ID = 60010
WIDTH = 24
HEIGHT = 24
EXPECTED_REF_SHA256 = '7eb419659ca28a006bc0c1a0980e863472fcdd45149c5e90076e1f991c7afceb'
EXPECTED_MAP_O_SHA256 = 'f92cb8de6d5816e3311c2ad73f2ebfcbd069526da4349aa81855fda8ed8b3a4a'


def project_dir() -> Path:
    return Path(__file__).resolve().parent


def ref_spec_path() -> Path:
    return project_dir() / 'maps' / f'{MAP_ID}.map.ref.json'


def output_ref_path() -> Path:
    return project_dir() / 'maps' / f'{MAP_ID}.map.ref'


def output_map_o_path() -> Path:
    return project_dir() / 'maps' / f'{MAP_ID}.map.o'


def _layout() -> tuple[list[int], list[bool], list[bool]]:
    cells: list[int] = []
    collision: list[bool] = []
    mirror: list[bool] = []
    landmarks = {(6, 6), (17, 7), (8, 16), (16, 17)}

    for y in range(HEIGHT):
        for x in range(WIDTH):
            blocked = False
            if x in (0, WIDTH - 1) or y in (0, HEIGHT - 1):
                value = 5
                blocked = True
            elif (x, y) in landmarks:
                value = 4
                blocked = True
            elif x in (11, 12) or y in (11, 12):
                value = 3
            elif (x // 4 + y // 4) % 3 == 0:
                value = 1
            elif (x + y) % 5 == 0:
                value = 2
            else:
                value = 0
            cells.append(value)
            collision.append(blocked)
            mirror.append((x + y) % 17 == 0 and value < 4)

    # Keep the centre spawn and its immediate exits traversable.
    for x, y in ((12, 12), (12, 13), (11, 12), (13, 12)):
        index = y * WIDTH + x
        cells[index] = 3
        collision[index] = False
        mirror[index] = False
    return cells, collision, mirror


def build_map_ref() -> bytes:
    spec = json.loads(ref_spec_path().read_text(encoding='utf-8'))
    records, composites = from_spec(spec)
    data = serialize_map_ref(records, composites)
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_REF_SHA256:
        raise ValueError(f'60010.map.ref digest mismatch: {digest}')
    return data


def build_map_o() -> bytes:
    cells, collision, mirror = _layout()
    result = MapO(
        width=WIDTH,
        height=HEIGHT,
        map_type=0,
        tile_definitions=[0, 1, 2, 3, 4, 5],
        tiles=cells,
        collision=collision,
        mirror=mirror,
    )
    data = result.to_file()
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_MAP_O_SHA256:
        raise ValueError(f'60010.map.o digest mismatch: {digest}')
    return data


def ensure_map_60010() -> tuple[Path, Path]:
    ref_path = output_ref_path()
    map_o_path = output_map_o_path()
    ref_data = build_map_ref()
    map_o_data = build_map_o()

    if not ref_path.is_file() or ref_path.read_bytes() != ref_data:
        ref_path.write_bytes(ref_data)
    if not map_o_path.is_file() or map_o_path.read_bytes() != map_o_data:
        map_o_path.write_bytes(map_o_data)
    return ref_path, map_o_path


if __name__ == '__main__':
    ref_path, map_o_path = ensure_map_60010()
    print(f'wrote {ref_path} ({ref_path.stat().st_size} bytes)')
    print(f'wrote {map_o_path} ({map_o_path.stat().st_size} bytes)')
