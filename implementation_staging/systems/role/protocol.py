
from __future__ import annotations

from protocol import byte, encode_frame, integer, short, string

def creation_names() -> bytes:
    # 创建界面当前种族有男女两个分支，因此 action=4 后固定读取两个名字。
    return encode_frame(1080, [short(4), string(''), string('')])



def deletion_result(role_id: int) -> bytes:
    return encode_frame(1080, [short(1), integer(role_id)])



def character_extension_info() -> bytes:
    """Initialize the optional rows consumed by the character base page.

    The original client keeps these rows in ``pmsj.work.b.f.u``.  That field
    starts as null and the base page calls ``size()`` without checking it, so
    protocol 1089/action 0 must be delivered even when there are no rows.
    """
    return encode_frame(1089, [byte(0), byte(0)])

# ---------------------------------------------------------------------------
# 角色协议帧：登录、账号、门派、外观、邮件、坐骑与登出（自 server.py 迁入）。
# ---------------------------------------------------------------------------
import logging
import time

from systems.fuyuan import service as fuyuan
from systems.inventory.service import bag_capacity, is_equipment, role_items
from systems.skill.service import ensure_life_skills
from protocol import (
    Field, TYPE_BYTE, TYPE_INT, TYPE_SHORT,
    binary, byte, encode_frame, integer, long_integer, short, string,
)
from systems.inventory.registry import (
    ItemRegistry, armor_property2_from_equipment,
    armor_property2_from_icon, battle_weapon_image_from_icon,
    default_item_registry, helmet_property20_from_icon,
    normalized_strengthen_level, weapon_appearance_field_from_icon_and_strengthen,
    weapon_icon_to_image_mapping,
)
from systems.role.registry import mount_ride_code_for_role
from systems.role.service import (
    CURRENCY_PROPERTIES, _get_sect_skill_level, default_role,
    effective_character_stats, level_experience_required, role_level_properties,
    normalized_currency_balance, normalized_sect_id,
)

LOG = logging.getLogger('piaomiao-local')

# Opening the main function menu makes this client prefetch several optional
# systems (tasks, instances and activities). Their response dispatchers all
# release the same global waiting state even when the subtype is not handled.
# Use deliberately unhandled subtypes so an unavailable system behaves as an
# empty module without constructing a screen that expects additional fields.
MENU_PREFETCH_EMPTY_SUBTYPES = {
    # In the active client, subtype 2 opens a panel and immediately reads a
    # multi-field payload.  Subtype 0 is intentionally unhandled and safely
    # releases the menu's loading state with this one-field empty response.
    1090: 0,
    1153: 0,
    1061: 3,
}
# APK-confirmed in-game logout flow (reverse-engineered; 1074 is NOT logout):
#   C->S 1054 [BYTE 8] opens the logout page;
#   S->C 1054 [BYTE 8, BYTE flag, STRING text] renders it;
#   C->S 1003 [INT 0] confirms logout (INT, never byte);
#   S->C 1003 [BYTE 0] acknowledges, then the client closes the connection
#   itself after about one second. The server must not hard-close the socket.
LOGOUT_PAGE_TEXT = '是否确认退出游戏？'


def logout_page_frame(
    text: str = LOGOUT_PAGE_TEXT,
    flag: int = 0,
) -> bytes:
    """S->C 1054 logout page: BYTE 8, BYTE flag, STRING text."""
    return encode_frame(1054, [
        byte(8),
        byte(flag),
        string(text),
    ])


def logout_ack_frame() -> bytes:
    """S->C 1003 clean-logout acknowledgement: a single BYTE 0."""
    return encode_frame(1003, [byte(0)])


def is_logout_page_request(fields: list[Field]) -> bool:
    """True only for the APK's exact 1054 open-logout-page request: BYTE 8.

    The TLV type must be BYTE (type_id 2): an INT 8 or STRING '8' is a
    different request and must never open the logout page.
    """
    return bool(
        len(fields) >= 1
        and fields[0].type_id == TYPE_BYTE
        and fields[0].value == 8
    )


