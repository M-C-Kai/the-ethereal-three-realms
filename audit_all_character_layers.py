from __future__ import annotations

import copy
import importlib.util
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parent
RENDERER_PATH = Path(
    r"C:\Users\Kail\Documents\Codex\2026-08-24\new-chat\outputs"
    r"\equipment_resources\render_role_resources.py"
)
ROLE_PATH = Path(
    r"C:\Users\Kail\Documents\Codex\2026-08-24\new-chat\work"
    r"\apk-initial-role-reference\assets\res\role\100000.dat"
)
IMAGE_DIR = Path(
    r"C:\Users\Kail\Documents\Codex\2026-08-24\new-chat\outputs"
    r"\equipment_resources\output\rebuilt"
)
OUTPUT_DIR = ROOT / "appearance-layer-audit"


def load_renderer():
    spec = importlib.util.spec_from_file_location("appearance_role_renderer", RENDERER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load renderer: {RENDERER_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def render_isolated_sequence(renderer, resource, sequence_index, images, image_slot):
    all_parts = []
    layer_parts = []
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
            crop = source.convert("RGBA").crop(
                (record.x, record.y, record.x + record.width, record.y + record.height)
            )
        operation = renderer.TRANSFORMS[piece.transform]
        if operation is not None:
            crop = crop.transpose(operation)
        rendered = (crop, piece.x, piece.y)
        all_parts.append(rendered)
        if record.image_index == image_slot:
            layer_parts.append(rendered)
    if not all_parts:
        return Image.new("RGBA", (1, 1))
    left = min(x for _, x, _ in all_parts)
    top = min(y for _, _, y in all_parts)
    right = max(x + part.width for part, x, _ in all_parts)
    bottom = max(y + part.height for part, _, y in all_parts)
    canvas = Image.new("RGBA", (max(1, right - left), max(1, bottom - top)))
    for part, x, y in layer_parts:
        canvas.alpha_composite(part, (x - left, y - top))
    return canvas


def render_property_sheet(renderer, base_role, images, property_id: int) -> dict[str, object]:
    image_slot = property_id - 10
    group_base = (property_id + 1) * 1000
    candidate_ids = sorted(
        image_id for image_id in images if group_base <= image_id < group_base + 1000
    )
    preview_sequences = renderer.representative_sequences(base_role, limit=4)

    cell_w, cell_h, columns = 190, 170, 6
    rows = max(1, (len(candidate_ids) + columns - 1) // columns)
    sheet = Image.new("RGB", (columns * cell_w, rows * cell_h), "#f4f4f4")
    isolated_sheet = Image.new("RGB", (columns * cell_w, rows * cell_h), "#f4f4f4")
    draw = ImageDraw.Draw(sheet)
    isolated_draw = ImageDraw.Draw(isolated_sheet)

    for cell, image_id in enumerate(candidate_ids):
        resource = copy.deepcopy(base_role)
        resource.image_ids[image_slot] = image_id
        ox = (cell % columns) * cell_w
        oy = (cell // columns) * cell_h
        value = image_id - group_base
        is_default = image_id == base_role.image_ids[image_slot]
        label = f"p{property_id}={value}  image={image_id}"
        if is_default:
            label += "  DEFAULT"
        draw.text((ox + 4, oy + 3), label, fill="#a00000" if is_default else "black")
        isolated_draw.text((ox + 4, oy + 3), label, fill="#a00000" if is_default else "black")
        for frame_index, sequence_index in enumerate(preview_sequences):
            frame = renderer.render_sequence(resource, sequence_index, images)
            isolated = render_isolated_sequence(
                renderer, resource, sequence_index, images, image_slot
            )
            thumb = frame.copy()
            isolated_thumb = isolated.copy()
            thumb.thumbnail((82, 64), Image.Resampling.NEAREST)
            isolated_thumb.thumbnail((82, 64), Image.Resampling.NEAREST)
            x = ox + 5 + (frame_index % 2) * 90
            y = oy + 24 + (frame_index // 2) * 70
            sheet.paste(
                thumb,
                (x + (82 - thumb.width) // 2, y + (64 - thumb.height) // 2),
                thumb,
            )
            isolated_sheet.paste(
                isolated_thumb,
                (x + (82 - isolated_thumb.width) // 2, y + (64 - isolated_thumb.height) // 2),
                isolated_thumb,
            )
        draw.rectangle((ox, oy, ox + cell_w - 1, oy + cell_h - 1), outline="#999")
        isolated_draw.rectangle(
            (ox, oy, ox + cell_w - 1, oy + cell_h - 1), outline="#999"
        )

    target = OUTPUT_DIR / f"property-{property_id}-group-{group_base}.png"
    isolated_target = OUTPUT_DIR / f"property-{property_id}-isolated-{group_base}.png"
    sheet.save(target)
    isolated_sheet.save(isolated_target)
    return {
        "property": property_id,
        "image_slot": image_slot,
        "group_base": group_base,
        "default_image_id": base_role.image_ids[image_slot],
        "default_value": base_role.image_ids[image_slot] - group_base,
        "candidate_count": len(candidate_ids),
        "candidate_image_ids": candidate_ids,
        "preview_sequences": preview_sequences,
        "sheet": target.name,
        "isolated_sheet": isolated_target.name,
    }


def main() -> None:
    renderer = load_renderer()
    base_role = renderer.parse_role(ROLE_PATH)
    images = renderer.image_index(IMAGE_DIR)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest = {
        str(property_id): render_property_sheet(
            renderer, base_role, images, property_id
        )
        for property_id in range(14, 21)
    }
    (OUTPUT_DIR / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
