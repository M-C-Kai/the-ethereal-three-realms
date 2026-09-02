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


def receive_tolerant(sock: socket.socket, cipher: GameCipher | None = None) -> tuple[int, list[object]]:
    """Receive the next non-heartbeat frame, skipping recurring 1012 heartbeats.

    The local server pushes a 1012 heartbeat every 25 seconds (original
    watchdog); the longer role/map/escape exercise can therefore have a
    heartbeat interleave with an expected message. This helper threads past
    them so the assertion sees only the application message.
    """
    while True:
        message_id, values = receive_frame(sock, cipher)
        if message_id == 1012:
            continue
        return message_id, values


def expect_tolerant(sock: socket.socket, message_id: int, cipher: GameCipher | None = None) -> list[object]:
    actual_id, values = receive_tolerant(sock, cipher)
    assert actual_id == message_id, (actual_id, values)
    return values


LOCKED_APPEARANCE_PROPERTIES = (2, 7, 14, 15, 16, 17, 18, 19, 20)


def parse_appearance(frame: list[object]) -> tuple[int, int, dict[int, int]]:
    """Parse a protocol-1017 character-appearance payload.

    The server's 1017 carries the full locked appearance after any equip or
    unequip: ``[action, role_id, property_count, (property_id, value) * count]``.
    The APK consumer ``pmsj.work.main.e.O`` reads field 1 as the target role id,
    field 2 as the pair count, then byte/int property pairs from field 3.

    Returns ``(action, role_id, {property_id: value})``.
    """
    action = int(frame[0])
    role_id = int(frame[1])
    count = int(frame[2])
    pairs = frame[3:]
    assert len(pairs) == count * 2, (frame, count)
    properties: dict[int, int] = {}
    for index in range(0, count * 2, 2):
        property_id = int(pairs[index])
        value = int(pairs[index + 1])
        assert property_id not in properties, (frame, property_id)
        properties[property_id] = value
    return action, role_id, properties


def name_appearance_from_1006(player: list[object]) -> dict[int, int]:
    """Extract the authoritative locked appearance from the login 1006 frame.

    1006 is a flat ``properties[0..84]`` list: ``[count, prop0..prop84, time]``,
    so the value of character property ``i`` lives at ``player[1 + i]``.
    """
    return {prop: int(player[1 + prop]) for prop in LOCKED_APPEARANCE_PROPERTIES}


def assert_minimal_change(
    frame: list[object],
    role_id: int,
    property_id: int,
    value: int,
) -> dict[int, int]:
    """Assert a 1017 frame is the single-property minimal change frame."""
    action, actual_id, properties = parse_appearance(frame)
    assert action == 0, frame
    assert actual_id == role_id, frame
    assert properties == {property_id: value}, (frame, property_id, value)
    return properties


def assert_full_refresh(
    frame: list[object],
    role_id: int,
    authoritative: dict[int, int],
) -> dict[int, int]:
    """Assert a 1017 frame is the full locked-appearance refresh.

    The property set must be exactly the nine locked appearance layers and each
    value must equal the current authoritative appearance.
    """
    action, actual_id, properties = parse_appearance(frame)
    assert action == 0, frame
    assert actual_id == role_id, frame
    assert set(properties) == set(LOCKED_APPEARANCE_PROPERTIES), frame
    for locked in LOCKED_APPEARANCE_PROPERTIES:
        assert properties[locked] == authoritative[locked], (frame, locked, authoritative[locked])
    return properties


def team_create_request(role_id: int) -> bytes:
    """Build the native APK's 1023 create-team request."""
    return encode_frame(1023, [short(0), integer(role_id)])


def team_disband_request() -> bytes:
    """Build the native APK's 1023 leader-disband request."""
    return encode_frame(1023, [short(11)])


