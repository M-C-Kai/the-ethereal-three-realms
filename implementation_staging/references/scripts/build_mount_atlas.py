from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from tools.map_ref_renderer import AssetReader
from tools.mirror_role_dat import PIL_TRANSFORM, RoleLayout, parse_layout

CATALOG = ROOT / 'data' / 'catalog' / 'mount_appearance_mapping.json'
OUTPUT_DIR = ROOT / 'references' / 'mount-atlas'

COLUMNS = 6
CELL_WIDTH = 250
CELL_HEIGHT = 210
IMAGE_WIDTH = 230
IMAGE_HEIGHT = 150
HEADER_HEIGHT = 64


def _primary_mount_slot(layout: RoleLayout, image_ids: list[int]) -> int:
    """Derive the role DAT slot that owns this mount family.

    The catalog defines the verified primary image ids.  The role DAT supplies
    the actual image-slot layout.  Matching the hundred-family distinguishes
    primary 410xx bodies from 411xx saddle/rider interface layers and likewise
    separates 400xx from the 401xx/402xx secondary flying layers.
    """
    if not image_ids:
        raise ValueError('mount family has no image_ids')
    family_prefix = int(image_ids[0]) // 100
    slots = [
        index
        for index, image_id in enumerate(layout.image_ids)
        if int(image_id) // 100 == family_prefix
    ]
    if len(slots) != 1:
        raise ValueError(
            f'expected exactly one primary mount slot for image family '
            f'{family_prefix}, got {slots}'
        )
    return slots[0]


def _representative_group(layout: RoleLayout, primary_slot: int) -> int:
    """Pick the first animation group that actually references the mount slot."""
    groups_with_mount: set[int] = set()
    for group_index, pieces in enumerate(layout.groups):
        for piece in pieces:
            if not 0 <= piece.record_index < len(layout.records):
                continue
            if layout.records[piece.record_index].image_slot == primary_slot:
                groups_with_mount.add(group_index)
                break

    for sequence in layout.sequences:
        for group_index in sequence:
            if group_index in groups_with_mount:
                return group_index
    if groups_with_mount:
        return min(groups_with_mount)
    raise ValueError(f'no group references primary mount slot {primary_slot}')


def _replace_mount_image(layout: RoleLayout, slot: int, image_id: int) -> RoleLayout:
    image_ids = list(layout.image_ids)
    image_ids[slot] = int(image_id)
    return RoleLayout(
        image_ids=tuple(image_ids),
        records=layout.records,
        groups=layout.groups,
        sequences=layout.sequences,
        group_offsets=layout.group_offsets,
    )


def _render_group(layout: RoleLayout, group_index: int, assets: AssetReader) -> Image.Image:
    prepared: list[tuple[Image.Image, int, int]] = []
    for piece in layout.groups[group_index]:
        if not 0 <= piece.record_index < len(layout.records):
            continue
        record = layout.records[piece.record_index]
        if not 0 <= record.image_slot < len(layout.image_ids):
            continue
        image_id = layout.image_ids[record.image_slot]
        if image_id not in assets.locations:
            continue
        atlas = assets.image(image_id)
        image = atlas.crop((
            record.crop_x,
            record.crop_y,
            record.crop_x + record.width,
            record.crop_y + record.height,
        ))
        operation = PIL_TRANSFORM[piece.transform]
        if operation is not None:
            image = image.transpose(operation)
        prepared.append((image, piece.x, piece.y))

    if not prepared:
        return Image.new('RGBA', (1, 1))
    left = min(x for image, x, y in prepared)
    top = min(y for image, x, y in prepared)
    right = max(x + image.width for image, x, y in prepared)
    bottom = max(y + image.height for image, x, y in prepared)
    canvas = Image.new('RGBA', (max(1, right - left), max(1, bottom - top)))
    for image, x, y in prepared:
        canvas.alpha_composite(image, (x - left, y - top))
    alpha_box = canvas.getchannel('A').getbbox()
    return canvas.crop(alpha_box) if alpha_box else canvas


def _font() -> ImageFont.ImageFont:
    return ImageFont.load_default()


def _draw_card(
    sheet: Image.Image,
    draw: ImageDraw.ImageDraw,
    preview: Image.Image,
    x: int,
    y: int,
    image_id: int,
    ride_code: int,
    role_model: int,
) -> None:
    draw.rectangle(
        (x, y, x + CELL_WIDTH - 1, y + CELL_HEIGHT - 1),
        outline=(80, 84, 92, 255),
        fill=(23, 27, 34, 255),
    )
    thumb = preview.copy()
    thumb.thumbnail((IMAGE_WIDTH, IMAGE_HEIGHT), Image.Resampling.NEAREST)
    px = x + (CELL_WIDTH - thumb.width) // 2
    py = y + 34 + (IMAGE_HEIGHT - thumb.height) // 2
    sheet.alpha_composite(thumb, (px, py))
    font = _font()
    draw.text((x + 8, y + 7), f'{image_id}', fill='white', font=font)
    draw.text((x + 8, y + CELL_HEIGHT - 36), f'ride={ride_code}', fill=(190, 198, 210, 255), font=font)
    draw.text((x + 8, y + CELL_HEIGHT - 20), f'role={role_model}', fill=(190, 198, 210, 255), font=font)


