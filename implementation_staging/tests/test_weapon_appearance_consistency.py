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
from server import (
    Settings,
    battle_actor_frame,
    battle_actor_frames,
    character_appearance,
    equipped_weapon_battle_field2,
)

EXPECTED_FAMILIES = {
    21: 220, 22: 260, 23: 271, 24: 250, 25: 231, 26: 280, 27: 242,
    28: 240, 29: 241, 30: 221, 31: 290, 32: 270, 33: 230,
}

class WeaponAppearanceConsistencyTests(unittest.TestCase):
    def test_user_confirmed_icon_group_to_battle_family_mapping(self):
        self.assertEqual(WEAPON_ICON_GROUP_TO_BATTLE_FAMILY, EXPECTED_FAMILIES)

    def test_all_130_weapon_icons_follow_extracted_battle_family_rows(self):
        root = Path(__file__).resolve().parents[1]
        manifest = json.loads((root / 'references/battle-weapon-appearance-audit/manifest.json').read_text(encoding='utf-8'))
        families = manifest['battle_weapon_families']
        for icon_group, battle_family in EXPECTED_FAMILIES.items():
            extracted = [int(value) for value in families[str(battle_family)]]
            self.assertGreaterEqual(len(extracted), 10, battle_family)
            mapped_images = extracted[:10]
            for variant, expected_image in enumerate(mapped_images):
                icon_code = icon_group * 100 + variant
                self.assertEqual(battle_weapon_image_from_icon(icon_code), expected_image, icon_code)
                self.assertEqual(battle_weapon_field2_from_icon(icon_code, 1), expected_image * 10 + 1, icon_code)

    def test_group_25_uses_first_ten_of_twelve_231_family_images(self):
        self.assertEqual(battle_weapon_image_from_icon(2500), 23100)
        self.assertEqual(battle_weapon_image_from_icon(2509), 23109)

    def test_special_23_group_uses_27101_through_27110(self):
        self.assertEqual(battle_weapon_image_from_icon(2300), 27101)
        self.assertEqual(battle_weapon_image_from_icon(2309), 27110)
        self.assertEqual(battle_weapon_field2_from_icon(2300, 1), 271011)
        self.assertEqual(battle_weapon_field2_from_icon(2309, 1), 271101)

    def test_unknown_group_variant_or_quality_never_invents_battle_appearance(self):
        self.assertEqual(battle_weapon_image_from_icon(2000), 0)
        self.assertEqual(battle_weapon_image_from_icon(2110), 0)
        self.assertEqual(battle_weapon_field2_from_icon(2100, 10), 0)

    def test_equipped_weapon_icon_drives_1048_field2_independently_of_map_property7(self):
        root = Path(__file__).resolve().parents[1]
        preview = json.loads((root / 'data/catalog/equipment_resource_preview_items.json').read_text(encoding='utf-8'))
        item = next(row for row in preview['items'] if int(row.get('equipment_slot', 0)) == 10 and int(row.get('icon_code', 0)) == 3200)
        registry = default_item_registry()
        role = {
            'id': 10001, 'name': '测试角色', 'model': 19,
            'items': [{'id': 1, 'template_id': int(item['template_id']), 'quantity': 1, 'location': 'equipped'}],
        }
        self.assertGreater(character_appearance(role, registry)[7], 0)
        self.assertEqual(equipped_weapon_battle_field2(role, registry), 270001)
        settings = Settings(item_registry=registry)
        message_id, fields = decode_frame(battle_actor_frames(role, settings)[0])
        self.assertEqual(message_id, 1048)
        self.assertEqual(field_values(fields)[2], 270001)

    def test_battle_actor_frame_uses_explicit_battle_weapon_code(self):
        frame = battle_actor_frame(
            actor_id=10001, model=19, name='测试角色', kind=1, side_code=2, slot=1,
            appearance={7: 333003}, weapon_field2=220001, current_hp=100, max_hp=100,
        )
        message_id, fields = decode_frame(frame)
        self.assertEqual(message_id, 1048)
        self.assertEqual(field_values(fields)[2], 220001)

    def test_no_equipped_weapon_sends_zero_battle_weapon(self):
        registry = default_item_registry()
        role = {'id': 10001, 'name': '测试角色', 'model': 19, 'items': []}
        self.assertEqual(equipped_weapon_battle_field2(role, registry), 0)

if __name__ == '__main__':
    unittest.main()
