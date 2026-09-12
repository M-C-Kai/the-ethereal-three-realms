import unittest

from pet_core_bridge import handle_pet_core_action, translate_pet_core_request
from pet_model import ensure_pet_schema
from pet_registry import default_pet_registry
from protocol import (
    TYPE_BYTE,
    TYPE_INT,
    TYPE_STRING,
    byte,
    decode_frame,
    field_values,
    integer,
    short,
    string,
)


class _Roles:
    def __init__(self):
        self.saves = 0

    def save(self):
        self.saves += 1


class _Server:
    def __init__(self):
        self.roles = _Roles()


class PetServerCoreTests(unittest.TestCase):
    def setUp(self):
        self.role = {'id': 10001}
        ensure_pet_schema(self.role, default_pet_registry())
        self.pet = self.role['pets'][0]
        self.pet_id = int(self.pet['id'])
        self.server = _Server()

    def _translate_values(self, message_id, fields):
        translated_id, translated_fields = translate_pet_core_request(message_id, fields)
        self.assertEqual(translated_id, 1103)
        return field_values(translated_fields)

    def test_rename_routes_and_acks_with_native_1130_action15(self):
        values = self._translate_values(1130, [byte(15), integer(self.pet_id), string('灵狐')])
        frames = handle_pet_core_action(self.server, self.role, values)
        self.assertEqual(self.server.roles.saves, 1)
        self.assertEqual(self.pet['name'], '灵狐')
        self.assertEqual(len(frames), 1)
        message_id, fields = decode_frame(frames[0])
        self.assertEqual(message_id, 1130)
        self.assertEqual(
            [(field.type_id, field.value) for field in fields],
            [(TYPE_BYTE, 15), (TYPE_INT, self.pet_id), (TYPE_STRING, '灵狐')],
        )

    def test_release_walking_pet_detaches_map_before_native_release_ack(self):
        self.pet['walking'] = True
        values = self._translate_values(1130, [byte(1), integer(self.pet_id)])
        frames = handle_pet_core_action(self.server, self.role, values)
        self.assertEqual(self.server.roles.saves, 1)
        self.assertEqual(self.role['pets'], [])
        self.assertEqual(len(frames), 2)
        self.assertEqual(decode_frame(frames[0])[0], 1010)
        message_id, fields = decode_frame(frames[1])
        self.assertEqual(message_id, 1130)
        self.assertEqual(
            [(field.type_id, field.value) for field in fields],
            [(TYPE_BYTE, 1), (TYPE_INT, self.pet_id)],
        )

    def test_stat_allocate_routes_exact_short_layout_and_returns_1134(self):
        self.pet['remaining_points'] = 5
        values = self._translate_values(
            1128,
            [
                integer(self.pet_id), short(2),
                short(1), short(1), short(1), short(1), short(1),
            ],
        )
        frames = handle_pet_core_action(self.server, self.role, values)
        self.assertEqual(self.server.roles.saves, 1)
        self.assertEqual(self.pet['remaining_points'], 0)
        self.assertEqual(self.pet['base_stats'], [11, 11, 11, 11, 11])
        message_id, fields = decode_frame(frames[0])
        self.assertEqual(message_id, 1134)
        self.assertEqual((fields[0].type_id, fields[0].value), (TYPE_BYTE, 0))
        self.assertEqual((fields[1].type_id, fields[1].value), (TYPE_INT, self.pet_id))
        self.assertEqual(fields[2].type_id, TYPE_INT)
        self.assertEqual(fields[2].value, 15)

    def test_wrong_1128_action_is_not_intercepted(self):
        original = [integer(self.pet_id), short(3), short(0), short(0), short(0), short(0), short(0)]
        message_id, fields = translate_pet_core_request(1128, original)
        self.assertEqual(message_id, 1128)
        self.assertIs(fields, original)

    def test_wrong_types_are_not_intercepted(self):
        original = [byte(15), integer(self.pet_id), integer(123)]
        message_id, fields = translate_pet_core_request(1130, original)
        self.assertEqual(message_id, 1130)
        self.assertIs(fields, original)


if __name__ == '__main__':
    unittest.main()
