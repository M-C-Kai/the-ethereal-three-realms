import tempfile
import unittest
from pathlib import Path

from protocol import decode_frame, field_values
from server import AccountStore, RoleStore, Settings, account_result, creation_names, role_creation_frames, role_list


class AccountAuthTests(unittest.TestCase):
    def settings(self, directory: str) -> Settings:
        return Settings(
            role_data_file=str(Path(directory) / 'roles.json'),
            account_data_file=str(Path(directory) / 'accounts.json'),
            password_hash_iterations=1_000,
            accept_any_credentials=False,
        )

    def test_registration_authentication_and_password_change_are_persistent(self):
        with tempfile.TemporaryDirectory() as directory:
            settings = self.settings(directory)
            accounts = AccountStore(settings)
            self.assertEqual(accounts.register('tester01', 'pass1234'), 'ok')
            self.assertEqual(accounts.register('tester01', 'pass1234'), 'exists')
            self.assertTrue(accounts.authenticate('tester01', 'pass1234'))
            self.assertFalse(accounts.authenticate('tester01', 'wrong123'))
            self.assertEqual(accounts.change_password('tester01', 'pass1234', 'newpass9'), 'ok')
            reloaded = AccountStore(settings)
            self.assertFalse(reloaded.authenticate('tester01', 'pass1234'))
            self.assertTrue(reloaded.authenticate('tester01', 'newpass9'))

    def test_new_account_has_no_default_role_and_creation_names_are_blank(self):
        with tempfile.TemporaryDirectory() as directory:
            settings = self.settings(directory)
            self.assertEqual(RoleStore(settings).roles_for('brandnew', create_default=False), [])
        message_id, fields = decode_frame(creation_names())
        self.assertEqual(message_id, 1080)
        self.assertEqual(field_values(fields), [4, '', ''])

    def test_account_result_matches_client_1055_layout(self):
        message_id, fields = decode_frame(account_result(5))
        self.assertEqual(message_id, 1055)
        self.assertEqual(field_values(fields), [5, ''])

    def test_newly_created_role_returns_to_role_page_without_entry_frames(self):
        with tempfile.TemporaryDirectory() as directory:
            settings = self.settings(directory)
            store = RoleStore(settings)
            role = store.create('brandnew', '仙族测试', 6, 0)
            frames = role_creation_frames(settings, store.roles_for('brandnew'))
        self.assertEqual(role['sect_id'], 0)
        message_ids = [decode_frame(frame)[0] for frame in frames]
        self.assertEqual(message_ids, [1080])

    def test_role_page_composite_field_is_sect_times_ten_plus_race(self):
        settings = Settings()
        role = {
            'id': 77, 'name': '仙族无门派', 'model': 6, 'slot': 0,
            'level': 1, 'race': 1, 'gender': 0, 'sect_id': 0, 'items': [],
        }
        _, fields = decode_frame(role_list(settings, [role]))
        self.assertEqual(field_values(fields)[6], 1)
        role['sect_id'] = 1
        _, fields = decode_frame(role_list(settings, [role]))
        self.assertEqual(field_values(fields)[6], 11)


if __name__ == '__main__':
    unittest.main()
