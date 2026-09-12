from __future__ import annotations

from dataclasses import dataclass

from pet_registry import PetRegistry
from protocol import Field, TYPE_BYTE, TYPE_INT, byte, encode_frame, integer, string


PET_ACTION_CREATE = 1
PET_ACTION_DETAIL = 9
PET_SKILL_ACTION_LIST = 10
PET_STATE_DEPLOYED = 10
PET_STATE_WALKING = 48
PET_PROPERTY_UPDATE_ACTION = 0


@dataclass(frozen=True)
class PetStateResult:
    changed: bool
    pet_id: int = 0
    action: int = 0
    enabled: bool = False
    reason: str = ''
    updates: tuple[tuple[int, int, int], ...] = ()


def role_pets(role: dict[str, object]) -> list[dict[str, object]]:
    pets = role.get('pets')
    if not isinstance(pets, list):
        pets = []
        role['pets'] = pets
    return pets


def _starter_pet_id(role_id: int) -> int:
    return max(1, int(role_id) * 1000 + 1)


def create_starter_pet(role_id: int, registry: PetRegistry) -> dict[str, object]:
    definition = registry.require(registry.default_template_id)
    return {
        'id': _starter_pet_id(role_id),
        'template_id': definition.template_id,
        'name': definition.name,
        'level': definition.base_level,
        'experience': 0,
        'life': definition.base_life,
        'deployed': False,
        'walking': False,
        'base_stats': list(definition.base_stats),
        'remaining_points': 0,
        'qualifications': list(definition.qualifications),
        'insight_points': 0,
        'insight_training': 0,
    }


def ensure_role_pets(role: dict[str, object], registry: PetRegistry) -> bool:
    """Migrate one role to the persisted pet schema without duplication."""
    pets = role.get('pets')
    changed = False
    if not isinstance(pets, list):
        role['pets'] = [create_starter_pet(int(role.get('id', 0)), registry)]
        role['pets_initialized'] = True
        return True
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
            'life': definition.base_life,
            'deployed': False,
            'walking': False,
            'base_stats': list(definition.base_stats),
            'remaining_points': 0,
            'qualifications': list(definition.qualifications),
            'insight_points': 0,
            'insight_training': 0,
        }
        for key, value in defaults.items():
            if key not in pet:
                pet[key] = list(value) if isinstance(value, list) else value
                changed = True
    return changed


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


def is_pet_detail_request(fields: list[Field]) -> bool:
    return bool(len(fields) == 2 and fields[0].type_id == TYPE_BYTE and fields[0].value == PET_ACTION_DETAIL and fields[1].type_id == TYPE_INT)


def is_pet_skill_request(fields: list[Field]) -> bool:
    return bool(len(fields) == 2 and fields[0].type_id == TYPE_BYTE and fields[0].value == PET_SKILL_ACTION_LIST and fields[1].type_id == TYPE_INT)


def is_pet_state_request(fields: list[Field]) -> bool:
    return bool(
        len(fields) == 3
        and fields[0].type_id == TYPE_BYTE
        and fields[0].value in (PET_STATE_DEPLOYED, PET_STATE_WALKING)
        and fields[1].type_id == TYPE_INT
        and fields[2].type_id == TYPE_BYTE
        and fields[2].value in (0, 1)
    )


def pet_instance_frame(pet: dict[str, object], registry: PetRegistry) -> bytes:
    definition = registry.require(int(pet['template_id']))
    name = str(pet.get('name') or definition.name)
    level = max(1, int(pet.get('level', definition.base_level)))
    return encode_frame(1127, [
        byte(PET_ACTION_CREATE),
        integer(int(pet['id'])),
        integer(definition.model_dat_id),
        string(name),
        integer(0),
        integer(0),
        integer(definition.growth_rank),
        integer(level),
        integer(0),
        integer(definition.carry_level),
        integer(0),
        integer(1 if bool(pet.get('deployed', False)) else 0),
        integer(1 if bool(pet.get('walking', False)) else 0),
    ])


def role_pet_frames(role: dict[str, object], registry: PetRegistry) -> tuple[bytes, ...]:
    return tuple(
        pet_instance_frame(pet, registry)
        for pet in role_pets(role)
        if isinstance(pet, dict) and int(pet.get('id', 0)) > 0
    )


