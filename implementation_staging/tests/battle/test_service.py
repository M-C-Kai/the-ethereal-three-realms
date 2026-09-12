from __future__ import annotations

import unittest

from battle.service import battle_round_action_frames
from battle.state import CombatStats, LocalBattleState
from protocol import decode_frame, field_values


class BattleServiceTests(unittest.TestCase):
    def test_round_service_resolves_domain_actions_then_encodes_protocol_frames(self):
        state = LocalBattleState()
        state.begin(10001, 700001, CombatStats(100, 20, 4))

        frames, defeated = battle_round_action_frames(
            state,
            1,
            round_number=1,
            target_id=700001,
        )

        self.assertFalse(defeated)
        self.assertEqual(len(frames), 2)
        first_id, first_fields = decode_frame(frames[0])
        second_id, second_fields = decode_frame(frames[1])
        self.assertEqual((first_id, second_id), (1042, 1042))
        self.assertEqual(field_values(first_fields)[1:4], [10001, 700001, 1])
        self.assertEqual(field_values(first_fields)[12:14], [22, -20])
        self.assertEqual(field_values(second_fields)[1:4], [700001, 10001, 1])
        self.assertEqual(field_values(second_fields)[12:14], [22, -8])


if __name__ == '__main__':
    unittest.main()
