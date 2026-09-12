from __future__ import annotations

from dataclasses import dataclass

from pet_registry import PetRegistry
from protocol import Field, TYPE_BYTE, TYPE_INT, byte, encode_frame, integer, string


PET_ACTION_CREATE = 1
PET_STATE_DEPLOYED = 10
PET_STATE_WALKING = 48


@dataclass(frozen=True)
class PetStateResult:
    changed: bool
    pet_id: int = 0
    action: int = 0
    enabled: bool = False
    reason: str = ''


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
    }


def ensure_role_pets(role: dict[str, object], registry: PetRegistry) -> bool:
    """Migrate one role to the minimal persisted pet schema without duplication."""
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
        defaults = {
            'name': definition.name,
            'level': definition.base_level,
            'experience': 0,
            'life': definition.base_life,
            'deployed': False,
            'walking': False,
        }
        for key, value in defaults.items():
            if key not in pet:
                pet[key] = value
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


def pet_instance_frame(pet: dict[str, object], registry: PetRegistry) -> bytes:
    """Encode APK 1127/action=1 through property 12 only.

    Reverse-engineered ``main/e.aa(w)`` action 1 reads field[1] as the pet
    instance id, constructs ``b/u``, then loops field indexes 2..N and stores
    each object with the field index itself as the pet property id.  Therefore
    this minimal record intentionally stops at property 12 instead of guessing
    any unconfirmed later field layout.
    """
    definition = registry.require(int(pet['template_id']))
    name = str(pet.get('name') or definition.name)
    level = max(1, int(pet.get('level', definition.base_level)))
    fields = [
        byte(PET_ACTION_CREATE),               # field 0: action
        integer(int(pet['id'])),               # field 1: instance id
        integer(definition.model_dat_id),       # property 2: body dat/resource id
        string(name),                           # property 3: display name
        integer(0),                             # property 4: animation config (unknown; neutral)
        integer(0),                             # property 5: animation config (unknown; neutral)
        integer(0),                             # property 6: not required by list view
        integer(level),                         # property 7: level
        integer(0),                             # property 8: unneeded by minimal list
        integer(0),                             # property 9: unneeded by minimal list
        integer(0),                             # property 10: unneeded by minimal list
        integer(1 if bool(pet.get('deployed', False)) else 0),
        integer(1 if bool(pet.get('walking', False)) else 0),
    ]
    return encode_frame(1127, fields)


def role_pet_frames(role: dict[str, object], registry: PetRegistry) -> tuple[bytes, ...]:
    return tuple(
        pet_instance_frame(pet, registry)
        for pet in role_pets(role)
        if isinstance(pet, dict) and int(pet.get('id', 0)) > 0
    )


def apply_pet_state_request(role: dict[str, object], fields: list[Field]) -> PetStateResult:
    """Apply confirmed C->S 1130 [BYTE action, INT petId, BYTE enabled]."""
    if not (
        len(fields) == 3
        and fields[0].type_id == TYPE_BYTE
        and fields[0].value in (PET_STATE_DEPLOYED, PET_STATE_WALKING)
        and fields[1].type_id == TYPE_INT
        and fields[2].type_id == TYPE_BYTE
        and fields[2].value in (0, 1)
    ):
        return PetStateResult(False, reason='invalid_request')

    action = int(fields[0].value)
    pet_id = int(fields[1].value)
    enabled = bool(int(fields[2].value))
    pet = find_pet(role, pet_id)
    if pet is None:
        return PetStateResult(False, pet_id=pet_id, action=action, enabled=enabled, reason='unknown_pet')

    key = 'deployed' if action == PET_STATE_DEPLOYED else 'walking'
    changed = bool(pet.get(key, False)) != enabled
    if enabled:
        for candidate in role_pets(role):
            if not isinstance(candidate, dict) or candidate is pet:
                continue
            if bool(candidate.get(key, False)):
                candidate[key] = False
                changed = True
    pet[key] = enabled
    return PetStateResult(changed, pet_id=pet_id, action=action, enabled=enabled)
