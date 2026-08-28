"""Binary protocol helpers for the Piao Miao San Jie 2 client."""

from __future__ import annotations

import dataclasses
import struct
from typing import Iterable, Sequence


TYPE_SHORT_ALT = 1
TYPE_BYTE = 2
TYPE_SHORT = 3
TYPE_INT = 4
TYPE_STRING = 6
TYPE_BYTES = 7
TYPE_BYTE_ALT = 8
TYPE_LONG = 9


class ProtocolError(ValueError):
    pass


def _signed_byte(value: int) -> int:
    value &= 0xFF
    return value - 256 if value >= 128 else value


def _java_remainder(value: int, divisor: int) -> int:
    # Java integer division truncates toward zero; Python's // floors.
    return value - int(value / divisor) * divisor


class GameCipher:
    """Stateful field-stream cipher enabled after the client receives 1052.

    Client-to-server frames keep the outer length and message id plain and
    encrypt only typed fields (frame offset 4 onward). Server-to-client frames
    encrypt the complete frame; the client decrypts the two-byte length first,
    then decrypts the remaining bytes with the same stream position. Send and
    receive directions have independent counters, as in the APK's a.c.b class.
    """

    def __init__(self) -> None:
        table_a: list[int] = []
        table_b: list[int] = []

        value = _signed_byte(111)
        for _ in range(256):
            table_a.append(value & 0xFF)
            value = _signed_byte(_java_remainder(
                (value * 54) + ((34 * value) * value) + 123,
                256,
            ))

        value = _signed_byte(123)
        for _ in range(256):
            table_b.append(value & 0xFF)
            value = _signed_byte(_java_remainder(
                (value * 44) + ((65 * value) * value) + 78,
                256,
            ))

        self._a = table_a
        self._b = table_b
        self._c = [(left ^ right) & 0xFF for left, right in zip(table_a, table_b)]
        self._d = [(left & right) & 0xFF for left, right in zip(table_a, table_b)]
        self._decrypt_position = 0
        self._encrypt_position = 0

    @staticmethod
    def _swap_nibbles(value: int) -> int:
        return (((value & 0x0F) << 4) | ((value & 0xF0) >> 4)) & 0xFF

    def encrypt(self, data: bytes) -> bytes:
        result = bytearray(data)
        for index, original in enumerate(result):
            position = self._encrypt_position
            value = original ^ self._a[position & 0xFF]
            value = (value + self._c[position & 0xFF]) & 0xFF
            value ^= self._b[(position & 0xFF00) >> 8]
            value = (value + self._d[(position & 0xFF00) >> 8]) & 0xFF
            result[index] = self._swap_nibbles(value)
            self._encrypt_position = (position + 1) & 0xFFFF
        return bytes(result)

    def decrypt(self, data: bytes) -> bytes:
        result = bytearray(data)
        for index, original in enumerate(result):
            position = self._decrypt_position
            value = self._swap_nibbles(original)
            value = (value - self._d[(position & 0xFF00) >> 8]) & 0xFF
            value ^= self._b[(position & 0xFF00) >> 8]
            value = (value - self._c[position & 0xFF]) & 0xFF
            value ^= self._a[position & 0xFF]
            result[index] = value
            self._decrypt_position = (position + 1) & 0xFFFF
        return bytes(result)

    def encrypt_frame(self, frame: bytes) -> bytes:
        if len(frame) < 4:
            raise ProtocolError('frame is too short for game encryption')
        return frame[:4] + self.encrypt(frame[4:])

    def decrypt_frame(self, frame: bytes) -> bytes:
        if len(frame) < 4:
            raise ProtocolError('frame is too short for game decryption')
        return frame[:4] + self.decrypt(frame[4:])

    def encrypt_server_frame(self, frame: bytes) -> bytes:
        """Encrypt a complete server-to-client frame."""
        if len(frame) < 4:
            raise ProtocolError('frame is too short for game encryption')
        return self.encrypt(frame)


@dataclasses.dataclass(frozen=True)
class Field:
    type_id: int
    value: object


def byte(value: int) -> Field:
    return Field(TYPE_BYTE, value)


def short(value: int) -> Field:
    return Field(TYPE_SHORT, value)


