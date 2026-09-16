"""Generate the complete 60011 scene, map.ref and 127x127 map.o source specs."""
from __future__ import annotations

import io
import json
import zipfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImageChops


ROOT = Path(__file__).resolve().parents[1]
MAP_DIR = ROOT / "maps" / "60011"
SOURCE = MAP_DIR / "source_scene.png"
ASSET_BUNDLE = MAP_DIR / "60011_apk_assets.zip"
MAP_WIDTH = MAP_HEIGHT = 127
SCENE_WIDTH, SCENE_HEIGHT = 1040, 743
COLUMNS, ROWS = 18, 7
SCENE_X, SCENE_Y = -520, 270
COORDINATE_SHIFT = 9

# Traced against source_scene.png after resizing to SCENE_WIDTH x SCENE_HEIGHT.
# White polygons are ground/road surfaces. Dark polygons remove visible solid
# scenery which shares grass colours with the walkable floor.
EDGE_MARGIN = 180
WALKABLE_POLYGONS = (
    # Main courtyard and road on the right bank.
    ((547, 301), (642, 314), (759, 349), (854, 424),
     (807, 533), (663, 588), (615, 547), (649, 492),
     (745, 410), (677, 383), (561, 369), (506, 362),
     (479, 342), (499, 314)),
    # Opposite bank's inner road; outer terraces are scenery only.
    ((205, 219), (321, 232), (362, 260), (342, 287),
     (301, 308), (219, 314), (137, 294), (151, 267)),
)
# User-authorized local shallow walking line across the visible stone shoal.
SHOAL_PATH = ((325, 278), (355, 281), (388, 285), (422, 294),
              (454, 307), (483, 321), (514, 335))
SHOAL_WIDTH = 34
BLOCKED_POLYGONS = (
    # House and adjacent tree.
    ((645, 170), (755, 169), (829, 221), (842, 288),
     (813, 339), (749, 331), (683, 286), (642, 250)),
    # Central cliff/tree below the courtyard.
    ((464, 378), (568, 370), (637, 397), (663, 449),
     (624, 513), (539, 540), (467, 485)),
    # Stone lantern.
    ((653, 414), (681, 411), (691, 484), (667, 503), (647, 469)),
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


def prepare_scene() -> None:
    """Deterministically cut/reflect border scenery around the unmarked art."""
    art = Image.open(MAP_DIR / 'source_art.png').convert('RGB')
    marked = Image.open(MAP_DIR / 'walkable_reference.png').convert('RGB')
    if art.size != marked.size:
        raise ValueError('walkable reference and clean art sizes differ')
    # Extract the neon boundary, then fill the regions it encloses. The two
    # attachments have minor texture differences, so pixel subtraction alone
    # is not a reliable walking mask.
    values = [255 if g > 180 and g-r > 90 and g-b > 100 else 0
              for r,g,b in marked.getdata()]
    raw = Image.new('L', art.size); raw.putdata(values)
    raw = raw.filter(ImageFilter.MaxFilter(5))
    ImageDraw.floodfill(raw, (0,0), 128, thresh=0)
    enclosed = raw.point(lambda v: 0 if v == 128 else 255)
    raw = Image.new('L', art.size)
    while enclosed.getbbox():
        box = enclosed.getbbox(); y = box[1]
        x = next(x for x in range(box[0],box[2]) if enclosed.getpixel((x,y)))
        before = enclosed.copy()
        ImageDraw.floodfill(enclosed, (x,y), 0, thresh=0)
        component = ImageChops.subtract(before, enclosed)
        if component.histogram()[255] > 500:
            raw = ImageChops.lighter(raw, component)
    # The courtyard contour touches the house/vegetation and has a break in
    # its anti-aliased outline. Trace that enclosed area from the user overlay.
    ImageDraw.Draw(raw).polygon(((950,435),(1050,385),(1045,410),
        (1100,430),(1140,438),(1130,455),(1190,485),(1210,495),
        (1260,480),(1280,480),(1275,500),(1320,525),(1250,555),
        (1205,550),(1190,580),(1110,580),(1090,555),(1030,550),
        (985,530),(935,530),(885,500),(900,480),(975,480),(970,460)), fill=255)
    inner = art.resize((680,383), Image.Resampling.LANCZOS)
    scene = Image.new('RGB', (1040,743))
    scene.paste(inner, (180,180))
    scene.paste(ImageOps.mirror(inner.crop((0,0,180,383))), (0,180))
    scene.paste(ImageOps.mirror(inner.crop((500,0,680,383))), (860,180))
    scene.paste(ImageOps.flip(scene.crop((0,180,1040,360))), (0,0))
    scene.paste(ImageOps.flip(scene.crop((0,383,1040,563))), (0,563))
    scene.save(SOURCE)
    mask = Image.new('L', scene.size)
    mask.paste(raw.resize(inner.size, Image.Resampling.NEAREST), (180,180))
    mask.save(MAP_DIR / 'walkable_reference_mask.png')


def build_collision(scene: Image.Image) -> tuple[list[str], Image.Image]:
    # Approximate a marked boundary to the 20x10 diamond grid with 3px tolerance.
    safe = Image.open(MAP_DIR / 'walkable_reference_mask.png').convert('L')
    safe = safe.filter(ImageFilter.MaxFilter(7))
    border = ImageDraw.Draw(safe)
    border.rectangle((0, 0, SCENE_WIDTH - 1, EDGE_MARGIN - 1), fill=0)
    border.rectangle((0, SCENE_HEIGHT - EDGE_MARGIN, SCENE_WIDTH - 1, SCENE_HEIGHT - 1), fill=0)
    border.rectangle((0, 0, EDGE_MARGIN - 1, SCENE_HEIGHT - 1), fill=0)
    border.rectangle((SCENE_WIDTH - EDGE_MARGIN, 0, SCENE_WIDTH - 1, SCENE_HEIGHT - 1), fill=0)
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
    prepare_scene()
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
                "flags": 6, "terrain": 0, "value_b": 0, "value_c": 0,
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
            "name": "翠溪村", "spawn": {"x": 71, "y": 58}, "npcs": [],
            "portals": [{
                "id": 6001101, "name": "返回长安", "model": -2043000,
                "x": 72, "y": 59, "direction": 0,
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
        "collision_source": "walkable_reference.png",
        "collision_method": "green annotation difference mask, 3px grid tolerance, 180px blocked border",
        "source_art": "source_art.png",
        "inner_size": [680, 383],
        "inner_origin": [180, 180],
        "border_method": "reflected edge scenery",
        "edge_margin": EDGE_MARGIN,
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
    collision_preview.save(MAP_DIR / "collision_preview_marked.png")
    with zipfile.ZipFile(ASSET_BUNDLE, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("resource_manifest.json", json.dumps(manifest, ensure_ascii=False))
        for filename, payload in slice_payloads.items():
            archive.writestr(f"slices/{filename}", payload)
    print(f"generated {index} slices, {MAP_WIDTH}x{MAP_HEIGHT} map and {ASSET_BUNDLE}")


if __name__ == "__main__":
    generate()
