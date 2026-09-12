from __future__ import annotations

import contextvars
import logging
import time

from battle import integration as _battle_integration
from battle import state as _battle_state
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
    pet_skill_list_frame,
    role_pet_frames,
)
from pet_registry import default_pet_registry
from pet_walking_protocol import pet_state_response_frames
from protocol import TYPE_BYTE, TYPE_INT, byte, field_values, integer


LOG = logging.getLogger('piaomiao-local')
PET_REGISTRY = default_pet_registry()
ROAMING_BOSS_CONTACT_RADIUS = _battle_state.CONTACT_RADIUS_TILES

# Internal-only routing actions; these values never go onto the wire.
_INTERNAL_PET_SKILL_ACTION = 248
_INTERNAL_PET_DETAIL_ACTION = 249
_INTERNAL_PET_STATE_ACTION = 250

_ORIGINAL_DEFAULT_ROLE = _server.default_role
_ORIGINAL_ROLE_ENTRY_FRAMES = _server.role_entry_frames
_ORIGINAL_ROLES_FOR = _server.RoleStore.roles_for
_ORIGINAL_ROLE_CREATE = _server.RoleStore.create
_ORIGINAL_DECODE_PAYLOAD = _server.decode_payload
_ORIGINAL_HANDLE_SECT_SKILL_REQUEST = _server.LocalGameServer.handle_sect_skill_request
_ORIGINAL_DYNAMIC_MAP_ENTER_FRAMES = _dynamic.dynamic_map_enter_frames

_ACTIVE_ROLE: contextvars.ContextVar[dict[str, object] | None] = contextvars.ContextVar(
    'piaomiao_active_pet_role', default=None,
)
_ROAMING_BOSS_ENTERED_AT: contextvars.ContextVar[float | None] = contextvars.ContextVar(
    'piaomiao_roaming_boss_entered_at', default=None,
)
_ROAMING_BOSS_SPAWN_TILE: contextvars.ContextVar[tuple[int, int] | None] = contextvars.ContextVar(
    'piaomiao_roaming_boss_spawn_tile', default=None,
)
_ROLE_STORES: dict[int, _server.RoleStore] = {}


def _register_role_store(store: _server.RoleStore, role: dict[str, object]) -> None:
    _ROLE_STORES[id(role)] = store


def pet_default_role(settings):
    role = _ORIGINAL_DEFAULT_ROLE(settings)
    ensure_role_pets(role, PET_REGISTRY)
    return role


def pet_roles_for(store, username: str, *, create_default: bool = True):
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
    role = _ORIGINAL_ROLE_CREATE(store, username, name, model, requested_slot)
    if ensure_role_pets(role, PET_REGISTRY):
        store.save()
    _register_role_store(store, role)
    return role


def pet_role_entry_frames(settings, role: dict[str, object]) -> tuple[bytes, ...]:
    ensure_role_pets(role, PET_REGISTRY)
    _ACTIVE_ROLE.set(role)
    frames = _ORIGINAL_ROLE_ENTRY_FRAMES(settings, role)
    pet_frames = role_pet_frames(role, PET_REGISTRY)
    LOG.info(
        'PET_1127_DOWNLINK role_id=%d pet_count=%d ids=%r',
        int(role.get('id', 0)), len(pet_frames),
        [int(pet.get('id', 0)) for pet in role.get('pets', []) if isinstance(pet, dict)],
    )
    return (*frames, *pet_frames)


def pet_dynamic_map_enter_frames(definition, role_id: int | None = None) -> list[bytes]:
    """Preserve the roaming-Boss position tracker used for contact battles."""
    frames = _ORIGINAL_DYNAMIC_MAP_ENTER_FRAMES(definition, role_id)
    monster = getattr(definition, 'monster', None)
    if (
        int(getattr(definition, 'id', 0)) == _dynamic.ROAMING_BOSS_MAP_ID
        and monster is not None
        and int(getattr(monster, 'id', 0)) == _dynamic.ROAMING_BOSS_ID
    ):
        spawn_tile = (int(monster.x), int(monster.y))
        _ROAMING_BOSS_ENTERED_AT.set(time.monotonic())
        _ROAMING_BOSS_SPAWN_TILE.set(spawn_tile)
        LOG.info(
            'MAP_BOSS_CONTACT_TRACK_START actor=%d spawn=%s target=(%d,%d) delay=%.1f',
            _dynamic.ROAMING_BOSS_ID, spawn_tile,
            _dynamic.ROAMING_BOSS_TARGET_X, _dynamic.ROAMING_BOSS_TARGET_Y,
            _dynamic.ROAMING_BOSS_MOVE_DELAY_SECONDS,
        )
    else:
        _ROAMING_BOSS_ENTERED_AT.set(None)
        _ROAMING_BOSS_SPAWN_TILE.set(None)
    return frames


def _roaming_boss_current_tile(*, now: float | None = None) -> tuple[int, int] | None:
    entered_at = _ROAMING_BOSS_ENTERED_AT.get()
    spawn_tile = _ROAMING_BOSS_SPAWN_TILE.get()
    if entered_at is None or spawn_tile is None:
        return None
    current = time.monotonic() if now is None else float(now)
    if current - entered_at < _dynamic.ROAMING_BOSS_MOVE_DELAY_SECONDS:
        return spawn_tile
    return int(_dynamic.ROAMING_BOSS_TARGET_X), int(_dynamic.ROAMING_BOSS_TARGET_Y)


