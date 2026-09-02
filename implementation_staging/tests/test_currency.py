import json
import sys
import tempfile
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from protocol import decode_frame, field_values
from server import RoleStore, Settings, default_role, player_info


class CurrencyTests(unittest.TestCase):
    def test_new_role_receives_all_three_apk_currencies_in_player_info(self):
        role = default_role(Settings())

        message_id, fields = decode_frame(player_info(Settings(), role))
        values = field_values(fields)

        self.assertEqual(message_id, 1006)
        self.assertEqual(
            {
                'immortal_stones': values[50],  # property 49
                'silver': values[51],           # property 50
                'immortal_crystals': values[53],  # property 52
            },
            {
                'immortal_stones': 10_000_000,
                'silver': 10_000_000,
                'immortal_crystals': 10_000_000,
            },
        )
        self.assertEqual(
            [fields[index].type_id for index in (50, 51, 53)],
            [4, 4, 4],
        )

    def test_legacy_role_receives_and_persists_all_three_currencies(self):
        with tempfile.TemporaryDirectory() as directory:
            role_path = Path(directory) / 'roles.json'
            legacy_role = default_role(Settings())
            legacy_role.pop('currencies')
            legacy_role['name'] = '旧档角色'
            original_item_ids = [item['id'] for item in legacy_role['items']]
            role_path.write_text(json.dumps({
                'next_role_id': 10002,
                'accounts': {'legacy': [legacy_role]},
            }, ensure_ascii=False), encoding='utf-8')

            migrated = RoleStore(
                Settings(role_data_file=str(role_path))
            ).roles_for('legacy')[0]

            self.assertEqual(migrated.get('currencies'), {
                'immortal_stones': 10_000_000,
                'silver': 10_000_000,
                'immortal_crystals': 10_000_000,
            })
            self.assertEqual(migrated['name'], '旧档角色')
            self.assertEqual(
                [item['id'] for item in migrated['items']],
                original_item_ids,
            )
            persisted = json.loads(role_path.read_text(encoding='utf-8'))
            self.assertEqual(
                persisted['accounts']['legacy'][0]['currencies'],
                migrated['currencies'],
            )

    def test_additional_created_role_keeps_all_three_currencies_after_reload(self):
        with tempfile.TemporaryDirectory() as directory:
            role_path = Path(directory) / 'roles.json'
            settings = Settings(role_data_file=str(role_path))
            created = RoleStore(settings).create('tester', '第二角色', 6, 1)

            self.assertEqual(created.get('currencies'), {
                'immortal_stones': 10_000_000,
                'silver': 10_000_000,
                'immortal_crystals': 10_000_000,
            })
            reloaded = RoleStore(settings).find('tester', int(created['id']))
            self.assertIsNotNone(reloaded)
            self.assertEqual(reloaded.get('currencies'), created['currencies'])

    def test_partial_currency_data_keeps_existing_balance_and_fills_missing_types(self):
        with tempfile.TemporaryDirectory() as directory:
            role_path = Path(directory) / 'roles.json'
            legacy_role = default_role(Settings())
            legacy_role['currencies'] = {'silver': 123}
            role_path.write_text(json.dumps({
                'next_role_id': 10002,
                'accounts': {'legacy': [legacy_role]},
            }, ensure_ascii=False), encoding='utf-8')

            migrated = RoleStore(
                Settings(role_data_file=str(role_path))
            ).roles_for('legacy')[0]

            self.assertEqual(migrated.get('currencies'), {
                'immortal_stones': 10_000_000,
                'silver': 123,
                'immortal_crystals': 10_000_000,
            })
            reloaded = RoleStore(
                Settings(role_data_file=str(role_path))
            ).roles_for('legacy')[0]
            self.assertEqual(reloaded.get('currencies'), migrated['currencies'])
            _, fields = decode_frame(player_info(Settings(), reloaded))
            values = field_values(fields)
            self.assertEqual(
                [values[index] for index in (50, 51, 53)],
                [10_000_000, 123, 10_000_000],
            )

    def test_invalid_legacy_currency_values_are_repaired_before_login(self):
        invalid_values = ('bad', True, -1, 2_147_483_648)
        expected = {
            'immortal_stones': 10_000_000,
            'silver': 10_000_000,
            'immortal_crystals': 10_000_000,
        }
        for invalid_value in invalid_values:
            with self.subTest(invalid_value=invalid_value):
                with tempfile.TemporaryDirectory() as directory:
                    role_path = Path(directory) / 'roles.json'
                    legacy_role = default_role(Settings())
                    legacy_role['currencies'] = {
                        name: invalid_value
                        for name in expected
                    }
                    role_path.write_text(json.dumps({
                        'next_role_id': 10002,
                        'accounts': {'legacy': [legacy_role]},
                    }, ensure_ascii=False), encoding='utf-8')

                    migrated = RoleStore(
                        Settings(role_data_file=str(role_path))
                    ).roles_for('legacy')[0]

                    self.assertEqual(migrated.get('currencies'), expected)
                    persisted = json.loads(role_path.read_text(encoding='utf-8'))
                    self.assertEqual(
                        persisted['accounts']['legacy'][0]['currencies'],
                        expected,
                    )

    def test_player_info_safely_normalizes_malformed_currency_values(self):
        role = default_role(Settings())
        role['currencies'] = {
            'immortal_stones': 'bad',
            'silver': True,
            'immortal_crystals': 2_147_483_648,
        }

        try:
            message_id, fields = decode_frame(player_info(Settings(), role))
        except (OverflowError, ValueError) as exc:
            self.fail(f'malformed currency prevented login frame: {exc}')
        values = field_values(fields)

        self.assertEqual(message_id, 1006)
        self.assertEqual(
            [values[index] for index in (50, 51, 53)],
            [10_000_000, 10_000_000, 10_000_000],
        )


if __name__ == '__main__':
    unittest.main()
