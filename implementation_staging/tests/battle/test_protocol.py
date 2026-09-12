from __future__ import annotations

import unittest

from battle.protocol import (
    battle_action_frame,
    battle_action_show_frame,
    battle_actor_frame,
    battle_defend_frame,
    battle_end_frame,
    battle_escape_frame,
    battle_move_frame,
    battle_reset_frame,
    battle_reward_popup,
    battle_start_frame,
    is_player_escape_command,
)
from battle.state import LocalBattleState
from protocol import decode_frame, field_values


class BattleProtocolTests(unittest.TestCase):
    def test_1040_lifecycle_frames_preserve_verified_types(self):
        reset_id, reset_fields = decode_frame(battle_reset_frame())
        self.assertEqual((reset_id, field_values(reset_fields)), (1040, [0]))
        self.assertEqual([field.type_id for field in reset_fields], [2])

        start_id, start_fields = decode_frame(battle_start_frame())
        self.assertEqual(start_id, 1040)
        self.assertEqual(field_values(start_fields), [1, 1, 0, 30, 0, '', 0, '', 1])
        self.assertEqual(
            [field.type_id for field in start_fields],
            [2, 4, 2, 4, 3, 6, 3, 6, 2],
        )

        state = LocalBattleState(round=3)
        show_id, show_fields = decode_frame(battle_action_show_frame(state))
        self.assertEqual(show_id, 1040)
        self.assertEqual(field_values(show_fields), [2, 3, 0, 0, 0, '', 0, '', 1])
        self.assertEqual(
            [field.type_id for field in show_fields],
            [2, 4, 2, 4, 3, 6, 3, 6, 2],
        )

        end_id, end_fields = decode_frame(battle_end_frame())
        self.assertEqual((end_id, field_values(end_fields)), (1040, [4]))
        self.assertEqual([field.type_id for field in end_fields], [2])

    def test_1041_escape_result_uses_two_ints(self):
        message_id, fields = decode_frame(battle_escape_frame(10003))

        self.assertEqual(message_id, 1041)
        self.assertEqual(field_values(fields), [10, 10003])
        self.assertEqual([field.type_id for field in fields], [4, 4])
        self.assertTrue(is_player_escape_command(6))
        self.assertFalse(is_player_escape_command(10))

    def test_1042_attack_contains_native_hp_delta_effect(self):
        state = LocalBattleState(round=2, player_id=10003, monster_id=700001)

        message_id, fields = decode_frame(battle_action_frame(state, damage=17))

        self.assertEqual(message_id, 1042)
        self.assertEqual(
            field_values(fields),
            [2, 10003, 700001, 1, 1, 0, 0, 0, '普通攻击', 1,
             700001, 0, 22, -17, ''],
        )
        self.assertEqual(
            [field.type_id for field in fields],
            [4, 4, 4, 2, 2, 2, 4, 4, 6, 4, 4, 4, 4, 4, 6],
        )

    def test_1042_defend_and_effect_free_move_keep_existing_layout(self):
        state = LocalBattleState(round=4, player_id=10003, monster_id=700001)

        defend_id, defend_fields = decode_frame(battle_defend_frame(state))
        self.assertEqual(defend_id, 1042)
        self.assertEqual(
            field_values(defend_fields),
            [4, 10003, 10003, 2, 1, 0, 0, 0, '防御', 0],
        )

        move_id, move_fields = decode_frame(battle_move_frame(state))
        self.assertEqual(move_id, 1042)
        self.assertEqual(
            field_values(move_fields),
            [4, 10003, 700001, 1, 0, 0, 0, 0, '', 0],
        )

    def test_1048_actor_layout_is_protocol_only(self):
        message_id, fields = decode_frame(battle_actor_frame(
            actor_id=10003,
            model=6,
            name='本地侠客',
            kind=1,
            side_code=2,
            slot=1,
            weapon_field2=270001,
            current_hp=126,
            max_hp=126,
            appearance={14: 3, 15: 4, 16: 5, 17: 6, 18: 7, 19: 8, 20: 9},
        ))

        values = field_values(fields)
        self.assertEqual(message_id, 1048)
        self.assertEqual(values[0], 60)
        self.assertEqual(values[2], 270001)
        self.assertEqual(values[3], 126)
        self.assertEqual(values[5:10], [2, '本地侠客', 1, 1, 10003])
        self.assertEqual(values[10:12], [126, 126])
        self.assertEqual(values[14:22], [3, 4, 5, 6, 7, 8, 9, 6])
        self.assertEqual(
            [field.type_id for field in fields],
            [4, 4, 4, 4, 4, 4, 6, 3, 4, 4, 4, 4, 4, 4, 4, 3, 4, 4, 4, 4, 4, 3],
        )

    def test_1049_reward_popup_preserves_native_top_overlay(self):
        message_id, fields = decode_frame(battle_reward_popup(
            50,
            {'name': '小还丹', 'quantity_gained': 1},
        ))

        self.assertEqual(message_id, 1049)
        self.assertEqual(field_values(fields), [3, 50, 0, 0, 0, 'x'])
        self.assertEqual([field.type_id for field in fields], [2, 4, 4, 4, 4, 6])


if __name__ == '__main__':
    unittest.main()
