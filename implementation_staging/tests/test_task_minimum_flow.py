import json
import tempfile
import unittest
from pathlib import Path

from protocol import Field, TYPE_BYTE, TYPE_INT, decode_frame
from task_protocol import parse_task_accept_request
from task_registry import TaskRegistry
from task_runtime import TaskRuntime


class TaskMinimumFlowTests(unittest.TestCase):
    def make_runtime(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        path = Path(temp.name) / 'tasks.json'
        path.write_text(json.dumps({'version': 1, 'tasks': [{
            'task_id': 101,
            'category': 'main',
            'name': '试炼起步',
            'description': '',
            'level_requirement': 1,
            'prerequisites': [],
            'objectives': [{'kind': 'map_entered', 'target_id': 50000, 'required': 1}],
            'rewards': [],
            'repeat_policy': 'once',
            'daily_limit': 0,
            'client_route': {
                'route_id': 1101,
                'route_kind': 7,
                'accept_map_id': 58,
                'accept_x': 34,
                'accept_y': 50,
                'accept_actor_id': 1900003,
                'submit_map_id': 58,
                'submit_x': 34,
                'submit_y': 50,
                'submit_actor_id': 1900003,
            },
        }]}), encoding='utf-8')
        return TaskRuntime(TaskRegistry(path, item_exists=lambda _: True))

    def test_apk_action8_accept_request_is_exact_byte_int_int(self):
        request = parse_task_accept_request([
            Field(TYPE_BYTE, 8),
            Field(TYPE_INT, 10001),
            Field(TYPE_INT, 101),
        ])
        self.assertIsNotNone(request)
        self.assertEqual((10001, 101), (request.player_id, request.task_id))
        self.assertIsNone(parse_task_accept_request([
            Field(TYPE_INT, 8),
            Field(TYPE_INT, 10001),
            Field(TYPE_INT, 101),
        ]))

    def test_action8_accepts_task_and_refreshes_native_status(self):
        runtime = self.make_runtime()
        role = {'id': 10001, 'level': 1}
        result = runtime.handle_1403(
            role,
            [Field(TYPE_BYTE, 8), Field(TYPE_INT, 10001), Field(TYPE_INT, 101)],
            now=10,
            today='2026-09-12',
        )
        self.assertTrue(result.changed)
        self.assertEqual('active', role['tasks']['active']['101']['status'])
        _, fields = decode_frame(result.frames[0])
        self.assertEqual(50, fields[0].value)
        self.assertEqual(2, fields[5].value)

    def test_action8_rejects_other_player_id(self):
        runtime = self.make_runtime()
        role = {'id': 10001, 'level': 1}
        result = runtime.handle_1403(
            role,
            [Field(TYPE_BYTE, 8), Field(TYPE_INT, 99999), Field(TYPE_INT, 101)],
            now=10,
            today='2026-09-12',
        )
        self.assertFalse(result.changed)
        self.assertEqual({}, role['tasks']['active'])

    def test_task_accept_and_submit_coordinates_are_valid_path_targets(self):
        runtime = self.make_runtime()
        self.assertTrue(runtime.matches_path_target(58, 34, 50))
        self.assertFalse(runtime.matches_path_target(58, 35, 50))
        self.assertFalse(runtime.matches_path_target(50000, 34, 50))


if __name__ == '__main__':
    unittest.main()
