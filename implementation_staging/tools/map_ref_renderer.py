from __future__ import annotations

import argparse
import io
import json
import struct
import sys
import zipfile
import zlib
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from map_o import MapO, MapOError, load_spec


PNG_SIGNATURE = b'\x89PNG\r\n\x1a\n'
PNG_IEND = b'\x00\x00\x00\x00IEND\xaeB\x60\x82'


def unsigned_short(data: bytes, offset: int) -> int:
    return struct.unpack_from('>H', data, offset)[0]


def signed_byte(value: int) -> int:
    return value if value < 128 else value - 256


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
    x: int
    y: int
    transform: int


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


@dataclass(frozen=True)
class RenderedTile:
    image: Image.Image
    offset_x: int
    offset_y: int


def parse_map_ref(data: bytes) -> tuple[list[ImageRecord], list[CompositeTile]]:
    if len(data) < 4:
        raise MapOError('map.ref is truncated')
    composite_count, image_count = struct.unpack_from('>HH', data, 0)
    offset = 4
    records: list[ImageRecord] = []
    for index in range(image_count):
        if offset + 8 > len(data):
            raise MapOError(f'image record {index} is truncated')
        image_id = struct.unpack_from('>I', data, offset)[0]
        crop_x, crop_y, width, height = data[offset + 4:offset + 8]
        records.append(ImageRecord(image_id, crop_x, crop_y, width, height))
        offset += 8

    composites: list[CompositeTile] = []
    for index in range(composite_count):
        if offset + 5 > len(data):
            raise MapOError(f'composite tile {index} is truncated')
        flags, terrain, value_b, value_c, layer_count = data[offset:offset + 5]
        offset += 5
        layers: list[Layer] = []
        for _ in range(layer_count):
            if offset + 2 > len(data):
                raise MapOError(f'composite tile {index} layer reference is truncated')
            reference = struct.unpack_from('>h', data, offset)[0]
            offset += 2
            if flags & 1:
                x = y = transform = 0
            else:
                if offset + 3 > len(data):
                    raise MapOError(f'composite tile {index} layer data is truncated')
                x = signed_byte(data[offset])
                y = signed_byte(data[offset + 1])
                transform = data[offset + 2]
                offset += 3
            layers.append(Layer(reference, x, y, transform))
        composites.append(CompositeTile(flags, terrain, value_b, value_c, tuple(layers)))
    if offset != len(data):
        raise MapOError(f'map.ref parser consumed {offset} of {len(data)} bytes')
    return records, composites


