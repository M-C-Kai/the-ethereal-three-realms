from __future__ import annotations

import json
import struct
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any


class MapOError(ValueError):
    pass


@dataclass(frozen=True)
class MapRefInfo:
    composite_tile_count: int
    image_record_count: int
    image_ids: tuple[int, ...]
    consumed_bytes: int
    total_bytes: int


def inspect_map_ref(data: bytes) -> MapRefInfo:
    """Parse the record boundaries used by pmsj.work.b.m.C()."""
    if len(data) < 4:
        raise MapOError('map.ref is shorter than its four-byte header')
    composite_count, image_count = struct.unpack_from('>HH', data, 0)
    offset = 4
    image_ids: list[int] = []
    for index in range(image_count):
        if offset + 8 > len(data):
            raise MapOError(f'map.ref image record {index} is truncated')
        image_ids.append(struct.unpack_from('>I', data, offset)[0])
        offset += 8

    for index in range(composite_count):
        if offset + 5 > len(data):
            raise MapOError(f'map.ref composite tile {index} is truncated')
        flags = data[offset]
        child_count = data[offset + 4]
        offset += 5
        child_size = 2 if flags & 1 else 5
        required = child_count * child_size
        if offset + required > len(data):
            raise MapOError(f'map.ref composite tile {index} children are truncated')
        offset += required

    return MapRefInfo(
        composite_tile_count=composite_count,
        image_record_count=image_count,
        image_ids=tuple(image_ids),
        consumed_bytes=offset,
        total_bytes=len(data),
    )


def read_map_ref(path: Path | None = None, apk: Path | None = None, map_id: int = 58) -> tuple[bytes, str]:
    if (path is None) == (apk is None):
        raise MapOError('provide exactly one of map.ref path or APK path')
    if path is not None:
        return path.read_bytes(), str(path)
    assert apk is not None
    member = f'assets/res/map/{map_id}.map.ref'
    with zipfile.ZipFile(apk) as archive:
        try:
            return archive.read(member), f'{apk}!/{member}'
        except KeyError as exc:
            raise MapOError(f'APK does not contain {member}') from exc


