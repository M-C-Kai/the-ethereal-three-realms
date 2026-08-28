from __future__ import annotations

import json
import struct
import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from map_o import MapO
from tools.map_ref_renderer import (
    AssetReader,
    CompositeRenderer,
    CompositeTile,
    ImageRecord,
    Layer,
    RenderedTile,
)


MAP_ID = 50000


def encode_map_ref(records: list[ImageRecord], composites: list[CompositeTile]) -> bytes:
    output = bytearray(struct.pack('>HH', len(composites), len(records)))
    for record in records:
        output.extend(struct.pack(
            '>IBBBB',
            record.image_id,
            record.crop_x,
            record.crop_y,
            record.width,
            record.height,
        ))
    for composite in composites:
        output.extend(bytes((
            composite.flags,
            composite.terrain,
            composite.value_b,
            composite.value_c,
            len(composite.layers),
        )))
        for layer in composite.layers:
            output.extend(struct.pack('>hbbb', layer.reference, layer.x, layer.y, layer.transform))
    return bytes(output)


def build_reference() -> tuple[list[ImageRecord], list[CompositeTile], list[str]]:
    records: list[ImageRecord] = []

    def add(image_id: int, crop_x: int, crop_y: int, width: int, height: int) -> int:
        records.append(ImageRecord(image_id, crop_x, crop_y, width, height))
        return len(records) - 1

    grass = add(322, 0, 0, 20, 9)
    earth = add(339, 0, 0, 20, 9)
    house_left = add(320, 0, 0, 57, 49)
    house_right = add(321, 0, 0, 57, 49)
    village_house_parts = add(319, 0, 0, 133, 120)
    tent = add(312, 0, 0, 147, 180)
    shrine = add(314, 0, 0, 90, 106)
    small_rock = add(309, 0, 0, 43, 45)
    bushes = add(137, 0, 0, 82, 43)
    trunk_top = add(19, 0, 0, 32, 25)
    trunk = add(19, 42, 27, 28, 55)
    crown_left = add(153, 0, 0, 71, 71)
    crown_right = add(154, 0, 0, 87, 73)
    crown_top = add(152, 0, 0, 83, 60)

    base = Layer(grass, -10, -9, 0)
    path = Layer(earth, -10, -9, 0)

    composites = [
        CompositeTile(4, 0, 1, 1, (base,)),
        CompositeTile(4, 0, 1, 1, (path,)),
        CompositeTile(2, 0, 1, 1, (base, Layer(house_left, -28, -49, 0))),
        CompositeTile(2, 0, 1, 1, (base, Layer(house_right, -28, -49, 0))),
        CompositeTile(2, 0, 1, 1, (base, Layer(village_house_parts, -66, -120, 0))),
        CompositeTile(2, 0, 1, 1, (base, Layer(tent, -73, -128, 0))),
        CompositeTile(2, 0, 1, 1, (base, Layer(shrine, -45, -106, 0))),
        CompositeTile(2, 0, 1, 1, (base, Layer(small_rock, -21, -45, 0))),
        CompositeTile(2, 0, 1, 1, (
            base,
            Layer(trunk_top, 3, -75, 0),
            Layer(trunk, -14, -59, 0),
            Layer(crown_left, -60, -95, 0),
            Layer(crown_right, -21, -94, 1),
            Layer(crown_top, -46, -121, 0),
        )),
        CompositeTile(2, 0, 1, 1, (base, Layer(bushes, -41, -43, 0))),
    ]
    names = [
        'grass',
        'earth_path',
        'small_house_left',
        'small_house_right',
        'village_house_parts',
        'village_tent',
        'village_shrine',
        'small_rock',
        'tree',
        'bushes',
    ]
    return records, composites, names