def is_logout_confirm_request(fields: list[Field]) -> bool:
    """True only for the APK's exact 1003 logout-confirm request: INT 0.

    The TLV type must be INT (type_id 4): a BYTE 0 is a different request
    and must never trigger the clean-logout save/ack path.
    """
    return bool(
        len(fields) >= 1
        and fields[0].type_id == TYPE_INT
        and fields[0].value == 0
    )
def menu_prefetch_empty_ack(message_id: int) -> bytes:
    try:
        subtype = MENU_PREFETCH_EMPTY_SUBTYPES[message_id]
    except KeyError as exc:
        raise ValueError(f'unsupported menu prefetch protocol: {message_id}') from exc
    return encode_frame(message_id, [byte(subtype)])
def mail_request_frames(
    role: dict[str, object],
    values: list[object],
) -> tuple[list[bytes], bool]:
    """Handle the APK's minimal protocol-1500 inbox flow."""
    action = int(values[0]) if values else -1
    mailbox = role.get('mailbox', [])
    messages = [message for message in mailbox if isinstance(message, dict)] if isinstance(mailbox, list) else []
    if action == 13 and len(values) > 1:
        mail_id = int(values[1])
        message = next(
            (candidate for candidate in messages if int(candidate.get('id', 0)) == mail_id),
            None,
        )
        if message is None:
            return [], False
        changed = not bool(message.get('read', False))
        message['read'] = True
        detail = [
            byte(14),
            integer(mail_id),
            integer(0),
            byte(0),
            integer(0),
            short(0),
            short(0),
            string(str(message.get('subject', ''))),
            string(str(message.get('body', ''))),
            string(
                f"{message.get('sent_at', '')}_{message.get('expires_at', '长期有效')}"
            ),
            byte(0),
        ]
        return [encode_frame(1500, detail)], changed
    if action == 16 and len(values) > 1:
        mail_id = int(values[1])
        remaining = [
            message for message in messages
            if int(message.get('id', 0)) != mail_id
        ]
        if len(remaining) == len(messages):
            return [], False
        role['mailbox'] = remaining
        page_count = 1 if remaining else 0
        return [
            encode_frame(1500, [byte(16), short(page_count), integer(mail_id)])
        ], True
    if action != 12:
        return [], False

    records: list[Field] = []
    for message in messages:
        flags = 1 if bool(message.get('read', False)) else 0
        records.extend([
            integer(int(message.get('id', 0))),
            integer(0),
            integer(0),
            string(str(message.get('sender', '系统'))),
            string(str(message.get('subject', ''))),
            byte(flags),
            string(str(message.get('expires_at', '长期有效'))),
        ])
    return [encode_frame(1500, [byte(11), short(1), byte(len(messages)), *records])], False
# The player sprite is composed from independently replaceable image layers.
# Property 2 is the armor/body layer and resolves to image 14000..14030.
# Property 7 is the weapon; properties 14..20 are other independent overlays.
# Slot-3 armor must never be routed through legacy property15.
BASE_CHARACTER_APPEARANCE = {
    2: 0,   # 铠甲主体：property2 -> image 14000..14030
    7: 0,
    14: 0,
    15: 0,
    16: 0,
    17: 0,
    18: 0,
    19: 0,
    20: 0,
}
def login_server_list(settings: Settings) -> bytes:
    # 服务器状态索引：0=维护、1=良好、2=繁忙、3=爆满。
    fields = [
        byte(0),
        string(''),
        byte(1),
        string(settings.server_name),
        string(f'{settings.advertise_host}:{settings.port}'),
        byte(1),
        byte(1),
    ]
    return encode_frame(1077, fields)


def account_result(code: int, message: str = '') -> bytes:
    return encode_frame(1055, [byte(code), string(message)])


