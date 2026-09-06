from __future__ import annotations

import json
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any


NPC_APPEARANCE_MODEL_OFFSET = 2_100_000
NPC_APPEARANCE_GALLERY_ID_BASE = 1_950_000
NPC_APPEARANCE_GALLERY_X = tuple(range(8, 79, 10))
NPC_APPEARANCE_GALLERY_Y = tuple(range(10, 61, 10))


@dataclass(frozen=True)
class PortalDefinition:
    id: int
    name: str
    model: int
    x: int
    y: int
    direction: int
    target_map_id: int
    target_x: int
    target_y: int


@dataclass(frozen=True)
class MapActorDefinition:
    id: int
    name: str
    model: int
    x: int
    y: int
    direction: int = 0
    label: str = ''
    dat_id: int = 0
    introduction: str = ''
    service: str = ''
    sect_id: int | None = None


@dataclass(frozen=True)
class MapDefinition:
    id: int
    name: str
    map_o_file: str
    map_ref_available: bool
    fallback_width: int
    fallback_height: int
    spawn_x: int
    spawn_y: int
    monster: MapActorDefinition | None
    npcs: tuple[MapActorDefinition, ...]
    portals: tuple[PortalDefinition, ...]

    def with_spawn(self, x: int, y: int) -> 'MapDefinition':
        return replace(self, spawn_x=int(x), spawn_y=int(y))


@dataclass(frozen=True)
class MapRegistry:
    default_map_id: int
    maps: dict[int, MapDefinition]

    def require(self, map_id: int) -> MapDefinition:
        try:
            return self.maps[int(map_id)]
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError(f'unknown map id {map_id}') from exc

    def portal(self, map_id: int, object_id: int) -> PortalDefinition | None:
        wanted = int(object_id)
        return next((item for item in self.require(map_id).portals if item.id == wanted), None)


def _actor(payload: dict[str, Any]) -> MapActorDefinition:
    raw_sect_id = payload.get('sect_id')
    return MapActorDefinition(
        id=int(payload['id']),
        name=str(payload['name']),
        model=int(payload.get('model', 0)),
        x=int(payload['x']),
        y=int(payload['y']),
        direction=int(payload.get('direction', 0)),
        label=str(payload.get('label', '')),
        dat_id=int(payload.get('dat_id', 0)),
        introduction=str(payload.get('introduction', '')),
        service=str(payload.get('service', '')),
        sect_id=None if raw_sect_id is None else int(raw_sect_id),
    )


def _portal(payload: dict[str, Any]) -> PortalDefinition:
    return PortalDefinition(
        id=int(payload['id']),
        name=str(payload['name']),
        model=int(payload['model']),
        x=int(payload['x']),
        y=int(payload['y']),
        direction=int(payload.get('direction', 0)),
        target_map_id=int(payload['target_map_id']),
        target_x=int(payload['target_x']),
        target_y=int(payload['target_y']),
    )


def _map_definition(map_id: int, payload: dict[str, Any]) -> MapDefinition:
    spawn = payload['spawn']
    monster_payload = payload.get('monster')
    return MapDefinition(
        id=int(payload.get('id', map_id)),
        name=str(payload['name']),
        map_o_file=str(payload['map_o_file']),
        map_ref_available=bool(payload.get('map_ref_available', True)),
        fallback_width=int(payload['fallback_width']),
        fallback_height=int(payload['fallback_height']),
        spawn_x=int(spawn['x']),
        spawn_y=int(spawn['y']),
        monster=_actor(monster_payload) if isinstance(monster_payload, dict) else None,
        npcs=tuple(_actor(item) for item in payload.get('npcs', [])),
        portals=tuple(_portal(item) for item in payload.get('portals', [])),
    )


