from __future__ import annotations

import inspect
import unittest

from battle import encounter, protocol, resources, rewards, service, state
import server


class BattleServerIntegrationTests(unittest.TestCase):
    def test_server_exports_authoritative_battle_objects_directly(self):
        self.assertIs(server.LocalBattleState, state.LocalBattleState)
        self.assertIs(server.CombatStats, state.CombatStats)
        self.assertIs(server.should_suppress_escape_retrigger, state.should_suppress_guard)
        self.assertIs(server.update_escape_guard_for_movement, encounter.update_player_tile)
        self.assertIs(server.battle_command_target_id, __import__('battle.engine', fromlist=['battle_command_target_id']).battle_command_target_id)
        self.assertIs(server.battle_round_action_frames, service.battle_round_action_frames)
        self.assertIs(server.battle_reset_frame, protocol.battle_reset_frame)
        self.assertIs(server.battle_actor_frame, protocol.battle_actor_frame)
        self.assertIs(server.battle_escape_frame, protocol.battle_escape_frame)
        self.assertIs(server.battle_resource_frames, resources.battle_resource_frames)
        self.assertIs(server.battle_image_frames, resources.battle_image_frames)
        self.assertEqual(server.BATTLE_EXP_REWARD, rewards.BATTLE_EXP_REWARD)
        self.assertEqual(server.BATTLE_DROP_TEMPLATE_ID, rewards.BATTLE_DROP_TEMPLATE_ID)

    def test_server_map_handler_calls_shared_encounter_entry(self):
        source = inspect.getsource(server.LocalGameServer._handle_map_object_interaction)
        self.assertIn('request_encounter(', source)
        self.assertIn('EncounterRequest(', source)
        self.assertNotIn('battle_state.begin(', source)


if __name__ == '__main__':
    unittest.main()
