from __future__ import annotations

from dataclasses import dataclass

from pet_model import find_pet, role_pets
from pet_registry import PetRegistry


@dataclass(frozen=True)
class PetMutation:
    changed: bool
    pet_id: int = 0
    updates: tuple[tuple[int, int], ...] = ()
    reason: str = ''
    name: str = ''
    was_walking: bool = False
    was_deployed: bool = False


def _bag_pet(role: dict[str, object], pet_id: int) -> dict[str, object] | None:
    pet = find_pet(role, pet_id)
    if pet is None or str(pet.get('location', 'bag')) != 'bag':
        return None
    return pet


def rename_pet(role: dict[str, object], pet_id: int, new_name: str) -> PetMutation:
    pet = _bag_pet(role, pet_id)
    if pet is None:
        return PetMutation(False, pet_id, reason='unknown_pet')
    name = str(new_name).strip()
    if not name:
        return PetMutation(False, pet_id, reason='empty_name')
    if len(name.encode('utf-8')) > 30:
        return PetMutation(False, pet_id, reason='name_too_long')
    if str(pet.get('name', '')) == name:
        return PetMutation(False, pet_id, reason='no_change', name=name)
    pet['name'] = name
    return PetMutation(True, pet_id, name=name)


def release_pet(role: dict[str, object], pet_id: int) -> PetMutation:
    pet = _bag_pet(role, pet_id)
    if pet is None:
        return PetMutation(False, pet_id, reason='unknown_pet')
    was_walking = bool(pet.get('walking', False))
    was_deployed = bool(pet.get('deployed', False))
    pet['walking'] = False
    pet['deployed'] = False
    role_pets(role).remove(pet)
    return PetMutation(
        True,
        pet_id,
        reason='',
        was_walking=was_walking,
        was_deployed=was_deployed,
    )


def recalculate_pet_properties(pet: dict[str, object], registry: PetRegistry) -> dict[int, int]:
    definition = registry.require(int(pet['template_id']))
    level = max(1, int(pet.get('level', definition.base_level)))
    stats = list(pet.get('base_stats', definition.base_stats))
    stats = (stats + list(definition.base_stats))[:5]

    # Keep one centralized derived-stat rule so detail and incremental updates agree.
    strength, endurance, intelligence, spirit, agility = [max(0, int(value)) for value in stats]
    max_hp = max(1, int(definition.base_hp) + ((level - 1) * 10) + endurance * 2)
    max_mp = max(1, int(definition.base_mp) + ((level - 1) * 5) + spirit)
    physical_attack = max(0, int(definition.physical_attack) + ((level - 1) * 2) + strength)
    magic_attack = max(0, int(definition.magic_attack) + ((level - 1) * 2) + intelligence)
    physical_defense = max(0, int(definition.physical_defense) + (level - 1) + endurance)
    magic_defense = max(0, int(definition.magic_defense) + (level - 1) + spirit)
    speed = max(0, int(definition.speed) + (level - 1) + agility)

    current_hp = max(0, min(max_hp, int(pet.get('hp', max_hp))))
    current_mp = max(0, min(max_mp, int(pet.get('mp', max_mp))))
    pet['hp'] = current_hp
    pet['mp'] = current_mp
    return {
        38: current_hp,
        39: max_hp,
        40: current_mp,
        41: max_mp,
        42: physical_attack,
        43: magic_attack,
        44: physical_defense,
        45: magic_defense,
        46: speed,
    }


def allocate_stats(
    role: dict[str, object],
    pet_id: int,
    deltas: tuple[int, int, int, int, int],
    registry: PetRegistry,
) -> PetMutation:
    pet = _bag_pet(role, pet_id)
    if pet is None:
        return PetMutation(False, pet_id, reason='unknown_pet')
    if len(deltas) != 5 or any(int(value) < 0 for value in deltas):
        return PetMutation(False, pet_id, reason='invalid_points')

    spend = sum(int(value) for value in deltas)
    remaining = max(0, int(pet.get('remaining_points', 0)))
    if spend <= 0:
        return PetMutation(False, pet_id, reason='no_change')
    if spend > remaining:
        return PetMutation(False, pet_id, reason='insufficient_points')

    definition = registry.require(int(pet['template_id']))
    stats = list(pet.get('base_stats', definition.base_stats))
    stats = (stats + list(definition.base_stats))[:5]
    pet['base_stats'] = [int(stats[index]) + int(deltas[index]) for index in range(5)]
    pet['remaining_points'] = remaining - spend

    updates: list[tuple[int, int]] = [
        (32 + index, int(pet['base_stats'][index]))
        for index in range(5)
    ]
    updates.append((37, int(pet['remaining_points'])))
    derived = recalculate_pet_properties(pet, registry)
    updates.extend((property_id, derived[property_id]) for property_id in range(38, 47))
    return PetMutation(True, pet_id, updates=tuple(updates))
