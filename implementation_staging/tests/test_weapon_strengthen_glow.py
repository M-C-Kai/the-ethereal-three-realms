import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from item_registry import battle_weapon_image_from_icon
from protocol import decode_frame, field_values
from server import (
    Settings,
    battle_actor_frames,
    character_appearance,
    default_role,
    equipped_weapon_battle_field2,
    item_slot,
    role_items,
    role_list,
)


class WeaponStrengthenGlowTests(unittest.TestCase):
    def setUp(self):
        self.settings = Settings()
        self.role = default_role(self.settings)
        self.weapon = next(
            item for item in role_items(self.role)
            if item_slot(item, self.settings.item_registry) == 10
        )
        self.weapon['location'] = 'equipped'
        resolved = self.settings.item_registry.resolve(self.weapon)
        self.icon_code = int(resolved['icon_code'])
        self.weapon_image = battle_weapon_image_from_icon(self.icon_code)
        self.assertGreater(self.weapon_image, 0)

    def expected_code(self, strengthen_level):
        selector = 0 if strengthen_level < 4 else strengthen_level - 3
        return self.weapon_image * 10 + selector

    def test_map_and_battle_use_strengthen_level_4_to_9_for_six_glow_stages(self):
        for level in range(10):
            with self.subTest(level=level):
                self.weapon['strengthen_level'] = level
                expected = self.expected_code(level)
                self.assertEqual(
                    character_appearance(self.role, self.settings.item_registry)[7],
                    expected,
                )
                self.assertEqual(
                    equipped_weapon_battle_field2(self.role, self.settings.item_registry),
                    expected,
                )
                _, fields = decode_frame(battle_actor_frames(self.role, self.settings)[0])
                self.assertEqual(field_values(fields)[2], expected)

    def test_login_1080_uses_same_strengthening_glow_selector(self):
        for level in (0, 3, 4, 5, 8, 9):
            with self.subTest(level=level):
                self.weapon['strengthen_level'] = level
                _, fields = decode_frame(role_list(self.settings, [self.role]))
                values = field_values(fields)
                record = values[2:17]
                self.assertEqual(record[2], self.expected_code(level))

    def test_template_quality_no_longer_forces_live_glow_at_plus_zero(self):
        resolved = self.settings.item_registry.resolve(self.weapon)
        self.assertGreater(int(resolved.get('quality', 0)), 0)
        self.weapon['strengthen_level'] = 0
        expected = self.weapon_image * 10
        self.assertEqual(
            character_appearance(self.role, self.settings.item_registry)[7],
            expected,
        )
        self.assertEqual(
            equipped_weapon_battle_field2(self.role, self.settings.item_registry),
            expected,
        )


if __name__ == '__main__':
    unittest.main()