def game_server_redirect(settings: Settings, session_id: int, account_id: int) -> bytes:
    # 客户端收到 1052 后会关闭登录连接，再连接这里给出的游戏服地址，
    # 并在新连接中发送同为 1052 的 session/account 两个整数。
    return encode_frame(1052, [
        integer(session_id),
        integer(account_id),
        integer(settings.port),
        string(settings.advertise_host),
        byte(66),
        byte(49),
    ])


def role_list(settings: Settings, roles: list[dict[str, object]] | None = None) -> bytes:
    roles = roles if roles is not None else [default_role(settings)]
    records = []
    preview_properties = (2, 14, 15, 16, 17, 18, 19, 20)
    for role in roles:
        race = int(role.get('race', 0))
        gender = int(role.get('gender', 0))
        appearance = character_appearance(role, settings.item_registry)
        record = [
            integer(int(role['id'])),
            # APK main/e.K: field 1 -> character property 11 (level).
            integer(int(role.get('level', 1))),
            # field 2 -> property7 and v.e(I): current equipped weapon preview.
            integer(int(appearance.get(7, 0))),
            integer(int(role.get('model', settings.role_model))),
            # APK main/e.K splits this field as property12=value/10 (sect)
            # and property39=value%10 (race). Gender comes from the model.
            integer((normalized_sect_id(role, settings.sect_registry) * 10) + race),
            string(str(role.get('name', settings.role_name))),
            integer(int(role.get('slot', 0))),
        ]
        # Fields 7..14 are not role stats.  main/e.K feeds them directly to
        # v.d/z/A/B/C/D/E/F, i.e. armor body and the seven visible overlays.
        record.extend(integer(int(appearance.get(index, 0))) for index in preview_properties)
        records.extend(record)
    # S->C action is SHORT while the C->S 1080 request action is BYTE.
    return encode_frame(1080, [short(0), byte(len(roles)), *records])


def role_creation_frames(
    settings: Settings,
    roles: list[dict[str, object]],
) -> tuple[bytes, ...]:
    """Creation returns to the role page; entering remains an explicit choice."""
    return (role_list(settings, roles),)



def player_info(settings: Settings, role: dict[str, object] | None = None) -> bytes:
    role = role if role is not None else default_role(settings)
    properties = role_property_fields(settings, role)
    return encode_frame(1006, [
        integer(len(properties)),
        *properties,
        integer(int(time.time())),
    ])


