import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from protocol import decode_frame, field_values
from server import (
    Settings,
    character_appearance,
    character_equipment_refresh_frames,
    character_panel_frames,
    combat_stats,
    default_role,
    effective_character_stats,
    equipped_attribute_totals,
    item_slot,
    role_items,
    role_list,
)


class CharacterEquipmentRefreshTests(unittest.TestCase):
    def setUp(self):
        self.settings = Settings()
        self.role = default_role(self.settings)

    def _equipment_in_slot(self, slot):
        return next(
            item for item in role_items(self.role)
            if item_slot(item, self.settings.item_registry) == slot
        )

    def test_role_list_uses_apk_appearance_contract_not_role_stats(self):
        armor = self._equipment_in_slot(3)
        weapon = self._equipment_in_slot(10)
        armor['location'] = 'equipped'
        weapon['location'] = 'equipped'
        self.role['level'] = 17
        self.role['race'] = 2
        self.role['gender'] = 1
        self.role['stats'] = [91, 92, 93, 94, 95, 96, 97, 98]

        message_id, fields = decode_frame(role_list(self.settings, [self.role]))
        values = field_values(fields)
        self.assertEqual(message_id, 1080)
        self.assertEqual(values[:2], [0, 1])
        record = values[2:17]
        appearance = character_appearance(self.role, self.settings.item_registry)
        self.assertEqual(record[0], self.role['id'])
        self.assertEqual(record[1], 17)
        self.assertEqual(record[2], appearance[7])
        self.assertEqual(record[3], self.role['model'])
        self.assertEqual(record[4], 21)
        self.assertEqual(record[5], self.role['name'])
        self.assertEqual(record[6], self.role['slot'])
        self.assertEqual(
            record[7:15],
            [appearance[index] for index in (2, 14, 15, 16, 17, 18, 19, 20)],
        )
        self.assertNotEqual(record[7:15], self.role['stats'])

    def test_equipment_attribute_totals_follow_equipped_instances(self):
        weapon = self._equipment_in_slot(10)
        shoulder = self._equipment_in_slot(2)
        weapon['location'] = 'equipped'
        shoulder['location'] = 'equipped'
        weapon['equipment_attributes'] = [15, 0, 0, 0]
        shoulder['equipment_attributes'] = [0, 7, 0, 0]
        self.assertEqual(
            equipped_attribute_totals(self.role, self.settings.item_registry)[:2],
            (15, 7),
        )

    def test_character_and_battle_stats_share_equipped_attack_defence(self):
        weapon = self._equipment_in_slot(10)
        shoulder = self._equipment_in_slot(2)
        weapon['location'] = 'equipped'
        shoulder['location'] = 'equipped'
        weapon['equipment_attributes'] = [15, 0, 0, 0]
        shoulder['equipment_attributes'] = [0, 7, 0, 0]

        raw = [max(0, int(v)) for v in self.role['stats'][:5]]
        display = effective_character_stats(self.role, self.settings.item_registry)
        self.assertEqual(display[0], raw[0] + 15)
        self.assertEqual(display[1], raw[1] + 7)
        battle = combat_stats(self.role, self.settings.item_registry)
        self.assertEqual(battle.physical_attack, 10 + raw[0] + 15)
        self.assertEqual(battle.physical_defence, raw[1] + 7)

    def test_full_refresh_contains_appearance_and_live_panel_stats(self):
        armor = self._equipment_in_slot(3)
        weapon = self._equipment_in_slot(10)
        armor['location'] = 'equipped'
        weapon['location'] = 'equipped'
        weapon['equipment_attributes'] = [13, 0, 0, 0]

        refresh_1017, refresh_1039 = character_equipment_refresh_frames(
            self.role, self.settings.item_registry
        )
        message_id, fields = decode_frame(refresh_1017)
        self.assertEqual(message_id, 1017)
        values = field_values(fields)
        self.assertEqual(values[0], 0)
        self.assertEqual(values[1], self.role['id'])
        pair_count = values[2]
        pairs = {
            int(values[3 + i * 2]): int(values[4 + i * 2])
            for i in range(pair_count)
        }
        appearance = character_appearance(self.role, self.settings.item_registry)
        for index, value in appearance.items():
            self.assertEqual(pairs[index], value)
        display = effective_character_stats(self.role, self.settings.item_registry)
        for index, value in enumerate(display, start=44):
            self.assertEqual(pairs[index], value)

        panel_id, panel_fields = decode_frame(refresh_1039)
        self.assertEqual(panel_id, 1039)
        panel_values = field_values(panel_fields)
        self.assertEqual(panel_values[0], 1)
        self.assertEqual(panel_values[-5:], display)

    def test_character_panel_changes_immediately_when_equipment_changes(self):
        weapon = self._equipment_in_slot(10)
        _, before = character_panel_frames(self.role, self.settings.item_registry)
        before_stats = effective_character_stats(self.role, self.settings.item_registry)
        weapon['location'] = 'equipped'
        weapon['equipment_attributes'] = [21, 0, 0, 0]
        attributes, _ = character_panel_frames(self.role, self.settings.item_registry)
        _, fields = decode_frame(attributes)
        values = field_values(fields)
        self.assertEqual(values[-5], before_stats[0] + 21)


class _AlwaysSuccessRng:
    def randrange(self, stop):
        return 0


class CharacterStrengtheningRefreshTests(unittest.TestCase):
    def test_strengthening_equipped_weapon_appends_1017_and_1039_refresh(self):
        import server as server_module
        from strengthening import INITIAL_STRENGTHEN_STONE_TEMPLATE_ID

        settings = server_module.Settings()
        role = server_module.default_role(settings)
        weapon = next(
  item for item in server_module.role_items(role)
  if server_module.item_slot(item, settings.item_registry) == 10
        )
        stone = next(
  item for item in server_module.role_items(role)
  if int(item.get('template_id', 0)) == INITIAL_STRENGTHEN_STONE_TEMPLATE_ID
        )
        weapon['location'] = 'equipped'
        server_module.ensure_weapon_base_attributes(weapon, settings.item_registry)

        game_server = server_module.LocalGameServer(settings)
        game_server.roles.save = lambda: None
        frames = game_server.handle_strengthening_request(
  role,
  [92, int(weapon['id']), int(stone['id']), 5],
  rng=_AlwaysSuccessRng(),
        )

        message_ids = [decode_frame(frame)[0] for frame in frames]
        self.assertGreaterEqual(len(message_ids), 2)
        self.assertEqual(message_ids[-2:], [1017, 1039])
        _, refresh_fields = decode_frame(frames[-1])
        self.assertEqual(field_values(refresh_fields)[0], 1)

if __name__ == '__main__':
    unittest.main()
