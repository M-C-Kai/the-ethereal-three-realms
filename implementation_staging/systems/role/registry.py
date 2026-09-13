"""角色系统静态目录：门派与门派技能目录。"""
from __future__ import annotations

import logging

LOG = logging.getLogger('piaomiao-local')

import logging

"""Sect and sect skill catalog registry.

This module defines the catalog for sects and their skills, providing a
data-driven way to manage what skills each sect has and what their
definitions look like.
"""


import logging
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING




@dataclass(frozen=True)
class SectDefinition:
    """A sect (sect_id, name, and associated skill IDs)."""

    sect_id: int
    name: str
    skill_ids: list[int]


@dataclass(frozen=True)
class SectSkillDefinition:
    """A skill belonging to a sect."""

    skill_id: int
    sect_id: int
    name: str
    max_level: int
    default_level: int
    icon: int
    required_role_level: int
    silver_base: int
    experience_base: int
    effect: str
    current_text: str
    next_text: str
    required_item_id: int
    required_item_name: str
    required_item_count: int
    source: str


class SectRegistryError(Exception):
    """Raised for sect catalog errors."""

    pass


class SectRegistry:
    """Catalog for sects and their skills."""

    def __init__(self, sects_path: Path, skills_path: Path):
        """Initialize the sect registry from catalog files.

        Args:
            sects_path: Path to the sects JSON file.
            skills_path: Path to the skills JSON file.

        Raises:
            SectRegistryError: If the catalogs are malformed.
        """
        self.sects_path = sects_path
        self.skills_path = skills_path
        self._sects: dict[int, SectDefinition] = {}
        self._skills: dict[int, SectSkillDefinition] = {}
        self._skills_by_sect: dict[int, list[SectSkillDefinition]] = {}

        self._load_catalog()

    def _load_catalog(self) -> None:
        """Load sect and skill definitions from catalog files."""
        try:
            import json

            # Load sects
            with open(self.sects_path, "r", encoding="utf-8") as f:
                sects_catalog = json.load(f)

            # Load skills
            with open(self.skills_path, "r", encoding="utf-8") as f:
                skills_catalog = json.load(f)

            # Load sects
            for sect_data in sects_catalog.get("sects", []):
                sect_id = int(sect_data.get("sect_id", 0))
                name = str(sect_data.get("name", ""))
                skill_ids = [int(sid) for sid in sect_data.get("skill_ids", [])]

                if sect_id in self._sects:
                    raise SectRegistryError(
                        f"Duplicate sect_id {sect_id} in catalog"
                    )

                self._sects[sect_id] = SectDefinition(
                    sect_id=sect_id, name=name, skill_ids=skill_ids
                )

                # Initialize skills_by_sect
                self._skills_by_sect[sect_id] = []

            # Load skills
            for skill_data in skills_catalog.get("skills", []):
                skill_id = int(skill_data.get("skill_id", 0))
                sect_id = int(skill_data.get("sect_id", 0))
                name = str(skill_data.get("name", ""))
                max_level = int(skill_data.get("max_level", 0))
                default_level = int(skill_data.get("default_level", 0))
                icon = int(skill_data.get("icon", 0))
                required_role_level = int(skill_data.get("required_role_level", 0))
                silver_base = int(skill_data.get("silver_base", 0))
                experience_base = int(skill_data.get("experience_base", 0))
                effect = str(skill_data.get("effect", ""))
                current_text = str(skill_data.get("current_text", ""))
                next_text = str(skill_data.get("next_text", ""))
                required_item_id = int(skill_data.get("required_item_id", 0))
                required_item_name = str(skill_data.get("required_item_name", ""))
                required_item_count = int(skill_data.get("required_item_count", 0))
                source = str(skill_data.get("source", "compat"))

                if skill_id in self._skills:
                    raise SectRegistryError(
                        f"Duplicate skill_id {skill_id} in catalog"
                    )

                if sect_id not in self._sects:
                    raise SectRegistryError(
                        f"Skill {skill_id} references non-existent sect {sect_id}"
                    )

                # Validate skill belongs to sect
                if skill_id not in self._sects[sect_id].skill_ids:
                    raise SectRegistryError(
                        f"Skill {skill_id} (sect {sect_id}) not listed in sect's skill_ids"
                    )

                skill = SectSkillDefinition(
                    skill_id=skill_id,
                    sect_id=sect_id,
                    name=name,
                    max_level=max_level,
                    default_level=default_level,
                    icon=icon,
                    required_role_level=required_role_level,
                    silver_base=silver_base,
                    experience_base=experience_base,
                    effect=effect,
                    current_text=current_text,
                    next_text=next_text,
                    required_item_id=required_item_id,
                    required_item_name=required_item_name,
                    required_item_count=required_item_count,
                    source=source,
                )

                # Validate sect_id matches skill's sect_id
                if skill.sect_id != sect_id:
                    raise SectRegistryError(
                        f"Skill {skill_id} has sect_id {skill.sect_id} but references sect {sect_id}"
                    )

                self._skills[skill_id] = skill
                self._skills_by_sect[sect_id].append(skill)

            LOG.info("Sect registry loaded: %d sects, %d skills",
                    len(self._sects), len(self._skills))

            # Perform reverse validation: check all sect.skill_ids reference existing skills
            for sect in self._sects.values():
                for skill_id in sect.skill_ids:
                    skill = self._skills.get(skill_id)
                    if skill is None:
                        raise SectRegistryError(
                            f"Sect {sect.sect_id} references unknown skill {skill_id}"
                        )
                    if skill.sect_id != sect.sect_id:
                        raise SectRegistryError(
                            f"Skill {skill_id} belongs to sect "
                            f"{skill.sect_id}, not {sect.sect_id}"
                        )

        except json.JSONDecodeError as e:
            raise SectRegistryError(f"Invalid JSON in catalog: {e}") from e
        except Exception as e:
            raise SectRegistryError(f"Failed to load catalog: {e}") from e

    def sect(self, sect_id: int) -> SectDefinition | None:
        """Get a sect definition by ID.

        Args:
            sect_id: The sect ID.

        Returns:
            The sect definition, or None if not found.
        """
        return self._sects.get(sect_id)

    def skill(self, skill_id: int) -> SectSkillDefinition | None:
        """Get a sect skill definition by ID.

        Args:
            skill_id: The skill ID.

        Returns:
            The skill definition, or None if not found.
        """
        return self._skills.get(skill_id)

    def skills_for_sect(self, sect_id: int) -> list[SectSkillDefinition]:
        """Get all skills for a sect.

        Args:
            sect_id: The sect ID.

        Returns:
            List of skill definitions. Empty if sect not found.
        """
        return self._skills_by_sect.get(sect_id, [])

    def skill_belongs_to_sect(self, skill_id: int, sect_id: int) -> bool:
        """Check if a skill belongs to a sect.

        Args:
            skill_id: The skill ID.
            sect_id: The sect ID.

        Returns:
            True if the skill belongs to the sect.
        """
        skill = self._skills.get(skill_id)
        return skill is not None and skill.sect_id == sect_id


def default_sect_registry() -> SectRegistry:
    """Get the default sect registry instance.

    Returns:
        The default sect registry.
    """
    sects_path = Path(__file__).resolve().parents[2] / "data" / "catalog" / "sects.json"
    skills_path = Path(__file__).resolve().parents[2] / "data" / "catalog" / "sect_skills.json"
    return SectRegistry(sects_path, skills_path)

# ---------------------------------------------------------------------------
# 坐骑目录（自 mount_constructor.py 收编）。
# ---------------------------------------------------------------------------
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
    return Path(__file__).resolve().parents[2] / 'data' / 'catalog' / 'mount_appearance_mapping.json'


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

# ---------------------------------------------------------------------------
# 坐骑状态构建（自 mount_constructor.py 收编）。
# ---------------------------------------------------------------------------
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