def main() -> None:
    parser = argparse.ArgumentParser(description='Test the complete local login/role/map protocol')
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=6805)
    parser.add_argument('--username', default='localtest')
    parser.add_argument('--password', default='test123')
    parser.add_argument('--exercise-role-crud', action='store_true')
    parser.add_argument(
        '--exercise-mail-only',
        action='store_true',
        help='Exercise the persisted 1500 inbox/detail/read flow and exit',
    )
    parser.add_argument(
        '--exercise-team-only',
        action='store_true',
        help='Exercise the APK-confirmed 1023/1026 create-and-disband team flow and exit',
    )
    parser.add_argument('--exercise-portal', action='store_true')
    parser.add_argument('--exercise-monster', action='store_true')
    parser.add_argument('--exercise-monster-kill', action='store_true')
    parser.add_argument('--exercise-monster-escape', action='store_true')
    parser.add_argument(
        '--exercise-skill-only',
        action='store_true',
        help='Exercise 1103 detail/learn and exit; selected role must belong to local sect 1',
    )
    parser.add_argument(
        '--exercise-kunlun-only',
        action='store_true',
        help='Exercise the Kunlun portal/mentor learning-mode UI without changing skill level',
    )
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
        player_properties = {
            property_index: player[1 + property_index]
            for property_index in range(int(player[0]))
        }
        appearance = name_appearance_from_1006(player)
        extension = expect(game_sock, 1089, cipher)
        assert extension == [0, 0], extension
        skills = expect(game_sock, 1132, cipher)
        assert skills[0:2] == [0, 1] and len(skills) == 16, skills
        sect_skills = expect(game_sock, 1103, cipher)
        assert sect_skills[0] == 0 and sect_skills[1] in (0, 1), sect_skills
        current_skill_level = None
        if sect_skills[1] == 1:
            assert sect_skills[2:4] == ['协议测试技能', 10001], sect_skills
            assert skills[2:4] == ['协议测试技能', 10001], skills
            current_skill_level = int(sect_skills[4])
        else:
            assert skills[2:4] == ['基础技能', 0], skills
        item_records = [expect(game_sock, 1008, cipher) for _ in range(16)]
        items = {str(values[8]): values for values in item_records}
        assert len(items) == 16 and {'青锋剑', '青纹项链', '青纹长靴', '小还丹', '辟邪'} <= set(items), items

        if args.exercise_team_only:
            game_sock.sendall(cipher.encrypt_frame(team_create_request(role_id)))
            leader_status = expect(game_sock, 1017, cipher)
            assert leader_status == [0, role_id, 1, 0, 0x40], leader_status
            created_team = expect(game_sock, 1026, cipher)
            assert created_team == [
                0,
                1,
                player_properties[3],
                role_id,
                player_properties[40],
                player_properties[41],
                player_properties[12],
                player_properties[11],
                player_properties[42],
                player_properties[43],
                0,
            ], created_team

            game_sock.sendall(cipher.encrypt_frame(team_disband_request()))
            cleared_status = expect(game_sock, 1017, cipher)
            assert cleared_status == [0, role_id, 1, 0, 0], cleared_status
            assert expect(game_sock, 1023, cipher) == [11], 'team disband acknowledgement'

            # A stale native leader page may repeat the same action after the
            # connection-local state has already been cleared.
            game_sock.sendall(cipher.encrypt_frame(team_disband_request()))
            repeated_clear = expect(game_sock, 1017, cipher)
            assert repeated_clear == [0, role_id, 1, 0, 0], repeated_clear
            assert expect(game_sock, 1023, cipher) == [11], 'repeated team disband acknowledgement'
            print(f'OK: 角色 {player_properties[3]} 创建单人队伍 -> 解散队伍')
            return

        game_sock.sendall(cipher.encrypt_frame(encode_frame(1500, [byte(12), byte(0), byte(0)])))
        inbox = expect(game_sock, 1500, cipher)
        assert inbox[:3] == [11, 1, 1], inbox
        mail_id = int(inbox[3])
        assert inbox[6:8] == ['系统', '欢迎来到本地服'], inbox
        game_sock.sendall(cipher.encrypt_frame(encode_frame(1500, [byte(13), integer(mail_id)])))
        mail_detail = expect(game_sock, 1500, cipher)
        assert mail_detail[:4] == [14, mail_id, 0, 0], mail_detail
        assert mail_detail[7] == '欢迎来到本地服' and '本地服' in str(mail_detail[8]), mail_detail
        assert '_' in str(mail_detail[9]), mail_detail

        if args.exercise_mail_only:
            game_sock.sendall(cipher.encrypt_frame(encode_frame(1500, [byte(12), byte(0), byte(0)])))
            read_inbox = expect(game_sock, 1500, cipher)
            assert read_inbox[3] == mail_id and int(read_inbox[8]) & 1 == 1, read_inbox
            print(
                f'OK: {servers[3]}(良好) -> 1052 游戏服 -> 角色 {roles[7]} '
                f'-> 邮件 {mail_id} 列表/详情/已读持久化已应答'
            )
            return

        if args.exercise_kunlun_only:
            assert current_skill_level is not None, 'selected role must belong to Kunlun'
            game_sock.sendall(cipher.encrypt_frame(encode_frame(1123, [
                byte(0), byte(53), short(2000), short(15)
            ])))
            assert expect(game_sock, 1123, cipher)[2] == '本地服务正常'
            initial_world = expect(game_sock, 1110, cipher)
            assert initial_world[1] == 58 and initial_world[3] == '长安', initial_world

            game_sock.sendall(cipher.encrypt_frame(encode_frame(1010, [short(7), integer(580005)])))
            kunlun_world = expect(game_sock, 1110, cipher)
            assert kunlun_world[1] == 60001 and kunlun_world[3] == '昆仑', kunlun_world

            game_sock.sendall(cipher.encrypt_frame(encode_frame(1010, [short(12), integer(0)])))
            kunlun_data = [receive_frame(game_sock, cipher) for _ in range(7)]
            assert [frame[0] for frame in kunlun_data] == [1010, 1407, 1407, 1407, 1407, 1407, 1010], kunlun_data

            game_sock.sendall(cipher.encrypt_frame(encode_frame(1010, [short(13), integer(0)])))
            kunlun_enter = [receive_frame(game_sock, cipher) for _ in range(6)]
            assert [frame[1][5] for frame in kunlun_enter[:3]] == [13, 14, 105], kunlun_enter
            assert kunlun_enter[0][1][4] == 1, kunlun_enter[0]
            assert kunlun_enter[3][0] == 1126 and kunlun_enter[3][1][2] == 6000101, kunlun_enter[3]
            assert kunlun_enter[4][0] == 2030 and kunlun_enter[4][1][0] == 1900101, kunlun_enter[4]
            assert kunlun_enter[4][1][6] == '昆仑导师', kunlun_enter[4]

            game_sock.sendall(cipher.encrypt_frame(encode_frame(2031, [
                integer(1900101), integer(0), short(12), short(8), short(0), short(0)
            ])))
            mentor_dialogue = expect(game_sock, 2032, cipher)
            assert mentor_dialogue[:2] == [1900101, 4], mentor_dialogue
            assert mentor_dialogue[14:17] == [1, 2, '学习门派技能'], mentor_dialogue

            game_sock.sendall(cipher.encrypt_frame(encode_frame(2032, [
                byte(1), byte(101), string('')
            ])))
            mentor_ack = expect(game_sock, 1010, cipher)
            mentor_screen = expect(game_sock, 1010, cipher)
            assert mentor_ack == [0, 0, 0, 0, 0, 7], mentor_ack
            assert mentor_screen == [179, 0, 0, 0, 1, 69], mentor_screen

            game_sock.sendall(cipher.encrypt_frame(encode_frame(1010, [short(7), integer(6000101)])))
            returned_world = expect(game_sock, 1110, cipher)
            assert returned_world[1] == 58 and returned_world[3] == '长安', returned_world
            print('OK: 长安 -> 昆仑 -> 昆仑导师学习模式 -> 长安')
            return

        if args.exercise_skill_only:
            assert current_skill_level is not None, 'selected role does not expose the local sect skill'
            game_sock.sendall(cipher.encrypt_frame(encode_frame(1103, [
                byte(2), integer(10001), byte(current_skill_level), byte(1), byte(1)
            ])))
            detail = expect(game_sock, 1103, cipher)
            assert detail[:3] == [2, 10001, current_skill_level] and len(detail) == 14, detail
            assert detail[11:] == [0, '', 0], detail

            game_sock.sendall(cipher.encrypt_frame(encode_frame(1103, [byte(3), integer(10001)])))
            refreshed = expect(game_sock, 1103, cipher)
            expected_skill_level = min(20, current_skill_level + 1)
            assert refreshed[:5] == [0, 1, '协议测试技能', 10001, expected_skill_level], refreshed
            assert expect(game_sock, 1103, cipher) == [5], 'sect skill redraw'
            refreshed_character = expect(game_sock, 1132, cipher)
            assert refreshed_character[:5] == [0, 1, '协议测试技能', 10001, expected_skill_level], refreshed_character
            print('OK')
            return

        weapon_id = int(items['青锋剑'][1])
        potion_id = int(items['小还丹'][1])
        mount_token_id = int(items['辟邪'][1])
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
            assert equip_ack == [5], equip_ack
            # The server sends a minimal single-property change frame only when
            # the appearance actually differs; otherwise it falls back to the
            # full locked-appearance refresh. Mirror that decision from the
            # authoritative appearance so either legal response is validated.
            if appearance[property_index] != value:
                assert_minimal_change(equipped_appearance, role_id, property_index, value)
            else:
                assert_full_refresh(equipped_appearance, role_id, appearance)
            appearance[property_index] = value

            game_sock.sendall(cipher.encrypt_frame(encode_frame(1009, [short(6), integer(item_id)])))
            unequipped = expect(game_sock, 1008, cipher)
            unequip_ack = expect(game_sock, 1009, cipher)
            restored_appearance = expect(game_sock, 1017, cipher)
            assert unequipped[0:5] == [3, item_id, 1, 1, 50], unequipped
            assert unequip_ack == [6], unequip_ack
            if appearance[property_index] != 0:
                assert_minimal_change(restored_appearance, role_id, property_index, 0)
            else:
                assert_full_refresh(restored_appearance, role_id, appearance)
            appearance[property_index] = 0

        # The six APK-defined accessory slots have no independent character
        # sprite property, so their equipment-vector move must still update
        # the equipment panel immediately on both equip and unequip. Because
        # no sprite property changes, the server always returns the full
        # locked-appearance refresh.
        for name, slot in icon_only_slots.items():
            item_id = int(items[name][1])
            game_sock.sendall(cipher.encrypt_frame(encode_frame(1009, [short(5), integer(item_id)])))
            equipped = expect(game_sock, 1008, cipher)
            equip_ack = expect(game_sock, 1009, cipher)
            panel_refresh = expect(game_sock, 1017, cipher)
            assert equipped[0:5] == [3, item_id, 1, 1, slot], equipped
            assert equip_ack == [5], equip_ack
            assert_full_refresh(panel_refresh, role_id, appearance)

            game_sock.sendall(cipher.encrypt_frame(encode_frame(1009, [short(6), integer(item_id)])))
            unequipped = expect(game_sock, 1008, cipher)
            unequip_ack = expect(game_sock, 1009, cipher)
            panel_refresh = expect(game_sock, 1017, cipher)
            assert unequipped[0:5] == [3, item_id, 1, 1, 50], unequipped
            assert unequip_ack == [6], unequip_ack
            assert_full_refresh(panel_refresh, role_id, appearance)

        game_sock.sendall(cipher.encrypt_frame(encode_frame(1009, [short(4), integer(potion_id)])))
        used = expect(game_sock, 1008, cipher)
        login_quantity = int(items['小还丹'][2])
        assert used[0:2] == [3, potion_id], used
        assert used[2] == max(0, login_quantity - 1), (used, login_quantity)
        first_ack = expect(game_sock, 1009, cipher)
        if first_ack == [3, potion_id]:
            # Using the last potion exhausts the stack, so the server removes
            # the item and issues a discard ack before the use ack.
            use_ack = expect(game_sock, 1009, cipher)
        else:
            use_ack = first_ack
        assert use_ack == [4], use_ack

        # The APK has a dedicated equipment-panel mount slot (position 17).
        # Equip/unequip use the same 1008/1009 flow as the other equipment,
        # plus property 22 to redraw the character page and map sprite.
        game_sock.sendall(cipher.encrypt_frame(encode_frame(1009, [short(5), integer(mount_token_id)])))
        mounted_item = expect(game_sock, 1008, cipher)
        mount_ack = expect(game_sock, 1009, cipher)
        mounted = expect(game_sock, 1017, cipher)
        assert mounted_item[0:2] == [3, mount_token_id] and mounted_item[4] == 17, mounted_item
        assert mount_ack == [5] and mounted == [0, role_id, 1, 22, 105000], (mount_ack, mounted)

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
        assert world[1] == 58 and world[3] == '长安', world

        game_sock.sendall(cipher.encrypt_frame(encode_frame(1010, [short(12), integer(0)])))
        received = [receive_frame(game_sock, cipher) for _ in range(7)]
        assert [x[0] for x in received] == [1010, 1407, 1407, 1407, 1407, 1407, 1010], received
        assert received[-1][1][5] == 12 and received[-1][1][4] == 1, received[-1]

        game_sock.sendall(cipher.encrypt_frame(encode_frame(1010, [short(13), integer(4964)])))
        # Map 58 advertises the monster and three generic 1126 portals, then
        # three native 2030 NPCs and one direction frame per generic actor.
        entered = [receive_frame(game_sock, cipher) for _ in range(14)]
        assert [x[1][5] for x in entered[:3]] == [13, 14, 105], entered
        assert entered[3][0] == 1126 and entered[3][1][:2] == [0, 1], entered[3]
        assert entered[4][0] == 1126 and entered[4][1][2] == 580001, entered[4]
        assert entered[5][0] == 1126 and entered[5][1][2] == 580003, entered[5]
        assert entered[5][1][3] == 34 and entered[5][1][4] == 7, entered[5]
        assert entered[6][0] == 1126 and entered[6][1][2] == 580005, entered[6]
        assert entered[6][1][3] == 62 and entered[6][1][4] == 67, entered[6]
        assert entered[7][0] == 2030 and entered[7][1][0] == 1900002, entered[7]
        assert entered[7][1][1] == 50 and entered[7][1][2] == 64, entered[7]
        assert entered[7][1][6] == '孙思邈', entered[7]
        assert entered[8][0] == 2030 and entered[8][1][0] == 1900003, entered[8]
        assert entered[8][1][1] == 34 and entered[8][1][2] == 50, entered[8]
        assert entered[8][1][6] == '接引真人', entered[8]
        assert entered[9][0] == 2030 and entered[9][1][0] == 1900004, entered[9]
        assert entered[9][1][1] == 11 and entered[9][1][2] == 21, entered[9]
        assert entered[9][1][6] == '赵公明', entered[9]
        assert [frame[1][2] for frame in entered[10:14]] == [1900001, 580001, 580003, 580005], entered[10:14]

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
            level = int(player_properties[11])
            player_max_hp = int(player_properties[40])
            player_attack = 10 + int(player_properties[44]) + ((level - 1) * 2)
            player_defence = int(player_properties[45]) + (level - 1)
            monster_damage = max(1, 10 - (player_defence // 2))
            defended_damage = max(1, monster_damage // 2)
            assert player_actor[3] == player_max_hp, player_actor
            assert player_actor[10:12] == [player_max_hp, player_max_hp], player_actor
            monster_start = expect(game_sock, 1040, cipher)
            assert monster_start[0:2] == [1, 1], monster_start

            # Defence command 2 consumes the player's action, leaves monster HP
            # untouched and halves the already-armour-reduced counterattack.
            game_sock.sendall(cipher.encrypt_frame(encode_frame(1041, [
                integer(2), byte(1), integer(role_id), integer(1), integer(0), integer(0), integer(0), integer(0)
            ])))
            defend_action = expect(game_sock, 1042, cipher)
            assert defend_action[0:6] == [1, role_id, role_id, 2, 1, 0], defend_action
            assert defend_action[9] == 0, defend_action
            defended_counter = expect(game_sock, 1042, cipher)
            assert defended_counter[9:] == [1, role_id, 0, 22, -defended_damage, ''], defended_counter
            defend_round = expect(game_sock, 1040, cipher)
            assert defend_round[0:2] == [2, 1], defend_round
            game_sock.sendall(cipher.encrypt_frame(encode_frame(1040, [byte(2), integer(1)])))

            game_sock.sendall(cipher.encrypt_frame(encode_frame(1041, [
                integer(1), byte(2), integer(role_id), integer(1), integer(monster[2]), integer(2), integer(0), integer(0)
            ])))
            player_action = expect(game_sock, 1042, cipher)
            assert player_action[0:6] == [2, role_id, int(monster[2]), 1, 1, 0], player_action
            assert player_action[9:] == [1, int(monster[2]), 0, 22, -player_attack, ''], player_action
            monster_hp = max(0, 100 - player_attack)
            if monster_hp > 0:
                counter_action = expect(game_sock, 1042, cipher)
                assert counter_action[0:6] == [2, int(monster[2]), role_id, 1, 1, 0], counter_action
                assert counter_action[9:] == [1, role_id, 0, 22, -monster_damage, ''], counter_action
            monster_round = expect(game_sock, 1040, cipher)
            assert monster_round[0:2] == [2, 2], monster_round
            # Full action=2 starts playback; the real APK returns the short
            # form only after both native action records have completed.
            game_sock.sendall(cipher.encrypt_frame(encode_frame(1040, [byte(2), integer(2)])))
            if args.exercise_monster_kill:
                # Continue until the panel-derived attack value kills the
                # monster, then verify settlement after the queue-drained ack.
                current_round = 2
                while monster_hp > 0:
                    current_round += 1
                    game_sock.sendall(cipher.encrypt_frame(encode_frame(1041, [
                        integer(1), byte(current_round), integer(role_id), integer(1), integer(monster[2]), integer(2), integer(0), integer(0)
                    ])))
                    repeated_attack = expect(game_sock, 1042, cipher)
                    assert repeated_attack[9:] == [1, int(monster[2]), 0, 22, -player_attack, ''], repeated_attack
                    monster_hp = max(0, monster_hp - player_attack)
                    if monster_hp > 0:
                        repeated_counter = expect(game_sock, 1042, cipher)
                        assert repeated_counter[9:] == [1, role_id, 0, 22, -monster_damage, ''], repeated_counter
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

        if args.exercise_monster_escape:
            monster = entered[3][1]
            contact_x, contact_y = int(monster[3]), int(monster[4])

            def _start_battle():
                # The 2031 object interaction carries the contact tile; the
                # server seeds its battle trace and escape guard from it.
                game_sock.sendall(cipher.encrypt_frame(encode_frame(2031, [
                    integer(monster[2]), integer(0), short(contact_x), short(contact_y), short(6), short(0)
                ])))
                assert expect_tolerant(game_sock, 1040, cipher) == [0], 'battle reset'
                expect_tolerant(game_sock, 1048, cipher)  # player actor
                expect_tolerant(game_sock, 1048, cipher)  # monster actor
                start = expect_tolerant(game_sock, 1040, cipher)
                assert start[0:2] == [1, 1], start

            def _escape() -> list[object]:
                # C->S 1041 command 6 is the APK-confirmed 逃跑 (escape) request:
                # [6, byte(round), player_id, side=1, 0,0,0,0]. Command 10 is a
                # different action (退出观战, quit spectator) and must NOT be sent
                # as a player escape request. The original client first consumes
                # a 1042 action-6 record whose inert effect enters the fighter-exit
                # state machine. Only after its 1040/action=2 playback barrier is
                # acknowledged may the server send 1041 [10, player_id] to close.
                game_sock.sendall(cipher.encrypt_frame(encode_frame(1041, [
                    integer(6), byte(1), integer(role_id), integer(1), integer(0), integer(0), integer(0), integer(0)
                ])))
                escape_action = expect_tolerant(game_sock, 1042, cipher)
                assert escape_action == [
                    1, role_id, role_id, 6, 1, 0, 0, 0, '逃跑',
                    1, role_id, 1, 58, 0, '',
                ], escape_action
                playback = expect_tolerant(game_sock, 1040, cipher)
                assert playback[0:2] == [2, 1], playback
                game_sock.sendall(cipher.encrypt_frame(encode_frame(1040, [byte(2), integer(1)])))
                return expect_tolerant(game_sock, 1041, cipher)

            def _guarded_interaction_ack(expected_object_id: int):
                # b/ab.aj() enables the global wait overlay before sending the
                # automatic 1010/7 re-tap. The guard must acknowledge that
                # request with the complete no-op S->C action-7 record, then
                # remain quiet instead of restarting the battle.
                ack = expect_tolerant(game_sock, 1010, cipher)
                assert ack == [expected_object_id, 0, 0, 0, 0, 7], ack
                game_sock.settimeout(0.6)
                try:
                    while True:
                        id_, values = receive_frame(game_sock, cipher)
                        if id_ != 1012:
                            raise AssertionError(('battle restarted on guarded tile', (id_, values)))
                except socket.timeout:
                    pass
                finally:
                    game_sock.settimeout(None)

            def _move(tx: int, ty: int):
                # Protocol 1005 is the APK's player-movement frame: the first
                # two fields are the current (x, y) tile as shorts. Reaching a
                # different tile than the escape contact clears the guard.
                game_sock.sendall(cipher.encrypt_frame(encode_frame(1005, [
                    short(tx), short(ty), byte(0)
                ])))

            # 开战 -> 逃跑: the original 1042 exit animation and playback barrier
            # finish before the final 1041 close. No victory settlement,
            # 1010/action=18 removal, reward or counterattack follows.
            _start_battle()
            assert _escape() == [10, role_id], 'escape confirmation'

            # guard: the same monster on the same contact tile is suppressed.
            game_sock.sendall(cipher.encrypt_frame(encode_frame(2031, [
                integer(monster[2]), integer(0), short(contact_x), short(contact_y), short(6), short(0)
            ])))
            _guarded_interaction_ack(int(monster[2]))

            # 移动解除: moving off the contact tile clears the guard.
            _move(contact_x + 5, contact_y)

            # 再次开战: the same monster can be engaged again and escaped again.
            _start_battle()
            assert _escape() == [10, role_id], 're-enter escape confirmation'

            # ---- 真机无 tile 路径: 1010/7 + 1005 ----
            # The real device starts battles through 1010 [short(7), int(obj)]
            # which carries NO contact tile, and reports its position with 1005
            # first. This exact ordering previously never armed the guard (it
            # required a contact tile), so the same monster was instantly
            # re-engaged (consecutive BT-...-2/-3/-4/-5 traces). Exercise the
            # corrected guard here.
            obj_id = int(monster[2])

            def _position(tx: int, ty: int):
                game_sock.sendall(cipher.encrypt_frame(encode_frame(1005, [
                    short(tx), short(ty), byte(0)
                ])))

            def _start_battle_1010():
                game_sock.sendall(cipher.encrypt_frame(encode_frame(1010, [short(7), integer(obj_id)])))
                assert expect_tolerant(game_sock, 1040, cipher) == [0], '1010 battle reset'
                expect_tolerant(game_sock, 1048, cipher)  # player actor
                expect_tolerant(game_sock, 1048, cipher)  # monster actor
                start = expect_tolerant(game_sock, 1040, cipher)
                assert start[0:2] == [1, 1], start

            # Release the 2031 guard, then report the standing position before
            # engaging through the tile-less 1010/7 path.
            _move(contact_x + 5, contact_y)
            _position(8, 6)
            _start_battle_1010()
            assert _escape() == [10, role_id], '1010 escape confirmation'
            # Immediate 1010/7 re-tap on the same monster must be suppressed.
            game_sock.sendall(cipher.encrypt_frame(encode_frame(1010, [short(7), integer(obj_id)])))
            _guarded_interaction_ack(obj_id)
            # A real move off the origin tile clears the guard.
            _position(9, 6)
            _start_battle_1010()
            assert _escape() == [10, role_id], '1010 re-enter escape confirmation'

        if args.exercise_portal:
            for forward_portal_id in (580001, 580003):
                game_sock.sendall(cipher.encrypt_frame(encode_frame(1010, [short(7), integer(forward_portal_id)])))
                switched_world = expect(game_sock, 1110, cipher)
                assert switched_world[1] == 50000 and switched_world[3] == '传送测试区', switched_world
                game_sock.sendall(cipher.encrypt_frame(encode_frame(1010, [short(12), integer(0)])))
                switched_data = [receive_frame(game_sock, cipher) for _ in range(7)]
                assert [x[0] for x in switched_data] == [1010, 1407, 1407, 1407, 1407, 1407, 1010], switched_data
                game_sock.sendall(cipher.encrypt_frame(encode_frame(1010, [short(13), integer(0)])))
                switched_enter = [receive_frame(game_sock, cipher) for _ in range(7)]
                assert [x[1][5] for x in switched_enter[:3]] == [13, 14, 105], switched_enter
                assert switched_enter[0][1][4] == 0, switched_enter[0]
                assert switched_enter[4][0] == 1126 and switched_enter[4][1][2] == 580002, switched_enter[4]
                assert [frame[1][2] for frame in switched_enter[5:7]] == [1900001, 580002], switched_enter[5:7]

                game_sock.sendall(cipher.encrypt_frame(encode_frame(1010, [short(7), integer(580002)])))
                returned_world = expect(game_sock, 1110, cipher)
                assert returned_world[1] == 58 and returned_world[3] == '长安', returned_world
                game_sock.sendall(cipher.encrypt_frame(encode_frame(1010, [short(12), integer(0)])))
                returned_data = [receive_frame(game_sock, cipher) for _ in range(7)]
                assert [x[0] for x in returned_data] == [1010, 1407, 1407, 1407, 1407, 1407, 1010], returned_data
                game_sock.sendall(cipher.encrypt_frame(encode_frame(1010, [short(13), integer(4964)])))
                returned_enter = [receive_frame(game_sock, cipher) for _ in range(14)]
                assert [x[1][5] for x in returned_enter[:3]] == [13, 14, 105], returned_enter
                assert returned_enter[0][1][4] == 0, returned_enter[0]
                assert returned_enter[4][0] == 1126 and returned_enter[4][1][2] == 580001, returned_enter[4]
                assert returned_enter[5][0] == 1126 and returned_enter[5][1][2] == 580003, returned_enter[5]
                assert returned_enter[6][0] == 1126 and returned_enter[6][1][2] == 580005, returned_enter[6]
                assert returned_enter[7][0] == 2030 and returned_enter[7][1][0] == 1900002, returned_enter[7]
                assert returned_enter[7][1][6] == '孙思邈', returned_enter[7]
                assert returned_enter[8][0] == 2030 and returned_enter[8][1][0] == 1900003, returned_enter[8]
                assert returned_enter[8][1][6] == '接引真人', returned_enter[8]
                assert returned_enter[9][0] == 2030 and returned_enter[9][1][0] == 1900004, returned_enter[9]
                assert returned_enter[9][1][6] == '赵公明', returned_enter[9]

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