def _translate_roaming_boss_fight_request(message_id: int, fields):
    if (
        message_id == 2029 and len(fields) >= 2
        and fields[0].type_id == TYPE_BYTE and int(fields[0].value) == 1
        and fields[1].type_id == TYPE_INT
        and int(fields[1].value) == _dynamic.ROAMING_BOSS_ID
    ):
        LOG.info(
            'MAP_BOSS_NATIVE_FIGHT_BRIDGE protocol=2029 action=1 actor=%d -> protocol=2031',
            _dynamic.ROAMING_BOSS_ID,
        )
        return 2031, [integer(_dynamic.ROAMING_BOSS_ID)]
    return message_id, fields


def _translate_roaming_boss_contact_request(message_id: int, fields, *, now: float | None = None):
    """Route every in-range movement attempt through the shared battle entry.

    The synthetic 2031 record carries the Boss tile, not the player's tile, so
    the battle subsystem uses that tile as the contact-radius anchor. The
    player's real position is still persisted from the decoded 1005 path.
    """
    if message_id != 1005:
        return message_id, fields
    role = _ACTIVE_ROLE.get()
    if role is None or int(role.get('map_id', -1)) != _dynamic.ROAMING_BOSS_MAP_ID:
        return message_id, fields
    boss_tile = _roaming_boss_current_tile(now=now)
    if boss_tile is None:
        return message_id, fields
    try:
        player_x, player_y = _server.map_movement_final_tile(field_values(fields))
    except (TypeError, ValueError):
        return message_id, fields
    inside = max(abs(player_x - boss_tile[0]), abs(player_y - boss_tile[1])) <= ROAMING_BOSS_CONTACT_RADIUS
    if not inside:
        return message_id, fields
    if _server.update_role_position(role, player_x, player_y):
        store = _ROLE_STORES.get(id(role))
        if store is not None:
            store.save()
    LOG.info(
        'MAP_BOSS_CONTACT_BATTLE actor=%d player=(%d,%d) boss=(%d,%d) radius=%d protocol=1005->2031',
        _dynamic.ROAMING_BOSS_ID, player_x, player_y, boss_tile[0], boss_tile[1],
        ROAMING_BOSS_CONTACT_RADIUS,
    )
    return 2031, [
        integer(_dynamic.ROAMING_BOSS_ID), integer(0),
        integer(boss_tile[0]), integer(boss_tile[1]), integer(6), integer(0),
    ]


def pet_decode_payload(payload: bytes):
    """Preserve Boss routing and translate only exact pet requests."""
    message_id, fields = _ORIGINAL_DECODE_PAYLOAD(payload)
    message_id, fields = _translate_roaming_boss_fight_request(message_id, fields)
    message_id, fields = _translate_roaming_boss_contact_request(message_id, fields)

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
            return 1103, [
                byte(_INTERNAL_PET_STATE_ACTION), integer(pet_id),
                byte(int(fields[0].value)), byte(int(fields[2].value)),
            ]

    return message_id, fields


def pet_handle_sect_skill_request(
    server,
    role: dict[str, object],
    values: list[object],
) -> tuple[bytes, ...]:
    """Use the existing response-capable 1103 route for pet wire replies."""
    action = int(values[0]) if values else -1

    if action == _INTERNAL_PET_DETAIL_ACTION and len(values) >= 2:
        pet_id = int(values[1])
        pet = find_pet(role, pet_id)
        if pet is None:
            return ()
        LOG.info('PET_1127_DETAIL role_id=%d pet_id=%d properties=30..90', int(role.get('id', 0)), pet_id)
        return (pet_detail_frame(pet, PET_REGISTRY),)

    if action == _INTERNAL_PET_SKILL_ACTION and len(values) >= 2:
        pet_id = int(values[1])
        pet = find_pet(role, pet_id)
        if pet is None:
            return ()
        LOG.info('PET_1103_SKILLS role_id=%d pet_id=%d count=0', int(role.get('id', 0)), pet_id)
        return (pet_skill_list_frame(pet),)

    if action == _INTERNAL_PET_STATE_ACTION and len(values) >= 4:
        pet_id = int(values[1])
        result = apply_pet_state_request(
            role,
            [byte(int(values[2])), integer(pet_id), byte(int(values[3]))],
        )
        if result.changed:
            server.roles.save()
        frames = pet_state_response_frames(int(role.get('id', 0)), result)
        LOG.info(
            'PET_1130_STATE role_id=%d pet_id=%d action=%d enabled=%s changed=%s updates=%r reason=%s',
            int(role.get('id', 0)), result.pet_id, result.action, result.enabled,
            result.changed, result.updates, result.reason,
        )
        return frames

    return _ORIGINAL_HANDLE_SECT_SKILL_REQUEST(server, role, values)


def install_pet_support() -> None:
    # Keep battle compatibility inside the battle subsystem, not the pet layer.
    _battle_integration.install(_server)

    _server.default_role = pet_default_role
    _server.RoleStore.roles_for = pet_roles_for
    _server.RoleStore.create = pet_create_role
    _server.role_entry_frames = pet_role_entry_frames
    _server.decode_payload = pet_decode_payload
    _server.LocalGameServer.handle_sect_skill_request = pet_handle_sect_skill_request
    _dynamic.dynamic_map_enter_frames = pet_dynamic_map_enter_frames


def main() -> None:
    install_pet_support()
    _dynamic.main()


if __name__ == '__main__':
    main()
