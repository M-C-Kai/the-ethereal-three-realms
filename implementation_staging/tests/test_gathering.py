"""APK-confirmed map gathering protocol tests (1141 catalog, 2027 flow, 1145 pathfind).

Wire shapes per docs/protocol/life-skills.md. The real gather protocol is
2027 (0x7EB) with the 1141 (0x475) target catalog; 1145 (0x479) is the
cross-map auto-pathfinding request. Durations/costs are local-compat data.
"""
import asyncio
import copy
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from protocol import (  # noqa: E402
    TYPE_BYTE,
    TYPE_INT,
    TYPE_STRING,
    byte,
    decode_frame,
    encode_frame,
    field_values,
    integer,
    string,
)
import server as server_module  # noqa: E402
from server import (  # noqa: E402
    ConnectionGathering,
    LocalGameServer,
    Settings,
    default_role,
    ensure_life_skills,
    gather_catalog_frame,
    gather_interrupt_frame,
    gather_remove_frame,
    gather_spawn_frame,
    gather_start_frame,
    gather_start_check,
    is_gather_start_request,
    is_map_pathfind_request,
    map_pathfind_frame,
    role_items,
)
from life_skill_service import gathering_reward_result  # noqa: E402

HERB_TARGET_ID = 6001
HERB_SKILL_ID = 2001


def _ids(fields):
    return [field.type_id for field in fields]


def _learned_herbalism(role):
    ensure_life_skills(role)
    role['life_skills']['skills'][str(HERB_SKILL_ID)] = {'level': 1, 'proficiency': 0}


class GatheringGuardTests(unittest.TestCase):
    def test_gather_start_request_is_byte_int(self):
        fields = decode_frame(encode_frame(2027, [byte(1), integer(6001)]))[1]
        self.assertTrue(is_gather_start_request(fields))
        for bad in ([integer(1), integer(6001)], [byte(1), byte(6001)], [byte(1)]):
            fields = decode_frame(encode_frame(2027, bad))[1]
            self.assertFalse(is_gather_start_request(fields), bad)

    def test_map_pathfind_request_is_byte_int_byte_byte(self):
        fields = decode_frame(encode_frame(1145, [byte(0), integer(58), byte(12), byte(8)]))[1]
        self.assertTrue(is_map_pathfind_request(fields))
        for bad in (
            [byte(0), integer(58), integer(12), byte(8)],
            [integer(0), integer(58), byte(12), byte(8)],
        ):
            fields = decode_frame(encode_frame(1145, bad))[1]
            self.assertFalse(is_map_pathfind_request(fields), bad)


class GatheringFrameTests(unittest.TestCase):
    def setUp(self):
        self.settings = Settings()
        self.target = self.settings.life_registry.gather_target(HERB_TARGET_ID)

    def test_catalog_frame_has_no_action_byte_and_nine_field_records(self):
        targets = self.settings.life_registry.gather_targets
        message_id, fields = decode_frame(gather_catalog_frame(targets))
        self.assertEqual(message_id, 1141)
        values = field_values(fields)
        self.assertEqual(values[0], len(targets))
        size = len(values)
        count = values[0]
        self.assertEqual((size - 1) % count, 0)
        width = (size - 1) // count
        self.assertEqual(width, 9)
        first = values[1:1 + width]
        self.assertEqual(first[0], targets[0].target_id)
        self.assertEqual(first[1], targets[0].name)
        self.assertEqual(first[3], targets[0].x)
        self.assertEqual(first[7], targets[0].map_id)

    def test_spawn_frame_layout_with_menu_label_at_field_nine(self):
        message_id, fields = decode_frame(gather_spawn_frame(self.target))
        self.assertEqual(message_id, 2027)
        values = field_values(fields)
        self.assertEqual(_ids(fields), [
            TYPE_BYTE, TYPE_INT, TYPE_INT, TYPE_INT, TYPE_INT,
            TYPE_STRING, TYPE_INT, TYPE_INT, TYPE_INT, TYPE_STRING,
        ])
        self.assertEqual(values[0], 0)
        self.assertEqual(values[1], self.target.target_id)
        self.assertEqual(values[2], self.target.x)
        self.assertEqual(values[3], self.target.y)
        self.assertEqual(values[4], self.target.model_id)
        self.assertEqual(values[5], self.target.name)
        self.assertEqual(values[9], '采集')

    def test_start_interrupt_remove_frames(self):
        message_id, fields = decode_frame(gather_start_frame(3, HERB_TARGET_ID))
        self.assertEqual(message_id, 2027)
        self.assertEqual(_ids(fields), [TYPE_BYTE, TYPE_INT, TYPE_INT])
        self.assertEqual(field_values(fields), [1, 3, HERB_TARGET_ID])

        message_id, fields = decode_frame(gather_interrupt_frame())
        self.assertEqual((message_id, field_values(fields)), (2027, [2]))

        message_id, fields = decode_frame(gather_remove_frame(HERB_TARGET_ID))
        self.assertEqual(message_id, 2027)
        self.assertEqual(field_values(fields), [3, HERB_TARGET_ID])

    def test_pathfind_frame_single_hop(self):
        message_id, fields = decode_frame(map_pathfind_frame(58, 12, 8))
        self.assertEqual(message_id, 1145)
        self.assertEqual(field_values(fields), [0, 1, 58, 12, 8, 0])


