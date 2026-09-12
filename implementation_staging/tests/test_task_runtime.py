import json
import tempfile
import unittest
from pathlib import Path

from protocol import Field, TYPE_BYTE, TYPE_INT, decode_frame
from task_registry import TaskRegistry
from task_runtime import TaskRuntime


class TaskRuntimeTests(unittest.TestCase):
    def make_runtime(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        path = Path(temp.name) / 'tasks.json'
        path.write_text(json.dumps({'version': 1, 'tasks': [
            {
                'task_id': 101, 'category': 'main', 'name': '击败妖兽', 'description': '',
                'level_requirement': 1, 'prerequisites': [],
                'objectives': [{'kind': 'monster_killed', 'target_id': 1900001, 'required': 1}],
                'rewards': [{'kind': 'experience', 'amount': 10}],
                'repeat_policy': 'once', 'daily_limit': 0,
                'client_route': {'route_id': 1101, 'route_kind': 7},
            },
            {
                'task_id': 102, 'category': 'daily', 'name': '进昆仑', 'description': '',
                'level_requirement': 1, 'prerequisites': [],
                'objectives': [{'kind': 'map_entered', 'target_id': 60001, 'required': 1}],
                'rewards': [], 'repeat_policy': 'daily', 'daily_limit': 1,
                'client_route': {'route_id': 1102, 'route_kind': 7},
            },
        ]}), encoding='utf-8')
        return TaskRuntime(TaskRegistry(path, item_exists=lambda _: True))

    def test_1403_list_requests_return_native_snapshots(self):
        runtime = self.make_runtime()
        role = {'level': 1}
        available = runtime.handle_1403(role, [Field(TYPE_BYTE, 50), Field(TYPE_BYTE, 0), Field(TYPE_BYTE, 0)], today='2026-09-12')
        self.assertTrue(available.handled)
        self.assertTrue(available.changed)
        message_id, fields = decode_frame(available.frames[0])
        self.assertEqual(1403, message_id)
        self.assertEqual(50, fields[0].value)
        self.assertEqual(2, fields[1].value)

        active = runtime.handle_1403(role, [Field(TYPE_BYTE, 6), Field(TYPE_BYTE, 0), Field(TYPE_BYTE, 0), Field(TYPE_BYTE, 0)], today='2026-09-12')
        self.assertEqual(5, len(active.frames))
        self.assertEqual([1, 2, 3, 4, 6], [decode_frame(frame)[1][3].value for frame in active.frames])

    def test_available_1145_accepts_by_route_and_returns_snapshots(self):
        runtime = self.make_runtime()
        role = {'level': 1}
        result = runtime.handle_1145(role, [
            Field(TYPE_BYTE, 0), Field(TYPE_INT, 1101), Field(TYPE_BYTE, 1), Field(TYPE_BYTE, 7)
        ], now=10, today='2026-09-12')
        self.assertTrue(result.handled)
        self.assertTrue(result.changed)
        self.assertEqual('active', role['tasks']['active']['101']['status'])
        self.assertEqual(6, len(result.frames))

    def test_active_1145_abandon_and_claim_use_exact_task_route(self):
        runtime = self.make_runtime()
        role = {'level': 1}
        runtime.handle_1145(role, [Field(TYPE_BYTE, 0), Field(TYPE_INT, 1101), Field(TYPE_BYTE, 1), Field(TYPE_BYTE, 7)], now=1, today='2026-09-12')
        abandon = runtime.handle_1145(role, [
            Field(TYPE_BYTE, 0), Field(TYPE_INT, 1101), Field(TYPE_BYTE, 4), Field(TYPE_BYTE, 1), Field(TYPE_INT, 101)
        ], now=2, today='2026-09-12')
        self.assertTrue(abandon.changed)
        self.assertNotIn('101', role['tasks']['active'])

        runtime.handle_1145(role, [Field(TYPE_BYTE, 0), Field(TYPE_INT, 1101), Field(TYPE_BYTE, 1), Field(TYPE_BYTE, 7)], now=3, today='2026-09-12')
        runtime.record_event(role, 'monster_killed', target_id=1900001, now=4, today='2026-09-12')
        claimed = runtime.handle_1145(role, [
            Field(TYPE_BYTE, 0), Field(TYPE_INT, 1101), Field(TYPE_BYTE, 2), Field(TYPE_BYTE, 1), Field(TYPE_INT, 101)
        ], reward_applier=lambda _role, _task: True, now=5, today='2026-09-12')
        self.assertTrue(claimed.changed)
        self.assertEqual(1, role['tasks']['completed']['101'])

    def test_wrong_route_does_not_mutate_role(self):
        runtime = self.make_runtime()
        role = {'level': 1}
        runtime.migrate_role(role, today='2026-09-12')
        result = runtime.handle_1145(role, [
            Field(TYPE_BYTE, 0), Field(TYPE_INT, 9999), Field(TYPE_BYTE, 1), Field(TYPE_BYTE, 7)
        ], today='2026-09-12')
        self.assertTrue(result.handled)
        self.assertFalse(result.changed)
        self.assertEqual({}, role['tasks']['active'])

    def test_non_task_1145_shape_falls_through(self):
        runtime = self.make_runtime()
        role = {'level': 1}
        self.assertIsNone(runtime.handle_1145(role, [Field(TYPE_INT, 58), Field(TYPE_INT, 10), Field(TYPE_INT, 11)], today='2026-09-12'))

    def test_record_event_persists_ready_state_and_returns_refresh(self):
        runtime = self.make_runtime()
        role = {'level': 1}
        runtime.handle_1145(role, [Field(TYPE_BYTE, 0), Field(TYPE_INT, 1101), Field(TYPE_BYTE, 1), Field(TYPE_BYTE, 7)], now=1, today='2026-09-12')
        result = runtime.record_event(role, 'monster_killed', target_id=1900001, now=2, today='2026-09-12')
        self.assertTrue(result.changed)
        self.assertEqual('ready', role['tasks']['active']['101']['status'])
        active_frames = [frame for frame in result.frames if decode_frame(frame)[1][0].value == 6]
        main = next(frame for frame in active_frames if decode_frame(frame)[1][3].value == 1)
        self.assertEqual(2, decode_frame(main)[1][10].value)

    def test_detail_request_uses_safe_ack_until_layout_is_fully_traced(self):
        runtime = self.make_runtime()
        role = {'level': 1}
        result = runtime.handle_1403(role, [Field(TYPE_BYTE, 52), Field(TYPE_INT, 101)], today='2026-09-12')
        self.assertTrue(result.handled)
        self.assertEqual(1, decode_frame(result.frames[0])[1][0].value)


if __name__ == '__main__':
    unittest.main()