def _legacy_registry_payload(payload: dict[str, Any]) -> dict[str, Any]:
    source_map_id = int(payload.get('map_id', 58))
    target_map_id = int(payload.get('portal_target_map_id', 50000))
    source_spawn = {
        'x': int(payload.get('spawn_x', 60)),
        'y': int(payload.get('spawn_y', 67)),
    }
    target_spawn = {
        'x': int(payload.get('portal_target_spawn_x', 8)),
        'y': int(payload.get('portal_target_spawn_y', 6)),
    }
    monster_model = int(payload.get('monster_model', 3_760_000))
    source_portals: list[dict[str, Any]] = []
    if bool(payload.get('portal_enabled', False)):
        raw_portals = payload.get('portals')
        if not isinstance(raw_portals, list) or not raw_portals:
            raw_portals = [
                {
                    'id': payload.get('portal_id', 580001),
                    'name': payload.get('portal_name', '跨地图传送点'),
                    'x': payload.get('portal_x', 64),
                    'y': payload.get('portal_y', 67),
                    'direction': payload.get('portal_direction', 0),
                }
            ]
        for entry in raw_portals:
            source_portals.append(
                {
                    'id': entry['id'],
                    'name': entry.get('name', payload.get('portal_name', '跨地图传送点')),
                    'model': entry.get('model', monster_model),
                    'x': entry['x'],
                    'y': entry['y'],
                    'direction': entry.get('direction', payload.get('portal_direction', 0)),
                    'target_map_id': entry.get('target_map_id', target_map_id),
                    'target_x': entry.get('target_x', target_spawn['x']),
                    'target_y': entry.get('target_y', target_spawn['y']),
                }
            )

    return_portals: list[dict[str, Any]] = []
    if bool(payload.get('portal_enabled', False)):
        return_portals.append(
            {
                'id': payload.get('return_portal_id', 580002),
                'name': payload.get('return_portal_name', '返回仙石村'),
                'model': monster_model,
                'x': payload.get('return_portal_x', 9),
                'y': payload.get('return_portal_y', 6),
                'direction': payload.get('portal_direction', 0),
                'target_map_id': source_map_id,
                'target_x': source_spawn['x'],
                'target_y': source_spawn['y'],
            }
        )

    monster = {
        'id': int(payload.get('monster_id', 1_900_001)),
        'name': str(payload.get('monster_name', '试炼妖兽')),
        'model': monster_model,
        'x': int(payload.get('monster_x', 10)),
        'y': int(payload.get('monster_y', 6)),
        'direction': int(payload.get('monster_direction', 0)),
    }
    return {
        'default_map_id': source_map_id,
        'maps': {
            str(source_map_id): {
                'id': source_map_id,
                'name': str(payload.get('map_name', '仙石村')),
                'map_o_file': str(payload.get('map_o_file', 'maps/58.map.o')),
                'map_ref_available': bool(payload.get('map_ref_available', True)),
                'fallback_width': int(payload.get('map_width', 96)),
                'fallback_height': int(payload.get('map_height', 96)),
                'spawn': source_spawn,
                'monster': monster,
                'npcs': list(payload.get('npcs', [])) if payload.get('npc_enabled', True) else [],
                'portals': source_portals,
            },
            str(target_map_id): {
                'id': target_map_id,
                'name': str(payload.get('portal_target_map_name', '传送测试区')),
                'map_o_file': str(payload.get('portal_target_map_o_file', 'maps/50000.map.o')),
                'map_ref_available': bool(payload.get('portal_target_map_ref_available', True)),
                'fallback_width': int(payload.get('portal_target_map_width', 90)),
                'fallback_height': int(payload.get('portal_target_map_height', 90)),
                'spawn': target_spawn,
                'monster': {**monster, 'x': 12, 'y': 8},
                'npcs': [],
                'portals': return_portals,
            },
        },
    }


def _merge_npc_catalog(
    maps_payload: dict[str, Any],
    npc_catalog: list[dict[str, Any]] | None,
) -> dict[str, Any]:
    catalog = {
        int(entry['id']): entry
        for entry in (npc_catalog or [])
        if isinstance(entry, dict) and 'id' in entry
    }
    merged_maps: dict[str, Any] = {}
    for raw_map_id, raw_definition in maps_payload.items():
        definition = dict(raw_definition)
        merged_npcs = []
        for raw_npc in definition.get('npcs', []):
            npc = dict(raw_npc)
            supplement = catalog.get(int(npc['id']))
            if supplement:
                npc.update(supplement)
            merged_npcs.append(npc)
        definition['npcs'] = merged_npcs
        merged_maps[str(raw_map_id)] = definition
    return merged_maps


def _default_data_file(name: str) -> Path:
    return Path(__file__).with_name('data') / name


def _load_json_file(path: Path) -> Any | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except (OSError, ValueError) as exc:
        raise ValueError(f'failed to load {path.name}: {exc}') from exc


