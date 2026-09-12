from __future__ import annotations

import unittest

from battle.encounter import EncounterRequest, request_encounter, update_player_tile
from battle.state import CombatStats, LocalBattleState


class BattleEncounterTests(unittest.TestCase):
    def request(self, source: str = 'map_interaction') -> EncounterRequest:
        return EncounterRequest(
            map_id=58,
            monster_id=700001,
            player_id=10001,
            player_tile=(11, 28),
            monster_tile=(12, 28),
            source=source,
        )

    def test_all_confirmed_entry_sources_share_one_admission_path(self):
        for source in ('map_interaction', 'q_action', 'proximity'):
            with self.subTest(source=source):
                state = LocalBattleState()
                decision = request_encounter(
                    state,
                    self.request(source),
                    player_stats=CombatStats(180, 25, 7),
                )
                self.assertTrue(decision.start)
                self.assertFalse(decision.suppressed)
                self.assertEqual(decision.reason, 'started')
                self.assertTrue(state.active)
                self.assertEqual(state.map_id, 58)
                self.assertEqual(state.contact_tile, (12, 28))
                self.assertEqual(state.player_tile, (11, 28))
                self.assertEqual(state.player_hp, 180)

    def test_active_battle_cannot_be_reopened(self):
        state = LocalBattleState(active=True)

        decision = request_encounter(state, self.request())

        self.assertFalse(decision.start)
        self.assertTrue(decision.suppressed)
        self.assertEqual(decision.reason, 'battle_active')

    def test_defeated_same_monster_cannot_reopen_before_map_reset(self):
        state = LocalBattleState(monster_id=700001, monster_defeated=True)

        decision = request_encounter(state, self.request())

        self.assertFalse(decision.start)
        self.assertEqual(decision.reason, 'monster_defeated')

    def test_escape_guard_suppresses_before_timeout(self):
        state = LocalBattleState()
        state.set_escape_guard(58, 700001, 10001, (12, 28), now=10.0)

        decision = request_encounter(state, self.request(), now=11.9)

        self.assertFalse(decision.start)
        self.assertEqual(decision.reason, 'escape_guard')

    def test_escape_guard_releases_after_two_seconds(self):
        state = LocalBattleState()
        state.set_escape_guard(58, 700001, 10001, (12, 28), now=10.0)

        decision = request_encounter(state, self.request(), now=12.0)

        self.assertTrue(decision.start)
        self.assertIsNone(state.escape_guard)

    def test_leaving_one_tile_radius_releases_guard_before_timeout(self):
        state = LocalBattleState()
        state.set_escape_guard(58, 700001, 10001, (12, 28), now=10.0)

        self.assertTrue(update_player_tile(state, 10, 28, now=10.1))
        decision = request_encounter(state, self.request(), now=10.2)

        self.assertTrue(decision.start)

    def test_invalid_source_is_rejected_instead_of_silently_creating_new_path(self):
        state = LocalBattleState()
        bad = EncounterRequest(58, 700001, 10001, None, None, 'invented')

        with self.assertRaises(ValueError):
            request_encounter(state, bad)


if __name__ == '__main__':
    unittest.main()
