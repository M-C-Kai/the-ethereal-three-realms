from __future__ import annotations

import copy
import importlib.util
import sys
from pathlib import Path

from PIL import Image, ImageDraw


REFERENCE_SCRIPT = Path(
    r"C:\Users\Kail\Documents\Codex\2026-08-24\new-chat\outputs\piaomiao_local_login"
    r"\references\scripts\render_role_resources.py"
)
ROLE_DIR = Path(
    r"C:\Users\Kail\Documents\Codex\2026-08-24\new-chat\work"
    r"\apk-initial-role-reference\assets\res\role"
)
IMAGE_DIR = Path(
    r"C:\Users\Kail\Documents\Codex\2026-08-24\new-chat\work"
    r"\initial-apk-images\rebuilt"
)
OUTPUT = Path(__file__).with_name("player_overlay_variants.png")


spec = importlib.util.spec_from_file_location("role_renderer", REFERENCE_SCRIPT)
renderer = importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules[spec.name] = renderer
spec.loader.exec_module(renderer)

base = renderer.parse_role(ROLE_DIR / "100000.dat")
images = renderer.image_index(IMAGE_DIR)

# Indices 4..10 are exactly the image slots changed by character properties
# 14..20. Each row changes one slot while keeping the other base layers fixed.
variants = [
    ("base", None, None),
    ("p14=1", 4, 15001),
    ("p14=20", 4, 15020),
    ("p15=2", 5, 16002),
    ("p15=20", 5, 16020),
    ("p16=1", 6, 17001),
    ("p16=20", 6, 17020),
    ("p17=2", 7, 18002),
    ("p17=20", 7, 18020),
    ("p18=2", 8, 19002),
    ("p18=20", 8, 19020),
    ("p19=2", 9, 20002),
    ("p19=10", 9, 20010),
]

frames = []
for label, index, value in variants:
    resource = copy.deepcopy(base)
    if index is not None:
        resource.image_ids[index] = value
    frame = renderer.render_sequence(resource, 0, images)
    frames.append((label, frame))

cell_w, cell_h = 180, 155
sheet = Image.new("RGBA", (cell_w * 4, cell_h * 4), "white")
draw = ImageDraw.Draw(sheet)
for item_index, (label, frame) in enumerate(frames):
    x = (item_index % 4) * cell_w
    y = (item_index // 4) * cell_h
    thumb = frame.copy()
    thumb.thumbnail((160, 125), Image.Resampling.NEAREST)
    sheet.alpha_composite(thumb, (x + (cell_w - thumb.width) // 2, y + 24))
    draw.text((x + 5, y + 5), label, fill="black")
    draw.rectangle((x, y, x + cell_w - 1, y + cell_h - 1), outline="#999")

sheet.convert("RGB").save(OUTPUT)
