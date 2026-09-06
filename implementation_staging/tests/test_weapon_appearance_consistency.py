import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from item_registry import (
    WEAPON_ICON_GROUP_TO_BATTLE_FAMILY,
    battle_weapon_field2_from_icon,
    battle_weapon_image_from_icon,
    default_item_registry,
)
from protocol import decode_frame, field_values
from server import Settings, battle_actor_frames, character_appearance, equipped_weapon_battle_field2

EXPECTED = {
    21: 220, 22: 260, 23: 271, 24: 250, 25: 231, 26: 280,
    27: 242, 28: 240, 29: 241, 30: 221, 31: 290, 32: 270, 33: 230,
}

class WeaponAppearanceConsistencyTests(unittest.TestCase):
    def test_confirmed_family_mapping(self):
        self.assertEqual(WEAPON_ICON_GROUP_TO_BATTLE_FAMILY, EXPECTED)

    def test_all_130_preview_weapons_use_unified_code(self):
        root = Path(__file__).resolve().parents[1]
        preview = json.loads((root / 'data/catalog/equipment_resource_preview_items.json').read_text(encoding='utf-8'))
        manifest = json.loads((root / 'references/battle-weapon-appearance-audit/manifest.json').read_text(encoding='utf-8'))
        weapons = [x for x in preview['items'] if int(x.get('equipment_slot', 0)) == 10]
        self.assertEqual(len(weapons), 130)
        for item in weapons:
            icon = int(item['icon_code'])
            quality = int(item['quality'])
            code = int(item['appearance_properties']['7'])
            self.assertEqual(code, battle_weapon_field2_from_icon(icon, quality), icon)
            family = EXPECTED[icon // 100]
            images = [int(v) for v in manifest['battle_weapon_families'][str(family)]]
            if family == 231:
                images = images[:10]
            self.assertIn(code // 10, images, icon)

    def test_special_rows(self):
        self.assertEqual(battle_weapon_image_from_icon(2300), 27101)
        self.assertEqual(battle_weapon_image_from_icon(2309), 27110)
        self.assertEqual(battle_weapon_field2_from_icon(2509, 1), 231091)
        self.assertEqual(battle_weapon_field2_from_icon(2701, 1), 242011)

    def test_starter_map_and_battle_match(self):
        settings = Settings()
        role = {'id': 10001, 'name': '测试角色', 'model': 19, 'items': [
            {'id': 1, 'template_id': 100001001, 'quantity': 1, 'location': 'equipped'}
        ]}
        map_code = character_appearance(role, settings.item_registry)[7]
        self.assertEqual(map_code, 242011)
        self.assertEqual(equipped_weapon_battle_field2(role, settings.item_registry), map_code)
        _, fields = decode_frame(battle_actor_frames(role, settings)[0])
        self.assertEqual(field_values(fields)[2], map_code)

    def test_preview_map_and_battle_match(self):
        root = Path(__file__).resolve().parents[1]
        preview = json.loads((root / 'data/catalog/equipment_resource_preview_items.json').read_text(encoding='utf-8'))
        item = next(x for x in preview['items'] if int(x.get('equipment_slot', 0)) == 10 and int(x['icon_code']) == 3200)
        registry = default_item_registry()
        role = {'id': 10001, 'name': '测试角色', 'model': 19, 'items': [
            {'id': 1, 'template_id': int(item['template_id']), 'quantity': 1, 'location': 'equipped'}
        ]}
        map_code = character_appearance(role, registry)[7]
        self.assertEqual(map_code, 270001)
        self.assertEqual(equipped_weapon_battle_field2(role, registry), map_code)
        _, fields = decode_frame(battle_actor_frames(role, Settings(item_registry=registry))[0])
        self.assertEqual(field_values(fields)[2], map_code)

    def test_unequipped_is_zero(self):
        registry = default_item_registry()
        role = {'id': 10001, 'name': '测试角色', 'model': 19, 'items': []}
        self.assertEqual(character_appearance(role, registry)[7], 0)
        self.assertEqual(equipped_weapon_battle_field2(role, registry), 0)

if __name__ == '__main__':
    unittest.main()
