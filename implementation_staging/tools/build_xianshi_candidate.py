from __future__ import annotations

import json
from pathlib import Path


WIDTH = 32
HEIGHT = 24


def main() -> None:
    # Use every composite index directly, so a grid value is also the tile
    # number printed in 58.tile-atlas.png.
    tiles = [[5 for _ in range(WIDTH)] for _ in range(HEIGHT)]
    mirror = [[False for _ in range(WIDTH)] for _ in range(HEIGHT)]

    # Subtle grass variation, kept sparse so buildings remain readable.
    grass_variants = (5, 10, 12, 13, 21, 22, 23, 24, 27, 28, 29, 30, 33, 46, 54, 56, 68, 82, 87, 91, 95, 98, 102, 103, 107, 109)
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if ((x * 7) + (y * 11)) % 13 == 0:
                tiles[y][x] = grass_variants[((x * 3) + y) % len(grass_variants)]

    # Main village roads.
    for x in range(2, WIDTH - 2):
        tiles[12][x] = 17 if x % 2 == 0 else 20
    for y in range(2, HEIGHT - 1):
        tiles[y][16] = 17 if y % 2 == 0 else 25

    # Five-by-five central stone plaza.
    plaza = (61, 62, 64, 69, 70, 71, 73, 74, 78, 79)
    for y in range(10, 15):
        for x in range(14, 19):
            tiles[y][x] = plaza[((y - 10) * 5 + (x - 14)) % len(plaza)]

    # Northern entrance and boundary markers.
    tiles[2][16] = 18
    tiles[3][12] = 0
    tiles[3][20] = 55
    tiles[5][9] = 7
    mirror[5][9] = True
    tiles[5][23] = 9
    tiles[4][14] = 36
    tiles[4][18] = 37
    tiles[7][13] = 38
    tiles[7][19] = 39

    # Houses and shops around the two roads.
    placements = {
        (6, 8): 34,
        (6, 24): 35,
        (10, 5): 49,
        (10, 27): 51,
        (16, 6): 52,
        (16, 26): 53,
        (20, 10): 57,
        (20, 22): 101,
        (9, 11): 15,
        (15, 22): 32,
    }
    for (y, x), tile in placements.items():
        tiles[y][x] = tile
    mirror[6][8] = True
    mirror[10][5] = True
    mirror[16][6] = True
    mirror[20][10] = True

    # Central village landmarks.
    tiles[12][16] = 100
    tiles[11][13] = 59
    tiles[11][19] = 65
    tiles[15][16] = 63
    tiles[18][16] = 80
    tiles[21][16] = 113

    # Trees, shrubs and decorative foliage around the village edge.
    for y, x in ((4, 5), (4, 27), (9, 2), (9, 29), (17, 3), (17, 29), (22, 5), (22, 27)):
        tiles[y][x] = 26
    shrub_tiles = (85, 88, 90, 97, 104)
    shrub_points = (
        (2, 5), (2, 8), (2, 24), (2, 27),
        (6, 3), (6, 29), (13, 3), (13, 29),
        (19, 4), (19, 28), (22, 8), (22, 24),
    )
    for index, (y, x) in enumerate(shrub_points):
        tiles[y][x] = shrub_tiles[index % len(shrub_tiles)]

    # Lantern line along the east-west road.
    lanterns = (40, 41, 42, 43, 44, 45)
    for index, x in enumerate((4, 8, 12, 20, 24, 28)):
        tiles[13][x] = lanterns[index]

    # A few flags establish districts without adding collision yet.
    for (y, x), tile in {
        (8, 3): 93,
        (8, 29): 96,
        (18, 8): 106,
        (18, 24): 111,
    }.items():
        tiles[y][x] = tile

    spec = {
        '_comment': (
            'Plausible Xianshi Village visual candidate assembled only from APK map 58 composites. '
            'Original map grid is unavailable; collision remains disabled for mobile layout testing.'
        ),
        'map_id': 58,
        'width': WIDTH,
        'height': HEIGHT,
        'map_type': 0,
        'tile_definitions': list(range(115)),
        'tiles': tiles,
        'collision': ['.' * WIDTH for _ in range(HEIGHT)],
        'mirror': [''.join('#' if value else '.' for value in row) for row in mirror],
    }
    output = Path(__file__).resolve().parents[1] / 'maps' / '58.xianshi-candidate.map.json'
    output.write_text(json.dumps(spec, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'wrote {output}')


if __name__ == '__main__':
    main()
