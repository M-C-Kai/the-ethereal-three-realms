"""统一测试：角色系统（账号、登录跳转、角色存储、面板、登出）。"""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from app.context import SystemContext
from protocol import byte, decode_frame, encode_frame, field_values, integer, short, string
from systems.role.handler import RoleSystem
from systems.role.service import AccountStore, RoleStore, default_role, role_entry_frames


ROOT = Path(__file__).resolve().parent.parent


def load_settings():
    import server

    settings = server.Settings.load(server.Path(ROOT) / 'config.json')
    settings.accept_any_credentials = False
    return settings


class RoleStoreTests(unittest.TestCase):
    def test_battle_speed_matches_live_character_attribute(self):
        from systems.role.service import combat_stats, effective_character_stats
        role = {'level': 1, 'stats': [10, 10, 10, 10, 23], 'items': []}
        self.assertEqual(combat_stats(role).speed, 23)
        role['stats'][4] = 41
        self.assertEqual(combat_stats(role).speed, effective_character_stats(role)[4])

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.settings = load_settings()
        self.settings.role_data_file = str(Path(self.tmp.name) / 'roles.json')
        self.settings.account_data_file = str(Path(self.tmp.name) / 'accounts.json')
        self.store = RoleStore(self.settings)

    def tearDown(self):
        self.tmp.cleanup()

    def test_default_role_shape(self):
        role = default_role(self.settings)
        self.assertEqual(int(role['bag_capacity']), 1000)
        self.assertIsInstance(role['items'], list)
        self.assertGreater(len(role['items']), 0)
        self.assertTrue(role.get('mailbox_initialized'))
        self.assertIn('fuyuan', role)
        self.assertIn('tasks', role)
        currencies = role['currencies']
        for name in ('silver', 'immortal_stones', 'immortal_crystals'):
            self.assertIn(name, currencies)

    def test_create_persists_and_reload_keeps_items(self):
        created = self.store.create('tester', '测试角色', 0, 0)
        roles = self.store.roles_for('tester')
        self.assertIn(created['id'], [r['id'] for r in roles])
        store2 = RoleStore(self.settings)
        roles2 = store2.roles_for('tester')
        self.assertEqual(len(roles2[0]['items']), len(created['items']))

    def test_delete_role(self):
        created = self.store.create('tester', '测试角色', 0, 0)
        self.assertTrue(self.store.delete('tester', int(created['id'])))
        self.assertFalse(self.store.delete('tester', int(created['id'])))


class RoleHandlerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.settings = load_settings()
        self.settings.accept_any_credentials = True
        self.settings.role_data_file = str(Path(self.tmp.name) / 'roles.json')
        self.settings.account_data_file = str(Path(self.tmp.name) / 'accounts.json')
        self.accounts = AccountStore(self.settings)
        self.store = RoleStore(self.settings)
        self.role_system = RoleSystem(
            self.settings,
            store=self.store,
            accounts=self.accounts,
        )
        self.session = {}

    def tearDown(self):
        self.tmp.cleanup()

    def _context(self, role=None):
        return SystemContext(username='tester', active_role=role, session=self.session)

    def _dispatch(self, frame_id, fields, role=None):
        return self.role_system.handle(self._context(role), frame_id, fields)

    def test_login_with_any_credentials_disabled_rejects(self):
        self.settings.accept_any_credentials = False
        result = self._dispatch(1077, [short(2000), byte(53), byte(0), string('ghost'), string('badpw')])
        self.assertTrue(result.handled)
        message_id, fields = decode_frame(result.frames[0])
        self.assertEqual(message_id, 1055)
        self.assertEqual(int(fields[0].value), 5)

    def test_login_success_returns_server_list(self):
        result = self._dispatch(1077, [short(2000), byte(53), byte(0), string('tester'), string('x')])
        message_id, fields = decode_frame(result.frames[0])
        self.assertEqual(message_id, 1077)
        self.assertEqual(int(fields[2].value), 1)  # 服务器状态：良好

    def test_logout_page_and_confirm_frames(self):
        logout_frame = encode_frame(1054, [byte(8)])
        result = self.role_system.handle(self._context(), 1054, [logout_frame and None][0:0] or [
            __import__('protocol').Field(2, 8)  # BYTE 8
        ])
        self.assertTrue(result.handled)
        message_id, fields = decode_frame(result.frames[0])
        self.assertEqual(message_id, 1054)
        confirm = self.role_system.handle(self._context(), 1003, [__import__('protocol').Field(4, 0)])
        message_id, fields = decode_frame(confirm.frames[0])
        self.assertEqual(message_id, 1003)

    def test_menu_prefetch_ack(self):
        result = self.role_system.handle(self._context(), 1090, [byte(0)])
        self.assertTrue(result.handled)
        message_id, fields = decode_frame(result.frames[0])
        self.assertEqual((message_id, int(fields[0].value)), (1090, 0))

    def test_character_panel_frames(self):
        role = default_role(self.settings)
        result = self.role_system.handle(self._context(role), 1039, [byte(1)])
        self.assertTrue(result.handled)
        self.assertEqual(len(result.frames), 3)  # 1049 进度 + 1039 属性 + 1039 神通
        message_id, _ = decode_frame(result.frames[1])
        self.assertEqual(message_id, 1039)


if __name__ == '__main__':
    unittest.main()
