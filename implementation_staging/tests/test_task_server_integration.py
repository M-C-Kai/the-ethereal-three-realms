import tempfile
import unittest
from pathlib import Path

from protocol import Field, TYPE_BYTE, TYPE_INT, decode_frame
from server import LocalGameServer, MENU_PREFETCH_EMPTY_SUBTYPES, Settings, default_role


class TaskServerIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.settings = Settings(
            account_data_file=str(root / 'accounts.json'),
            role_data_file=str(root / 'roles.json'),
        )
        self.server = LocalGameServer(self.settings)

    def test_task_protocol_is_not_served_by_empty_prefetch_anymore(self):
        self.assertNotIn(1403, MENU_PREFETCH_EMPTY_SUBTYPES)
        self.assertTrue(hasattr(self.server, 'task_runtime'))

    def test_roles_for_migrates_legacy_role_task_state_and_persists_it(self):
        legacy = default_role(self.settings)
        legacy.pop('tasks', None)
        self.server.roles.data = {
            'next_role_id': int(legacy['id']) + 1,
            'accounts': {'tester': [legacy]},
        }
        roles = self.server.roles.roles_for('tester')
        self.assertEqual(1, roles[0]['tasks']['version'])
        self.assertEqual({}, roles[0]['tasks']['active'])
        self.assertTrue(self.server.roles.path.exists())
        self.assertIn('"tasks"', self.server.roles.path.read_text(encoding='utf-8'))

    def test_1403_available_list_uses_task_runtime_and_real_npc_route(self):
        role = default_role(self.settings)
        frames = self.server.handle_task_1403(
            role,
            [Field(TYPE_BYTE, 50), Field(TYPE_BYTE, 0), Field(TYPE_BYTE, 0)],
        )
        self.assertEqual(1, len(frames))
        message_id, fields = decode_frame(frames[0])
        self.assertEqual(1403, message_id)
        self.assertEqual(50, fields[0].value)
        self.assertEqual(0, fields[1].value)
        self.assertGreaterEqual(fields[2].value, 1)
        # First catalog row is the minimum main task.  The APK's native task
        # row can now pathfind its “领取任务” action to 接引真人 in 长安.
        self.assertEqual(
            [900001, '试炼启程', 1, 58, 34, 50, 1900003],
            [field.value for field in fields[3:10]],
        )

    def test_accept_progress_claim_round_trip_persists_state_and_rewards(self):
        role = default_role(self.settings)
        self.server.task_runtime.migrate_role(role, today='2026-09-12')
        self.server.roles.data = {
            'next_role_id': int(role['id']) + 1,
            'accounts': {'tester': [role]},
        }
        silver_before = int(role['currencies']['silver'])

        accepted = self.server.handle_task_1145(
            role,
            [
                Field(TYPE_BYTE, 0),
                Field(TYPE_INT, 900001),
                Field(TYPE_BYTE, 1),
                Field(TYPE_BYTE, 1),
            ],
            now=10,
            today='2026-09-12',
        )
        self.assertIsNotNone(accepted)
        self.assertEqual('active', role['tasks']['active']['900001']['status'])

        self.server.record_task_event(
            role,
            'map_entered',
            target_id=50000,
            now=20,
            today='2026-09-12',
        )
        self.assertEqual('ready', role['tasks']['active']['900001']['status'])

        claimed = self.server.handle_task_1145(
            role,
            [
                Field(TYPE_BYTE, 0),
                Field(TYPE_INT, 900001),
                Field(TYPE_BYTE, 2),
                Field(TYPE_BYTE, 1),
                Field(TYPE_INT, 900001),
            ],
            now=30,
            today='2026-09-12',
        )
        self.assertIsNotNone(claimed)
        self.assertNotIn('900001', role['tasks']['active'])
        self.assertEqual(1, role['tasks']['completed']['900001'])
        self.assertGreater(int(role['currencies']['silver']), silver_before)
        self.assertTrue(self.server.roles.path.exists())

    def test_live_pathfind_1145_payload_still_falls_through(self):
        role = default_role(self.settings)
        result = self.server.handle_task_1145(
            role,
            [
                Field(TYPE_BYTE, 0),
                Field(TYPE_INT, 58),
                Field(TYPE_BYTE, 10),
                Field(TYPE_BYTE, 11),
            ],
        )
        self.assertIsNone(result)

    def test_non_task_1145_payload_still_falls_through(self):
        role = default_role(self.settings)
        result = self.server.handle_task_1145(
            role,
            [Field(TYPE_INT, 58), Field(TYPE_INT, 10), Field(TYPE_INT, 11)],
        )
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
