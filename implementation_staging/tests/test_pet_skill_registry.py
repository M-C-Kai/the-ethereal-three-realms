import unittest

from pet_skill_registry import default_pet_skill_registry


class PetSkillRegistryTests(unittest.TestCase):
    def test_starter_skill_maps_to_native_skill_book_range(self):
        registry = default_pet_skill_registry()
        skill = registry.require(1)
        self.assertEqual(skill.name, '灵宠猛击')
        self.assertEqual(skill.book_template_id, 399010011)
        self.assertIs(registry.for_book(399010011), skill)
        self.assertIsNone(registry.for_book(399010010))


if __name__ == '__main__':
    unittest.main()
