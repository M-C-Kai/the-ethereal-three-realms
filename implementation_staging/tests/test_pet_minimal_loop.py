import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

from protocol import TYPE_BYTE, TYPE_INT, TYPE_STRING, decode_frame


class PetMinimalLoopTests(unittest.TestCase):
    def _modules(self):
        self.assertIsNotNone(importlib.util.find_spec('pet_registry'))
        self.assertIsNotNone(importlib.util.find_spec('pet_protocol'))
        import pet_registry
        import pet_protocol
        return pet_registry, pet_protocol

    def test_pet_modules_exist(self):
        self._modules()

    def test_catalog_loads_one_renderable_test_pet(self):
        pet_registry, _ = self._modules()
        registry = pet_registry.default_pet_registry()
        definition = registry.require(50100)
        self.assertEqual(definition.name, '测试灵宠')
        self.assertEqual(definition.model_dat_id, 50100)
        self.assertEqual(definition.pet_type, 1)

    def test_starter_pet_is_idempotent_and_persistable(self):
        pet_registry, pet_protocol = self._modules()
        role = {'id': 10001}
        registry = pet_registry.default_pet_registry()
        self.assertTrue(pet_protocol.ensure_role_pets(role, registry))
        self.assertFalse(pet_protocol.ensure_role_pets(role, registry))
        self.assertEqual(len(role['pets']), 1)
        pet = role['pets'][0]
        self.assertEqual(pet['template_id'], 50100)
        self.assertEqual(pet['level'], 1)
        self.assertFalse(pet['deployed'])
        self.assertFalse(pet['walking'])
        json.dumps(role, ensure_ascii=False)

    def test_1127_action_1_uses_property_index_layout_through_property_12(self):
        pet_registry, pet_protocol = self._modules()
        registry = pet_registry.default_pet_registry()
        role = {'id': 10001}
        pet_protocol.ensure_role_pets(role, registry)
        frame = pet_protocol.pet_instance_frame(role['pets'][0], registry)
        message_id, fields = decode_frame(frame)
        self.assertEqual(message_id, 1127)
        self.assertEqual(len(fields), 13)
        self.assertEqual(fields[0].type_id, TYPE_BYTE)
        self.assertEqual(fields[0].value, 1)
        self.assertEqual(fields[1].type_id, TYPE_INT)
        self.assertEqual(fields[1].value, role['pets'][0]['id'])
        self.assertEqual(fields[2].type_id, TYPE_INT)
        self.assertEqual(fields[2].value, 50100)
        self.assertEqual(fields[3].type_id, TYPE_STRING)
        self.assertEqual(fields[3].value, '测试灵宠')
        self.assertEqual(fields[7].type_id, TYPE_INT)
        self.assertEqual(fields[7].value, 1)
        self.assertEqual(fields[11].value, 0)
        self.assertEqual(fields[12].value, 0)

    def test_role_pet_frames_emit_all_owned_pets(self):
        pet_registry, pet_protocol = self._modules()
        registry = pet_registry.default_pet_registry()
        role = {'id': 10001}
        pet_protocol.ensure_role_pets(role, registry)
        frames = pet_protocol.role_pet_frames(role, registry)
        self.assertEqual(len(frames), 1)
        self.assertEqual(decode_frame(frames[0])[0], 1127)

    def test_1130_exact_request_types_and_state_transition(self):
        pet_registry, pet_protocol = self._modules()
        from protocol import byte, integer

        registry = pet_registry.default_pet_registry()
        role = {'id': 10001}
        pet_protocol.ensure_role_pets(role, registry)
        pet_id = role['pets'][0]['id']

        deployed_fields = [byte(10), integer(pet_id), byte(1)]
        result = pet_protocol.apply_pet_state_request(role, deployed_fields)
        self.assertTrue(result.changed)
        self.assertEqual(result.pet_id, pet_id)
        self.assertTrue(role['pets'][0]['deployed'])

        walking_fields = [byte(48), integer(pet_id), byte(1)]
        result = pet_protocol.apply_pet_state_request(role, walking_fields)
        self.assertTrue(result.changed)
        self.assertTrue(role['pets'][0]['walking'])

        bad_types = [integer(48), integer(pet_id), byte(0)]
        result = pet_protocol.apply_pet_state_request(role, bad_types)
        self.assertFalse(result.changed)
        self.assertEqual(result.reason, 'invalid_request')


if __name__ == '__main__':
    unittest.main()
