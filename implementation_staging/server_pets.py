from __future__ import annotations

import contextvars
import logging

import server as _server
import server_dynamic_maps as _dynamic
from pet_protocol import apply_pet_state_request, ensure_role_pets, role_pet_frames
from pet_registry import default_pet_registry


LOG = logging.getLogger('piaomiao-local')
PET_REGISTRY = default_pet_registry()

_ORIGINAL_DEFAULT_ROLE = _server.default_role
_ORIGINAL_ROLE_ENTRY_FRAMES = _server.role_entry_frames
_ORIGINAL_ROLES_FOR = _server.RoleStore.roles_for
_ORIGINAL_ROLE_CREATE = _server.RoleStore.create
_ORIGINAL_DECODE_PAYLOAD = _server.decode_payload

_ACTIVE_ROLE: contextvars.ContextVar[dict[str, object] | None] = contextvars.ContextVar(
    'piaomiao_active_pet_role',
    default=None,
)
_ROLE_STORES: dict[int, _server.RoleStore] = {}


def _register_role_store(store: _server.RoleStore, role: dict[str, object]) -> None:
    _ROLE_STORES[id(role)] = store


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
        _register_role_store(store, role)
    if changed:
        store.save()
        LOG.info('PET_MIGRATION user=%r role_count=%d', username, len(roles))
    return roles


def pet_create_role(store, username: str, name: str, model: int, requested_slot: int):
    """Attach the starter pet to newly created characters before returning them."""
    role = _ORIGINAL_ROLE_CREATE(store, username, name, model, requested_slot)
    if ensure_role_pets(role, PET_REGISTRY):
        store.save()
    _register_role_store(store, role)
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


def pet_decode_payload(payload: bytes):
    """Persist confirmed C->S 1130 state toggles while preserving core routing.

    APK ``e/cn`` sends exactly ``[BYTE action, INT petId, BYTE enabled]`` for
    action 10 (出战/待命) and 48 (溜宠/隐藏).  The base server does not yet own a
    1130 branch, so the launcher observes those two verified requests here and
    still returns the untouched decoded message to the normal handler.
    """
    message_id, fields = _ORIGINAL_DECODE_PAYLOAD(payload)
    if message_id != 1130:
        return message_id, fields

    role = _ACTIVE_ROLE.get()
    if role is None:
        LOG.info('PET_1130_IGNORED reason=no_active_role')
        return message_id, fields

    result = apply_pet_state_request(role, fields)
    LOG.info(
        'PET_1130_STATE role_id=%d pet_id=%d action=%d enabled=%s changed=%s reason=%s',
        int(role.get('id', 0)),
        result.pet_id,
        result.action,
        result.enabled,
        result.changed,
        result.reason,
    )
    if result.changed:
        store = _ROLE_STORES.get(id(role))
        if store is not None:
            store.save()
    return message_id, fields


def install_pet_support() -> None:
    """Install the minimal pet overlay before the dynamic-map launcher starts."""
    _server.default_role = pet_default_role
    _server.RoleStore.roles_for = pet_roles_for
    _server.RoleStore.create = pet_create_role
    _server.role_entry_frames = pet_role_entry_frames
    _server.decode_payload = pet_decode_payload


def main() -> None:
    install_pet_support()
    _dynamic.main()


if __name__ == '__main__':
    main()
