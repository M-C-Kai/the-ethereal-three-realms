import unittest

from app.context import SystemContext
from protocol import (
    TYPE_BYTE,
    TYPE_INT,
    TYPE_STRING,
    byte,
    decode_frame,
    integer,
    short,
    string,
)
from systems.pet.handler import PetSystem
from systems.pet.registry import default_pet_registry
from systems.pet.service import ensure_pet_schema


class PetSystemTests(unittest.TestCase):
    def setUp(self):
        self.saves = 0
        self.role = {'id': 10001, 'items': []}
        ensure_pet_schema(self.role, default_pet_registry())
        self.pet = self.role['pets'][0]
        self.pet_id = int(self.pet['id'])
        self.context = SystemContext(username='tester', active_role=self.role)
        self.system = PetSystem(save=self._save)

    def _save(self):
        self.saves += 1

    def test_native_core_actions_are_owned_by_pet_system(self):
        self.assertTrue(self.system.can_handle(
            self.context, 1130, [byte(15), integer(self.pet_id), string('灵狐')]
        ))
        self.assertTrue(self.system.can_handle(
            self.context, 1130, [byte(1), integer(self.pet_id)]
        ))
        self.assertTrue(self.system.can_handle(
            self.context, 1128,
            [integer(self.pet_id), short(2), short(1), short(0), short(0), short(0), short(0)],
        ))
        self.assertTrue(self.system.can_handle(
            self.context, 1130,
            [byte(50), integer(self.pet_id), integer(399010011), integer(777001)],
        ))

    def test_rename_mutates_and_returns_native_ack(self):
        result = self.system.handle(
            self.context, 1130, [byte(15), integer(self.pet_id), string('灵狐')]
        )
        self.assertTrue(result.handled)
        self.assertEqual(self.pet['name'], '灵狐')
        self.assertEqual(self.saves, 1)
        message_id, fields = decode_frame(result.frames[0])
        self.assertEqual(message_id, 1130)
        self.assertEqual(
            [(field.type_id, field.value) for field in fields],
            [(TYPE_BYTE, 15), (TYPE_INT, self.pet_id), (TYPE_STRING, '灵狐')],
        )

    def test_release_walking_pet_detaches_map_then_removes_pet(self):
        self.pet['walking'] = True
        result = self.system.handle(
            self.context, 1130, [byte(1), integer(self.pet_id)]
        )
        self.assertTrue(result.handled)
        self.assertEqual(self.role['pets'], [])
        self.assertEqual(self.saves, 1)
        self.assertEqual([decode_frame(frame)[0] for frame in result.frames], [1010, 1130])

    def test_stat_allocation_uses_1128_and_returns_1134_batch(self):
        self.pet['remaining_points'] = 5
        result = self.system.handle(
            self.context,
            1128,
            [
                integer(self.pet_id), short(2),
                short(1), short(1), short(1), short(1), short(1),
            ],
        )
        self.assertTrue(result.handled)
        self.assertEqual(self.pet['remaining_points'], 0)
        self.assertEqual(self.pet['base_stats'], [11, 11, 11, 11, 11])
        self.assertEqual(self.saves, 1)
        message_id, fields = decode_frame(result.frames[0])
        self.assertEqual(message_id, 1134)
        self.assertEqual(fields[0].value, 0)
        self.assertEqual(fields[1].value, self.pet_id)
        self.assertEqual(fields[2].value, 15)

    def test_persisted_skill_is_encoded_as_native_action10_record(self):
        self.pet['skill_ids'] = [1]
        result = self.system.handle(
            self.context, 1103, [byte(10), integer(self.pet_id)]
        )
        self.assertTrue(result.handled)
        message_id, fields = decode_frame(result.frames[0])
        self.assertEqual(message_id, 1103)
        self.assertEqual(fields[0].value, 10)
        self.assertEqual(fields[1].value, self.pet_id)
        self.assertEqual(fields[3].value, 1)
        self.assertEqual(len(fields), 4 + 27)
        self.assertEqual((fields[4].type_id, fields[4].value), (TYPE_STRING, '灵宠猛击'))
        self.assertEqual((fields[5].type_id, fields[5].value), (TYPE_INT, 1))

    def test_learning_skill_consumes_exact_book_and_refreshes_skill_list(self):
        self.role['items'].append({
            'id': 777001,
            'template_id': 399010011,
            'quantity': 2,
            'location': 'bag',
        })
        result = self.system.handle(
            self.context,
            1130,
            [byte(50), integer(self.pet_id), integer(399010011), integer(777001)],
        )
        self.assertTrue(result.handled)
        self.assertEqual(self.pet['skill_ids'], [1])
        self.assertEqual(self.role['items'][0]['quantity'], 1)
        self.assertEqual(self.saves, 1)
        self.assertEqual(len(result.frames), 2)
        message_id, fields = decode_frame(result.frames[0])
        self.assertEqual(message_id, 1130)
        self.assertEqual([field.value for field in fields], [50, self.pet_id, 1, 0])
        message_id, fields = decode_frame(result.frames[1])
        self.assertEqual(message_id, 1103)
        self.assertEqual(fields[3].value, 1)

    def test_duplicate_skill_learning_does_not_consume_another_book(self):
        self.pet['skill_ids'] = [1]
        self.role['items'].append({
            'id': 777001,
            'template_id': 399010011,
            'quantity': 2,
            'location': 'bag',
        })
        result = self.system.handle(
            self.context,
            1130,
            [byte(50), integer(self.pet_id), integer(399010011), integer(777001)],
        )
        self.assertTrue(result.handled)
        self.assertEqual(self.role['items'][0]['quantity'], 2)
        self.assertEqual(self.saves, 0)
        self.assertEqual(result.frames, ())


if __name__ == '__main__':
    unittest.main()
