from __future__ import annotations

import asyncio
import logging
import unittest
from types import SimpleNamespace

from battle import integration, protocol, resources, state
from protocol import decode_frame, encode_frame, field_values, integer


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

    def make_server_module_with_map(self):
        server = self.make_server_module()
        monster = SimpleNamespace(id=700001, x=12, y=28)
        definition = SimpleNamespace(
            id=58,
            portals=(),
            monsters=(monster,),
        )

        class FakeLocalGameServer:
            delegated = 0

            async def _handle_map_object_interaction(self, **kwargs):
                type(self).delegated += 1

            def __init__(self):
                self.settings = object()
                self.sent = []

            async def _send(self, writer, *frames, cipher=None, lock=None):
                self.sent.append((writer, frames, cipher, lock))

        server.LocalGameServer = FakeLocalGameServer
        server.LOG = logging.getLogger('test-battle-integration')
        server.settings_for_role = lambda settings, role: definition
        server.map_npc_for_object_id = lambda current, object_id: None
        server.map_monster_for_object_id = (
            lambda current, object_id: monster if int(object_id) == monster.id else None
        )
        server.default_role = lambda settings: {
            'id': 10001,
            'map_x': 11,
            'map_y': 28,
        }
        server.combat_stats = lambda role: state.CombatStats(100, 20, 4)
        server.map_object_interaction_ack_frame = lambda object_id: encode_frame(
            1010,
            [integer(int(object_id))],
        )
        server.map_object_remove_frame = lambda object_id: encode_frame(
            1010,
            [integer(int(object_id))],
        )
        server.battle_actor_frames = lambda role, current, trace_id='', state=None: [
            encode_frame(1048, [integer(999)])
        ]
        return server, definition

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
        battle.set_escape_guard(58, 700001, 10001, (12, 28))

        self.assertTrue(server.should_suppress_escape_retrigger(
            battle.escape_guard,
            58,
            700001,
        ))
        self.assertTrue(server.update_escape_guard_for_movement(battle, 10, 28))
        self.assertIsNone(battle.escape_guard)

    def test_monster_interaction_uses_shared_encounter_and_starts_protocol_chain(self):
        server, _definition = self.make_server_module_with_map()
        integration.install(server)
        app = server.LocalGameServer()
        battle = server.LocalBattleState()
        role = {'id': 10001, 'map_x': 11, 'map_y': 28}

        asyncio.run(app._handle_map_object_interaction(
            username='tester',
            active_role=role,
            object_id=700001,
            object_x=12,
            object_y=28,
            action=6,
            source='2031',
            writer='writer',
            cipher=None,
            send_lock='lock',
            battle_state=battle,
            npc_dialogue_state=object(),
        ))

        self.assertTrue(battle.active)
        self.assertEqual(battle.map_id, 58)
        self.assertEqual(battle.player_tile, (11, 28))
        self.assertEqual(battle.contact_tile, (12, 28))
        self.assertEqual(len(app.sent), 1)
        sent_frames = app.sent[0][1]
        self.assertEqual([decode_frame(frame)[0] for frame in sent_frames], [1040, 1048, 1040])
        self.assertEqual(field_values(decode_frame(sent_frames[0])[1]), [0])
        self.assertEqual(field_values(decode_frame(sent_frames[-1])[1])[0], 1)

    def test_q_action_without_tile_keeps_contact_unset_and_player_tile_real(self):
        server, _definition = self.make_server_module_with_map()
        integration.install(server)
        app = server.LocalGameServer()
        battle = server.LocalBattleState()
        role = {'id': 10001, 'map_x': 11, 'map_y': 28}

        asyncio.run(app._handle_map_object_interaction(
            username='tester',
            active_role=role,
            object_id=700001,
            object_x=None,
            object_y=None,
            action=None,
            source='2031',
            writer='writer',
            cipher=None,
            send_lock='lock',
            battle_state=battle,
            npc_dialogue_state=object(),
        ))

        self.assertTrue(battle.active)
        self.assertIsNone(battle.contact_tile)
        self.assertEqual(battle.player_tile, (11, 28))

    def test_non_monster_interaction_still_delegates_to_map_layer(self):
        server, _definition = self.make_server_module_with_map()
        integration.install(server)
        app = server.LocalGameServer()
        battle = server.LocalBattleState()

        asyncio.run(app._handle_map_object_interaction(
            username='tester',
            active_role={'id': 10001, 'map_x': 1, 'map_y': 1},
            object_id=12345,
            object_x=1,
            object_y=1,
            action=0,
            source='2031',
            writer='writer',
            cipher=None,
            send_lock='lock',
            battle_state=battle,
            npc_dialogue_state=object(),
        ))

        self.assertEqual(server.LocalGameServer.delegated, 1)
        self.assertFalse(battle.active)


if __name__ == '__main__':
    unittest.main()
