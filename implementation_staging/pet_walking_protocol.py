from __future__ import annotations

from pet_protocol import PET_STATE_WALKING, PetStateResult, pet_property_update_frame
from protocol import byte, encode_frame, integer, short


PET_MAP_ATTACH_ACTION = 13
PET_MAP_DETACH_ACTION = 102


def pet_map_attach_frame(pet_id: int, role_id: int) -> bytes:
    """Attach an already-known pet instance to the local map player.

    APK ``main/e.aa`` 1127/action=13 reads field 1 as the pet id and the final
    field as the owner/player id.  For the local player it resolves the pet
    from ``b/f.k``, assigns ``b/v.E``, calls ``pet.b()`` and refreshes the
    follower position with ``player.ae()``.
    """
    return encode_frame(1127, [
        byte(PET_MAP_ATTACH_ACTION),
        integer(int(pet_id)),
        integer(int(role_id)),
    ])


def pet_map_detach_frame(role_id: int) -> bytes:
    """Remove the walking pet from one map player.

    APK 1010/action=102 passes field 0 to ``b/m.q(playerId)``.  For the local
    player that calls ``b/v.X()``, which disposes ``b/v.E`` and refreshes the
    map render list.
    """
    return encode_frame(1010, [
        integer(int(role_id)),
        short(0),
        short(0),
        integer(0),
        integer(0),
        short(PET_MAP_DETACH_ACTION),
    ])


def pet_state_response_frames(role_id: int, result: PetStateResult) -> tuple[bytes, ...]:
    """Return property-state acks plus the map-side walking-pet operation."""
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