def role_property_fields(settings: Settings, role: dict[str, object]) -> list:
    """Build the 85-slot character property table shared by 1006 and 1014.

    The APK keeps one property bag per character (pmsj.work.b.v.a(B,Object));
    1006 prefixes a count field while the 1014 handler (main/e.T) consumes the
    fields directly as property slots, so this table stays index-exact.
    """
    # 1006 的第 0 字段是连续属性数量。地图只会读取前 30 项，但人物
    # 面板会继续读取到属性 84（斗法排行），所以发送完整的 0..84 表。
    properties = [integer(0) for _ in range(85)]
    properties[1] = integer(int(role['id']))
    properties[3] = string(str(role.get('name', settings.role_name)))
    properties[6] = integer(int(role.get('model', settings.role_model)))
    properties[10] = string('')
    properties[11] = integer(int(role.get('level', 1)))
    # property 12 = 门派 ID; property 39 = 种族 ID.
    properties[12] = integer(normalized_sect_id(role, settings.sect_registry))
    # Item icons/templates and character image layers are separate catalogues.
    # Only verified appearance pairs are applied here.
    for property_index, value in character_appearance(role, settings.item_registry).items():
        properties[property_index] = integer(value)
    # Property 21 is the gang position slot the APK reads through b/v.W()
    # (0=无帮派, 200=帮众, 1000=帮主) to branch the main-menu gang entry.
    properties[21] = integer(int(role.get('gang_position', 0) or 0))
    properties[23] = integer(1000)
    properties[22] = integer(mount_ride_code_for_role(role, settings.item_registry))
    properties[24] = integer(fuyuan.tier(role))
    properties[25] = integer(0)
    level = max(1, int(role.get('level', 1)))
    experience = max(0, int(role.get('experience', 0)))
    properties[31] = long_integer(experience)
    properties[32] = long_integer(max(100, level * 100))
    properties[38] = integer(0)
    properties[39] = integer(int(role.get('race', 0)))

    level = max(1, int(role.get('level', 1)))
    raw_stats = [int(value) for value in list(role.get('stats', []))]
    base_stats = [max(0, value) for value in (raw_stats + [10, 10, 10, 10, 10])[:5]]
    display_stats = effective_character_stats(role, settings.item_registry)
    max_hp = fuyuan.hp_limit(role, 100 + ((level - 1) * 10) + base_stats[1])
    max_mp = 50 + ((level - 1) * 5) + base_stats[2]
    properties[40] = integer(max_hp)
    properties[41] = integer(max_hp)
    properties[42] = integer(max_mp)
    properties[43] = integer(max_mp)
    for index, value in enumerate(display_stats, start=44):
        properties[index] = integer(max(0, value))

    properties[49] = integer(0)
    currencies = role.get('currencies', {})
    if not isinstance(currencies, dict):
        currencies = {}
    for name, property_index in CURRENCY_PROPERTIES.items():
        properties[property_index] = integer(
            normalized_currency_balance(currencies.get(name))
        )
    properties[54] = string('无')
    # Properties 55-58 are the life-skill stamina/vitality pair; the role
    # state in role['life_skills'] is the single truth, migrated on load.
    life_state = ensure_life_skills(role, settings.life_registry) if role is not None else None
    properties[55] = integer(int(life_state.get('stamina', 100)) if life_state else 100)
    properties[56] = integer(int(life_state.get('stamina_max', 100)) if life_state else 100)
    properties[57] = integer(int(life_state.get('vitality', 100)) if life_state else 100)
    properties[58] = integer(int(life_state.get('vitality_max', 100)) if life_state else 100)
    # APK pmsj/work/b/ab.g() reads character property 62 as the personal
    # inventory capacity. Property 59 is the separate warehouse capacity and
    # deliberately remains untouched while warehouse support is out of scope.
    properties[62] = integer(bag_capacity(role))
    # The original item subclass gates the weapon "装备" menu through
    # character property 63 (weapon-family permission bitmask).  Bit 0 is
    # the starter weapon family used by template 100001001; leaving this
    # property at zero makes armour look normal but hides the weapon action.
    properties[63] = integer(1)
    properties[75] = integer(0)
    properties[77] = integer(0)
    properties[78] = integer(100)
    properties[79] = string('无')
    properties[80] = integer(level)
    properties[82] = integer(300)
    properties[83] = integer(300)
    properties[84] = integer(0)
    return properties


def player_appear_frame(
    settings: Settings,
    role: dict[str, object],
    actor_id: int,
    x: int,
    y: int,
) -> bytes:
    """Native S->C 1014 "other player appears" frame (pmsj.work.main.e.T).

    T reads the map actor id from field 1 (guarded against the receiver's own
    role id), the tile from integer fields 4/5, the overlay seed from field 6,
    and the sprite family from H(field 22) — the same mount ride code the self
    1006 carries. Every field is copied into the b/v property bag by index, so
    this reuses the verified 1006 property table with the actor id swapped for
    1_000_000 + role_id (1005 b/v walks and 1010/action=18 removal range).
    """
    properties = role_property_fields(settings, role)
    properties[1] = integer(int(actor_id))
    properties[4] = integer(int(x))
    properties[5] = integer(int(y))
    return encode_frame(1014, properties)


