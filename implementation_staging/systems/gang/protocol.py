"""Gang protocol field layouts and response frames.

Incoming layouts were verified against the decoded APK smali:

- ``main/w.a(ISI)`` sends 1107 as ``[short sub, int param]``; sub 3 has no
  param, sub 4 (kick) carries ``[short, byte page_x, byte page_y, int id]``
  and sub 0x1f (motto) carries ``[short, string]``.
- ``e/cx.i``, ``e/ef.j`` and ``e/ec.k`` send the list requests as
  ``[byte 1, byte page_x, byte page_y]``; ``e/ef.b`` requests a member
  detail as ``[byte 2, int role_id]``.

Response layouts follow the client parsers: ``main/e`` reads the 1107
sub-command as field 0 short; ``e/ed`` and ``e/cx`` read the info fields by
fixed vector index (2 name, 4 leader, 5 members, 6 funds, 7 activity,
8 motto, 9 strength); list frames use ``[byte type, short page, byte count]``
headers with fixed-stride records starting at field 3.
"""

from __future__ import annotations

from dataclasses import dataclass

from protocol import TYPE_BYTE, TYPE_INT, TYPE_SHORT, TYPE_STRING, byte, encode_frame, integer, short, string
from systems.gang.registry import (
    APPLICATION_LIST_COMMAND,
    GANG_COMMAND,
    GANG_LIST_COMMAND,
    GANG_POSITION_LEADER,
    GANG_POSITION_MEMBER,
    GANG_POSITION_PROPERTY,
    MEMBER_LIST_COMMAND,
    SUB_ACCEPT_INVITE,
    SUB_GANG_INFO,
    SUB_INVITE,
    SUB_REJECT_INVITE,
)

GANG_INFO_FIELD_NAME = 2
GANG_INFO_FIELD_LEADER_NAME = 4
GANG_INFO_FIELD_MEMBER_COUNT = 5
GANG_INFO_FIELD_FUNDS = 6
GANG_INFO_FIELD_ACTIVITY = 7
GANG_INFO_FIELD_MOTTO = 8
GANG_INFO_FIELD_STRENGTH = 9


@dataclass(frozen=True)
class GangListEntry:
    gang_id: int
    name: str
    leader_name: str
    member_count: int


@dataclass(frozen=True)
class GangMemberEntry:
    role_id: int
    name: str
    position: int
    level: int
    online: bool


@dataclass(frozen=True)
class GangApplicationEntry:
    role_id: int
    name: str
    race: int
    level: int
    online: bool


@dataclass(frozen=True)
class GangMemberDetail:
    name: str
    sex: int
    level: int
    race: int
    sect_id: int
    joined_at: int
    position: int
    contribution: int
    online: bool


def _field_int(fields: list[object], index: int) -> int | None:
    if len(fields) <= index:
        return None
    value = fields[index].value
    if isinstance(value, bool) or not isinstance(value, int):
        return None
    return value


def _field_str(fields: list[object], index: int) -> str | None:
    if len(fields) <= index:
        return None
    value = fields[index].value
    if not isinstance(value, str):
        return None
    return value


class GangProtocol:
    """Recognize and decode the gang requests emitted by the APK."""

    @staticmethod
    def is_gang_message(message_id: int) -> bool:
        return message_id in (GANG_COMMAND, GANG_LIST_COMMAND, MEMBER_LIST_COMMAND, APPLICATION_LIST_COMMAND)

    @staticmethod
    def gang_subcommand(fields: list[object]) -> int | None:
        if not fields or fields[0].type_id != TYPE_SHORT:
            return None
        value = fields[0].value
        if isinstance(value, bool) or not isinstance(value, int):
            return None
        return value

    @staticmethod
    def gang_int_param(fields: list[object]) -> int | None:
        return _field_int(fields, 1)

    @staticmethod
    def gang_motto_param(fields: list[object]) -> str | None:
        return _field_str(fields, 1)

    @staticmethod
    def gang_kick_member_id(fields: list[object]) -> int | None:
        return _field_int(fields, 3)

    @staticmethod
    def is_list_request(fields: list[object]) -> bool:
        return bool(fields and fields[0].type_id == TYPE_BYTE and fields[0].value == 1)

    @staticmethod
    def is_detail_request(fields: list[object]) -> bool:
        return bool(fields and fields[0].type_id == TYPE_BYTE and fields[0].value == 2)

    @staticmethod
    def detail_role_id(fields: list[object]) -> int | None:
        return _field_int(fields, 1)


