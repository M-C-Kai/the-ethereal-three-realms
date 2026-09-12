import unittest

from pet_protocol import (
    apply_pet_state_request,
    pet_map_attach_frame,
    pet_map_detach_frame,
    pet_state_response_frames,
)
from protocol import TYPE_BYTE, TYPE_INT, TYPE_SHORT, byte, decode_frame, integer


class PetWalkingMapTests(unittest.TestCase):
    def test_walk_attach_uses_1127_action_13_for_local_role(self):
        message_id, fields = decode_frame(pet_map_attach_frame(10001001, 10001))
        self.assertEqual(message_id, 1127)
        self.assertEqual(
            [(field.type_id, field.value) for field in fields],
            [(TYPE_BYTE, 13), (TYPE_INT, 10001001), (TYPE_INT, 10001)],
        )

    def test_walk_hide_uses_1010_action_102_for_role(self):
        message_id, fields = decode_frame(pet_map_detach_frame(10001))
        self.assertEqual(message_id, 1010)
        self.assertEqual(fields[0].type_id, TYPE_INT)
        self.assertEqual(fields[0].value, 10001)
        self.assertEqual(fields[5].type_id, TYPE_SHORT)
        self.assertEqual(fields[5].value, 102)

    def test_walking_state_reply_adds_map_attach_after_property_update(self):
        role = {'id': 10001, 'pets': [{'id': 10001001, 'walking': False, 'deployed': False}]}
        result = apply_pet_state_request(role, [byte(48), integer(10001001), byte(1)])
        frames = pet_state_response_frames(role['id'], result)
        self.assertEqual([decode_frame(frame)[0] for frame in frames], [1134, 1127])
        self.assertEqual(decode_frame(frames[-1])[1][0].value, 13)

    def test_walking_hide_reply_adds_map_detach_after_property_update(self):
        role = {'id': 10001, 'pets': [{'id': 10001001, 'walking': True, 'deployed': False}]}
        result = apply_pet_state_request(role, [byte(48), integer(10001001), byte(0)])
        frames = pet_state_response_frames(role['id'], result)
        self.assertEqual([decode_frame(frame)[0] for frame in frames], [1134, 1010])
        self.assertEqual(decode_frame(frames[-1])[1][5].value, 102)


if __name__ == '__main__':
    unittest.main()
