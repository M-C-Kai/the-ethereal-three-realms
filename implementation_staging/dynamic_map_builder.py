from __future__ import annotations

import copy
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from map_o import MapO, inspect_map_ref
from tools.map_ref_generator import from_spec as map_ref_from_spec
from tools.map_ref_generator import parse_map_ref, serialize_map_ref


DYNAMIC_MAP_FORMAT = 'piaomiao-dynamic-map-v1'
MAP_REF_FORMAT = 'piaomiao-map-ref-v1'


@dataclass(frozen=True)
class DynamicMapPackage:
    map_id: int
    directory: Path
    map_spec_path: Path
    map_ref_spec_path: Path
    output_map_o_path: Path
    output_map_ref_path: Path


@dataclass(frozen=True)
class MaterializedDynamicMap:
    map_id: int
    map_ref_path: Path
    map_o_path: Path
    map_ref_bytes: int
    map_o_bytes: int


def default_maps_root() -> Path:
    return Path(__file__).resolve().parent / 'maps'


def discover_dynamic_maps(root: Path | None = None) -> list[DynamicMapPackage]:
    """Discover numeric ``maps/<id>/`` packages containing both JSON specs."""
    root = Path(root) if root is not None else default_maps_root()
    if not root.exists():
        return []

    packages: list[DynamicMapPackage] = []
    for directory in root.iterdir():
        if not directory.is_dir() or not directory.name.isdigit():
            continue
        map_spec = directory / 'map.json'
        map_ref_spec = directory / 'map.ref.json'
        if not map_spec.exists() and not map_ref_spec.exists():
            continue
        if not map_spec.is_file() or not map_ref_spec.is_file():
            missing = 'map.json' if not map_spec.is_file() else 'map.ref.json'
            raise ValueError(f'dynamic map package {directory.name} is missing {missing}')
        map_id = int(directory.name)
        packages.append(DynamicMapPackage(
            map_id=map_id,
            directory=directory,
            map_spec_path=map_spec,
            map_ref_spec_path=map_ref_spec,
            output_map_o_path=root / f'{map_id}.map.o',
            output_map_ref_path=root / f'{map_id}.map.ref',
        ))
    return sorted(packages, key=lambda item: item.map_id)


def _load_object(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding='utf-8'))
    except (OSError, ValueError) as exc:
        raise ValueError(f'failed to load dynamic map spec {path}: {exc}') from exc
    if not isinstance(payload, dict):
        raise ValueError(f'dynamic map spec {path} must contain a JSON object')
    return payload


def _validate_identity(
    payload: dict[str, Any],
    package: DynamicMapPackage,
    *,
    expected_format: str,
    path: Path,
) -> None:
    if payload.get('format') != expected_format:
        raise ValueError(f'{path} format must be {expected_format!r}')
    try:
        declared_map_id = int(payload['map_id'])
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError(f'{path} requires integer map_id') from exc
    if declared_map_id != package.map_id:
        raise ValueError(
            f'{path} map_id {declared_map_id} does not match directory {package.map_id}'
        )


def _normalize_tile_rows(payload: dict[str, Any]) -> dict[str, Any]:
    """Allow editable whitespace/comma separated tile rows in addition to arrays."""
    normalized = dict(payload)
    raw_rows = payload.get('tiles')
    if isinstance(raw_rows, list) and raw_rows and all(isinstance(row, str) for row in raw_rows):
        rows: list[list[int | None]] = []
        for row_index, raw_row in enumerate(raw_rows):
            values: list[int | None] = []
            for token in raw_row.replace(',', ' ').split():
                if token.lower() in {'null', 'none', '.'}:
                    values.append(None)
                else:
                    try:
                        values.append(int(token))
                    except ValueError as exc:
                        raise ValueError(
                            f'tiles row {row_index} contains non-integer token {token!r}'
                        ) from exc
            rows.append(values)
        normalized['tiles'] = rows
    return normalized


def _build_map_ref(package: DynamicMapPackage) -> bytes:
    payload = _load_object(package.map_ref_spec_path)
    _validate_identity(
        payload,
        package,
        expected_format=MAP_REF_FORMAT,
        path=package.map_ref_spec_path,
    )
    records, composites = map_ref_from_spec(payload)
    data = serialize_map_ref(records, composites)
    parsed_records, parsed_composites = parse_map_ref(data)
    if parsed_records != records or parsed_composites != composites:
        raise ValueError(f'{package.map_ref_spec_path} failed map.ref round-trip validation')
    return data


def _build_map_o(package: DynamicMapPackage, ref_data: bytes) -> bytes:
    payload = _load_object(package.map_spec_path)
    _validate_identity(
        payload,
        package,
        expected_format=DYNAMIC_MAP_FORMAT,
        path=package.map_spec_path,
    )
    result = MapO.from_spec(_normalize_tile_rows(payload))
    result.validate(inspect_map_ref(ref_data))
    return result.to_file()


