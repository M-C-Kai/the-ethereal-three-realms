from __future__ import annotations

import unittest

from battle.state import (
    CONTACT_RADIUS_TILES,
    RETRIGGER_TIMEOUT_SECONDS,
    movement_outside_guard_radius,
    should_suppress_guard,
    stamp_guard,
)


class BattleEscapeGuardTests(unittest.TestCase):
    def make_guard(self) -> dict[str, object]:
        return {
            'map_id': 58,
            'monster_id': 700_001,
            'player_id': 10_001,
            'origin': (12, 28),
        }

    def test_policy_constants_match_contact_design(self):
        self.assertEqual(CONTACT_RADIUS_TILES, 1)
        self.assertEqual(RETRIGGER_TIMEOUT_SECONDS, 2.0)

    def test_same_encounter_is_suppressed_before_two_seconds(self):
        guard = self.make_guard()
        stamp_guard(guard, now=100.0)

        self.assertTrue(should_suppress_guard(guard, 58, 700_001, now=101.999))

    def test_same_encounter_is_released_at_two_seconds(self):
        guard = self.make_guard()
        stamp_guard(guard, now=100.0)

        self.assertFalse(should_suppress_guard(guard, 58, 700_001, now=102.0))

    def test_other_monster_is_not_suppressed(self):
        guard = self.make_guard()
        stamp_guard(guard, now=100.0)

        self.assertFalse(should_suppress_guard(guard, 58, 700_002, now=100.1))

    def test_one_tile_from_contact_origin_remains_guarded(self):
        guard = self.make_guard()

        self.assertFalse(movement_outside_guard_radius(guard, 11, 28))

    def test_more_than_one_tile_from_contact_origin_releases_guard(self):
        guard = self.make_guard()

        self.assertTrue(movement_outside_guard_radius(guard, 10, 28))


if __name__ == '__main__':
    unittest.main()
