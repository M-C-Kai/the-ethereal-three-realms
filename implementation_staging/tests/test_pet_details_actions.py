import unittest

from pet_registry import default_pet_registry
from pet_protocol import (
    apply_pet_state_request,
    ensure_role_pets,
    is_pet_detail_request,
    is_pet_skill_request,
    is_pet_state_request,
    pet_detail_frame,
    pet_instance_frame,
    pet_property_update_frame,
    pet_skill_list_frame,
)
from protocol import TYPE_BYTE, TYPE_INT, TYPE_STRING, byte, decode_frame, integer


class PetDetailsActionsTests(unittest.TestCase):
    def setUp(self):
        self.registry = default_pet_registry()
        self.role = {'id': 10001}
        ensure_role_pets(self.role, self.registry)
        self.pet = self.role['pets'][0]

    @staticmethod
    def property_field(fields, property_id):
        # 1127/action=9 field[2] maps to property 30.
        return fields[property_id - 28]

    def test_action_1_property_9_is_confirmed_carry_level_gate(self):
        _, fields = decode_frame(pet_instance_frame(self.pet, self.registry))
        self.assertEqual(fields[9].type_id, TYPE_INT)
        self.assertEqual(fields[9].value, 1)

    def test_1127_action_9_maps_properties_30_through_90(self):
        frame = pet_detail_frame(self.pet, self.registry)
        message_id, fields = decode_frame(frame)

        self.assertEqual(message_id, 1127)
        self.assertEqual(len(fields), 63)
        self.assertEqual((fields[0].type_id, fields[0].value), (TYPE_BYTE, 9))
        self.assertEqual((fields[1].type_id, fields[1].value), (TYPE_INT, self.pet['id']))

        self.assertEqual(self.property_field(fields, 30).value, 0)
        self.assertGreater(self.property_field(fields, 31).value, 0)
        self.assertEqual(
            self.property_field(fields, 38).value,
            self.property_field(fields, 39).value,
        )
        self.assertEqual(self.property_field(fields, 59).value, 100)
        self.assertEqual(self.property_field(fields, 60).value, 1)
        self.assertEqual(self.property_field(fields, 73).value, 0)
        self.assertEqual(self.property_field(fields, 77).value, 100)
        self.assertEqual(self.property_field(fields, 78).value, 0)
        self.assertEqual(self.property_field(fields, 79).type_id, TYPE_STRING)
        self.assertEqual(self.property_field(fields, 79).value, '测试灵宠')
        self.assertEqual(self.property_field(fields, 80).value, 0)
        self.assertEqual(self.property_field(fields, 82).value, 1)
        self.assertEqual(self.property_field(fields, 83).type_id, TYPE_STRING)
        for property_id in range(84, 91):
            self.assertGreaterEqual(self.property_field(fields, property_id).value, 500)

    def test_1103_action_10_empty_pet_skill_container(self):
        message_id, fields = decode_frame(pet_skill_list_frame(self.pet))
        self.assertEqual(message_id, 1103)
        self.assertEqual(
            [(field.type_id, field.value) for field in fields],
            [
                (TYPE_BYTE, 10),
                (TYPE_INT, self.pet['id']),
                (TYPE_BYTE, 0),
                (TYPE_BYTE, 0),
            ],
        )

    def test_1134_generic_property_update_layout(self):
        message_id, fields = decode_frame(
            pet_property_update_frame(self.pet['id'], [(11, 1)])
        )
        self.assertEqual(message_id, 1134)
        self.assertEqual(
            [(field.type_id, field.value) for field in fields],
            [
                (TYPE_BYTE, 0),
                (TYPE_INT, self.pet['id']),
                (TYPE_INT, 1),
                (TYPE_BYTE, 11),
                (TYPE_INT, 1),
            ],
        )

    def test_state_transition_reports_property_11_and_12_updates(self):
        result = apply_pet_state_request(
            self.role,
            [byte(10), integer(self.pet['id']), byte(1)],
        )
        self.assertEqual(result.updates, ((self.pet['id'], 11, 1),))

        result = apply_pet_state_request(
            self.role,
            [byte(48), integer(self.pet['id']), byte(1)],
        )
        self.assertEqual(result.updates, ((self.pet['id'], 12, 1),))

    def test_request_classifiers_preserve_exact_apk_field_types(self):
        pet_id = self.pet['id']
        self.assertTrue(is_pet_detail_request([byte(9), integer(pet_id)]))
        self.assertFalse(is_pet_detail_request([integer(9), integer(pet_id)]))

        self.assertTrue(is_pet_skill_request([byte(10), integer(pet_id)]))
        self.assertFalse(is_pet_skill_request([byte(10), byte(1)]))

        self.assertTrue(is_pet_state_request([byte(10), integer(pet_id), byte(1)]))
        self.assertTrue(is_pet_state_request([byte(48), integer(pet_id), byte(0)]))
        self.assertFalse(is_pet_state_request([integer(48), integer(pet_id), byte(0)]))


if __name__ == '__main__':
    unittest.main()
