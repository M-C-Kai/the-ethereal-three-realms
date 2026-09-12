import unittest

from pet_protocol_core import (
    parse_pet_release_request,
    parse_pet_rename_request,
    parse_pet_stat_request,
    pet_property_update_frame,
    pet_release_frame,
    pet_rename_frame,
)
from protocol import (
    TYPE_BYTE,
    TYPE_INT,
    TYPE_SHORT,
    TYPE_STRING,
    byte,
    decode_frame,
    integer,
    short,
    string,
)


class PetProtocolCoreTests(unittest.TestCase):
    def test_rename_native_layout(self):
        fields = [byte(15), integer(123), string('灵狐')]
        self.assertEqual(parse_pet_rename_request(fields), (123, '灵狐'))
        message_id, out = decode_frame(pet_rename_frame(123, '灵狐'))
        self.assertEqual(message_id, 1130)
        self.assertEqual(
            [(field.type_id, field.value) for field in out],
            [(TYPE_BYTE, 15), (TYPE_INT, 123), (TYPE_STRING, '灵狐')],
        )
        self.assertIsNone(parse_pet_rename_request([integer(15), integer(123), string('灵狐')]))

    def test_release_native_layout(self):
        fields = [byte(1), integer(123)]
        self.assertEqual(parse_pet_release_request(fields), 123)
        message_id, out = decode_frame(pet_release_frame(123))
        self.assertEqual(message_id, 1130)
        self.assertEqual(
            [(field.type_id, field.value) for field in out],
            [(TYPE_BYTE, 1), (TYPE_INT, 123)],
        )
        self.assertIsNone(parse_pet_release_request([integer(1), integer(123)]))

    def test_stat_allocate_native_layout(self):
        fields = [integer(123), short(2), short(1), short(2), short(3), short(4), short(5)]
        self.assertEqual(parse_pet_stat_request(fields), (123, (1, 2, 3, 4, 5)))
        self.assertIsNone(parse_pet_stat_request([integer(123), integer(2), short(1), short(2), short(3), short(4), short(5)]))

    def test_property_update_layout(self):
        message_id, fields = decode_frame(pet_property_update_frame(123, [(32, 11), (37, 0)]))
        self.assertEqual(message_id, 1134)
        self.assertEqual(
            [(field.type_id, field.value) for field in fields],
            [
                (TYPE_BYTE, 0), (TYPE_INT, 123), (TYPE_INT, 2),
                (TYPE_BYTE, 32), (TYPE_INT, 11),
                (TYPE_BYTE, 37), (TYPE_INT, 0),
            ],
        )


if __name__ == '__main__':
    unittest.main()
