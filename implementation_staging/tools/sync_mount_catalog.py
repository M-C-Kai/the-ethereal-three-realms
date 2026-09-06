from __future__ import annotations

import argparse
import json
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / 'data' / 'catalog' / 'mount_appearance_mapping.json'
ITEMS = ROOT / 'data' / 'catalog' / 'items.json'
STARTER = ROOT / 'data' / 'catalog' / 'starter_inventory.json'


def load_json(path: Path) -> dict:
    data = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(data, dict):
        raise ValueError(f'expected JSON object: {path}')
    return data


def catalog_mount_rows(catalog: dict) -> list[dict]:
    projection = catalog['item_projection']
    image_base = int(catalog['image_base'])
    named = catalog.get('named_templates', {})
    rows: list[dict] = []
    sort_order = 0
    for family in catalog['families']:
        role_model = int(family['role_model'])
        for raw_image_id in family['image_ids']:
            sort_order += 1
            image_id = int(raw_image_id)
            ride_code = image_id - image_base
            known = named.get(str(image_id), {})
            template_id = int(
                known.get('template_id', int(projection['template_base']) + ride_code)
            )
            name = str(
                known.get(
                    'name',
                    str(projection['unnamed_name']).format(image_id=image_id),
                )
            )
            description = str(projection['description']).format(
                image_id=image_id,
                ride_code=ride_code,
                role_model=role_model,
            )
            rows.append({
                'template_id': template_id,
                'kind': 'mount',
                'name': name,
                'description': description,
                'max_quantity': int(projection['max_quantity']),
                'equipment_slot': int(projection['equipment_slot']),
                'price': int(projection['price']),
                'level_required': int(projection['level_required']),
                'icon_code': int(projection['icon_code']),
                'quality': int(projection['quality']),
                'sort_group': int(projection['sort_group']),
                'sort_order': sort_order,
                'equipment_attributes': [int(value) for value in projection['equipment_attributes']],
                'mount_model': ride_code,
            })
    if len(rows) != int(catalog['count']):
        raise ValueError('catalog mount count mismatch')
    if len({row['template_id'] for row in rows}) != len(rows):
        raise ValueError('duplicate projected mount template id')
    return rows


def projected_documents(catalog: dict, items_doc: dict, starter_doc: dict) -> tuple[dict, dict]:
    mount_rows = catalog_mount_rows(catalog)
    old_mount_ids = {
        int(row['template_id'])
        for row in items_doc.get('items', [])
        if isinstance(row, dict) and row.get('kind') == 'mount'
    }

    projected_items = deepcopy(items_doc)
    base_items = [
        row for row in projected_items.get('items', [])
        if not (isinstance(row, dict) and row.get('kind') == 'mount')
    ]
    projected_items['items'] = base_items + mount_rows

    projected_starter = deepcopy(starter_doc)
    base_starter = [
        row for row in projected_starter.get('items', [])
        if not (
            isinstance(row, dict)
            and int(row.get('template_id', 0)) in old_mount_ids
        )
    ]
    # Riding appearances are atlas/catalog resources, not default ownership.
    projected_starter['items'] = base_starter
    return projected_items, projected_starter


def canonical(data: dict) -> str:
    return json.dumps(data, ensure_ascii=False, separators=(',', ':')) + '\n'


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()

    catalog = load_json(CATALOG)
    items_doc = load_json(ITEMS)
    starter_doc = load_json(STARTER)
    projected_items, projected_starter = projected_documents(catalog, items_doc, starter_doc)

    expected_items = canonical(projected_items)
    expected_starter = canonical(projected_starter)
    if args.check:
        current_items = canonical(items_doc)
        current_starter = canonical(starter_doc)
        if current_items != expected_items or current_starter != expected_starter:
            raise SystemExit('mount catalog projections are stale; run tools/sync_mount_catalog.py')
        print(f'mount catalog projections OK: {catalog["count"]} mounts')
        return

    ITEMS.write_text(expected_items, encoding='utf-8')
    STARTER.write_text(expected_starter, encoding='utf-8')
    print(f'synced {catalog["count"]} mount item definitions; starter grants=0')


if __name__ == '__main__':
    main()
