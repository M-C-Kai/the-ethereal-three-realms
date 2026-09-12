import copy
import unittest

from pet_model import ensure_pet_schema
from pet_registry import default_pet_registry
from pet_service import allocate_stats, recalculate_pet_properties, release_pet, rename_pet


class PetServiceTests(unittest.TestCase):
    def setUp(self):
        self.registry = default_pet_registry()
        self.role = {'id': 10001}
        ensure_pet_schema(self.role, self.registry)
        self.pet = self.role['pets'][0]

    def test_rename_owned_bag_pet(self):
        result = rename_pet(self.role, self.pet['id'], '灵狐')
        self.assertTrue(result.changed)
        self.assertEqual(self.pet['name'], '灵狐')
        self.assertEqual(result.name, '灵狐')

    def test_rename_rejects_invalid_name_without_mutation(self):
        before = copy.deepcopy(self.role)
        result = rename_pet(self.role, self.pet['id'], '')
        self.assertFalse(result.changed)
        self.assertEqual(result.reason, 'empty_name')
        self.assertEqual(self.role, before)

    def test_release_removes_pet_and_reports_previous_states(self):
        self.pet['deployed'] = True
        self.pet['walking'] = True
        pet_id = self.pet['id']
        result = release_pet(self.role, pet_id)
        self.assertTrue(result.changed)
        self.assertTrue(result.was_deployed)
        self.assertTrue(result.was_walking)
        self.assertEqual(self.role['pets'], [])

    def test_release_rejects_storage_pet_without_mutation(self):
        self.pet['location'] = 'storage'
        before = copy.deepcopy(self.role)
        result = release_pet(self.role, self.pet['id'])
        self.assertFalse(result.changed)
        self.assertEqual(self.role, before)

    def test_allocate_stats_spends_points_and_returns_32_through_46_updates(self):
        self.pet['remaining_points'] = 5
        result = allocate_stats(self.role, self.pet['id'], (1, 1, 1, 1, 1), self.registry)
        self.assertTrue(result.changed)
        self.assertEqual(self.pet['remaining_points'], 0)
        self.assertEqual([property_id for property_id, _ in result.updates], list(range(32, 47)))

    def test_allocate_stats_rejects_overspend_without_mutation(self):
        self.pet['remaining_points'] = 1
        before = copy.deepcopy(self.role)
        result = allocate_stats(self.role, self.pet['id'], (1, 1, 0, 0, 0), self.registry)
        self.assertFalse(result.changed)
        self.assertEqual(result.reason, 'insufficient_points')
        self.assertEqual(self.role, before)

    def test_recalculate_properties_is_deterministic(self):
        first = recalculate_pet_properties(self.pet, self.registry)
        second = recalculate_pet_properties(self.pet, self.registry)
        self.assertEqual(first, second)
        self.assertEqual(sorted(first), list(range(38, 47)))


if __name__ == '__main__':
    unittest.main()
