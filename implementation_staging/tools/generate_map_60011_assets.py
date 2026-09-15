"""Generate the complete 60011 scene, map.ref and 127x127 map.o source specs."""
from __future__ import annotations

import io
import json
import zipfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
MAP_DIR = ROOT / "maps" / "60011"
SOURCE = MAP_DIR / "source_scene.png"
ASSET_BUNDLE = MAP_DIR / "60011_apk_assets.zip"
MAP_WIDTH = MAP_HEIGHT = 127
SCENE_WIDTH, SCENE_HEIGHT = 675, 900
COLUMNS, ROWS = 9, 14
SCENE_X, SCENE_Y = -337, 190
COORDINATE_SHIFT = 9

# Traced against source_scene.png after resizing to SCENE_WIDTH x SCENE_HEIGHT.
# White polygons are ground/road surfaces. Dark polygons remove visible solid
# scenery which shares grass colours with the walkable floor.
WALKABLE_POLYGONS = (
    ((282, 300), (360, 275), (455, 265), (535, 285), (675, 305),
     (675, 900), (505, 900), (482, 858), (490, 810), (520, 760),
     (568, 706), (610, 646), (620, 590), (590, 536), (540, 492),
     (480, 454), (410, 430), (350, 414), (302, 382), (270, 342)),
)
BLOCKED_POLYGONS = (
    # House, steps, barrels and chest.
    ((468, 48), (675, 35), (675, 329), (575, 316), (500, 286), (463, 226)),
    # Central cliff, large tree and dense foreground vegetation.
    ((118, 450), (252, 415), (397, 458), (505, 520), (525, 617),
     (492, 724), (438, 812), (292, 900), (80, 900), (58, 746), (87, 570)),
    # Stone lantern and its base.
    ((526, 620), (591, 616), (613, 719), (553, 760), (516, 709)),
)


def anchor_for_rect(x: int, y: int, width: int, height: int) -> tuple[int, int, int, int]:
    """Choose the nearest isometric tile anchor to a scene rectangle's centre."""
    center_x = x + width / 2
    center_y = y + height / 2
    tile_x = round((center_x / 10 + center_y / 5 - 2) / 2)
    tile_y = round((center_y / 5 - 2 - center_x / 10) / 2)
    offset_x = x - 10 * (tile_x - tile_y)
    offset_y = y - 5 * (tile_x + tile_y + 2)
    if not (0 <= tile_x < MAP_WIDTH and 0 <= tile_y < MAP_HEIGHT):
        raise ValueError(f"slice anchor outside map: {(tile_x, tile_y)}")
    if not (-128 <= offset_x <= 127 and -128 <= offset_y <= 127):
        raise ValueError(f"slice offset outside signed byte: {(offset_x, offset_y)}")
    return tile_x, tile_y, offset_x, offset_y


def build_collision(scene: Image.Image) -> tuple[list[str], Image.Image]:
    mask = Image.new("L", scene.size, 0)
    draw = ImageDraw.Draw(mask)
    for polygon in WALKABLE_POLYGONS:
        draw.polygon(polygon, fill=255)
    for polygon in BLOCKED_POLYGONS:
        draw.polygon(polygon, fill=0)
    # Keep the actor footprint away from traced scenery edges.
    safe = mask.filter(ImageFilter.MinFilter(15))
    collision: list[str] = []
    for tile_y in range(MAP_HEIGHT):
        row = []
        for tile_x in range(MAP_WIDTH):
            screen_x = 10 * (tile_x - tile_y) - SCENE_X
            screen_y = 5 * (tile_x + tile_y + 2) - SCENE_Y
            inside = 0 <= screen_x < SCENE_WIDTH and 0 <= screen_y < SCENE_HEIGHT
            row.append("." if inside and safe.getpixel((screen_x, screen_y)) else "#")
        collision.append("".join(row))

    overlay = scene.convert("RGBA")
    tint = Image.new("RGBA", scene.size, (30, 220, 70, 0))
    tint.putalpha(safe.point(lambda value: 105 if value else 0))
    overlay.alpha_composite(tint)
    return collision, overlay


