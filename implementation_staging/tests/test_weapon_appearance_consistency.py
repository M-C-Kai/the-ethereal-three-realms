import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import item_registry
from item_registry import (
    WEAPON_APPEARANCE_MAPPING_FILE,
    battle_weapon_field2_from_icon,
    battle_weapon_image_from_icon,
    default_item_registry,
    weapon_icon_to_image_mapping,
)
from protocol import decode_frame, field_values
from server import Settings, battle_actor_frames, character_appearance, equipped_weapon_battle_field2


EXPECTED_GROUPS = {
    21: (220, 0), 22: (260, 0), 23: (271, 1), 24: (250, 0),
    25: (231, 0), 26: (280, 0), 27: (242, 0), 28: (240, 0),
    29: (241, 0), 30: (221, 0), 31: (290, 0), 32: (270, 0),
    33: (230, 0),
}


def expected_visual_mapping():
    result = {}
    for group, (family, offset) in EXPECTED_GROUPS.items():
        for variant in range(10):
            result[group * 100 + variant] = family * 100 + variant + offset
    return result


class WeaponAppearanceConsistencyTests(unittest.TestCase):
    def test_correspondence_is_stored_in_catalog(self):
        data = json.loads(WEAPON_APPEARANCE_MAPPING_FILE.read_text(encoding='utf-8'))
        stored = {int(k): int(v) for k, v in data['icon_to_weapon_image'].items()}
        self.assertEqual(data['kind'], 'weapon_appearance_mapping')
        self.assertEqual(data['status'], 'user_confirmed_visual_mapping')
        self.assertEqual(len(stored), 130)
        self.assertEqual(stored, expected_visual_mapping())

    def test_runtime_reads_catalog_mapping(self):
        stored = expected_visual_mapping()
        self.assertEqual(weapon_icon_to_image_mapping(), stored)
        self.assertFalse(hasattr(item_registry, 'WEAPON_ICON_GROUP_TO_BATTLE_FAMILY'))
        for icon_code, weapon_image in stored.items():
            self.assertEqual(battle_weapon_image_from_icon(icon_code), weapon_image)

    def test_special_rows_are_data_not_code_guesses(self):
        self.assertEqual(battle_weapon_image_from_icon(2300), 27101)
        self.assertEqual(battle_weapon_image_from_icon(2309), 27110)
        self.assertEqual(battle_weapon_image_from_icon(2500), 23100)
        self.assertEqual(battle_weapon_image_from_icon(2509), 23109)
        self.assertEqual(battle_weapon_image_from_icon(3400), 0)

    def test_all_130_preview_weapons_use_catalog_mapping(self):
        root = Path(__file__).resolve().parents[1]
        preview = json.loads(
            (root / 'data/catalog/equipment_resource_preview_items.json').read_text(encoding='utf-8')
        )
        stored = weapon_icon_to_image_mapping()
        weapons = [x for x in preview['items'] if int(x.get('equipment_slot', 0)) == 10]
        self.assertEqual(len(weapons), 130)
        for item in weapons:
            icon = int(item['icon_code'])
            quality = int(item['quality'])
            code = int(item['appearance_properties']['7'])
            self.assertEqual(code // 10, stored[icon], icon)
            self.assertEqual(code, stored[icon] * 10 + quality, icon)
            self.assertEqual(code, battle_weapon_field2_from_icon(icon, quality), icon)

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
        preview = json.loads(
            (root / 'data/catalog/equipment_resource_preview_items.json').read_text(encoding='utf-8')
        )
        item = next(
            x for x in preview['items']
            if int(x.get('equipment_slot', 0)) == 10 and int(x['icon_code']) == 3200
        )
        registry = default_item_registry()
        role = {'id': 10001, 'name': '测试角色', 'model': 19, 'items': [
            {'id': 1, 'template_id': int(item['template_id']), 'quantity': 1, 'location': 'equipped'}
        ]}
        map_code = character_appearance(role, registry)[7]
        self.assertEqual(map_code, 270001)
        self.assertEqual(equipped_weapon_battle_field2(role, registry), map_code)
        _, fields = decode_frame(
            battle_actor_frames(role, Settings(item_registry=registry))[0]
        )
        self.assertEqual(field_values(fields)[2], map_code)

    def test_unequipped_is_zero(self):
        registry = default_item_registry()
        role = {'id': 10001, 'name': '测试角色', 'model': 19, 'items': []}
        self.assertEqual(character_appearance(role, registry)[7], 0)
        self.assertEqual(equipped_weapon_battle_field2(role, registry), 0)


if __name__ == '__main__':
    unittest.main()