def sect_skill_list(role: dict[str, object], settings: Settings) -> bytes:
    """Return the protocol-1103 list for the role's sect skills."""
    sect_id = normalized_sect_id(role, settings.sect_registry)
    skills = settings.sect_registry.skills_for_sect(sect_id)

    if not skills:
        LOG.info(
            'SKILL_1103_LIST role_id=%s sect_id=%d count=0 (no skills for this sect)',
            role.get('id', 0), sect_id,
        )
        return encode_frame(1103, [byte(0), byte(0)])

    records = []
    for slot, skill_def in enumerate(skills, start=1):
        level = _get_sect_skill_level(role, skill_def.skill_id, settings)
        record = [
            string(skill_def.name),
            integer(skill_def.skill_id),
            integer(level),
            integer(skill_def.max_level),
            integer(skill_def.icon),  # field[4]: icon code
            *(integer(0) for _ in range(7)),
            integer(slot),  # field[12]: native sect-skill slot, 1..14.
            integer(0),
        ]
        records.append(record)

    LOG.info(
        'SKILL_1103_LIST role_id=%s sect_id=%d count=%d',
        role.get('id', 0), sect_id, len(skills),
    )
    return encode_frame(1103, [byte(0), byte(len(skills)), *[field for record in records for field in record]])



def sect_skill_detail_frame(role: dict[str, object], skill_id: int, settings: Settings) -> bytes:
    """Answer the native 1103/action-2 skill detail and learning-condition query.

    ``pmsj/work/e/dy.a(main/w)`` reads the first three fields as
    ``action, skill id, current level``.  It then consumes five integer
    conditions, effect/current/next strings, and the required-item
    ``int, string, int`` triple.  Returning nothing leaves the client's
    global wait flag set.
    """
    sect_id = normalized_sect_id(role, settings.sect_registry)
    skill = settings.sect_registry.skill(skill_id)

    if skill is None:
        LOG.warning(
            'SECT_SKILL_DETAIL_REJECT role_id=%s sect_id=%d skill_id=%d reason=unknown_skill',
            role.get('id', 0), sect_id, skill_id,
        )
        return encode_frame(1103, [byte(3)])

    if not settings.sect_registry.skill_belongs_to_sect(skill_id, sect_id):
        LOG.warning(
            'SECT_SKILL_DETAIL_REJECT role_id=%s sect_id=%d skill_id=%d reason=wrong_sect',
            role.get('id', 0), sect_id, skill_id,
        )
        return encode_frame(1103, [byte(3)])

    level = _get_sect_skill_level(role, skill_id, settings)
    return encode_frame(1103, [
        byte(2),
        integer(skill_id),
        integer(level),
        integer(skill.required_role_level),
        integer(skill.silver_base),
        integer(skill.experience_base),
        integer(0),  # First prerequisite-skill level.
        integer(0),  # Second prerequisite-skill level.
        string(skill.effect),
        string(skill.current_text),
        string(skill.next_text),
        integer(skill.required_item_id),
        string(skill.required_item_name),
        integer(skill.required_item_count),
    ])

