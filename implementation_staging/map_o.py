from __future__ import annotations

import json
import struct
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any


class MapOError(ValueError):
    pass


@dataclass(frozen=True)
class MapRefInfo:
    composite_tile_count: int
    image_record_count: int
    image_ids: tuple[int, ...]
    consumed_bytes: int
    total_bytes: int


def inspect_map_ref(data: bytes) -> MapRefInfo:
    """Parse the record boundaries used by pmsj.work.b.m.C()."""
    if len(data) < 4:
        raise MapOError('map.ref is shorter than its four-byte header')
    composite_count, image_count = struct.unpack_from('>HH', data, 0)
    offset = 4
    image_ids: list[int] = []
    for index in range(image_count):
        if offset + 8 > len(data):
            raise MapOError(f'map.ref image record {index} is truncated')
        image_ids.append(struct.unpack_from('>I', data, offset)[0])
        offset += 8

    for index in range(composite_count):
        if offset + 5 > len(data):
            raise MapOError(f'map.ref composite tile {index} is truncated')
        flags = data[offset]
        child_count = data[offset + 4]
        offset += 5
        child_size = 2 if flags & 1 else 5
        required = child_count * child_size
        if offset + required > len(data):
            raise MapOError(f'map.ref composite tile {index} children are truncated')
        offset += required

    return MapRefInfo(
        composite_tile_count=composite_count,
        image_record_count=image_count,
        image_ids=tuple(image_ids),
        consumed_bytes=offset,
        total_bytes=len(data),
    )


def read_map_ref(path: Path | None = None, apk: Path | None = None, map_id: int = 58) -> tuple[bytes, str]:
    if (path is None) == (apk is None):
        raise MapOError('provide exactly one of map.ref path or APK path')
    if path is not None:
        return path.read_bytes(), str(path)
    assert apk is not None
    member = f'assets/res/map/{map_id}.map.ref'
    with zipfile.ZipFile(apk) as archive:
        try:
            return archive.read(member), f'{apk}!/{member}'
        except KeyError as exc:
            raise MapOError(f'APK does not contain {member}') from exc


