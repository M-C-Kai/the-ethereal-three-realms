from __future__ import annotations

import unittest

from protocol import TYPE_INT, byte, encode_payload, field_values, integer
import server_pets as pets


class RoamingBossInteractionTests(unittest.TestCase):
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


if __name__ == '__main__':
    unittest.main()
