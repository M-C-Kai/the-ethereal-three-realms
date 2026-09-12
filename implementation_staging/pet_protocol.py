from __future__ import annotations

from dataclasses import dataclass

from pet_model import (
    create_starter_pet,
    ensure_pet_schema,
    find_pet,
    role_pets,
)
from pet_registry import PetRegistry
from pet_service import recalculate_pet_properties
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


def ensure_role_pets(role: dict[str, object], registry: PetRegistry) -> bool:
    """Backward-compatible facade for the authoritative pet schema migration."""
    return ensure_pet_schema(role, registry)


def is_pet_detail_request(fields: list[Field]) -> bool:
    return bool(
        len(fields) == 2
        and fields[0].type_id == TYPE_BYTE
        and fields[0].value == PET_ACTION_DETAIL
        and fields[1].type_id == TYPE_INT
    )


def is_pet_skill_request(fields: list[Field]) -> bool:
    return bool(
        len(fields) == 2
        and fields[0].type_id == TYPE_BYTE
        and fields[0].value == PET_SKILL_ACTION_LIST
        and fields[1].type_id == TYPE_INT
    )


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
        integer(int(pet.get('rank', 0))),
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
        if (
            isinstance(pet, dict)
            and int(pet.get('id', 0)) > 0
            and str(pet.get('location', 'bag')) == 'bag'
        )
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
    values.update(recalculate_pet_properties(pet, registry))

    raw_qualifications = list(pet.get('qualifications', definition.qualifications))
    for property_id, value in enumerate((raw_qualifications + list(definition.qualifications))[:12], start=47):
        values[property_id] = max(0, int(value))

    values[59] = max(0, int(pet.get('life', definition.base_life)))
    values[60] = int(definition.pet_type)
    values[73] = max(0, int(pet.get('insight_points', 0)))
    values[76] = max(0, int(pet.get('insight_training', 0)))
    values[77] = max(1, int(definition.insight_training_max))
    values[78] = max(0, int(pet.get('rank', 0)))
    values[79] = str(definition.species_name or definition.name)
    values[80] = max(0, min(4, int(pet.get('growth_rank', definition.growth_rank))))
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
    return encode_frame(1103, [
        byte(PET_SKILL_ACTION_LIST),
        integer(int(pet['id'])),
        byte(0),
        byte(0),
    ])


def pet_property_update_frame(
    pet_id: int,
    updates: list[tuple[int, int]] | tuple[tuple[int, int], ...],
) -> bytes:
    fields: list[Field] = [
        byte(PET_PROPERTY_UPDATE_ACTION),
        integer(int(pet_id)),
        integer(len(updates)),
    ]
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
    if pet is None or str(pet.get('location', 'bag')) != 'bag':
        return PetStateResult(False, pet_id=pet_id, action=action, enabled=enabled, reason='unknown_pet')

    key = 'deployed' if action == PET_STATE_DEPLOYED else 'walking'
    property_id = 11 if action == PET_STATE_DEPLOYED else 12
    changed = False
    updates: list[tuple[int, int, int]] = []
    if enabled:
        for candidate in role_pets(role):
            if not isinstance(candidate, dict) or candidate is pet:
                continue
            if str(candidate.get('location', 'bag')) != 'bag':
                continue
            if bool(candidate.get(key, False)):
                candidate[key] = False
                changed = True
                updates.append((int(candidate.get('id', 0)), property_id, 0))
    if bool(pet.get(key, False)) != enabled:
        pet[key] = enabled
        changed = True
    updates.append((pet_id, property_id, 1 if enabled else 0))
    return PetStateResult(
        changed,
        pet_id=pet_id,
        action=action,
        enabled=enabled,
        updates=tuple(updates),
    )
