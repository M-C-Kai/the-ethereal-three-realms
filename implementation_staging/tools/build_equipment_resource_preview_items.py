#!/usr/bin/env python3
"""Generate compatibility-preview equipment catalog from APK icon resources.

Not official equipment templates. Only icon_code / grouping come from the APK.
"""
from __future__ import annotations

import json
from pathlib import Path

from item_registry import SLOT_FAMILY_LABELS, synthetic_preview_template_id

ROOT = Path(__file__).resolve().parents[1]
RESOURCES_FILE = ROOT / 'data' / 'catalog' / 'apk_equipment_resources.json'
ITEMS_FILE = ROOT / 'data' / 'catalog' / 'items.json'
OUTPUT_FILE = ROOT / 'data' / 'catalog' / 'equipment_resource_preview_items.json'

DESCRIPTION = (
    '兼容服 APK 装备图标资源预览项。仅 icon_code/资源分组来自 APK，'
    'template_id、名称、等级、属性均为本地预览构造数据，不代表官方装备。'
)


def main() -> None:
    resources = json.loads(RESOURCES_FILE.read_text(encoding='utf-8'))['resources']
    official_items = json.loads(ITEMS_FILE.read_text(encoding='utf-8'))['items']
    reserved = {int(item['template_id']) for item in official_items}
    preview_items = []
    used = set(reserved)
    for index, resource in enumerate(resources, start=1):
        template_id = synthetic_preview_template_id(
            resource['equipment_slot'],
            resource['resource_group'],
            resource['frame'],
            reserved_ids=reserved,
        )
        if template_id in used:
            raise SystemExit(f'duplicate synthetic template_id {template_id}')
        used.add(template_id)
        family = str(resource['slot_family'])
        label = SLOT_FAMILY_LABELS[family]
        icon_code = int(resource['icon_code'])
        preview_items.append({
            'template_id': template_id,
            'kind': 'equipment',
            'name': f'APK资源预览-{label}-{icon_code:04d}',
            'description': DESCRIPTION,
            'max_quantity': 1,
            'equipment_slot': int(resource['equipment_slot']),
            'price': 0,
            'level_required': 1,
            'icon_code': icon_code,
            'quality': 1,
            'sort_group': 100,
            'sort_order': index,
            'equipment_attributes': [0, 0, 0, 0],
            'appearance_properties': {},
        })
    payload = {
        'version': 1,
        'kind': 'compatibility_preview',
        'status': 'compatibility_preview',
        'metadata': {
            'synthetic_template_id': True,
            'synthetic_name': True,
            'synthetic_required_level': True,
            'only_icon_resource_is_apk_confirmed': True,
            'not_official_equipment_template': True,
            'note': (
                'APK装备资源预览项。仅 icon_code/资源分组来自 APK；'
                'template_id、名称、等级、属性均为本地预览构造，不代表官方装备。'
            ),
        },
        'items': preview_items,
    }
    OUTPUT_FILE.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + '\n',
        encoding='utf-8',
    )
    print(f'wrote {len(preview_items)} preview items to {OUTPUT_FILE}')


if __name__ == '__main__':
    main()
