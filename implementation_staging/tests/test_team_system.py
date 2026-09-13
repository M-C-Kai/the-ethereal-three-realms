"""The team router owns every 1023 action and keeps both clients in sync."""
from __future__ import annotations

import unittest

from app.context import SystemContext
from protocol import decode_frame, integer, short
from systems.map.protocol import player_actor_object_id
from systems.role.service import default_role

import server


class TeamSystemTests(unittest.TestCase):
    def setUp(self):
        self.settings = server.Settings.load(server.Path(__file__).resolve().parent.parent / 'config.json')
        self.alice = default_role(self.settings)
        self.bob = default_role(self.settings)
        self.alice.update(id=10001, name='甲')
        self.bob.update(id=10002, name='乙')
        self.roles = {10001: self.alice, 10002: self.bob}
        self.online = {10001, 10002}
        self.pushed = {10001: [], 10002: []}
        from systems.team.handler import TeamSystem
        self.team = TeamSystem(
            self.settings,
            find_role=self.roles.get,
            online_role_ids=lambda: set(self.online),
            push_to_role=lambda role_id, frames: self.pushed[role_id].extend(frames),
            can_follow=lambda leader_id, member_id: True,
        )

    def send(self, role, action, peer=None):
        fields = [short(action)]
        if peer is not None:
            fields.append(integer(peer))
        return self.team.handle(SystemContext(str(role['name']), role, {}), 1023, fields)

    def decoded(self, role_id):
        return [decode_frame(frame) for frame in self.pushed[role_id]]

    def test_invite_accept_syncs_both_rosters_without_map_ui_frames(self):
        created = self.send(self.alice, 0, 10001)
        from systems.role.protocol import role_property_fields
        props = role_property_fields(self.settings, self.alice)
        roster = [fields for mid, fields in (decode_frame(frame) for frame in created.frames)
                  if mid == 1026][0]
        self.assertEqual([field.value for field in roster[4:6]],
                         [props[40].value, props[41].value])
        self.assertEqual([field.value for field in roster[8:10]],
                         [props[42].value, props[43].value])
        self.send(self.alice, 2, player_actor_object_id(10002))
        self.pushed = {10001: [], 10002: []}
        self.send(self.bob, 3, 10001)
        self.assertEqual(self.team.registry.team_of(10002).members, [10001, 10002])
        for role_id, peer_id in ((10001, 10002), (10002, 10001)):
            frames = self.decoded(role_id)
            self.assertFalse(any(message_id == 1023 and fields[0].value == 6
                                 for message_id, fields in frames))
            self.assertTrue(any(message_id == 1026 and int(fields[3].value) == peer_id
                                for message_id, fields in frames))
        member_ids = [message_id for message_id, _ in self.decoded(10002)]
        self.assertEqual(member_ids.count(1028), 1)
        self.assertLess(max(i for i, message_id in enumerate(member_ids) if message_id == 1026),
                        member_ids.index(1028))

    def test_disband_and_disconnect_release_membership(self):
        self.send(self.alice, 0, 10001)
        self.send(self.alice, 2, player_actor_object_id(10002))
        self.send(self.bob, 3, 10001)
        self.team.on_disconnect(10002)
        self.assertIsNone(self.team.registry.team_of(10002))
        self.send(self.alice, 11)
        self.assertIsNone(self.team.registry.team_of(10001))

    def test_member_leave_updates_server_and_both_clients(self):
        self.send(self.alice, 0, 10001)
        self.send(self.alice, 2, player_actor_object_id(10002))
        self.send(self.bob, 3, 10001)
        self.pushed = {10001: [], 10002: []}
        self.send(self.bob, 1, 10002)
        self.assertIsNone(self.team.registry.team_of(10002))
        self.assertEqual(self.team.registry.team_of(10001).members, [10001])
        self.assertTrue(any(message_id == 1023 and fields[0].value == 1
                            for message_id, fields in self.decoded(10001)))

    def test_leader_kick_updates_own_roster_and_target(self):
        self.send(self.alice, 0, 10001)
        self.send(self.alice, 2, player_actor_object_id(10002))
        self.send(self.bob, 3, 10001)
        self.pushed = {10001: [], 10002: []}
        result = self.send(self.alice, 1, 10002)
        self.assertIsNone(self.team.registry.team_of(10002))
        self.assertEqual(self.team.registry.team_of(10001).members, [10001])
        self.assertTrue(any(mid == 1023 and fields[0].value == 1 and fields[1].value == 10002
                            for mid, fields in (decode_frame(frame) for frame in result.frames)))
        self.assertTrue(any(mid == 1023 and fields[0].value == 11
                            for mid, fields in self.decoded(10002)))

    def test_follow_movement_uses_chain_only_for_active_member(self):
        self.send(self.alice, 0, 10001)
        self.send(self.alice, 2, player_actor_object_id(10002))
        self.send(self.bob, 3, 10001)
        frame = self.team.follow_movement_frame(10001, 10002, 30, 35)
        message_id, fields = decode_frame(frame)
        self.assertEqual(message_id, 1028)
        self.assertEqual([int(field.value) for field in fields],
                         [player_actor_object_id(10001), 0, 0, 30, 35, 1, 10002])
        self.send(self.bob, 18)
        self.assertIsNone(self.team.follow_movement_frame(10001, 10002, 31, 35))
        self.assertIsNone(self.team.follow_movement_frame(10002, 10001, 31, 35))

    def test_router_has_single_team_owner(self):
        game = server.LocalGameServer(self.settings)
        self.assertEqual(
            sum(1 for route in game.system_router.routes
                if route.predicate(SystemContext('甲', self.alice, {}), 1023, [short(2), integer(10002)])),
            1,
        )