class GatheringStartCheckTests(unittest.TestCase):
    def setUp(self):
        self.settings = Settings()
        self.registry = self.settings.life_registry
        self.target = self.registry.gather_target(HERB_TARGET_ID)
        self.role = default_role(self.settings)

    def test_ok_when_skill_and_stamina_available(self):
        _learned_herbalism(self.role)
        self.assertEqual(gather_start_check(self.role, self.target, False, self.registry), '')

    def test_rejected_without_skill(self):
        ensure_life_skills(self.role)
        self.assertNotEqual(gather_start_check(self.role, self.target, False, self.registry), '')

    def test_rejected_when_skill_level_too_low(self):
        _learned_herbalism(self.role)
        self.role['life_skills']['skills'][str(HERB_SKILL_ID)]['level'] = 0
        self.assertNotEqual(gather_start_check(self.role, self.target, False, self.registry), '')

    def test_rejected_when_stamina_insufficient(self):
        _learned_herbalism(self.role)
        self.role['life_skills']['stamina'] = self.target.stamina_cost - 1
        self.assertNotEqual(gather_start_check(self.role, self.target, False, self.registry), '')

    def test_rejected_when_already_gathering(self):
        _learned_herbalism(self.role)
        self.assertNotEqual(gather_start_check(self.role, self.target, True, self.registry), '')


class GatheringRewardTests(unittest.TestCase):
    def setUp(self):
        self.settings = Settings()
        self.registry = self.settings.life_registry
        self.target = self.registry.gather_target(HERB_TARGET_ID)
        self.role = default_role(self.settings)
        _learned_herbalism(self.role)

    def test_reward_grants_item_deducts_stamina_and_adds_proficiency(self):
        result = gathering_reward_result(
            self.role, self.target, self.registry, self.settings.item_registry,
        )
        self.assertTrue(result.changed)
        self.assertEqual(self.role['life_skills']['stamina'], 100 - self.target.stamina_cost)
        state = self.role['life_skills']['skills'][str(HERB_SKILL_ID)]
        self.assertEqual(state['proficiency'], self.target.proficiency_gain)
        reward = next(
            i for i in role_items(self.role)
            if i.get('template_id') == self.target.reward_template_id
        )
        self.assertEqual(reward['quantity'], 10 + self.target.reward_quantity)
        frame_ids = [decode_frame(f)[0] for f in result.frames]
        self.assertEqual(frame_ids[0], 1008)
        self.assertIn(1017, frame_ids)
        self.assertIn(1132, frame_ids)
        remove_id, remove_fields = decode_frame(result.frames[-1])
        self.assertEqual((remove_id, field_values(remove_fields)), (2027, [3, HERB_TARGET_ID]))

    def test_reward_rolls_back_when_save_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            settings = Settings(role_data_file=str(Path(directory) / 'roles.json'))
            server = LocalGameServer(settings)
            role = server.roles.roles_for('gather-roll')[0]
            _learned_herbalism(role)
            before = copy.deepcopy(role)
            with mock.patch.object(server.roles, 'save', side_effect=OSError('disk full')):
                with self.assertRaises(OSError):
                    server.handle_gather_completion(role, self.target)
            self.assertEqual(role, before)