def _confirmed_appearance_entries(
    appearance_catalog: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    if appearance_catalog is None:
        return []
    if not isinstance(appearance_catalog, dict):
        raise ValueError('NPC appearance catalog must be an object')
    appearances = appearance_catalog.get('appearances')
    if not isinstance(appearances, list):
        raise ValueError('NPC appearance catalog requires appearances list')

    confirmed: list[dict[str, Any]] = []
    seen_keys: set[str] = set()
    seen_dat_ids: set[int] = set()
    for raw_entry in appearances:
        if not isinstance(raw_entry, dict):
            continue
        if raw_entry.get('enabled') is not True or raw_entry.get('status') != 'confirmed':
            continue
        key = str(raw_entry.get('key', '')).strip()
        if not key:
            raise ValueError('confirmed NPC appearance requires key')
        try:
            dat_id = int(raw_entry['dat_id'])
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError(f'NPC appearance {key!r} requires integer dat_id') from exc
        if dat_id <= 0:
            raise ValueError(f'NPC appearance {key!r} dat_id must be positive')
        if key in seen_keys:
            raise ValueError(f'duplicate NPC appearance key {key}')
        if dat_id in seen_dat_ids:
            raise ValueError(f'duplicate NPC appearance dat_id {dat_id}')
        seen_keys.add(key)
        seen_dat_ids.add(dat_id)
        confirmed.append({'key': key, 'dat_id': dat_id})
    return confirmed


def _gallery_coordinates(definition: dict[str, Any]) -> list[tuple[int, int]]:
    occupied: set[tuple[int, int]] = set()
    spawn = definition.get('spawn')
    if isinstance(spawn, dict):
        occupied.add((int(spawn['x']), int(spawn['y'])))
    monster = definition.get('monster')
    if isinstance(monster, dict):
        occupied.add((int(monster['x']), int(monster['y'])))
    for portal in definition.get('portals', []):
        if isinstance(portal, dict):
            occupied.add((int(portal['x']), int(portal['y'])))
    for npc in definition.get('npcs', []):
        if isinstance(npc, dict):
            occupied.add((int(npc['x']), int(npc['y'])))

    width = int(definition['fallback_width'])
    height = int(definition['fallback_height'])
    return [
        (x, y)
        for y in NPC_APPEARANCE_GALLERY_Y
        for x in NPC_APPEARANCE_GALLERY_X
        if 0 <= x < width and 0 <= y < height and (x, y) not in occupied
    ]


def _merge_npc_appearance_catalog(
    maps_payload: dict[str, Any],
    appearance_catalog: dict[str, Any] | None,
) -> dict[str, Any]:
    confirmed = _confirmed_appearance_entries(appearance_catalog)
    by_key = {entry['key']: entry for entry in confirmed}
    merged_maps: dict[str, Any] = {}

    for raw_map_id, raw_definition in maps_payload.items():
        definition = dict(raw_definition)
        resolved_npcs: list[dict[str, Any]] = []
        used_dat_ids: set[int] = set()
        used_object_ids: set[int] = set()

        monster = definition.get('monster')
        if isinstance(monster, dict) and 'id' in monster:
            used_object_ids.add(int(monster['id']))
        for portal in definition.get('portals', []):
            if isinstance(portal, dict) and 'id' in portal:
                used_object_ids.add(int(portal['id']))

        for raw_npc in definition.get('npcs', []):
            npc = dict(raw_npc)
            key = npc.pop('appearance_key', None)
            if key is not None:
                normalized_key = str(key)
                appearance = by_key.get(normalized_key)
                if appearance is None:
                    raise ValueError(f'unknown or unavailable NPC appearance key {normalized_key}')
                dat_id = int(appearance['dat_id'])
                npc['dat_id'] = dat_id
                npc['model'] = dat_id - NPC_APPEARANCE_MODEL_OFFSET
            dat_id = int(npc.get('dat_id', 0))
            if dat_id > 0:
                if dat_id in used_dat_ids:
                    raise ValueError(f'duplicate NPC appearance dat_id {dat_id} on map {raw_map_id}')
                used_dat_ids.add(dat_id)
            used_object_ids.add(int(npc['id']))
            resolved_npcs.append(npc)

        definition['npcs'] = resolved_npcs
        if bool(definition.get('npc_appearance_gallery', False)):
            if not confirmed:
                raise ValueError(f'map {raw_map_id} enables NPC appearance gallery but catalog is empty')
            pending = [entry for entry in confirmed if int(entry['dat_id']) not in used_dat_ids]
            coordinates = _gallery_coordinates(definition)
            if len(coordinates) < len(pending):
                raise ValueError(
                    f'map {raw_map_id} has {len(coordinates)} gallery slots for {len(pending)} NPC appearances'
                )

            next_id = NPC_APPEARANCE_GALLERY_ID_BASE
            for entry, (x, y) in zip(pending, coordinates):
                while next_id in used_object_ids:
                    next_id += 1
                dat_id = int(entry['dat_id'])
                resolved_npcs.append({
                    'id': next_id,
                    'name': f'NPC外观 {dat_id}',
                    'label': str(entry['key']),
                    'model': dat_id - NPC_APPEARANCE_MODEL_OFFSET,
                    'dat_id': dat_id,
                    'x': x,
                    'y': y,
                    'direction': 0,
                })
                used_object_ids.add(next_id)
                used_dat_ids.add(dat_id)
                next_id += 1
            definition['npcs'] = resolved_npcs

        definition.pop('npc_appearance_gallery', None)
        merged_maps[str(raw_map_id)] = definition
    return merged_maps


def _coordinate_in_bounds(x: int, y: int, definition: MapDefinition) -> bool:
    return 0 <= int(x) < definition.fallback_width and 0 <= int(y) < definition.fallback_height


def _validate_registry(registry: MapRegistry, map_keys: dict[int, int]) -> None:
    if registry.default_map_id not in registry.maps:
        raise ValueError(f'unknown default map {registry.default_map_id}')

    seen_portals: set[int] = set()
    for map_key, internal_id in map_keys.items():
        if map_key != internal_id:
            raise ValueError(f'map key {map_key} does not match id {internal_id}')

    for definition in registry.maps.values():
        if not 2 <= definition.fallback_width <= 127:
            raise ValueError(f'map {definition.id} fallback width must be within 2..127')
        if not 2 <= definition.fallback_height <= 127:
            raise ValueError(f'map {definition.id} fallback height must be within 2..127')
        if not _coordinate_in_bounds(definition.spawn_x, definition.spawn_y, definition):
            raise ValueError(f'map {definition.id} spawn coordinate is out of bounds')

        object_ids: set[int] = set()
        actors = (() if definition.monster is None else (definition.monster,)) + definition.npcs
        for actor in actors:
            if actor.id in object_ids:
                raise ValueError(f'duplicate object id {actor.id} on map {definition.id}')
            object_ids.add(actor.id)
            if not _coordinate_in_bounds(actor.x, actor.y, definition):
                raise ValueError(f'actor {actor.id} coordinate is out of bounds on map {definition.id}')
            if actor.service not in ('', 'sect_skill_mentor'):
                raise ValueError(f'unknown NPC service {actor.service!r} on actor {actor.id}')
            if actor.service == 'sect_skill_mentor':
                if actor.sect_id is None:
                    raise ValueError(f'sect skill mentor {actor.id} requires sect_id')
                if not 1 <= actor.sect_id <= 13:
                    raise ValueError(f'sect skill mentor {actor.id} sect_id must be within 1..13')

        for portal in definition.portals:
            if portal.id in seen_portals:
                raise ValueError(f'duplicate portal id {portal.id}')
            seen_portals.add(portal.id)
            if portal.id in object_ids:
                raise ValueError(f'duplicate object id {portal.id} on map {definition.id}')
            object_ids.add(portal.id)
            if not _coordinate_in_bounds(portal.x, portal.y, definition):
                raise ValueError(f'portal {portal.id} coordinate is out of bounds on map {definition.id}')
            if portal.target_map_id not in registry.maps:
                raise ValueError(f'portal {portal.id} has unknown target map {portal.target_map_id}')
            target = registry.maps[portal.target_map_id]
            if not _coordinate_in_bounds(portal.target_x, portal.target_y, target):
                raise ValueError(f'portal {portal.id} target coordinate is out of bounds')


def load_map_registry(
    payload: dict[str, Any],
    npc_catalog: list[dict[str, Any]] | None = None,
    appearance_catalog: dict[str, Any] | None = None,
) -> MapRegistry:
    if not isinstance(payload.get('maps'), dict):
        payload = _legacy_registry_payload(payload)
    maps_payload = _merge_npc_catalog(payload['maps'], npc_catalog)
    if appearance_catalog is None and any(
        isinstance(definition, dict) and bool(definition.get('npc_appearance_gallery', False))
        for definition in maps_payload.values()
    ):
        loaded = _load_json_file(_default_data_file('npc_appearance_catalog.json'))
        if loaded is not None and not isinstance(loaded, dict):
            raise ValueError('npc_appearance_catalog.json must contain an object')
        appearance_catalog = loaded
    maps_payload = _merge_npc_appearance_catalog(maps_payload, appearance_catalog)
    map_keys = {
        int(raw_map_id): int(map_payload.get('id', raw_map_id))
        for raw_map_id, map_payload in maps_payload.items()
    }
    maps = {
        int(raw_map_id): _map_definition(int(raw_map_id), map_payload)
        for raw_map_id, map_payload in maps_payload.items()
    }
    registry = MapRegistry(default_map_id=int(payload['default_map_id']), maps=maps)
    _validate_registry(registry, map_keys)
    return registry


DEFAULT_MAP_PAYLOAD: dict[str, Any] = {
    'default_map_id': 58,
    'maps': {
        '58': {
            'name': '长安',
            'map_o_file': 'maps/58.map.o',
            'map_ref_available': True,
            'fallback_width': 96,
            'fallback_height': 96,
            'spawn': {'x': 60, 'y': 67},
            'monster': {
                'id': 1_900_001,
                'name': '试炼妖兽',
                'model': -2_004_250,
                'x': 9,
                'y': 28,
                'direction': 0,
            },
            'npcs': [
                {
                    'id': 1_900_002,
                    'name': '孙思邈',
                    'label': '药王',
                    'appearance_key': 'npc_95750',
                    'x': 50,
                    'y': 64,
                },
                {
                    'id': 1_900_003,
                    'name': '接引真人',
                    'label': '接引',
                    'appearance_key': 'npc_96010',
                    'x': 34,
                    'y': 50,
                },
                {
                    'id': 1_900_004,
                    'name': '赵公明',
                    'label': '赵公明',
                    'appearance_key': 'npc_95520',
                    'x': 11,
                    'y': 21,
                },
            ],
            'npc_appearance_gallery': True,
            'portals': [
                {
                    'id': 580001,
                    'name': '跨地图传送点',
                    'model': -2_004_250,
                    'x': 55,
                    'y': 55,
                    'direction': 0,
                    'target_map_id': 50000,
                    'target_x': 8,
                    'target_y': 6,
                },
                {
                    'id': 580003,
                    'name': '跨地图传送点',
                    'model': -2_004_250,
                    'x': 34,
                    'y': 7,
                    'direction': 0,
                    'target_map_id': 50000,
                    'target_x': 8,
                    'target_y': 6,
                },
                {
                    'id': 580005,
                    'name': '昆仑传送阵',
                    'model': -2_004_250,
                    'x': 62,
                    'y': 67,
                    'direction': 0,
                    'target_map_id': 60001,
                    'target_x': 8,
                    'target_y': 6,
                },
            ],
        },
        '50000': {
            'name': '传送测试区',
            'map_o_file': 'maps/50000.map.o',
            'map_ref_available': True,
            'fallback_width': 90,
            'fallback_height': 90,
            'spawn': {'x': 8, 'y': 6},
            'monster': {
                'id': 1_900_001,
                'name': '试炼妖兽',
                'model': -2_004_250,
                'x': 12,
                'y': 8,
                'direction': 0,
            },
            'npcs': [],
            'portals': [
                {
                    'id': 580002,
                    'name': '返回长安',
                    'model': -2_004_250,
                    'x': 9,
                    'y': 6,
                    'direction': 0,
                    'target_map_id': 58,
                    'target_x': 60,
                    'target_y': 67,
                }
            ],
        },
        '60001': {
            'name': '昆仑',
            'map_o_file': 'maps/60001.map.o',
            'map_ref_available': True,
            'fallback_width': 32,
            'fallback_height': 32,
            'spawn': {'x': 8, 'y': 6},
            'npcs': [
                {
                    'id': 1_900_101,
                    'name': '昆仑导师',
                    'label': '昆仑导师',
                    'introduction': '昆仑道法，贵在潜心修行。',
                    'x': 12,
                    'y': 8,
                    'service': 'sect_skill_mentor',
                    'sect_id': 1,
                },
            ],
            'portals': [
                {
                    'id': 6_000_101,
                    'name': '返回长安',
                    'model': -2_004_250,
                    'x': 9,
                    'y': 6,
                    'direction': 0,
                    'target_map_id': 58,
                    'target_x': 60,
                    'target_y': 67,
                },
            ],
        },
    },
}


def default_map_registry() -> MapRegistry:
    legacy_catalog = _load_json_file(_default_data_file('npcs.json'))
    if legacy_catalog is not None and not isinstance(legacy_catalog, list):
        raise ValueError('npcs.json must contain a list')
    return load_map_registry(DEFAULT_MAP_PAYLOAD, npc_catalog=legacy_catalog)
