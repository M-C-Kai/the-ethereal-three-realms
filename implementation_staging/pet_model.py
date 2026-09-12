from __future__ import annotations

from pet_registry import PetRegistry


def role_pets(role: dict[str, object]) -> list[dict[str, object]]:
    pets = role.get('pets')
    if not isinstance(pets, list):
        pets = []
        role['pets'] = pets
    return pets


def find_pet(role: dict[str, object], pet_id: int) -> dict[str, object] | None:
    for pet in role_pets(role):
        if not isinstance(pet, dict):
            continue
        try:
            if int(pet.get('id', 0)) == int(pet_id):
                return pet
        except (TypeError, ValueError):
            continue
    return None


def allocate_pet_id(role: dict[str, object]) -> int:
    base = max(1, int(role.get('id', 0)) * 1000 + 1)
    ids: list[int] = []
    for pet in role_pets(role):
        if not isinstance(pet, dict):
            continue
        try:
            ids.append(int(pet.get('id', 0)))
        except (TypeError, ValueError):
            continue
    return max([base - 1, *ids]) + 1


def create_starter_pet(role_id: int, registry: PetRegistry) -> dict[str, object]:
    definition = registry.require(registry.default_template_id)
    return {
        'id': max(1, int(role_id) * 1000 + 1),
        'template_id': definition.template_id,
        'name': definition.name,
        'level': definition.base_level,
        'experience': 0,
        'hp': definition.base_hp,
        'mp': definition.base_mp,
        'life': definition.base_life,
        'deployed': False,
        'walking': False,
        'location': 'bag',
        'base_stats': list(definition.base_stats),
        'remaining_points': 0,
        'qualifications': list(definition.qualifications),
        'insight_points': 0,
        'insight_training': 0,
        'rank': 0,
        'growth_rank': definition.growth_rank,
        'skill_ids': [],
        'bound': False,
        'trade_locked': False,
    }


def ensure_pet_schema(role: dict[str, object], registry: PetRegistry) -> bool:
    """Migrate pet instances without duplicating the existing starter pet."""
    changed = False
    pets = role.get('pets')
    if not isinstance(pets, list):
        role['pets'] = []
        pets = role['pets']
        changed = True

    if not bool(role.get('pets_initialized', False)):
        if not pets:
            pets.append(create_starter_pet(int(role.get('id', 0)), registry))
        role['pets_initialized'] = True
        changed = True

    for pet in pets:
        if not isinstance(pet, dict):
            continue
        try:
            definition = registry.require(int(pet.get('template_id', registry.default_template_id)))
        except (KeyError, TypeError, ValueError):
            continue
        defaults: dict[str, object] = {
            'name': definition.name,
            'level': definition.base_level,
            'experience': 0,
            'hp': definition.base_hp,
            'mp': definition.base_mp,
            'life': definition.base_life,
            'deployed': False,
            'walking': False,
            'location': 'bag',
            'base_stats': list(definition.base_stats),
            'remaining_points': 0,
            'qualifications': list(definition.qualifications),
            'insight_points': 0,
            'insight_training': 0,
            'rank': 0,
            'growth_rank': definition.growth_rank,
            'skill_ids': [],
            'bound': False,
            'trade_locked': False,
        }
        for key, value in defaults.items():
            if key not in pet:
                pet[key] = list(value) if isinstance(value, list) else value
                changed = True
    return changed
