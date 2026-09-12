import json
import tempfile
import unittest
from pathlib import Path

from task_registry import TaskRegistry
from task_service import (
    abandon_task,
    accept_task,
    available_tasks,
    claim_task,
    ensure_task_state,
    record_event,
)


class TaskServiceTests(unittest.TestCase):
    def make_registry(self):
        tasks = [
            {
                'task_id': 1, 'category': 'main', 'name': '主线一', 'description': '',
                'level_requirement': 1, 'prerequisites': [],
                'objectives': [{'kind': 'monster_killed', 'target_id': 10, 'required': 2}],
                'rewards': [{'kind': 'experience', 'amount': 10}],
                'repeat_policy': 'once', 'daily_limit': 0,
                'client_route': {'route_id': 1, 'route_kind': 1},
            },
            {
                'task_id': 2, 'category': 'side', 'name': '前置任务', 'description': '',
                'level_requirement': 2, 'prerequisites': [1],
                'objectives': [{'kind': 'map_entered', 'target_id': 58, 'required': 1}],
                'rewards': [], 'repeat_policy': 'once', 'daily_limit': 0,
                'client_route': {'route_id': 2, 'route_kind': 1},
            },
            {
                'task_id': 3, 'category': 'cycle', 'name': '循环任务', 'description': '',
                'level_requirement': 1, 'prerequisites': [],
                'objectives': [{'kind': 'battle_won', 'target_id': 0, 'required': 1}],
                'rewards': [], 'repeat_policy': 'repeat', 'daily_limit': 0,
                'client_route': {'route_id': 3, 'route_kind': 1},
            },
            {
                'task_id': 4, 'category': 'daily', 'name': '每日任务', 'description': '',
                'level_requirement': 1, 'prerequisites': [],
                'objectives': [{'kind': 'npc_talked', 'target_id': 99, 'required': 1}],
                'rewards': [], 'repeat_policy': 'daily', 'daily_limit': 1,
                'client_route': {'route_id': 4, 'route_kind': 1},
            },
        ]
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        path = Path(temp.name) / 'tasks.json'
        path.write_text(json.dumps({'version': 1, 'tasks': tasks}), encoding='utf-8')
        return TaskRegistry(path, item_exists=lambda _: True)

    def test_migrates_legacy_role_without_touching_existing_fields(self):
        role = {'id': 7, 'name': '旧角色', 'items': [{'id': 1}]}
        changed = ensure_task_state(role, today='2026-09-12')
        self.assertTrue(changed)
        self.assertEqual('旧角色', role['name'])
        self.assertEqual([{'id': 1}], role['items'])
        self.assertEqual(1, role['tasks']['version'])
        self.assertEqual({}, role['tasks']['active'])
        self.assertEqual({}, role['tasks']['completed'])
        self.assertEqual({'date': '2026-09-12', 'counts': {}}, role['tasks']['daily'])
        self.assertFalse(ensure_task_state(role, today='2026-09-12'))

    def test_available_tasks_apply_level_and_prerequisite_gates(self):
        registry = self.make_registry()
        role = {'level': 1}
        ensure_task_state(role, today='2026-09-12')
        self.assertEqual([1, 3, 4], [task.task_id for task in available_tasks(role, registry, today='2026-09-12')])
        role['level'] = 2
        role['tasks']['completed']['1'] = 1
        self.assertEqual([2, 3, 4], [task.task_id for task in available_tasks(role, registry, today='2026-09-12')])

    def test_accept_and_abandon_are_idempotent_and_do_not_mark_completed(self):
        registry = self.make_registry()
        role = {'level': 1}
        first = accept_task(role, registry, 1, now=100, today='2026-09-12')
        self.assertTrue(first.ok)
        self.assertTrue(first.changed)
        self.assertEqual('active', role['tasks']['active']['1']['status'])
        duplicate = accept_task(role, registry, 1, now=101, today='2026-09-12')
        self.assertFalse(duplicate.ok)
        self.assertFalse(duplicate.changed)
        abandoned = abandon_task(role, registry, 1, today='2026-09-12')
        self.assertTrue(abandoned.ok)
        self.assertNotIn('1', role['tasks']['active'])
        self.assertNotIn('1', role['tasks']['completed'])
        again = abandon_task(role, registry, 1, today='2026-09-12')
        self.assertFalse(again.ok)
        self.assertFalse(again.changed)

    def test_matching_events_increment_and_transition_to_ready(self):
        registry = self.make_registry()
        role = {'level': 1}
        accept_task(role, registry, 1, now=100, today='2026-09-12')
        self.assertEqual((), record_event(role, registry, 'monster_killed', target_id=11, amount=1, now=101, today='2026-09-12'))
        changed = record_event(role, registry, 'monster_killed', target_id=10, amount=1, now=102, today='2026-09-12')
        self.assertEqual((1,), changed)
        self.assertEqual([1], role['tasks']['active']['1']['progress'])
        changed = record_event(role, registry, 'monster_killed', target_id=10, amount=5, now=103, today='2026-09-12')
        self.assertEqual((1,), changed)
        self.assertEqual([2], role['tasks']['active']['1']['progress'])
        self.assertEqual('ready', role['tasks']['active']['1']['status'])
        self.assertEqual(103, role['tasks']['active']['1']['completed_at'])
        self.assertEqual((), record_event(role, registry, 'monster_killed', target_id=10, amount=1, now=104, today='2026-09-12'))

    def test_zero_target_is_wildcard_for_repeatable_battle_task(self):
        registry = self.make_registry()
        role = {'level': 1}
        accept_task(role, registry, 3, now=1, today='2026-09-12')
        self.assertEqual((3,), record_event(role, registry, 'battle_won', target_id=888, now=2, today='2026-09-12'))
        self.assertEqual('ready', role['tasks']['active']['3']['status'])

    def test_claim_is_atomic_when_reward_applier_rejects(self):
        registry = self.make_registry()
        role = {'level': 1}
        accept_task(role, registry, 1, now=1, today='2026-09-12')
        record_event(role, registry, 'monster_killed', target_id=10, amount=2, now=2, today='2026-09-12')
        result = claim_task(role, registry, 1, reward_applier=lambda _role, _task: False, now=3, today='2026-09-12')
        self.assertFalse(result.ok)
        self.assertFalse(result.changed)
        self.assertEqual('ready', role['tasks']['active']['1']['status'])
        self.assertEqual({}, role['tasks']['completed'])

    def test_claim_once_records_completion_and_removes_task(self):
        registry = self.make_registry()
        role = {'level': 1}
        accept_task(role, registry, 1, now=1, today='2026-09-12')
        record_event(role, registry, 'monster_killed', target_id=10, amount=2, now=2, today='2026-09-12')
        result = claim_task(role, registry, 1, reward_applier=lambda _role, _task: True, now=3, today='2026-09-12')
        self.assertTrue(result.ok)
        self.assertNotIn('1', role['tasks']['active'])
        self.assertEqual(1, role['tasks']['completed']['1'])
        self.assertNotIn(1, [task.task_id for task in available_tasks(role, registry, today='2026-09-12')])

    def test_repeat_task_becomes_available_after_claim(self):
        registry = self.make_registry()
        role = {'level': 1}
        accept_task(role, registry, 3, now=1, today='2026-09-12')
        record_event(role, registry, 'battle_won', target_id=1, now=2, today='2026-09-12')
        claim_task(role, registry, 3, reward_applier=lambda _role, _task: True, now=3, today='2026-09-12')
        self.assertEqual(1, role['tasks']['completed']['3'])
        self.assertIn(3, [task.task_id for task in available_tasks(role, registry, today='2026-09-12')])

    def test_daily_limit_blocks_same_day_and_resets_lazily(self):
        registry = self.make_registry()
        role = {'level': 1}
        accept_task(role, registry, 4, now=1, today='2026-09-12')
        record_event(role, registry, 'npc_talked', target_id=99, now=2, today='2026-09-12')
        claim_task(role, registry, 4, reward_applier=lambda _role, _task: True, now=3, today='2026-09-12')
        self.assertEqual(1, role['tasks']['daily']['counts']['4'])
        self.assertNotIn(4, [task.task_id for task in available_tasks(role, registry, today='2026-09-12')])
        self.assertIn(4, [task.task_id for task in available_tasks(role, registry, today='2026-09-13')])
        self.assertEqual({'date': '2026-09-13', 'counts': {}}, role['tasks']['daily'])


if __name__ == '__main__':
    unittest.main()