def pack_bits(values: list[bool]) -> bytes:
    packed = bytearray((len(values) + 7) // 8)
    for index, value in enumerate(values):
        if value:
            packed[index // 8] |= 1 << (index % 8)
    return bytes(packed)


def unpack_bits(data: bytes, count: int) -> list[bool]:
    return [bool(data[index // 8] & (1 << (index % 8))) for index in range(count)]


def encode_tile_rle(values: list[int], sentinel: int = 255) -> bytes:
    """Encode the byte RLE consumed by m.a(byte[], int) for 1407 actions 3/4."""
    if not 0 <= sentinel <= 255:
        raise MapOError('RLE sentinel must fit an unsigned byte')
    raw = [value & 0xFF for value in values]
    encoded = bytearray([sentinel])
    index = 0
    while index < len(raw):
        value = raw[index]
        run = 1
        while index + run < len(raw) and raw[index + run] == value:
            run += 1
        remaining = run
        while remaining:
            chunk = min(remaining, 255)
            if value != sentinel and chunk <= 2:
                encoded.extend([value] * chunk)
            else:
                encoded.extend((sentinel, 0 if chunk == 255 else chunk, value))
            remaining -= chunk
        index += run
    return bytes(encoded)


def decode_tile_rle(data: bytes, expected_count: int) -> list[int]:
    if not data:
        raise MapOError('RLE data is empty')
    sentinel = data[0]
    decoded: list[int] = []
    index = 1
    while index < len(data):
        value = data[index]
        index += 1
        if value != sentinel:
            decoded.append(value)
            continue
        if index >= len(data):
            raise MapOError('RLE marker is missing its count')
        count = data[index]
        index += 1
        if count == sentinel:
            decoded.append(sentinel)
            continue
        if index >= len(data):
            raise MapOError('RLE run is missing its value')
        value = data[index]
        index += 1
        decoded.extend([value] * (255 if count == 0 else count))
        if len(decoded) > expected_count:
            raise MapOError('RLE expands beyond the configured map size')
    if len(decoded) != expected_count:
        raise MapOError(f'RLE expands to {len(decoded)} cells, expected {expected_count}')
    return decoded


def _parse_tile_grid(value: Any, width: int, height: int, default_tile: int) -> list[int]:
    if value is None:
        return [default_tile] * (width * height)
    if not isinstance(value, list) or len(value) != height:
        raise MapOError(f'tiles must contain exactly {height} rows')
    cells: list[int] = []
    for row_index, row in enumerate(value):
        if not isinstance(row, list) or len(row) != width:
            raise MapOError(f'tiles row {row_index} must contain exactly {width} cells')
        for cell in row:
            cells.append(-1 if cell is None else int(cell))
    return cells


def _parse_bool_grid(value: Any, width: int, height: int, name: str) -> list[bool]:
    if value is None:
        return [False] * (width * height)
    if not isinstance(value, list) or len(value) != height:
        raise MapOError(f'{name} must contain exactly {height} strings')
    result: list[bool] = []
    for row_index, row in enumerate(value):
        if not isinstance(row, str) or len(row) != width:
            raise MapOError(f'{name} row {row_index} must be a {width}-character string')
        invalid = set(row) - {'.', '#'}
        if invalid:
            raise MapOError(f'{name} row {row_index} contains invalid markers: {sorted(invalid)!r}')
        result.extend(character == '#' for character in row)
    return result


def _bool_rows(values: list[bool], width: int, height: int) -> list[str]:
    return [
        ''.join('#' if value else '.' for value in values[row * width:(row + 1) * width])
        for row in range(height)
    ]


@dataclass
class MapO:
    width: int
    height: int
    map_type: int
    tile_definitions: list[int]
    tiles: list[int]
    collision: list[bool]
    mirror: list[bool]
    tile_pixel_width: int = 20
    tile_pixel_height: int = 10

    def validate(self, ref: MapRefInfo | None = None) -> None:
        if not 1 <= self.width <= 127 or not 1 <= self.height <= 127:
            raise MapOError('the original client stores width and height as signed bytes (1..127)')
        if not 0 <= self.map_type <= 255:
            raise MapOError('map_type must be between 0 and 255')
        if not 1 <= self.tile_pixel_width <= 255 or not 1 <= self.tile_pixel_height <= 255:
            raise MapOError('tile pixel dimensions must be between 1 and 255')
        if not 1 <= len(self.tile_definitions) <= 128:
            raise MapOError('tile_definitions must contain 1..128 entries')
        if any(not -32768 <= value <= 32767 for value in self.tile_definitions):
            raise MapOError('tile definition references must fit signed 16-bit values')
        if ref is not None:
            invalid = [value for value in self.tile_definitions if not 0 <= value < ref.composite_tile_count]
            if invalid:
                raise MapOError(
                    f'tile definition references outside map.ref composite range '
                    f'0..{ref.composite_tile_count - 1}: {invalid}'
                )
        cell_count = self.width * self.height
        for name, values in (('tiles', self.tiles), ('collision', self.collision), ('mirror', self.mirror)):
            if len(values) != cell_count:
                raise MapOError(f'{name} has {len(values)} cells, expected {cell_count}')
        for value in self.tiles:
            if value != -1 and not 0 <= value < len(self.tile_definitions):
                raise MapOError(
                    f'tile grid value {value} is not -1 and is outside definition range '
                    f'0..{len(self.tile_definitions) - 1}'
                )

    @classmethod
    def from_spec(cls, spec: dict[str, Any]) -> 'MapO':
        width = int(spec['width'])
        height = int(spec['height'])
        definitions = [int(value) for value in spec.get('tile_definitions', [0])]
        default_tile = int(spec.get('default_tile', 0))
        result = cls(
            width=width,
            height=height,
            map_type=int(spec.get('map_type', 0)),
            tile_definitions=definitions,
            tiles=_parse_tile_grid(spec.get('tiles'), width, height, default_tile),
            collision=_parse_bool_grid(spec.get('collision'), width, height, 'collision'),
            mirror=_parse_bool_grid(spec.get('mirror'), width, height, 'mirror'),
            tile_pixel_width=int(spec.get('tile_pixel_width', 20)),
            tile_pixel_height=int(spec.get('tile_pixel_height', 10)),
        )
        result.validate()
        return result

    @classmethod
    def from_file(cls, data: bytes) -> 'MapO':
        if not data:
            raise MapOError('.map.o file is empty')
        definition_count = data[0]
        if definition_count == 0:
            raise MapOError('.map.o definition count is zero')
        definition_end = 1 + (definition_count * 2)
        if len(data) < definition_end + 5:
            raise MapOError('.map.o header is truncated')
        definitions = list(struct.unpack_from(f'>{definition_count}h', data, 1))
        map_type, width, height, tile_pixel_width, tile_pixel_height = data[definition_end:definition_end + 5]
        cell_count = width * height
        mask_size = (cell_count + 7) // 8
        expected_size = definition_end + 5 + cell_count + (mask_size * 2)
        if len(data) != expected_size:
            raise MapOError(
                f'.map.o has {len(data)} bytes; its embedded dimensions require {expected_size}. '
                'The five skipped bytes may follow another convention.'
            )
        offset = definition_end + 5
        raw_tiles = data[offset:offset + cell_count]
        offset += cell_count
        collision = unpack_bits(data[offset:offset + mask_size], cell_count)
        offset += mask_size
        mirror = unpack_bits(data[offset:offset + mask_size], cell_count)
        result = cls(
            width=width,
            height=height,
            map_type=map_type,
            tile_definitions=definitions,
            tiles=[-1 if value == 255 else value for value in raw_tiles],
            collision=collision,
            mirror=mirror,
            tile_pixel_width=tile_pixel_width,
            tile_pixel_height=tile_pixel_height,
        )
        result.validate()
        return result

    def to_file(self) -> bytes:
        self.validate()
        header = bytes((len(self.tile_definitions),))
        definitions = struct.pack(f'>{len(self.tile_definitions)}h', *self.tile_definitions)
        # The APK reader skips these five bytes because the server has already
        # supplied the first three through 1407/0. Original map 58 stores the
        # same map metadata followed by the client's 20x10 isometric tile size.
        compatibility_header = bytes((
            self.map_type,
            self.width,
            self.height,
            self.tile_pixel_width,
            self.tile_pixel_height,
        ))
        grid = bytes(value & 0xFF for value in self.tiles)
        return header + definitions + compatibility_header + grid + pack_bits(self.collision) + pack_bits(self.mirror)

    def to_spec(self) -> dict[str, Any]:
        return {
            'width': self.width,
            'height': self.height,
            'map_type': self.map_type,
            'tile_pixel_width': self.tile_pixel_width,
            'tile_pixel_height': self.tile_pixel_height,
            'tile_definitions': self.tile_definitions,
            'tiles': [
                [None if value == -1 else value for value in self.tiles[row * self.width:(row + 1) * self.width]]
                for row in range(self.height)
            ],
            'collision': _bool_rows(self.collision, self.width, self.height),
            'mirror': _bool_rows(self.mirror, self.width, self.height),
        }

    def to_1407_sections(self) -> dict[str, bytes | int]:
        self.validate()
        return {
            'map_type': self.map_type,
            'width': self.width,
            'height': self.height,
            'definitions': struct.pack(f'>{len(self.tile_definitions)}h', *self.tile_definitions),
            'tiles_rle': encode_tile_rle(self.tiles),
            'collision': pack_bits(self.collision),
            'mirror': pack_bits(self.mirror),
        }


def load_spec(path: Path) -> dict[str, Any]:
    loaded = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(loaded, dict):
        raise MapOError('map specification root must be a JSON object')
    return loaded
from protocol import Field, TYPE_BYTE, TYPE_INT, byte, decode_frame, encode_frame, field_values, integer


def is_map_pathfind_request(fields: list[Field]) -> bool:
    return bool(
        len(fields) == 4
        and fields[0].type_id == TYPE_BYTE and fields[0].value == 0
        and fields[1].type_id == TYPE_INT
        and fields[2].type_id == TYPE_BYTE
        and fields[3].type_id == TYPE_BYTE
    )


def map_pathfind_frame(map_id: int, x: int, y: int) -> bytes:
    return encode_frame(1145, [
        byte(0), integer(1), integer(int(map_id)), integer(int(x)), integer(int(y)),
        integer(0),
    ])

from protocol import short, string
from systems.map.registry import MapActorDefinition, MapDefinition, PortalDefinition

NPC_DIRECTION_DOWN = 0
NPC_DIRECTION_RIGHT = 1
NPC_DIRECTION_UP = 2
NPC_DIRECTION_LEFT = 3
_DIRECTION_RANGE = (NPC_DIRECTION_DOWN, NPC_DIRECTION_RIGHT, NPC_DIRECTION_UP, NPC_DIRECTION_LEFT)
NPC_STREAM_RADIUS = 20
_MAP_PATH_DELTAS = {
    0: (0, 1), 1: (-1, 1), 2: (-1, 0), 3: (-1, -1),
    4: (0, -1), 5: (1, -1), 6: (1, 0), 7: (1, 1), 8: (0, 0),
}

def map_action(
    definition: MapDefinition,
    action: int,
    status: int = 0,
    role_id: int | None = None,
) -> bytes:
    # 游戏端读取 1010 应答时固定从字段 5 取动作码。
    return encode_frame(1010, [
        integer(10001 if role_id is None else role_id),
        short(definition.spawn_x),
        short(definition.spawn_y),
        integer(0),
        integer(status),
        # 客户端在 1010 响应中用 w.b(5) 读取动作码，必须是 short。
        short(action),
    ])


# 1126 subtype=1 (local-compat extension) sets the facing of an existing generic
# map actor (pmsj.work.b/n) in place.  The client looks the actor up by id in the
# same container that 1126 subtype=0 used (b/m.u), then calls b/n.q(direction) and
# b/n.I().  Facing values match the APK's b/n.n byte (four cardinal directions).
NPC_DIRECTION_DOWN = 0
NPC_DIRECTION_RIGHT = 1
NPC_DIRECTION_UP = 2
NPC_DIRECTION_LEFT = 3

_DIRECTION_RANGE = (NPC_DIRECTION_DOWN, NPC_DIRECTION_RIGHT, NPC_DIRECTION_UP, NPC_DIRECTION_LEFT)
NPC_STREAM_RADIUS = 20
SECT_MENTOR_LEARN_OPTION = 1

# 1005 path directions are produced by APK a/c/x.a(x1, y1, x2, y2).
_MAP_PATH_DELTAS = {
    0: (0, 1),
    1: (-1, 1),
    2: (-1, 0),
    3: (-1, -1),
    4: (0, -1),
    5: (1, -1),
    6: (1, 0),
    7: (1, 1),
    8: (0, 0),
}



def map_movement_final_tile(values: list[object]) -> tuple[int, int]:
    """Decode the final tile from the APK's compact 1005 movement path."""
    if len(values) < 2:
        raise ValueError('map movement requires a starting tile')
    x, y = int(values[0]), int(values[1])
    step_count = min(max(0, int(values[2])) if len(values) > 2 else 0, max(0, len(values) - 3))
    for raw_direction in values[3:3 + step_count]:
        direction = int(raw_direction)
        try:
            dx, dy = _MAP_PATH_DELTAS[direction]
        except KeyError as exc:
            raise ValueError(f'unsupported map movement direction {direction}') from exc
        x += dx
        y += dy
    return x, y



def map_actor_direction_frame(object_id: int, direction: int) -> bytes:
    """Return a 1126 subtype=1 frame setting one actor's facing in place.

    Strict wire format: [byte(1), byte(1), integer(object_id), byte(direction)].
    The client never moves, recreates, or renames the actor -- it only calls
    b/n.q(direction) then b/n.I() on the existing entity.
    """
    if direction not in _DIRECTION_RANGE:
        raise ValueError(f'NPC direction must be 0..3, got {direction}')
    return encode_frame(1126, [
        byte(1),
        byte(1),
        integer(int(object_id)),
        byte(direction),
    ])



def map_actor_selection_frame(object_id: int) -> bytes:
    """Select one generic actor through the local APK compatibility branch.

    The patched client resolves the id in the same generic actor container used
    by subtype=0 and assigns it as the current target. The original entity
    renderer then draws its bundled 0x203230 selection ring beneath the actor.
    """
    return encode_frame(1126, [
        byte(2),
        integer(int(object_id)),
    ])



def map_actor_directions_frame(items: list[tuple[int, int]]) -> bytes:
    """Batch form of map_actor_direction_frame.

    Wire format: [byte(1), byte(count), integer(id1), byte(dir1), ...].
    """
    if not items:
        raise ValueError('direction frame requires at least one actor')
    encoded = [byte(1), byte(len(items))]
    for object_id, direction in items:
        if direction not in _DIRECTION_RANGE:
            raise ValueError(f'NPC direction must be 0..3, got {direction}')
        encoded.append(integer(int(object_id)))
        encoded.append(byte(direction))
    return encode_frame(1126, encoded)



def map_monster_frame(definition: MapDefinition) -> bytes:
    """Return the verified 1126 actor-spawn frame for local monsters.

    ``pmsj.work.main.e.Q`` decodes subtype 0 as a list of generic map actors:
    field 0 is the subtype, field 1 the count, then each record contains
    id/x/y/raw-model/name.  The client adds 0x200b20 to raw-model before
    loading the sprite resource.
    """
    if not definition.monsters:
        raise ValueError(f'map {definition.id} has no monster')
    fields = [
        byte(0),
        byte(len(definition.monsters)),
    ]
    for monster in definition.monsters:
        fields.extend((
            integer(monster.id),
            integer(monster.x),
            integer(monster.y),
            integer(monster.model),
            string(monster.name),
        ))
    return encode_frame(1126, fields)


# 同图在线角色的通用对象 id 基数。1010/action=18 只对 [1_000_000, 499_999_999]
# 的 id 走 b/m.p 通用移除（pmsj.work.main/e.smali），role_id 从 10001 递增，
# 1_000_000 + role_id 同时避开了怪物 1_900_001+ 与传送点 580_001 区段。
PLAYER_ACTOR_ID_BASE = 1_000_000


def player_actor_object_id(role_id: int) -> int:
    """Generic-actor id for an online role (despawnable via 1010/action=18).

    The id must ALSO stay outside [699_233, 798_975] so the APK 1005 handler
    routes it to the b/v player branch (m.n lookup) instead of the q branch,
    and inside [1_000_000, 499_999_999] so 1010/action=18 reaches b/m.p —
    both hold for every role_id below 900_000.
    """
    return PLAYER_ACTOR_ID_BASE + int(role_id)



def map_monster_for_object_id(
    definition: MapDefinition,
    object_id: int,
) -> MapActorDefinition | None:
    """Resolve any configured monster instead of only the legacy first one."""
    wanted = int(object_id)
    return next((monster for monster in definition.monsters if monster.id == wanted), None)



def map_portal_frame(portal: PortalDefinition) -> bytes:
    """Return the verified 1126 generic-actor shape for the test portal."""
    return encode_frame(1126, [
        byte(0),
        byte(1),
        integer(portal.id),
        integer(portal.x),
        integer(portal.y),
        # Reuse the known-good local actor sprite.  The important part of the
        # portal is its actor id/position; no new client resource is required.
        integer(portal.model),
        string(portal.name),
    ])



def map_portal_frames(definition: MapDefinition) -> list[bytes]:
    """Spawn every portal registered for one map, in configuration order."""
    return [map_portal_frame(portal) for portal in definition.portals]



def map_return_portal_frame(definition: MapDefinition) -> bytes:
    """Compatibility helper for the first portal on a return map."""
    try:
        portal = definition.portals[0]
    except IndexError as exc:
        raise ValueError(f'map {definition.id} has no return portal') from exc
    return map_portal_frame(portal)



def map_npc_frame(definition: MapDefinition, npc: MapActorDefinition) -> bytes:
    """Spawn one map NPC through the client's native 2030 NPC path.

    ``main/e.X`` constructs ``pmsj.work.b/t`` from this record.  Unlike the
    generic 1126 actor, that class participates in the map's built-in target
    selection, draws the bundled selection ring, and supplies the portrait and
    title used by the native NPC dialogue overlay.

    The roaming-Boss effect carrier (dat_id 3000100) is an invisible body:
    integer field 5 becomes the attached-display code 3000000 (resource
    3000000, animation index 0) and field 7 bit 1 routes the actor into the
    map manager's W vector -- merged into the render list but omitted from
    ``m.l(x, y)`` hit-testing, so the ring stays visible without adding a
    clickable NPC target over the Boss.
    """
    if int(getattr(npc, 'dat_id', 0)) == BOSS_EFFECT_CARRIER_DAT_ID:
        return encode_frame(2030, [
            integer(npc.id),
            integer(npc.x),
            integer(npc.y),
            integer(npc.dat_id),
            integer(npc.direction),
            integer(BOSS_EFFECT_RESOURCE_ID),
            string(npc.name),
            integer(2),
            string(npc.label),
        ])
    return encode_frame(2030, [
        integer(npc.id),
        integer(npc.x),
        integer(npc.y),
        integer(npc.dat_id),
        integer(npc.direction),
        integer(0),
        string(npc.name),
        integer(0),
        string(npc.label),
    ])



def map_npc_frames(definition: MapDefinition) -> list[bytes]:
    """Return native NPC spawn frames for the current map definition."""
    return [map_npc_frame(definition, npc) for npc in definition.npcs]



def map_npcs_near(definition: MapDefinition, x: int, y: int) -> list[MapActorDefinition]:
    """Return NPCs retained by the client's native 20-tile stream window."""
    return [
        npc for npc in definition.npcs
        if abs(npc.x - int(x)) <= NPC_STREAM_RADIUS
        and abs(npc.y - int(y)) <= NPC_STREAM_RADIUS
    ]



def map_npc_for_object_id(
    definition: MapDefinition,
    object_id: int,
) -> MapActorDefinition | None:
    """Return the current map's NPC matching a clicked actor id."""
    return next(
        (npc for npc in definition.npcs if npc.id == int(object_id)),
        None,
    )



def map_auto_grind_start_frame() -> bytes:
    """1010 action is SHORT field 5 in APK main/e (not C->S field 0).

    Action 280 reads no other fields; unused header fields stay zero.
    The APK records the current tile as its client-side roaming origin.
    """
    return encode_frame(1010, [
        integer(0), short(0), short(0), integer(0), integer(0), short(280),
    ])


def map_object_remove_frame(object_id: int) -> bytes:
    """Remove a generic 1126 actor via verified ``1010/action=18``.

    ``main/e`` dispatches protocol 1010 using short field 5. Action 18 reads
    the actor id from integer field 0 and removes ids >= 1_000_000 from the
    generic-actor container. It is not a standalone protocol number 18.
    """
    return encode_frame(1010, [
        integer(object_id),
        short(0),
        short(0),
        integer(0),
        integer(0),
        short(18),
    ])



def map_object_interaction_ack_frame(object_id: int) -> bytes:
    """Release the APK wait overlay after suppressing a 1010/action=7 re-tap.

    The inbound 1010 dispatcher clears its wait flags before checking action
    field 5. Action 7 has no inbound map mutation branch, so this complete
    six-field record acknowledges the interaction without moving or removing
    the actor.
    """
    return encode_frame(1010, [
        integer(object_id),
        short(0),
        short(0),
        integer(0),
        integer(0),
        short(7),
    ])



def map_object_interaction_values(values: list[object]) -> tuple[int, int | None, int | None, int | None]:
    """Decode the active APK's 2031 map-object request.

    ``main/e.a(IISS)`` writes ``[object_id, 0, x, y, action, 0]``.  Keep
    the optional fields tolerant because older builds omit the trailing
    values when an actor has no interaction metadata.
    """
    if not values:
        raise ValueError('map object interaction requires an object id')
    object_id = int(values[0])
    object_x = int(values[2]) if len(values) > 2 else None
    object_y = int(values[3]) if len(values) > 3 else None
    action = int(values[4]) if len(values) > 4 else None
    return object_id, object_x, object_y, action

import logging
from protocol import binary

LOG = logging.getLogger(__name__)

def map_data_frames(definition: MapDefinition, role_id: int | None = None) -> list[bytes]:
    configured = Path(definition.map_o_file)
    map_path = configured if configured.is_absolute() else Path(__file__).resolve().parents[2] / configured
    try:
        generated = MapO.from_file(map_path.read_bytes())
    except (OSError, MapOError) as exc:
        LOG.warning('cannot load generated map %s; using flat fallback: %s', map_path, exc)
        width = definition.fallback_width
        height = definition.fallback_height
        generated = MapO(
            width=width,
            height=height,
            map_type=0,
            tile_definitions=[0],
            tiles=[0] * (width * height),
            collision=[False] * (width * height),
            mirror=[False] * (width * height),
        )
    sections = generated.to_1407_sections()
    map_type = int(sections['map_type'])
    width = int(sections['width'])
    height = int(sections['height'])
    tile_definitions = sections['definitions']
    encoded_tiles = sections['tiles_rle']
    collision = sections['collision']
    mirror = sections['mirror']
    assert isinstance(tile_definitions, bytes)
    assert isinstance(encoded_tiles, bytes)
    assert isinstance(collision, bytes)
    assert isinstance(mirror, bytes)

    return [
        map_action(definition, 11, role_id=role_id),
        encode_frame(1407, [byte(0), byte(map_type), byte(width), byte(height)]),
        encode_frame(1407, [byte(1), short(len(tile_definitions)), binary(tile_definitions)]),
        encode_frame(1407, [byte(3), short(len(encoded_tiles)), binary(encoded_tiles)]),
        encode_frame(1407, [byte(5), short(len(collision)), binary(collision)]),
        encode_frame(1407, [byte(7), short(len(mirror)), binary(mirror)]),
        # status=1 skips the APK-local map.o lookup; 1407 still supplies the
        # authoritative logical map data used by the server transition.
        map_action(definition, 12, status=1, role_id=role_id),
    ]



def map_enter_frames(definition: MapDefinition, role_id: int | None = None) -> list[bytes]:
    # Distinct drawable map ids must carry matching APK-local map.ref/map.o
    # resources.  status=0 asks the client to load those resources before it
    # acknowledges entry; status=1 is reserved for definitions without them.
    ref_status = 0 if definition.map_ref_available else 1
    frames = [
        map_action(definition, 13, status=ref_status, role_id=role_id),
        map_action(definition, 14, role_id=role_id),
        map_action(definition, 105, role_id=role_id),
    ]
    if definition.monsters:
        frames.append(map_monster_frame(definition))
    frames.extend(map_portal_frames(definition))
    frames.extend(map_npc_frames(definition))
    # After every 1126 subtype=0 actor is created, set their initial facing with
    # 1126 subtype=1 (local-compat extension): the client finds the actor by id in
    # the same generic container and rotates it in place.  The direction frame is
    # never appended to the subtype=0 record (that would break its fixed field read).
    if definition.monsters:
        frames.append(map_actor_directions_frame([
            (monster.id, monster.direction)
            for monster in definition.monsters
        ]))
    frames.extend(
        map_actor_direction_frame(portal.id, portal.direction)
        for portal in definition.portals
    )
    return frames


SECT_MENTOR_LEARN_OPTION = 1

def map_npc_dialogue_frames(
    npc: MapActorDefinition,
    role: dict[str, object] | None,
    settings,
) -> list[bytes]:
    """Open the compact map-overlay NPC dialogue used by the original client.

    Protocol 2032 opens screen 6 (``pmsj.work.e.cb`` / ``6.ui``).  Its records
    are eight fields wide: type 1 supplies the wrapped introduction text, type
    2 supplies an option row, and type 100 finalizes layout after resolving the
    native 2030 NPC by id for its title and portrait.
    """
    from systems.map.service import settings_for_role  # 局部导入避免 service<->protocol 循环
    from systems.role.service import normalized_sect_id
    npc_id = npc.id
    is_sect_mentor = npc.service == 'sect_skill_mentor' and npc.sect_id is not None
    sect_matches = (
        is_sect_mentor
        and role is not None
        and normalized_sect_id(role, settings.sect_registry) == npc.sect_id
    )
    if is_sect_mentor and not sect_matches:
        sect = settings.sect_registry.sect(npc.sect_id)
        sect_name = sect.name if sect is not None else "本门"
        introduction = f'仅限{sect_name}弟子学习。'
    else:
        introduction = npc.introduction or npc.label or npc.name

    def dialogue_record(kind: int, *, option_id: int = 0, text: str = '', icon: int = 0) -> list[Field]:
        return [
            integer(0),
            integer(0),
            integer(0),
            short(0),
            integer(option_id),
            byte(kind),
            string(text),
            integer(icon),
        ]

    records = [*dialogue_record(1, text=introduction)]
    if sect_matches:
        records.extend(dialogue_record(
            2,
            option_id=SECT_MENTOR_LEARN_OPTION,
            text='学习门派技能',
        ))
    records.extend(dialogue_record(2, option_id=0, text='结束对话'))
    records.extend(dialogue_record(100))
    return [encode_frame(2032, [
        integer(npc_id),
        byte(len(records) // 8),
        *records,
    ])]



def sect_skill_screen_frame(mode: int = 1) -> bytes:
    """Open external screen 179, remapped by the APK to sect screen 602.

    ``main/e`` dispatches the generic UI action from short field 5, reads the
    external screen id from integer field 4 and the mode from integer field 3.
    It maps external id 0xb3 to 0x25a; mode 1 is the mentor learning variant
    rather than the remote view variant.
    """
    return encode_frame(1010, [
        integer(0),
        short(0),
        short(0),
        integer(mode),
        integer(179),
        short(69),
    ])



def npc_dialogue_option_frames(
    settings,
    role: dict[str, object] | None,
    state,
    option_id: int,
    input_text: str = '',
) -> list[bytes]:
    """Acknowledge one 2032 option and open mentor mode only if still valid."""
    from systems.map.service import settings_for_role  # 局部导入避免 service<->protocol 循环
    from systems.role.service import normalized_sect_id
    frames = [map_object_interaction_ack_frame(0)]
    try:
        if role is None or int(option_id) != SECT_MENTOR_LEARN_OPTION:
            return frames
        try:
            definition = settings_for_role(settings, role)
        except ValueError:
            return frames
        if state.map_id != definition.id or state.npc_id is None:
            return frames
        npc = map_npc_for_object_id(definition, state.npc_id)
        if (
            npc is None
            or npc.service != 'sect_skill_mentor'
            or npc.sect_id is None
            or normalized_sect_id(role, settings.sect_registry) != npc.sect_id
        ):
            return frames
        frames.append(sect_skill_screen_frame(1))
        return frames
    finally:
        state.clear()

# ---------------------------------------------------------------------------
# 世界初始化帧（自 server.py 迁入）。
# ---------------------------------------------------------------------------
from protocol import byte, encode_frame, integer, string
from systems.role.service import default_role

def notice_and_world(settings: Settings, role: dict[str, object] | None = None) -> list[bytes]:
    role = role if role is not None else default_role(settings)
    from systems.map.service import settings_for_role  # 局部导入避免 service<->protocol 循环
    current_map = settings_for_role(settings, role)
    notice = encode_frame(1123, [byte(0), integer(0), string('本地服务正常')])
    # APK main/e stores 1110 as logical map id (field 0), resource map id
    # (field 1), map flags (field 2), and map name (field 3). Task screens
    # compare m.q() (field 0) to route map id before same-map local pathing.
    client_map_id = current_map.id
    world = encode_frame(1110, [
        integer(client_map_id),
        integer(client_map_id),
        integer(0),
        string(current_map.name),
    ])
    return [notice, world]

# ---------------------------------------------------------------------------
# 动态地图与巡逻 Boss 协议（自 server_dynamic_maps.py / server_pets.py 收编）。
# ---------------------------------------------------------------------------
MAP_REF_CHUNK_SIZE = 12_000
MAX_MAP_REF_TRANSFER_SIZE = 0x7FFF
BOSS_EFFECT_CARRIER_DAT_ID = 3_000_100
BOSS_EFFECT_RESOURCE_ID = 3_000_000
ROAMING_BOSS_MAP_ID = 58
ROAMING_BOSS_ID = 700_001
ROAMING_BOSS_MODEL_OFFSET = 2_100_000
ROAMING_BOSS_EFFECT_MASK = 0x800000
ROAMING_BOSS_MOVE_DELAY_SECONDS = 3.0
ROAMING_BOSS_TARGET_X = 12
ROAMING_BOSS_TARGET_Y = 28


def map_ref_path(map_id: int) -> Path:
    """Return the server-side map.ref path for one logical map id."""
    return Path(__file__).resolve().parents[2] / 'maps' / f'{int(map_id)}.map.ref'


def map_ref_transfer_frames(definition, *, chunk_size: int = MAP_REF_CHUNK_SIZE) -> list[bytes]:
    """Encode one server-side .map.ref as APK-native 1407/11+12 chunks.

    Reverse-engineered APK path:
      1407 subtype 11/12 -> pmsj.work.b.m.a(short total, short offset, byte[])
      -> m.z byte buffer -> m.C() map.ref parser.

    Wire fields are [byte subtype, short total_size, binary chunk, short offset].
    The first chunk uses subtype 11 and continuations use subtype 12. The APK
    stores total length and offset as signed Java shorts, so this compatibility
    path deliberately rejects resources above 32767 bytes rather than silently
    wrapping their offsets.
    """
    if chunk_size <= 0:
        raise ValueError('map.ref chunk size must be positive')

    path = map_ref_path(definition.id)
    if not path.is_file():
        return []

    data = path.read_bytes()
    total = len(data)
    if total <= 0:
        raise ValueError(f'map.ref is empty: {path}')
    if total > MAX_MAP_REF_TRANSFER_SIZE:
        raise ValueError(
            f'map.ref {path} is {total} bytes; APK 1407 map.ref transfer '
            f'uses signed short length/offset and supports at most {MAX_MAP_REF_TRANSFER_SIZE}'
        )

    frames: list[bytes] = []
    for offset in range(0, total, chunk_size):
        chunk = data[offset:offset + chunk_size]
        subtype = 11 if offset == 0 else 12
        frames.append(encode_frame(1407, [
            byte(subtype),
            short(total),
            binary(chunk),
            short(offset),
        ]))
    return frames


def roaming_boss_spawn_frame(definition) -> bytes:
    """Create the map-58 Boss through APK-native 2028 / ``b/q``.

    The old 1126 path adds 2,100,000 to the configured raw model before
    creating ``b/n``.  Protocol 2028 creates ``b/q`` directly from field 3, so
    preserve the same visible resource by applying that offset server-side.
    Fields 1/2 are map coordinates; ``W(w)`` stores them as actor properties
    and immediately seeds the q actor position from those properties.

    q.p() reads property 4 as the actor display/interaction name. Keep it as a
    STRING: sending an INT placeholder leaves the roaming actor without the
    metadata used by the native map-object interaction path. Property 6 is the
    q effect mask; bit 0x800000 calls ``q.c(40000, true)`` so the ring remains
    attached to the moving actor itself.
    """
    monster = getattr(definition, 'monster', None)
    if monster is None:
        raise ValueError('roaming Boss requires a map monster definition')
    resource_id = int(monster.model) + ROAMING_BOSS_MODEL_OFFSET
    return encode_frame(2028, [
        integer(int(monster.id)),
        short(int(monster.x)),
        short(int(monster.y)),
        integer(resource_id),
        string(str(monster.name)),
        integer(0),
        integer(ROAMING_BOSS_EFFECT_MASK),
    ])


def roaming_boss_move_frame(
    actor_id: int,
    source_x: int,
    source_y: int,
    target_x: int,
    target_y: int,
) -> bytes:
    """Encode one native 1005 map movement update for a q actor.

    APK 1005 reads actor id from field 0 and target x/y from short fields 3/4.
    Fields 1/2 are retained as short source coordinates; the q branch does not
    read them, but keeping the coordinate-shaped five-field record mirrors the
    native movement packet without inventing a new protocol.
    """
    return encode_frame(1005, [
        integer(int(actor_id)),
        short(int(source_x)),
        short(int(source_y)),
        short(int(target_x)),
        short(int(target_y)),
    ])


def map_actor_move_frame(
    actor_id: int,
    source_x: int,
    source_y: int,
    target_x: int,
    target_y: int,
) -> bytes:
    """Native 1005 walk update for any generic ``q`` actor (online roles too).

    Same verified shape as ``roaming_boss_move_frame``; kept as a separate
    name so call sites for player movement do not read as Boss-specific.
    """
    return roaming_boss_move_frame(actor_id, source_x, source_y, target_x, target_y)


def is_roaming_boss_definition(definition) -> bool:
    """True for the map-58 roaming Boss encounter definition."""
    monster = getattr(definition, 'monster', None)
    return (
        int(getattr(definition, 'id', 0)) == ROAMING_BOSS_MAP_ID
        and monster is not None
        and int(getattr(monster, 'id', 0)) == ROAMING_BOSS_ID
    )


def _replace_roaming_boss_spawn(definition, frames: list[bytes]) -> list[bytes]:
    """Replace only map 58's generic 1126 Boss record with native 2028/q."""
    if not is_roaming_boss_definition(definition):
        return frames

    result: list[bytes] = []
    replaced = False
    for frame in frames:
        try:
            message_id, fields = decode_frame(frame)
            values = field_values(fields)
        except Exception:
            result.append(frame)
            continue
        if (
            not replaced
            and message_id == 1126
            and len(values) >= 3
            and int(values[2]) == ROAMING_BOSS_ID
        ):
            result.append(roaming_boss_spawn_frame(definition))
            replaced = True
        else:
            result.append(frame)
    return result


def dynamic_map_enter_frames(definition, role_id: int | None = None) -> list[bytes]:
    """Prefer server-delivered map.ref and use native q actor for the map-58 Boss."""
    original = _replace_roaming_boss_spawn(
        definition,
        list(map_enter_frames(definition, role_id)),
    )
    transfer = map_ref_transfer_frames(definition)
    if not transfer:
        return original

    if not original:
        raise ValueError(f'map {definition.id} produced no enter frames')

    # Phone-verified order: action 13 must establish the native transition
    # state before 1407/11+12 causes m.C() to parse the target map.ref.
    transition_start = map_action(
        definition,
        13,
        status=1,
        role_id=role_id,
    )
    continuation = original[1:]
    path = map_ref_path(definition.id)
    LOG.info(
        'MAP_REF_STREAM map=%d path=%s bytes=%d chunks=%d '
        'protocol=1010/13->1407/11+12->1010/14+105',
        int(definition.id),
        path,
        path.stat().st_size,
        len(transfer),
    )
    return [transition_start, *transfer, *continuation]
