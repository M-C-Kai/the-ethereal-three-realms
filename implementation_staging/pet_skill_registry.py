from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


class PetSkillCatalogError(ValueError):
    pass


@dataclass(frozen=True)
class PetSkillDefinition:
    skill_id: int
    name: str
    level: int
    icon_id: int
    hp_cost: int
    mp_cost: int
    category: int
    probability: int
    book_template_id: int
    description: str = ''


class PetSkillRegistry:
    def __init__(self, definitions: list[PetSkillDefinition]):
        self._by_skill = {definition.skill_id: definition for definition in definitions}
        self._by_book = {definition.book_template_id: definition for definition in definitions}
        if len(self._by_skill) != len(definitions):
            raise PetSkillCatalogError('duplicate pet skill_id')
        if len(self._by_book) != len(definitions):
            raise PetSkillCatalogError('duplicate pet skill book_template_id')

    @classmethod
    def from_path(cls, path: str | Path) -> 'PetSkillRegistry':
        source = Path(path)
        try:
            payload = json.loads(source.read_text(encoding='utf-8'))
        except (OSError, ValueError) as exc:
            raise PetSkillCatalogError(f'failed to load pet skill catalog {source}: {exc}') from exc
        if not isinstance(payload, dict) or not isinstance(payload.get('skills'), list):
            raise PetSkillCatalogError('pet skill catalog must contain a skills list')
        definitions: list[PetSkillDefinition] = []
        for raw in payload['skills']:
            if not isinstance(raw, dict):
                raise PetSkillCatalogError('pet skill definition must be an object')
            definition = PetSkillDefinition(
                skill_id=int(raw['skill_id']),
                name=str(raw['name']),
                level=max(1, int(raw.get('level', 1))),
                icon_id=max(0, int(raw.get('icon_id', 0))),
                hp_cost=max(0, int(raw.get('hp_cost', 0))),
                mp_cost=max(0, int(raw.get('mp_cost', 0))),
                category=max(0, int(raw.get('category', 0))),
                probability=max(0, min(100, int(raw.get('probability', 0)))),
                book_template_id=int(raw['book_template_id']),
                description=str(raw.get('description', '')),
            )
            if definition.skill_id <= 0:
                raise PetSkillCatalogError('pet skill_id must be positive')
            if not (399010011 <= definition.book_template_id <= 399050321):
                raise PetSkillCatalogError('pet skill book id must be inside the APK-native filter range')
            definitions.append(definition)
        return cls(definitions)

    def require(self, skill_id: int) -> PetSkillDefinition:
        try:
            return self._by_skill[int(skill_id)]
        except (KeyError, TypeError, ValueError) as exc:
            raise KeyError(f'unknown pet skill {skill_id}') from exc

    def for_book(self, template_id: int) -> PetSkillDefinition | None:
        try:
            return self._by_book.get(int(template_id))
        except (TypeError, ValueError):
            return None

    @property
    def definitions(self) -> tuple[PetSkillDefinition, ...]:
        return tuple(self._by_skill[key] for key in sorted(self._by_skill))


def default_pet_skill_registry() -> PetSkillRegistry:
    return PetSkillRegistry.from_path(Path(__file__).resolve().parent / 'data' / 'pet_skills.json')
