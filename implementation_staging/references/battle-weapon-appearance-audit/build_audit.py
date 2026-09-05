#!/usr/bin/env python3
"""Build battle-weapon visual audit sheets from extracted APK images.

Does not guess icon-group to battle-family mappings.
"""
from __future__ import annotations

import json
import struct
import sys
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / 'references' / 'scripts'
sys.path.insert(0, str(SCRIPTS))
from extract_game_images import rebuild_png  # noqa: E402

AUDIT_DIR = Path(__file__).resolve().parent
IMAGE_DIR = ROOT / 'build' / 'weapon-apk-extracted' / 'assets' / 'res' / 'images'
ICON_GROUPS = list(range(21, 34))
BATTLE_FAMILIES = [220, 221, 230, 231, 240, 241, 242, 250, 260, 270, 271, 280, 290]


def parse_images_o(path: Path) -> dict[int, tuple[int, int]]:
    index = path.read_bytes()
    index_len = struct.unpack_from('>H', index, 0)[0]
    records = index[2:2 + index_len]
    mapping: dict[int, tuple[int, int]] = {}
    for offset in range(0, len(records), 7):
        rec = records[offset:offset + 7]
        if len(rec) != 7:
            continue
        image_id, container_no, data_offset = struct.unpack_from('>IBH', rec, 0)
        mapping[int(image_id)] = (int(container_no), int(data_offset))
    return mapping


def load_png(index_map: dict[int, tuple[int, int]], containers: dict[int, bytes], image_id: int) -> Image.Image:
    container_no, data_offset = index_map[image_id]
    if container_no not in containers:
        path = IMAGE_DIR / f'png{container_no}.p'
        containers[container_no] = path.read_bytes()
    png, _, _ = rebuild_png(containers[container_no], data_offset)
    return Image.open(BytesIO(png)).convert('RGBA')


def fit_cell(image: Image.Image, max_side: int) -> Image.Image:
    width, height = image.size
    if width <= 0 or height <= 0:
        return Image.new('RGBA', (max_side, max_side))
    scale = min(max_side / width, max_side / height, 4)
    new_size = (max(1, int(width * scale)), max(1, int(height * scale)))
    return image.resize(new_size, Image.Resampling.NEAREST)


def build_icon_sheet(index_map: dict[int, tuple[int, int]], containers: dict[int, bytes]) -> dict[str, list[int]]:
    scale = 3
    gutter = 36
    cell_width, cell_height = 82, 96
    catalog: dict[str, list[int]] = {}
    rows: list[tuple[int, list[tuple[int, Image.Image]]]] = []
    for group in ICON_GROUPS:
        atlas_id = 3_002_424 + group * 10_000
        cells: list[tuple[int, Image.Image]] = []
        if atlas_id in index_map:
            atlas = load_png(index_map, containers, atlas_id)
            frame_count = min(10, atlas.width // 24)
            for frame in range(frame_count):
                icon_code = group * 100 + frame
                icon = atlas.crop((frame * 24, 0, frame * 24 + 24, 24)).resize(
                    (24 * scale, 24 * scale), Image.Resampling.NEAREST
                )
                cells.append((icon_code, icon))
        catalog[str(group)] = [code for code, _ in cells]
        rows.append((group, cells))
    max_frames = max((len(cells) for _, cells in rows), default=1)
    sheet = Image.new(
        'RGB',
        (gutter + max(1, max_frames) * cell_width, len(ICON_GROUPS) * cell_height),
        'white',
    )
    draw = ImageDraw.Draw(sheet)
    for row, (group, cells) in enumerate(rows):
        y = row * cell_height
        draw.text((4, y + 40), str(group), fill='#333')
        for col, (icon_code, icon) in enumerate(cells):
            x = gutter + col * cell_width
            sheet.paste(icon, (x + 5, y + 3), icon)
            draw.text((x + 5, y + 78), str(icon_code), fill='black')
            draw.rectangle((x, y, x + cell_width - 1, y + cell_height - 1), outline='#999')
    sheet.save(AUDIT_DIR / 'icon_groups.png')
    return catalog


def build_battle_sheet(index_map: dict[int, tuple[int, int]], containers: dict[int, bytes]) -> dict[str, list[int]]:
    catalog: dict[str, list[int]] = {}
    rows: list[tuple[int, list[tuple[int, Image.Image]]]] = []
    for family in BATTLE_FAMILIES:
        found: list[tuple[int, Image.Image]] = []
        ids: list[int] = []
        for image_id in range(family * 100, family * 100 + 100):
            if image_id not in index_map:
                continue
            try:
                image = load_png(index_map, containers, image_id)
            except Exception:
                continue
            found.append((image_id, image))
            ids.append(image_id)
        catalog[str(family)] = ids
        rows.append((family, found))
    max_count = max((len(found) for _, found in rows), default=1)
    gutter = 44
    cell = 72
    label = 16
    row_h = cell + label
    sheet = Image.new(
        'RGB',
        (gutter + max(1, max_count) * cell, len(BATTLE_FAMILIES) * row_h),
        'white',
    )
    draw = ImageDraw.Draw(sheet)
    for row, (family, found) in enumerate(rows):
        y = row * row_h
        draw.text((4, y + cell // 2), str(family), fill='#333')
        for col, (image_id, image) in enumerate(found):
            x = gutter + col * cell
            fitted = fit_cell(image, cell - 18)
            px = x + (cell - fitted.width) // 2
            py = y + (cell - fitted.height) // 2
            sheet.paste(fitted, (px, py), fitted)
            draw.text((x + 4, y + cell + 2), str(image_id), fill='black')
            draw.rectangle((x, y, x + cell - 1, y + row_h - 1), outline='#999')
    sheet.save(AUDIT_DIR / 'battle_weapon_families.png')
    return catalog


def main() -> None:
    index_map = parse_images_o(IMAGE_DIR / 'images.o')
    containers: dict[int, bytes] = {}
    icon_groups = build_icon_sheet(index_map, containers)
    battle_families = build_battle_sheet(index_map, containers)
    payload = {
        'source': 'build/weapon-apk-extracted/assets/res/images',
        'icon_groups': icon_groups,
        'battle_weapon_families': battle_families,
    }
    (AUDIT_DIR / 'manifest.json').write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + '\n',
        encoding='utf-8',
    )
    print('icon_groups', {k: len(v) for k, v in icon_groups.items()})
    print('battle_weapon_families', {k: len(v) for k, v in battle_families.items()})


if __name__ == '__main__':
    main()