def rebuild_png(blob: bytes, offset: int) -> bytes:
    position = offset
    group_count, group_index = blob[position], blob[position + 1]
    position += 2
    if group_count:
        position += (group_count - group_index - 1) * 2
    header = blob[position:position + 22]
    if len(header) != 22:
        raise MapOError('packed image header is truncated')
    position += 22
    width, height = unsigned_short(header, 0), unsigned_short(header, 2)
    bit_depth, transparent_index = header[4], header[5]
    palette_crc, _transparency_crc, image_header_crc = struct.unpack_from('>III', header, 6)
    palette_length, idat_total_length = struct.unpack_from('>HH', header, 18)
    if group_count:
        position += group_index * palette_length
        palette565 = blob[position:position + palette_length]
        position += palette_length
        position += (group_count - group_index - 1) * palette_length
    else:
        palette565 = blob[position:position + palette_length]
        position += palette_length
    idat_and_crc = blob[position:position + idat_total_length]
    if len(palette565) != palette_length or len(idat_and_crc) != idat_total_length:
        raise MapOError('packed image palette or IDAT is truncated')

    palette = bytearray()
    for index in range(0, palette_length, 2):
        rgb565 = unsigned_short(palette565, index)
        # Match the original packer's signed-short red conversion exactly;
        # the stored PLTE CRC was calculated from these reconstructed bytes.
        signed565 = rgb565 if rgb565 < 0x8000 else rgb565 - 0x10000
        palette.extend((
            int(((signed565 >> 11) * 255) / 31) & 0xFF,
            ((rgb565 >> 5) & 63) * 255 // 63,
            (rgb565 & 31) * 255 // 31,
        ))
    chunks = [
        PNG_SIGNATURE,
        struct.pack('>I4sIIBBBBBI', 13, b'IHDR', width, height, bit_depth, 3, 0, 0, 0, image_header_crc),
        struct.pack('>I4s', len(palette), b'PLTE') + palette + struct.pack('>I', palette_crc),
    ]
    if transparent_index != 255:
        alpha = bytearray(b'\xff' * (palette_length // 2))
        if transparent_index < len(alpha):
            alpha[transparent_index] = 0
        transparency_crc = zlib.crc32(b'tRNS' + alpha) & 0xFFFFFFFF
        chunks.append(struct.pack('>I4s', len(alpha), b'tRNS') + alpha + struct.pack('>I', transparency_crc))
    chunks.append(struct.pack('>I4s', idat_total_length - 4, b'IDAT') + idat_and_crc)
    chunks.append(PNG_IEND)
    return b''.join(chunks)


class AssetReader:
    def __init__(self, apk: Path):
        self.archive = zipfile.ZipFile(apk)
        index = self.archive.read('assets/res/images/images.o')
        records_length = unsigned_short(index, 0)
        records = index[2:2 + records_length]
        self.locations: dict[int, tuple[int, int]] = {}
        for offset in range(0, len(records), 7):
            record = records[offset:offset + 7]
            if len(record) == 7:
                self.locations[struct.unpack_from('>I', record, 0)[0]] = (record[4], unsigned_short(record, 5))

    def close(self) -> None:
        self.archive.close()

    @lru_cache(maxsize=None)
    def image(self, image_id: int) -> Image.Image:
        try:
            container, offset = self.locations[image_id]
        except KeyError as exc:
            raise MapOError(f'images.o has no image id {image_id}') from exc
        blob = self.archive.read(f'assets/res/images/png{container}.p')
        return Image.open(io.BytesIO(rebuild_png(blob, offset))).convert('RGBA')


def transform_image(image: Image.Image, transform: int) -> Image.Image:
    transform &= 3
    if transform == 1:
        return image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    if transform == 2:
        return image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    if transform == 3:
        return image.transpose(Image.Transpose.ROTATE_180)
    return image


class CompositeRenderer:
    def __init__(self, records: list[ImageRecord], composites: list[CompositeTile], assets: AssetReader):
        self.records = records
        self.composites = composites
        self.assets = assets

    @lru_cache(maxsize=None)
    def render(self, index: int, mirrored: bool = False) -> RenderedTile:
        return self._render(index, mirrored, ())

    def _render(self, index: int, mirrored: bool, stack: tuple[int, ...]) -> RenderedTile:
        if not 0 <= index < len(self.composites):
            raise MapOError(f'composite reference {index} is outside 0..{len(self.composites) - 1}')
        if index in stack:
            raise MapOError(f'cyclic composite reference: {stack + (index,)}')
        composite = self.composites[index]
        if composite.is_variant:
            if not composite.layers:
                return RenderedTile(Image.new('RGBA', (1, 1)), 0, 0)
            return self._render(composite.layers[0].reference, mirrored, stack + (index,))

        prepared: list[tuple[Image.Image, int, int]] = []
        for layer in composite.layers:
            if not 0 <= layer.reference < len(self.records):
                continue
            record = self.records[layer.reference]
            sheet = self.assets.image(record.image_id)
            patch = sheet.crop((record.crop_x, record.crop_y, record.crop_x + record.width, record.crop_y + record.height))
            x = layer.x
            transform = layer.transform
            if mirrored:
                x = -x - record.width
                transform ^= 1
            patch = transform_image(patch, transform)
            prepared.append((patch, x, layer.y))
        if not prepared:
            return RenderedTile(Image.new('RGBA', (1, 1)), 0, 0)
        minimum_x = min(x for image, x, y in prepared)
        minimum_y = min(y for image, x, y in prepared)
        maximum_x = max(x + image.width for image, x, y in prepared)
        maximum_y = max(y + image.height for image, x, y in prepared)
        canvas = Image.new('RGBA', (max(1, maximum_x - minimum_x), max(1, maximum_y - minimum_y)))
        for patch, x, y in prepared:
            canvas.alpha_composite(patch, (x - minimum_x, y - minimum_y))
        return RenderedTile(canvas, minimum_x, minimum_y)


def load_renderer(apk: Path, map_id: int) -> tuple[CompositeRenderer, AssetReader]:
    assets = AssetReader(apk)
    ref_data = assets.archive.read(f'assets/res/map/{map_id}.map.ref')
    records, composites = parse_map_ref(ref_data)
    return CompositeRenderer(records, composites, assets), assets


def atlas_command(args: argparse.Namespace) -> None:
    renderer, assets = load_renderer(args.apk, args.map_id)
    try:
        output = args.output
        output.parent.mkdir(parents=True, exist_ok=True)
        columns = args.columns
        rows = (len(renderer.composites) + columns - 1) // columns
        cell_width, cell_height = args.cell_width, args.cell_height
        atlas = Image.new('RGBA', (columns * cell_width, rows * cell_height), (30, 32, 36, 255))
        draw = ImageDraw.Draw(atlas)
        font = ImageFont.load_default()
        metadata = []
        for index, composite in enumerate(renderer.composites):
            rendered = renderer.render(index)
            preview = rendered.image.copy()
            preview.thumbnail((cell_width - 8, cell_height - 24), Image.Resampling.NEAREST)
            left = (index % columns) * cell_width
            top = (index // columns) * cell_height
            x = left + ((cell_width - preview.width) // 2)
            y = top + 18 + ((cell_height - 22 - preview.height) // 2)
            atlas.alpha_composite(preview, (x, y))
            draw.rectangle((left, top, left + cell_width - 1, top + cell_height - 1), outline=(80, 84, 92, 255))
            draw.text((left + 4, top + 3), f'{index:03d} t={composite.terrain} l={len(composite.layers)}', fill='white', font=font)
            metadata.append({
                'index': index,
                'flags': composite.flags,
                'terrain': composite.terrain,
                'layers': len(composite.layers),
                'width': rendered.image.width,
                'height': rendered.image.height,
                'offset_x': rendered.offset_x,
                'offset_y': rendered.offset_y,
            })
        atlas.save(output)
        output.with_suffix('.json').write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding='utf-8')
        print(f'wrote atlas: {output} ({atlas.width}x{atlas.height})')
    finally:
        assets.close()


def image_atlas_command(args: argparse.Namespace) -> None:
    assets = AssetReader(args.apk)
    try:
        image_ids = sorted(assets.locations)
        page_size = args.columns * args.rows
        output = args.output
        output.parent.mkdir(parents=True, exist_ok=True)
        metadata = []
        page_count = (len(image_ids) + page_size - 1) // page_size
        for page_index in range(page_count):
            page_ids = image_ids[page_index * page_size:(page_index + 1) * page_size]
            atlas = Image.new(
                'RGBA',
                (args.columns * args.cell_width, args.rows * args.cell_height),
                (30, 32, 36, 255),
            )
            draw = ImageDraw.Draw(atlas)
            font = ImageFont.load_default()
            for cell_index, image_id in enumerate(page_ids):
                left = (cell_index % args.columns) * args.cell_width
                top = (cell_index // args.columns) * args.cell_height
                container, offset = assets.locations[image_id]
                try:
                    source = assets.image(image_id)
                    preview = source.copy()
                    preview.thumbnail((args.cell_width - 8, args.cell_height - 24), Image.Resampling.NEAREST)
                    x = left + ((args.cell_width - preview.width) // 2)
                    y = top + 18 + ((args.cell_height - 22 - preview.height) // 2)
                    atlas.alpha_composite(preview, (x, y))
                    error = None
                    width, height = source.size
                except Exception as exc:  # Keep the atlas useful when one packed image is malformed.
                    error = str(exc)
                    width = height = 0
                    draw.text((left + 4, top + 24), 'decode error', fill=(255, 100, 100, 255), font=font)
                draw.rectangle(
                    (left, top, left + args.cell_width - 1, top + args.cell_height - 1),
                    outline=(80, 84, 92, 255),
                )
                draw.text(
                    (left + 4, top + 3),
                    f'id={image_id} p={container} @{offset}',
                    fill='white',
                    font=font,
                )
                metadata.append({
                    'image_id': image_id,
                    'container': container,
                    'offset': offset,
                    'width': width,
                    'height': height,
                    'page': page_index + 1,
                    'error': error,
                })
            page_path = output.with_name(f'{output.stem}.page-{page_index + 1:02d}{output.suffix}')
            atlas.save(page_path)
            print(f'wrote image atlas page {page_index + 1}/{page_count}: {page_path}')
        output.with_suffix('.json').write_text(
            json.dumps(metadata, ensure_ascii=False, indent=2),
            encoding='utf-8',
        )
        print(f'wrote image metadata: {output.with_suffix(".json")} ({len(metadata)} images)')
    finally:
        assets.close()


def parse_id_ranges(value: str) -> list[int]:
    result: set[int] = set()
    for item in value.split(','):
        item = item.strip()
        if not item:
            continue
        if '-' in item:
            start_text, end_text = item.split('-', 1)
            start, end = int(start_text), int(end_text)
            if end < start:
                raise ValueError(f'invalid descending image range {item!r}')
            result.update(range(start, end + 1))
        else:
            result.add(int(item))
    return sorted(result)


def extract_images_command(args: argparse.Namespace) -> None:
    assets = AssetReader(args.apk)
    try:
        image_ids = parse_id_ranges(args.ids)
        args.output.mkdir(parents=True, exist_ok=True)
        metadata = []
        for image_id in image_ids:
            if image_id not in assets.locations:
                print(f'skipped missing image id: {image_id}')
                continue
            source = assets.image(image_id)
            path = args.output / f'image-{image_id}.png'
            source.save(path)
            container, offset = assets.locations[image_id]
            metadata.append({
                'image_id': image_id,
                'container': container,
                'offset': offset,
                'width': source.width,
                'height': source.height,
                'file': path.name,
            })
            print(f'wrote image {image_id}: {path} ({source.width}x{source.height})')
        (args.output / 'manifest.json').write_text(
            json.dumps(metadata, ensure_ascii=False, indent=2),
            encoding='utf-8',
        )
    finally:
        assets.close()


def preview_command(args: argparse.Namespace) -> None:
    renderer, assets = load_renderer(args.apk, args.map_id)
    try:
        map_data = MapO.from_spec(load_spec(args.spec))
        items: list[tuple[int, int, RenderedTile]] = []
        for y in range(map_data.height):
            for x in range(map_data.width):
                value = map_data.tiles[(y * map_data.width) + x]
                if value == -1:
                    continue
                composite_index = map_data.tile_definitions[value]
                rendered = renderer.render(composite_index, map_data.mirror[(y * map_data.width) + x])
                anchor_x = 10 * (x - y)
                anchor_y = 5 * (x + y + 2)
                items.append((anchor_x, anchor_y, rendered))
        if not items:
            raise MapOError('map specification has no visible tiles')
        minimum_x = min(x + tile.offset_x for x, y, tile in items)
        minimum_y = min(y + tile.offset_y for x, y, tile in items)
        maximum_x = max(x + tile.offset_x + tile.image.width for x, y, tile in items)
        maximum_y = max(y + tile.offset_y + tile.image.height for x, y, tile in items)
        margin = 12
        canvas = Image.new(
            'RGBA',
            (maximum_x - minimum_x + (margin * 2), maximum_y - minimum_y + (margin * 2)),
            (32, 36, 40, 255),
        )
        for anchor_x, anchor_y, tile in sorted(items, key=lambda item: (item[1], item[0])):
            canvas.alpha_composite(
                tile.image,
                (anchor_x + tile.offset_x - minimum_x + margin, anchor_y + tile.offset_y - minimum_y + margin),
            )
        args.output.parent.mkdir(parents=True, exist_ok=True)
        canvas.save(args.output)
        print(f'wrote map preview: {args.output} ({canvas.width}x{canvas.height})')
    finally:
        assets.close()


def main() -> None:
    parser = argparse.ArgumentParser(description='Render Piao Miao San Jie 2 map.ref composite tiles')
    commands = parser.add_subparsers(dest='command', required=True)

    atlas = commands.add_parser('atlas')
    atlas.add_argument('--apk', type=Path, required=True)
    atlas.add_argument('--map-id', type=int, default=58)
    atlas.add_argument('-o', '--output', type=Path, required=True)
    atlas.add_argument('--columns', type=int, default=10)
    atlas.add_argument('--cell-width', type=int, default=170)
    atlas.add_argument('--cell-height', type=int, default=150)
    atlas.set_defaults(function=atlas_command)

    image_atlas = commands.add_parser('image-atlas')
    image_atlas.add_argument('--apk', type=Path, required=True)
    image_atlas.add_argument('-o', '--output', type=Path, required=True)
    image_atlas.add_argument('--columns', type=int, default=12)
    image_atlas.add_argument('--rows', type=int, default=10)
    image_atlas.add_argument('--cell-width', type=int, default=160)
    image_atlas.add_argument('--cell-height', type=int, default=120)
    image_atlas.set_defaults(function=image_atlas_command)

    extract_images = commands.add_parser('extract-images')
    extract_images.add_argument('--apk', type=Path, required=True)
    extract_images.add_argument('--ids', required=True, help='Comma-separated IDs and ranges, for example 301-343,50')
    extract_images.add_argument('-o', '--output', type=Path, required=True)
    extract_images.set_defaults(function=extract_images_command)

    preview = commands.add_parser('preview')
    preview.add_argument('spec', type=Path)
    preview.add_argument('--apk', type=Path, required=True)
    preview.add_argument('--map-id', type=int, default=58)
    preview.add_argument('-o', '--output', type=Path, required=True)
    preview.set_defaults(function=preview_command)

    args = parser.parse_args()
    try:
        args.function(args)
    except (MapOError, OSError, ValueError, zipfile.BadZipFile) as exc:
        parser.error(str(exc))


if __name__ == '__main__':
    main()
