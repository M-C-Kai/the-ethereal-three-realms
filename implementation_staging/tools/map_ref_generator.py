from __future__ import annotations

import argparse
import json
import struct
import zipfile
from dataclasses import dataclass, asdict
from pathlib import Path


class MapRefError(ValueError):
    pass


@dataclass(frozen=True)
class ImageRecord:
    image_id: int
    crop_x: int
    crop_y: int
    width: int
    height: int


@dataclass(frozen=True)
class Layer:
    reference: int
    x: int = 0
    y: int = 0
    transform: int = 0


@dataclass(frozen=True)
class CompositeTile:
    flags: int
    terrain: int
    value_b: int
    value_c: int
    layers: tuple[Layer, ...]

    @property
    def is_variant(self) -> bool:
        return bool(self.flags & 1)


def _signed_byte(value: int) -> int:
    return value if value < 128 else value - 256


def _check_u8(name: str, value: int) -> None:
    if not 0 <= value <= 0xFF:
        raise MapRefError(f'{name} must be within 0..255, got {value}')


def _check_i8(name: str, value: int) -> None:
    if not -128 <= value <= 127:
        raise MapRefError(f'{name} must be within -128..127, got {value}')


def _check_i16(name: str, value: int) -> None:
    if not -32768 <= value <= 32767:
        raise MapRefError(f'{name} must be within -32768..32767, got {value}')


def parse_map_ref(data: bytes) -> tuple[list[ImageRecord], list[CompositeTile]]:
    if len(data) < 4:
        raise MapRefError('map.ref is truncated')
    composite_count, image_count = struct.unpack_from('>HH', data, 0)
    offset = 4

    records: list[ImageRecord] = []
    for index in range(image_count):
        if offset + 8 > len(data):
            raise MapRefError(f'image record {index} is truncated')
        image_id = struct.unpack_from('>I', data, offset)[0]
        crop_x, crop_y, width, height = data[offset + 4:offset + 8]
        records.append(ImageRecord(image_id, crop_x, crop_y, width, height))
        offset += 8

    composites: list[CompositeTile] = []
    for index in range(composite_count):
        if offset + 5 > len(data):
            raise MapRefError(f'composite tile {index} is truncated')
        flags, terrain, value_b, value_c, layer_count = data[offset:offset + 5]
        offset += 5
        layers: list[Layer] = []
        for layer_index in range(layer_count):
            if offset + 2 > len(data):
                raise MapRefError(f'composite tile {index} layer {layer_index} is truncated')
            reference = struct.unpack_from('>h', data, offset)[0]
            offset += 2
            if flags & 1:
                x = y = transform = 0
            else:
                if offset + 3 > len(data):
                    raise MapRefError(f'composite tile {index} layer {layer_index} data is truncated')
                x = _signed_byte(data[offset])
                y = _signed_byte(data[offset + 1])
                transform = data[offset + 2]
                offset += 3
            layers.append(Layer(reference, x, y, transform))
        composites.append(CompositeTile(flags, terrain, value_b, value_c, tuple(layers)))

    if offset != len(data):
        raise MapRefError(f'map.ref parser consumed {offset} of {len(data)} bytes')
    return records, composites


def serialize_map_ref(records: list[ImageRecord], composites: list[CompositeTile]) -> bytes:
    if len(records) > 0xFFFF or len(composites) > 0xFFFF:
        raise MapRefError('map.ref counts must fit in unsigned short')

    out = bytearray(struct.pack('>HH', len(composites), len(records)))

    for index, record in enumerate(records):
        if not 0 <= record.image_id <= 0xFFFFFFFF:
            raise MapRefError(f'image record {index} image_id out of uint32 range: {record.image_id}')
        for name, value in (
            ('crop_x', record.crop_x), ('crop_y', record.crop_y),
            ('width', record.width), ('height', record.height),
        ):
            _check_u8(f'image record {index} {name}', value)
        out.extend(struct.pack('>I4B', record.image_id, record.crop_x, record.crop_y, record.width, record.height))

    for tile_index, tile in enumerate(composites):
        for name, value in (
            ('flags', tile.flags), ('terrain', tile.terrain),
            ('value_b', tile.value_b), ('value_c', tile.value_c),
        ):
            _check_u8(f'composite {tile_index} {name}', value)
        if len(tile.layers) > 0xFF:
            raise MapRefError(f'composite {tile_index} has more than 255 layers')
        out.extend(bytes((tile.flags, tile.terrain, tile.value_b, tile.value_c, len(tile.layers))))
        for layer_index, layer in enumerate(tile.layers):
            _check_i16(f'composite {tile_index} layer {layer_index} reference', layer.reference)
            out.extend(struct.pack('>h', layer.reference))
            if not tile.is_variant:
                _check_i8(f'composite {tile_index} layer {layer_index} x', layer.x)
                _check_i8(f'composite {tile_index} layer {layer_index} y', layer.y)
                _check_u8(f'composite {tile_index} layer {layer_index} transform', layer.transform)
                out.extend(bytes((layer.x & 0xFF, layer.y & 0xFF, layer.transform)))
    return bytes(out)


