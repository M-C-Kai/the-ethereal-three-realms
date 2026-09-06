from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from protocol import Field, TYPE_BYTE, byte, encode_frame, integer, string


MOUNT_MESSAGE_ID = 1024
MOUNT_ATLAS_ACTION = 30
DEFAULT_MOUNT_TYPE = 0


@dataclass(frozen=True)
class MountAtlasEntry:
    catalog_id: int
    name: str
    ride_code: int
    mount_type: int = DEFAULT_MOUNT_TYPE


def default_mount_catalog_path() -> Path:
    return Path(__file__).resolve().parent / 'data' / 'catalog' / 'mount_appearance_mapping.json'


def load_mount_atlas_entries(path: Path | None = None) -> tuple[MountAtlasEntry, ...]:
    """Build the APK riding atlas directly from the resource mapping catalog.

    The catalog remains the single source of truth.  No 54-entry protocol list
    is duplicated in Python.  The APK's property-22 riding code is derived as
    ``image_id - image_base``.
    """
    catalog_path = path or default_mount_catalog_path()
    data = json.loads(catalog_path.read_text(encoding='utf-8'))
    image_base = int(data.get('image_base', 40000))
    named = data.get('named_templates', {})
    unnamed_template = str(
        data.get('item_projection', {}).get('unnamed_name', '骑乘资源 {image_id}')
    )

    entries: list[MountAtlasEntry] = []
    seen: set[int] = set()
    for family in data.get('families', []):
        for raw_image_id in family.get('image_ids', []):
            image_id = int(raw_image_id)
            ride_code = image_id - image_base
            if ride_code <= 0 or ride_code in seen:
                raise ValueError(f'invalid or duplicate ride code: image_id={image_id} ride_code={ride_code}')
            seen.add(ride_code)

            override = named.get(str(image_id), {})
            name = str(override.get('name') or unnamed_template.format(image_id=image_id))
            mount_type = int(override.get('mount_type', DEFAULT_MOUNT_TYPE))
            entries.append(MountAtlasEntry(
                catalog_id=ride_code,
                name=name,
                ride_code=ride_code,
                mount_type=mount_type,
            ))

    expected_count = int(data.get('count', len(entries)))
    if len(entries) != expected_count:
        raise ValueError(f'mount atlas count mismatch: expected={expected_count} actual={len(entries)}')
    return tuple(entries)


def is_mount_atlas_request(fields: list[Field]) -> bool:
    """APK request: C->S 1024 [BYTE 30]."""
    return bool(
        len(fields) >= 1
        and fields[0].type_id == TYPE_BYTE
        and fields[0].value == MOUNT_ATLAS_ACTION
    )


def mount_atlas_frame(entries: tuple[MountAtlasEntry, ...] | None = None) -> bytes:
    """APK response: S->C 1024 action 30 followed by riding atlas records.

    Record layout recovered from the client's riding-atlas screen:
    INT catalog_id, STRING name, INT ride_code, BYTE mount_type.
    """
    if entries is None:
        entries = load_mount_atlas_entries()
    if len(entries) > 255:
        raise ValueError('mount atlas count does not fit BYTE')

    fields = [byte(MOUNT_ATLAS_ACTION), byte(len(entries))]
    for entry in entries:
        fields.extend([
            integer(entry.catalog_id),
            string(entry.name),
            integer(entry.ride_code),
            byte(entry.mount_type),
        ])
    return encode_frame(MOUNT_MESSAGE_ID, fields)
