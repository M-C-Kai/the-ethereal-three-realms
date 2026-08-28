from __future__ import annotations

import argparse
import socket
import struct
import time

from protocol import GameCipher, byte, decode_frame, encode_frame, field_values, integer, short, string


def receive_frame(sock: socket.socket, cipher: GameCipher | None = None) -> tuple[int, list[object]]:
    header = sock.recv(2)
    if len(header) != 2:
        raise RuntimeError('server closed before sending a frame')
    if cipher is not None:
        header = cipher.decrypt(header)
    length = struct.unpack('>H', header)[0]
    body = bytearray()
    while len(body) < length - 2:
        chunk = sock.recv(length - 2 - len(body))
        if not chunk:
            raise RuntimeError('server closed during a frame')
        body.extend(chunk)
    if cipher is not None:
        body = bytearray(cipher.decrypt(bytes(body)))
    frame = header + body
    message_id, fields = decode_frame(frame)
    return message_id, field_values(fields)


def expect(sock: socket.socket, message_id: int, cipher: GameCipher | None = None) -> list[object]:
    actual_id, values = receive_frame(sock, cipher)
    assert actual_id == message_id, (actual_id, values)
    return values


def main() -> None:
    parser = argparse.ArgumentParser(description='Test the complete local login/role/map protocol')
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=6805)
    parser.add_argument('--username', default='localtest')
    parser.add_argument('--password', default='test123')
    parser.add_argument('--exercise-role-crud', action='store_true')
    parser.add_argument('--exercise-portal', action='store_true')
    parser.add_argument('--exercise-monster', action='store_true')
    parser.add_argument('--exercise-monster-kill', action='store_true')
    parser.add_argument('--hold-seconds', type=float, default=0, help='Stay in the map and answer 1012 heartbeats')
    args = parser.parse_args()

    login = encode_frame(1077, [
        short(2000), byte(53), byte(0), string(args.username), string(args.password), short(15), byte(0)
    ])
    with socket.create_connection((args.host, args.port), timeout=5) as account_sock:
        account_sock.sendall(login)
        servers = expect(account_sock, 1077)
        assert servers[2] == 1 and servers[5] == 1, servers
        account_sock.sendall(encode_frame(1051, [
            string(args.username), string(args.password), string(servers[4]), integer(1), byte(0)
        ]))
        redirect = expect(account_sock, 1052)

    session_id, account_id, game_port, game_host = redirect[:4]
    with socket.create_connection((str(game_host), int(game_port)), timeout=5) as game_sock:
        cipher = GameCipher()
        game_sock.sendall(cipher.encrypt_frame(encode_frame(1052, [integer(session_id), integer(account_id)])))
        roles = expect(game_sock, 1080, cipher)
        assert roles[0] == 0 and roles[1] >= 1, roles
        role_id = int(roles[2])

        if args.exercise_role_crud:
            occupied_slots = {int(roles[8 + (index * 15)]) for index in range(int(roles[1]))}
            slot = next(candidate for candidate in range(3) if candidate not in occupied_slots)
            game_sock.sendall(cipher.encrypt_frame(encode_frame(1080, [short(4)])))
            suggested = expect(game_sock, 1080, cipher)
            assert suggested[0] == 4 and len(suggested) == 3, suggested

            created_name = f'测试{int(time.time()) % 100000}'
            create = encode_frame(1080, [
                short(2), string(created_name), byte(6), byte(slot), byte(0), byte(53), short(2000), short(15)
            ])
            game_sock.sendall(cipher.encrypt_frame(create))
            after_create = expect(game_sock, 1080, cipher)
            assert after_create[0] == 0 and after_create[1] == roles[1] + 1, after_create
            created_id = next(
                int(after_create[2 + (index * 15)])
                for index in range(int(after_create[1]))
                if after_create[7 + (index * 15)] == created_name
            )
            game_sock.sendall(cipher.encrypt_frame(encode_frame(1080, [short(1), integer(created_id)])))
            deleted = expect(game_sock, 1080, cipher)
            assert deleted == [1, created_id], deleted

        game_sock.sendall(cipher.encrypt_frame(encode_frame(1080, [short(0), integer(role_id)])))
        player = expect(game_sock, 1006, cipher)
        assert player[0] == 85 and player[2] == role_id, player
        extension = expect(game_sock, 1089, cipher)
        assert extension == [0, 0], extension
        skills = expect(game_sock, 1132, cipher)
        assert skills[0:4] == [0, 1, '基础技能', 0] and len(skills) == 16, skills
        item_records = [expect(game_sock, 1008, cipher) for _ in range(16)]
        items = {str(values[8]): values for values in item_records}
        assert len(items) == 16 and {'青锋剑', '青纹项链', '青纹长靴', '小还丹', '坐骑验证令'} <= set(items), items

        weapon_id = int(items['青锋剑'][1])
        potion_id = int(items['小还丹'][1])
        mount_token_id = int(items['坐骑验证令'][1])
        game_sock.sendall(cipher.encrypt_frame(encode_frame(1009, [short(82), integer(weapon_id)])))
        description = expect(game_sock, 1009, cipher)
        assert description[0:2] == [82, weapon_id], description

        visible_appearance = {
            '青纹盔': (1, 20, 3),
            '青纹肩甲': (2, 16, 23),
            '青纹铠甲': (3, 15, 34),
            '青纹腿甲': (5, 14, 25),
            '青纹披风': (7, 19, 3),
            '青纹护腕': (8, 17, 8),
            '青纹长靴': (9, 18, 22),
            '青锋剑': (10, 7, 270001),
        }
        icon_only_slots = {
            '青纹腰带': 4,
            '青纹项链': 6,
            '青纹戒指': 11,
            '青纹外套': 12,
            '青纹饰品': 13,
            '青纹法宝': 14,
        }
        for name, (slot, property_index, value) in visible_appearance.items():
            item_id = int(items[name][1])
            game_sock.sendall(cipher.encrypt_frame(encode_frame(1009, [short(5), integer(item_id)])))
            equipped = expect(game_sock, 1008, cipher)
            equip_ack = expect(game_sock, 1009, cipher)
            equipped_appearance = expect(game_sock, 1017, cipher)
            assert equipped[0:5] == [3, item_id, 1, 1, slot], equipped
            assert equip_ack == [5] and equipped_appearance == [0, role_id, 1, property_index, value], (
                name,
                equip_ack,
                equipped_appearance,
            )

            game_sock.sendall(cipher.encrypt_frame(encode_frame(1009, [short(6), integer(item_id)])))
            unequipped = expect(game_sock, 1008, cipher)
            unequip_ack = expect(game_sock, 1009, cipher)
            restored_appearance = expect(game_sock, 1017, cipher)
            assert unequipped[0:5] == [3, item_id, 1, 1, 50], unequipped
            assert unequip_ack == [6] and restored_appearance == [0, role_id, 1, property_index, 0], (
                name,
                unequip_ack,
                restored_appearance,
            )

        # The six APK-defined accessory slots have no independent character
        # sprite property, but their equipment-vector move must still update
        # the equipment panel immediately on both equip and unequip.
        for name, slot in icon_only_slots.items():
            item_id = int(items[name][1])
            game_sock.sendall(cipher.encrypt_frame(encode_frame(1009, [short(5), integer(item_id)])))
            equipped = expect(game_sock, 1008, cipher)
            equip_ack = expect(game_sock, 1009, cipher)
            panel_refresh = expect(game_sock, 1017, cipher)
            assert equipped[0:5] == [3, item_id, 1, 1, slot], equipped
            assert equip_ack == [5], equip_ack
            assert panel_refresh[0:3] == [0, role_id, 8], panel_refresh

            game_sock.sendall(cipher.encrypt_frame(encode_frame(1009, [short(6), integer(item_id)])))
            unequipped = expect(game_sock, 1008, cipher)
            unequip_ack = expect(game_sock, 1009, cipher)
            panel_refresh = expect(game_sock, 1017, cipher)
            assert unequipped[0:5] == [3, item_id, 1, 1, 50], unequipped
            assert unequip_ack == [6], unequip_ack
            assert panel_refresh[0:3] == [0, role_id, 8], panel_refresh

        game_sock.sendall(cipher.encrypt_frame(encode_frame(1009, [short(4), integer(potion_id)])))
        used = expect(game_sock, 1008, cipher)
        use_ack = expect(game_sock, 1009, cipher)
        assert used[0:2] == [3, potion_id] and used[2] == int(items['小还丹'][2]) - 1 and use_ack == [4], (
            used,
            use_ack,
        )

        # The APK has a dedicated equipment-panel mount slot (position 17).
        # Equip/unequip use the same 1008/1009 flow as the other equipment,
        # plus property 22 to redraw the character page and map sprite.
        game_sock.sendall(cipher.encrypt_frame(encode_frame(1009, [short(5), integer(mount_token_id)])))
        mounted_item = expect(game_sock, 1008, cipher)
        mount_ack = expect(game_sock, 1009, cipher)
        mounted = expect(game_sock, 1017, cipher)
        assert mounted_item[0:2] == [3, mount_token_id] and mounted_item[4] == 17, mounted_item
        assert mount_ack == [5] and mounted == [0, role_id, 1, 22, 41004], (mount_ack, mounted)

        game_sock.sendall(cipher.encrypt_frame(encode_frame(1009, [short(6), integer(mount_token_id)])))
        dismounted_item = expect(game_sock, 1008, cipher)
        dismount_ack = expect(game_sock, 1009, cipher)
        dismounted = expect(game_sock, 1017, cipher)
        assert dismounted_item[0:2] == [3, mount_token_id] and dismounted_item[4] == 50, dismounted_item
        assert dismount_ack == [6] and dismounted == [0, role_id, 1, 22, 0], (dismount_ack, dismounted)

        game_sock.sendall(cipher.encrypt_frame(encode_frame(1123, [byte(0), byte(53), short(2000), short(15)])))
        notice = expect(game_sock, 1123, cipher)
        world = expect(game_sock, 1110, cipher)
        assert notice[2] == '本地服务正常', notice
        assert world[1] == 58, world

        game_sock.sendall(cipher.encrypt_frame(encode_frame(1010, [short(12), integer(0)])))
        received = [receive_frame(game_sock, cipher) for _ in range(7)]
        assert [x[0] for x in received] == [1010, 1407, 1407, 1407, 1407, 1407, 1010], received
        assert received[-1][1][5] == 12 and received[-1][1][4] == 1, received[-1]

        game_sock.sendall(cipher.encrypt_frame(encode_frame(1010, [short(13), integer(4964)])))
        # Map 58 now also advertises one 1126 portal actor after the verified
        # monster actor.  Keep the original first four frames unchanged.
        entered = [receive_frame(game_sock, cipher) for _ in range(5)]
        assert [x[1][5] for x in entered[:3]] == [13, 14, 105], entered
        assert entered[3][0] == 1126 and entered[3][1][:2] == [0, 1], entered[3]
        assert entered[4][0] == 1126 and entered[4][1][2] == 580001, entered[4]

        if args.exercise_monster:
            monster = entered[3][1]
            # Active APK main/k.a(n) sends protocol 2031 as
            # [object_id, 0, x, y, action=6, 0]. The local server starts the
            # small APK-compatible battle probe, then accepts a 1041 command.
            game_sock.sendall(cipher.encrypt_frame(encode_frame(2031, [
                integer(monster[2]), integer(0), short(monster[3]), short(monster[4]), short(6), short(0)
            ])))
            monster_reset = expect(game_sock, 1040, cipher)
            assert monster_reset == [0], monster_reset
            player_actor = expect(game_sock, 1048, cipher)
            monster_actor = expect(game_sock, 1048, cipher)
            assert player_actor[7:10] == [1, 1, role_id], player_actor
            assert monster_actor[7:10] == [2, 1, int(monster[2])], monster_actor
            monster_start = expect(game_sock, 1040, cipher)
            assert monster_start[0:2] == [1, 1], monster_start
            game_sock.sendall(cipher.encrypt_frame(encode_frame(1041, [
                integer(10), byte(1), integer(role_id), integer(0), integer(0), integer(0), integer(0), integer(0)
            ])))
            player_action = expect(game_sock, 1042, cipher)
            assert player_action[0:6] == [1, role_id, int(monster[2]), 1, 1, 0], player_action
            assert player_action[9:] == [1, int(monster[2]), 0, 22, -10, ''], player_action
            counter_action = expect(game_sock, 1042, cipher)
            assert counter_action[0:6] == [1, int(monster[2]), role_id, 1, 1, 0], counter_action
            assert counter_action[9:] == [1, role_id, 0, 22, -10, ''], counter_action
            monster_round = expect(game_sock, 1040, cipher)
            assert monster_round[0:2] == [2, 1], monster_round
            # Full action=2 starts playback; the real APK returns the short
            # form only after both native action records have completed.
            game_sock.sendall(cipher.encrypt_frame(encode_frame(1040, [byte(2), integer(1)])))
            if args.exercise_monster_kill:
                # Finish the deterministic 10-hit encounter and verify that
                # a killing blow closes the scene after the queue-drained ack.
                current_round = 2
                for _ in range(9):
                    game_sock.sendall(cipher.encrypt_frame(encode_frame(1041, [
                        integer(10), byte(current_round), integer(role_id), integer(0), integer(0), integer(0), integer(0), integer(0)
                    ])))
                    expect(game_sock, 1042, cipher)  # player ACTION_ATTACK + damage
                    if _ < 8:
                        expect(game_sock, 1042, cipher)  # monster ACTION_ATTACK + damage
                        next_round = expect(game_sock, 1040, cipher)
                        assert next_round[0:2] == [2, current_round], next_round
                        game_sock.sendall(cipher.encrypt_frame(encode_frame(1040, [byte(2), integer(current_round)])))
                        current_round += 1
                    else:
                        playback = expect(game_sock, 1040, cipher)
                        assert playback[0:2] == [2, current_round], playback
                        game_sock.sendall(cipher.encrypt_frame(encode_frame(1040, [byte(2), integer(current_round)])))
                        assert expect(game_sock, 1040, cipher) == [4], 'battle end was not delivered'
                        removed = expect(game_sock, 1010, cipher)
                        assert removed[0] == int(monster[2]) and removed[5] == 18, 'monster removal was not delivered'
                        progress = expect(game_sock, 1017, cipher)  # incremental level/EXP refresh
                        expect(game_sock, 1008, cipher)  # dropped item
                        expect(game_sock, 1123, cipher)  # reward notice
                        top_protocol, result_prompt = receive_frame(game_sock, cipher)
                        progress_properties = dict(zip(progress[3::2], progress[4::2]))
                        if top_protocol == 1049:
                            assert result_prompt == [3, 50, 0, 0, 0, 'x'], result_prompt
                        else:
                            assert top_protocol == 1129, (top_protocol, result_prompt)
                            assert result_prompt[0] == role_id, result_prompt
                            assert result_prompt[1] == progress_properties[11], result_prompt

        if args.exercise_portal:
            game_sock.sendall(cipher.encrypt_frame(encode_frame(1010, [short(7), integer(580001)])))
            switched_world = expect(game_sock, 1110, cipher)
            assert switched_world[1] == 50000 and switched_world[3] == '传送测试区', switched_world
            game_sock.sendall(cipher.encrypt_frame(encode_frame(1010, [short(12), integer(0)])))
            switched_data = [receive_frame(game_sock, cipher) for _ in range(7)]
            assert [x[0] for x in switched_data] == [1010, 1407, 1407, 1407, 1407, 1407, 1010], switched_data
            game_sock.sendall(cipher.encrypt_frame(encode_frame(1010, [short(13), integer(0)])))
            switched_enter = [receive_frame(game_sock, cipher) for _ in range(5)]
            assert [x[1][5] for x in switched_enter[:3]] == [13, 14, 105], switched_enter
            assert switched_enter[0][1][4] == 0, switched_enter[0]
            assert switched_enter[4][0] == 1126 and switched_enter[4][1][2] == 580002, switched_enter[4]

            game_sock.sendall(cipher.encrypt_frame(encode_frame(1010, [short(7), integer(580002)])))
            returned_world = expect(game_sock, 1110, cipher)
            assert returned_world[1] == 58 and returned_world[3] == '仙石村', returned_world
            game_sock.sendall(cipher.encrypt_frame(encode_frame(1010, [short(12), integer(0)])))
            returned_data = [receive_frame(game_sock, cipher) for _ in range(7)]
            assert [x[0] for x in returned_data] == [1010, 1407, 1407, 1407, 1407, 1407, 1010], returned_data
            game_sock.sendall(cipher.encrypt_frame(encode_frame(1010, [short(13), integer(4964)])))
            returned_enter = [receive_frame(game_sock, cipher) for _ in range(5)]
            assert [x[1][5] for x in returned_enter[:3]] == [13, 14, 105], returned_enter
            assert returned_enter[0][1][4] == 0, returned_enter[0]
            assert returned_enter[4][0] == 1126 and returned_enter[4][1][2] == 580001, returned_enter[4]

        menu_prefetches = (
            (1403, [byte(6), byte(0), byte(12), byte(2)], 1),
            (1090, [byte(1), integer(501), integer(0), byte(0), byte(13)], 0),
            (1153, [byte(1)], 0),
            (1061, [byte(0)], 3),
        )
        for protocol_id, request_fields, empty_subtype in menu_prefetches:
            game_sock.sendall(cipher.encrypt_frame(encode_frame(protocol_id, request_fields)))
            response_id, response_values = receive_frame(game_sock, cipher)
            assert (response_id, response_values) == (protocol_id, [empty_subtype]), (
                response_id,
                response_values,
            )

        game_sock.sendall(cipher.encrypt_frame(encode_frame(1039, [byte(1)])))
        # Opening the character panel now refreshes the cached EXP/HP fields
        # with an incremental 1017 update before the legacy 1039 summaries.
        panel_progress = expect(game_sock, 1017, cipher)
        assert panel_progress[0] == 0 and panel_progress[2] >= 2, panel_progress
        panel_properties = dict(zip(panel_progress[3::2], panel_progress[4::2]))
        assert {31, 32, 85, 86} <= set(panel_properties), panel_progress
        character_attributes = expect(game_sock, 1039, cipher)
        divine_summary = expect(game_sock, 1039, cipher)
        assert character_attributes[0] == 1 and len(character_attributes[1:]) == 7, character_attributes
        assert divine_summary[0] == 2 and len(divine_summary[1:]) == 13, divine_summary

        heartbeat_count = 0
        deadline = time.monotonic() + max(0, args.hold_seconds)
        while time.monotonic() < deadline:
            game_sock.settimeout(max(0.1, deadline - time.monotonic()))
            try:
                message_id, values = receive_frame(game_sock, cipher)
            except socket.timeout:
                break
            assert message_id == 1012 and len(values) == 1, (message_id, values)
            nonce = int(values[0])
            current_millis = int(time.time() * 1000) & 0xFFFFFFFF
            response_value = (current_millis ^ nonce) & 0xFFFFFFFF
            if response_value >= 0x80000000:
                response_value -= 0x100000000
            game_sock.sendall(cipher.encrypt_frame(encode_frame(1012, [
                integer(nonce), integer(response_value), integer(0)
            ])))
            heartbeat_count += 1

    print(
        f'OK: {servers[3]}(良好) -> 1052 游戏服 -> 角色 {roles[7]} '
        f'-> 物品查看/装备/卸下/使用 -> 地图 {world[3]} ({entered[1][1][1]},{entered[1][1][2]}) '
        f'-> 人物菜单预加载及属性/神通数据已应答 '
        f'-> 心跳 {heartbeat_count} 次'
    )


if __name__ == '__main__':
    main()