def to_spec(records: list[ImageRecord], composites: list[CompositeTile]) -> dict:
    return {
        'format': 'piaomiao-map-ref-v1',
        'image_records': [asdict(r) for r in records],
        'composite_tiles': [
            {
                'flags': t.flags,
                'terrain': t.terrain,
                'value_b': t.value_b,
                'value_c': t.value_c,
                'layers': [asdict(layer) for layer in t.layers],
            }
            for t in composites
        ],
    }


def from_spec(spec: dict) -> tuple[list[ImageRecord], list[CompositeTile]]:
    records = [ImageRecord(**item) for item in spec.get('image_records', [])]
    composites = []
    for item in spec.get('composite_tiles', []):
        layers = tuple(Layer(**layer) for layer in item.get('layers', []))
        composites.append(CompositeTile(
            flags=item['flags'], terrain=item['terrain'], value_b=item['value_b'],
            value_c=item['value_c'], layers=layers,
        ))
    return records, composites


def read_map_ref(path: Path | None, apk: Path | None, map_id: int) -> bytes:
    if path is not None:
        return path.read_bytes()
    if apk is None:
        raise MapRefError('either --input or --apk is required')
    with zipfile.ZipFile(apk) as zf:
        return zf.read(f'assets/res/map/{map_id}.map.ref')


def cmd_dump(args: argparse.Namespace) -> None:
    data = read_map_ref(args.input, args.apk, args.map_id)
    records, composites = parse_map_ref(data)
    args.output.write_text(json.dumps(to_spec(records, composites), ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'wrote {args.output}: {len(records)} image records, {len(composites)} composite tiles')


def cmd_build(args: argparse.Namespace) -> None:
    spec = json.loads(args.spec.read_text(encoding='utf-8'))
    records, composites = from_spec(spec)
    data = serialize_map_ref(records, composites)
    parsed_records, parsed_composites = parse_map_ref(data)
    if parsed_records != records or parsed_composites != composites:
        raise MapRefError('generated map.ref failed round-trip validation')
    args.output.write_bytes(data)
    print(f'wrote {args.output}: {len(data)} bytes, {len(records)} image records, {len(composites)} composite tiles')


def cmd_roundtrip(args: argparse.Namespace) -> None:
    original = read_map_ref(args.input, args.apk, args.map_id)
    records, composites = parse_map_ref(original)
    rebuilt = serialize_map_ref(records, composites)
    if rebuilt != original:
        for i, (a, b) in enumerate(zip(original, rebuilt)):
            if a != b:
                raise MapRefError(f'round-trip mismatch at byte {i}: original={a:#04x} rebuilt={b:#04x}')
        raise MapRefError(f'round-trip length mismatch: original={len(original)} rebuilt={len(rebuilt)}')
    print(f'round-trip OK: {len(original)} bytes, {len(records)} image records, {len(composites)} composite tiles')


def main() -> None:
    parser = argparse.ArgumentParser(description='Dump, build and verify Piao Miao San Jie .map.ref files')
    sub = parser.add_subparsers(dest='command', required=True)

    def add_source(p):
        group = p.add_mutually_exclusive_group(required=True)
        group.add_argument('--input', type=Path)
        group.add_argument('--apk', type=Path)
        p.add_argument('--map-id', type=int, default=58)

    dump = sub.add_parser('dump', help='Convert binary .map.ref to editable JSON')
    add_source(dump)
    dump.add_argument('-o', '--output', type=Path, required=True)
    dump.set_defaults(func=cmd_dump)

    build = sub.add_parser('build', help='Build binary .map.ref from JSON')
    build.add_argument('spec', type=Path)
    build.add_argument('-o', '--output', type=Path, required=True)
    build.set_defaults(func=cmd_build)

    rt = sub.add_parser('roundtrip', help='Parse and rebuild a .map.ref, requiring byte-identical output')
    add_source(rt)
    rt.set_defaults(func=cmd_roundtrip)

    args = parser.parse_args()
    try:
        args.func(args)
    except (MapRefError, OSError, ValueError, KeyError, zipfile.BadZipFile) as exc:
        parser.error(str(exc))


if __name__ == '__main__':
    main()
