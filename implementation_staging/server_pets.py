from __future__ import annotations

import contextvars
import logging

import server as _server
import server_dynamic_maps as _dynamic
from pet_protocol import (
    apply_pet_state_request,
    ensure_role_pets,
    find_pet,
    is_pet_detail_request,
    is_pet_skill_request,
    is_pet_state_request,
    pet_detail_frame,
    pet_property_update_frame,
    pet_skill_list_frame,
    role_pet_frames,
)
from pet_registry import default_pet_registry
from protocol import TYPE_BYTE, TYPE_INT, byte, integer


LOG = logging.getLogger('piaomiao-local')
PET_REGISTRY = default_pet_registry()

# Internal-only actions used to route pet requests through the base server's
# existing 1103 response branch. They never appear on the wire.
_INTERNAL_PET_SKILL_ACTION = 248
_INTERNAL_PET_DETAIL_ACTION = 249
_INTERNAL_PET_STATE_ACTION = 250

_ORIGINAL_DEFAULT_ROLE = _server.default_role
_ORIGINAL_ROLE_ENTRY_FRAMES = _server.role_entry_frames
_ORIGINAL_ROLES_FOR = _server.RoleStore.roles_for
_ORIGINAL_ROLE_CREATE = _server.RoleStore.create
_ORIGINAL_DECODE_PAYLOAD = _server.decode_payload
_ORIGINAL_HANDLE_SECT_SKILL_REQUEST = _server.LocalGameServer.handle_sect_skill_request

_ACTIVE_ROLE: contextvars.ContextVar[dict[str, object] | None] = contextvars.ContextVar(
    'piaomiao_active_pet_role',
    default=None,
)


def pet_default_role(settings):
    """Give a newly materialized default role one persisted starter pet."""
    role = _ORIGINAL_DEFAULT_ROLE(settings)
    ensure_role_pets(role, PET_REGISTRY)
    return role


def pet_roles_for(store, username: str, *, create_default: bool = True):
    """Migrate legacy roles in-place without touching unrelated role fields."""
    roles = _ORIGINAL_ROLES_FOR(store, username, create_default=create_default)
    changed = False
    for role in roles:
        if not isinstance(role, dict):
            continue
        changed = ensure_role_pets(role, PET_REGISTRY) or changed
    if changed:
        store.save()
        LOG.info('PET_MIGRATION user=%r role_count=%d', username, len(roles))
    return roles


def pet_create_role(store, username: str, name: str, model: int, requested_slot: int):
    """Attach the starter pet to newly created characters before returning them."""
    role = _ORIGINAL_ROLE_CREATE(store, username, name, model, requested_slot)
    if ensure_role_pets(role, PET_REGISTRY):
        store.save()
    return role


def pet_role_entry_frames(settings, role: dict[str, object]) -> tuple[bytes, ...]:
    """Append APK-native 1127/action=1 pet instances after normal role init."""
    ensure_role_pets(role, PET_REGISTRY)
    _ACTIVE_ROLE.set(role)
    frames = _ORIGINAL_ROLE_ENTRY_FRAMES(settings, role)
    pet_frames = role_pet_frames(role, PET_REGISTRY)
    LOG.info(
        'PET_1127_DOWNLINK role_id=%d pet_count=%d ids=%r',
        int(role.get('id', 0)),
        len(pet_frames),
        [int(pet.get('id', 0)) for pet in role.get('pets', []) if isinstance(pet, dict)],
    )
    return (*frames, *pet_frames)


def _translate_roaming_boss_fight_request(message_id: int, fields):
    """Bridge the APK-native q-monster fight request into the server's battle route."""
    if (
        message_id == 2029
        and len(fields) >= 2
        and fields[0].type_id == TYPE_BYTE
        and int(fields[0].value) == 1
        and fields[1].type_id == TYPE_INT
        and int(fields[1].value) == _dynamic.ROAMING_BOSS_ID
    ):
        LOG.info(
            'MAP_BOSS_NATIVE_FIGHT_BRIDGE protocol=2029 action=1 actor=%d -> protocol=2031',
            _dynamic.ROAMING_BOSS_ID,
        )
        return 2031, [integer(_dynamic.ROAMING_BOSS_ID)]
    return message_id, fields


