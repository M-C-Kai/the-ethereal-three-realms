"""Sect and sect skill catalog registry.

This module defines the catalog for sects and their skills, providing a
data-driven way to manage what skills each sect has and what their
definitions look like.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING


LOG = logging.getLogger('piaomiao-local')


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

    @property
    def is_locked(self) -> bool:
        """Return True if this skill is a compat placeholder."""
        return self.source == "compat"


class SectRegistryError(Exception):
    """Raised for sect catalog errors."""

    pass


class SectRegistry:
    """Catalog for sects and their skills."""

    def __init__(self, catalog_path: Path):
        """Initialize the sect registry from a catalog file.

        Args:
            catalog_path: Path to the sect catalog JSON file.

        Raises:
            SectRegistryError: If the catalog is malformed.
        """
        self.catalog_path = catalog_path
        self._sects: dict[int, SectDefinition] = {}
        self._skills: dict[int, SectSkillDefinition] = {}
        self._skills_by_sect: dict[int, list[SectSkillDefinition]] = {}

        self._load_catalog()

    def _load_catalog(self) -> None:
        """Load sect and skill definitions from the catalog file."""
        try:
            import json

            with open(self.catalog_path, "r", encoding="utf-8") as f:
                catalog = json.load(f)

            # Load sects
            for sect_data in catalog.get("sects", []):
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
            for skill_data in catalog.get("skills", []):
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
                if sect_id not in self._sects[sect_id].skill_ids:
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

                self._skills[skill_id] = skill
                self._skills_by_sect[sect_id].append(skill)

            LOG.info("Sect registry loaded: %d sects, %d skills",
                    len(self._sects), len(self._skills))

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
    catalog_path = Path(__file__).parent / "data" / "catalog" / "sects.json"
    return SectRegistry(catalog_path)
