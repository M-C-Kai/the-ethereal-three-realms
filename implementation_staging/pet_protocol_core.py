from __future__ import annotations

from collections.abc import Sequence

from protocol import (
    Field,
    TYPE_BYTE,
    TYPE_INT,
    TYPE_SHORT,
    TYPE_STRING,
    byte,
    encode_frame,
    integer,
    string,
)

PET_RENAME_ACTION = 15
PET_RELEASE_ACTION = 1
PET_STAT_ACTION = 2
PET_PROPERTY_UPDATE_ACTION = 0


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


def pet_property_update_frame(pet_id: int, updates: Sequence[tuple[int, int]]) -> bytes:
    fields: list[Field] = [byte(PET_PROPERTY_UPDATE_ACTION), integer(pet_id), integer(len(updates))]
    for property_id, value in updates:
        fields.extend((byte(property_id), integer(value)))
    return encode_frame(1134, fields)
