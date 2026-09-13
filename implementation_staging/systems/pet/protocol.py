"""宠物系统 APK 原生协议帧与请求解析。"""
from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from protocol import (
    Field,
    TYPE_BYTE,
    TYPE_INT,
    TYPE_SHORT,
    TYPE_STRING,
    byte,
    encode_frame,
    integer,
    short,
    string,
)
from systems.pet.registry import (
    PetRegistry,
    PetSkillDefinition,
    PetSkillRegistry,
    default_pet_skill_registry,
)
from systems.pet.service import (
    ensure_pet_schema,
    find_pet,
    recalculate_pet_properties,
    role_pets,
)


PET_ACTION_CREATE = 1
PET_ACTION_DETAIL = 9
PET_SKILL_ACTION_LIST = 10
PET_SKILL_ACTION_LEARN = 50
PET_STATE_DEPLOYED = 10
PET_STATE_WALKING = 48
PET_PROPERTY_UPDATE_ACTION = 0
PET_RENAME_ACTION = 15
PET_RELEASE_ACTION = 1
PET_STAT_ACTION = 2
PET_MAP_ATTACH_ACTION = 13
PET_MAP_DETACH_ACTION = 102
PET_SKILL_RECORD_WIDTH = 27


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


def pet_skill_record_fields(definition: PetSkillDefinition) -> list[Field]:
    """Encode one b/w-compatible 27-property skill record.

    Reverse-engineering locks property 0 as display name and property 1 as
    skill id.  The known runtime-safe numeric slots below are populated from
    the catalog; every still-unresolved property remains zero rather than
    inventing protocol semantics.
    """
    values = [0] * PET_SKILL_RECORD_WIDTH
    values[1] = int(definition.skill_id)
    values[2] = 1
    values[3] = int(definition.level)
    values[4] = int(definition.icon_id)
    values[5] = int(definition.hp_cost)
    values[6] = int(definition.mp_cost)
    values[10] = int(definition.category)
    values[11] = int(definition.probability)
    fields: list[Field] = [string(definition.name)]
    fields.extend(integer(values[index]) for index in range(1, PET_SKILL_RECORD_WIDTH))
    return fields


def pet_skill_list_frame(
    pet: dict[str, object],
    skill_registry: PetSkillRegistry | None = None,
) -> bytes:
    if skill_registry is None:
        skill_registry = default_pet_skill_registry()
    definitions: list[PetSkillDefinition] = []
    raw_ids = pet.get('skill_ids', [])
    if isinstance(raw_ids, list):
        for raw_skill_id in raw_ids:
            try:
                definition = skill_registry.require(int(raw_skill_id))
            except (KeyError, TypeError, ValueError):
                continue
            if definition not in definitions:
                definitions.append(definition)
    definitions = definitions[:255]
    fields: list[Field] = [
        byte(PET_SKILL_ACTION_LIST),
        integer(int(pet['id'])),
        byte(0),
        byte(len(definitions)),
    ]
    for definition in definitions:
        fields.extend(pet_skill_record_fields(definition))
    return encode_frame(1103, fields)


def parse_pet_skill_learn_request(fields: list[Field]) -> tuple[int, int, int] | None:
    if (
        len(fields) != 4
        or fields[0].type_id != TYPE_BYTE
        or int(fields[0].value) != PET_SKILL_ACTION_LEARN
        or any(field.type_id != TYPE_INT for field in fields[1:])
    ):
        return None
    return int(fields[1].value), int(fields[2].value), int(fields[3].value)


def pet_skill_learn_result_frame(
    pet_id: int,
    *,
    success: bool,
    forgotten_skill_id: int = 0,
) -> bytes:
    return encode_frame(1130, [
        byte(PET_SKILL_ACTION_LEARN),
        integer(int(pet_id)),
        integer(1 if success else 0),
        integer(int(forgotten_skill_id)),
    ])


def pet_property_update_frame(
    pet_id: int,
    updates: Sequence[tuple[int, int]],
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


def parse_pet_rename_request(fields: list[Field]) -> tuple[int, str] | None:
    if (
        len(fields) != 3
        or fields[0].type_id != TYPE_BYTE
        or int(fields[0].value) != PET_RENAME_ACTION
        or fields[1].type_id != TYPE_INT
        or fields[2].type_id != TYPE_STRING
    ):
        return None
    return int(fields[1].value), str(fields[2].value)


def pet_rename_frame(pet_id: int, name: str) -> bytes:
    return encode_frame(1130, [byte(PET_RENAME_ACTION), integer(pet_id), string(name)])


def parse_pet_release_request(fields: list[Field]) -> int | None:
    if (
        len(fields) != 2
        or fields[0].type_id != TYPE_BYTE
        or int(fields[0].value) != PET_RELEASE_ACTION
        or fields[1].type_id != TYPE_INT
    ):
        return None
    return int(fields[1].value)


def pet_release_frame(pet_id: int) -> bytes:
    return encode_frame(1130, [byte(PET_RELEASE_ACTION), integer(pet_id)])


def parse_pet_stat_request(fields: list[Field]) -> tuple[int, tuple[int, int, int, int, int]] | None:
    if (
        len(fields) != 7
        or fields[0].type_id != TYPE_INT
        or fields[1].type_id != TYPE_SHORT
        or int(fields[1].value) != PET_STAT_ACTION
        or any(field.type_id != TYPE_SHORT for field in fields[2:])
    ):
        return None
    values = tuple(int(field.value) for field in fields[2:])
    return int(fields[0].value), (values[0], values[1], values[2], values[3], values[4])


def pet_map_attach_frame(pet_id: int, role_id: int) -> bytes:
    return encode_frame(1127, [
        byte(PET_MAP_ATTACH_ACTION),
        integer(int(pet_id)),
        integer(int(role_id)),
    ])


def pet_map_detach_frame(role_id: int) -> bytes:
    return encode_frame(1010, [
        integer(int(role_id)),
        short(0),
        short(0),
        integer(0),
        integer(0),
        short(PET_MAP_DETACH_ACTION),
    ])


def pet_state_response_frames(role_id: int, result: PetStateResult) -> tuple[bytes, ...]:
    frames = [
        pet_property_update_frame(pet_id, [(property_id, value)])
        for pet_id, property_id, value in result.updates
    ]
    if result.action == PET_STATE_WALKING and not result.reason:
        if result.enabled:
            frames.append(pet_map_attach_frame(result.pet_id, role_id))
        else:
            frames.append(pet_map_detach_frame(role_id))
    return tuple(frames)
