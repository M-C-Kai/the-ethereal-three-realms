import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from map_o import decode_tile_rle
from protocol import GameCipher, byte, decode_frame, encode_frame, field_values, integer, long_integer, short, string
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
    battle_actor_frame,
    battle_actor_frames,
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
    battle_progress_frame,
    battle_reward_popup,
    level_experience_required,
    level_up_effect_frame,
    apply_one_level,
    apply_battle_rewards,
    LocalBattleState,
    map_portal_frame,
    mount_update_frame,
    menu_prefetch_empty_ack,
    notice_and_world,
    player_info,
    role_items,
    role_list,
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
            self.assertEqual(created['map_name'], '仙石村')
            self.assertEqual(len(role_items(created)), 16)
            self.assertEqual(
                {int(item.get('equipment_slot', 0)) for item in role_items(created) if int(item.get('equipment_slot', 0)) > 0},
                set(range(1, 15)) | {17},
            )

            reloaded = RoleStore(settings)
            self.assertEqual(len(reloaded.roles_for('tester')), 2)
            self.assertTrue(reloaded.delete('tester', int(created['id'])))
            self.assertEqual(len(RoleStore(settings).roles_for('tester')), 1)

    def test_item_records_match_original_client_layout(self):
        items = role_items(default_role(Settings()))
        weapon = next(item for item in items if item['name'] == '青锋剑')
        armour = next(item for item in items if item['name'] == '青纹铠甲')
        potion = next(item for item in items if item['name'] == '小还丹')
        mount = next(item for item in items if item['name'] == '坐骑验证令')

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
        self.assertEqual(values[7:9], [170_410_004, '坐骑验证令'])
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
        self.assertEqual(len(migrated), 16)
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
        mounted_role['mount_model'] = 41004
        mounted_values = field_values(decode_frame(player_info(settings, mounted_role))[1])
        self.assertEqual(mounted_values[23], 41004)
        mount_id, mount_fields = decode_frame(mount_update_frame(mounted_role))
        self.assertEqual(mount_id, 1017)
        self.assertEqual(field_values(mount_fields), [0, settings.role_id, 1, 22, 41004])

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

        skill_id, skill_fields = decode_frame(character_skill_list())
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

    def test_map_flow(self):
        settings = Settings()
        frames = map_data_frames(settings)
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

        enter_frames = map_enter_frames(settings)
        enter_actions = [field_values(decode_frame(x)[1])[5] for x in enter_frames[:3]]
        self.assertEqual(enter_actions, [13, 14, 105])
        monster_id, monster_fields = decode_frame(enter_frames[3])
        self.assertEqual(monster_id, 1126)
        self.assertEqual(field_values(monster_fields), [0, 1, settings.monster_id, 10, 6, 3_760_000, '试炼妖兽'])
        self.assertEqual([field.type_id for field in monster_fields], [2, 2, 4, 4, 4, 4, 6])
        self.assertGreaterEqual(settings.monster_id, 1_000_000)

        standalone_id, standalone_fields = decode_frame(map_monster_frame(settings))
        self.assertEqual(standalone_id, 1126)
        self.assertEqual(field_values(standalone_fields)[2], settings.monster_id)

        remove_id, remove_fields = decode_frame(map_object_remove_frame(settings.monster_id))
        self.assertEqual(remove_id, 1010)
        self.assertEqual(field_values(remove_fields), [settings.monster_id, 0, 0, 0, 0, 18])
        self.assertEqual([field.type_id for field in remove_fields], [4, 3, 3, 4, 4, 3])

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

    def test_battle_actor_frames_match_apk_participant_parser(self):
        role = default_role(Settings())
        frames = battle_actor_frames(role, Settings())
        self.assertEqual(len(frames), 2)
        player_id, player_fields = decode_frame(frames[0])
        self.assertEqual(player_id, 1048)
        self.assertEqual(
            [field.type_id for field in player_fields],
            [4, 4, 4, 4, 4, 4, 6, 3, 4, 4, 4, 4, 4, 4, 4, 3, 4, 4, 4, 4, 4, 3],
        )
        self.assertEqual(field_values(player_fields)[5], 2)
        self.assertEqual(field_values(player_fields)[7:10], [1, 1, role['id']])
        monster_id, monster_fields = decode_frame(frames[1])
        self.assertEqual(monster_id, 1048)
        self.assertEqual(field_values(monster_fields)[7:10], [2, 1, Settings().monster_id])
        self.assertEqual(field_values(monster_fields)[5], 1)

        # A full 1048 refresh remains available for resync/reconnect paths,
        # while normal combat HP is changed by the type-22 effect in 1042.
        state = LocalBattleState()
        state.begin(int(role['id']), Settings().monster_id)
        state.monster_hp = 90
        update_id, update_fields = decode_frame(
            battle_actor_update_frame(role, Settings(), state, state.monster_id)
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
        self.assertFalse(state.apply_basic_attack(40))
        # Damage application no longer advances the protocol round.  The APK
        # supplies that round in 1041 and advances it after the matching
        # 1040/action=2 acknowledgement.
        self.assertEqual((state.round, state.monster_hp), (1, 60))
        self.assertTrue(state.apply_basic_attack(60))
        self.assertTrue(state.active)
        state.finish()
        self.assertFalse(state.active)

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
        settings = Settings(portal_enabled=True)
        self.assertEqual(settings.portal_target_map_o_file, 'maps/50000.map.o')
        portal_id, portal_fields = decode_frame(map_portal_frame(settings))
        self.assertEqual(portal_id, 1126)
        self.assertEqual(field_values(portal_fields)[0:5], [0, 1, settings.portal_id, settings.portal_x, settings.portal_y])
        target = __import__('server').settings_for_map(settings, settings.portal_target_map_id)
        self.assertEqual((target.monster_x, target.monster_y), (12, 8))
        entered = map_enter_frames(target)
        self.assertEqual(field_values(decode_frame(entered[0])[1])[4:], [0, 13])
        self.assertEqual(field_values(decode_frame(entered[-1])[1])[2], settings.return_portal_id)


if __name__ == '__main__':
    unittest.main()
