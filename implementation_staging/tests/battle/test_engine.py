from __future__ import annotations

import unittest

from battle.engine import battle_command_target_id, resolve_round
from battle.state import CombatStats, LocalBattleState


class BattleEngineTests(unittest.TestCase):
    def make_state(self) -> LocalBattleState:
        state = LocalBattleState()
        state.begin(
            10001,
            700001,
            CombatStats(100, 20, 4),
            monster_ids=[700001, 700002],
        )
        return state

    def test_target_parser_accepts_only_living_encounter_monsters(self):
        state = self.make_state()

        self.assertEqual(
            battle_command_target_id([1, 1, 10001, 1, 700002], state),
            700002,
        )
        self.assertIsNone(
            battle_command_target_id([1, 1, 10001, 1, 799999], state)
        )
        state.monster_hp_by_id[700002] = 0
        self.assertIsNone(
            battle_command_target_id([1, 1, 10001, 1, 700002], state)
        )

    def test_basic_attack_mutates_hp_and_returns_domain_actions(self):
        state = self.make_state()

        result = resolve_round(state, 1, target_id=700002)

        self.assertTrue(result.accepted)
        self.assertFalse(result.monster_defeated)
        self.assertEqual(state.monster_hp_for(700002), 80)
        # Existing formula: max(1, monster_attack - player_defence // 2)
        # = 10 - 4 // 2 = 8.
        self.assertEqual(state.player_hp, 92)
        self.assertEqual(len(result.actions), 2)
        self.assertEqual(
            (result.actions[0].kind, result.actions[0].actor_id, result.actions[0].target_id, result.actions[0].damage),
            ('attack', 10001, 700002, 20),
        )
        self.assertEqual(
            (result.actions[1].kind, result.actions[1].actor_id, result.actions[1].target_id, result.actions[1].damage),
            ('attack', 700002, 10001, 8),
        )

    def test_defend_halves_monster_damage_without_inventing_player_damage(self):
        state = self.make_state()

        result = resolve_round(state, 2)

        self.assertTrue(result.accepted)
        # Base damage 8, defending halves to 4.
        self.assertEqual(state.player_hp, 96)
        self.assertEqual(result.actions[0].kind, 'defend')
        self.assertEqual(result.actions[0].damage, 0)
        self.assertEqual(result.actions[1].damage, 4)

    def test_killing_last_monster_prevents_counterattack(self):
        state = LocalBattleState()
        state.begin(10001, 700001, CombatStats(100, 150, 0))

        result = resolve_round(state, 1, target_id=700001)

        self.assertTrue(result.monster_defeated)
        self.assertEqual(state.monster_hp_for(700001), 0)
        self.assertEqual(state.player_hp, 100)
        self.assertEqual(len(result.actions), 1)

    def test_invalid_command_and_target_do_not_mutate_state(self):
        state = self.make_state()
        before_hp = state.player_hp
        before_monsters = dict(state.monster_hp_by_id)

        bad_command = resolve_round(state, 99)
        bad_target = resolve_round(state, 1, target_id=799999)

        self.assertFalse(bad_command.accepted)
        self.assertFalse(bad_target.accepted)
        self.assertEqual(state.player_hp, before_hp)
        self.assertEqual(state.monster_hp_by_id, before_monsters)


if __name__ == '__main__':
    unittest.main()
