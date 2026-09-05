#!/usr/bin/env python3
"""Build a minimal, reviewable weapon-appearance audit from local APK extracts.

Read-only against build/. Does not guess icon_code → property7 mappings.
"""
from __future__ import annotations

import json
import shutil
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AUDIT_DIR = Path(__file__).resolve().parent
ROLE_OUT = AUDIT_DIR / 'role'
SCRIPTS = ROOT / 'references' / 'scripts'
sys.path.insert(0, str(SCRIPTS))
from render_role_resources import parse_role  # noqa: E402

EXTRACTED_ROLE = ROOT / 'build' / 'weapon-apk-extracted' / 'assets' / 'res' / 'role'
EXTRACTED_IMAGES_O = ROOT / 'build' / 'weapon-apk-extracted' / 'assets' / 'res' / 'images' / 'images.o'
WANTED_DATS = [101000, 102000, 103000, 104000, 105000, 106000, 107000, 108000, 109000, 110000]
BASE_DAT = 100000
IMAGE_ID_MIN = 40000
IMAGE_ID_MAX = 49999


def parse_images_o(path: Path) -> list[int]:
    index = path.read_bytes()
    index_len = struct.unpack_from('>H', index, 0)[0]
    records = index[2:2 + index_len]
    ids: list[int] = []
    for offset in range(0, len(records), 7):
        rec = records[offset:offset + 7]
        if len(rec) != 7:
            continue
        ids.append(int(struct.unpack_from('>I', rec, 0)[0]))
    return ids


def role_dat_for_suffix(suffix: int) -> int:
    return 100000 + ((suffix // 1000) + 1) * 1000


def weapon_layer_for_suffix(suffix: int, role_dat: int) -> int:
    layer = ((suffix % 1000) // 100) + 32
    if role_dat >= 102000:
        layer += 1
    return layer


def copy_role_dats() -> list[int]:
    ROLE_OUT.mkdir(parents=True, exist_ok=True)
    copied: list[int] = []
    extra_note = []
    base_src = EXTRACTED_ROLE / f'{BASE_DAT}.dat'
    if base_src.is_file():
        shutil.copy2(base_src, ROLE_OUT / f'{BASE_DAT}.dat')
        extra_note.append(BASE_DAT)
    for role_id in WANTED_DATS:
        src = EXTRACTED_ROLE / f'{role_id}.dat'
        if not src.is_file():
            continue
        shutil.copy2(src, ROLE_OUT / f'{role_id}.dat')
        copied.append(role_id)
    return copied, extra_note


def build_role_manifest(role_ids: list[int]) -> list[dict]:
    entries = []
    for role_id in role_ids:
        path = ROLE_OUT / f'{role_id}.dat'
        resource = parse_role(path)
        used_slots = sorted({rec.image_index for rec in resource.records})
        slots_32plus = [slot for slot in used_slots if slot >= 32]
        seq_uses_32plus = False
        for sequence in resource.sequences:
            for piece in sequence:
                if not 0 <= piece.record_index < len(resource.records):
                    continue
                if resource.records[piece.record_index].image_index >= 32:
                    seq_uses_32plus = True
                    break
            if seq_uses_32plus:
                break
        weapon_image_ids = [
            image_id for image_id in resource.image_ids
            if IMAGE_ID_MIN <= int(image_id) <= IMAGE_ID_MAX
        ]
        observed_weapon_slots = [
            index for index, image_id in enumerate(resource.image_ids)
            if IMAGE_ID_MIN <= int(image_id) <= IMAGE_ID_MAX
        ]
        entries.append({
            'role_id': role_id,
            'file': f'role/{role_id}.dat',
            'image_ids': [int(value) for value in resource.image_ids],
            'image_slot_count': len(resource.image_ids),
            'records': len(resource.records),
            'sequences': len(resource.sequences),
            'animations': len(resource.animations),
            'record_image_slots_used': used_slots,
            'slots_32plus_used_by_records': bool(slots_32plus),
            'slots_32plus_used_by_sequences': seq_uses_32plus,
            'referenced_weapon_image_ids': weapon_image_ids,
            'observed_weapon_slots': observed_weapon_slots,
        })
    return entries


def main() -> None:
    if not EXTRACTED_ROLE.is_dir():
        raise SystemExit(f'missing extracted role dir: {EXTRACTED_ROLE}')
    if not EXTRACTED_IMAGES_O.is_file():
        raise SystemExit(f'missing images.o: {EXTRACTED_IMAGES_O}')

    copied, extra = copy_role_dats()
    archived_ids = sorted(set(copied) | set(extra))
    existing_role_files = {int(path.stem) for path in ROLE_OUT.glob('*.dat')}

    all_image_ids = parse_images_o(EXTRACTED_IMAGES_O)
    weapon_image_ids = sorted({
        image_id for image_id in all_image_ids
        if IMAGE_ID_MIN <= image_id <= IMAGE_ID_MAX
    })
    image_payload = {
        'range': f'{IMAGE_ID_MIN}-{IMAGE_ID_MAX}',
        'source': 'build/weapon-apk-extracted/assets/res/images/images.o',
        'count': len(weapon_image_ids),
        'image_ids': weapon_image_ids,
    }
    (AUDIT_DIR / 'weapon_image_ids.json').write_text(
        json.dumps(image_payload, ensure_ascii=False, indent=2) + '\n',
        encoding='utf-8',
    )

    seen_other = sorted(
        int(path.stem)
        for path in EXTRACTED_ROLE.glob('*.dat')
        if path.stem.isdigit()
        and 100000 <= int(path.stem) <= 199999
        and int(path.stem) not in archived_ids
    )
    manifest = {
        'source_role_dir': 'build/weapon-apk-extracted/assets/res/role',
        'wanted_role_ids': WANTED_DATS,
        'missing_wanted_role_ids': [role_id for role_id in WANTED_DATS if role_id not in copied],
        'additional_character_template_ids': extra,
        'other_100000_199999_seen_not_copied': seen_other,
        'roles': build_role_manifest(archived_ids),
    }
    (AUDIT_DIR / 'role_manifest.json').write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + '\n',
        encoding='utf-8',
    )

    candidates = []
    for image_id in weapon_image_ids:
        suffix = image_id - 40000
        role_dat = role_dat_for_suffix(suffix)
        if role_dat not in existing_role_files:
            continue
        candidates.append({
            'suffix': suffix,
            'role_dat': role_dat,
            'weapon_layer': weapon_layer_for_suffix(suffix, role_dat),
            'weapon_image_id': image_id,
            'role_dat_exists': True,
            'weapon_image_exists': True,
            'property7_low4_candidate': suffix,
        })
    candidate_payload = {
        'note': (
            'Candidates are reverse-supported by extracted images.o IDs and archived role DATs. '
            'Only property7 low-4-digit resource semantics are recorded. '
            'This is not an official icon_code mapping.'
        ),
        'count': len(candidates),
        'candidates': candidates,
    }
    (AUDIT_DIR / 'property7_candidates.json').write_text(
        json.dumps(candidate_payload, ensure_ascii=False, indent=2) + '\n',
        encoding='utf-8',
    )
    print(f'copied role dats: {archived_ids}')
    print(f'missing wanted: {manifest["missing_wanted_role_ids"]}')
    print(f'weapon images: {len(weapon_image_ids)}')
    print(f'property7 candidates: {len(candidates)}')


if __name__ == '__main__':
    main()