def character_panel_frames(
    role: dict[str, object],
    registry: ItemRegistry | None = None,
) -> tuple[bytes, bytes]:
    """Return live attribute and divine-power datasets requested by UI 31."""
    level = max(1, int(role.get('level', 1)))
    raw_stats = [int(value) for value in list(role.get('stats', []))]
    base_stats = [max(0, value) for value in (raw_stats + [10, 10, 10, 10, 10])[:5]]
    display_stats = effective_character_stats(role, registry)
    max_hp = fuyuan.hp_limit(role, 100 + ((level - 1) * 10) + base_stats[1])
    max_mp = 50 + ((level - 1) * 5) + base_stats[2]

    attribute_thresholds = [max_hp, max_mp, *display_stats]
    attributes = encode_frame(1039, [byte(1), *(integer(value) for value in attribute_thresholds)])

    divine_values = [int(role['id']), level, level, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    divine = encode_frame(1039, [byte(2), *(integer(value) for value in divine_values)])
    return attributes, divine


def character_appearance(
    role: dict[str, object],
    registry: ItemRegistry | None = None,
) -> dict[int, int]:
    """Return the effective verified character-layer properties for a role."""
    properties = dict(BASE_CHARACTER_APPEARANCE)
    for item in role_items(role):
        if item.get('location') != 'equipped' or not is_equipment(item):
            continue
        resolved = registry.resolve(item) if registry is not None else item
        slot = int(resolved.get('equipment_slot', 0))
        if slot == 1:
            # 头盔只从 helmet_appearance_mapping.json 取 property20；未知映射不猜。
            properties[20] = helmet_property20_from_icon(
                int(resolved.get('icon_code', 0)),
            )
        if slot == 3:
            # 铠甲只从 armor_appearance_mapping.json 取 property2；未知映射不猜。
            armor_value = armor_property2_from_equipment(
                int(resolved.get('template_id', 0)),
                int(resolved.get('icon_code', 0)),
            )
            if armor_value is not None:
                properties[2] = int(armor_value)
        if slot == 10:
            # 武器主体来自 icon 映射；外部炫光只由实例强化等级控制。
            # +0..+3 无炫光，+4..+9 对应 APK 六档效果 1..6。
            properties[7] = weapon_appearance_field_from_icon_and_strengthen(
                int(resolved.get('icon_code', 0)),
                normalized_strengthen_level(resolved),
            )
        appearance = resolved.get('appearance_properties', {})
        if not isinstance(appearance, dict):
            continue
        for property_index, value in appearance.items():
            index = int(property_index)
            if slot == 1 and index == 20:
                # 头盔 property20 以资料库映射为准，模板硬编码不覆盖。
                continue
            if slot == 3 and index in {2, 15}:
                # 旧铠甲 property15 以及模板内硬编码 property2 都不得覆盖资料库。
                continue
            if slot == 10 and index == 7:
                # 模板中的静态 quality 外观不得覆盖实例强化等级生成的武器效果。
                continue
            if index in BASE_CHARACTER_APPEARANCE:
                properties[index] = int(value)
    return properties


def map_player_appearance_debug(
    role: dict[str, object],
    settings: Settings | None = None,
) -> dict[str, object]:
    """Return the current-player map appearance values sent through 1006.

    This snapshot is read-only.  It does not encode a frame and must not be
    used to decide protocol field values.
    """
    appearance = character_appearance(role, settings.item_registry if settings is not None else None)
    model = int(role.get('model', settings.role_model if settings is not None else 0))
    return {
        'role_id': int(role.get('id', 0)),
        'role_name': str(role.get('name', '')),
        'model': model,
        'race': int(role.get('race', 0)),
        'gender': int(role.get('gender', 0)),
        'properties': {
            6: model,
            7: int(appearance.get(7, 0)),
            14: int(appearance.get(14, 0)),
            15: int(appearance.get(15, 0)),
            16: int(appearance.get(16, 0)),
            17: int(appearance.get(17, 0)),
            18: int(appearance.get(18, 0)),
            19: int(appearance.get(19, 0)),
            20: int(appearance.get(20, 0)),
        },
    }


def format_map_player_appearance_log(
    username: str,
    role: dict[str, object],
    settings: Settings | None = None,
) -> str:
    """Format the MAP_PLAYER_APPEARANCE diagnostic block."""
    snapshot = map_player_appearance_debug(role, settings)
    properties = snapshot['properties']
    assert isinstance(properties, dict)
    return (
        "MAP_PLAYER_APPEARANCE\n"
        f"user={username!r}\n"
        f"role_id={snapshot['role_id']}\n"
        f"name={snapshot['role_name']!r}\n"
        f"model={snapshot['model']}\n"
        f"race={snapshot['race']}\n"
        f"gender={snapshot['gender']}\n"
        "properties={\n"
        f"  6: {properties[6]},\n"
        f"  7: {properties[7]},\n"
        f"  14: {properties[14]},\n"
        f"  15: {properties[15]},\n"
        f"  16: {properties[16]},\n"
        f"  17: {properties[17]},\n"
        f"  18: {properties[18]},\n"
        f"  19: {properties[19]},\n"
        f"  20: {properties[20]}\n"
        "}"
    )


def character_appearance_frame(role_id: int, properties: dict[int, int]) -> bytes:
    """Encode the client's protocol-1017 incremental character update.

    ``pmsj.work.main.e.O`` reads field 1 as the target role id, field 2 as
    the pair count, then byte/int property pairs beginning at field 3. Field 0
    is the unused update subtype retained by the original wire layout.
    """
    fields = [byte(0), integer(role_id), integer(len(properties))]
    for property_index, value in sorted(properties.items()):
        fields.extend((byte(property_index), integer(value)))
    return encode_frame(1017, fields)

def battle_progress_frame(role: dict[str, object]) -> bytes:
    """Incrementally refresh level/experience after a battle reward.

    ``1006`` is the APK's full login-time user initializer: receiving it
    destroys and recreates the local player and immediately starts the map
    entry handshake. Battle settlement must instead use the verified ``1017``
    character-property update layout consumed by ``main/e.O``.
    """
    properties = role_level_properties(role)
    fields = [byte(0), integer(int(role['id'])), integer(len(properties))]
    for property_index, value in sorted(properties.items()):
        fields.extend((
            byte(property_index),
            # 1017 carries the low words as int fields.  APK ``main/e.O``
            # consumes 85/86 as the corresponding high words and rebuilds
            # properties 31/32 as Long values.
            integer(value),
        ))
    return encode_frame(1017, fields)

def mount_update_frame(role: dict[str, object]) -> bytes:
    """Update the APK's mount/transform property (1006/1017 property 22)."""
    return character_appearance_frame(
        int(role['id']),
        {22: int(role.get('mount_model', 0))},
    )

def character_appearance_change_frame(
    role: dict[str, object],
    previous: dict[int, int],
    registry: ItemRegistry | None = None,
) -> bytes | None:
    current = character_appearance(role, registry)
    changed = {
        property_index: current[property_index]
        for property_index in current
        if previous.get(property_index) != current[property_index]
    }
    if not changed:
        return None
    return character_appearance_frame(int(role['id']), changed)


def equipment_panel_refresh_frame(
    role: dict[str, object],
    registry: ItemRegistry | None = None,
) -> bytes:
    """Enter the APK's verified 1017 redraw callback with the full appearance."""
    return character_appearance_frame(int(role['id']), character_appearance(role, registry))


def character_equipment_refresh_frames(
    role: dict[str, object],
    registry: ItemRegistry | None = None,
) -> tuple[bytes, bytes]:
    """Refresh world appearance plus the open character panel after equipment changes.

    ``main/e.O`` applies 1017 property pairs to the live world character and
    invokes the native dependent-UI redraws. ``main/e.ae`` action 1 is the
    character-panel data path and redraws UI 0x166 when that panel is open.
    """
    if registry is None:
        registry = default_item_registry()
    level = max(1, int(role.get('level', 1)))
    raw_stats = [int(value) for value in list(role.get('stats', []))]
    base_stats = [max(0, value) for value in (raw_stats + [10, 10, 10, 10, 10])[:5]]
    display_stats = effective_character_stats(role, registry)
    max_hp = fuyuan.hp_limit(role, 100 + ((level - 1) * 10) + base_stats[1])
    max_mp = 50 + ((level - 1) * 5) + base_stats[2]

    properties = character_appearance(role, registry)
    properties.update({
        40: max_hp,
        41: max_hp,
        42: max_mp,
        43: max_mp,
        **{index: value for index, value in enumerate(display_stats, start=44)},
    })
    attributes, _ = character_panel_frames(role, registry)
    return character_appearance_frame(int(role['id']), properties), attributes


def level_up_effect_frame(role: dict[str, object], levels_gained: int = 1) -> bytes:
    """Play the APK's native level-up effect and attribute-growth panel.

    ``main/e.ar`` dispatches protocol 1129 to the map overlay. Field 0 is the
    character id; fields 3..11 are HP, MP, physical attack, physical defence,
    speed, dodge, hit, magic attack and magic defence gains.
    """
    count = max(1, int(levels_gained))
    return encode_frame(1129, [
        integer(int(role['id'])),
        integer(int(role.get('level', 1))),
        integer(count * 5),
        integer(count * 11),
        integer(count * 6),
        integer(count * 2),
        integer(count),
        integer(count),
        integer(count),
        integer(count),
        integer(count * 2),
        integer(count),
    ])

# ---------------------------------------------------------------------------
# 坐骑图鉴协议（自 mount_protocol.py 收编）。
# ---------------------------------------------------------------------------
import json
from dataclasses import dataclass
from pathlib import Path

from protocol import Field, TYPE_BYTE, byte, encode_frame, integer, string


MOUNT_MESSAGE_ID = 1024
MOUNT_ATLAS_ACTION = 30
DEFAULT_MOUNT_TYPE = 0


@dataclass(frozen=True)
class MountAtlasEntry:
    catalog_id: int
    name: str
    ride_code: int
    mount_type: int = DEFAULT_MOUNT_TYPE


def default_mount_catalog_path() -> Path:
    return Path(__file__).resolve().parents[2] / 'data' / 'catalog' / 'mount_appearance_mapping.json'


def load_mount_atlas_entries(path: Path | None = None) -> tuple[MountAtlasEntry, ...]:
    """Build the APK riding atlas directly from the resource mapping catalog.

    The catalog remains the single source of truth.  No 54-entry protocol list
    is duplicated in Python.  The APK's property-22 riding code is derived as
    ``image_id - image_base``.
    """
    catalog_path = path or default_mount_catalog_path()
    data = json.loads(catalog_path.read_text(encoding='utf-8'))
    image_base = int(data.get('image_base', 40000))
    named = data.get('named_templates', {})
    unnamed_template = str(
        data.get('item_projection', {}).get('unnamed_name', '骑乘资源 {image_id}')
    )

    entries: list[MountAtlasEntry] = []
    seen: set[int] = set()
    for family in data.get('families', []):
        for raw_image_id in family.get('image_ids', []):
            image_id = int(raw_image_id)
            ride_code = image_id - image_base
            if ride_code <= 0 or ride_code in seen:
                raise ValueError(f'invalid or duplicate ride code: image_id={image_id} ride_code={ride_code}')
            seen.add(ride_code)

            override = named.get(str(image_id), {})
            name = str(override.get('name') or unnamed_template.format(image_id=image_id))
            mount_type = int(override.get('mount_type', DEFAULT_MOUNT_TYPE))
            entries.append(MountAtlasEntry(
                catalog_id=ride_code,
                name=name,
                ride_code=ride_code,
                mount_type=mount_type,
            ))

    expected_count = int(data.get('count', len(entries)))
    if len(entries) != expected_count:
        raise ValueError(f'mount atlas count mismatch: expected={expected_count} actual={len(entries)}')
    return tuple(entries)


def is_mount_atlas_request(fields: list[Field]) -> bool:
    """APK request: C->S 1024 [BYTE 30]."""
    return bool(
        len(fields) >= 1
        and fields[0].type_id == TYPE_BYTE
        and fields[0].value == MOUNT_ATLAS_ACTION
    )


def mount_atlas_frame(entries: tuple[MountAtlasEntry, ...] | None = None) -> bytes:
    """APK response: S->C 1024 action 30 followed by riding atlas records.

    Record layout recovered from the client's riding-atlas screen:
    INT catalog_id, STRING name, INT ride_code, BYTE mount_type.
    """
    if entries is None:
        entries = load_mount_atlas_entries()
    if len(entries) > 255:
        raise ValueError('mount atlas count does not fit BYTE')

    fields = [byte(MOUNT_ATLAS_ACTION), byte(len(entries))]
    for entry in entries:
        fields.extend([
            integer(entry.catalog_id),
            string(entry.name),
            integer(entry.ride_code),
            byte(entry.mount_type),
        ])
    return encode_frame(MOUNT_MESSAGE_ID, fields)
