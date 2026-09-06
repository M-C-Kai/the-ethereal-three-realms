import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from server import (
    BASE_CHARACTER_APPEARANCE,
    Settings,
    character_appearance,
    default_role,
    role_items,
)


class ArmorDownlinkTests(unittest.TestCase):
    def _role_with_only_armor_equipped(self):
        settings = Settings()
        role = default_role(settings)
        armor = None
        for item in role_items(role):
            item["location"] = "bag"
            resolved = settings.item_registry.resolve(item)
            if int(resolved.get("equipment_slot", 0)) == 3:
                armor = item
        self.assertIsNotNone(armor)
        armor["location"] = "equipped"
        return settings, role, armor

    def test_base_snapshot_explicitly_clears_legacy_property15_and_has_property2(self):
        self.assertIn(2, BASE_CHARACTER_APPEARANCE)
        self.assertEqual(BASE_CHARACTER_APPEARANCE[2], 0)
        self.assertEqual(BASE_CHARACTER_APPEARANCE[15], 0)
        settings, role, _ = self._role_with_only_armor_equipped()
        appearance = character_appearance(role, settings.item_registry)
        self.assertEqual(appearance[2], 0)
        self.assertEqual(appearance[15], 0)

    def test_confirmed_catalog_value_is_downlinked_as_property2(self):
        settings, role, _ = self._role_with_only_armor_equipped()
        with patch("server.armor_property2_from_icon", return_value=12):
            appearance = character_appearance(role, settings.item_registry)
        self.assertEqual(appearance[2], 12)
        self.assertEqual(appearance[15], 0)

    def test_stale_armor_template_property15_cannot_reappear(self):
        settings, role, _ = self._role_with_only_armor_equipped()
        real_resolve = settings.item_registry.resolve

        def stale_resolve(item):
            resolved = real_resolve(item)
            if int(resolved.get("equipment_slot", 0)) == 3:
                resolved["appearance_properties"] = {"15": 34, "2": 30}
            return resolved

        with patch.object(settings.item_registry, "resolve", side_effect=stale_resolve):
            with patch("server.armor_property2_from_icon", return_value=7):
                appearance = character_appearance(role, settings.item_registry)
        self.assertEqual(appearance[2], 7)
        self.assertEqual(appearance[15], 0)


if __name__ == "__main__":
    unittest.main()
