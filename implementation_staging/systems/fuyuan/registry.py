"""福缘系统静态目录：data/fuyuan.json 加载与校验。"""
from __future__ import annotations

import json
from pathlib import Path

MAX_POINTS = 2_000_000_000


def load_catalog(path: Path | None = None) -> dict:
    path = path or Path(__file__).resolve().parents[2] / 'data' / 'fuyuan.json'
    data = json.loads(path.read_text(encoding='utf-8'))
    for key in ('initial_points', 'silver_per_point', 'quote_lifetime_seconds'):
        value = data[key]
        if type(value) is not int or not 0 <= value <= MAX_POINTS:
            raise ValueError(f'invalid fuyuan {key}')
    if not data['silver_per_point'] or not data['quote_lifetime_seconds']:
        raise ValueError('fuyuan price and quote lifetime must be positive')
    packages = data['topup_packages']
    if not isinstance(packages, list) or not 1 <= len(packages) <= 20:
        raise ValueError('invalid fuyuan topup packages')
    if any(type(p) is not int or not 0 < p <= MAX_POINTS for p in packages):
        raise ValueError('invalid fuyuan package points')
    rows = data['benefits']
    if not isinstance(rows, list) or not 1 <= len(rows) <= 100:
        raise ValueError('invalid fuyuan benefits')
    ids = set()
    for row in rows:
        if type(row['id']) is not int or not 0 < row['id'] < 1000 or row['id'] in ids:
            raise ValueError('invalid/duplicate fuyuan benefit id')
        ids.add(row['id'])
        if type(row['tier']) is not int or row['tier'] not in (1, 2, 3):
            raise ValueError('invalid fuyuan benefit tier')
        if type(row['implemented']) is not bool:
            raise ValueError('invalid fuyuan benefit state')
        if any(not isinstance(row[key], str) or not row[key] for key in ('name', 'description')):
            raise ValueError('invalid fuyuan benefit text')
    return data


CATALOG = load_catalog()
