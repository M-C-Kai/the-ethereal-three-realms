from __future__ import annotations

import copy
import importlib.util
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


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
OUTPUT = ROOT / "docs" / "diagnostics" / "character-appearance" / "appearance-layer-audit" / "selected-equipment-mapping.png"


spec = importlib.util.spec_from_file_location("selected_role_renderer", RENDERER_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError(f"cannot load renderer: {RENDERER_PATH}")
renderer = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = renderer
spec.loader.exec_module(renderer)

base = renderer.parse_role(ROLE_PATH)
images = renderer.image_index(IMAGE_DIR)
sequences = renderer.representative_sequences(base, limit=4)
weapon_sequences = [
    sequence_index
    for sequence_index, pieces in enumerate(base.sequences)
    if any(
        0 <= piece.record_index < len(base.records)
        and base.records[piece.record_index].image_index in {16, 25}
        for piece in pieces
    )
]
print(f"weapon sequences: {weapon_sequences}")

# The unequipped client state keeps the mandatory base trousers (property 14=0
# resolves to image 15000) and clears every optional armour/weapon layer.
unequipped = copy.deepcopy(base)
unequipped.image_ids[4] = 15000
for image_slot in range(5, 32):
    unequipped.image_ids[image_slot] = 0

SELECTIONS = {
    "01 头盔 p20=3": {10: 21003},
    "02 肩甲 p16=23": {6: 17023},
    "03 铠甲 p15=34": {5: 16034},
    "05 腿甲 p14=25": {4: 15025},
    "07 披风 p19=3": {9: 20003},
    "08 护腕 p17=8": {7: 18008},
    "09 鞋子 p18=22": {8: 19022},
    # property 7=270001 selects weapon atlas 27000 and quality overlay 30601.
    "10 武器 p7=270001": {16: 27000, 25: 30601},
}

variants = [("00 未装备", {})]
variants.extend(SELECTIONS.items())
full_set = {}
for selection in SELECTIONS.values():
    full_set.update(selection)
variants.append(("全部可见装备", full_set))

cell_w, cell_h, columns = 240, 200, 4
rows = (len(variants) + columns - 1) // columns
sheet = Image.new("RGB", (columns * cell_w, rows * cell_h), "#f4f4f4")
draw = ImageDraw.Draw(sheet)
font = ImageFont.truetype(r"C:\Windows\Fonts\msyh.ttc", 14)

for cell, (label, replacements) in enumerate(variants):
    resource = copy.deepcopy(unequipped)
    for image_slot, image_id in replacements.items():
        resource.image_ids[image_slot] = image_id
    ox = (cell % columns) * cell_w
    oy = (cell // columns) * cell_h
    draw.text((ox + 6, oy + 5), label, fill="black", font=font)
    for frame_index, sequence in enumerate(sequences):
        frame = renderer.render_sequence(resource, sequence, images)
        thumb = frame.copy()
        thumb.thumbnail((105, 78), Image.Resampling.NEAREST)
        x = ox + 6 + (frame_index % 2) * 112
        y = oy + 28 + (frame_index // 2) * 82
        sheet.paste(
            thumb,
            (x + (105 - thumb.width) // 2, y + (78 - thumb.height) // 2),
            thumb,
        )
    draw.rectangle((ox, oy, ox + cell_w - 1, oy + cell_h - 1), outline="#888")

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
sheet.save(OUTPUT)
print(OUTPUT)
