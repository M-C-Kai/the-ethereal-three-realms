from __future__ import annotations

import unittest

from protocol import TYPE_INT, byte, encode_payload, field_values, integer
import server_pets as pets


class RoamingBossInteractionTests(unittest.TestCase):
    def setUp(self):
        self.role = {
            'id': 10001,
            'map_id': pets._dynamic.ROAMING_BOSS_MAP_ID,
            'map_x': 7,
            'map_y': 28,
        }
        self.role_token = pets._ACTIVE_ROLE.set(self.role)
        self.entered_token = pets._ROAMING_BOSS_ENTERED_AT.set(100.0)
        self.spawn_token = pets._ROAMING_BOSS_SPAWN_TILE.set((9, 28))

    def tearDown(self):
        pets._ROAMING_BOSS_SPAWN_TILE.reset(self.spawn_token)
        pets._ROAMING_BOSS_ENTERED_AT.reset(self.entered_token)
        pets._ACTIVE_ROLE.reset(self.role_token)

    def test_native_q_fight_request_routes_into_existing_map_interaction_handler(self):
        message_id, fields = pets.pet_decode_payload(encode_payload(2029, [
            byte(1),
            integer(pets._dynamic.ROAMING_BOSS_ID),
        ]))

        self.assertEqual(message_id, 2031)
        self.assertEqual(field_values(fields), [pets._dynamic.ROAMING_BOSS_ID])
        self.assertEqual([field.type_id for field in fields], [TYPE_INT])

    def test_other_2029_requests_are_not_rewritten(self):
        message_id, fields = pets.pet_decode_payload(encode_payload(2029, [
            byte(1),
            integer(700_002),
        ]))

        self.assertEqual(message_id, 2029)
        self.assertEqual(field_values(fields), [1, 700_002])

    def test_player_entering_spawn_contact_radius_becomes_boss_interaction(self):
        message_id, fields = pets._translate_roaming_boss_contact_request(
            1005,
            [integer(8), integer(28)],
            now=100.5,
        )

        self.assertEqual(message_id, 2031)
        self.assertEqual(
            field_values(fields),
            [pets._dynamic.ROAMING_BOSS_ID, 0, 8, 28, 6, 0],
        )
        self.assertEqual((self.role['map_x'], self.role['map_y']), (8, 28))

    def test_player_entering_moved_boss_contact_radius_uses_current_target(self):
        message_id, fields = pets._translate_roaming_boss_contact_request(
            1005,
            [integer(11), integer(28)],
            now=104.0,
        )

        self.assertEqual(message_id, 2031)
        self.assertEqual(
            field_values(fields),
            [pets._dynamic.ROAMING_BOSS_ID, 0, 11, 28, 6, 0],
        )

    def test_far_player_movement_stays_normal_1005(self):
        original_fields = [integer(20), integer(20)]
        message_id, fields = pets._translate_roaming_boss_contact_request(
            1005,
            original_fields,
            now=104.0,
        )

        self.assertEqual(message_id, 1005)
        self.assertIs(fields, original_fields)

    def test_contact_attempt_is_not_latched_outside_battle_state(self):
        first_message_id, _ = pets._translate_roaming_boss_contact_request(
            1005,
            [integer(11), integer(28)],
            now=104.0,
        )
        second_message_id, _ = pets._translate_roaming_boss_contact_request(
            1005,
            [integer(12), integer(28)],
            now=104.1,
        )

        self.assertEqual(first_message_id, 2031)
        self.assertEqual(second_message_id, 2031)


if __name__ == '__main__':
    unittest.main()
