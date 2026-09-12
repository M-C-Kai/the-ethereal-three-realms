import json
import tempfile
import unittest
from pathlib import Path

from task_registry import TaskCatalogError, TaskRegistry


class TaskRegistryTests(unittest.TestCase):
    def write_catalog(self, data):
        temp = tempfile.TemporaryDirectory()
        path = Path(temp.name) / 'tasks.json'
        path.write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')
        self.addCleanup(temp.cleanup)
        return path

    def base_task(self, **overrides):
        task = {
            'task_id': 10001,
            'category': 'main',
            'name': '试炼起步',
            'description': '击败试炼妖兽。',
            'level_requirement': 1,
            'prerequisites': [],
            'objectives': [{'kind': 'monster_killed', 'target_id': 1900001, 'required': 1}],
            'rewards': [{'kind': 'experience', 'amount': 100}],
            'repeat_policy': 'once',
            'daily_limit': 0,
            'client_route': {'route_id': 10001, 'route_kind': 1},
        }
        task.update(overrides)
        return task

    def test_loads_valid_catalog_and_orders_by_task_id(self):
        data = {'version': 1, 'tasks': [self.base_task(task_id=10002), self.base_task(task_id=10001)]}
        registry = TaskRegistry(self.write_catalog(data), item_exists=lambda _: True)
        self.assertEqual([10001, 10002], [task.task_id for task in registry.all_tasks()])
        self.assertEqual('main', registry.require(10001).category)

    def test_rejects_duplicate_task_id(self):
        data = {'version': 1, 'tasks': [self.base_task(), self.base_task()]}
        with self.assertRaisesRegex(TaskCatalogError, 'duplicate task_id 10001'):
            TaskRegistry(self.write_catalog(data), item_exists=lambda _: True)

    def test_rejects_invalid_category(self):
        data = {'version': 1, 'tasks': [self.base_task(category='mystery')]}
        with self.assertRaisesRegex(TaskCatalogError, 'invalid category'):
            TaskRegistry(self.write_catalog(data), item_exists=lambda _: True)

    def test_rejects_invalid_objective(self):
        data = {'version': 1, 'tasks': [self.base_task(objectives=[{'kind': 'monster_killed', 'target_id': 1, 'required': 0}])]}
        with self.assertRaisesRegex(TaskCatalogError, 'objective required'):
            TaskRegistry(self.write_catalog(data), item_exists=lambda _: True)

    def test_rejects_unknown_item_reward(self):
        data = {'version': 1, 'tasks': [self.base_task(rewards=[{'kind': 'item', 'template_id': 999, 'quantity': 1}])]}
        with self.assertRaisesRegex(TaskCatalogError, 'unknown item template 999'):
            TaskRegistry(self.write_catalog(data), item_exists=lambda value: value != 999)

    def test_rejects_broken_prerequisite(self):
        data = {'version': 1, 'tasks': [self.base_task(prerequisites=[99999])]}
        with self.assertRaisesRegex(TaskCatalogError, 'unknown prerequisite 99999'):
            TaskRegistry(self.write_catalog(data), item_exists=lambda _: True)

    def test_category_wire_ids_match_apk_task_tabs(self):
        data = {'version': 1, 'tasks': [
            self.base_task(task_id=1, category='main'),
            self.base_task(task_id=2, category='side'),
            self.base_task(task_id=3, category='cycle'),
            self.base_task(task_id=4, category='daily'),
            self.base_task(task_id=5, category='divine'),
        ]}
        registry = TaskRegistry(self.write_catalog(data), item_exists=lambda _: True)
        self.assertEqual([1, 2, 3, 4, 6], [registry.require(i).category_wire_id for i in range(1, 6)])


if __name__ == '__main__':
    unittest.main()