def gang_info_frame(gang_id: int, name: str, leader_id: int, leader_name: str, member_count: int, funds: int, activity: int, motto: str, strength: int) -> bytes:
    return encode_frame(GANG_COMMAND, [
        short(SUB_GANG_INFO),
        integer(gang_id),
        string(name),
        integer(leader_id),
        string(leader_name),
        integer(member_count),
        integer(funds),
        integer(activity),
        string(motto),
        integer(strength),
    ])


def gang_close_frame(subcommand: int) -> bytes:
    """1107 sub 3/4 tells the client to close the gang screens 0x13b/0x13d/0x13e."""
    return encode_frame(GANG_COMMAND, [short(subcommand)])


def gang_invite_frame(inviter_id: int, inviter_name: str, gang_name: str) -> bytes:
    return encode_frame(GANG_COMMAND, [
        short(SUB_INVITE),
        integer(inviter_id),
        string(inviter_name),
        string(gang_name),
    ])


def gang_list_frame(entries: list[GangListEntry]) -> bytes:
    fields: list[object] = [byte(1), integer(len(entries)), integer(len(entries))]
    for entry in entries:
        fields.extend((
            integer(entry.gang_id),
            string(entry.name),
            string(entry.leader_name),
            string(str(entry.member_count)),
        ))
    return encode_frame(GANG_LIST_COMMAND, fields)


def member_list_frame(members: list[GangMemberEntry]) -> bytes:
    fields: list[object] = [byte(1), short(0), byte(len(members))]
    for member in members:
        fields.extend((
            integer(member.role_id),
            string(member.name),
            integer(member.position),
            string(str(member.level)),
            integer(1 if member.online else 0),
        ))
    return encode_frame(MEMBER_LIST_COMMAND, fields)


def member_detail_frame(detail: GangMemberDetail) -> bytes:
    return encode_frame(MEMBER_LIST_COMMAND, [
        byte(2),
        string(detail.name),
        integer(detail.sex),
        integer(detail.level),
        integer(detail.race),
        integer(detail.sect_id),
        integer(detail.joined_at),
        integer(detail.position),
        string(str(detail.contribution)),
        integer(1 if detail.online else 0),
    ])


def application_list_frame(applications: list[GangApplicationEntry]) -> bytes:
    fields: list[object] = [byte(1), short(0), byte(len(applications))]
    for application in applications:
        fields.extend((
            integer(application.role_id),
            string(application.name),
            integer(application.race),
            string(str(application.level)),
            integer(1 if application.online else 0),
        ))
    return encode_frame(APPLICATION_LIST_COMMAND, fields)


def gang_properties_update_frame(role_id: int, properties: dict[int, int]) -> bytes:
    """1017 incremental property update for gang-related slots (21 position, 50 silver)."""
    return encode_frame(1017, [
        byte(0),
        integer(role_id),
        integer(len(properties)),
        *(
            field
            for property_index, value in sorted(properties.items())
            for field in (byte(property_index), integer(value))
        ),
    ])


def gang_position_update_frame(role_id: int, position: int) -> bytes:
    """1017 incremental property update for the gang-position slot 21."""
    return gang_properties_update_frame(role_id, {GANG_POSITION_PROPERTY: position})


def position_name(position: int) -> str:
    if position == GANG_POSITION_LEADER:
        return '帮主'
    if position == GANG_POSITION_MEMBER:
        return '帮众'
    return ''