def generate() -> None:
    old_map = json.loads((MAP_DIR / "map.json").read_text(encoding="utf-8"))
    scene = Image.open(SOURCE).convert("RGB").resize(
        (SCENE_WIDTH, SCENE_HEIGHT), Image.Resampling.LANCZOS
    )

    resources = []
    image_records = []
    composites = []
    tiles = [[None for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]
    slice_payloads: dict[str, bytes] = {}

    index = 0
    for row in range(ROWS):
        y0 = round(row * SCENE_HEIGHT / ROWS)
        y1 = round((row + 1) * SCENE_HEIGHT / ROWS)
        for column in range(COLUMNS):
            x0 = round(column * SCENE_WIDTH / COLUMNS)
            x1 = round((column + 1) * SCENE_WIDTH / COLUMNS)
            width, height = x1 - x0, y1 - y0
            image_id = 60011000 + index
            filename = f"60011_{index:03d}.png"
            tile_x, tile_y, offset_x, offset_y = anchor_for_rect(
                SCENE_X + x0, SCENE_Y + y0, width, height
            )
            if tiles[tile_y][tile_x] is not None:
                raise ValueError(f"duplicate slice anchor: {(tile_x, tile_y)}")
            tiles[tile_y][tile_x] = index
            resources.append({
                "image_id": image_id, "file": filename,
                "column": column, "row": row,
                "x": x0, "y": y0, "width": width, "height": height,
                "screen_x": SCENE_X + x0, "screen_y": SCENE_Y + y0,
                "tile_x": tile_x, "tile_y": tile_y,
            })
            image_records.append({
                "image_id": image_id, "crop_x": 0, "crop_y": 0,
                "width": width, "height": height,
            })
            composites.append({
                "flags": 2, "terrain": 0, "value_b": 0, "value_c": 0,
                "layers": [{
                    "reference": index, "x": offset_x, "y": offset_y, "transform": 0,
                }],
            })
            with io.BytesIO() as buffer:
                scene.crop((x0, y0, x1, y1)).save(buffer, format="PNG")
                slice_payloads[filename] = buffer.getvalue()
            index += 1

    if index != COLUMNS * ROWS:
        raise AssertionError(index)

    collision, collision_preview = build_collision(scene)
    mirror = ["." * MAP_WIDTH for _ in range(MAP_HEIGHT)]
    map_spec = {
        "format": "piaomiao-dynamic-map-v1", "map_id": 60011,
        "width": MAP_WIDTH, "height": MAP_HEIGHT, "map_type": old_map["map_type"],
        "tile_pixel_width": 20, "tile_pixel_height": 10,
        "tile_definitions": list(range(index)), "tiles": tiles,
        "collision": ["".join(row) for row in collision],
        "mirror": ["".join(row) for row in mirror],
        "registry": {
            "name": "翠溪村", "spawn": {"x": 59, "y": 42}, "npcs": [],
            "portals": [{
                "id": 6001101, "name": "返回长安", "model": -2043000,
                "x": 61, "y": 44, "direction": 0,
                "target_map_id": 58, "target_x": 60, "target_y": 67,
            }],
            "inbound_portals": [{
                "source_map_id": 58, "id": 580007, "name": "翠溪村传送阵",
                "model": -2043000, "x": 50, "y": 70, "direction": 0,
            }],
        },
    }
    ref_spec = {
        "format": "piaomiao-map-ref-v1", "map_id": 60011,
        "image_records": image_records, "composite_tiles": composites,
    }
    manifest = {
        "format": "piaomiao-map-asset-bundle-v2", "map_id": 60011,
        "source_size": list(Image.open(SOURCE).size),
        "scene_size": [SCENE_WIDTH, SCENE_HEIGHT],
        "scene_origin": [SCENE_X, SCENE_Y],
        "grid": [COLUMNS, ROWS],
        "collision_source": "source_scene.png",
        "collision_method": "scene-coordinate walkable polygons minus solid scenery, 7px inset",
        "resources": resources,
    }

    (MAP_DIR / "map.json").write_text(
        json.dumps(map_spec, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (MAP_DIR / "map.ref.json").write_text(
        json.dumps(ref_spec, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (MAP_DIR / "resource_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    scene.save(MAP_DIR / "preview.png")
    collision_preview.save(MAP_DIR / "collision_preview.png")
    with zipfile.ZipFile(ASSET_BUNDLE, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("resource_manifest.json", json.dumps(manifest, ensure_ascii=False))
        for filename, payload in slice_payloads.items():
            archive.writestr(f"slices/{filename}", payload)
    print(f"generated {index} slices, {MAP_WIDTH}x{MAP_HEIGHT} map and {ASSET_BUNDLE}")


if __name__ == "__main__":
    generate()
