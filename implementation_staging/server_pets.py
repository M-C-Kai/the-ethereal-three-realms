from __future__ import annotations

import contextvars
import logging
import time

import server as _server
import server_dynamic_maps as _dynamic
from pet_protocol import apply_pet_state_request, ensure_role_pets, role_pet_frames
from pet_registry import default_pet_registry
from protocol import TYPE_BYTE, TYPE_INT, field_values, integer


LOG = logging.getLogger('piaomiao-local')
PET_REGISTRY = default_pet_registry()
ROAMING_BOSS_CONTACT_RADIUS = 1

_ORIGINAL_DEFAULT_ROLE = _server.default_role
_ORIGINAL_ROLE_ENTRY_FRAMES = _server.role_entry_frames
_ORIGINAL_ROLES_FOR = _server.RoleStore.roles_for
_ORIGINAL_ROLE_CREATE = _server.RoleStore.create
_ORIGINAL_DECODE_PAYLOAD = _server.decode_payload
_ORIGINAL_DYNAMIC_MAP_ENTER_FRAMES = _dynamic.dynamic_map_enter_frames

_ACTIVE_ROLE: contextvars.ContextVar[dict[str, object] | None] = contextvars.ContextVar(
    'piaomiao_active_pet_role',
    default=None,
)
_ROAMING_BOSS_ENTERED_AT: contextvars.ContextVar[float | None] = contextvars.ContextVar(
    'piaomiao_roaming_boss_entered_at',
    default=None,
)
_ROAMING_BOSS_SPAWN_TILE: contextvars.ContextVar[tuple[int, int] | None] = contextvars.ContextVar(
    'piaomiao_roaming_boss_spawn_tile',
    default=None,
)
_ROAMING_BOSS_CONTACT_INSIDE: contextvars.ContextVar[bool] = contextvars.ContextVar(
    'piaomiao_roaming_boss_contact_inside',
    default=False,
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


def pet_dynamic_map_enter_frames(definition, role_id: int | None = None) -> list[bytes]:
    """Track the connection-local roaming Boss position epoch for contact battles."""
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
        _ROAMING_BOSS_CONTACT_INSIDE.set(False)
        LOG.info(
            'MAP_BOSS_CONTACT_TRACK_START actor=%d spawn=%s target=(%d,%d) delay=%.1f',
            _dynamic.ROAMING_BOSS_ID,
            spawn_tile,
            _dynamic.ROAMING_BOSS_TARGET_X,
            _dynamic.ROAMING_BOSS_TARGET_Y,
            _dynamic.ROAMING_BOSS_MOVE_DELAY_SECONDS,
        )
    else:
        _ROAMING_BOSS_ENTERED_AT.set(None)
        _ROAMING_BOSS_SPAWN_TILE.set(None)
        _ROAMING_BOSS_CONTACT_INSIDE.set(False)
    return frames


def _roaming_boss_current_tile(*, now: float | None = None) -> tuple[int, int] | None:
    """Return the current server-authoritative tile for the one-shot roaming probe."""
    entered_at = _ROAMING_BOSS_ENTERED_AT.get()
    spawn_tile = _ROAMING_BOSS_SPAWN_TILE.get()
    if entered_at is None or spawn_tile is None:
        return None
    current = time.monotonic() if now is None else float(now)
    if current - entered_at < _dynamic.ROAMING_BOSS_MOVE_DELAY_SECONDS:
        return spawn_tile
    return int(_dynamic.ROAMING_BOSS_TARGET_X), int(_dynamic.ROAMING_BOSS_TARGET_Y)


def _translate_roaming_boss_fight_request(message_id: int, fields):
    """Bridge the APK-native q-monster fight request into the server's battle route.

    Reverse-engineered client path:
      map q actor -> action menu "战斗" -> main/w.a(2029, 1, selectedActorId)
      -> wire fields [BYTE 1, INT actorId].

    The existing local battle implementation is intentionally centralized in
    the 2031 map-object interaction branch. Rewrite only the dedicated map-58
    roaming Boss request into the minimal 2031 shape [INT objectId], which the
    existing tolerant decoder accepts with x/y/action omitted. Other 2029
    actions and actor ids remain untouched.
    """
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


def _translate_roaming_boss_contact_request(message_id: int, fields, *, now: float | None = None):
    """Turn the first player movement into Boss contact into the existing battle path.

    Native q actors intentionally show a "战斗" menu instead of auto-sending a
    fight request when approached.  Preserve normal 1005 movement outside the
    one-tile contact radius, but when the player first enters that radius,
    rewrite the movement as the same 2031 map-object interaction already used
    by the local battle implementation.  The latch resets after the player
    moves away, matching the existing post-escape leave-and-return behavior.
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
    was_inside = _ROAMING_BOSS_CONTACT_INSIDE.get()
    _ROAMING_BOSS_CONTACT_INSIDE.set(inside)
    if not inside or was_inside:
        return message_id, fields

    if _server.update_role_position(role, player_x, player_y):
        store = _ROLE_STORES.get(id(role))
        if store is not None:
            store.save()

    LOG.info(
        'MAP_BOSS_CONTACT_BATTLE actor=%d player=(%d,%d) boss=(%d,%d) radius=%d protocol=1005->2031',
        _dynamic.ROAMING_BOSS_ID,
        player_x,
        player_y,
        boss_tile[0],
        boss_tile[1],
        ROAMING_BOSS_CONTACT_RADIUS,
    )
    return 2031, [
        integer(_dynamic.ROAMING_BOSS_ID),
        integer(0),
        integer(player_x),
        integer(player_y),
        integer(6),
        integer(0),
    ]


def pet_decode_payload(payload: bytes):
    """Observe launcher-specific client requests while preserving core routing.

    APK ``e/cn`` sends exactly ``[BYTE action, INT petId, BYTE enabled]`` for
    1130 action 10 (出战/待命) and 48 (溜宠/隐藏). The native roaming q monster
    uses 2029 ``[BYTE 1, INT actorId]`` when the player chooses "战斗"; bridge
    that request and first-entry proximity contact into the server's existing
    2031 battle path.
    """
    message_id, fields = _ORIGINAL_DECODE_PAYLOAD(payload)
    message_id, fields = _translate_roaming_boss_fight_request(message_id, fields)
    message_id, fields = _translate_roaming_boss_contact_request(message_id, fields)
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
    """Install the pet overlay plus roaming-Boss interaction compatibility."""
    _server.default_role = pet_default_role
    _server.RoleStore.roles_for = pet_roles_for
    _server.RoleStore.create = pet_create_role
    _server.role_entry_frames = pet_role_entry_frames
    _server.decode_payload = pet_decode_payload
    _dynamic.dynamic_map_enter_frames = pet_dynamic_map_enter_frames


def main() -> None:
    install_pet_support()
    _dynamic.main()


if __name__ == '__main__':
    main()
