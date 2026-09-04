"""Life skill catalog data layer (采药/采矿/炼药/炼器 + gathering nodes).

Mirrors the existing registry style (item_registry / shop_registry):
stdlib only, frozen dataclasses, validation at load time. All item
references are validated against the item registry at load time so the
server can never register an uncraftable/unrewardable definition.

Protocol shapes live in docs/protocol/life-skills.md. Every numeric game
value here (ids, costs, durations, gains) is a *local compatibility value*:
the original server data is not recoverable from the APK.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from item_registry import ItemRegistry, default_item_registry


class LifeSkillCatalogError(Exception):
    """Raised when the life skill catalog is invalid."""


@dataclass(frozen=True)
class LifeSkillDefinition:
    skill_id: int
    name: str
    icon: int
    max_level: int
    tier_count: int
    upgrade_proficiency_required: int
    upgrade_silver_base: int
    upgrade_exp_base: int
    upgrade_required_role_level: int

    def upgrade_silver_cost(self, next_level: int) -> int:
        return int(self.upgrade_silver_base) * max(1, int(next_level))

    def upgrade_exp_cost(self, next_level: int) -> int:
        return int(self.upgrade_exp_base) * max(1, int(next_level))


@dataclass(frozen=True)
class LifeRecipeDefinition:
    recipe_id: int
    skill_id: int
    tier: int
    name: str
    output_template_id: int
    output_quantity: int
    materials: tuple[tuple[int, int], ...]
    vitality_cost: int
    required_level: int
    proficiency_gain: int
    description: str

    def material_slots(self) -> tuple[tuple[int, int], int, int, int]:
        """Return (4 padded (template, qty) slots, first_empty_slot)."""
        padded: list[tuple[int, int]] = []
        for index in range(4):
            padded.append(self.materials[index] if index < len(self.materials) else (0, 0))
        return tuple(padded), len(self.materials), 4 - len(self.materials)  # type: ignore[return-value]


@dataclass(frozen=True)
class GatherTargetDefinition:
    target_id: int
    name: str
    map_id: int
    x: int
    y: int
    category: int
    skill_id: int
    required_level: int
    stamina_cost: int
    duration_seconds: int
    reward_template_id: int
    reward_quantity: int
    proficiency_gain: int
    model_id: int


@dataclass(frozen=True)
class LearnableEntryDefinition:
    entry_id: int
    skill_id: int
    level_requirement: int
    silver_cost: int
    experience_cost: int
    display: str
    detail: str


@dataclass(frozen=True)
class LifeSkillTrainerDefinition:
    trainer_id: int
    name: str
    entry_ids: tuple[int, ...]

    def teaches(self, entry_id: int) -> bool:
        return int(entry_id) in self.entry_ids


class LifeSkillRegistry:
    """Load and validate the life skill catalog."""

    def __init__(self, catalog_file: Path, item_registry: ItemRegistry) -> None:
        self.item_registry = item_registry
        self.stamina_max = 100
        self.vitality_max = 100
        self.skills: dict[int, LifeSkillDefinition] = {}
        self.recipes: dict[int, LifeRecipeDefinition] = {}
        self.gather_targets: tuple[GatherTargetDefinition, ...] = ()
        self.learnable: dict[int, LearnableEntryDefinition] = {}
        self.trainers: dict[int, LifeSkillTrainerDefinition] = {}
        self._load(catalog_file)

    def _load(self, path: Path) -> None:
        data = json.loads(path.read_text(encoding='utf-8'))
        if not isinstance(data, dict):
            raise LifeSkillCatalogError(f'life skill catalog must be a dict: {path}')
        defaults = data.get('defaults', {})
        if not isinstance(defaults, dict):
            raise LifeSkillCatalogError(f'"defaults" must be a dict: {path}')
        self.stamina_max = int(defaults.get('stamina_max', 100))
        self.vitality_max = int(defaults.get('vitality_max', 100))
        self._load_skills(data.get('skills', []), path)
        self._load_recipes(data.get('recipes', []), path)
        self._load_targets(data.get('gather_targets', []), path)
        self._load_learnable(data.get('learnable', []), path)
        self._load_trainers(data.get('trainers', []), path)

    def _load_skills(self, raw_skills: Any, path: Path) -> None:
        if not isinstance(raw_skills, list):
            raise LifeSkillCatalogError(f'"skills" must be a list: {path}')
        for raw in raw_skills:
            if not isinstance(raw, dict):
                raise LifeSkillCatalogError(f'each skill must be a dict: {path}')
            skill_id = int(raw['skill_id'])
            if skill_id in self.skills:
                raise LifeSkillCatalogError(f'duplicate skill_id {skill_id}: {path}')
            name = str(raw.get('name', ''))
            if not name:
                raise LifeSkillCatalogError(f'skill {skill_id} needs a name')
            max_level = int(raw.get('max_level', 1))
            if max_level < 1:
                raise LifeSkillCatalogError(f'skill {skill_id} max_level must be >= 1')
            self.skills[skill_id] = LifeSkillDefinition(
                skill_id=skill_id,
                name=name,
                icon=int(raw.get('icon', 0)),
                max_level=max_level,
                tier_count=int(raw.get('tier_count', 1)),
                upgrade_proficiency_required=int(raw.get('upgrade_proficiency_required', 100)),
                upgrade_silver_base=int(raw.get('upgrade_silver_base', 10000)),
                upgrade_exp_base=int(raw.get('upgrade_exp_base', 500)),
                upgrade_required_role_level=int(raw.get('upgrade_required_role_level', 1)),
            )

    def _load_recipes(self, raw_recipes: Any, path: Path) -> None:
        if not isinstance(raw_recipes, list):
            raise LifeSkillCatalogError(f'"recipes" must be a list: {path}')
        for raw in raw_recipes:
            if not isinstance(raw, dict):
                raise LifeSkillCatalogError(f'each recipe must be a dict: {path}')
            recipe_id = int(raw['recipe_id'])
            if recipe_id in self.recipes:
                raise LifeSkillCatalogError(f'duplicate recipe_id {recipe_id}: {path}')
            skill_id = int(raw['skill_id'])
            if skill_id not in self.skills:
                raise LifeSkillCatalogError(
                    f'recipe {recipe_id} references unknown skill {skill_id}: {path}'
                )
            output_template_id = int(raw['output_template_id'])
            try:
                self.item_registry.require(output_template_id)
            except KeyError as exc:
                raise LifeSkillCatalogError(
                    f'recipe {recipe_id} output template {output_template_id} unknown'
                ) from exc
            raw_materials = raw.get('materials', [])
            if not isinstance(raw_materials, list) or not raw_materials:
                raise LifeSkillCatalogError(f'recipe {recipe_id} needs materials: {path}')
            if len(raw_materials) > 4:
                raise LifeSkillCatalogError(f'recipe {recipe_id} has more than 4 materials')
            materials: list[tuple[int, int]] = []
            for raw_material in raw_materials:
                template_id = int(raw_material[0])
                quantity = int(raw_material[1])
                if quantity < 1:
                    raise LifeSkillCatalogError(
                        f'recipe {recipe_id} material quantity must be >= 1'
                    )
                try:
                    self.item_registry.require(template_id)
                except KeyError as exc:
                    raise LifeSkillCatalogError(
                        f'recipe {recipe_id} material template {template_id} unknown'
                    ) from exc
                materials.append((template_id, quantity))
            output_quantity = int(raw.get('output_quantity', 1))
            if output_quantity < 1:
                raise LifeSkillCatalogError(f'recipe {recipe_id} output_quantity must be >= 1')
            self.recipes[recipe_id] = LifeRecipeDefinition(
                recipe_id=recipe_id,
                skill_id=skill_id,
                tier=int(raw.get('tier', 0)),
                name=str(raw.get('name', '')),
                output_template_id=output_template_id,
                output_quantity=output_quantity,
                materials=tuple(materials),
                vitality_cost=int(raw.get('vitality_cost', 0)),
                required_level=int(raw.get('required_level', 1)),
                proficiency_gain=int(raw.get('proficiency_gain', 0)),
                description=str(raw.get('description', '')),
            )

    def _load_targets(self, raw_targets: Any, path: Path) -> None:
        if not isinstance(raw_targets, list):
            raise LifeSkillCatalogError(f'"gather_targets" must be a list: {path}')
        targets: list[GatherTargetDefinition] = []
        seen: set[int] = set()
        for raw in raw_targets:
            if not isinstance(raw, dict):
                raise LifeSkillCatalogError(f'each gather target must be a dict: {path}')
            target_id = int(raw['target_id'])
            if target_id in seen:
                raise LifeSkillCatalogError(f'duplicate gather target id {target_id}: {path}')
            seen.add(target_id)
            skill_id = int(raw['skill_id'])
            if skill_id not in self.skills:
                raise LifeSkillCatalogError(
                    f'gather target {target_id} references unknown skill {skill_id}'
                )
            reward_template_id = int(raw['reward_template_id'])
            try:
                self.item_registry.require(reward_template_id)
            except KeyError as exc:
                raise LifeSkillCatalogError(
                    f'gather target {target_id} reward template {reward_template_id} unknown'
                ) from exc
            targets.append(GatherTargetDefinition(
                target_id=target_id,
                name=str(raw.get('name', '')),
                map_id=int(raw.get('map_id', 0)),
                x=int(raw.get('x', 0)),
                y=int(raw.get('y', 0)),
                category=int(raw.get('category', 0)),
                skill_id=skill_id,
                required_level=int(raw.get('required_level', 1)),
                stamina_cost=int(raw.get('stamina_cost', 0)),
                duration_seconds=int(raw.get('duration_seconds', 1)),
                reward_template_id=reward_template_id,
                reward_quantity=int(raw.get('reward_quantity', 1)),
                proficiency_gain=int(raw.get('proficiency_gain', 0)),
                model_id=int(raw.get('model_id', 1)),
            ))
        self.gather_targets = tuple(targets)

    def _load_learnable(self, raw_entries: Any, path: Path) -> None:
        if not isinstance(raw_entries, list):
            raise LifeSkillCatalogError(f'"learnable" must be a list: {path}')
        for raw in raw_entries:
            if not isinstance(raw, dict):
                raise LifeSkillCatalogError(f'each learnable entry must be a dict: {path}')
            entry_id = int(raw['entry_id'])
            if entry_id in self.learnable:
                raise LifeSkillCatalogError(f'duplicate learnable entry {entry_id}: {path}')
            skill_id = int(raw['skill_id'])
            if skill_id not in self.skills:
                raise LifeSkillCatalogError(
                    f'learnable entry {entry_id} references unknown skill {skill_id}'
                )
            self.learnable[entry_id] = LearnableEntryDefinition(
                entry_id=entry_id,
                skill_id=skill_id,
                level_requirement=int(raw.get('level_requirement', 1)),
                silver_cost=int(raw.get('silver_cost', 0)),
                experience_cost=int(raw.get('experience_cost', 0)),
                display=str(raw.get('display', '')),
                detail=str(raw.get('detail', '')),
            )

    def _load_trainers(self, raw_trainers: Any, path: Path) -> None:
        if not isinstance(raw_trainers, list):
            raise LifeSkillCatalogError(f'"trainers" must be a list: {path}')
        for raw in raw_trainers:
            if not isinstance(raw, dict):
                raise LifeSkillCatalogError(f'each trainer must be a dict: {path}')
            trainer_id = int(raw['trainer_id'])
            if trainer_id in self.trainers:
                raise LifeSkillCatalogError(f'duplicate trainer id {trainer_id}: {path}')
            entry_ids = tuple(int(entry) for entry in raw.get('entry_ids', []))
            for entry_id in entry_ids:
                if entry_id not in self.learnable:
                    raise LifeSkillCatalogError(
                        f'trainer {trainer_id} references unknown entry {entry_id}'
                    )
            self.trainers[trainer_id] = LifeSkillTrainerDefinition(
                trainer_id=trainer_id,
                name=str(raw.get('name', '')),
                entry_ids=entry_ids,
            )

    def recipe(self, recipe_id: int) -> LifeRecipeDefinition | None:
        return self.recipes.get(int(recipe_id))

    def recipes_for(self, skill_id: int, tier: int) -> list[LifeRecipeDefinition]:
        return [
            recipe for recipe in self.recipes.values()
            if recipe.skill_id == int(skill_id) and recipe.tier == int(tier)
        ]

    def gather_target(self, target_id: int) -> GatherTargetDefinition | None:
        for target in self.gather_targets:
            if target.target_id == int(target_id):
                return target
        return None

    def gather_targets_for(self, map_id: int) -> list[GatherTargetDefinition]:
        return [target for target in self.gather_targets if target.map_id == int(map_id)]


_DEFAULT_CATALOG_FILE = (
    Path(__file__).resolve().parent / 'data' / 'catalog' / 'life_skills.json'
)


def default_life_skill_registry(item_registry: ItemRegistry | None = None) -> LifeSkillRegistry:
    if item_registry is None:
        item_registry = default_item_registry()
    return LifeSkillRegistry(_DEFAULT_CATALOG_FILE, item_registry)