def _write_if_changed(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.is_file() or path.read_bytes() != data:
        path.write_bytes(data)


def materialize_dynamic_map(package: DynamicMapPackage) -> MaterializedDynamicMap:
    """Build one package into the flat runtime files consumed by the server."""
    ref_data = _build_map_ref(package)
    map_o_data = _build_map_o(package, ref_data)
    _write_if_changed(package.output_map_ref_path, ref_data)
    _write_if_changed(package.output_map_o_path, map_o_data)
    return MaterializedDynamicMap(
        map_id=package.map_id,
        map_ref_path=package.output_map_ref_path,
        map_o_path=package.output_map_o_path,
        map_ref_bytes=len(ref_data),
        map_o_bytes=len(map_o_data),
    )


def materialize_all_dynamic_maps(root: Path | None = None) -> list[MaterializedDynamicMap]:
    return [materialize_dynamic_map(package) for package in discover_dynamic_maps(root)]


def _registry_definition(
    package: DynamicMapPackage,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    payload = _load_object(package.map_spec_path)
    _validate_identity(
        payload,
        package,
        expected_format=DYNAMIC_MAP_FORMAT,
        path=package.map_spec_path,
    )
    registry = payload.get('registry')
    if not isinstance(registry, dict):
        raise ValueError(f'{package.map_spec_path} requires registry object')
    if not str(registry.get('name', '')).strip():
        raise ValueError(f'{package.map_spec_path} registry requires name')
    spawn = registry.get('spawn')
    if not isinstance(spawn, dict) or 'x' not in spawn or 'y' not in spawn:
        raise ValueError(f'{package.map_spec_path} registry requires spawn x/y')

    inbound = registry.get('inbound_portals', [])
    if not isinstance(inbound, list):
        raise ValueError(f'{package.map_spec_path} registry inbound_portals must be a list')
    if any(not isinstance(item, dict) for item in inbound):
        raise ValueError(f'{package.map_spec_path} registry inbound_portals entries must be objects')

    definition = {
        key: copy.deepcopy(value)
        for key, value in registry.items()
        if key != 'inbound_portals'
    }
    definition.update({
        'id': package.map_id,
        'map_o_file': f'maps/{package.map_id}.map.o',
        # Dynamic refs must use 1010/13 status=1 + 1407/11+12, never APK-local lookup.
        'map_ref_available': False,
        'fallback_width': int(payload['width']),
        'fallback_height': int(payload['height']),
    })
    definition.setdefault('npcs', [])
    definition.setdefault('portals', [])
    return definition, [copy.deepcopy(item) for item in inbound]


def merge_dynamic_maps_into_registry_payload(
    payload: dict[str, Any],
    root: Path | None = None,
) -> dict[str, Any]:
    """Merge package registration metadata into a modern server config payload.

    A dynamic package owns its target-map definition. ``inbound_portals`` may
    additionally attach one or more entry portals to already registered maps.
    Target id/x/y default to the package and its spawn, making a complete new
    map deployable without editing ``config.json``.
    """
    merged = copy.deepcopy(payload)
    maps = merged.get('maps')
    if not isinstance(maps, dict):
        raise ValueError('dynamic map packages require config.json maps object')

    pending_inbound: list[tuple[int, dict[str, Any], dict[str, Any]]] = []
    for package in discover_dynamic_maps(root):
        key = str(package.map_id)
        if key in maps:
            raise ValueError(
                f'dynamic map {package.map_id} is also declared in config.json; '
                'remove the duplicate config entry'
            )
        definition, inbound = _registry_definition(package)
        maps[key] = definition
        for portal in inbound:
            try:
                source_map_id = int(portal.pop('source_map_id'))
            except (KeyError, TypeError, ValueError) as exc:
                raise ValueError(
                    f'dynamic map {package.map_id} inbound portal requires source_map_id'
                ) from exc
            pending_inbound.append((source_map_id, portal, definition))

    for source_map_id, portal, target_definition in pending_inbound:
        source = maps.get(str(source_map_id))
        if not isinstance(source, dict):
            raise ValueError(f'dynamic inbound portal references unknown source map {source_map_id}')
        target_map_id = int(target_definition['id'])
        spawn = target_definition['spawn']
        if 'target_map_id' in portal and int(portal['target_map_id']) != target_map_id:
            raise ValueError(
                f'inbound portal on map {source_map_id} must target its package map {target_map_id}'
            )
        portal['target_map_id'] = target_map_id
        portal.setdefault('target_x', int(spawn['x']))
        portal.setdefault('target_y', int(spawn['y']))
        portals = source.setdefault('portals', [])
        if not isinstance(portals, list):
            raise ValueError(f'map {source_map_id} portals must be a list')
        portals.append(portal)

    return merged
