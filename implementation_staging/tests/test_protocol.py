import inspect
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from map_o import decode_tile_rle
from protocol import GameCipher, binary, byte, decode_frame, encode_frame, field_debug_entries, field_debug_value, field_type_name, field_values, integer, long_integer, short, string
import server as server_module
import test_client as test_client_module
from server import (
    RoleStore,
    Settings,
    character_appearance,
    character_appearance_change_frame,
    character_extension_info,
    character_panel_frames,
    character_skill_list,
    creation_names,
    default_role,
    deletion_result,
    game_server_redirect,
    heartbeat_challenge,
    is_equipment,
    item_description_frame,
    item_detail_frame,
    item_frame,
    login_server_list,
    map_data_frames,
    map_enter_frames,
    map_monster_frame,
    map_object_remove_frame,
    map_object_interaction_values,
    battle_reset_frame,
    battle_actor_debug_snapshot,
    battle_actor_frame,
    battle_actor_frames,
    battle_actor_source_model_for_debug,
    battle_image_resolve_debug,
    battle_resource_resolution,
    format_battle_actor_1048_log,
    format_map_player_appearance_log,
    map_player_appearance_debug,
    battle_actor_update_frame,
    battle_image_frames,
    battle_image_resource,
    battle_resource_frames,
    battle_resource_path,
    battle_start_frame,
    battle_move_frame,
    battle_action_frame,
    battle_action_show_frame,
    battle_end_frame,
    battle_escape_frame,
    is_player_escape_command,
    should_suppress_escape_retrigger,
    battle_progress_frame,
    battle_reward_popup,
    level_experience_required,
    level_up_effect_frame,
    apply_one_level,
    apply_battle_rewards,
    LocalBattleState,
    map_portal_frames,
    map_return_portal_frame,
    map_npc_frame,
    map_npc_frames,
    mount_update_frame,
    menu_prefetch_empty_ack,
    notice_and_world,
    player_info,
    role_items,
    role_list,
    settings_for_role,
    update_role_position,
)