def pet_decode_payload(payload: bytes):
    """Route confirmed pet requests into a response-capable base-server branch.

    The base server has no 1127/1130 branches yet, while its 1103 branch calls
    one overridable handler and sends every returned frame. Exact APK-shaped
    pet requests are therefore translated to internal-only 1103 actions after
    decoding; all wire responses retain their real protocol ids (1127/1103/1134).
    """
    message_id, fields = _ORIGINAL_DECODE_PAYLOAD(payload)
    message_id, fields = _translate_roaming_boss_fight_request(message_id, fields)

    role = _ACTIVE_ROLE.get()
    if role is None:
        return message_id, fields

    if message_id == 1127 and is_pet_detail_request(fields):
        pet_id = int(fields[1].value)
        if find_pet(role, pet_id) is not None:
            LOG.info('PET_1127_DETAIL_REQUEST role_id=%d pet_id=%d', int(role.get('id', 0)), pet_id)
            return 1103, [byte(_INTERNAL_PET_DETAIL_ACTION), integer(pet_id)]

    if message_id == 1103 and is_pet_skill_request(fields):
        pet_id = int(fields[1].value)
        if find_pet(role, pet_id) is not None:
            LOG.info('PET_1103_SKILL_REQUEST role_id=%d pet_id=%d', int(role.get('id', 0)), pet_id)
            return 1103, [byte(_INTERNAL_PET_SKILL_ACTION), integer(pet_id)]

    if message_id == 1130 and is_pet_state_request(fields):
        pet_id = int(fields[1].value)
        if find_pet(role, pet_id) is not None:
            action = int(fields[0].value)
            enabled = int(fields[2].value)
            return 1103, [
                byte(_INTERNAL_PET_STATE_ACTION),
                integer(pet_id),
                byte(action),
                byte(enabled),
            ]

    return message_id, fields


def pet_handle_sect_skill_request(
    server,
    role: dict[str, object],
    values: list[object],
) -> tuple[bytes, ...]:
    """Serve pet detail/skill/state requests routed through protocol 1103."""
    action = int(values[0]) if values else -1

    if action == _INTERNAL_PET_DETAIL_ACTION and len(values) >= 2:
        pet_id = int(values[1])
        pet = find_pet(role, pet_id)
        if pet is None:
            return ()
        LOG.info(
            'PET_1127_DETAIL role_id=%d pet_id=%d properties=30..90',
            int(role.get('id', 0)),
            pet_id,
        )
        return (pet_detail_frame(pet, PET_REGISTRY),)

    if action == _INTERNAL_PET_SKILL_ACTION and len(values) >= 2:
        pet_id = int(values[1])
        pet = find_pet(role, pet_id)
        if pet is None:
            return ()
        LOG.info(
            'PET_1103_SKILLS role_id=%d pet_id=%d count=0',
            int(role.get('id', 0)),
            pet_id,
        )
        return (pet_skill_list_frame(pet),)

    if action == _INTERNAL_PET_STATE_ACTION and len(values) >= 4:
        pet_id = int(values[1])
        state_action = int(values[2])
        enabled = int(values[3])
        result = apply_pet_state_request(
            role,
            [byte(state_action), integer(pet_id), byte(enabled)],
        )
        if result.changed:
            server.roles.save()

        frames = tuple(
            pet_property_update_frame(update_pet_id, [(property_id, value)])
            for update_pet_id, property_id, value in result.updates
        )
        LOG.info(
            'PET_1130_STATE role_id=%d pet_id=%d action=%d enabled=%s changed=%s '
            'updates=%r reason=%s',
            int(role.get('id', 0)),
            result.pet_id,
            result.action,
            result.enabled,
            result.changed,
            result.updates,
            result.reason,
        )
        return frames

    return _ORIGINAL_HANDLE_SECT_SKILL_REQUEST(server, role, values)


def install_pet_support() -> None:
    """Install pet support before the dynamic-map launcher starts."""
    _server.default_role = pet_default_role
    _server.RoleStore.roles_for = pet_roles_for
    _server.RoleStore.create = pet_create_role
    _server.role_entry_frames = pet_role_entry_frames
    _server.decode_payload = pet_decode_payload
    _server.LocalGameServer.handle_sect_skill_request = pet_handle_sect_skill_request


def main() -> None:
    install_pet_support()
    _dynamic.main()


if __name__ == '__main__':
    main()
