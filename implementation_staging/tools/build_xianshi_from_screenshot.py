from __future__ import annotations

import json
from pathlib import Path


WIDTH = 96
HEIGHT = 96
SPAWN_X = 63
SPAWN_Y = 67


def screen_position(x: int, y: int) -> tuple[int, int]:
    return 10 * (x - y), 5 * (x + y)


def main() -> None:
    tan = 69
    grass = 5
    tiles: list[list[int]] = []
    for y in range(HEIGHT):
        row: list[int] = []
        for x in range(WIDTH):
            # The screenshot changes from a large beige plaza to grass near
            # the observer. x+y maps directly to vertical screen position.
            row.append(tan if (x + y) <= 119 else grass)
        tiles.append(row)

    # Two diagonal gray roads through the grass area.
    road = (17, 20, 25)
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if (x + y) >= 116 and (abs(x - 63) <= 2 or abs(y - 67) <= 2):
                tiles[y][x] = road[(x + y) % len(road)]

    # Screen-aligned stone stages reconstructed from the screenshot. Using
    # projected u/v bounds produces rectangular platforms in the camera view.
    for y in range(HEIGHT):
        for x in range(WIDTH):
            u, v = screen_position(x, y)
            if abs(u + 50) <= 120 and abs(v - 410) <= 30:
                tiles[y][x] = 92
            if abs(u + 110) <= 78 and abs(v - 615) <= 28:
                tiles[y][x] = 92

    mirror = [[False for _ in range(WIDTH)] for _ in range(HEIGHT)]

    # Static landmarks measured from the screenshot around [63,67].
    landmarks = {
        (44, 39): 100,  # northern drum
        (67, 56): 113,  # central-left gong/drum substitute
        (65, 71): 100,  # eastern drum
        (81, 63): 26,   # large southern tree
        (84, 88): 105,  # decorative potted tree
    }
    for (y, x), tile in landmarks.items():
        tiles[y][x] = tile

    # Yellow-roof buildings are assembled along constant x+y, which is a
    # horizontal row in the isometric camera. The overlapping composites are
    # the same roof/end pieces visible in the APK atlas.
    def building(center_x: int, center_y: int, mirrored: bool = False) -> None:
        pieces = (34, 35, 35, 53)
        offsets = (-3, -1, 1, 3)
        for piece, offset in zip(pieces, offsets):
            x = center_x + offset
            y = center_y - offset
            tiles[y][x] = piece
            mirror[y][x] = mirrored

    building(46, 61, mirrored=True)
    building(57, 50)
    building(78, 82)
    tiles[62][43] = 93
    tiles[51][60] = 96

    # Raised flower beds visible in the north-east background.
    for y, x in ((31, 50), (33, 52), (35, 54), (38, 70), (40, 72)):
        tiles[y][x] = (85, 88, 90, 97, 104)[(x + y) % 5]
    for y, x in ((32, 48), (32, 56), (39, 68), (39, 76)):
        tiles[y][x] = 76

    # Flowers and low foliage around the lower grass, kept outside roads.
    for y, x in (
        (73, 48), (76, 51), (78, 57), (72, 75), (75, 78),
        (83, 55), (86, 60), (80, 86), (87, 82),
    ):
        tiles[y][x] = (85, 88, 90, 97, 104)[(x * 3 + y) % 5]

    # Sparse ground variations provide the small flowers visible in the grass
    # without turning the base into a checkerboard.
    for y, x in ((72, 54), (75, 58), (73, 72), (77, 76), (84, 68), (86, 74)):
        if tiles[y][x] == grass:
            tiles[y][x] = (10, 12, 13, 21, 22, 23)[(x + y) % 6]

    spec = {
        '_comment': (
            'Screenshot-derived reconstruction around the visible [63,67] region. '
            'Static placement is estimated from the client isometric projection; '
            'players, NPCs, text, portals and unseen areas are not present in the source image.'
        ),
        'reference_image': 'codex-clipboard-9aba704e-ecb0-4834-96ab-a49d5947cd97.png',
        'map_id': 58,
        'width': WIDTH,
        'height': HEIGHT,
        'map_type': 0,
        'recommended_spawn': [SPAWN_X, SPAWN_Y],
        'tile_definitions': list(range(115)),
        'tiles': tiles,
        'collision': ['.' * WIDTH for _ in range(HEIGHT)],
        'mirror': [''.join('#' if value else '.' for value in row) for row in mirror],
    }
    output = Path(__file__).resolve().parents[1] / 'maps' / '58.screenshot-replica.map.json'
    output.write_text(json.dumps(spec, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'wrote {output}')


if __name__ == '__main__':
    main()