def pack_bits(values: list[bool]) -> bytes:
    packed = bytearray((len(values) + 7) // 8)
    for index, value in enumerate(values):
        if value:
            packed[index // 8] |= 1 << (index % 8)
    return bytes(packed)


def unpack_bits(data: bytes, count: int) -> list[bool]:
    return [bool(data[index // 8] & (1 << (index % 8))) for index in range(count)]


def encode_tile_rle(values: list[int], sentinel: int = 255) -> bytes:
    """Encode the byte RLE consumed by m.a(byte[], int) for 1407 actions 3/4."""
    if not 0 <= sentinel <= 255:
        raise MapOError('RLE sentinel must fit an unsigned byte')
    raw = [value & 0xFF for value in values]
    encoded = bytearray([sentinel])
    index = 0
    while index < len(raw):
        value = raw[index]
        run = 1
        while index + run < len(raw) and raw[index + run] == value:
            run += 1
        remaining = run
        while remaining:
            chunk = min(remaining, 255)
            if value != sentinel and chunk <= 2:
                encoded.extend([value] * chunk)
            else:
                encoded.extend((sentinel, 0 if chunk == 255 else chunk, value))
            remaining -= chunk
        index += run
    return bytes(encoded)


def decode_tile_rle(data: bytes, expected_count: int) -> list[int]:
    if not data:
        raise MapOError('RLE data is empty')
    sentinel = data[0]
    decoded: list[int] = []
    index = 1
    while index < len(data):
        value = data[index]
        index += 1
        if value != sentinel:
            decoded.append(value)
            continue
        if index >= len(data):
            raise MapOError('RLE marker is missing its count')
        count = data[index]
        index += 1
        if count == sentinel:
            decoded.append(sentinel)
            continue
        if index >= len(data):
            raise MapOError('RLE run is missing its value')
        value = data[index]
        index += 1
        decoded.extend([value] * (255 if count == 0 else count))
        if len(decoded) > expected_count:
            raise MapOError('RLE expands beyond the configured map size')
    if len(decoded) != expected_count:
        raise MapOError(f'RLE expands to {len(decoded)} cells, expected {expected_count}')
    return decoded


def _parse_tile_grid(value: Any, width: int, height: int, default_tile: int) -> list[int]:
    if value is None:
        return [default_tile] * (width * height)
    if not isinstance(value, list) or len(value) != height:
        raise MapOError(f'tiles must contain exactly {height} rows')
    cells: list[int] = []
    for row_index, row in enumerate(value):
        if not isinstance(row, list) or len(row) != width:
            raise MapOError(f'tiles row {row_index} must contain exactly {width} cells')
        for cell in row:
            cells.append(-1 if cell is None else int(cell))
    return cells


def _parse_bool_grid(value: Any, width: int, height: int, name: str) -> list[bool]:
    if value is None:
        return [False] * (width * height)
    if not isinstance(value, list) or len(value) != height:
        raise MapOError(f'{name} must contain exactly {height} strings')
    result: list[bool] = []
    for row_index, row in enumerate(value):
        if not isinstance(row, str) or len(row) != width:
            raise MapOError(f'{name} row {row_index} must be a {width}-character string')
        invalid = set(row) - {'.', '#'}
        if invalid:
            raise MapOError(f'{name} row {row_index} contains invalid markers: {sorted(invalid)!r}')
        result.extend(character == '#' for character in row)
    return result


def _bool_rows(values: list[bool], width: int, height: int) -> list[str]:
    return [
        ''.join('#' if value else '.' for value in values[row * width:(row + 1) * width])
        for row in range(height)
    ]


@dataclass
class MapO:
    width: int
    height: int
    map_type: int
    tile_definitions: list[int]
    tiles: list[int]
    collision: list[bool]
    mirror: list[bool]
    tile_pixel_width: int = 20
    tile_pixel_height: int = 10

    def validate(self, ref: MapRefInfo | None = None) -> None:
        if not 1 <= self.width <= 127 or not 1 <= self.height <= 127:
            raise MapOError('the original client stores width and height as signed bytes (1..127)')
        if not 0 <= self.map_type <= 255:
            raise MapOError('map_type must be between 0 and 255')
        if not 1 <= self.tile_pixel_width <= 255 or not 1 <= self.tile_pixel_height <= 255:
            raise MapOError('tile pixel dimensions must be between 1 and 255')
        if not 1 <= len(self.tile_definitions) <= 128:
            raise MapOError('tile_definitions must contain 1..128 entries')
        if any(not -32768 <= value <= 32767 for value in self.tile_definitions):
            raise MapOError('tile definition references must fit signed 16-bit values')
        if ref is not None:
            invalid = [value for value in self.tile_definitions if not 0 <= value < ref.composite_tile_count]
            if invalid:
                raise MapOError(
                    f'tile definition references outside map.ref composite range '
                    f'0..{ref.composite_tile_count - 1}: {invalid}'
                )
        cell_count = self.width * self.height
        for name, values in (('tiles', self.tiles), ('collision', self.collision), ('mirror', self.mirror)):
            if len(values) != cell_count:
                raise MapOError(f'{name} has {len(values)} cells, expected {cell_count}')
        for value in self.tiles:
            if value != -1 and not 0 <= value < len(self.tile_definitions):
                raise MapOError(
                    f'tile grid value {value} is not -1 and is outside definition range '
                    f'0..{len(self.tile_definitions) - 1}'
                )

    @classmethod
    def from_spec(cls, spec: dict[str, Any]) -> 'MapO':
        width = int(spec['width'])
        height = int(spec['height'])
        definitions = [int(value) for value in spec.get('tile_definitions', [0])]
        default_tile = int(spec.get('default_tile', 0))
        result = cls(
            width=width,
            height=height,
            map_type=int(spec.get('map_type', 0)),
            tile_definitions=definitions,
            tiles=_parse_tile_grid(spec.get('tiles'), width, height, default_tile),
            collision=_parse_bool_grid(spec.get('collision'), width, height, 'collision'),
            mirror=_parse_bool_grid(spec.get('mirror'), width, height, 'mirror'),
            tile_pixel_width=int(spec.get('tile_pixel_width', 20)),
            tile_pixel_height=int(spec.get('tile_pixel_height', 10)),
        )
        result.validate()
        return result

    @classmethod
    def from_file(cls, data: bytes) -> 'MapO':
        if not data:
            raise MapOError('.map.o file is empty')
        definition_count = data[0]
        if definition_count == 0:
            raise MapOError('.map.o definition count is zero')
        definition_end = 1 + (definition_count * 2)
        if len(data) < definition_end + 5:
            raise MapOError('.map.o header is truncated')
        definitions = list(struct.unpack_from(f'>{definition_count}h', data, 1))
        map_type, width, height, tile_pixel_width, tile_pixel_height = data[definition_end:definition_end + 5]
        cell_count = width * height
        mask_size = (cell_count + 7) // 8
        expected_size = definition_end + 5 + cell_count + (mask_size * 2)
        if len(data) != expected_size:
            raise MapOError(
                f'.map.o has {len(data)} bytes; its embedded dimensions require {expected_size}. '
                'The five skipped bytes may follow another convention.'
            )
        offset = definition_end + 5
        raw_tiles = data[offset:offset + cell_count]
        offset += cell_count
        collision = unpack_bits(data[offset:offset + mask_size], cell_count)
        offset += mask_size
        mirror = unpack_bits(data[offset:offset + mask_size], cell_count)
        result = cls(
            width=width,
            height=height,
            map_type=map_type,
            tile_definitions=definitions,
            tiles=[-1 if value == 255 else value for value in raw_tiles],
            collision=collision,
            mirror=mirror,
            tile_pixel_width=tile_pixel_width,
            tile_pixel_height=tile_pixel_height,
        )
        result.validate()
        return result

    def to_file(self) -> bytes:
        self.validate()
        header = bytes((len(self.tile_definitions),))
        definitions = struct.pack(f'>{len(self.tile_definitions)}h', *self.tile_definitions)
        # The APK reader skips these five bytes because the server has already
        # supplied the first three through 1407/0. Original map 58 stores the
        # same map metadata followed by the client's 20x10 isometric tile size.
        compatibility_header = bytes((
            self.map_type,
            self.width,
            self.height,
            self.tile_pixel_width,
            self.tile_pixel_height,
        ))
        grid = bytes(value & 0xFF for value in self.tiles)
        return header + definitions + compatibility_header + grid + pack_bits(self.collision) + pack_bits(self.mirror)

    def to_spec(self) -> dict[str, Any]:
        return {
            'width': self.width,
            'height': self.height,
            'map_type': self.map_type,
            'tile_pixel_width': self.tile_pixel_width,
            'tile_pixel_height': self.tile_pixel_height,
            'tile_definitions': self.tile_definitions,
            'tiles': [
                [None if value == -1 else value for value in self.tiles[row * self.width:(row + 1) * self.width]]
                for row in range(self.height)
            ],
            'collision': _bool_rows(self.collision, self.width, self.height),
            'mirror': _bool_rows(self.mirror, self.width, self.height),
        }

    def to_1407_sections(self) -> dict[str, bytes | int]:
        self.validate()
        return {
            'map_type': self.map_type,
            'width': self.width,
            'height': self.height,
            'definitions': struct.pack(f'>{len(self.tile_definitions)}h', *self.tile_definitions),
            'tiles_rle': encode_tile_rle(self.tiles),
            'collision': pack_bits(self.collision),
            'mirror': pack_bits(self.mirror),
        }


def load_spec(path: Path) -> dict[str, Any]:
    loaded = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(loaded, dict):
        raise MapOError('map specification root must be a JSON object')
    return loaded