class ProtocolTests(unittest.TestCase):
    def test_round_trip(self):
        frame = encode_frame(1077, [short(2000), byte(53), string('测试'), integer(123), long_integer(456)])
        message_id, fields = decode_frame(frame)
        self.assertEqual(message_id, 1077)
        self.assertEqual(field_values(fields), [2000, 53, '测试', 123, 456])
        self.assertEqual([field.type_id for field in fields], [3, 2, 6, 4, 9])

    def test_game_cipher_matches_apk_and_round_trips(self):
        cipher = GameCipher()
        self.assertEqual(cipher.encrypt(b'\x04'), b'\xf6')

        sender = GameCipher()
        receiver = GameCipher()
        original = encode_frame(1052, [integer(1001), integer(101001)])
        encrypted = sender.encrypt_frame(original)
        self.assertEqual(encrypted[:4], original[:4])
        self.assertEqual(encrypted[4], 0xF6)
        self.assertEqual(receiver.decrypt_frame(encrypted), original)

        server_sender = GameCipher()
        client_receiver = GameCipher()
        server_encrypted = server_sender.encrypt_server_frame(original)
        self.assertNotEqual(server_encrypted[:2], original[:2])
        plain_header = client_receiver.decrypt(server_encrypted[:2])
        plain_body = client_receiver.decrypt(server_encrypted[2:])
        self.assertEqual(plain_header + plain_body, original)

    def test_create_team_builds_the_apk_1026_leader_record(self):
        """Using 1056 or omitting the member record would leave the APK on its no-team page."""
        self.assertTrue(hasattr(server_module, 'LocalTeamState'))
        self.assertTrue(hasattr(server_module, 'team_request_frames'))
        role = default_role(Settings())
        role['sect_id'] = 1
        role['race'] = 2
        state = server_module.LocalTeamState()

        frames = server_module.team_request_frames(role, [0, 10001], state)

        self.assertTrue(state.active)
        self.assertEqual(state.leader_id, 10001)
        self.assertEqual(len(frames), 2)

        status_id, status_fields = decode_frame(frames[0])
        self.assertEqual(status_id, 1017)
        self.assertEqual(field_values(status_fields), [0, 10001, 1, 0, 0x40])
        self.assertEqual([field.type_id for field in status_fields], [2, 4, 4, 2, 4])

        message_id, fields = decode_frame(frames[1])
        self.assertEqual(message_id, 1026)
        self.assertEqual(
            field_values(fields),
            [0, 1, '本地侠客', 10001, 100, 100, 1, 1, 50, 50, 0],
        )
        self.assertEqual(
            [field.type_id for field in fields],
            [2, 2, 6, 4, 4, 4, 2, 4, 4, 4, 4],
        )

    def test_disband_team_clears_state_and_returns_apk_1023_action_11(self):
        """Leaving the team active or returning a byte action would desynchronise the native team UI."""
        role = default_role(Settings())
        state = server_module.LocalTeamState()
        server_module.team_request_frames(role, [0, 10001], state)

        frames = server_module.team_request_frames(role, [11], state)

        self.assertFalse(state.active)
        self.assertEqual(state.leader_id, 0)
        self.assertEqual(len(frames), 2)
        status_id, status_fields = decode_frame(frames[0])
        self.assertEqual(status_id, 1017)
        self.assertEqual(field_values(status_fields), [0, 10001, 1, 0, 0])
        self.assertEqual([field.type_id for field in status_fields], [2, 4, 4, 2, 4])

        message_id, fields = decode_frame(frames[1])
        self.assertEqual(message_id, 1023)
        self.assertEqual(field_values(fields), [11])
        self.assertEqual([field.type_id for field in fields], [3])

    def test_disband_team_is_idempotent_for_a_stale_native_team_page(self):
        """Ignoring a repeated disband would leave the APK waiting on stale client-side state."""
        role = default_role(Settings())
        state = server_module.LocalTeamState()

        frames = server_module.team_request_frames(role, [11], state)

        self.assertFalse(state.active)
        self.assertEqual(len(frames), 2)
        status_id, status_fields = decode_frame(frames[0])
        self.assertEqual(status_id, 1017)
        self.assertEqual(field_values(status_fields), [0, 10001, 1, 0, 0])

        message_id, fields = decode_frame(frames[1])
        self.assertEqual(message_id, 1023)
        self.assertEqual(field_values(fields), [11])
        self.assertEqual([field.type_id for field in fields], [3])

    def test_team_request_builders_preserve_apk_short_and_int_types(self):
        """Changing the native request action or role ID types would break server compatibility."""
        self.assertTrue(hasattr(test_client_module, 'team_create_request'))
        self.assertTrue(hasattr(test_client_module, 'team_disband_request'))

        create_id, create_fields = decode_frame(test_client_module.team_create_request(10001))
        disband_id, disband_fields = decode_frame(test_client_module.team_disband_request())

        self.assertEqual(create_id, 1023)
        self.assertEqual(field_values(create_fields), [0, 10001])
        self.assertEqual([field.type_id for field in create_fields], [3, 4])
        self.assertEqual(disband_id, 1023)
        self.assertEqual(field_values(disband_fields), [11])
        self.assertEqual([field.type_id for field in disband_fields], [3])

    def test_login_server_list(self):
        frame = login_server_list(Settings(advertise_host='192.168.1.8'))
        message_id, fields = decode_frame(frame)
        values = field_values(fields)
        self.assertEqual(message_id, 1077)
        self.assertEqual(values[2], 1)
        self.assertEqual(values[3], '本地一区')
        self.assertEqual(values[4], '192.168.1.8:6805')
        self.assertEqual(values[5], 1)

    def test_redirect_and_role_list(self):
        settings = Settings(advertise_host='192.168.1.8')
        message_id, fields = decode_frame(game_server_redirect(settings, 1001, 101001))
        self.assertEqual(message_id, 1052)
        self.assertEqual(field_values(fields)[:4], [1001, 101001, 6805, '192.168.1.8'])

        message_id, fields = decode_frame(role_list(settings))
        values = field_values(fields)
        self.assertEqual(message_id, 1080)
        self.assertEqual(values[:3], [0, 1, settings.role_id])
        self.assertEqual(values[7], settings.role_name)
        self.assertEqual([fields[0].type_id, fields[1].type_id], [3, 2])

        names_id, names_fields = decode_frame(creation_names())
        self.assertEqual(names_id, 1080)
        self.assertEqual(field_values(names_fields), [4, '云生', '月华'])
        self.assertEqual(names_fields[0].type_id, 3)

        delete_id, delete_fields = decode_frame(deletion_result(10001))
        self.assertEqual(delete_id, 1080)
        self.assertEqual(field_values(delete_fields), [1, 10001])

    def test_heartbeat_challenge(self):
        message_id, fields = decode_frame(heartbeat_challenge(17))
        self.assertEqual(message_id, 1012)
        self.assertEqual(field_values(fields), [17])
        self.assertEqual(fields[0].type_id, 4)

    def test_menu_prefetch_empty_acks_release_client_wait_state(self):
        expected = {1403: 1, 1090: 0, 1153: 0, 1061: 3}
        for protocol_id, subtype in expected.items():
            message_id, fields = decode_frame(menu_prefetch_empty_ack(protocol_id))
            self.assertEqual(message_id, protocol_id)
            self.assertEqual(field_values(fields), [subtype])
            self.assertEqual(fields[0].type_id, 2)

        with self.assertRaises(ValueError):
            menu_prefetch_empty_ack(9999)

    def test_role_store_create_delete_and_persist(self):
        with tempfile.TemporaryDirectory() as directory:
            role_file = str(Path(directory) / 'roles.json')
            settings = Settings(role_data_file=role_file)
            store = RoleStore(settings)
            initial = store.roles_for('tester')
            self.assertEqual(len(initial), 1)
            created = store.create('tester', '新角色', 6, 1)
            self.assertEqual(created['slot'], 1)
            self.assertEqual(created['race'], 1)
            self.assertEqual(created['gender'], 0)
            self.assertEqual(created.get('sect_id'), 0)
            self.assertEqual(created['map_name'], '长安')
            self.assertEqual(len(role_items(created)), 18)
            self.assertEqual(
                {int(item.get('equipment_slot', 0)) for item in role_items(created) if int(item.get('equipment_slot', 0)) > 0},
                set(range(1, 15)) | {17},
            )

            reloaded = RoleStore(settings)
            self.assertEqual(len(reloaded.roles_for('tester')), 2)
            self.assertTrue(reloaded.delete('tester', int(created['id'])))
            self.assertEqual(len(RoleStore(settings).roles_for('tester')), 1)

    def test_mailbox_list_response_matches_apk_1500_contract(self):
        """Changing action 11 field order or types must break the native inbox parser."""
        self.assertTrue(hasattr(server_module, 'mail_request_frames'))
        role = default_role(Settings())
        role['mailbox'] = [{
            'id': 1_000_101,
            'sender': '系统',
            'subject': '欢迎来到本地服',
            'body': '这是一封持久化测试邮件。',
            'sent_at': '2026-09-01',
            'expires_at': '长期有效',
            'read': False,
        }]

        frames, changed = server_module.mail_request_frames(role, [12, 0, 0])

        self.assertFalse(changed)
        self.assertEqual(len(frames), 1)
        message_id, fields = decode_frame(frames[0])
        self.assertEqual(message_id, 1500)
        self.assertEqual(
            field_values(fields),
            [11, 1, 1, 1_000_101, 0, 0, '系统', '欢迎来到本地服', 0, '长期有效'],
        )
        self.assertEqual(
            [field.type_id for field in fields],
            [2, 3, 2, 4, 4, 4, 6, 6, 2, 6],
        )

    def test_opening_mail_returns_action_14_and_marks_it_read(self):
        """Omitting the read transition would make reopened inboxes show stale unread state."""
        self.assertTrue(hasattr(server_module, 'mail_request_frames'))
        role = default_role(Settings())
        message = {
            'id': 1_000_101,
            'sender': '系统',
            'subject': '欢迎来到本地服',
            'body': '这是一封持久化测试邮件。',
            'sent_at': '2026-09-01',
            'expires_at': '长期有效',
            'read': False,
        }
        role['mailbox'] = [message]

        frames, changed = server_module.mail_request_frames(role, [13, 1_000_101])

        self.assertTrue(changed)
        self.assertTrue(message['read'])
        self.assertEqual(len(frames), 1)
        message_id, fields = decode_frame(frames[0])
        self.assertEqual(message_id, 1500)
        self.assertEqual(
            field_values(fields),
            [
                14,
                1_000_101,
                0,
                0,
                0,
                0,
                0,
                '欢迎来到本地服',
                '这是一封持久化测试邮件。',
                '2026-09-01_长期有效',
                0,
            ],
        )
        self.assertEqual(
            [field.type_id for field in fields],
            [2, 4, 4, 2, 4, 3, 3, 6, 6, 6, 2],
        )

    def test_role_store_migrates_and_persists_mail_read_and_delete_state(self):
        """A deleted starter mail must not be recreated when the role file reloads."""
        self.assertTrue(hasattr(server_module, 'mail_request_frames'))
        with tempfile.TemporaryDirectory() as directory:
            role_path = Path(directory) / 'roles.json'
            settings = Settings(role_data_file=str(role_path))
            legacy_role = default_role(settings)
            legacy_role.pop('mailbox', None)
            legacy_role.pop('mailbox_initialized', None)
            role_path.write_text(json.dumps({
                'next_role_id': int(legacy_role['id']) + 1,
                'accounts': {'legacy-mail': [legacy_role]},
            }, ensure_ascii=False), encoding='utf-8')

            store = RoleStore(settings)
            migrated = store.roles_for('legacy-mail')[0]
            self.assertTrue(migrated.get('mailbox_initialized'))
            self.assertEqual(len(migrated.get('mailbox', [])), 1)
            message = migrated['mailbox'][0]
            self.assertEqual(
                (message['sender'], message['subject'], message['read']),
                ('系统', '欢迎来到本地服', False),
            )

            _, read_changed = server_module.mail_request_frames(migrated, [13, int(message['id'])])
            self.assertTrue(read_changed)
            store.save()
            reloaded = RoleStore(settings)
            read_role = reloaded.roles_for('legacy-mail')[0]
            self.assertTrue(read_role['mailbox'][0]['read'])

            frames, delete_changed = server_module.mail_request_frames(
                read_role,
                [16, int(message['id'])],
            )
            self.assertTrue(delete_changed)
            delete_id, delete_fields = decode_frame(frames[0])
            self.assertEqual(delete_id, 1500)
            self.assertEqual(field_values(delete_fields), [16, 0, int(message['id'])])
            self.assertEqual([field.type_id for field in delete_fields], [2, 3, 4])
            reloaded.save()

            after_delete = RoleStore(settings).roles_for('legacy-mail')[0]
            self.assertTrue(after_delete['mailbox_initialized'])
            self.assertEqual(after_delete['mailbox'], [])

    def test_default_role_starts_without_sect(self):
        self.assertEqual(default_role(Settings()).get('sect_id'), 0)

    def test_role_store_migrates_missing_sect_id_and_persists_existing_role(self):
        with tempfile.TemporaryDirectory() as directory:
            role_path = Path(directory) / 'roles.json'
            settings = Settings(role_data_file=str(role_path))
            legacy_role = default_role(settings)
            legacy_role.update({
                'id': 10003,
                'name': '月华',
                'level': 7,
                'map_id': 50000,
                'map_name': '传送测试区',
            })
            legacy_role.pop('sect_id', None)
            role_path.write_text(json.dumps({
                'next_role_id': 10004,
                'accounts': {'legacy': [legacy_role]},
            }, ensure_ascii=False), encoding='utf-8')

            migrated = RoleStore(settings).roles_for('legacy')[0]

            self.assertEqual(migrated.get('sect_id'), 0)
            self.assertEqual(
                (migrated['id'], migrated['name'], migrated['level'], migrated['map_id'], migrated['map_name']),
                (10003, '月华', 7, 50000, '传送测试区'),
            )
            persisted = json.loads(role_path.read_text(encoding='utf-8'))
            self.assertEqual(persisted['accounts']['legacy'][0].get('sect_id'), 0)

    def test_player_info_writes_sect_and_race_to_their_own_wire_properties(self):
        role = default_role(Settings())
        role['sect_id'] = 1
        role['race'] = 2

        message_id, fields = decode_frame(player_info(Settings(), role))
        values = field_values(fields)

        self.assertEqual(message_id, 1006)
        self.assertEqual(values[0], 85)
        self.assertEqual(values[13], 1)  # property 12: sect ID
        self.assertEqual(values[40], 2)  # property 39: race ID

    def test_player_info_normalizes_invalid_sect_id_on_the_wire(self):
        role = default_role(Settings())
        role['sect_id'] = 999
        role['race'] = 2

        message_id, fields = decode_frame(player_info(Settings(), role))

        self.assertEqual(message_id, 1006)
        self.assertEqual(field_values(fields)[13], 0)  # property 12: sect ID

    def test_join_sect_allows_one_valid_initial_membership_only(self):
        join = getattr(server_module, 'join_sect', None)
        self.assertIsNotNone(join)
        role = default_role(Settings())

        self.assertTrue(join(role, 1))
        self.assertEqual(role.get('sect_id'), 1)
        self.assertFalse(join(role, 2))
        self.assertFalse(join(role, 0))
        self.assertFalse(join(role, 999))
        self.assertEqual(role.get('sect_id'), 1)

    def test_item_records_match_original_client_layout(self):
        items = role_items(default_role(Settings()))
        weapon = next(item for item in items if item['name'] == '青锋剑')
        armour = next(item for item in items if item['name'] == '青纹铠甲')
        potion = next(item for item in items if item['name'] == '小还丹')
        mount = next(item for item in items if item['name'] == '辟邪')

        message_id, fields = decode_frame(item_frame(weapon))
        values = field_values(fields)
        self.assertEqual(message_id, 1008)
        self.assertEqual(values[:5], [1, weapon['id'], 1, 1, 50])
        self.assertEqual(values[7:9], [100_001_001, '青锋剑'])
        self.assertEqual(values[12], 2701)
        self.assertEqual(values[14:16], [100, 10])
        self.assertEqual(len(values), 35)
        visible_appearance = {
            1: {'20': 3},
            2: {'16': 23},
            3: {'15': 34},
            5: {'14': 25},
            7: {'19': 3},
            8: {'17': 8},
            9: {'18': 22},
            10: {'7': 270001},
        }
        self.assertEqual(
            {
                int(item['equipment_slot']): item['appearance_properties']
                for item in items
                if 'appearance_properties' in item
            },
            visible_appearance,
        )

        message_id, fields = decode_frame(item_frame(potion))
        values = field_values(fields)
        self.assertEqual(message_id, 1008)
        self.assertEqual(len(values), 16)
        self.assertEqual(values[9:11], [0x40, 0x06])
        self.assertEqual(values[14:16], [150, 1])

        message_id, fields = decode_frame(item_frame(mount))
        values = field_values(fields)
        self.assertEqual(message_id, 1008)
        self.assertEqual(values[:5], [1, mount['id'], 1, 1, 50])
        self.assertEqual(values[7:9], [170_410_004, '辟邪'])
        self.assertEqual(values[14:16], [100, 17])
        self.assertEqual(len(values), 35)
        mount['location'] = 'equipped'
        self.assertEqual(field_values(decode_frame(item_frame(mount, operation=3))[1])[4], 17)
        mount['location'] = 'bag'

        message_id, fields = decode_frame(item_description_frame(armour))
        self.assertEqual(message_id, 1009)
        self.assertEqual(field_values(fields)[:2], [82, armour['id']])

        message_id, fields = decode_frame(item_detail_frame(armour))
        self.assertEqual(message_id, 1032)
        self.assertEqual(field_values(fields)[:3], [1, 30_001_001, 305])

        armour['location'] = 'equipped'
        equipped_values = field_values(decode_frame(item_frame(armour))[1])
        self.assertEqual(equipped_values[4], 3)

        moved_values = field_values(decode_frame(item_frame(armour, operation=3))[1])
        self.assertEqual(moved_values[:5], [3, armour['id'], 1, 1, 3])
        armour['location'] = 'bag'
        moved_back_values = field_values(decode_frame(item_frame(armour, operation=3))[1])
        self.assertEqual(moved_back_values[:5], [3, armour['id'], 1, 1, 50])

    def test_legacy_starter_items_migrate_to_complete_set(self):
        role_id = 10003
        role = {
            'id': role_id,
            'items': [
                {'id': role_id * 100 + 1, 'template_id': 70_000_000, 'name': '新手木剑', 'location': 'equipped'},
                {'id': role_id * 100 + 2, 'template_id': 160_000_003, 'name': '粗布衣', 'location': 'bag'},
                {'id': role_id * 100 + 3, 'template_id': 260_000_001, 'name': '小还丹', 'location': 'bag', 'quantity': 9},
            ],
        }
        self.assertTrue(RoleStore._ensure_items(role))
        migrated = role_items(role)
        self.assertEqual(len(migrated), 18)
        weapon = next(item for item in migrated if item['name'] == '青锋剑')
        potion = next(item for item in migrated if item['name'] == '小还丹')
        self.assertEqual((weapon['location'], weapon['equipment_slot'], weapon['icon_code']), ('equipped', 10, 2701))
        self.assertEqual(potion['quantity'], 9)
        self.assertEqual(
            {int(item.get('equipment_slot', 0)) for item in migrated if is_equipment(item)},
            set(range(1, 15)) | {17},
        )

    def test_player_and_world(self):
        settings = Settings()
        message_id, fields = decode_frame(player_info(settings))
        values = field_values(fields)
        self.assertEqual(message_id, 1006)
        self.assertEqual(values[0], 85)
        self.assertEqual(values[2], settings.role_id)
        self.assertEqual(values[4], settings.role_name)
        self.assertEqual(values[7], settings.role_model)
        self.assertEqual(values[12], 1)
        self.assertEqual(values[41], values[42])
        # Character UI ``dg.o`` reads current/required EXP from properties
        # 31/32. Keep the full login payload populated, not just the panel
        # refresh frame sent when 1039/action=1 is opened.
        self.assertEqual(values[32:34], [0, 100])
        self.assertEqual([fields[32].type_id, fields[33].type_id], [9, 9])
        self.assertEqual(values[43], values[44])
        # Weapon item class 0 is allowed by the starter role's bitmask;
        # without this field the original APK hides the "装备" menu for
        # weapons while armour continues to work.
        self.assertEqual(values[64], 1)
        self.assertEqual(values[23], 0)
        self.assertEqual(values[55], '无')
        self.assertEqual(values[80], '无')
        self.assertEqual(len(values), 87)

        mounted_role = default_role(settings)
        mounted_role['mount_model'] = 105000
        mounted_values = field_values(decode_frame(player_info(settings, mounted_role))[1])
        self.assertEqual(mounted_values[23], 105000)
        mount_id, mount_fields = decode_frame(mount_update_frame(mounted_role))
        self.assertEqual(mount_id, 1017)
        self.assertEqual(field_values(mount_fields), [0, settings.role_id, 1, 22, 105000])

        role = default_role(settings)
        helmet = next(item for item in role_items(role) if item['name'] == '青纹盔')
        helmet['location'] = 'equipped'
        equipped_values = field_values(decode_frame(player_info(settings, role))[1])
        self.assertEqual(equipped_values[21], 3)
        helmet['location'] = 'bag'

        visible_appearance = {
            1: (20, 3),
            2: (16, 23),
            3: (15, 34),
            5: (14, 25),
            7: (19, 3),
            8: (17, 8),
            9: (18, 22),
            10: (7, 270001),
        }
        before = character_appearance(role)
        self.assertEqual(before, {7: 0, 14: 0, 15: 0, 16: 0, 17: 0, 18: 0, 19: 0, 20: 0})
        for item in role_items(role):
            if int(item.get('equipment_slot', 0)) in visible_appearance:
                item['location'] = 'equipped'
        appearance_frame = character_appearance_change_frame(role, before)
        self.assertIsNotNone(appearance_frame)
        appearance_id, appearance_fields = decode_frame(appearance_frame)
        self.assertEqual(appearance_id, 1017)
        self.assertEqual(
            field_values(appearance_fields),
            [0, role['id'], 8, 7, 270001, 14, 25, 15, 34, 16, 23, 17, 8, 18, 22, 19, 3, 20, 3],
        )
        self.assertEqual(
            [field.type_id for field in appearance_fields],
            [2, 4, 4, *(value for _ in range(8) for value in (2, 4))],
        )
        equipped_player = field_values(decode_frame(player_info(settings, role))[1])
        for property_index, value in character_appearance(role).items():
            self.assertEqual(equipped_player[property_index + 1], value)

        before = character_appearance(role)
        for item in role_items(role):
            item['location'] = 'bag'
        restored_frame = character_appearance_change_frame(role, before)
        self.assertIsNotNone(restored_frame)
        _, restored_fields = decode_frame(restored_frame)
        self.assertEqual(
            field_values(restored_fields),
            [0, role['id'], 8, 7, 0, 14, 0, 15, 0, 16, 0, 17, 0, 18, 0, 19, 0, 20, 0],
        )

        extension_id, extension_fields = decode_frame(character_extension_info())
        self.assertEqual(extension_id, 1089)
        self.assertEqual(field_values(extension_fields), [0, 0])
        self.assertEqual([field.type_id for field in extension_fields], [2, 2])

        skill_id, skill_fields = decode_frame(character_skill_list(default_role(settings)))
        skill_values = field_values(skill_fields)
        self.assertEqual(skill_id, 1132)
        self.assertEqual(skill_values[:4], [0, 1, '基础技能', 0])
        self.assertEqual(len(skill_values), 16)
        self.assertEqual(skill_values[4:], [0] * 12)

        attributes, divine = character_panel_frames(default_role(settings))
        attribute_id, attribute_fields = decode_frame(attributes)
        divine_id, divine_fields = decode_frame(divine)
        self.assertEqual(attribute_id, 1039)
        self.assertEqual(divine_id, 1039)
        self.assertEqual(field_values(attribute_fields)[0], 1)
        self.assertEqual(len(field_values(attribute_fields)[1:]), 7)
        self.assertEqual(field_values(divine_fields)[0], 2)
        self.assertEqual(len(field_values(divine_fields)[1:]), 13)

        notice, world = notice_and_world(settings)
        self.assertEqual(decode_frame(notice)[0], 1123)
        world_id, world_fields = decode_frame(world)
        self.assertEqual(world_id, 1110)
        self.assertEqual(field_values(world_fields)[1], 58)

    def test_kunlun_skill_list_encodes_the_visible_probe_record(self):
        """A sect-1 role must receive the documented action-0 skill record."""
        role = default_role(Settings())
        role['sect_id'] = 1

        self.assertEqual(tuple(inspect.signature(character_skill_list).parameters), ('role',))
        message_id, fields = decode_frame(character_skill_list(role))
        values = field_values(fields)

        self.assertEqual(message_id, 1132)
        self.assertEqual(values[:2], [0, 1])
        record = values[2:]
        self.assertEqual(len(record), 14)
        self.assertEqual(record, ['协议测试技能', 10001, 3, 20, 123, 1000, 1, *([0] * 7)])

        other_role = default_role(Settings())
        other_role['sect_id'] = 2
        _, other_fields = decode_frame(character_skill_list(other_role))
        self.assertNotIn('协议测试技能', field_values(other_fields))

    def test_kunlun_sect_skill_list_encodes_the_first_native_slot(self):
        """Protocol 1103 must populate the native sect page's first slot."""
        self.assertTrue(hasattr(server_module, 'sect_skill_list'))
        role = default_role(Settings())
        role['sect_id'] = 1

        message_id, fields = decode_frame(server_module.sect_skill_list(role))
        values = field_values(fields)

        self.assertEqual(message_id, 1103)
        self.assertEqual(values[:2], [0, 1])
        record = values[2:]
        self.assertEqual(len(record), 14)
        self.assertEqual(
            record,
            ['协议测试技能', 10001, 3, 20, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        )
        self.assertEqual([field.type_id for field in fields[:3]], [2, 2, 6])
        self.assertEqual([field.type_id for field in fields[3:]], [4] * 13)

        other_role = default_role(Settings())
        other_role['sect_id'] = 2
        other_id, other_fields = decode_frame(server_module.sect_skill_list(other_role))
        self.assertEqual(other_id, 1103)
        self.assertEqual(field_values(other_fields), [0, 0])

    def test_initial_skill_frames_preload_the_native_sect_container(self):
        """The 1103 container must exist before the native page is constructed."""
        self.assertTrue(hasattr(server_module, 'initial_skill_frames'))
        role = default_role(Settings())
        role['sect_id'] = 1

        frames = server_module.initial_skill_frames(role)

        self.assertEqual([decode_frame(frame)[0] for frame in frames], [1132, 1103])
        self.assertEqual(field_values(decode_frame(frames[1])[1])[:2], [0, 1])

    def test_sect_skill_detail_request_returns_native_learning_conditions(self):
        """1103/action 2 must answer the detail page instead of leaving its wait overlay set."""
        role = default_role(Settings())
        role['sect_id'] = 1

        frame = server_module.sect_skill_detail_frame(role, 10001)

        message_id, fields = decode_frame(frame)
        self.assertEqual(message_id, 1103)
        self.assertEqual(
            field_values(fields),
            [
                2,
                10001,
                3,
                1,
                0,
                0,
                0,
                0,
                '本地测试技能效果：用于验证技能学习与升级。',
                '协议测试技能说明',
                '下一级效果：技能等级提高。',
                0,
                '',
                0,
            ],
        )
        self.assertEqual(
            [field.type_id for field in fields],
            [2, 4, 4, 4, 4, 4, 4, 4, 6, 6, 6, 4, 6, 4],
        )

    def test_sect_skill_learn_request_records_level_and_refreshes_both_containers(self):
        """1103/action 3 must change role state and return frames that release and refresh the UI."""
        role = default_role(Settings())
        role['sect_id'] = 1

        frames = server_module.sect_skill_request_frames(role, [3, 10001])

        self.assertEqual(role['skill_levels'], {'10001': 4})
        self.assertEqual([decode_frame(frame)[0] for frame in frames], [1103, 1103, 1132])
        list_values = field_values(decode_frame(frames[0])[1])
        self.assertEqual(list_values[:5], [0, 1, '协议测试技能', 10001, 4])
        self.assertEqual(field_values(decode_frame(frames[1])[1]), [5])
        character_values = field_values(decode_frame(frames[2])[1])
        self.assertEqual(character_values[:5], [0, 1, '协议测试技能', 10001, 4])

    def test_server_skill_transition_is_saved_and_survives_role_store_reload(self):
        """The network transition boundary must persist the upgraded level, not only mutate memory."""
        with tempfile.TemporaryDirectory() as temporary:
            role_path = Path(temporary) / 'roles.json'
            settings = Settings(role_data_file=str(role_path))
            game_server = server_module.LocalGameServer(settings)
            role = game_server.roles.roles_for('skill-persistence')[0]
            role['sect_id'] = 1
            game_server.roles.save()

            frames = game_server.handle_sect_skill_request(role, [3, 10001])

            self.assertEqual([decode_frame(frame)[0] for frame in frames], [1103, 1103, 1132])
            reloaded = RoleStore(settings).find('skill-persistence', int(role['id']))
            self.assertIsNotNone(reloaded)
            self.assertEqual(reloaded['skill_levels'], {'10001': 4})

    def test_sect_skill_level_normalizes_legacy_values_and_stops_at_maximum(self):
        """Legacy values are wire-safe and action 3 never advances beyond level 20."""
        role = default_role(Settings())
        role['sect_id'] = 1
        self.assertEqual(server_module.sect_skill_level(role), 3)
        for raw, expected in [('bad', 3), (-5, 0), (99, 20)]:
            role['skill_levels'] = {'10001': raw}
            self.assertEqual(server_module.sect_skill_level(role), expected)

        role['skill_levels'] = {'10001': 20}
        frames = server_module.sect_skill_request_frames(role, [3, 10001])
        self.assertEqual(role['skill_levels'], {'10001': 20})
        self.assertEqual(field_values(decode_frame(frames[0])[1])[:5], [0, 1, '协议测试技能', 10001, 20])

    def test_invalid_sect_skill_learn_still_acknowledges_without_mutating_role(self):
        """A stale skill id must clear the native wait flag without inventing role state."""
        role = default_role(Settings())
        role['sect_id'] = 1

        frames = server_module.sect_skill_request_frames(role, [3, 99999])

        self.assertNotIn('skill_levels', role)
        self.assertEqual(len(frames), 1)
        self.assertEqual(field_values(decode_frame(frames[0])[1]), [3])

    def test_map_flow(self):
        settings = Settings()
        changan = server_module.settings_for_map(settings, 58)
        frames = map_data_frames(changan)
        self.assertEqual([decode_frame(x)[0] for x in frames], [1010, 1407, 1407, 1407, 1407, 1407, 1010])
        header_values = field_values(decode_frame(frames[1])[1])
        tile_values = field_values(decode_frame(frames[3])[1])
        self.assertEqual(
            len(decode_tile_rle(tile_values[2], header_values[2] * header_values[3])),
            header_values[2] * header_values[3],
        )
        final_values = field_values(decode_frame(frames[-1])[1])
        self.assertEqual(final_values[4:], [1, 12])
        self.assertEqual(decode_frame(frames[-1])[1][5].type_id, 3)

        enter_frames = map_enter_frames(changan)
        enter_actions = [field_values(decode_frame(x)[1])[5] for x in enter_frames[:3]]
        self.assertEqual(enter_actions, [13, 14, 105])
        monster_id, monster_fields = decode_frame(enter_frames[3])
        self.assertEqual(monster_id, 1126)
        self.assertEqual(field_values(monster_fields), [0, 1, changan.monster.id, 9, 28, -2_004_250, '试炼妖兽'])
        self.assertEqual([field.type_id for field in monster_fields], [2, 2, 4, 4, 4, 4, 6])
        self.assertGreaterEqual(changan.monster.id, 1_000_000)

        standalone_id, standalone_fields = decode_frame(map_monster_frame(changan))
        self.assertEqual(standalone_id, 1126)
        self.assertEqual(field_values(standalone_fields)[2], changan.monster.id)

        remove_id, remove_fields = decode_frame(map_object_remove_frame(changan.monster.id))
        self.assertEqual(remove_id, 1010)
        self.assertEqual(field_values(remove_fields), [changan.monster.id, 0, 0, 0, 0, 18])
        self.assertEqual([field.type_id for field in remove_fields], [4, 3, 3, 4, 4, 3])

    def test_current_map_definition_drives_battle_monster(self):
        settings = Settings()
        changan = server_module.settings_for_map(settings, 58)
        role = default_role(settings)

        _, monster_fields = decode_frame(battle_actor_frames(role, changan)[1])
        values = field_values(monster_fields)

        self.assertEqual(values[0], -2_004_251)
        self.assertEqual(values[6], '试炼妖兽')
        self.assertEqual(values[9], 1_900_001)

    def test_map_object_interaction_2031_layout(self):
        object_id, object_x, object_y, action = map_object_interaction_values(
            [900001, 0, 10, 6, 6, 0]
        )
        self.assertEqual((object_id, object_x, object_y, action), (900001, 10, 6, 6))
        self.assertEqual(map_object_interaction_values([580001]), (580001, None, None, None))

    def test_local_battle_encounter_reset_rearms_monster(self):
        state = LocalBattleState(monster_defeated=True)
        state.reset_encounter()
        self.assertFalse(state.active)
        self.assertFalse(state.monster_defeated)

    def test_battle_progress_uses_incremental_character_update(self):
        role = default_role(Settings())
        role['level'] = 4
        role['experience'] = 75
        message_id, fields = decode_frame(battle_progress_frame(role))
        self.assertEqual(message_id, 1017)
        values = field_values(fields)
        self.assertEqual(values[:3], [0, role['id'], 15])
        properties = dict(zip(values[3::2], values[4::2]))
        self.assertEqual(properties[11], 4)
        self.assertEqual(properties[31], 75)
        self.assertEqual(properties[32], 400)
        self.assertEqual(properties[80], 4)
        self.assertEqual(properties[85], 0)
        self.assertEqual(properties[86], 0)
        self.assertTrue(all(fields[index].type_id == 2 for index in range(3, len(fields), 2)))
        self.assertTrue(all(fields[index].type_id == 4 for index in range(4, len(fields), 2)))

    def test_battle_reward_popup_uses_native_top_reward_overlay(self):
        item = {'name': '小还丹', 'quantity_gained': 1}
        message_id, fields = decode_frame(battle_reward_popup(50, item))
        self.assertEqual(message_id, 1049)
        self.assertEqual(field_values(fields), [3, 50, 0, 0, 0, 'x'])
        self.assertEqual([field.type_id for field in fields], [2, 4, 4, 4, 4, 6])

    def test_level_up_effect_matches_apk_twelve_integer_layout(self):
        role = default_role(Settings())
        role['level'] = 2
        message_id, fields = decode_frame(level_up_effect_frame(role))
        self.assertEqual(message_id, 1129)
        self.assertEqual(len(fields), 12)
        self.assertEqual([field.type_id for field in fields], [4] * 12)
        self.assertEqual(field_values(fields)[0:5], [role['id'], 2, 5, 11, 6])

    def test_manual_level_consumes_experience_and_grows_stats(self):
        role = default_role(Settings())
        role['experience'] = level_experience_required(1)
        before_stats = list(role['stats'])
        self.assertTrue(apply_one_level(role))
        self.assertEqual((role['level'], role['experience']), (2, 0))
        self.assertEqual(list(role['stats'])[:5], [value + 1 for value in before_stats[:5]])
        self.assertFalse(apply_one_level(role))

    def test_battle_reset_frame_uses_verified_action_zero(self):
        message_id, fields = decode_frame(battle_reset_frame())
        self.assertEqual(message_id, 1040)
        self.assertEqual(field_values(fields), [0])
        self.assertEqual([field.type_id for field in fields], [2])

    def test_local_battle_frames_match_apk_dispatch_types(self):
        role = default_role(Settings())
        start_id, start_fields = decode_frame(battle_start_frame(role, Settings()))
        self.assertEqual(start_id, 1040)
        self.assertEqual([field.type_id for field in start_fields], [2, 4, 2, 4, 3, 6, 3, 6, 2])
        self.assertEqual(field_values(start_fields)[:4], [1, 1, 0, 30])

        state = LocalBattleState()
        state.begin(int(role['id']), Settings().monster_id)
        move_id, move_fields = decode_frame(battle_move_frame(state))
        self.assertEqual(move_id, 1042)
        self.assertEqual(field_values(move_fields)[:4], [1, role['id'], Settings().monster_id, 1])
        self.assertEqual(field_values(move_fields)[9], 0)
        action_id, action_fields = decode_frame(battle_action_frame(state))
        self.assertEqual(action_id, 1042)
        self.assertEqual(
            [field.type_id for field in action_fields],
            [4, 4, 4, 2, 2, 2, 4, 4, 6, 4, 4, 4, 4, 4, 6],
        )
        self.assertEqual(field_values(action_fields)[:3], [1, role['id'], Settings().monster_id])
        self.assertEqual(field_values(action_fields)[3:6], [1, 1, 0])
        self.assertEqual(field_values(action_fields)[9:], [1, Settings().monster_id, 0, 22, -10, ''])

        show_id, show_fields = decode_frame(battle_action_show_frame(state))
        self.assertEqual(show_id, 1040)
        self.assertEqual([field.type_id for field in show_fields], [2, 4, 2, 4, 3, 6, 3, 6, 2])
        shown_id, shown_fields = decode_frame(battle_action_show_frame(state, 1))
        self.assertEqual(shown_id, 1040)
        self.assertEqual(field_values(shown_fields)[:2], [2, 1])
        end_id, end_fields = decode_frame(battle_end_frame())
        self.assertEqual((end_id, field_values(end_fields)), (1040, [4]))

    def test_battle_actor_frames_preserve_structure_and_runtime_identity(self):
        settings = Settings(monster_id=1_900_123, monster_name='动态妖兽')
        field_types = [4, 4, 4, 4, 4, 4, 6, 3, 4, 4, 4, 4, 4, 4, 4, 3, 4, 4, 4, 4, 4, 3]

        for role_id, role_name in ((10031, '动态角色甲'), (10072, '动态角色乙')):
            with self.subTest(role_id=role_id, role_name=role_name):
                role = default_role(settings)
                role['id'] = role_id
                role['name'] = role_name
                frames = battle_actor_frames(role, settings)

                self.assertEqual(len(frames), 2)
                player_id, player_fields = decode_frame(frames[0])
                monster_id, monster_fields = decode_frame(frames[1])
                self.assertEqual((player_id, monster_id), (1048, 1048))
                self.assertEqual((len(player_fields), len(monster_fields)), (22, 22))
                self.assertEqual([field.type_id for field in player_fields], field_types)
                self.assertEqual([field.type_id for field in monster_fields], field_types)

                player_values = field_values(player_fields)
                monster_values = field_values(monster_fields)
                self.assertEqual(player_values[6], role_name)
                self.assertEqual(player_values[9], role_id)
                self.assertEqual(monster_values[6], settings.monster_name)
                self.assertEqual(monster_values[9], settings.monster_id)

        # A full 1048 refresh remains available for resync/reconnect paths,
        # while normal combat HP is changed by the type-22 effect in 1042.
        state = LocalBattleState()
        state.begin(int(role['id']), settings.monster_id)
        state.monster_hp = 90
        update_id, update_fields = decode_frame(
            battle_actor_update_frame(role, settings, state, state.monster_id)
        )
        self.assertEqual(update_id, 1048)
        self.assertEqual(field_values(update_fields)[3], 90)
        self.assertEqual(field_values(update_fields)[10:12], [90, 100])

    def test_battle_resource_response_is_two_chunk_1503(self):
        path = battle_resource_path(Settings().monster_model)
        self.assertIsNotNone(path)
        frames = battle_resource_frames(Settings().monster_model)
        self.assertEqual(len(frames), 2)
        first_id, first_fields = decode_frame(frames[0])
        last_id, last_fields = decode_frame(frames[1])
        self.assertEqual((first_id, last_id), (1503, 1503))
        self.assertEqual([field.type_id for field in first_fields[:4]], [2, 4, 3, 3])
        self.assertEqual(field_values(first_fields)[:3], [0, Settings().monster_model, path.stat().st_size])
        self.assertEqual(field_values(last_fields)[0], 2)
        self.assertEqual(field_values(last_fields)[2:4], [path.stat().st_size, 0])

        player_path = battle_resource_path(6)
        self.assertIsNotNone(player_path)
        self.assertEqual(player_path.name, '100000.dat')

        # Model 0 is translated to the bundled attack/effect role resource
        # (2100000.dat), which the client requests before rendering an attack.
        effect_path = battle_resource_path(0)
        self.assertIsNotNone(effect_path)
        effect_frames = battle_resource_frames(0)
        self.assertEqual(len(effect_frames), 2)
        effect_id, effect_fields = decode_frame(effect_frames[0])
        self.assertEqual(effect_id, 1503)
        self.assertEqual(field_values(effect_fields)[:3], [0, 0, effect_path.stat().st_size])

    def test_battle_image_response_uses_1501_and_role_cache(self):
        # The monster role asks for this directional variant while images.o
        # stores its payload under base id 5860004.
        resource = battle_image_resource(5_860_104)
        self.assertIsNotNone(resource)
        self.assertEqual(resource[:4], (69, 69, 8, 14))
        self.assertEqual(resource[7:9], (30, 1044))
        self.assertEqual(len(resource[9]), 1074)

        frames = battle_image_frames(2, 5_860_104)
        self.assertEqual(len(frames), 3)
        first_id, first_fields = decode_frame(frames[0])
        last_id, last_fields = decode_frame(frames[1])
        redraw_id, redraw_fields = decode_frame(frames[2])
        first_values = field_values(first_fields)
        last_values = field_values(last_fields)
        self.assertEqual((first_id, last_id), (1501, 1501))
        self.assertEqual(
            [field.type_id for field in first_fields],
            [4, 4, 2, 2, 4, 3, 3, 2, 2, 3, 3, 4, 4, 4, 3, 7],
        )
        self.assertEqual(first_values[:11], [1, 1074, 0, 0, 5_860_104, 69, 69, 8, 14, 30, 1044])
        self.assertEqual(len(first_values[15]), 1074)
        self.assertEqual(last_values[3], 2)
        self.assertEqual(last_values[14:16], [0, b''])
        self.assertEqual((redraw_id, redraw_fields), (1502, []))

    def test_battle_image_response_falls_back_to_original_jar(self):
        attack = battle_image_resource(2_100_000)
        weapon_attack = battle_image_resource(2_040_000)
        player = battle_image_resource(2_110_000)
        map_player = battle_image_resource(2_270_000)
        self.assertIsNotNone(attack)
        self.assertEqual(attack[:4], (99, 48, 8, 63))
        self.assertEqual(attack[7:9], (128, 2352))
        self.assertIsNotNone(weapon_attack)
        self.assertEqual(weapon_attack[:4], (59, 32, 8, 19))
        self.assertEqual(weapon_attack[7:9], (40, 472))
        self.assertIsNotNone(player)
        self.assertIsNotNone(map_player)
        self.assertEqual(player[:4], (157, 108, 8, 63))
        self.assertEqual(player[7:9], (128, 4627))
        self.assertEqual(len(player[9]), 4755)
        self.assertEqual(map_player[:4], (27, 36, 8, 9))
        self.assertEqual(map_player[7:9], (20, 213))

        frames = battle_image_frames(2, 2_110_000)
        first_id, first_fields = decode_frame(frames[0])
        self.assertEqual(first_id, 1501)
        self.assertEqual(field_values(first_fields)[:11], [1, 4755, 0, 0, 2_110_000, 157, 108, 8, 63, 128, 4627])

    def test_local_battle_state_attack_and_finish(self):
        state = LocalBattleState()
        state.begin(10001, 900001)
        self.assertEqual(state.trace_id, 'BT-10001-900001-1')
        self.assertFalse(state.apply_basic_attack(40))
        # Damage application no longer advances the protocol round.  The APK
        # supplies that round in 1041 and advances it after the matching
        # 1040/action=2 acknowledgement.
        self.assertEqual((state.round, state.monster_hp), (1, 60))
        self.assertTrue(state.apply_basic_attack(60))
        self.assertTrue(state.active)
        state.finish()
        self.assertFalse(state.active)

    def test_character_panel_stats_drive_battle_hp_attack_and_defence(self):
        """Removing the role-derived formulas must change observable combat state."""
        self.assertTrue(hasattr(server_module, 'combat_stats'))
        role = default_role(Settings())
        role['level'] = 3
        role['stats'] = [4, 6, 0, 0, 0, 0, 0, 0]

        stats = server_module.combat_stats(role)
        self.assertEqual(
            (stats.max_hp, stats.physical_attack, stats.physical_defence),
            (126, 18, 8),
        )

        state = LocalBattleState()
        state.begin(10001, 900001, player_stats=stats)
        self.assertEqual((state.player_hp, state.player_max_hp), (126, 126))
        self.assertEqual(state.player_basic_attack_damage(), 18)
        self.assertEqual(state.monster_basic_attack_damage(), 6)
        self.assertEqual(state.monster_basic_attack_damage(defending=True), 3)

    def test_attack_round_uses_panel_damage_in_state_and_wire_effects(self):
        """A fixed -10 effect would desynchronise the client from derived combat HP."""
        self.assertTrue(hasattr(server_module, 'battle_round_action_frames'))
        role = default_role(Settings())
        role['level'] = 3
        role['stats'] = [4, 6, 0, 0, 0, 0, 0, 0]
        state = LocalBattleState()
        state.begin(10001, 900001, player_stats=server_module.combat_stats(role))

        frames, monster_defeated = server_module.battle_round_action_frames(state, 1, 1)

        self.assertFalse(monster_defeated)
        self.assertEqual((state.monster_hp, state.player_hp), (82, 120))
        self.assertEqual(len(frames), 2)
        player_effect = field_values(decode_frame(frames[0])[1])
        monster_effect = field_values(decode_frame(frames[1])[1])
        self.assertEqual(player_effect[3:5], [1, 1])
        self.assertEqual(player_effect[12:14], [22, -18])
        self.assertEqual(monster_effect[12:14], [22, -6])

    def test_defence_round_skips_player_attack_and_halves_incoming_damage(self):
        """Command 2 must not fall through to the ordinary-attack branch."""
        self.assertTrue(hasattr(server_module, 'battle_round_action_frames'))
        role = default_role(Settings())
        role['level'] = 3
        role['stats'] = [4, 6, 0, 0, 0, 0, 0, 0]
        state = LocalBattleState()
        state.begin(10001, 900001, player_stats=server_module.combat_stats(role))

        frames, monster_defeated = server_module.battle_round_action_frames(state, 2, 1)

        self.assertFalse(monster_defeated)
        self.assertEqual((state.monster_hp, state.player_hp), (100, 123))
        self.assertEqual(len(frames), 2)
        defend_values = field_values(decode_frame(frames[0])[1])
        counter_values = field_values(decode_frame(frames[1])[1])
        self.assertEqual(defend_values[1:5], [10001, 10001, 2, 1])
        self.assertEqual(defend_values[9], 0)
        self.assertEqual(counter_values[12:14], [22, -3])

    def test_initial_battle_actor_uses_character_panel_max_hp(self):
        """The first 1048 actor packet must not reset a derived player HP to 100."""
        self.assertTrue(hasattr(server_module, 'combat_stats'))
        role = default_role(Settings())
        role['level'] = 3
        role['stats'] = [4, 6, 0, 0, 0, 0, 0, 0]
        state = LocalBattleState()
        state.begin(10001, Settings().monster_id, player_stats=server_module.combat_stats(role))

        player_frame = battle_actor_frames(role, Settings(), state=state)[0]
        values = field_values(decode_frame(player_frame)[1])

        self.assertEqual(values[3], 126)
        self.assertEqual(values[10:12], [126, 126])

    def test_battle_escape_frame_layout(self):
        message_id, fields = decode_frame(battle_escape_frame(10003))
        self.assertEqual(message_id, 1041)
        self.assertEqual(field_values(fields), [10, 10003])
        # The APK reads both fields with c(I) (int), matching La/c/m.
        self.assertEqual([field.type_id for field in fields], [4, 4])

    def test_battle_escape_is_distinct_from_victory_settlement(self):
        player_id = 10003
        escape = battle_escape_frame(player_id)
        _, escape_fields = decode_frame(escape)
        self.assertEqual(field_values(escape_fields), [10, player_id])
        # No battle-end settlement and no monster removal are part of an escape.
        self.assertNotEqual(decode_frame(escape)[0], decode_frame(battle_end_frame())[0])
        removal_id, removal_fields = decode_frame(map_object_remove_frame(1900001))
        self.assertEqual((removal_id, field_values(removal_fields)[0]), (1010, 1900001))
        self.assertNotEqual(escape, battle_end_frame())
        self.assertNotEqual(escape, map_object_remove_frame(1900001))

    def test_battle_escape_leaves_hp_and_monster_state_untouched(self):
        state = LocalBattleState()
        state.begin(10001, 900001)
        state.map_id = 58
        state.player_tile = (9, 28)
        full_monster_hp = state.monster_hp
        full_player_hp = state.player_hp
        # Escape mirrors a clean finish(): no attack HRP/no counterattack and
        # the monster remains on the map so the player can re-engage it.
        self.assertTrue(state.escape())
        self.assertFalse(state.active)
        self.assertEqual(state.phase, 'idle')
        self.assertFalse(state.monster_defeated)
        self.assertEqual(state.monster_hp, full_monster_hp)
        self.assertEqual(state.player_hp, full_player_hp)

    def test_c2s_escape_command_is_6(self):
        # The APK's 逃跑 branch sends C->S 1041 command 6 (E(6)). This is the
        # player escape request and must be recognized by the server. The full
        # device frame is [6, round, player_id, side=1, 0,0,0,0].
        self.assertTrue(is_player_escape_command(6))

    def test_c2s_command_10_is_not_player_escape(self):
        # C->S 1041 command 10 is 退出观战 (quit spectator) via h.b/c_(1), NOT a
        # player escape request. It must never take the player-escape branch.
        self.assertFalse(is_player_escape_command(10))

    def test_escape_response_is_single_1041_without_victory_frames(self):
        # The server immediately hands departure and closure to the APK with
        # one 1041 [10, player_id] frame. It must NOT carry any victory-settle
        # frame: no 1040/action=4, no 1010/action=18 monster removal, and no
        # reward/EXP frame (1049/1129 settle overlay).
        escape = battle_escape_frame(10003)
        self.assertEqual(decode_frame(escape)[0], 1041)
        self.assertEqual(field_values(decode_frame(escape)[1]), [10, 10003])
        # Not the battle-close frame nor the reward overlay.
        self.assertNotEqual(decode_frame(escape)[0], decode_frame(battle_end_frame())[0])
        # Not the monster-removal frame.
        removal = map_object_remove_frame(1900001)
        self.assertNotEqual(decode_frame(escape)[0], decode_frame(removal)[0])
        self.assertNotEqual(field_values(decode_frame(escape)[1]), field_values(decode_frame(removal)[1]))

    def test_escape_state_cleanup_matches_victory_but_keeps_monster(self):
        # Both victory and escape finish the battle (active=False, phase=idle),
        # but escape must leave monster_defeated=False and keep HP untouched,
        # whereas victory sets monster_defeated=True.
        escaped = LocalBattleState()
        escaped.begin(10001, 1900001)
        escaped.map_id = 58
        escaped.player_tile = (9, 28)
        self.assertTrue(escaped.escape())
        self.assertFalse(escaped.active)
        self.assertEqual(escaped.phase, 'idle')
        self.assertFalse(escaped.monster_defeated)
        self.assertEqual(escaped.monster_hp, 100)
        self.assertEqual(escaped.player_hp, 100)

        won = LocalBattleState()
        won.begin(10001, 1900001)
        won.apply_basic_attack(100)
        won.finish()
        won.monster_defeated = True
        self.assertFalse(won.active)
        self.assertTrue(won.monster_defeated)

    def test_escape_guard_suppresses_same_monster_same_map(self):
        guard = {'map_id': 58, 'monster_id': 1900001, 'player_id': 10001, 'origin': (9, 28)}
        self.assertTrue(should_suppress_escape_retrigger(guard, 58, 1900001))

    def test_escape_guard_suppresses_even_without_tile(self):
        # The real client's immediate re-tap (1010/7) carries no tile; the
        # guard must suppress on (map_id, monster_id) alone, exactly like a
        # guard armed with an unknown origin.
        guard = {'map_id': 58, 'monster_id': 1900001, 'player_id': 10001, 'origin': None}
        self.assertTrue(should_suppress_escape_retrigger(guard, 58, 1900001))

    def test_escape_guard_does_not_lock_other_monster_other_map(self):
        guard = {'map_id': 58, 'monster_id': 1900001, 'player_id': 10001, 'origin': (9, 28)}
        # A different monster is never suppressed by monster A's guard.
        self.assertFalse(should_suppress_escape_retrigger(guard, 58, 1999999))
        # A different map is never suppressed.
        self.assertFalse(should_suppress_escape_retrigger(guard, 50000, 1900001))
        # No guard means never suppress, so the monster can always be fought.
        self.assertFalse(should_suppress_escape_retrigger(None, 58, 1900001))

    def test_escape_guard_released_only_by_real_movement(self):
        # A guard armed with a known origin is released only when a 1005 move
        # lands on a different tile; a repeated same-tile report does NOT clear it.
        state = LocalBattleState()
        state.begin(10001, 1900001)
        state.map_id = 58
        state.player_tile = (9, 28)
        state.set_escape_guard(58, 1900001, 10001, (9, 28))
        self.assertIsNotNone(state.escape_guard)
        self.assertEqual(state.escape_guard['origin'], (9, 28))
        self.assertEqual(state.escape_guard.get('tile', 'missing'), 'missing')
        # Simulate a 1005 report of the SAME coordinates (no real move): still guarded.
        state.player_tile = (9, 28)
        self.assertIsNotNone(state.escape_guard)
        # A genuine move to a new tile releases the guard.
        state.player_tile = (9, 30)
        state.clear_escape_guard()
        self.assertIsNone(state.escape_guard)

    def test_escape_guard_origin_established_lazily(self):
        # Guard may be armed with no known position (origin None); suppression
        # still applies until the first 1005 establishes a reference tile, and
        # only a later move off that reference releases it.
        state = LocalBattleState()
        state.map_id = 58
        state.set_escape_guard(58, 1900001, 10001, None)
        self.assertIsNotNone(state.escape_guard)
        self.assertTrue(should_suppress_escape_retrigger(state.escape_guard, 58, 1900001))
        # First 1005 establishes the reference without clearing.
        state.player_tile = (8, 6)
        if state.escape_guard['origin'] is None:
            state.escape_guard['origin'] = state.player_tile
        self.assertEqual(state.escape_guard['origin'], (8, 6))
        # Moving off the reference must clear the guard.
        state.player_tile = (9, 6)
        state.clear_escape_guard()
        self.assertIsNone(state.escape_guard)

    def test_escape_guard_cleared_by_new_battle(self):
        # A new battle (begin) resets the guard so a re-approach always works.
        state = LocalBattleState()
        state.map_id = 58
        state.set_escape_guard(58, 1900001, 10001, (9, 28))
        self.assertTrue(state.escape_guard is not None)
        state.begin(10001, 1900001)
        self.assertIsNone(state.escape_guard)

    def test_escape_guard_cleared_by_map_reload(self):
        state = LocalBattleState()
        state.set_escape_guard(58, 1900001, 10001, (9, 28))
        self.assertTrue(state.escape_guard is not None)
        state.reset_encounter()
        self.assertIsNone(state.escape_guard)

    def test_battle_rewards_persist_experience_and_drop(self):
        role = default_role(Settings())
        before = next(item for item in role_items(role) if int(item['template_id']) == 260_000_001)
        before_quantity = int(before['quantity'])
        item, level_up = apply_battle_rewards(role)
        self.assertFalse(level_up)
        self.assertEqual(int(role['experience']), 50)
        self.assertEqual(int(role['level']), 1)
        self.assertEqual(int(item['quantity']), before_quantity + 1)
        self.assertEqual(int(item['template_id']), 260_000_001)

        # A second victory crosses the level threshold and carries the
        # remainder into the next level's EXP bar.
        item, level_up = apply_battle_rewards(role)
        self.assertTrue(level_up)
        self.assertEqual((int(role['level']), int(role['experience'])), (2, 0))

        manual_role = default_role(Settings())
        manual_role['auto_level'] = False
        apply_battle_rewards(manual_role, 100)
        self.assertEqual((manual_role['level'], manual_role['experience']), (1, 100))

    def test_portal_actor_and_target_map_use_bundled_ref(self):
        settings = Settings()
        changan = server_module.settings_for_map(settings, 58)
        self.assertEqual(settings.portal_target_map_o_file, 'maps/50000.map.o')
        portal_id, portal_fields = decode_frame(map_portal_frames(changan)[0])
        self.assertEqual(portal_id, 1126)
        self.assertEqual(field_values(portal_fields)[0:5], [0, 1, 580001, 55, 55])
        target = server_module.settings_for_map(settings, 50000)
        self.assertEqual((target.monster.x, target.monster.y), (12, 8))
        self.assertEqual([portal.id for portal in target.portals], [580002])
        entered = map_enter_frames(target)
        self.assertEqual(field_values(decode_frame(entered[0])[1])[4:], [0, 13])
        self.assertEqual(field_values(decode_frame(entered[-1])[1])[2], 580002)

    def test_forward_portals_spawn_all_entries_on_origin_map(self):
        settings = Settings()
        changan = server_module.settings_for_map(settings, 58)
        frames = map_portal_frames(changan)
        self.assertEqual(len(frames), 3)
        ids = [field_values(decode_frame(f)[1])[2] for f in frames]
        self.assertEqual(ids, [580001, 580003, 580005])
        self.assertEqual(field_values(decode_frame(frames[1])[1])[3:5], [34, 7])
        self.assertEqual(field_values(decode_frame(frames[2])[1])[3:5], [62, 67])
        entered = map_enter_frames(changan)
        self.assertEqual(field_values(decode_frame(entered[4])[1])[2], 580001)
        self.assertEqual(field_values(decode_frame(entered[5])[1])[2], 580003)
        self.assertEqual(field_values(decode_frame(entered[6])[1])[2], 580005)

    def test_npc_actor_spawns_only_on_map_58(self):
        settings = Settings()
        changan = server_module.settings_for_map(settings, 58)
        frames = map_npc_frames(changan)
        self.assertEqual(len(frames), 3)
        ids = [field_values(decode_frame(f)[1]) for f in frames]
        self.assertEqual(ids[0][0:3], [1_900_002, 50, 64])
        self.assertEqual(ids[0][6], '孙思邈')
        self.assertEqual(ids[1][0:3], [1_900_003, 34, 50])
        self.assertEqual(ids[2][0:3], [1_900_004, 11, 21])
        on_58 = map_enter_frames(changan)
        self.assertTrue(all(f in on_58 for f in frames))
        off_map = map_enter_frames(server_module.settings_for_map(settings, 50000))
        self.assertFalse(any(f in off_map for f in frames))

    def test_sect_skill_screen_frame_places_screen_and_mode_in_apk_read_indices(self):
        build_frame = getattr(server_module, 'sect_skill_screen_frame', None)
        self.assertIsNotNone(build_frame, 'sect mentor screen frame is missing')

        message_id, fields = decode_frame(build_frame())

        self.assertEqual(message_id, 1010)
        self.assertEqual([field.type_id for field in fields], [4, 3, 3, 4, 4, 3])
        self.assertEqual(field_values(fields), [0, 0, 0, 1, 179, 69])

    def test_kunlun_mentor_dialogue_exposes_learning_only_to_kunlun_role(self):
        settings = Settings(map_registry=server_module.default_map_registry())
        kunlun = server_module.settings_for_map(settings, 60001)
        mentor = kunlun.npcs[0]
        kunlun_role = default_role(settings)
        kunlun_role['sect_id'] = 1

        enter_action = field_values(decode_frame(map_enter_frames(kunlun)[0])[1])
        self.assertEqual(enter_action[4:], [0, 13])

        message_id, fields = decode_frame(server_module.map_npc_dialogue_frames(mentor, kunlun_role)[0])
        values = field_values(fields)

        self.assertEqual(message_id, 2032)
        self.assertEqual(values[:2], [1900101, 4])
        self.assertEqual(values[14:17], [1, 2, '学习门派技能'])
        self.assertEqual(values[22:25], [0, 2, '结束对话'])
        self.assertEqual(values[31], 100)

        outsider = default_role(settings)
        outsider['sect_id'] = 2
        _, outsider_fields = decode_frame(server_module.map_npc_dialogue_frames(mentor, outsider)[0])
        outsider_values = field_values(outsider_fields)
        self.assertEqual(outsider_values[:2], [1900101, 3])
        self.assertEqual(outsider_values[8], '仅限昆仑弟子学习。')
        self.assertNotIn('学习门派技能', outsider_values)

        ordinary = server_module.settings_for_map(settings, 58).npcs[0]
        _, ordinary_fields = decode_frame(server_module.map_npc_dialogue_frames(ordinary, kunlun_role)[0])
        ordinary_values = field_values(ordinary_fields)
        self.assertEqual(ordinary_values[:2], [1900002, 3])
        self.assertNotIn('学习门派技能', ordinary_values)

    def test_active_kunlun_mentor_option_opens_learning_once(self):
        state_type = getattr(server_module, 'LocalNpcDialogueState', None)
        route_option = getattr(server_module, 'npc_dialogue_option_frames', None)
        self.assertIsNotNone(state_type, 'NPC dialogue state is missing')
        self.assertIsNotNone(route_option, 'NPC dialogue option router is missing')
        settings = Settings(map_registry=server_module.default_map_registry())
        role = default_role(settings)
        role.update({'sect_id': 1, 'map_id': 60001, 'map_name': '昆仑', 'map_x': 8, 'map_y': 6})
        state = state_type()
        state.select(60001, 1900101)

        frames = route_option(settings, role, state, 1)

        self.assertEqual([decode_frame(frame)[0] for frame in frames], [1010, 1010])
        self.assertEqual(field_values(decode_frame(frames[0])[1])[-1], 7)
        self.assertEqual(field_values(decode_frame(frames[1])[1]), [0, 0, 0, 1, 179, 69])
        self.assertIsNone(state.map_id)
        self.assertIsNone(state.npc_id)

        replay = route_option(settings, role, state, 1)
        self.assertEqual(len(replay), 1)
        self.assertEqual(field_values(decode_frame(replay[0])[1])[-1], 7)

    def test_invalid_or_stale_mentor_option_only_clears_wait_state(self):
        settings = Settings(map_registry=server_module.default_map_registry())
        base_role = default_role(settings)
        base_role.update({'sect_id': 1, 'map_id': 60001, 'map_name': '昆仑', 'map_x': 8, 'map_y': 6})
        cases = [
            ({'sect_id': 2}, 60001, 1900101, 1),
            ({}, 58, 1900101, 1),
            ({}, 60001, 1900101, 0),
            ({}, 60001, 1900002, 1),
        ]
        for role_updates, map_id, npc_id, option_id in cases:
            with self.subTest(role_updates=role_updates, map_id=map_id, npc_id=npc_id, option_id=option_id):
                role = dict(base_role)
                role.update(role_updates)
                state = server_module.LocalNpcDialogueState()
                state.select(map_id, npc_id)

                frames = server_module.npc_dialogue_option_frames(
                    settings,
                    role,
                    state,
                    option_id,
                )

                self.assertEqual(len(frames), 1)
                self.assertEqual(field_values(decode_frame(frames[0])[1])[-1], 7)
                self.assertIsNone(state.map_id)
                self.assertIsNone(state.npc_id)

    def test_field_debug_helpers_are_read_only(self):
        fields = [integer(60), short(34), string('月华'), binary(b'abc')]
        encoded = encode_frame(1048, fields)
        self.assertEqual(field_type_name(4), 'int')
        self.assertEqual(field_type_name(3), 'short')
        self.assertEqual(field_debug_value(fields[3]), 'bytes[3]')
        entries = field_debug_entries(fields)
        self.assertEqual(
            entries,
            [
                {'index': 0, 'type': 'int', 'value': 60},
                {'index': 1, 'type': 'short', 'value': 34},
                {'index': 2, 'type': 'string', 'value': '月华'},
                {'index': 3, 'type': 'binary', 'value': 'bytes[3]'},
            ],
        )
        self.assertEqual(encode_frame(1048, fields), encoded)
        self.assertEqual(field_values(decode_frame(encoded)[1]), [60, 34, '月华', b'abc'])

    def test_map_player_appearance_debug_matches_1006_without_changing_it(self):
        settings = Settings()
        role = default_role(settings)
        helmet = next(item for item in role_items(role) if item['name'] == '青纹盔')
        helmet['location'] = 'equipped'
        payload = player_info(settings, role)
        message_id, fields = decode_frame(payload)
        values = field_values(fields)
        snapshot = map_player_appearance_debug(role, settings)
        self.assertEqual(message_id, 1006)
        self.assertEqual(snapshot['model'], values[7])
        self.assertEqual(snapshot['properties'][6], values[7])
        self.assertEqual(snapshot['properties'][7], values[8])
        for property_index in (14, 15, 16, 17, 18, 19, 20):
            self.assertEqual(snapshot['properties'][property_index], values[property_index + 1])
        self.assertEqual(snapshot['properties'][20], 3)
        log_text = format_map_player_appearance_log('1', role, settings)
        self.assertIn('MAP_PLAYER_APPEARANCE', log_text)
        self.assertIn("user='1'", log_text)
        self.assertEqual(decode_frame(player_info(settings, role))[1][0].type_id, fields[0].type_id)
        self.assertEqual(field_values(decode_frame(player_info(settings, role))[1]), values)

    def test_battle_actor_debug_snapshot_does_not_change_1048(self):
        role = default_role(Settings())
        frames = battle_actor_frames(role, Settings(), trace_id='BT-10001-1900001-1')
        _, player_fields = decode_frame(frames[0])
        _, monster_fields = decode_frame(frames[1])
        player_snapshot = battle_actor_debug_snapshot(
            actor_id=int(role['id']),
            model=int(role['model']),
            name=str(role['name']),
            kind=1,
            side_code=2,
            appearance=character_appearance(role),
            fields=player_fields,
            trace_id='BT-10001-1900001-1',
        )
        monster_snapshot = battle_actor_debug_snapshot(
            actor_id=Settings().monster_id,
            model=Settings().monster_model,
            name=Settings().monster_name,
            kind=2,
            side_code=1,
            fields=monster_fields,
            trace_id='BT-10001-1900001-1',
        )
        self.assertEqual(player_snapshot['source_model'], 20000)
        self.assertEqual(player_snapshot['source_model'], field_values(player_fields)[0])
        self.assertEqual(player_snapshot['source_model'], battle_actor_source_model_for_debug(2000, 1, False))
        self.assertEqual(len(player_snapshot['fields']), 22)
        self.assertEqual(player_snapshot['fields'][0], {'index': 0, 'type': 'int', 'value': 20000})
        self.assertEqual(player_snapshot['fields'][15], {'index': 15, 'type': 'short', 'value': 0})
        self.assertEqual(player_snapshot['fields'][21], {'index': 21, 'type': 'short', 'value': int(role['model'])})
        self.assertEqual(player_snapshot['appearance_preset'], int(role['model']))
        self.assertEqual(monster_snapshot['source_model'], 3_759_999)
        self.assertEqual(monster_snapshot['source_model'], field_values(monster_fields)[0])
        self.assertEqual(monster_snapshot['source_model'], battle_actor_source_model_for_debug(3_760_000, 2, False))
        player_log = format_battle_actor_1048_log(player_snapshot)
        monster_log = format_battle_actor_1048_log(monster_snapshot)
        self.assertIn('BATTLE_ACTOR_1048 PLAYER', player_log)
        self.assertIn('battle_trace=BT-10001-1900001-1', player_log)
        self.assertIn(f'appearance_preset={int(role["model"])}', player_log)
        self.assertIn('BATTLE_ACTOR_1048 MONSTER', monster_log)
        self.assertEqual(len(player_fields), 22)
        self.assertEqual(len(monster_fields), 22)
        locked = battle_actor_frames(role, Settings())
        self.assertEqual(field_values(decode_frame(locked[0])[1]), field_values(player_fields))
        self.assertEqual(field_values(decode_frame(locked[1])[1]), field_values(monster_fields))

    def test_battle_resource_resolution_does_not_change_1502_payloads(self):
        monster_id = Settings().monster_model
        monster_path = battle_resource_path(monster_id)
        monster_resolution = battle_resource_resolution(monster_id)
        self.assertEqual(monster_resolution['branch'], 'offset')
        self.assertEqual(monster_resolution['offset_id'], monster_id + 0x200B20)
        self.assertEqual(Path(str(monster_resolution['resolved_path'])), monster_path)

        alias_path = battle_resource_path(6)
        alias_resolution = battle_resource_resolution(6)
        self.assertEqual(alias_resolution['branch'], 'alias')
        self.assertEqual(alias_resolution['alias'], 100_000)
        self.assertEqual(Path(str(alias_resolution['resolved_path'])).name, '100000.dat')
        self.assertEqual(alias_path, Path(str(alias_resolution['resolved_path'])))

        effect_path = battle_resource_path(0)
        effect_resolution = battle_resource_resolution(0)
        self.assertEqual(effect_resolution['branch'], 'offset')
        self.assertEqual(effect_path, Path(str(effect_resolution['resolved_path'])))

        frames = battle_resource_frames(monster_id)
        self.assertEqual(len(frames), 2)
        self.assertEqual(decode_frame(frames[0])[0], 1503)
        self.assertEqual(field_values(decode_frame(frames[0])[1])[:3], [0, monster_id, monster_path.stat().st_size])

        image_frames = battle_image_frames(2, 5_860_104)
        image_debug = battle_image_resolve_debug(5_860_104)
        self.assertFalse(image_debug['missing'])
        self.assertEqual(image_debug['resolved_id'], 5_860_004)
        self.assertEqual(image_debug['alias'], 5_860_004)
        self.assertEqual(decode_frame(image_frames[0])[0], 1501)
        self.assertEqual(decode_frame(image_frames[2]), (1502, []))
        self.assertEqual(field_values(decode_frame(image_frames[0])[1])[4], 5_860_104)

    def test_kind2_monster_source_model_keeps_signed_minus_one(self):
        # APK e.af kind=2 reconstructs model as field[0]+1. Negative map
        # models such as -2004250 must not be clamped to 0 before encoding.
        self.assertEqual(battle_actor_source_model_for_debug(-2_004_250, 2, False), -2_004_251)
        self.assertEqual(battle_actor_source_model_for_debug(3_760_000, 2, False), 3_759_999)
        negative_id, negative_fields = decode_frame(
            battle_actor_frame(
                actor_id=1_900_001,
                model=-2_004_250,
                name='试炼妖兽',
                kind=2,
                side_code=1,
            )
        )
        positive_id, positive_fields = decode_frame(
            battle_actor_frame(
                actor_id=1_900_001,
                model=3_760_000,
                name='试炼妖兽',
                kind=2,
                side_code=1,
            )
        )
        self.assertEqual(negative_id, 1048)
        self.assertEqual(positive_id, 1048)
        self.assertEqual(field_values(negative_fields)[0], -2_004_251)
        self.assertEqual(field_values(positive_fields)[0], 3_759_999)
        self.assertEqual(field_values(positive_fields)[2], 0)
        self.assertEqual(field_values(negative_fields)[7], 2)
        self.assertEqual(field_values(negative_fields)[21], 0)
        self.assertEqual(field_values(positive_fields)[21], 0)

class BattleEscapeSettlementTest(unittest.TestCase):
    """Escape immediately hands departure and closure to the native client."""

    def test_escape_request_finishes_immediately_with_single_native_close(self):
        state = LocalBattleState()
        state.begin(10001, 1900001)
        state.map_id = 58
        state.player_tile = (9, 28)

        frames = server_module.battle_escape_request_frames(state, 1)

        self.assertEqual(len(frames), 1)
        message_id, fields = decode_frame(frames[0])
        self.assertEqual(message_id, 1041)
        self.assertEqual(field_values(fields), [10, 10001])
        self.assertFalse(state.active)
        self.assertEqual(state.phase, 'idle')
        self.assertFalse(state.monster_defeated)
        self.assertEqual((state.player_hp, state.monster_hp), (100, 100))
        self.assertEqual(
            state.escape_guard,
            {'map_id': 58, 'monster_id': 1900001, 'player_id': 10001, 'origin': (9, 28)},
        )

    def test_escape_request_without_active_battle_is_ignored(self):
        state = LocalBattleState()

        frames = server_module.battle_escape_request_frames(state, 1)

        self.assertEqual(frames, [])
        self.assertFalse(state.active)
        self.assertEqual(state.phase, 'idle')
        self.assertIsNone(state.escape_guard)

    def test_guarded_1010_interaction_ack_clears_wait_without_map_action(self):
        # b/ab.aj() sets main/t's wait flags before sending C->S 1010/7.  The
        # S->C 1010 dispatcher clears those flags before looking at field 5;
        # action 7 has no inbound branch, so this complete six-field record is
        # a side-effect-free acknowledgement for a guard-suppressed re-tap.
        build_ack = getattr(server_module, 'map_object_interaction_ack_frame', None)
        self.assertIsNotNone(build_ack, 'guarded interaction acknowledgement is missing')

        message_id, fields = decode_frame(build_ack(1900001))
        self.assertEqual(message_id, 1010)
        self.assertEqual([field.type_id for field in fields], [4, 3, 3, 4, 4, 3])
        self.assertEqual(field_values(fields), [1900001, 0, 0, 0, 0, 7])


class PositionPersistenceTests(unittest.TestCase):
    def test_update_role_position_changes_role_tile(self):
        role = default_role(Settings())

        changed = update_role_position(role, 23, 41)

        self.assertTrue(changed)
        self.assertEqual(role['map_x'], 23)
        self.assertEqual(role['map_y'], 41)

    def test_update_role_position_ignores_same_tile(self):
        role = default_role(Settings())
        role['map_x'] = 23
        role['map_y'] = 41

        changed = update_role_position(role, 23, 41)

        self.assertFalse(changed)
        self.assertEqual(role['map_x'], 23)
        self.assertEqual(role['map_y'], 41)

    def test_role_position_persists_across_store_reload(self):
        with tempfile.TemporaryDirectory() as directory:
            role_file = str(Path(directory) / 'roles.json')
            settings = Settings(role_data_file=role_file)

            store = RoleStore(settings)
            role = store.roles_for('position-user')[0]

            self.assertTrue(update_role_position(role, 31, 52))
            store.save()

            reloaded = RoleStore(settings)
            reloaded_role = reloaded.roles_for('position-user')[0]

            self.assertEqual(reloaded_role['map_x'], 31)
            self.assertEqual(reloaded_role['map_y'], 52)

    def test_settings_for_role_uses_persisted_position_as_spawn(self):
        settings = Settings()
        role = default_role(settings)

        role['map_x'] = 37
        role['map_y'] = 44

        current_map = settings_for_role(settings, role)

        self.assertEqual(current_map.spawn_x, 37)
        self.assertEqual(current_map.spawn_y, 44)


if __name__ == '__main__':
    unittest.main()