def build_map(width: int = 64, height: int = 64) -> MapO:
    tiles = [0] * (width * height)
    collision = [False] * (width * height)

    def place(x: int, y: int, tile: int, radius: int = 0) -> None:
        tiles[(y * width) + x] = tile
        for blocked_y in range(max(0, y - radius), min(height, y + radius + 1)):
            for blocked_x in range(max(0, x - radius), min(width, x + radius + 1)):
                collision[(blocked_y * width) + blocked_x] = True

    # Two broad paths leave a central village square.
    for position in range(5, 59):
        tiles[(32 * width) + position] = 1
        tiles[(position * width) + 32] = 1
    for y in range(27, 38):
        for x in range(27, 38):
            tiles[(y * width) + x] = 1

    # Candidate placement made only from APK resources outside 58.map.ref.
    for x, y, tile, radius in (
        (21, 21, 2, 1), (25, 17, 3, 1), (40, 20, 2, 1), (44, 24, 3, 1),
        (18, 39, 3, 1), (23, 45, 2, 1), (42, 43, 2, 1), (47, 38, 3, 1),
        (31, 22, 2, 1), (36, 42, 3, 1), (28, 47, 2, 1),
        (15, 18, 8, 1), (49, 18, 8, 1), (15, 47, 8, 1), (50, 47, 8, 1),
        (11, 28, 8, 1), (54, 29, 8, 1), (13, 35, 9, 1), (52, 35, 9, 1),
        (24, 27, 9, 1), (42, 29, 9, 1), (28, 39, 7, 0), (39, 35, 7, 0),
    ):
        place(x, y, tile, radius)

    return MapO(
        width=width,
        height=height,
        map_type=1,
        tile_definitions=list(range(10)),
        tiles=tiles,
        collision=collision,
        mirror=[False] * (width * height),
    )


def render_preview(map_data: MapO, renderer: CompositeRenderer) -> Image.Image:
    items: list[tuple[int, int, RenderedTile]] = []
    for y in range(map_data.height):
        for x in range(map_data.width):
            tile = map_data.tiles[(y * map_data.width) + x]
            if tile == -1:
                continue
            rendered = renderer.render(map_data.tile_definitions[tile])
            items.append((10 * (x - y), 5 * (x + y + 2), rendered))
    minimum_x = min(x + tile.offset_x for x, y, tile in items)
    minimum_y = min(y + tile.offset_y for x, y, tile in items)
    maximum_x = max(x + tile.offset_x + tile.image.width for x, y, tile in items)
    maximum_y = max(y + tile.offset_y + tile.image.height for x, y, tile in items)
    margin = 12
    canvas = Image.new(
        'RGBA',
        (maximum_x - minimum_x + margin * 2, maximum_y - minimum_y + margin * 2),
        (32, 36, 40, 255),
    )
    for anchor_x, anchor_y, tile in sorted(items, key=lambda item: (item[1], item[0])):
        canvas.alpha_composite(
            tile.image,
            (anchor_x + tile.offset_x - minimum_x + margin, anchor_y + tile.offset_y - minimum_y + margin),
        )
    return canvas


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description='Build an editable map-50000 village candidate from APK assets')
    parser.add_argument('--apk', type=Path, required=True)
    parser.add_argument('-o', '--output', type=Path, required=True)
    args = parser.parse_args()

    args.output.mkdir(parents=True, exist_ok=True)
    records, composites, names = build_reference()
    map_data = build_map()
    ref_path = args.output / f'{MAP_ID}.candidate.map.ref'
    map_o_path = args.output / f'{MAP_ID}.candidate.map.o'
    spec_path = args.output / f'{MAP_ID}.candidate.map.json'
    preview_path = args.output / f'{MAP_ID}.candidate.preview.png'

    ref_path.write_bytes(encode_map_ref(records, composites))
    map_o_path.write_bytes(map_data.to_file())
    spec = map_data.to_spec()
    spec.update({
        'map_id': MAP_ID,
        'map_name': '仙石村',
        'status': 'resource-group candidate; original server layout is unavailable',
        'composite_names': names,
        'source_image_ids': sorted({record.image_id for record in records}),
    })
    spec_path.write_text(json.dumps(spec, ensure_ascii=False, indent=2), encoding='utf-8')

    assets = AssetReader(args.apk)
    try:
        preview = render_preview(map_data, CompositeRenderer(records, composites, assets))
        preview.save(preview_path)
    finally:
        assets.close()

    print(f'wrote candidate map.ref: {ref_path} ({ref_path.stat().st_size} bytes)')
    print(f'wrote candidate map.o: {map_o_path} ({map_o_path.stat().st_size} bytes)')
    print(f'wrote candidate specification: {spec_path}')
    print(f'wrote candidate preview: {preview_path} ({preview.width}x{preview.height})')


if __name__ == '__main__':
    main()
