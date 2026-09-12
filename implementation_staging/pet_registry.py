from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


class PetCatalogError(ValueError):
    pass


def _int_tuple(
    raw: object,
    *,
    length: int,
    default: tuple[int, ...],
    minimum: int = 0,
) -> tuple[int, ...]:
    if not isinstance(raw, list):
        return default
    values: list[int] = []
    for value in raw[:length]:
        try:
            values.append(max(minimum, int(value)))
        except (TypeError, ValueError):
            values.append(default[len(values)])
    while len(values) < length:
        values.append(default[len(values)])
    return tuple(values)


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
    species_name: str = ''
    base_hp: int = 100
    base_mp: int = 50
    physical_attack: int = 20
    magic_attack: int = 15
    physical_defense: int = 10
    magic_defense: int = 10
    speed: int = 10
    base_stats: tuple[int, ...] = (10, 10, 10, 10, 10)
    qualifications: tuple[int, ...] = (
        70, 100, 70, 100, 70, 100,
        70, 100, 70, 100, 70, 100,
    )
    innate_divine_power: int = 0
    divine_power: int = 0
    standard_skill: str = '无'
    growth_values: tuple[int, ...] = (700, 700, 700, 700, 700, 700, 700)
    insight_training_max: int = 100
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
            name = str(raw['name'])
            definition = PetDefinition(
                template_id=int(raw['template_id']),
                name=name,
                model_dat_id=int(raw['model_dat_id']),
                pet_type=int(raw.get('pet_type', 1)),
                base_level=max(1, int(raw.get('base_level', 1))),
                carry_level=max(0, int(raw.get('carry_level', 1))),
                growth_rank=max(0, min(4, int(raw.get('growth_rank', 0)))),
                base_life=max(1, int(raw.get('base_life', 100))),
                species_name=str(raw.get('species_name', name)),
                base_hp=max(1, int(raw.get('base_hp', 100))),
                base_mp=max(1, int(raw.get('base_mp', 50))),
                physical_attack=max(0, int(raw.get('physical_attack', 20))),
                magic_attack=max(0, int(raw.get('magic_attack', 15))),
                physical_defense=max(0, int(raw.get('physical_defense', 10))),
                magic_defense=max(0, int(raw.get('magic_defense', 10))),
                speed=max(0, int(raw.get('speed', 10))),
                base_stats=_int_tuple(raw.get('base_stats'), length=5, default=(10, 10, 10, 10, 10)),
                qualifications=_int_tuple(
                    raw.get('qualifications'), length=12,
                    default=(70, 100, 70, 100, 70, 100, 70, 100, 70, 100, 70, 100),
                ),
                innate_divine_power=max(0, int(raw.get('innate_divine_power', 0))),
                divine_power=max(0, int(raw.get('divine_power', 0))),
                standard_skill=str(raw.get('standard_skill', '无')),
                growth_values=_int_tuple(
                    raw.get('growth_values'), length=7,
                    default=(700, 700, 700, 700, 700, 700, 700), minimum=500,
                ),
                insight_training_max=max(1, int(raw.get('insight_training_max', 100))),
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
