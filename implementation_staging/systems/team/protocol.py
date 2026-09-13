"""APK-confirmed team frames. Data changes never use map movement messages."""
from __future__ import annotations

from protocol import byte, encode_frame, integer, short, string
from systems.role.protocol import character_appearance_frame
from systems.map.protocol import player_actor_object_id

TEAM_LEADER_FLAG = 0x40


def invite_frame(role_id: int, name: str, level: int, sect_id: int) -> bytes:
    return encode_frame(1023, [
        short(2), integer(int(role_id)), string(str(name)),
        short(max(1, int(level))), byte(int(sect_id)),
    ])


def member_frame(name: str, role_id: int, max_hp: int, level: int,
                 max_mp: int, sect_id: int) -> bytes:
    """1026/0 appends one roster row to APK aa.a (role IDs, not map actors)."""
    return encode_frame(1026, [
        byte(0), byte(1), string(str(name)), integer(int(role_id)),
        integer(max(0, int(max_hp))), integer(max(0, int(max_hp))),
        byte(int(sect_id)), integer(max(1, int(level))),
        integer(max(0, int(max_mp))), integer(max(0, int(max_mp))), integer(0),
    ])


def leader_flag_frame(role_id: int, enabled: bool) -> bytes:
    return character_appearance_frame(int(role_id), {0: TEAM_LEADER_FLAG if enabled else 0})


def member_state_frame(action: int, role_id: int) -> bytes:
    return encode_frame(1023, [short(int(action)), integer(int(role_id))])


def member_removed_frame(role_id: int) -> bytes:
    return encode_frame(1023, [short(1), integer(int(role_id))])


def disband_frame() -> bytes:
    return encode_frame(1023, [short(11)])


def follow_chain_frame(leader_id: int, member_id: int, x: int, y: int) -> bytes:
    """1028/e.ai links a visible leader actor to the local member actor."""
    return encode_frame(1028, [
        integer(player_actor_object_id(leader_id)), integer(0), integer(0),
        integer(int(x)), integer(int(y)), byte(1), integer(int(member_id)),
    ])
