from __future__ import annotations

import unittest
from types import SimpleNamespace

from battle import integration, protocol, resources, state
from protocol import decode_frame, field_values


class BattleIntegrationTests(unittest.TestCase):
    def make_server_module(self):
        def role_items(role):
            return role.setdefault('items', [])

        def bag_item_count(role):
            return len(role_items(role))

        def bag_capacity(role):
            return int(role.get('bag_capacity', 20))

        def apply_one_level(role):
            return False

        return SimpleNamespace(
            role_items=role_items,
            bag_item_count=bag_item_count,
            bag_capacity=bag_capacity,
            apply_one_level=apply_one_level,
            MAX_ROLE_LEVEL=99,
        )

    def test_install_exposes_one_authoritative_state_protocol_and_resource_layer(self):
        server = self.make_server_module()

        integration.install(server)

        self.assertIs(server.LocalBattleState, state.LocalBattleState)
        self.assertIs(server.CombatStats, state.CombatStats)
        self.assertIs(server.battle_reset_frame, protocol.battle_reset_frame)
        self.assertIs(server.battle_resource_frames, resources.battle_resource_frames)
        self.assertIs(server.battle_image_frames, resources.battle_image_frames)
        self.assertEqual(server.BATTLE_RESOURCE_MODEL_OFFSET, resources.BATTLE_RESOURCE_MODEL_OFFSET)

    def test_legacy_round_adapter_uses_engine_then_protocol(self):
        server = self.make_server_module()
        integration.install(server)
        battle = server.LocalBattleState()
        battle.begin(10001, 700001, server.CombatStats(100, 20, 4))

        frames, defeated = server.battle_round_action_frames(
            battle,
            1,
            round_number=1,
            target_id=700001,
        )

        self.assertFalse(defeated)
        self.assertEqual(len(frames), 2)
        player_id, player_fields = decode_frame(frames[0])
        monster_id, monster_fields = decode_frame(frames[1])
        self.assertEqual((player_id, monster_id), (1042, 1042))
        self.assertEqual(field_values(player_fields)[1:4], [10001, 700001, 1])
        self.assertEqual(field_values(player_fields)[12:14], [22, -20])
        self.assertEqual(field_values(monster_fields)[1:4], [700001, 10001, 1])
        self.assertEqual(field_values(monster_fields)[12:14], [22, -8])

    def test_legacy_escape_helpers_use_state_owned_policy(self):
        server = self.make_server_module()
        integration.install(server)
        battle = server.LocalBattleState()
        battle.set_escape_guard(58, 700001, 10001, (12, 28), now=10.0)

        # The compatibility predicate uses real monotonic time; a manually
        # future-stamped guard therefore remains protected.
        self.assertTrue(server.should_suppress_escape_retrigger(
            battle.escape_guard,
            58,
            700001,
        ))
        self.assertTrue(server.update_escape_guard_for_movement(battle, 10, 28))
        self.assertIsNone(battle.escape_guard)


if __name__ == '__main__':
    unittest.main()
