from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw


@dataclass
class SpriteRecord:
    image_index: int
    x: int
    y: int
    width: int
    height: int


@dataclass
class Piece:
    record_index: int
    transform: int
    x: int
    y: int


@dataclass
class RoleResource:
    image_ids: list[int]
    records: list[SpriteRecord]
    sequences: list[list[Piece]]
    animations: list[list[int]]


def u16(data: bytes, offset: int) -> int:
    return int.from_bytes(data[offset : offset + 2], 'big')


def u32(data: bytes, offset: int) -> int:
    return int.from_bytes(data[offset : offset + 4], 'big')


def signed(value: int) -> int:
    return value if value < 128 else value - 256


def parse_role(path: Path) -> RoleResource:
    data = path.read_bytes()
    image_count = data[2] & 0x3F
    sequence_count = (data[3] << 2) | (data[2] >> 6)
    animation_count = data[4]
    offset = 8

    image_ids = [u32(data, offset + index * 4) for index in range(image_count)]
    offset += image_count * 4

    records: list[SpriteRecord] = []
    for _ in range(sequence_count):
        records.append(SpriteRecord(*data[offset : offset + 5]))
        offset += 5

    sequences: list[list[Piece]] = []
    for _ in range(data[4]):
        count = data[offset]
        offset += 1
        pieces: list[Piece] = []
        for _ in range(count):
            first, second, x, y = data[offset : offset + 4]
            offset += 4
            pieces.append(Piece((second << 5) | (first >> 3), first & 7, signed(x), signed(y)))
        sequences.append(pieces)

    animations: list[list[int]] = []
    for _ in range(data[5]):
        count = data[offset]
        offset += 1
        offset += 4  # optional lookup key, present even when lookup is disabled
        # The client stores the first byte of each two-byte animation entry as
        # the sequence index; the second byte is timing metadata.
        frames = [data[offset + index * 2] for index in range(count)]
        offset += count * 2
        animations.append(frames)

    if offset != len(data):
        raise ValueError(f'{path.name}: parsed {offset} of {len(data)} bytes')
    return RoleResource(image_ids, records, sequences, animations)


TRANSFORMS = {
    0: None,
    1: Image.Transpose.ROTATE_180,
    2: Image.Transpose.FLIP_LEFT_RIGHT,
    3: Image.Transpose.FLIP_TOP_BOTTOM,
    4: Image.Transpose.TRANSPOSE,
    5: Image.Transpose.ROTATE_90,
    6: Image.Transpose.ROTATE_270,
    7: Image.Transpose.TRANSVERSE,
}


def image_index(image_dir: Path) -> dict[int, Path]:
    found: dict[int, Path] = {}
    for path in image_dir.glob('*.png'):
        try:
            found[int(path.stem.split('_', 1)[0])] = path
        except ValueError:
            continue
    return found


def render_sequence(resource: RoleResource, sequence_index: int, images: dict[int, Path]) -> Image.Image:
    rendered: list[tuple[Image.Image, int, int]] = []
    for piece in resource.sequences[sequence_index]:
        if not 0 <= piece.record_index < len(resource.records):
            continue
        record = resource.records[piece.record_index]
        if not 0 <= record.image_index < len(resource.image_ids):
            continue
        source_path = images.get(resource.image_ids[record.image_index])
        if source_path is None:
            continue
        with Image.open(source_path) as source:
            crop = source.convert('RGBA').crop(
                (record.x, record.y, record.x + record.width, record.y + record.height)
            )
        operation = TRANSFORMS[piece.transform]
        if operation is not None:
            crop = crop.transpose(operation)
        rendered.append((crop, piece.x, piece.y))

    if not rendered:
        return Image.new('RGBA', (1, 1))
    left = min(x for _, x, _ in rendered)
    top = min(y for _, _, y in rendered)
    right = max(x + part.width for part, x, _ in rendered)
    bottom = max(y + part.height for part, _, y in rendered)
    canvas = Image.new('RGBA', (max(1, right - left), max(1, bottom - top)))
    for part, x, y in rendered:
        canvas.alpha_composite(part, (x - left, y - top))
    return canvas


def representative_sequences(resource: RoleResource, limit: int = 8) -> list[int]:
    candidates: list[int] = []
    for animation in resource.animations:
        if animation and animation[0] not in candidates:
            candidates.append(animation[0])
    if not candidates:
        candidates = list(range(len(resource.sequences)))
    return candidates[:limit]


def make_sheet(role_dir: Path, image_dir: Path, output: Path, role_ids: list[int]) -> dict[str, object]:
    images = image_index(image_dir)
    cells: list[tuple[int, list[Image.Image], RoleResource]] = []
    summary: dict[str, object] = {}
    for role_id in role_ids:
        path = role_dir / f'{role_id}.dat'
        if not path.exists():
            summary[str(role_id)] = {'missing': True}
            continue
        resource = parse_role(path)
        frames = [render_sequence(resource, index, images) for index in representative_sequences(resource)]
        cells.append((role_id, frames, resource))
        summary[str(role_id)] = {
            'image_ids': resource.image_ids,
            'records': len(resource.records),
            'sequences': len(resource.sequences),
            'animations': len(resource.animations),
            'preview_sequences': representative_sequences(resource),
        }

    cell_width, cell_height = 170, 170
    columns = 4
    rows = max(1, (len(cells) + columns - 1) // columns)
    sheet = Image.new('RGBA', (columns * cell_width, rows * cell_height), 'white')
    draw = ImageDraw.Draw(sheet)
    for cell_index, (role_id, frames, _) in enumerate(cells):
        origin_x = (cell_index % columns) * cell_width
        origin_y = (cell_index // columns) * cell_height
        draw.text((origin_x + 4, origin_y + 4), str(role_id), fill='black')
        for frame_index, frame in enumerate(frames[:8]):
            thumb = frame.copy()
            thumb.thumbnail((76, 62), Image.Resampling.NEAREST)
            x = origin_x + 4 + (frame_index % 2) * 82 + (76 - thumb.width) // 2
            y = origin_y + 24 + (frame_index // 2) * 34
            sheet.alpha_composite(thumb, (x, y))
        draw.rectangle((origin_x, origin_y, origin_x + cell_width - 1, origin_y + cell_height - 1), outline='#999')

    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.convert('RGB').save(output)
    output.with_suffix('.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--role-dir', type=Path, required=True)
    parser.add_argument('--image-dir', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('role_ids', nargs='+', type=int)
    args = parser.parse_args()
    make_sheet(args.role_dir, args.image_dir, args.output, args.role_ids)


if __name__ == '__main__':
    main()