def _write_sheet(entries: list[dict[str, object]], output: Path) -> None:
    rows = (len(entries) + COLUMNS - 1) // COLUMNS
    sheet = Image.new(
        'RGBA',
        (COLUMNS * CELL_WIDTH, HEADER_HEIGHT + rows * CELL_HEIGHT),
        (15, 17, 21, 255),
    )
    draw = ImageDraw.Draw(sheet)
    font = _font()
    draw.text((12, 10), 'Piao Miao San Jie - APK mount resource atlas', fill='white', font=font)
    draw.text(
        (12, 30),
        'source: images.o + png*.p + role/*.dat; ids/families from mount_appearance_mapping.json',
        fill=(170, 180, 194, 255),
        font=font,
    )
    for index, entry in enumerate(entries):
        x = (index % COLUMNS) * CELL_WIDTH
        y = HEADER_HEIGHT + (index // COLUMNS) * CELL_HEIGHT
        _draw_card(
            sheet,
            draw,
            entry['preview'],  # type: ignore[arg-type]
            x,
            y,
            int(entry['image_id']),
            int(entry['ride_code']),
            int(entry['role_model']),
        )
    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.convert('RGB').save(output, optimize=True)


def build(apk: Path, output_dir: Path = OUTPUT_DIR) -> dict[str, object]:
    catalog = json.loads(CATALOG.read_text(encoding='utf-8'))
    image_base = int(catalog['image_base'])
    role_template = str(catalog['resource_paths']['role_dat'])
    families = catalog['families']
    expected_count = int(catalog['count'])
    image_ids = [int(value) for family in families for value in family['image_ids']]
    if len(image_ids) != expected_count or len(set(image_ids)) != expected_count:
        raise ValueError('mount catalog count/uniqueness mismatch')

    assets = AssetReader(apk)
    entries: list[dict[str, object]] = []
    family_manifest: list[dict[str, object]] = []
    try:
        for family in families:
            role_model = int(family['role_model'])
            family_ids = [int(value) for value in family['image_ids']]
            role_resource = role_template.format(role_model=role_model)
            layout = parse_layout(assets.archive.read(role_resource))
            primary_slot = _primary_mount_slot(layout, family_ids)
            representative_group = _representative_group(layout, primary_slot)
            family_entries: list[dict[str, object]] = []
            for image_id in family_ids:
                if image_id not in assets.locations:
                    raise ValueError(f'images.o has no catalog image id {image_id}')
                preview = _render_group(
                    _replace_mount_image(layout, primary_slot, image_id),
                    representative_group,
                    assets,
                )
                container, offset = assets.locations[image_id]
                entry = {
                    'image_id': image_id,
                    'ride_code': image_id - image_base,
                    'role_model': role_model,
                    'role_resource': role_resource,
                    'primary_slot': primary_slot,
                    'representative_group': representative_group,
                    'asset_index': {'container': container, 'offset': offset},
                    'sprite_status': 'rendered_from_apk',
                    'preview_width': preview.width,
                    'preview_height': preview.height,
                    'preview': preview,
                }
                entries.append(entry)
                family_entries.append(entry)

            family_output = output_dir / f'model_{role_model}_resources.png'
            _write_sheet(family_entries, family_output)
            family_manifest.append({
                'role_model': role_model,
                'role_resource': role_resource,
                'primary_slot': primary_slot,
                'representative_group': representative_group,
                'count': len(family_entries),
                'atlas': family_output.name,
            })

        _write_sheet(entries, output_dir / 'mount_riding_atlas.png')
    finally:
        assets.close()

    named = catalog.get('named_templates', {})
    serializable_entries = []
    for entry in entries:
        row = {key: value for key, value in entry.items() if key != 'preview'}
        row['name'] = named.get(str(entry['image_id']), {}).get('name')
        serializable_entries.append(row)

    manifest = {
        'version': 2,
        'source': {
            'apk': apk.name,
            'catalog': str(CATALOG.relative_to(ROOT)),
            'images_index': catalog['resource_paths']['images_index'],
            'packed_image': catalog['resource_paths']['packed_image'],
        },
        'count': expected_count,
        'families': family_manifest,
        'entries': serializable_entries,
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / 'manifest.json').write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding='utf-8',
    )
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--apk', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, default=OUTPUT_DIR)
    args = parser.parse_args()
    manifest = build(args.apk, args.output_dir)
    print(f'wrote {manifest["count"]} resource-backed mount previews to {args.output_dir}')


if __name__ == '__main__':
    main()
