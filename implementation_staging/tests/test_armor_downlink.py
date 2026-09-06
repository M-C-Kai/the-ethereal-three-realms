import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from item_registry import armor_resource_preview_template_mapping
from server import BASE_CHARACTER_APPEARANCE, Settings, character_appearance, default_role, role_items


class ArmorDownlinkTests(unittest.TestCase):
    def _role_with_property2_equipped(self, property2: int):
        settings = Settings()
        role = default_role(settings)
        target_template = next(
            template_id for template_id, value in armor_resource_preview_template_mapping().items()
            if value == property2
        )
        armor = None
        for item in role_items(role):
            item['location'] = 'bag'
            if int(item.get('template_id', 0)) == target_template:
                armor = item
        self.assertIsNotNone(armor)
        armor['location'] = 'equipped'
        return settings, role, armor

    def test_base_snapshot_clears_legacy_property15(self):
        self.assertEqual(BASE_CHARACTER_APPEARANCE[2], 0)
        self.assertEqual(BASE_CHARACTER_APPEARANCE[15], 0)

    def test_resource_preview_armor_downlinks_exact_property2(self):
        settings, role, _ = self._role_with_property2_equipped(12)
        appearance = character_appearance(role, settings.item_registry)
        self.assertEqual(appearance[2], 12)
        self.assertEqual(appearance[15], 0)

    def test_stale_template_property15_cannot_override_resource_mapping(self):
        settings, role, _ = self._role_with_property2_equipped(7)
        real_resolve = settings.item_registry.resolve

        def stale_resolve(item):
            resolved = real_resolve(item)
            if int(resolved.get('equipment_slot', 0)) == 3:
                resolved['appearance_properties'] = {'15': 34, '2': 30}
            return resolved

        with patch.object(settings.item_registry, 'resolve', side_effect=stale_resolve):
            appearance = character_appearance(role, settings.item_registry)
        self.assertEqual(appearance[2], 7)
        self.assertEqual(appearance[15], 0)


if __name__ == '__main__':
    unittest.main()
