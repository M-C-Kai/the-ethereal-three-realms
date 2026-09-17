"""Materialize the bundled seven-sect combat skill catalog to plain JSON files."""
from __future__ import annotations

import argparse
import base64
import gzip
import hashlib
import json
from pathlib import Path


def decode_bundle(path: Path) -> dict:
    wrapper = json.loads(path.read_text(encoding='utf-8'))
    raw_json = gzip.decompress(base64.b64decode(wrapper['payload']))
    expected = wrapper.get('sha256_uncompressed_json', '')
    actual = hashlib.sha256(raw_json).hexdigest()
    if expected and actual != expected:
        raise SystemExit(f'checksum mismatch: expected {expected}, got {actual}')
    return json.loads(raw_json.decode('utf-8'))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--bundle',
        type=Path,
        default=Path(__file__).resolve().parents[1] / 'data' / 'catalog' / 'sect_combat_skill_catalog.bundle.json',
    )
    parser.add_argument(
        '--out-dir',
        type=Path,
        default=Path(__file__).resolve().parents[1] / 'data' / 'catalog',
    )
    args = parser.parse_args()

    data = decode_bundle(args.bundle)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    targets = {
        'sects.json': data['sects'],
        'sect_skills.json': data['sect_skills'],
        'sect_skill_rules.json': data['sect_skill_rules'],
    }
    for filename, payload in targets.items():
        path = args.out_dir / filename
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(path)


if __name__ == '__main__':
    main()
