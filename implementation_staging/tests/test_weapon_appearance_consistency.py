import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from protocol import decode_frame, field_values
from server import battle_actor_frame


class WeaponAppearanceConsistencyTests(unittest.TestCase):
    def test_battle_1048_uses_same_weapon_code_as_map_property7(self):
        weapon_code = 270001
        frame = battle_actor_frame(
            actor_id=10001,
            model=19,
            name='测试角色',
            kind=1,
            side_code=2,
            slot=1,
            appearance={7: weapon_code, 14: 0, 15: 0, 16: 0, 17: 0, 18: 0, 19: 0, 20: 0},
            current_hp=100,
            max_hp=100,
        )
        message_id, fields = decode_frame(frame)
        self.assertEqual(message_id, 1048)
        self.assertEqual(field_values(fields)[2], weapon_code)

    def test_battle_1048_has_no_weapon_when_map_property7_is_zero(self):
        frame = battle_actor_frame(
            actor_id=10001,
            model=19,
            name='测试角色',
            kind=1,
            side_code=2,
            slot=1,
            appearance={7: 0},
            current_hp=100,
            max_hp=100,
        )
        _, fields = decode_frame(frame)
        self.assertEqual(field_values(fields)[2], 0)

    def test_all_preview_weapons_reference_confirmed_nonzero_property7_resources(self):
        root = Path(__file__).resolve().parents[1]
        preview = json.loads((root / 'data/catalog/equipment_resource_preview_items.json').read_text(encoding='utf-8'))
        audit = json.loads((root / 'references/weapon-appearance-audit/property7_candidates.json').read_text(encoding='utf-8'))
        confirmed = {
            int(row['property7_low4_candidate'])
            for row in audit['candidates']
            if row.get('role_dat_exists') and row.get('weapon_image_exists')
        }
        weapons = [row for row in preview['items'] if int(row.get('equipment_slot', 0)) == 10]
        self.assertTrue(weapons)
        for row in weapons:
            code = int(row.get('appearance_properties', {}).get('7', 0))
            self.assertNotEqual(code, 0, row.get('name'))
            self.assertIn(code % 10000, confirmed, row.get('name'))


if __name__ == '__main__':
    unittest.main()
