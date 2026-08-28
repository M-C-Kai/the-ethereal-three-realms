from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--image-dir', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--min-group', type=int, default=0)
    parser.add_argument('--max-group', type=int, default=99)
    args = parser.parse_args()

    scale = 3
    cell_width, cell_height = 82, 96
    groups: list[tuple[int, Path]] = []
    for group in range(args.min_group, args.max_group + 1):
        image_id = 3_002_424 + group * 10_000
        matches = list(args.image_dir.glob(f'{image_id:07d}_*.png'))
        if matches:
            groups.append((group, matches[0]))
    max_frames = max(Image.open(path).width // 24 for _, path in groups)
    sheet = Image.new('RGB', (max_frames * cell_width, len(groups) * cell_height), 'white')
    draw = ImageDraw.Draw(sheet)
    for row, (group, path) in enumerate(groups):
        with Image.open(path) as atlas:
            atlas = atlas.convert('RGBA')
            frame_count = atlas.width // 24
            for frame in range(frame_count):
                icon = atlas.crop((frame * 24, 0, frame * 24 + 24, 24)).resize(
                    (24 * scale, 24 * scale), Image.Resampling.NEAREST
                )
                x = frame * cell_width
                y = row * cell_height
                sheet.paste(icon, (x + 5, y + 3), icon)
                draw.text((x + 5, y + 78), f'{group * 100 + frame}', fill='black')
                draw.rectangle((x, y, x + cell_width - 1, y + cell_height - 1), outline='#999')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(args.output)


if __name__ == '__main__':
    main()
