from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


class PetCatalogError(ValueError):
    pass


@dataclass(frozen=True)
class PetDefinition:
    template_id: int
    name: str
    model_dat_id: int
    pet_type: int
    base_level: int = 1
    carry_level: int = 1
    growth_rank: int = 0
    base_life: int = 100
    status: str = 'candidate_renderable'
    notes: str = ''


class PetRegistry:
    def __init__(self, definitions: list[PetDefinition], default_template_id: int):
        self._by_id = {definition.template_id: definition for definition in definitions}
        if len(self._by_id) != len(definitions):
            raise PetCatalogError('duplicate pet template_id')
        if default_template_id not in self._by_id:
            raise PetCatalogError(f'default pet template {default_template_id} is missing')
        self.default_template_id = int(default_template_id)

    @classmethod
    def from_path(cls, path: str | Path) -> 'PetRegistry':
        source = Path(path)
        try:
            payload = json.loads(source.read_text(encoding='utf-8'))
        except (OSError, ValueError) as exc:
            raise PetCatalogError(f'failed to load pet catalog {source}: {exc}') from exc
        if not isinstance(payload, dict):
            raise PetCatalogError('pet catalog root must be an object')
        raw_pets = payload.get('pets')
        if not isinstance(raw_pets, list) or not raw_pets:
            raise PetCatalogError('pet catalog must contain at least one pet')
        definitions: list[PetDefinition] = []
        for raw in raw_pets:
            if not isinstance(raw, dict):
                raise PetCatalogError('pet definition must be an object')
            definition = PetDefinition(
                template_id=int(raw['template_id']),
                name=str(raw['name']),
                model_dat_id=int(raw['model_dat_id']),
                pet_type=int(raw.get('pet_type', 1)),
                base_level=max(1, int(raw.get('base_level', 1))),
                carry_level=max(0, int(raw.get('carry_level', 1))),
                growth_rank=max(0, int(raw.get('growth_rank', 0))),
                base_life=max(1, int(raw.get('base_life', 100))),
                status=str(raw.get('status', 'candidate_renderable')),
                notes=str(raw.get('notes', '')),
            )
            if definition.template_id <= 0:
                raise PetCatalogError('pet template_id must be positive')
            if definition.model_dat_id <= 0:
                raise PetCatalogError('pet model_dat_id must be positive')
            if definition.pet_type not in (0, 1):
                raise PetCatalogError('pet_type must be 0 (wild) or 1 (baby)')
            definitions.append(definition)
        default_template_id = int(payload.get('default_template_id', definitions[0].template_id))
        return cls(definitions, default_template_id)

    def require(self, template_id: int) -> PetDefinition:
        try:
            return self._by_id[int(template_id)]
        except (KeyError, TypeError, ValueError) as exc:
            raise KeyError(f'unknown pet template {template_id}') from exc

    @property
    def definitions(self) -> tuple[PetDefinition, ...]:
        return tuple(self._by_id[key] for key in sorted(self._by_id))


def default_pet_registry() -> PetRegistry:
    return PetRegistry.from_path(Path(__file__).resolve().parent / 'data' / 'pets.json')