def integer(value: int) -> Field:
    return Field(TYPE_INT, value)


def long_integer(value: int) -> Field:
    return Field(TYPE_LONG, value)


def string(value: str) -> Field:
    return Field(TYPE_STRING, value)


def binary(value: bytes) -> Field:
    return Field(TYPE_BYTES, value)


def encode_field(field: Field) -> bytes:
    type_id = field.type_id
    value = field.value
    if type_id in (TYPE_BYTE, TYPE_BYTE_ALT):
        return struct.pack('>BB', type_id, int(value) & 0xFF)
    if type_id in (TYPE_SHORT, TYPE_SHORT_ALT):
        return struct.pack('>BH', type_id, int(value) & 0xFFFF)
    if type_id == TYPE_INT:
        return struct.pack('>Bi', type_id, int(value))
    if type_id == TYPE_LONG:
        return struct.pack('>Bq', type_id, int(value))
    if type_id == TYPE_STRING:
        raw = str(value).encode('utf-8')
        if len(raw) > 0xFFFF:
            raise ProtocolError('string field is too large')
        return struct.pack('>BH', type_id, len(raw)) + raw
    if type_id == TYPE_BYTES:
        raw = bytes(value)
        if len(raw) > 0xFFFF:
            raise ProtocolError('binary field is too large')
        return struct.pack('>BH', type_id, len(raw)) + raw
    raise ProtocolError(f'unsupported field type {type_id}')


def encode_payload(message_id: int, fields: Iterable[Field] = ()) -> bytes:
    return struct.pack('>H', message_id & 0xFFFF) + b''.join(encode_field(x) for x in fields)


def encode_frame(message_id: int, fields: Iterable[Field] = ()) -> bytes:
    payload = encode_payload(message_id, fields)
    frame_length = len(payload) + 2
    if frame_length > 0xFFFF:
        raise ProtocolError('frame is too large')
    return struct.pack('>H', frame_length) + payload


def decode_payload(payload: bytes) -> tuple[int, list[Field]]:
    if len(payload) < 2:
        raise ProtocolError('payload is missing the message id')
    message_id = struct.unpack_from('>H', payload, 0)[0]
    offset = 2
    fields: list[Field] = []
    while offset < len(payload):
        type_id = payload[offset]
        offset += 1
        if type_id in (TYPE_BYTE, TYPE_BYTE_ALT):
            if offset + 1 > len(payload):
                raise ProtocolError('truncated byte field')
            value = payload[offset]
            offset += 1
        elif type_id in (TYPE_SHORT, TYPE_SHORT_ALT):
            if offset + 2 > len(payload):
                raise ProtocolError('truncated short field')
            value = struct.unpack_from('>H', payload, offset)[0]
            offset += 2
        elif type_id == TYPE_INT:
            if offset + 4 > len(payload):
                raise ProtocolError('truncated int field')
            value = struct.unpack_from('>i', payload, offset)[0]
            offset += 4
        elif type_id == TYPE_LONG:
            if offset + 8 > len(payload):
                raise ProtocolError('truncated long field')
            value = struct.unpack_from('>q', payload, offset)[0]
            offset += 8
        elif type_id in (TYPE_STRING, TYPE_BYTES):
            if offset + 2 > len(payload):
                raise ProtocolError('truncated variable-length field')
            size = struct.unpack_from('>H', payload, offset)[0]
            offset += 2
            if offset + size > len(payload):
                raise ProtocolError('truncated variable-length data')
            raw = payload[offset:offset + size]
            offset += size
            value = raw.decode('utf-8') if type_id == TYPE_STRING else raw
        else:
            raise ProtocolError(f'unknown field type {type_id} at offset {offset - 1}')
        fields.append(Field(type_id, value))
    return message_id, fields


def decode_frame(frame: bytes) -> tuple[int, list[Field]]:
    if len(frame) < 4:
        raise ProtocolError('frame is too short')
    declared = struct.unpack_from('>H', frame, 0)[0]
    if declared != len(frame):
        raise ProtocolError(f'frame length mismatch: declared={declared}, actual={len(frame)}')
    return decode_payload(frame[2:])


def field_values(fields: Sequence[Field]) -> list[object]:
    return [x.value for x in fields]
