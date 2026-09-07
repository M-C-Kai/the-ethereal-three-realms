from __future__ import annotations

import json
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any


MOUNT_EQUIPMENT_SLOT = 17
MOUNT_STAGE_NORMAL = 0
MOUNT_STAGE_SPIRIT = 1
MOUNT_STAGE_IMMORTAL = 2
MOUNT_STAGE_DIVINE = 3
MOUNT_STAGE_NAMES = ('normal', 'spirit', 'immortal', 'divine')


def default_mount_catalog_path() -> Path:
    return Path(__file__).resolve().parent / 'data' / 'catalog' / 'mount_appearance_mapping.json'


@dataclass(frozen=True)
class MountSeries:
    series_id: int
    name: str
    appearances: dict[int, int]


@dataclass(frozen=True)
class MountState:
    series_id: int
    stage: int
    grade: int
    growth: int
    image_id: int
    ride_code: int
    role_model: int
    equipped: bool


@dataclass(frozen=True)
class MountCatalog:
    image_base: int
    series: dict[int, MountSeries]
    image_to_series_stage: dict[int, tuple[int, int]]
    named_templates: dict[int, dict[str, Any]]
    template_base: int

    def resolve_appearance(self, series_id: int, stage: int) -> int:
        series = self.series.get(int(series_id))
        if series is None:
            raise KeyError(f'unknown mount series: {series_id}')
        normalized_stage = max(MOUNT_STAGE_NORMAL, min(MOUNT_STAGE_DIVINE, int(stage)))
        # A logical evolution stage does not imply a distinct APK image. If a
        # stage has no dedicated resource, inherit the nearest earlier image.
        for candidate in range(normalized_stage, MOUNT_STAGE_NORMAL - 1, -1):
            image_id = series.appearances.get(candidate)
            if image_id is not None:
                return image_id
        raise ValueError(f'mount series has no normal appearance: {series_id}')

    def template_id_for_image(self, image_id: int) -> int:
        override = self.named_templates.get(int(image_id), {})
        if 'template_id' in override:
            return int(override['template_id'])
        return self.template_base + (int(image_id) - self.image_base)


@lru_cache(maxsize=4)
def load_mount_catalog(path: Path | None = None) -> MountCatalog:
    catalog_path = path or default_mount_catalog_path()
    data = json.loads(catalog_path.read_text(encoding='utf-8'))
    image_base = int(data.get('image_base', 40000))
    projection = data.get('item_projection', {})
    template_base = int(projection.get('template_base', 170900000))
    named_templates = {
        int(image_id): dict(payload)
        for image_id, payload in data.get('named_templates', {}).items()
    }

    series_map: dict[int, MountSeries] = {}
    image_to_series_stage: dict[int, tuple[int, int]] = {}
    for raw in data.get('mount_series', []):
        series_id = int(raw['series_id'])
        if series_id in series_map:
            raise ValueError(f'duplicate mount series id: {series_id}')
        appearances: dict[int, int] = {}
        for stage_name, raw_image_id in raw.get('appearances', {}).items():
            if stage_name not in MOUNT_STAGE_NAMES:
                raise ValueError(f'unknown mount stage name: {stage_name}')
            stage = MOUNT_STAGE_NAMES.index(stage_name)
            image_id = int(raw_image_id)
            appearances[stage] = image_id
            if image_id in image_to_series_stage:
                raise ValueError(f'mount appearance assigned twice: {image_id}')
            image_to_series_stage[image_id] = (series_id, stage)
        if MOUNT_STAGE_NORMAL not in appearances:
            raise ValueError(f'mount series missing normal appearance: {series_id}')
        series_map[series_id] = MountSeries(
            series_id=series_id,
            name=str(raw.get('name') or f'坐骑系列 {series_id}'),
            appearances=appearances,
        )

    return MountCatalog(
        image_base=image_base,
        series=series_map,
        image_to_series_stage=image_to_series_stage,
        named_templates=named_templates,
        template_base=template_base,
    )


def _role_model_for_ride_code(ride_code: int) -> int:
    code = int(ride_code)
    if code == 0:
        return 100000
    return 101000 + ((code % 10000) // 1000) * 1000


def _explicit_mount_state(item: dict[str, Any]) -> tuple[int, int, int, int] | None:
    raw = item.get('mount_state')
    if not isinstance(raw, dict) or 'series_id' not in raw:
        return None
    return (
        int(raw['series_id']),
        int(raw.get('stage', MOUNT_STAGE_NORMAL)),
        max(1, int(raw.get('grade', 1))),
        max(0, int(raw.get('growth', 0))),
    )


def construct_mount_state(
    item: dict[str, Any],
    item_registry: Any,
    catalog: MountCatalog | None = None,
) -> MountState | None:
    """Construct the client riding state from one real item instance.

    Explicit per-instance ``mount_state`` is authoritative. Legacy mount item
    templates remain readable: their historical ``mount_model`` ride code is
    mapped back to the confirmed series/stage relation so old saves can migrate
    without treating every APK appearance as a different mount species.
    """
    resolved = item_registry.resolve(item)
    if resolved.get('kind') != 'mount' and not isinstance(item.get('mount_state'), dict):
        return None

    catalog = catalog or load_mount_catalog()
    explicit = _explicit_mount_state(item)
    if explicit is not None:
        series_id, stage, grade, growth = explicit
    else:
        ride_code = int(resolved.get('mount_model', 0) or 0)
        if ride_code <= 0:
            return None
        image_id = catalog.image_base + ride_code
        relation = catalog.image_to_series_stage.get(image_id)
        if relation is None:
            return None
        series_id, stage = relation
        grade = 1
        growth = 0

    image_id = catalog.resolve_appearance(series_id, stage)
    ride_code = image_id - catalog.image_base
    return MountState(
        series_id=series_id,
        stage=max(MOUNT_STAGE_NORMAL, min(MOUNT_STAGE_DIVINE, stage)),
        grade=grade,
        growth=growth,
        image_id=image_id,
        ride_code=ride_code,
        role_model=_role_model_for_ride_code(ride_code),
        equipped=item.get('location') == 'equipped',
    )


def mount_ride_code_from_item(item: dict[str, Any], item_registry: Any) -> int:
    state = construct_mount_state(item, item_registry)
    return 0 if state is None else state.ride_code


def equipped_mount_state(role: dict[str, Any], item_registry: Any) -> MountState | None:
    for item in role.get('items', []):
        if not isinstance(item, dict) or item.get('location') != 'equipped':
            continue
        state = construct_mount_state(item, item_registry)
        if state is not None:
            return state
    return None


def mount_ride_code_for_role(role: dict[str, Any], item_registry: Any) -> int:
    state = equipped_mount_state(role, item_registry)
    return 0 if state is None else state.ride_code


def create_mount_item_instance(
    *,
    instance_id: int,
    series_id: int,
    stage: int = MOUNT_STAGE_NORMAL,
    grade: int = 1,
    growth: int = 0,
    location: str = 'bag',
    catalog: MountCatalog | None = None,
) -> dict[str, Any]:
    """Create a standard inventory/equipment item carrying mount state."""
    catalog = catalog or load_mount_catalog()
    image_id = catalog.resolve_appearance(series_id, stage)
    return {
        'id': int(instance_id),
        'template_id': catalog.template_id_for_image(image_id),
        'quantity': 1,
        'location': str(location),
        'mount_state': {
            'series_id': int(series_id),
            'stage': max(MOUNT_STAGE_NORMAL, min(MOUNT_STAGE_DIVINE, int(stage))),
            'grade': max(1, int(grade)),
            'growth': max(0, int(growth)),
        },
    }
