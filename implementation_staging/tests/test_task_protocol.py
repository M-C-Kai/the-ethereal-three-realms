import json
import tempfile
import unittest
from pathlib import Path

from protocol import Field, TYPE_BYTE, TYPE_INT, TYPE_SHORT, decode_frame
from task_registry import TaskRegistry
from task_protocol import (
    active_task_list_frame,
    available_task_list_frame,
    detail_request_task_id,
    is_active_list_request,
    is_available_list_request,
    parse_task_1145_request,
    parse_task_operation_request,
    safe_detail_ack_frame,
)


class TaskProtocolTests(unittest.TestCase):
    def make_task(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        path = Path(temp.name) / 'tasks.json'
        path.write_text(json.dumps({'version': 1, 'tasks': [{
            'task_id': 10001, 'category': 'main', 'name': '试炼起步', 'description': '',
            'level_requirement': 2, 'prerequisites': [],
            'objectives': [{'kind': 'battle_won', 'target_id': 0, 'required': 1}],
            'rewards': [], 'repeat_policy': 'once', 'daily_limit': 0,
            'client_route': {'route_id': 11001, 'route_kind': 7},
        }]}), encoding='utf-8')
        return TaskRegistry(path, item_exists=lambda _: True).require(10001)

    def test_recognizes_active_list_request_only_with_exact_byte_types(self):
        self.assertTrue(is_active_list_request([Field(TYPE_BYTE, 6), Field(TYPE_BYTE, 0), Field(TYPE_BYTE, 0), Field(TYPE_BYTE, 0)]))
        self.assertFalse(is_active_list_request([Field(TYPE_INT, 6), Field(TYPE_BYTE, 0), Field(TYPE_BYTE, 0), Field(TYPE_BYTE, 0)]))
        self.assertFalse(is_active_list_request([Field(TYPE_BYTE, 6), Field(TYPE_BYTE, 0), Field(TYPE_BYTE, 0)]))

    def test_recognizes_available_list_request_only_with_exact_byte_types(self):
        self.assertTrue(is_available_list_request([Field(TYPE_BYTE, 50), Field(TYPE_BYTE, 0), Field(TYPE_BYTE, 0)]))
        self.assertFalse(is_available_list_request([Field(TYPE_BYTE, 50), Field(TYPE_INT, 0), Field(TYPE_BYTE, 0)]))

    def test_parses_detail_requests_with_byte_action_and_int_task_id(self):
        for action in (15, 22, 52):
            self.assertEqual(77, detail_request_task_id([Field(TYPE_BYTE, action), Field(TYPE_INT, 77)]))
        self.assertIsNone(detail_request_task_id([Field(TYPE_SHORT, 52), Field(TYPE_INT, 77)]))

    def test_parses_1403_operation_request_exactly(self):
        request = parse_task_operation_request([
            Field(TYPE_BYTE, 7), Field(TYPE_INT, 11), Field(TYPE_INT, 12), Field(TYPE_BYTE, 4), Field(TYPE_BYTE, 5)
        ])
        self.assertIsNotNone(request)
        self.assertEqual((11, 12, 4, 5), (request.first_id, request.second_id, request.operation, request.category))
        self.assertIsNone(parse_task_operation_request([
            Field(TYPE_BYTE, 7), Field(TYPE_INT, 11), Field(TYPE_INT, 12), Field(TYPE_INT, 4), Field(TYPE_BYTE, 5)
        ]))

    def test_parses_1145_available_and_active_task_variants(self):
        available = parse_task_1145_request([
            Field(TYPE_BYTE, 0), Field(TYPE_INT, 11001), Field(TYPE_BYTE, 1), Field(TYPE_BYTE, 7)
        ])
        self.assertEqual(('available', 11001, 0, 1, 0, 7), (available.variant, available.route_id, available.operation, available.category, available.task_id, available.route_kind))
        active = parse_task_1145_request([
            Field(TYPE_BYTE, 0), Field(TYPE_INT, 11001), Field(TYPE_BYTE, 2), Field(TYPE_BYTE, 1), Field(TYPE_INT, 10001)
        ])
        self.assertEqual(('active', 11001, 2, 1, 10001, 0), (active.variant, active.route_id, active.operation, active.category, active.task_id, active.route_kind))
        self.assertIsNone(parse_task_1145_request([Field(TYPE_BYTE, 0), Field(TYPE_INT, 1)]))

    def test_available_frame_matches_apk_action_50_header_and_record_layout(self):
        task = self.make_task()
        message_id, fields = decode_frame(available_task_list_frame([task]))
        self.assertEqual(1403, message_id)
        self.assertEqual([(TYPE_BYTE, 50), (TYPE_SHORT, 1), (TYPE_BYTE, 6)], [(f.type_id, f.value) for f in fields[:3]])
        self.assertEqual([10001, '试炼起步', 0, 11001, 1, 7], [f.value for f in fields[3:]])

    def test_active_frame_matches_apk_action_6_header_and_record_layout(self):
        task = self.make_task()
        message_id, fields = decode_frame(active_task_list_frame(1, [(task, 'ready')]))
        self.assertEqual(1403, message_id)
        self.assertEqual([(TYPE_BYTE, 6), (TYPE_SHORT, 1), (TYPE_BYTE, 9), (TYPE_BYTE, 1)], [(f.type_id, f.value) for f in fields[:4]])
        self.assertEqual([10001, '试炼起步', 0, 2, 4, 11001, 2, 1, 10001], [f.value for f in fields[4:]])

    def test_detail_ack_is_safe_unhandled_action(self):
        message_id, fields = decode_frame(safe_detail_ack_frame())
        self.assertEqual(1403, message_id)
        self.assertEqual([(TYPE_BYTE, 1)], [(f.type_id, f.value) for f in fields])


if __name__ == '__main__':
    unittest.main()