def pet_detail_properties(pet: dict[str, object], registry: PetRegistry) -> dict[int, object]:
    """Build the APK-confirmed contiguous 1127/action=9 properties 30..90."""
    definition = registry.require(int(pet['template_id']))
    level = max(1, int(pet.get('level', definition.base_level)))
    values: dict[int, object] = {property_id: 0 for property_id in range(30, 91)}
    values[30] = max(0, int(pet.get('experience', 0)))
    values[31] = max(100, level * 100)
    raw_stats = list(pet.get('base_stats', definition.base_stats))
    for property_id, value in enumerate((raw_stats + list(definition.base_stats))[:5], start=32):
        values[property_id] = max(0, int(value))
    values[37] = max(0, int(pet.get('remaining_points', 0)))
    max_hp = max(1, int(definition.base_hp) + ((level - 1) * 10))
    max_mp = max(1, int(definition.base_mp) + ((level - 1) * 5))
    values[38] = max(0, min(max_hp, int(pet.get('hp', max_hp))))
    values[39] = max_hp
    values[40] = max(0, min(max_mp, int(pet.get('mp', max_mp))))
    values[41] = max_mp
    values[42] = max(0, int(definition.physical_attack) + ((level - 1) * 2))
    values[43] = max(0, int(definition.magic_attack) + ((level - 1) * 2))
    values[44] = max(0, int(definition.physical_defense) + (level - 1))
    values[45] = max(0, int(definition.magic_defense) + (level - 1))
    values[46] = max(0, int(definition.speed) + (level - 1))
    raw_qualifications = list(pet.get('qualifications', definition.qualifications))
    for property_id, value in enumerate((raw_qualifications + list(definition.qualifications))[:12], start=47):
        values[property_id] = max(0, int(value))
    values[59] = max(0, int(pet.get('life', definition.base_life)))
    values[60] = int(definition.pet_type)
    values[73] = max(0, int(pet.get('insight_points', 0)))
    values[76] = max(0, int(pet.get('insight_training', 0)))
    values[77] = max(1, int(definition.insight_training_max))
    values[78] = max(0, int(definition.divine_power))
    values[79] = str(definition.species_name or definition.name)
    values[80] = max(0, min(4, int(definition.growth_rank)))
    values[81] = max(0, int(definition.innate_divine_power))
    values[82] = max(0, int(definition.carry_level))
    values[83] = str(definition.standard_skill)
    for property_id, value in enumerate((list(definition.growth_values) + [700] * 7)[:7], start=84):
        values[property_id] = max(500, int(value))
    return values


def pet_detail_frame(pet: dict[str, object], registry: PetRegistry) -> bytes:
    properties = pet_detail_properties(pet, registry)
    fields: list[Field] = [byte(PET_ACTION_DETAIL), integer(int(pet['id']))]
    for property_id in range(30, 91):
        value = properties[property_id]
        fields.append(string(value) if property_id in (79, 83) else integer(int(value)))
    return encode_frame(1127, fields)


def pet_skill_list_frame(pet: dict[str, object]) -> bytes:
    return encode_frame(1103, [byte(PET_SKILL_ACTION_LIST), integer(int(pet['id'])), byte(0), byte(0)])


def pet_property_update_frame(pet_id: int, updates: list[tuple[int, int]] | tuple[tuple[int, int], ...]) -> bytes:
    fields: list[Field] = [byte(PET_PROPERTY_UPDATE_ACTION), integer(int(pet_id)), integer(len(updates))]
    for property_id, value in updates:
        fields.extend((byte(int(property_id)), integer(int(value))))
    return encode_frame(1134, fields)


def apply_pet_state_request(role: dict[str, object], fields: list[Field]) -> PetStateResult:
    if not is_pet_state_request(fields):
        return PetStateResult(False, reason='invalid_request')
    action = int(fields[0].value)
    pet_id = int(fields[1].value)
    enabled = bool(int(fields[2].value))
    pet = find_pet(role, pet_id)
    if pet is None:
        return PetStateResult(False, pet_id=pet_id, action=action, enabled=enabled, reason='unknown_pet')
    key = 'deployed' if action == PET_STATE_DEPLOYED else 'walking'
    property_id = 11 if action == PET_STATE_DEPLOYED else 12
    changed = False
    updates: list[tuple[int, int, int]] = []
    if enabled:
        for candidate in role_pets(role):
            if not isinstance(candidate, dict) or candidate is pet:
                continue
            if bool(candidate.get(key, False)):
                candidate[key] = False
                changed = True
                updates.append((int(candidate.get('id', 0)), property_id, 0))
    if bool(pet.get(key, False)) != enabled:
        pet[key] = enabled
        changed = True
    updates.append((pet_id, property_id, 1 if enabled else 0))
    return PetStateResult(changed, pet_id=pet_id, action=action, enabled=enabled, updates=tuple(updates))
