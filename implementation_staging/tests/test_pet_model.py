import unittest

from pet_model import allocate_pet_id, ensure_pet_schema
from pet_registry import default_pet_registry


class PetModelTests(unittest.TestCase):
    def test_existing_pet_migrates_without_duplication(self):
        role = {
            'id': 10001,
            'pets_initialized': True,
            'pets': [{'id': 10001001, 'template_id': 50100, 'name': '测试灵宠'}],
        }
        changed = ensure_pet_schema(role, default_pet_registry())
        self.assertTrue(changed)
        self.assertEqual(len(role['pets']), 1)
        pet = role['pets'][0]
        self.assertEqual(pet['location'], 'bag')
        self.assertEqual(pet['skill_ids'], [])
        self.assertIn('hp', pet)
        self.assertIn('mp', pet)
        self.assertFalse(pet['bound'])
        self.assertFalse(pet['trade_locked'])
        self.assertFalse(ensure_pet_schema(role, default_pet_registry()))

    def test_allocate_pet_id_does_not_collide(self):
        role = {'id': 10001, 'pets': [{'id': 10001001}, {'id': 10001003}]}
        self.assertEqual(allocate_pet_id(role), 10001004)


if __name__ == '__main__':
    unittest.main()
