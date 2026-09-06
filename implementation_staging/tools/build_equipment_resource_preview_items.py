#!/usr/bin/env python3
"""Generate compatibility-preview equipment catalog from APK icon resources.

Not official equipment templates. Only icon_code / grouping come from the APK.
"""
from __future__ import annotations

import json
from pathlib import Path

from item_registry import (
    ARMOR_APPEARANCE_MAPPING_FILE,
    SLOT_FAMILY_LABELS,
    preview_appearance_properties,
    synthetic_preview_template_id,
    unsupported_equipment_slots,
)

ROOT = Path(__file__).resolve().parents[1]
RESOURCES_FILE = ROOT / 'data' / 'catalog' / 'apk_equipment_resources.json'
ITEMS_FILE = ROOT / 'data' / 'catalog' / 'items.json'
MANIFEST_FILE = ROOT / 'materials' / 'appearance-layer-audit' / 'manifest.json'
OUTPUT_FILE = ROOT / 'data' / 'catalog' / 'equipment_resource_preview_items.json'

DESCRIPTION = (
    '兼容服 APK 装备图标资源预览项。仅 icon_code/资源分组来自 APK，'
    'template_id、名称、等级、属性均为本地预览构造数据，不代表官方装备。'
)


def main() -> None:
    resources = json.loads(RESOURCES_FILE.read_text(encoding='utf-8'))['resources']
    disabled_slots = unsupported_equipment_slots()
    armor_catalog = json.loads(ARMOR_APPEARANCE_MAPPING_FILE.read_text(encoding='utf-8'))
    official_items = json.loads(ITEMS_FILE.read_text(encoding='utf-8'))['items']
    manifest = json.loads(MANIFEST_FILE.read_text(encoding='utf-8'))
    reserved = {int(item['template_id']) for item in official_items}
    preview_items = []
    used = set(reserved)
    for index, resource in enumerate(resources, start=1):
        slot = int(resource['equipment_slot'])
        if slot == 3:
            # Old 0300..0309 icon-only armor previews are deprecated.
            continue
        if slot in disabled_slots:
            # 外套/饰品/法宝尚无确认装备关系，暂不进入角色背包。
            continue
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
    armor_preview = armor_catalog['resource_preview']
    property2_to_icon = {
        int(value): int(icon_code)
        for value, icon_code in armor_preview['property2_to_icon_code'].items()
    }
    template_to_property2 = {
        int(template_id): int(value)
        for template_id, value in armor_preview['template_to_property2'].items()
    }
    for template_id, property2 in sorted(template_to_property2.items(), key=lambda row: row[1]):
        image_id = 14000 + property2
        icon_code = property2_to_icon[property2]
        preview_items.append({
            'template_id': template_id,
            'kind': 'equipment',
            'name': f'APK铠甲资源-{image_id}',
            'description': (
                f'APK铠甲主体资源 {image_id} / property2={property2}；'
                f'物品图标 icon_code={icon_code:04d} 已按 APK 铠甲图标组对齐。'
            ),
            'max_quantity': 1,
            'equipment_slot': 3,
            'price': 0,
            'level_required': 1,
            'icon_code': icon_code,
            'quality': 1,
            'sort_group': 100,
            'sort_order': 0,
            'equipment_attributes': [0, 0, 0, 0],
            'appearance_properties': {'2': property2},
        })

    preview_items.sort(key=lambda item: (
        int(item['equipment_slot']),
        int(item['appearance_properties'].get('2', 999)) if int(item['equipment_slot']) == 3 else int(item['sort_order']),
        int(item['template_id']),
    ))
    for sort_order, item in enumerate(preview_items, start=1):
        item['sort_order'] = sort_order

    by_slot: dict[int, list[dict]] = {}
    for item in preview_items:
        by_slot.setdefault(int(item['equipment_slot']), []).append(item)
    for slot, slot_items in by_slot.items():
        slot_items.sort(key=lambda item: int(item['sort_order']))
        for preview_index, item in enumerate(slot_items):
            if slot == 3:
                # Dedicated armor previews already carry the confirmed property2.
                continue
            item['appearance_properties'] = preview_appearance_properties(
                slot,
                preview_index,
                manifest,
                icon_code=int(item['icon_code']),
            )
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
            'appearance_pairing': 'confirmed_visual_weapon_family_mapping',
            'appearance_not_official_icon_mapping': True,
            'note': (
                'APK装备资源预览项。仅 icon_code/资源分组来自 APK；'
                'template_id、名称、等级、属性均为本地预览构造，不代表官方装备。'
                '头盔 property20 只读取 helmet_appearance_mapping.json；未解析图标不猜。'
                '铠甲下发30件：0300..0309→14001..14010、1200..1209→14011..14020、1300..1309→14021..14030；14000是默认身体不作为装备下发。'
                '外套(slot12)、饰品(slot13)、法宝(slot14)因没有明确装备关系暂时不下发。'
                '其他防具 appearance_properties 仍引用 appearance-layer-audit 人物图层候选。'
                '武器 property7 使用 weapon_appearance_mapping.json 的证据映射；'
                '地图 property7 与战斗 1048 field[2] 共用完整编码 image*10+quality。'
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
