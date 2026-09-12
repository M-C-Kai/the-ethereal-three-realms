from __future__ import annotations

import unittest

from battle.state import CombatStats, LocalBattleState


class BattleStateTests(unittest.TestCase):
    def test_begin_initializes_encounter_and_clears_guard(self):
        state = LocalBattleState(escape_guard={'map_id': 58})

        state.begin(
            10001,
            700001,
            CombatStats(240, 31, 9),
            monster_ids=[700001, 700002],
        )

        self.assertTrue(state.active)
        self.assertEqual(state.monster_ids, (700001, 700002))
        self.assertEqual(
            (state.player_hp, state.player_attack, state.player_defence),
            (240, 31, 9),
        )
        self.assertIsNone(state.escape_guard)

    def test_escape_guard_anchors_contact_tile_and_is_timed(self):
        state = LocalBattleState(
            active=True,
            player_id=10001,
            monster_id=700001,
            map_id=58,
            contact_tile=(12, 28),
            player_tile=(11, 28),
        )

        self.assertTrue(state.escape(now=10.0))

        self.assertFalse(state.active)
        self.assertIsNotNone(state.escape_guard)
        assert state.escape_guard is not None
        self.assertEqual(state.escape_guard['origin'], (12, 28))
        self.assertEqual(state.escape_guard['created_at'], 10.0)
        self.assertTrue(state.should_suppress_retrigger(58, 700001, now=11.9))
        self.assertFalse(state.should_suppress_retrigger(58, 700001, now=12.0))
        self.assertIsNone(state.escape_guard)

    def test_guard_clears_only_after_leaving_one_tile_radius(self):
        state = LocalBattleState()
        state.set_escape_guard(58, 700001, 10001, (12, 28), now=10.0)

        self.assertFalse(state.update_player_tile(11, 28, now=10.1))
        self.assertIsNotNone(state.escape_guard)
        self.assertTrue(state.update_player_tile(10, 28, now=10.2))
        self.assertIsNone(state.escape_guard)

    def test_guard_clears_by_timeout_even_without_leaving_radius(self):
        state = LocalBattleState()
        state.set_escape_guard(58, 700001, 10001, (12, 28), now=10.0)

        self.assertTrue(state.update_player_tile(12, 28, now=12.0))

        self.assertIsNone(state.escape_guard)

    def test_reset_clears_contact_and_escape_context(self):
        state = LocalBattleState(
            active=True,
            monster_defeated=True,
            contact_tile=(12, 28),
            player_tile=(11, 28),
            escape_guard={'map_id': 58},
        )

        state.reset_encounter()

        self.assertFalse(state.active)
        self.assertFalse(state.monster_defeated)
        self.assertIsNone(state.contact_tile)
        self.assertIsNone(state.player_tile)
        self.assertIsNone(state.escape_guard)


if __name__ == '__main__':
    unittest.main()
