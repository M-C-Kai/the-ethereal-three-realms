from __future__ import annotations

import logging
from collections.abc import Callable

import server as _server
from pet_protocol_core import (
    parse_pet_release_request,
    parse_pet_rename_request,
    parse_pet_stat_request,
    pet_property_update_frame,
    pet_release_frame,
    pet_rename_frame,
)
from pet_service import allocate_stats, release_pet, rename_pet
from pet_walking_protocol import pet_map_detach_frame
from protocol import byte, integer, short, string
from pet_registry import default_pet_registry


LOG = logging.getLogger('piaomiao-local')
PET_REGISTRY = default_pet_registry()

_INTERNAL_PET_STAT_ACTION = 245
_INTERNAL_PET_RELEASE_ACTION = 246
_INTERNAL_PET_RENAME_ACTION = 247

_PREVIOUS_DECODE: Callable | None = None
_PREVIOUS_HANDLE: Callable | None = None


def translate_pet_core_request(message_id: int, fields):
    """Translate only exact APK-native pet core requests to internal 1103 actions."""
    if message_id == 1130:
        rename = parse_pet_rename_request(fields)
        if rename is not None:
            pet_id, name = rename
            return 1103, [byte(_INTERNAL_PET_RENAME_ACTION), integer(pet_id), string(name)]

        release = parse_pet_release_request(fields)
        if release is not None:
            return 1103, [byte(_INTERNAL_PET_RELEASE_ACTION), integer(release)]

    if message_id == 1128:
        stat = parse_pet_stat_request(fields)
        if stat is not None:
            pet_id, deltas = stat
            return 1103, [
                byte(_INTERNAL_PET_STAT_ACTION),
                integer(pet_id),
                *(short(value) for value in deltas),
            ]

    return message_id, fields


def handle_pet_core_action(
    server,
    role: dict[str, object],
    values: list[object],
) -> tuple[bytes, ...] | None:
    """Handle one translated core action; return None when the action is not ours."""
    action = int(values[0]) if values else -1
    role_id = int(role.get('id', 0))

    if action == _INTERNAL_PET_RENAME_ACTION and len(values) >= 3:
        pet_id = int(values[1])
        result = rename_pet(role, pet_id, str(values[2]))
        if result.changed:
            server.roles.save()
            LOG.info('PET_RENAME role_id=%d pet_id=%d name=%r', role_id, pet_id, result.name)
            return (pet_rename_frame(pet_id, result.name),)
        LOG.info('PET_RENAME_REJECT role_id=%d pet_id=%d reason=%s', role_id, pet_id, result.reason)
        return ()

    if action == _INTERNAL_PET_RELEASE_ACTION and len(values) >= 2:
        pet_id = int(values[1])
        result = release_pet(role, pet_id)
        if not result.changed:
            LOG.info('PET_RELEASE_REJECT role_id=%d pet_id=%d reason=%s', role_id, pet_id, result.reason)
            return ()
        server.roles.save()
        frames: list[bytes] = []
        if result.was_walking:
            frames.append(pet_map_detach_frame(role_id))
        frames.append(pet_release_frame(pet_id))
        LOG.info(
            'PET_RELEASE role_id=%d pet_id=%d walking=%s deployed=%s',
            role_id, pet_id, result.was_walking, result.was_deployed,
        )
        return tuple(frames)

    if action == _INTERNAL_PET_STAT_ACTION and len(values) >= 7:
        pet_id = int(values[1])
        deltas = tuple(int(value) for value in values[2:7])
        result = allocate_stats(role, pet_id, deltas, PET_REGISTRY)
        if not result.changed:
            LOG.info('PET_STAT_REJECT role_id=%d pet_id=%d reason=%s', role_id, pet_id, result.reason)
            return ()
        server.roles.save()
        LOG.info('PET_STAT_ALLOCATE role_id=%d pet_id=%d deltas=%r', role_id, pet_id, deltas)
        return (pet_property_update_frame(pet_id, result.updates),)

    return None


def pet_core_decode_payload(payload: bytes):
    if _PREVIOUS_DECODE is None:
        raise RuntimeError('pet core bridge is not installed')
    message_id, fields = _PREVIOUS_DECODE(payload)
    return translate_pet_core_request(message_id, fields)


def pet_core_handle_request(server, role: dict[str, object], values: list[object]):
    result = handle_pet_core_action(server, role, values)
    if result is not None:
        return result
    if _PREVIOUS_HANDLE is None:
        raise RuntimeError('pet core bridge is not installed')
    return _PREVIOUS_HANDLE(server, role, values)


def install_pet_core_bridge() -> None:
    global _PREVIOUS_DECODE, _PREVIOUS_HANDLE
    _PREVIOUS_DECODE = _server.decode_payload
    _PREVIOUS_HANDLE = _server.LocalGameServer.handle_sect_skill_request
    _server.decode_payload = pet_core_decode_payload
    _server.LocalGameServer.handle_sect_skill_request = pet_core_handle_request