class ConnectionGatheringTests(unittest.TestCase):
    def setUp(self):
        self.settings = Settings()
        self.registry = self.settings.life_registry
        self.target = self.registry.gather_target(HERB_TARGET_ID)
        self.role = default_role(self.settings)
        _learned_herbalism(self.role)
        self.gathering = ConnectionGathering()

    def test_start_creates_session_and_ack_frames(self):
        frames, session = self.gathering.start(self.role, self.target, 58)
        self.assertIsNotNone(session)
        self.assertEqual(session['target_id'], HERB_TARGET_ID)
        self.assertEqual(session['map_id'], 58)
        ack_id, ack_fields = decode_frame(frames[0])
        self.assertEqual((ack_id, field_values(ack_fields)), (2027, [1, self.target.duration_seconds, HERB_TARGET_ID]))

    def test_only_one_active_gather(self):
        frames, session = self.gathering.start(self.role, self.target, 58)
        self.assertIsNotNone(session)
        frames2, session2 = self.gathering.start(self.role, self.target, 58)
        self.assertIsNone(session2)

    def test_cancel_invalidates_session_and_returns_interrupt_frame(self):
        self.gathering.start(self.role, self.target, 58)
        interrupt = self.gathering.cancel()
        self.assertIsNotNone(interrupt)
        message_id, fields = decode_frame(interrupt)
        self.assertEqual((message_id, field_values(fields)), (2027, [2]))
        self.assertIsNone(self.gathering.session)
        # second cancel: nothing active
        self.assertIsNone(self.gathering.cancel())

    def test_stale_session_cannot_complete(self):
        frames, session = self.gathering.start(self.role, self.target, 58)
        self.assertTrue(self.gathering.is_current(session))
        self.gathering.cancel()
        self.assertFalse(self.gathering.is_current(session))

    def test_new_gather_invalidates_previous_token(self):
        _, first = self.gathering.start(self.role, self.target, 58)
        self.gathering.cancel()
        _, second = self.gathering.start(self.role, self.target, 58)
        self.assertFalse(self.gathering.is_current(first))
        self.assertTrue(self.gathering.is_current(second))
        self.assertNotEqual(first['token'], second['token'])

    def test_consume_is_one_shot(self):
        _, session = self.gathering.start(self.role, self.target, 58)
        self.assertTrue(self.gathering.consume(session))
        self.assertFalse(self.gathering.is_current(session))
        self.assertFalse(self.gathering.consume(session))


class FakeWriter:
    def __init__(self):
        self.frames = []

    def write(self, data):
        self.frames.append(data)

    async def drain(self):
        return None


class GatheringAsyncTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.settings = Settings()
        self.registry = self.settings.life_registry
        self.target = self.registry.gather_target(HERB_TARGET_ID)

    def _role(self):
        role = default_role(self.settings)
        _learned_herbalism(role)
        return role

    async def test_completion_task_sends_reward_exactly_once(self):
        with tempfile.TemporaryDirectory() as directory:
            settings = Settings(role_data_file=str(Path(directory) / 'roles.json'))
            server = LocalGameServer(settings)
            role = server.roles.roles_for('gather-live')[0]
            _learned_herbalism(role)
            gathering = ConnectionGathering()
            frames, session = gathering.start(role, self.target, 58)
            writer = FakeWriter()
            await server._finish_gathering_later(
                writer, None, None,
                username='gather-live',
                active_role=role,
                gathering=gathering,
                session=session,
                target=self.target,
                delay=0.0,
            )
            self.assertEqual(len(writer.frames), 4)
            self.assertEqual(
                self.role_quantity(role, HERB_REWARD := self.target.reward_template_id),
                10 + self.target.reward_quantity,
            )
            # a repeated/stale completion attempt must not reward again
            await server._finish_gathering_later(
                writer, None, None,
                username='gather-live',
                active_role=role,
                gathering=gathering,
                session=session,
                target=self.target,
                delay=0.0,
            )
            self.assertEqual(len(writer.frames), 4)

    async def test_cancelled_session_task_sends_nothing(self):
        with tempfile.TemporaryDirectory() as directory:
            settings = Settings(role_data_file=str(Path(directory) / 'roles.json'))
            server = LocalGameServer(settings)
            role = server.roles.roles_for('gather-cancel')[0]
            _learned_herbalism(role)
            gathering = ConnectionGathering()
            _, session = gathering.start(role, self.target, 58)
            writer = FakeWriter()
            gathering.cancel()
            await server._finish_gathering_later(
                writer, None, None,
                username='gather-cancel',
                active_role=role,
                gathering=gathering,
                session=session,
                target=self.target,
                delay=0.0,
            )
            self.assertEqual(writer.frames, [])
            self.assertEqual(self.role_quantity(role, self.target.reward_template_id), 10)

    @staticmethod
    def role_quantity(role, template_id):
        return sum(
            int(item['quantity']) for item in role_items(role)
            if item.get('template_id') == template_id
        )


if __name__ == '__main__':
    unittest.main()
