"""Bake the client's horizontal sprite transform into a role ``.dat`` file."""

from __future__ import annotations

import argparse
import io
import struct
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw

from tools.map_ref_renderer import AssetReader


MIRRORED_TRANSFORM = (2, 3, 0, 1, 5, 4, 7, 6)
PIL_TRANSFORM = (
    None,
    Image.Transpose.FLIP_TOP_BOTTOM,
    Image.Transpose.FLIP_LEFT_RIGHT,
    Image.Transpose.ROTATE_180,
    Image.Transpose.TRANSPOSE,
    Image.Transpose.ROTATE_270,
    Image.Transpose.ROTATE_90,
    Image.Transpose.TRANSVERSE,
)


@dataclass(frozen=True)
class FrameRecord:
    image_slot: int
    crop_x: int
    crop_y: int
    width: int
    height: int


@dataclass(frozen=True)
class Piece:
    transform: int
    record_index: int
    x: int
    y: int


@dataclass(frozen=True)
class RoleLayout:
    image_ids: tuple[int, ...]
    records: tuple[FrameRecord, ...]
    groups: tuple[tuple[Piece, ...], ...]
    sequences: tuple[tuple[int, ...], ...]
    group_offsets: tuple[tuple[int, ...], ...]


def _signed_byte(value: int) -> int:
    return value if value < 0x80 else value - 0x100


def parse_layout(data: bytes) -> RoleLayout:
    if len(data) < 8:
        raise ValueError("role dat header is truncated")
    image_count = data[2] & 0x3F
    record_count = (data[3] << 2) | (data[2] >> 6)
    group_count = data[4]
    sequence_count = data[5]
    position = 8

    image_ids = tuple(struct.unpack_from(">i", data, position + index * 4)[0] for index in range(image_count))
    position += image_count * 4

    records = []
    for _ in range(record_count):
        if position + 5 > len(data):
            raise ValueError("role dat frame table is truncated")
        records.append(FrameRecord(*data[position:position + 5]))
        position += 5

    groups = []
    group_offsets = []
    for _ in range(group_count):
        if position >= len(data):
            raise ValueError("role dat group table is truncated")
        piece_count = data[position]
        position += 1
        pieces = []
        offsets = []
        for _ in range(piece_count):
            if position + 4 > len(data):
                raise ValueError("role dat group piece is truncated")
            packed, low_index, raw_x, raw_y = data[position:position + 4]
            pieces.append(
                Piece(
                    transform=packed & 7,
                    record_index=(low_index << 5) | (packed >> 3),
                    x=_signed_byte(raw_x),
                    y=_signed_byte(raw_y),
                )
            )
            offsets.append(position)
            position += 4
        groups.append(tuple(pieces))
        group_offsets.append(tuple(offsets))

    sequences = []
    for _ in range(sequence_count):
        if position + 5 > len(data):
            raise ValueError("role dat sequence table is truncated")
        frame_count = data[position]
        position += 5  # one-byte length followed by the always-present four-byte key
        if position + frame_count > len(data):
            raise ValueError("role dat sequence frames are truncated")
        sequences.append(tuple(data[position:position + frame_count]))
        position += frame_count

    return RoleLayout(
        image_ids=image_ids,
        records=tuple(records),
        groups=tuple(groups),
        sequences=tuple(sequences),
        group_offsets=tuple(group_offsets),
    )


def mirror_role_dat(data: bytes) -> bytes:
    layout = parse_layout(data)
    mirrored = bytearray(data)
    for pieces, offsets in zip(layout.groups, layout.group_offsets):
        for piece, offset in zip(pieces, offsets):
            if not 0 <= piece.record_index < len(layout.records):
                raise ValueError(f"piece references missing frame record {piece.record_index}")
            record = layout.records[piece.record_index]
            # This matches a/a/a.a(..., transform=2): rotations 4..7 swap the
            # source axes, so their horizontal mirror offset uses the original
            # record height; transforms 0..3 use its width.
            mirrored_extent = record.height if piece.transform >= 4 else record.width
            mirrored_x = -piece.x - mirrored_extent
            if not -128 <= mirrored_x <= 127:
                raise ValueError(f"mirrored x offset {mirrored_x} does not fit a signed byte")
            mirrored[offset] = (mirrored[offset] & 0xF8) | MIRRORED_TRANSFORM[piece.transform]
            mirrored[offset + 2] = mirrored_x & 0xFF
    return bytes(mirrored)


def _render_group(layout: RoleLayout, group_index: int, assets: AssetReader) -> Image.Image:
    prepared: list[tuple[Image.Image, int, int]] = []
    for piece in layout.groups[group_index]:
        record = layout.records[piece.record_index]
        atlas = assets.image(layout.image_ids[record.image_slot])
        image = atlas.crop(
            (
                record.crop_x,
                record.crop_y,
                record.crop_x + record.width,
                record.crop_y + record.height,
            )
        )
        operation = PIL_TRANSFORM[piece.transform]
        if operation is not None:
            image = image.transpose(operation)
        prepared.append((image, piece.x, piece.y))
    if not prepared:
        return Image.new("RGBA", (1, 1))
    left = min(x for image, x, y in prepared)
    top = min(y for image, x, y in prepared)
    right = max(x + image.width for image, x, y in prepared)
    bottom = max(y + image.height for image, x, y in prepared)
    canvas = Image.new("RGBA", (right - left, bottom - top))
    for image, x, y in prepared:
        canvas.alpha_composite(image, (x - left, y - top))
    return canvas


def write_preview(source: bytes, mirrored: bytes, apk: Path, output: Path) -> None:
    source_layout = parse_layout(source)
    mirror_layout = parse_layout(mirrored)
    if not source_layout.sequences or not source_layout.sequences[0]:
        raise ValueError("role dat has no previewable sequence")
    group_index = source_layout.sequences[0][0]
    assets = AssetReader(apk)
    try:
        original_image = _render_group(source_layout, group_index, assets)
        mirrored_image = _render_group(mirror_layout, group_index, assets)
    finally:
        assets.close()

    expected = original_image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    if mirrored_image.size != expected.size or ImageChops.difference(mirrored_image, expected).getbbox() is not None:
        raise ValueError("generated dat does not render as an exact horizontal mirror")

    padding = 16
    label_height = 28
    width = original_image.width + mirrored_image.width + padding * 3
    height = max(original_image.height, mirrored_image.height) + label_height + padding * 2
    sheet = Image.new("RGBA", (width, height), "white")
    draw = ImageDraw.Draw(sheet)
    draw.text((padding, padding), "96030 original", fill="black")
    mirror_x = padding * 2 + original_image.width
    draw.text((mirror_x, padding), "96031 mirrored", fill="black")
    sheet.alpha_composite(original_image, (padding, padding + label_height))
    sheet.alpha_composite(mirrored_image, (mirror_x, padding + label_height))
    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--apk", type=Path)
    parser.add_argument("--preview", type=Path)
    args = parser.parse_args()
    source = args.source.read_bytes()
    mirrored = mirror_role_dat(source)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(mirrored)
    if args.preview:
        if not args.apk:
            parser.error("--preview requires --apk")
        write_preview(source, mirrored, args.apk, args.preview)
    print(f"wrote {args.output} ({len(mirrored)} bytes)")


if __name__ == "__main__":
    main()
