from __future__ import annotations

import argparse
import asyncio
import copy
import contextlib
import json
import logging
import random
import struct
import time
from dataclasses import dataclass, field, fields
from pathlib import Path

from item_registry import (
    ItemRegistry,
    default_item_registry,
)
from map_registry import (
    MapActorDefinition,
    MapDefinition,
    MapRegistry,
    PortalDefinition,
    default_map_registry,
    load_map_registry,
)
from map_o import MapO, MapOError
from protocol import (
    Field,
    GameCipher,
    ProtocolError,
    TYPE_BYTE,
    TYPE_INT,
    TYPE_SHORT,
    binary,
    byte,
    decode_frame,
    decode_payload,
    encode_frame,
    field_debug_entries,
    field_values,
    integer,
    long_integer,
    short,
    string,
)
from shop_registry import (
    MAX_SHOP_PURCHASE_QUANTITY,
    ShopCatalogError,
    ShopCategoryDefinition,
    ShopDefinition,
    ShopRegistry,
    default_shop_registry,
    shop_currency_type,
)
from life_skill_registry import (
    LifeSkillCatalogError,
    LifeSkillRegistry,
    default_life_skill_registry,
)
from life_skill_service import (
    LifeTransactionResult,
    ensure_life_skills,
    gather_start_check,
    gathering_reward_result,
    learn_result,
    life_skill_record,
    life_skill_state,
    life_progress_record,
    life_stamina,
    life_stamina_max,
    life_vitality,
    life_vitality_max,
    learn_result_frame,
    craft_result,
    upgrade_result,
)
from strengthening import (
    INITIAL_STRENGTHEN_STONE_TEMPLATE_ID,
    MIDDLE_STRENGTHEN_STONE_TEMPLATE_ID,
    STRENGTHENING_ATTACK_BONUSES,
    is_strengthening_stone,
    normalized_strengthen_level,
    rate_for,
    recalculate_equipment_attributes,
    stone_definition_for,
    strengthening_failure_level,
    strengthening_success,
    total_strengthening_rate,
)


LOG = logging.getLogger('piaomiao-local')


# Opening the main function menu makes this client prefetch several optional
# systems (tasks, instances and activities). Their response dispatchers all
# release the same global waiting state even when the subtype is not handled.
# Use deliberately unhandled subtypes so an unavailable system behaves as an
# empty module without constructing a screen that expects additional fields.
MENU_PREFETCH_EMPTY_SUBTYPES = {
    1403: 1,
    # In the active client, subtype 2 opens a panel and immediately reads a
    # multi-field payload.  Subtype 0 is intentionally unhandled and safely
    # releases the menu's loading state with this one-field empty response.
    1090: 0,
    1153: 0,
    1061: 3,
}

POSITION_CHECKPOINT_SECONDS = 5.0

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


# ---------------------------------------------------------------------------
# Mall (仙晶商城 / 仙石商城) protocol. APK evidence:
# - screen 611 class pmsj/work/e/bk; tabs R=[0x7d0(2000), 0x834(2100)]:
#   仙晶商城 -> mode 2000, 仙石商城 -> mode 2100.
# - First tab entry sends 1067 [BYTE 0, INT 611, INT mode] AND
#   1067 [BYTE 2, INT 611, INT mode]; cached tab switches send only the [2].
# - Category buttons start at widget id 612001 (bk 0x956a1); clicking one
#   sends 1067 [BYTE 1, INT 612, INT category_id].
# - The ONLY server reply that opens the screen-7 shop page (pmsj/work/e/dp)
#   is the generic 1010/open-screen action (main/e stream handler): short
#   field 5 = 0x45, integer field 4 = screen id (7), integer field 3 = mode
#   (passed to dp.y(mode)); optional string field 6 overrides the title.
#   1067 action-1 responses are dropped by both main/e.u and cd.a(w).
# - dp.ap() requests the goods list: 1033 [INT shop_id, BYTE 7, SHORT page1,
#   SHORT page2, BYTE mode%100] with shop_id = (mode/1000)*1000.
# - S->C 1033 action 7 header is index-addressed (dp.a(w)): [0]=BYTE action,
#   [1]=INT shop_id, [2]=INT batch count, [3]=INT page, [4]=INT total,
#   [5]=unread placeholder, [6]=BYTE currency type (must equal dp.E(mode) or
#   the page closes); goods records start at [7]; one trailing STRING title.
# - Purchase (main/e.a(BIIS)): 1033 [INT shop_id, BYTE 1, INT item_id,
#   SHORT quantity]. S->C 1033 actions 1/2 read no further fields (action 1
#   refreshes the shop currency label; action 2 also rebuilds the sell page).
# - Currency: property 50 = 银两, 52 = 仙晶 (type 1), 49 = 仙石 (type 2).
# ---------------------------------------------------------------------------
MALL_SCREEN_ID = 611
MALL_CATEGORY_SCREEN_ID = 612
SHOP_SCREEN_ID = 7
SHOP_OPEN_SCREEN_ACTION = 0x45
MALL_TAB_TO_DP_MODE = {2000: 1000, 2100: 2100}
SHOP_GOODS_HEADER_FIELDS = 7


def mall_category_list_frame(categories: tuple[ShopCategoryDefinition, ...]) -> bytes:
    """S->C 1067 action 0 category list for the screen-611 mall page.

    cd.a(w) reads byte field 3 as the count, derives the record length as
    ``(fieldCount - 4) / count`` and reads each record's [0] as the numeric
    id and [1] as the name; field 1 (INT 611) is the screen id the message
    router uses to find the target page, and field 2 is never read.
    """
    fields: list[Field] = [
        byte(0),
        integer(MALL_SCREEN_ID),
        byte(0),
        byte(len(categories)),
    ]
    for category in categories:
        fields.append(integer(category.category_id))
        fields.append(string(category.name))
    return encode_frame(1067, fields)


def mall_title_frame(title: str) -> bytes:
    """S->C 1067 action 2 title update: cd.a(w) reads only string field 2."""
    return encode_frame(1067, [
        byte(2),
        integer(MALL_SCREEN_ID),
        string(title),
    ])


def shop_screen_bridge_frame(dp_mode: int) -> bytes:
    """Open the screen-7 shop page via the APK's 1010 open-screen action.

    main/e reads short field 5 as the sub-command (0x45 = open screen),
    integer field 4 as the screen id and integer field 3 as the mode passed
    to dp.y(mode). Field 6 (title) is optional and omitted on purpose:
    dp.y() derives its own 仙晶商店/仙石商店 title from the mode.
    """
    return encode_frame(1010, [
        integer(0),
        short(0),
        short(0),
        integer(dp_mode),
        integer(SHOP_SCREEN_ID),
        short(SHOP_OPEN_SCREEN_ACTION),
    ])


def shop_purchase_ack_frame() -> bytes:
    """S->C 1033 action 1: dp.a(w) refreshes the shop currency label only."""
    return encode_frame(1033, [byte(1)])


def shop_goods_list_frame(
    shop: ShopDefinition,
    category: ShopCategoryDefinition,
    item_registry: ItemRegistry,
) -> bytes:
    """Encode the S->C 1033 action 7 goods page for one mall category.

    The whole category is served in a single batch (page 0): dp.a(w) skips
    further pages once its local vector reaches the total count.
    """
    fields: list[Field] = [
        byte(7),
        integer(shop.shop_id),
        integer(len(category.goods)),
        integer(0),
        integer(len(category.goods)),
        byte(0),
        byte(shop_currency_type(shop.mode)),
    ]
    for goods in category.goods:
        definition = item_registry.require(goods.template_id)
        fields.append(integer(goods.template_id))
        fields.append(integer(goods.price))
        fields.append(string(definition.name))
        # Four INT metas the client narrows to j.n(byte)/j.h/j.l/j.q(short).
        fields.extend(integer(0) for _ in range(4))
        if int(definition.equipment_slot) > 0:
            # Equipment goods (item.c() == true) read 4 SHORT attributes via
            # b/g.a(BS); omitting them misaligns every following record.
            for value in definition.equipment_attributes[:4]:
                fields.append(short(int(value)))
    fields.append(string(shop.name))
    return encode_frame(1033, fields)


def is_mall_category_request(fields: list[Field]) -> bool:
    """True only for 1067 [BYTE 0, INT 611, INT mode] tab entry requests."""
    return bool(
        len(fields) >= 3
        and fields[0].type_id == TYPE_BYTE
        and fields[0].value == 0
        and fields[1].type_id == TYPE_INT
        and fields[1].value == MALL_SCREEN_ID
        and fields[2].type_id == TYPE_INT
    )


def is_mall_title_request(fields: list[Field]) -> bool:
    """True only for 1067 [BYTE 2, INT 611, INT mode] title/mode requests."""
    return bool(
        len(fields) >= 3
        and fields[0].type_id == TYPE_BYTE
        and fields[0].value == 2
        and fields[1].type_id == TYPE_INT
        and fields[1].value == MALL_SCREEN_ID
        and fields[2].type_id == TYPE_INT
    )


def is_mall_open_category_request(fields: list[Field]) -> bool:
    """True only for 1067 [BYTE 1, INT 612, INT category_id] click requests."""
    return bool(
        len(fields) >= 3
        and fields[0].type_id == TYPE_BYTE
        and fields[0].value == 1
        and fields[1].type_id == TYPE_INT
        and fields[1].value == MALL_CATEGORY_SCREEN_ID
        and fields[2].type_id == TYPE_INT
    )


def is_shop_list_request(fields: list[Field]) -> bool:
    """True only for 1033 [INT, BYTE 7, SHORT, SHORT, BYTE] list requests."""
    return bool(
        len(fields) >= 5
        and fields[0].type_id == TYPE_INT
        and fields[1].type_id == TYPE_BYTE
        and fields[1].value == 7
        and fields[2].type_id == TYPE_SHORT
        and fields[3].type_id == TYPE_SHORT
        and fields[4].type_id == TYPE_BYTE
    )


def is_shop_purchase_request(fields: list[Field]) -> bool:
    """True only for 1033 [INT, BYTE 1, INT, SHORT>0] purchase requests.

    Mirrors main/e.a(BIIS): the TLV types [4, 2, 4, 3] and the action value
    are both verified; a BYTE quantity or action != 1 is never a purchase.
    """
    return bool(
        len(fields) == 4
        and fields[0].type_id == TYPE_INT
        and fields[1].type_id == TYPE_BYTE
        and fields[1].value == 1
        and fields[2].type_id == TYPE_INT
        and fields[3].type_id == TYPE_SHORT
        and type(fields[3].value) is int
        and 0 < fields[3].value <= MAX_SHOP_PURCHASE_QUANTITY
    )


def allocate_item_instance_id(role: dict[str, object]) -> int:
    """Allocate a free role-scoped item instance id (role_id * 100 + n)."""
    used = {int(item.get('id', 0)) for item in role_items(role)}
    candidate = int(role.get('id', 0)) * 100 + 50
    while candidate in used:
        candidate += 1
    return candidate


@dataclass(frozen=True)
class ShopPurchaseResult:
    frames: tuple[bytes, ...]
    changed: bool
    reason: str = ''


def _rejected_purchase(reason: str) -> ShopPurchaseResult:
    return ShopPurchaseResult((), False, reason)


def shop_purchase_result(
    role: dict[str, object],
    shop: ShopDefinition,
    category_id: int,
    template_id: int,
    quantity: int,
    item_registry: ItemRegistry | None = None,
) -> ShopPurchaseResult:
    """Apply one mall purchase atomically against server-side data.

    Server price, shop/category membership, quantity bounds, currency and
    bag capacity are all re-verified here; the client's own pre-checks are
    never trusted. On any failure the role is left untouched.
    """
    if item_registry is None:
        item_registry = default_item_registry()
    category = shop.category(int(category_id))
    if category is None:
        return _rejected_purchase('商城分类不存在')
    goods = shop.find_goods(int(category_id), int(template_id))
    if goods is None:
        return _rejected_purchase('商品不存在')
    if type(quantity) is not int or quantity <= 0:
        return _rejected_purchase('购买数量非法')
    if quantity > MAX_SHOP_PURCHASE_QUANTITY:
        return _rejected_purchase('购买数量超出上限')
    total = goods.price * quantity
    if total > MAX_CURRENCY_BALANCE:
        return _rejected_purchase('订单金额超出上限')
    currencies = role.get('currencies')
    if not isinstance(currencies, dict):
        currencies = {}
        role['currencies'] = currencies
    balance = normalized_currency_balance(currencies.get(shop.currency_name))
    if balance < total:
        return _rejected_purchase('货币不足')
    definition = item_registry.require(int(template_id))
    max_quantity = int(definition.max_quantity)
    stack = next(
        (
            item for item in role_items(role)
            if int(item.get('template_id', 0)) == int(template_id)
            and item.get('location', 'bag') == 'bag'
        ),
        None,
    ) if max_quantity > 1 else None
    if stack is not None:
        if int(stack.get('quantity', 1)) + quantity > max_quantity:
            return _rejected_purchase('超出物品堆叠上限')
    elif bag_item_count(role) >= bag_capacity(role):
        return _rejected_purchase('背包已满')

    balance_after = balance - total
    currencies[shop.currency_name] = balance_after
    if stack is not None:
        stack['quantity'] = int(stack.get('quantity', 1)) + quantity
        purchased = stack
    else:
        purchased = {
            'id': allocate_item_instance_id(role),
            'template_id': int(template_id),
            'quantity': quantity,
            'location': 'bag',
        }
        role_items(role).append(purchased)
    frames = (
        character_appearance_frame(
            int(role.get('id', 0)),
            {shop.currency_property: balance_after},
        ),
        item_frame(purchased, operation=3),
        shop_purchase_ack_frame(),
    )
    return ShopPurchaseResult(frames, True, '')


# ---------------------------------------------------------------------------
# Life skills (生活技能).  Protocol evidence in docs/protocol/life-skills.md:
# 1132 is the shared skill container (sect + life), 1143 is trainer learn +
# normal crafting, gathering runs over 1141 (catalog) / 2027 (flow) and 1145
# is cross-map auto-pathfinding.  All numeric game data is local-compat.
# ---------------------------------------------------------------------------
GATHER_MENU_LABEL = '采集'  # [compat] entity field 9 tap-menu text
LIFE_SKILL_PLACEHOLDER_NAME = '基础技能'
LIFE_SKILL_LOCKED_SLOT_NAME = '未开放'
LIFE_SKILL_LOCKED_SLOT_ID_BASE = 2_147_000_000
LIFE_SKILL_SCREEN_SLOTS = 7
# 14 fields per record: [name, skill_id, level, max_level, proficiency,
# max_proficiency, flags, (7 reserved ints)]
SKILL_RECORD_WIDTH = 14
FORGE_LOG_PREFIX = 'FORGE'


def life_skill_list_frame(role: dict[str, object], settings: Settings) -> bytes:
    """S->C 1132 action 0: the merged sect + life skill container list.

    All records share the 14-field width so the APK's `(size-2)/count`
    slicing stays correct. Screen 603 has a fixed seven-element array and
    dereferences every slot, so unused positions must be represented by
    unique, locked records. The sect record keeps its historical position
    first (the client merges records into b/f.n by skill id).
    """
    life_state = ensure_life_skills(role, settings.life_registry)
    records: list[list[object]] = []
    sect_id = normalized_sect_id(role)
    if sect_id == TEST_SECT_ID:
        sect_record = list(field_values(decode_frame(character_skill_list(role))[1]))[2:]
        records.append(sect_record)
    else:
        records.append([
            LIFE_SKILL_PLACEHOLDER_NAME, 0,
            *(0 for _ in range(SKILL_RECORD_WIDTH - 2)),
        ])
    for skill in settings.life_registry.skills.values():
        records.append(life_skill_record(
            skill, life_skill_state(role, skill.skill_id),
        ))
    if len(records) > LIFE_SKILL_SCREEN_SLOTS:
        raise ValueError(
            f'life skill screen supports at most {LIFE_SKILL_SCREEN_SLOTS} records'
        )
    while len(records) < LIFE_SKILL_SCREEN_SLOTS:
        records.append([
            LIFE_SKILL_LOCKED_SLOT_NAME,
            LIFE_SKILL_LOCKED_SLOT_ID_BASE + len(records),
            *(0 for _ in range(SKILL_RECORD_WIDTH - 2)),
        ])
    fields: list[Field] = [byte(0), byte(len(records))]
    for record in records:
        fields.append(string(str(record[0])))
        fields.extend(integer(int(value)) for value in record[1:])
    return encode_frame(1132, fields)


def life_recipe_list_frame(
    skill,
    tier: int,
    recipes: list,
    life_registry: LifeSkillRegistry,
) -> bytes:
    """S->C 1132 action 2 recipe list (e/db). rec[1] is unread placeholder."""
    fields: list[Field] = [
        byte(2),
        integer(int(skill.skill_id)),
        string('配方列表'),
        string('选择配方进行制造'),
        byte(0),
        byte(len(recipes)),
    ]
    for recipe in recipes:
        fields.append(integer(int(recipe.recipe_id)))
        fields.append(integer(0))
        fields.append(string(recipe.name))
        fields.append(string(f'消耗活力 {recipe.vitality_cost}'))
    return encode_frame(1132, fields)


def life_tier_frame(skill, life_registry: LifeSkillRegistry) -> bytes:
    """S->C 1132 action 1 tier page (e/ay). Minimal equal-width records."""
    tier_count = max(1, int(skill.tier_count))
    fields: list[Field] = [byte(1), integer(int(skill.skill_id)), byte(tier_count)]
    for tier in range(tier_count):
        recipes = life_registry.recipes_for(skill.skill_id, tier)
        fields.append(string(f'第{tier + 1}层 配方 {len(recipes)}个'))
        fields.append(byte(len(recipes)))
        fields.append(integer(0))
        fields.append(integer(0))
    return encode_frame(1132, fields)


def life_skill_info_frame(skill_id: int, level: int, text: str) -> bytes:
    """S->C 1132 action 3 info text (x.A on the 603 life skill page)."""
    return encode_frame(1132, [
        byte(3), integer(int(skill_id)), integer(int(level)), string(text),
    ])


def life_proficiency_frame(role: dict[str, object], settings: Settings) -> bytes:
    """S->C 1132 action 4 proficiency sync for every learned life skill."""
    skills = [
        (skill, life_skill_state(role, skill.skill_id))
        for skill in settings.life_registry.skills.values()
        if life_skill_state(role, skill.skill_id) is not None
    ]
    fields: list[Field] = [byte(4), byte(len(skills))]
    for skill, state in skills:
        record = life_progress_record(skill, state)
        fields.append(string(str(record[0])))
        fields.extend(integer(int(value)) for value in record[1:])
    return encode_frame(1132, fields)


def life_skill_upgrade_frame(
    skill,
    role: dict[str, object],
    settings: Settings,
) -> bytes:
    """S->C 1132 action 6 upgrade page push (e/az, screen 329)."""
    state = life_skill_state(role, skill.skill_id) or {'level': 0, 'proficiency': 0}
    level = int(state.get('level', 0))
    next_level = level + 1
    return encode_frame(1132, [
        byte(6),
        integer(int(skill.skill_id)),
        string(skill.name),
        byte(level),
        byte(int(skill.max_level)),
        byte(int(skill.upgrade_required_role_level)),
        integer(skill.upgrade_silver_cost(next_level)),
        integer(skill.upgrade_exp_cost(next_level)),
        string(f'当前等级 {level} 级'),
        string(f'下一级 {next_level} 级'),
        integer(int(skill.icon)),
    ])


def life_trainer_page_frame(trainer) -> bytes:
    """S->C 1143 action 0 trainer page push (e/de, screen 327)."""
    return encode_frame(1143, [
        byte(0),
        integer(int(trainer.trainer_id)),
        string(trainer.name),
        byte(1),
        string('选择要学习的生活技能'),
        string('学习需要消耗银两和经验'),
    ])


def life_learnable_list_frame(
    trainer,
    role: dict[str, object],
    settings: Settings,
) -> bytes:
    """S->C 1143 action 1 learnable list; exactly 7-field records (de.X=7)."""
    entries = [
        settings.life_registry.learnable[entry_id]
        for entry_id in trainer.entry_ids
        if entry_id in settings.life_registry.learnable
    ]
    fields: list[Field] = [byte(1), byte(0), byte(len(entries))]
    for entry in entries:
        fields.append(integer(int(entry.entry_id)))
        fields.append(integer(0))
        fields.append(integer(int(entry.level_requirement)))
        fields.append(integer(int(entry.silver_cost)))
        fields.append(integer(int(entry.experience_cost)))
        fields.append(string(entry.display))
        fields.append(string(entry.detail))
    return encode_frame(1143, fields)


def life_learnable_detail_frame(entry) -> bytes:
    """S->C 1143 action 2 detail text (underscore-delimited pages)."""
    return encode_frame(1143, [
        byte(2),
        string(f'{entry.display}_{entry.detail}_需要等级 {entry.level_requirement}'
               f'_银两 {entry.silver_cost}_经验 {entry.experience_cost}'),
    ])


def life_learn_result_frame(page: int, entry, learned: bool, next_entry) -> bytes:
    """S->C 1143 action 3: result 0 removes the row, otherwise rebuilds it."""
    return learn_result_frame(page, entry, learned, next_entry)


def life_craft_detail_frame(
    recipe,
    role: dict[str, object],
    settings: Settings,
) -> bytes:
    """S->C 1143 action 4 craft detail (e/dc): 17 confirmed fields."""
    slot_templates, _used, _free = recipe.material_slots()
    fields: list[Field] = [
        byte(4),
        integer(int(recipe.output_template_id)),
        string(recipe.name),
        integer(int(settings.item_registry.require(recipe.output_template_id).icon_code)),
        string(recipe.description),
    ]
    fields.extend(integer(int(template)) for template, _qty in slot_templates)
    fields.extend(string(str(template)) for template, _qty in slot_templates)
    fields.extend(byte(int(quantity)) for _template, quantity in slot_templates)
    return encode_frame(1143, fields)


def life_craft_ack_frame() -> bytes:
    """S->C 1143 action 5: no fields; the client re-scans the bag."""
    return encode_frame(1143, [byte(5)])


def life_craft_text_frame(text: str) -> bytes:
    """S->C 1143 action 6 dynamic craft-page text."""
    return encode_frame(1143, [byte(6), string(text)])


def is_life_skill_list_request(fields: list[Field]) -> bool:
    return bool(
        len(fields) == 1
        and fields[0].type_id == TYPE_BYTE
        and fields[0].value == 0
    )


def is_life_skill_open_request(fields: list[Field]) -> bool:
    return bool(
        len(fields) == 2
        and fields[0].type_id == TYPE_BYTE
        and fields[0].value == 1
        and fields[1].type_id == TYPE_INT
    )


def is_life_recipe_list_request(fields: list[Field]) -> bool:
    return bool(
        len(fields) >= 3
        and fields[0].type_id == TYPE_BYTE
        and fields[0].value == 2
        and fields[1].type_id == TYPE_INT
        and all(field.type_id == TYPE_BYTE for field in fields[2:])
    )


def is_life_skill_info_request(fields: list[Field]) -> bool:
    return bool(
        len(fields) == 3
        and fields[0].type_id == TYPE_BYTE
        and fields[0].value == 3
        and fields[1].type_id == TYPE_INT
        and fields[2].type_id == TYPE_BYTE
    )


def is_life_skill_upgrade_request(fields: list[Field]) -> bool:
    return bool(
        len(fields) == 2
        and fields[0].type_id == TYPE_BYTE
        and fields[0].value == 6
        and fields[1].type_id == TYPE_INT
    )


def is_life_trainer_list_request(fields: list[Field]) -> bool:
    return bool(
        len(fields) >= 2
        and fields[0].type_id == TYPE_BYTE
        and fields[0].value == 1
        and fields[1].type_id == TYPE_INT
    )


def is_life_learnable_detail_request(fields: list[Field]) -> bool:
    return bool(
        len(fields) == 2
        and fields[0].type_id == TYPE_BYTE
        and fields[0].value == 2
        and fields[1].type_id == TYPE_INT
    )


def is_life_learn_request(fields: list[Field]) -> bool:
    return bool(
        len(fields) == 2
        and fields[0].type_id == TYPE_BYTE
        and fields[0].value == 3
        and fields[1].type_id == TYPE_INT
    )


def is_life_craft_detail_request(fields: list[Field]) -> bool:
    return bool(
        len(fields) == 2
        and fields[0].type_id == TYPE_BYTE
        and fields[0].value == 4
        and fields[1].type_id == TYPE_INT
    )


def is_life_craft_request(fields: list[Field]) -> bool:
    """Normal craft: [BYTE 5, INT recipe, INT slot1..4, BYTE qty 1..99]."""
    return bool(
        len(fields) == 7
        and fields[0].type_id == TYPE_BYTE
        and fields[0].value == 5
        and all(field.type_id == TYPE_INT for field in fields[1:6])
        and fields[6].type_id == TYPE_BYTE
        and type(fields[6].value) is int
        and 1 <= fields[6].value <= 99
    )


def is_life_direct_use_request(fields: list[Field]) -> bool:
    """Screen-326 direct use: [BYTE 5, INT recipe, INT 0, INT 0, INT 0, INT 0]."""
    return bool(
        len(fields) == 6
        and fields[0].type_id == TYPE_BYTE
        and fields[0].value == 5
        and all(field.type_id == TYPE_INT for field in fields[1:])
    )


def is_life_craft_text_request(fields: list[Field]) -> bool:
    return bool(
        len(fields) == 2
        and fields[0].type_id == TYPE_BYTE
        and fields[0].value == 6
        and fields[1].type_id == TYPE_INT
    )


def is_gather_start_request(fields: list[Field]) -> bool:
    """C->S 2027 gather start: [BYTE 1, INT entity_id] (main/k tap menu)."""
    return bool(
        len(fields) == 2
        and fields[0].type_id == TYPE_BYTE
        and fields[0].value == 1
        and fields[1].type_id == TYPE_INT
    )


def is_map_pathfind_request(fields: list[Field]) -> bool:
    """C->S 1145 pathfind: [BYTE 0, INT map_id, BYTE x, BYTE y]."""
    return bool(
        len(fields) == 4
        and fields[0].type_id == TYPE_BYTE
        and fields[0].value == 0
        and fields[1].type_id == TYPE_INT
        and fields[2].type_id == TYPE_BYTE
        and fields[3].type_id == TYPE_BYTE
    )


def gather_catalog_frame(targets: list) -> bytes:
    """S->C 1141 gather target catalog (no action byte, 9-field records)."""
    fields: list[Field] = [integer(len(targets))]
    for target in targets:
        fields.extend((
            integer(int(target.target_id)),
            string(target.name),
            integer(int(target.category)),
            integer(int(target.x)),
            integer(int(target.y)),
            integer(0),
            integer(0),
            integer(int(target.map_id)),
            integer(0),
        ))
    return encode_frame(1141, fields)


def gather_spawn_frame(target) -> bytes:
    """S->C 2027 action 0: spawn one gather entity (b/i) on the map.

    Fields are stored on the entity at their own indices; index 9 is the
    tap-menu label the client compares before sending the gather request.
    Indices 6/7/8 are unread compatibility placeholders.
    """
    return encode_frame(2027, [
        byte(0),
        integer(int(target.target_id)),
        integer(int(target.x)),
        integer(int(target.y)),
        integer(int(target.model_id)),
        string(target.name),
        integer(0),
        integer(0),
        integer(0),
        string(GATHER_MENU_LABEL),
    ])


def gather_start_frame(duration_seconds: int, target_id: int) -> bytes:
    """S->C 2027 action 1: duration is SECONDS (client multiplies by 1000)."""
    return encode_frame(2027, [
        byte(1), integer(int(duration_seconds)), integer(int(target_id)),
    ])


def gather_interrupt_frame() -> bytes:
    """S->C 2027 action 2: stop timer, clear process, '采集中断!'."""
    return encode_frame(2027, [byte(2)])


def gather_remove_frame(target_id: int) -> bytes:
    """S->C 2027 action 3: stop timer and remove the map entity."""
    return encode_frame(2027, [byte(3), integer(int(target_id))])


def map_pathfind_frame(map_id: int, x: int, y: int) -> bytes:
    """S->C 1145 action 0: single-hop path record (same-map walk)."""
    return encode_frame(1145, [
        byte(0), integer(1), integer(int(map_id)), integer(int(x)), integer(int(y)),
        integer(0),
    ])


def is_forge_list_request(fields: list[Field]) -> bool:
    """C->S 1084 list: [BYTE 0, INT context, SHORT, SHORT, BYTE]."""
    return bool(
        len(fields) == 5
        and fields[0].type_id == TYPE_BYTE
        and fields[0].value == 0
        and fields[1].type_id == TYPE_INT
        and fields[2].type_id == TYPE_SHORT
        and fields[3].type_id == TYPE_SHORT
        and fields[4].type_id == TYPE_BYTE
    )


def is_forge_select_request(fields: list[Field]) -> bool:
    """C->S 1084 select/attr: [BYTE 1|2, INT recipe_id]."""
    return bool(
        len(fields) == 2
        and fields[0].type_id == TYPE_BYTE
        and fields[0].value in (1, 2)
        and fields[1].type_id == TYPE_INT
    )


def _is_forge_slot_request(fields: list[Field], action: int) -> bool:
    return bool(
        len(fields) == 6
        and fields[0].type_id == TYPE_BYTE
        and fields[0].value == action
        and all(field.type_id == TYPE_INT for field in fields[1:])
    )


def is_forge_collect_request(fields: list[Field]) -> bool:
    """C->S 1084 collect after the forge animation: [BYTE 3, INT x5]."""
    return _is_forge_slot_request(fields, 3)


def is_forge_confirm_request(fields: list[Field]) -> bool:
    """C->S 1084 confirm forge: [BYTE 5, INT x5]."""
    return _is_forge_slot_request(fields, 5)


class ConnectionGathering:
    """Connection-scoped gathering state: one active gather, token-guarded.

    The asyncio completion task closes over the session; every wakeup must
    pass `is_current` (same token/role/target) and `consume` before any
    reward is applied, so a stale task can never pay out twice.
    """

    def __init__(self) -> None:
        self.session: dict[str, object] | None = None
        self.task: asyncio.Task | None = None
        self._token = 0

    def start(
        self,
        role: dict[str, object],
        target,
        map_id: int,
    ) -> tuple[tuple[bytes, ...], dict[str, object] | None]:
        if self.session is not None:
            return (), None
        self._token += 1
        self.session = {
            'token': self._token,
            'role_id': int(role.get('id', 0)),
            'target_id': int(target.target_id),
            'map_id': int(map_id),
            'x': int(target.x),
            'y': int(target.y),
        }
        return (gather_start_frame(int(target.duration_seconds), int(target.target_id)),), self.session

    def is_current(self, session: dict[str, object] | None) -> bool:
        return (
            self.session is not None
            and session is not None
            and self.session is session
            and self.session.get('token') == self._token
        )

    def consume(self, session: dict[str, object] | None) -> bool:
        """Atomically claim the reward right for a current session."""
        if not self.is_current(session):
            return False
        self.session = None
        return True

    def cancel(self) -> bytes | None:
        """Stop any active gather; returns the 2027 interrupt frame if one ran."""
        had_session = self.session is not None
        self.session = None
        if self.task is not None:
            self.task.cancel()
            self.task = None
        return gather_interrupt_frame() if had_session else None


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


@dataclass
class Settings:
    host: str = '0.0.0.0'
    port: int = 6805
    advertise_host: str = '127.0.0.1'
    server_name: str = '本地一区'
    accept_any_credentials: bool = True
    expected_client_version: int = 2000
    role_id: int = 10001
    role_name: str = '本地侠客'
    role_model: int = 2000
    default_map_id: int = 58
    map_registry: MapRegistry = field(default_factory=default_map_registry)
    item_registry: ItemRegistry = field(default_factory=default_item_registry)
    shop_registry: ShopRegistry = field(default_factory=default_shop_registry)
    life_registry: LifeSkillRegistry = field(default_factory=default_life_skill_registry)
    # Deprecated aliases retained for protocol helpers and older local tests.
    # Map entry, entities and routing use ``map_registry`` below.
    map_id: int = 58
    map_name: str = '长安'
    map_width: int = 96
    map_height: int = 96
    spawn_x: int = 60
    spawn_y: int = 67
    # Protocol 1126 carries generic map actors.  The client adds 0x200b20 to
    # the raw model id before loading role/<model>.dat; 3760000 therefore maps
    # to the bundled role/5860000.dat sprite.  This model's image ids are
    # present in the local APK's images.o index.
    # Generic map actors can only be removed by the APK's protocol-18 handler
    # when their id is at least 1_000_000. Keep this encounter in that range
    # so victory despawns it before automatic battle mode can re-interact.
    monster_id: int = 1_900_001
    monster_name: str = '试炼妖兽'
    monster_model: int = 3_760_000
    monster_x: int = 10
    monster_y: int = 6
    # Initial facing for the 1126 subtype=0 monster actor, applied right after it
    # is spawned via a 1126 subtype=1 direction frame. 0=down, 1=right, 2=up, 3=left.
    monster_direction: int = 0
    # Minimal cross-map test portal.  The client treats 1126 actors as
    # interactable map objects and sends 1010/action=7 with this id when the
    # player reaches the actor's tile.
    portal_enabled: bool = False
    portal_id: int = 580001
    portal_name: str = '跨地图传送点'
    portal_x: int = 64
    portal_y: int = 67
    # Initial facing for the 1126 subtype=0 portal actor (it reuses the generic
    # b/n entity). Applied via a 1126 subtype=1 direction frame.
    portal_direction: int = 0
    portal_target_map_id: int = 50000
    portal_target_map_name: str = '传送测试区'
    portal_target_spawn_x: int = 8
    portal_target_spawn_y: int = 6
    portal_target_map_o_file: str = 'maps/50000.map.o'
    portal_target_map_ref_available: bool = True
    map_ref_available: bool = True
    return_portal_id: int = 580002
    return_portal_name: str = '返回长安'
    return_portal_x: int = 9
    return_portal_y: int = 6
    # Hand-placed map-58 NPCs. Each entry is a dict with id/name/label/x/y and
    # dat_id for the native 2030 b/t actor sprite. They only spawn on map 58.
    npc_enabled: bool = True
    npcs: list = field(default_factory=list)
    heartbeat_interval_seconds: float = 25.0
    map_o_file: str = 'maps/58.map.o'
    role_data_file: str = 'data/roles.json'

    @classmethod
    def load(cls, path: Path) -> 'Settings':
        if not path.exists():
            return cls()
        payload = json.loads(path.read_text(encoding='utf-8'))
        npc_catalog = None
        catalog = Path(__file__).with_name('data') / 'npcs.json'
        if catalog.exists():
            try:
                loaded_catalog = json.loads(catalog.read_text(encoding='utf-8'))
                if isinstance(loaded_catalog, list):
                    npc_catalog = loaded_catalog
            except (OSError, ValueError) as exc:
                LOG.warning('failed to load NPC catalog %s: %s', catalog, exc)

        registry = load_map_registry(payload, npc_catalog=npc_catalog)
        allowed = {
            item.name for item in fields(cls)
        } - {'map_registry', 'item_registry', 'shop_registry', 'life_registry'}
        values = {key: value for key, value in payload.items() if key in allowed}
        values['default_map_id'] = registry.default_map_id
        settings = cls(map_registry=registry, **values)

        # Keep the old public attributes coherent during the compatibility
        # cycle; new map code reads the typed definition instead.
        initial = registry.require(registry.default_map_id)
        settings.map_id = initial.id
        settings.map_name = initial.name
        settings.map_width = initial.fallback_width
        settings.map_height = initial.fallback_height
        settings.spawn_x = initial.spawn_x
        settings.spawn_y = initial.spawn_y
        settings.map_o_file = initial.map_o_file
        settings.map_ref_available = initial.map_ref_available
        settings.npcs = [dict(vars(npc)) for npc in initial.npcs]
        if initial.monster is not None:
            settings.monster_id = initial.monster.id
            settings.monster_name = initial.monster.name
            settings.monster_model = initial.monster.model
            settings.monster_x = initial.monster.x
            settings.monster_y = initial.monster.y
            settings.monster_direction = initial.monster.direction
        if initial.portals:
            portal = initial.portals[0]
            target = registry.require(portal.target_map_id)
            settings.portal_enabled = True
            settings.portal_id = portal.id
            settings.portal_name = portal.name
            settings.portal_x = portal.x
            settings.portal_y = portal.y
            settings.portal_direction = portal.direction
            settings.portal_target_map_id = target.id
            settings.portal_target_map_name = target.name
            settings.portal_target_spawn_x = portal.target_x
            settings.portal_target_spawn_y = portal.target_y
            settings.portal_target_map_o_file = target.map_o_file
            settings.portal_target_map_ref_available = target.map_ref_available
        return settings


@dataclass
class LocalNpcDialogueState:
    """Connection-local guard for one native 2032 NPC dialogue."""

    map_id: int | None = None
    npc_id: int | None = None

    def select(self, map_id: int, npc_id: int) -> None:
        self.map_id = int(map_id)
        self.npc_id = int(npc_id)

    def clear(self) -> None:
        self.map_id = None
        self.npc_id = None


@dataclass(frozen=True)
class CombatStats:
    max_hp: int
    physical_attack: int
    physical_defence: int


def equipped_weapon_attack(role: dict[str, object]) -> int:
    """Return the effective first attribute of the equipped slot-10 weapon."""
    weapon = next(
        (
            item
            for item in role_items(role)
            if item.get('location') == 'equipped'
            and is_equipment(item)
            and item_slot(item) == 10
        ),
        None,
    )
    if weapon is None:
        return 0
    attributes = list(weapon.get('equipment_attributes', [0, 0, 0, 0]))
    if not attributes or type(attributes[0]) is not int:
        return 0
    return max(0, attributes[0])


def combat_stats(role: dict[str, object]) -> CombatStats:
    """Derive battle values from the same level/stats shown by the character UI."""
    level = max(1, int(role.get('level', 1)))
    raw_stats = [int(value) for value in list(role.get('stats', []))]
    base_stats = [max(0, value) for value in (raw_stats + [10, 10, 10, 10, 10])[:5]]
    return CombatStats(
        max_hp=100 + ((level - 1) * 10) + base_stats[1],
        physical_attack=(
            10
            + base_stats[0]
            + ((level - 1) * 2)
            + equipped_weapon_attack(role)
        ),
        physical_defence=base_stats[1] + (level - 1),
    )


@dataclass
class LocalTeamState:
    """Connection-local ownership for the APK's minimal self-team flow."""

    leader_id: int = 0

    @property
    def active(self) -> bool:
        return self.leader_id > 0


TEAM_LEADER_FLAG = 0x40


def team_request_frames(
    role: dict[str, object],
    values: list[object],
    state: LocalTeamState,
) -> list[bytes]:
    """Handle the confirmed single-role create and disband team requests."""
    action = int(values[0]) if values else -1
    role_id = int(role.get('id', 0))
    if action == 11:
        # The APK may still display the leader page after reconnecting or
        # losing connection-local state.  Always acknowledge its confirmed
        # disband action so that the native UI can leave that stale page.
        state.leader_id = 0
        return [
            character_appearance_frame(role_id, {0: 0}),
            encode_frame(1023, [short(11)]),
        ]
    if action != 0 or len(values) < 2 or int(values[1]) != role_id or state.active:
        return []

    level = max(1, int(role.get('level', 1)))
    raw_stats = [int(value) for value in list(role.get('stats', []))]
    base_stats = (raw_stats + [10, 10, 10, 10, 10])[:5]
    max_hp = combat_stats(role).max_hp
    max_mp = 50 + ((level - 1) * 5) + max(0, base_stats[2])
    state.leader_id = role_id
    return [
        # The native team page and map HUD test property 0's 0x40 bit to
        # decide whether the local player is the leader.  Send it before the
        # member record so the 1026-triggered page refresh builds leader text.
        character_appearance_frame(role_id, {0: TEAM_LEADER_FLAG}),
        encode_frame(1026, [
            byte(0),
            byte(1),
            string(str(role.get('name', ''))),
            integer(role_id),
            integer(max_hp),
            integer(max_hp),
            byte(normalized_sect_id(role)),
            integer(level),
            integer(max_mp),
            integer(max_mp),
            integer(0),
        ]),
    ]


@dataclass
class LocalBattleState:
    """Connection-local state for the deliberately small APK battle probe.

    The APK owns rendering and animation; the compatibility server only keeps
    enough state to answer the confirmed 1040/1041/1042 messages for one
    player and one monster.  Nothing is persisted to the role store.
    """

    active: bool = False
    round: int = 1
    player_id: int = 0
    monster_id: int = 0
    player_hp: int = 100
    player_max_hp: int = 100
    monster_hp: int = 100
    monster_max_hp: int = 100
    player_attack: int = 10
    player_defence: int = 0
    monster_attack: int = 10
    monster_defence: int = 0
    # A defeated monster remains absent until the client reloads the map. This
    # covers automatic battle's short race with the removal frame.
    monster_defeated: bool = False
    # ``round_ack`` means the complete 1042 action queue has been sent and the
    # server is waiting for the APK to report that its animation queue drained.
    phase: str = 'idle'
    # Lightweight per-encounter id so map/battle/resource logs can be grepped
    # together.  It is diagnostic only and never written to the protocol.
    encounter_seq: int = 0
    trace_id: str = ''
    # Map/tile context anchors the post-escape re-trigger guard. The active APK
    # may start a battle through 1010/7 without a tile, so both values are
    # optional and the guard itself must not depend on contact_tile.
    map_id: int = 0
    contact_tile: tuple[int, int] | None = None
    escape_guard: dict[str, object] | None = None
    player_tile: tuple[int, int] | None = None

    def begin(
        self,
        player_id: int,
        monster_id: int,
        player_stats: CombatStats | None = None,
    ) -> None:
        selected_stats = player_stats or CombatStats(100, 10, 0)
        self.active = True
        self.round = 1
        self.player_id = player_id
        self.monster_id = monster_id
        self.player_max_hp = max(1, selected_stats.max_hp)
        self.player_hp = self.player_max_hp
        self.monster_max_hp = 100
        self.monster_hp = self.monster_max_hp
        self.player_attack = max(1, selected_stats.physical_attack)
        self.player_defence = max(0, selected_stats.physical_defence)
        self.monster_attack = 10
        self.monster_defence = 0
        self.phase = 'idle'
        self.encounter_seq += 1
        self.trace_id = f'BT-{player_id}-{monster_id}-{self.encounter_seq}'
        self.escape_guard = None

    def finish(self) -> None:
        self.active = False
        self.phase = 'idle'

    def reset_encounter(self) -> None:
        """Respawn the connection-local trial monster on a map reload."""
        self.finish()
        self.monster_defeated = False
        self.trace_id = ''
        self.escape_guard = None
        self.player_tile = None

    def set_escape_guard(
        self,
        map_id: int,
        monster_id: int,
        player_id: int,
        origin: tuple[int, int] | None,
    ) -> None:
        """Prevent an immediate same-map/same-monster re-trigger."""
        self.escape_guard = {
            'map_id': int(map_id),
            'monster_id': int(monster_id),
            'player_id': int(player_id),
            'origin': (int(origin[0]), int(origin[1])) if origin else None,
        }

    def clear_escape_guard(self) -> None:
        self.escape_guard = None

    def escape(self) -> bool:
        """Finish server state as the APK starts its native escape movement."""
        if not self.active:
            return False
        origin = self.player_tile
        self.finish()
        self.set_escape_guard(self.map_id, self.monster_id, self.player_id, origin)
        return True

    def apply_basic_attack(self, damage: int = 10) -> bool:
        """Apply one deterministic local attack and report whether it ended."""
        if not self.active:
            return True
        self.monster_hp = max(0, self.monster_hp - max(1, damage))
        return self.monster_hp == 0

    def player_basic_attack_damage(self) -> int:
        return max(1, self.player_attack - (self.monster_defence // 2))

    def monster_basic_attack_damage(self, *, defending: bool = False) -> int:
        damage = max(1, self.monster_attack - (self.player_defence // 2))
        return max(1, damage // 2) if defending else damage


# The APK does not contain the authoritative server-side reward table.  Keep
# the local trial encounter deterministic, but persist its result through the
# same role/inventory records used by the rest of the service.
BATTLE_EXP_REWARD = 50
BATTLE_DROP_TEMPLATE_ID = 260_000_001
MAX_ROLE_LEVEL = 99
LEVEL_BASE_STAT_GAIN = 1
DEFAULT_BAG_CAPACITY = 40
DEFAULT_CURRENCY_BALANCE = 10_000_000
MAX_CURRENCY_BALANCE = 2_147_483_647
CURRENCY_PROPERTIES = {
    'immortal_stones': 49,
    'silver': 50,
    'immortal_crystals': 52,
}


def initial_currency_balances() -> dict[str, int]:
    return {
        name: DEFAULT_CURRENCY_BALANCE
        for name in CURRENCY_PROPERTIES
    }


def normalized_currency_balance(value: object) -> int:
    if type(value) is int and 0 <= value <= MAX_CURRENCY_BALANCE:
        return value
    return DEFAULT_CURRENCY_BALANCE


# 1042 only appends records to the APK's battle queue. The following full
# 1040/action=2 calls the battle screen's i() method and starts playback. The
# client then returns the short [action=2, round] acknowledgement after the
# complete queue has drained, so the server never guesses sprite timings.
ROLE_MODELS = (
    ((0, 2, 4), (19, 23, 1, 3, 5)),
    ((6, 8, 10), (7, 9, 11)),
    ((12, 14, 16), (13, 15, 17)),
)

SECTS = {
    0: '无',
    1: '昆仑',
    2: '玄都洞',
    3: '瑶池',
    4: '蓬莱岛',
    5: '轩辕宫',
    6: '崂山',
    7: '蜀山',
    8: '女儿国',
    9: '碧游宫',
    10: '刑天殿',
    11: '幽冥地府',
    12: '兰若寺',
    13: '古仙人',
}

TEST_SECT_ID = 1
TEST_SKILL_ID = 10001
TEST_SKILL_NAME = '协议测试技能'
TEST_SKILL_DEFAULT_LEVEL = 3
TEST_SKILL_MAX_LEVEL = 20

ROLE_STATS = (
    (2, 16, 7, 28, 7, 18, 3, 15, 2, 15, 7, 14, 8, 15, 3, 11, 17, 28, 2, 16, 7, 28, 7, 18),
    (7, 7, 3, 25, 3, 25, 4, 22, 2, 22, 3, 23, 2, 22, 4, 1, 5, 25, 7, 7, 3, 25, 3, 25),
    (16, 14, 17, 41, 2, 9, 4, 13, 17, 7, 17, 9, 5, 13, 4, 9, 6, 41, 16, 14, 17, 41, 2, 9),
    (3, 0, 10, 49, 4, 6, 8, 10, 9, 4, 10, 0, 5, 10, 8, 0, 6, 49, 3, 0, 10, 49, 4, 6),
    (3, 6, 4, 16, 7, 5, 0, 4, 9, 7, 4, 1, 9, 4, 9, 6, 1, 16, 3, 6, 4, 16, 7, 5),
    (4, 21, 1, 46, 1, 9, 7, 1, 27, 1, 1, 5, 4, 1, 7, 22, 8, 46, 4, 21, 1, 46, 1, 9),
    (2, 1, 7, 3, 5, 3, 4, 7, 9, 5, 7, 6, 6, 7, 4, 9, 3, 3, 2, 1, 7, 3, 5, 3),
)


def is_player_escape_command(command_code: int) -> bool:
    """C->S 1041 command 6 is escape; command 10 is quit-spectator."""
    return int(command_code) == 6


def should_suppress_escape_retrigger(
    guard: dict[str, object] | None,
    map_id: int,
    monster_id: int,
) -> bool:
    """Suppress only the guarded monster on the guarded map."""
    if not guard:
        return False
    return (
        int(guard.get('map_id', -1)) == int(map_id)
        and int(guard.get('monster_id', -1)) == int(monster_id)
    )


def update_escape_guard_for_movement(state: LocalBattleState, x: int, y: int) -> bool:
    """Update the last tile and clear the guard only after real movement."""
    new_tile = (int(x), int(y))
    state.player_tile = new_tile
    guard = state.escape_guard
    if not guard:
        return False
    origin = guard.get('origin')
    if origin is None:
        guard['origin'] = new_tile
        return False
    if tuple(origin) == new_tile:
        return False
    state.clear_escape_guard()
    return True


# Protocol 1008 field 12 is not the equipment quality.  The original client
# turns this short into a 24x24 atlas lookup via ``a.c.x.f(int)``:
#
#   image id = 3_002_424 + (icon_code // 100 % 100) * 10_000
#   frame    = icon_code % 100
#
# These codes point at atlases already bundled in the APK.  The icon code is
# independent from the template id and from the equipment location byte.
# ``pmsj.work.e.af`` names the original equipment locations 1..14 exactly as
# listed below.  Groups 1..13 are matching armour/accessory icon atlases;
# groups 21..33 contain the different weapon families.
DEFAULT_MOUNT_MODEL = 105000
MOUNT_EQUIPMENT_SLOT = 17  # APK resource 0x4661: the dedicated "坐骑" slot.

# Protocol 1502 multiplexes two different resource requests. Action 1 asks for
# a role .dat and is answered by 1503; actions 0/2 ask for an image and must be
# answered by 1501. The battle actors use logical model ids while the bundled
# role directory keeps the monster sprite after the same 0x200b20 offset used
# by map actors.
BATTLE_RESOURCE_MODEL_OFFSET = 0x200B20
BATTLE_RESOURCE_ALIASES = {
    # A normal kind-1 fighter is constructed with logical model 6. The thin
    # APK does not bundle role/6.dat; its preloaded composite-player layout is
    # role/100000.dat, which is the matching server-delivered template.
    6: 100_000,
}
# The APK requests role/0.dat for the built-in basic-attack animation.  This
# is an optional empty effect definition in the original client; completing
# the 1503 transfer with zero bytes lets the animation queue advance while
# the accompanying image atlas is still loaded normally.
BATTLE_EMPTY_RESOURCE_IDS = {0}
PNG_QUERY_MAIN_CACHE = 0
PNG_QUERY_ROLE_CACHE = 2

# The player sprite is composed from independently replaceable image layers.
# Property 7 selects the weapon family; properties 14..20 select trousers,
# armour, shoulders, wrists, boots, cape and helmet respectively. Zero is the
# unequipped state (property 14 resolves zero to the bundled base trousers).
BASE_CHARACTER_APPEARANCE = {
    7: 0,
    14: 0,
    15: 0,
    16: 0,
    17: 0,
    18: 0,
    19: 0,
    20: 0,
}

STACKABLE_ITEM_FLAG = 0x40


def role_race_and_gender(model: int) -> tuple[int, int]:
    for race, gender_models in enumerate(ROLE_MODELS):
        for gender, models in enumerate(gender_models):
            if model in models:
                return race, gender
    return 0, 0


def role_stats(model: int) -> list[int]:
    if not 0 <= model < 24:
        return [0] * 8
    return [values[model] for values in ROLE_STATS] + [0]


def default_role(settings: Settings) -> dict[str, object]:
    initial_map = settings.map_registry.require(settings.default_map_id)
    role = {
        'id': settings.role_id,
        'name': settings.role_name,
        'model': settings.role_model,
        'slot': 0,
        'race': 0,
        'sect_id': 0,
        'gender': 0,
        'level': 1,
        'experience': 0,
        'auto_level': True,
        'stats': [0] * 8,
        'map_id': initial_map.id,
        'map_name': initial_map.name,
        'map_x': initial_map.spawn_x,
        'map_y': initial_map.spawn_y,
        'mount_model': 0,
        'bag_capacity': DEFAULT_BAG_CAPACITY,
        'currencies': initial_currency_balances(),
    }
    role['items'] = starter_items(int(role['id']), settings.item_registry)
    role['strengthening_stones_initialized'] = True
    role['mailbox'] = starter_mail(int(role['id']))
    role['mailbox_initialized'] = True
    return role


def normalized_sect_id(role: dict[str, object]) -> int:
    """Return a client-safe sect ID for the 1006 property table."""
    try:
        sect_id = int(role.get('sect_id', 0))
    except (TypeError, ValueError):
        return 0
    return sect_id if sect_id in SECTS else 0


def join_sect(role: dict[str, object], sect_id: int) -> bool:
    """Join one valid sect while the role currently has no sect."""
    if sect_id not in SECTS or sect_id == 0 or normalized_sect_id(role) != 0:
        return False
    role['sect_id'] = sect_id
    return True


def settings_for_map(settings: Settings, map_id: int) -> MapDefinition:
    """Return one independently validated map definition."""
    return settings.map_registry.require(map_id)


def settings_for_role(settings: Settings, role: dict[str, object] | None) -> MapDefinition:
    map_id = (
        int(role.get('map_id', settings.default_map_id))
        if role is not None
        else settings.default_map_id
    )
    definition = settings_for_map(settings, map_id)
    if role is None:
        return definition
    return definition.with_spawn(
        int(role.get('map_x', definition.spawn_x)),
        int(role.get('map_y', definition.spawn_y)),
    )


def apply_portal_transition(
    settings: Settings,
    role: dict[str, object],
    object_id: int,
) -> MapDefinition | None:
    """Apply one current-map portal and return its target definition."""
    current_map_id = int(role.get('map_id', settings.default_map_id))
    portal = settings.map_registry.portal(current_map_id, object_id)
    if portal is None:
        return None
    target = settings.map_registry.require(portal.target_map_id)
    role['map_id'] = target.id
    role['map_name'] = target.name
    role['map_x'] = portal.target_x
    role['map_y'] = portal.target_y
    return target.with_spawn(portal.target_x, portal.target_y)


def starter_items(
    role_id: int,
    registry: ItemRegistry | None = None,
) -> list[dict[str, object]]:
    """Return the starter inventory understood by the original client."""
    if registry is None:
        registry = default_item_registry()
    return registry.starter_instances(role_id)


def starter_mail(role_id: int) -> list[dict[str, object]]:
    """Return the one persisted system mail delivered to a new or legacy role."""
    return [{
        'id': (role_id * 100) + 90,
        'sender': '系统',
        'subject': '欢迎来到本地服',
        'body': '欢迎来到《飘渺三界2》本地服。_这封邮件会随角色存档保存。',
        'sent_at': '2026-09-01',
        'expires_at': '长期有效',
        'read': False,
    }]


class RoleStore:
    def __init__(self, settings: Settings):
        path = Path(settings.role_data_file)
        self.path = path if path.is_absolute() else Path(__file__).resolve().parent / path
        self.settings = settings
        self.data: dict[str, object] = {'next_role_id': settings.role_id + 1, 'accounts': {}}
        if self.path.exists():
            try:
                loaded = json.loads(self.path.read_text(encoding='utf-8'))
                if isinstance(loaded, dict) and isinstance(loaded.get('accounts'), dict):
                    self.data = loaded
            except (OSError, ValueError) as exc:
                LOG.warning('failed to load role data %s: %s', self.path, exc)

    def _save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_suffix(self.path.suffix + '.tmp')
        temporary.write_text(json.dumps(self.data, ensure_ascii=False, indent=2), encoding='utf-8')
        temporary.replace(self.path)

    def save(self) -> None:
        self._save()

    def _ensure_items(
        self,
        role: dict[str, object],
    ) -> bool:
        registry = self.settings.item_registry
        items = role.get('items')
        if not isinstance(items, list):
            role['items'] = starter_items(int(role.get('id', 0)), registry)
            role['strengthening_stones_initialized'] = True
            return True
        changed = False
        stones_initialized = bool(role.get('strengthening_stones_initialized', False))
        defaults = starter_items(int(role.get('id', 0)), registry)
        by_id = {
            int(item.get('id', 0)): item
            for item in items
            if isinstance(item, dict)
        }
        stones_by_template = {
            int(item.get('template_id', 0)): item
            for item in items
            if isinstance(item, dict) and is_strengthening_stone(item)
        }
        # Strip template fields from legacy items that still carry them.
        template_owned_fields = {
            'kind', 'name', 'description', 'max_quantity', 'price',
            'level_required', 'icon_code', 'quality', 'sort_group',
            'sort_order', 'equipment_slot', 'innate_attributes',
            'acquired_attributes', 'extra_attributes', 'appearance_properties',
            'item_flags', 'action_flags', 'heal', 'mount_model',
        }
        for item in items:
            if not isinstance(item, dict):
                continue
            before_keys = set(item.keys())
            for field_name in template_owned_fields:
                item.pop(field_name, None)
            if set(item.keys()) != before_keys:
                changed = True
        # Upgrade the two legacy test items in place and append the missing
        # equipment slots.  Location and quantities are player state, so they
        # survive this catalogue migration.
        for default in defaults:
            item_id = int(default['id'])
            if is_strengthening_stone(default):
                template_id = int(default['template_id'])
                current = stones_by_template.get(template_id)
                if current is None and stones_initialized:
                    continue
                if current is None:
                    conflicting = by_id.get(item_id)
                    if conflicting is not None:
                        used_ids = set(by_id)
                        replacement_id = (int(role.get('id', 0)) * 100) + 20
                        while replacement_id in used_ids:
                            replacement_id += 1
                        conflicting['id'] = replacement_id
                        del by_id[item_id]
                        by_id[replacement_id] = conflicting
                        changed = True
                        LOG.warning(
                            'reassigned legacy item id collision role_id=%s old_id=%d new_id=%d',
                            role.get('id', 0),
                            item_id,
                            replacement_id,
                        )
            else:
                current = by_id.get(item_id)
            if current is None:
                items.append(default)
                by_id[item_id] = default
                if is_strengthening_stone(default):
                    stones_by_template[int(default['template_id'])] = default
                changed = True
                continue
            preserved = {
                key: current[key]
                for key in (
                    'id',
                    'location',
                    'quantity',
                    'last_heal',
                    'strengthen_level',
                    'base_equipment_attributes',
                )
                if key in current
            }
            # Only preserve equipment_attributes if the item has been modified
            # (strengthened or has base_equipment_attributes). Otherwise, let
            # the template default from the registry take precedence.
            if 'base_equipment_attributes' in current or 'strengthen_level' in current:
                if 'equipment_attributes' in current:
                    preserved['equipment_attributes'] = list(current['equipment_attributes'])
            resolved_default = registry.resolve(default)
            if (
                int(resolved_default.get('equipment_slot', 0)) == 10
                and 'base_equipment_attributes' not in current
                and 'equipment_attributes' in current
            ):
                # Before strengthening existed, the effective weapon values
                # were also its base values. Seed the new stable base from the
                # persisted weapon instead of replacing custom legacy stats
                # with the starter catalogue defaults.
                current_attributes = list(
                    current.get('equipment_attributes', [0, 0, 0, 0])
                )
                base_attributes = [
                    (
                        current_attributes[index]
                        if index < len(current_attributes)
                        and type(current_attributes[index]) is int
                        and current_attributes[index] >= 0
                        else 0
                    )
                    for index in range(4)
                ]
                raw_level = current.get('strengthen_level', 0)
                level = normalized_strengthen_level(current)
                if type(raw_level) is int and 0 < raw_level <= 9:
                    base_attributes[0] = max(
                        0,
                        base_attributes[0] - STRENGTHENING_ATTACK_BONUSES[level],
                    )
                preserved['base_equipment_attributes'] = base_attributes
            resolved_default = registry.resolve(default)
            # Determine if this is a weapon before stripping template fields.
            is_weapon = int(resolved_default.get('equipment_slot', 0)) == 10
            # Strip template-owned fields from the resolved default before
            # merging.  Only preserved instance state should survive into the
            # role item; template fields are resolved at read time.
            for field_name in template_owned_fields:
                resolved_default.pop(field_name, None)
            merged = {**resolved_default, **preserved}
            if is_weapon:
                weapon_level = normalized_strengthen_level(current) if 'strengthen_level' in current else normalized_strengthen_level(merged)
                merged['strengthen_level'] = weapon_level
                recalculate_equipment_attributes(merged)
            if current != merged:
                current.clear()
                current.update(merged)
                changed = True
        # Handle extra items that don't match any starter default.
        # These need template field stripping and weapon base seeding.
        for item in items:
            if not isinstance(item, dict):
                continue
            item_id = int(item.get('id', 0))
            if item_id in {int(d['id']) for d in defaults}:
                continue
            resolved = registry.resolve(item)
            if (
                int(resolved.get('equipment_slot', 0)) == 10
                and 'base_equipment_attributes' not in item
            ):
                if 'equipment_attributes' in item:
                    current_attributes = list(item['equipment_attributes'])
                else:
                    current_attributes = list(
                        resolved.get('equipment_attributes', [0, 0, 0, 0])
                    )
                base_attributes = [
                    (
                        current_attributes[index]
                        if index < len(current_attributes)
                        and type(current_attributes[index]) is int
                        and current_attributes[index] >= 0
                        else 0
                    )
                    for index in range(4)
                ]
                raw_level = item.get('strengthen_level', 0)
                level = normalized_strengthen_level(item)
                if type(raw_level) is int and 0 < raw_level <= 9:
                    base_attributes[0] = max(
                        0,
                        base_attributes[0] - STRENGTHENING_ATTACK_BONUSES[level],
                    )
                item['base_equipment_attributes'] = base_attributes
                changed = True
        if not stones_initialized:
            role['strengthening_stones_initialized'] = True
            changed = True
        for item in items:
            if not isinstance(item, dict) or not is_strengthenable_weapon(item):
                continue
            before_strengthening = copy.deepcopy(item)
            raw_level = item.get('strengthen_level', 0)
            level = normalized_strengthen_level(item)
            if 'base_equipment_attributes' not in item:
                # For new weapons, initialise base from the catalogue
                # template rather than from the (possibly absent) instance
                # equipment_attributes.
                if 'equipment_attributes' in item:
                    current_attributes = list(item['equipment_attributes'])
                else:
                    resolved = registry.resolve(item)
                    current_attributes = list(
                        resolved.get('equipment_attributes', [0, 0, 0, 0])
                    )
                base_attributes = []
                for index in range(4):
                    value = current_attributes[index] if index < len(current_attributes) else 0
                    base_attributes.append(
                        value if type(value) is int and value >= 0 else 0
                    )
                if type(raw_level) is int and 0 < raw_level <= 9:
                    base_attributes[0] = max(
                        0,
                        base_attributes[0] - STRENGTHENING_ATTACK_BONUSES[level],
                    )
                item['base_equipment_attributes'] = base_attributes
            item['strengthen_level'] = level
            recalculate_equipment_attributes(item)
            if item != before_strengthening:
                changed = True
        return changed

    @staticmethod
    def _ensure_mailbox(role: dict[str, object]) -> bool:
        mailbox = role.get('mailbox')
        if not bool(role.get('mailbox_initialized', False)):
            if not isinstance(mailbox, list):
                role['mailbox'] = starter_mail(int(role.get('id', 0)))
            role['mailbox_initialized'] = True
            return True
        if not isinstance(mailbox, list):
            role['mailbox'] = []
            return True
        return False

    def roles_for(self, username: str) -> list[dict[str, object]]:
        accounts = self.data['accounts']
        assert isinstance(accounts, dict)
        if username not in accounts:
            accounts[username] = [default_role(self.settings)]
            self._save()
        roles = accounts[username]
        assert isinstance(roles, list)
        changed = False
        for role in roles:
            if 'experience' not in role:
                role['experience'] = 0
                changed = True
            if 'auto_level' not in role:
                role['auto_level'] = True
                changed = True
            if 'sect_id' not in role:
                role['sect_id'] = 0
                changed = True
            if 'bag_capacity' not in role:
                role['bag_capacity'] = DEFAULT_BAG_CAPACITY
                changed = True
            currencies = role.get('currencies')
            if not isinstance(currencies, dict):
                currencies = initial_currency_balances()
                role['currencies'] = currencies
                changed = True
            for name in CURRENCY_PROPERTIES:
                current_balance = currencies.get(name)
                normalized_balance = normalized_currency_balance(current_balance)
                if type(current_balance) is not int or current_balance != normalized_balance:
                    currencies[name] = normalized_balance
                    changed = True
            try:
                current_map = self.settings.map_registry.require(
                    int(role.get('map_id', self.settings.default_map_id))
                )
            except (TypeError, ValueError):
                current_map = self.settings.map_registry.require(self.settings.default_map_id)
                LOG.warning(
                    'role %s referenced unknown map %r; migrating to default map %d',
                    role.get('id', 0),
                    role.get('map_id'),
                    current_map.id,
                )
                role['map_id'] = current_map.id
                changed = True
            if role.get('map_name') != current_map.name:
                role['map_name'] = current_map.name
                changed = True
            if 'map_x' not in role:
                role['map_x'] = current_map.spawn_x
                changed = True
            if 'map_y' not in role:
                role['map_y'] = current_map.spawn_y
                changed = True
            changed = self._ensure_items(role) or changed
            changed = self._ensure_mailbox(role) or changed
        if changed:
            self._save()
        return sorted(roles, key=lambda role: int(role.get('slot', 0)))

    def find(self, username: str, role_id: int) -> dict[str, object] | None:
        return next((role for role in self.roles_for(username) if int(role.get('id', 0)) == role_id), None)

    def create(self, username: str, name: str, model: int, requested_slot: int) -> dict[str, object]:
        roles = self.roles_for(username)
        occupied = {int(role.get('slot', 0)) for role in roles}
        slot = requested_slot if requested_slot in range(3) and requested_slot not in occupied else -1
        if slot < 0:
            slot = next((candidate for candidate in range(3) if candidate not in occupied), 0)
        valid_models = {value for race in ROLE_MODELS for gender in race for value in gender}
        if model not in valid_models:
            model = 0
        race, gender = role_race_and_gender(model)
        role_id = int(self.data.get('next_role_id', self.settings.role_id + 1))
        self.data['next_role_id'] = role_id + 1
        initial_map = self.settings.map_registry.require(self.settings.default_map_id)
        role: dict[str, object] = {
            'id': role_id,
            'name': name.strip() or f'本地侠客{role_id}',
            'model': model,
            'slot': slot,
            'race': race,
            'sect_id': 0,
            'gender': gender,
            'level': 1,
            'experience': 0,
            'auto_level': True,
            'stats': role_stats(model),
            'map_id': initial_map.id,
            'map_name': initial_map.name,
            'map_x': initial_map.spawn_x,
            'map_y': initial_map.spawn_y,
            'bag_capacity': DEFAULT_BAG_CAPACITY,
            'currencies': initial_currency_balances(),
        }
        role['items'] = starter_items(role_id, self.settings.item_registry)
        role['strengthening_stones_initialized'] = True
        role['mailbox'] = starter_mail(role_id)
        role['mailbox_initialized'] = True
        roles.append(role)
        accounts = self.data['accounts']
        assert isinstance(accounts, dict)
        accounts[username] = roles
        self._save()
        return role

    def delete(self, username: str, role_id: int) -> bool:
        roles = self.roles_for(username)
        remaining = [role for role in roles if int(role.get('id', 0)) != role_id]
        if len(remaining) == len(roles):
            return False
        accounts = self.data['accounts']
        assert isinstance(accounts, dict)
        accounts[username] = remaining
        self._save()
        return True


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
    for role in roles:
        race = int(role.get('race', 0))
        gender = int(role.get('gender', 0))
        record = [
            integer(int(role['id'])),
            integer(race),
            integer(int(role.get('level', 1))),
            integer(int(role.get('model', settings.role_model))),
            integer((race * 10) + gender),
            string(str(role.get('name', settings.role_name))),
            integer(int(role.get('slot', 0))),
        ]
        stats = list(role.get('stats', [0] * 8))
        record.extend(integer(int(value)) for value in (stats + [0] * 8)[:8])
        records.extend(record)
    # 响应的 action 字段由客户端 w.b(0) 读取，必须是 short；客户端发来的
    # 1080 请求则使用 byte action。这是该协议的非对称字段类型之一。
    return encode_frame(1080, [short(0), byte(len(roles)), *records])


def creation_names() -> bytes:
    # 创建界面当前种族有男女两个分支，因此 action=4 后固定读取两个名字。
    return encode_frame(1080, [short(4), string('云生'), string('月华')])


def deletion_result(role_id: int) -> bytes:
    return encode_frame(1080, [short(1), integer(role_id)])


def player_info(settings: Settings, role: dict[str, object] | None = None) -> bytes:
    role = role if role is not None else default_role(settings)
    # 1006 的第 0 字段是连续属性数量。地图只会读取前 30 项，但人物
    # 面板会继续读取到属性 84（斗法排行），所以发送完整的 0..84 表。
    properties = [integer(0) for _ in range(85)]
    properties[1] = integer(int(role['id']))
    properties[3] = string(str(role.get('name', settings.role_name)))
    properties[6] = integer(int(role.get('model', settings.role_model)))
    properties[10] = string('')
    properties[11] = integer(int(role.get('level', 1)))
    # property 12 = 门派 ID; property 39 = 种族 ID.
    properties[12] = integer(normalized_sect_id(role))
    # Item icons/templates and character image layers are separate catalogues.
    # Only verified appearance pairs are applied here.
    for property_index, value in character_appearance(role, settings.item_registry).items():
        properties[property_index] = integer(value)
    properties[23] = integer(1000)
    properties[22] = integer(int(role.get('mount_model', 0)))
    properties[24] = integer(1)
    properties[25] = integer(0)
    level = max(1, int(role.get('level', 1)))
    experience = max(0, int(role.get('experience', 0)))
    properties[31] = long_integer(experience)
    properties[32] = long_integer(max(100, level * 100))
    properties[38] = integer(0)
    properties[39] = integer(int(role.get('race', 0)))

    level = max(1, int(role.get('level', 1)))
    raw_stats = [int(value) for value in list(role.get('stats', []))]
    base_stats = (raw_stats + [10, 10, 10, 10, 10])[:5]
    max_hp = 100 + ((level - 1) * 10) + max(0, base_stats[1])
    max_mp = 50 + ((level - 1) * 5) + max(0, base_stats[2])
    properties[40] = integer(max_hp)
    properties[41] = integer(max_hp)
    properties[42] = integer(max_mp)
    properties[43] = integer(max_mp)
    for index, value in enumerate(base_stats, start=44):
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
    return encode_frame(1006, [
        integer(len(properties)),
        *properties,
        integer(int(time.time())),
    ])


def character_extension_info() -> bytes:
    """Initialize the optional rows consumed by the character base page.

    The original client keeps these rows in ``pmsj.work.b.f.u``.  That field
    starts as null and the base page calls ``size()`` without checking it, so
    protocol 1089/action 0 must be delivered even when there are no rows.
    """
    return encode_frame(1089, [byte(0), byte(0)])


def character_skill_list(role: dict[str, object]) -> bytes:
    """Return the minimal action-0 skill list appropriate for one role."""
    sect_id = normalized_sect_id(role)
    if sect_id == TEST_SECT_ID:
        skill_id = TEST_SKILL_ID
        skill_name = TEST_SKILL_NAME
        level = sect_skill_level(role)
        max_level = TEST_SKILL_MAX_LEVEL
        proficiency = 123
        max_proficiency = 1000
        flags = 1  # APK: field[6] bit 0 enables proficiency display.
        skill = [
            string(skill_name),
            integer(skill_id),
            integer(level),
            integer(max_level),
            integer(proficiency),
            integer(max_proficiency),
            integer(flags),
            *(integer(0) for _ in range(7)),
        ]
    else:
        skill_id = 0
        skill_name = '基础技能'
        level = max_level = proficiency = max_proficiency = flags = 0
        skill = [
            string(skill_name),
            integer(skill_id),
            integer(0),
            integer(0),
            integer(0),
            integer(0),
            integer(0),
            *(integer(0) for _ in range(7)),
        ]

    LOG.info(
        'SKILL_1132_LIST role_id=%s sect_id=%d count=1 skill_id=%d name=%r '
        'level=%d/%d proficiency=%d/%d flags=%d',
        role.get('id', 0), sect_id, skill_id, skill_name,
        level, max_level, proficiency, max_proficiency, flags,
    )
    return encode_frame(1132, [byte(0), byte(1), *skill])


def sect_skill_list(role: dict[str, object]) -> bytes:
    """Return the minimal protocol-1103 list consumed by the sect-skill page."""
    sect_id = normalized_sect_id(role)
    if sect_id != TEST_SECT_ID:
        LOG.info(
            'SKILL_1103_LIST role_id=%s sect_id=%d count=0',
            role.get('id', 0), sect_id,
        )
        return encode_frame(1103, [byte(0), byte(0)])

    skill_id = TEST_SKILL_ID
    skill_name = TEST_SKILL_NAME
    level = sect_skill_level(role)
    max_level = TEST_SKILL_MAX_LEVEL
    slot = 1
    record = [
        string(skill_name),
        integer(skill_id),
        integer(level),
        integer(max_level),
        integer(0),  # field[4]: icon code; zero is a valid APK image object.
        *(integer(0) for _ in range(7)),
        integer(slot),  # field[12]: native sect-skill slot, 1..14.
        integer(0),
    ]
    LOG.info(
        'SKILL_1103_LIST role_id=%s sect_id=%d count=1 skill_id=%d name=%r '
        'level=%d/%d slot=%d',
        role.get('id', 0), sect_id, skill_id, skill_name,
        level, max_level, slot,
    )
    return encode_frame(1103, [byte(0), byte(1), *record])


def sect_skill_level(role: dict[str, object]) -> int:
    """Return the persisted level of the local sect-skill probe."""
    if normalized_sect_id(role) != TEST_SECT_ID:
        return 0
    levels = role.get('skill_levels')
    if not isinstance(levels, dict):
        return TEST_SKILL_DEFAULT_LEVEL
    try:
        level = int(levels.get(str(TEST_SKILL_ID), TEST_SKILL_DEFAULT_LEVEL))
    except (TypeError, ValueError):
        level = TEST_SKILL_DEFAULT_LEVEL
    return max(0, min(TEST_SKILL_MAX_LEVEL, level))


def sect_skill_detail_frame(role: dict[str, object], skill_id: int) -> bytes:
    """Answer the native 1103/action-2 skill detail and learning-condition query.

    ``pmsj/work/e/dy.a(main/w)`` reads the first three fields as
    ``action, skill id, current level``.  It then consumes five integer
    conditions, effect/current/next strings, and the required-item
    ``int, string, int`` triple.  Returning nothing leaves the client's
    global wait flag set.
    """
    if normalized_sect_id(role) != TEST_SECT_ID or int(skill_id) != TEST_SKILL_ID:
        return encode_frame(1103, [byte(3)])
    return encode_frame(1103, [
        byte(2),
        integer(TEST_SKILL_ID),
        integer(sect_skill_level(role)),
        integer(1),  # Required character level.
        integer(0),  # Silver cost for the local probe.
        integer(0),  # Experience cost for the local probe.
        integer(0),  # First prerequisite-skill level.
        integer(0),  # Second prerequisite-skill level.
        string('本地测试技能效果：用于验证技能学习与升级。'),
        string('协议测试技能说明'),
        string('下一级效果：技能等级提高。'),
        integer(0),  # Required item template id; zero means no item.
        string(''),  # Required item display name.
        integer(0),  # Required item quantity.
    ])


def sect_skill_request_frames(
    role: dict[str, object],
    values: list[object],
) -> tuple[bytes, ...]:
    """Handle the confirmed native sect-skill request actions."""
    if not values:
        return (encode_frame(1103, [byte(3)]),)
    action = int(values[0])
    if action == 6:
        return (sect_skill_list(role),)

    skill_id = int(values[1]) if len(values) > 1 else 0
    valid_skill = (
        normalized_sect_id(role) == TEST_SECT_ID
        and skill_id == TEST_SKILL_ID
    )
    if action == 2:
        return (sect_skill_detail_frame(role, skill_id),)
    if action == 3 and valid_skill:
        current_level = sect_skill_level(role)
        if current_level < TEST_SKILL_MAX_LEVEL:
            levels = role.get('skill_levels')
            if not isinstance(levels, dict):
                levels = {}
                role['skill_levels'] = levels
            levels[str(TEST_SKILL_ID)] = current_level + 1
            LOG.info(
                'SKILL_1103_LEARN role_id=%s skill_id=%d level=%d->%d',
                role.get('id', 0), TEST_SKILL_ID, current_level, current_level + 1,
            )
        # Action 0 replaces the record in b/y by skill id; action 5 redraws
        # the native sect page.  1132 keeps the character skill container in
        # sync for the battle/person screens.
        return (
            sect_skill_list(role),
            encode_frame(1103, [byte(5)]),
            character_skill_list(role),
        )

    # Action 3 is a native no-op response.  It still passes through main/e's
    # dispatcher and clears the global wait flag for stale/invalid requests.
    return (encode_frame(1103, [byte(3)]),)


def initial_skill_frames(role: dict[str, object]) -> tuple[bytes, bytes]:
    """Preload both skill containers before their native pages are opened."""
    return character_skill_list(role), sect_skill_list(role)


def character_panel_frames(role: dict[str, object]) -> tuple[bytes, bytes]:
    """Return the attribute and divine-power datasets requested by UI 31."""
    level = max(1, int(role.get('level', 1)))
    raw_stats = [int(value) for value in list(role.get('stats', []))]
    base_stats = [max(0, value) for value in (raw_stats + [10, 10, 10, 10, 10])[:5]]
    max_hp = 100 + ((level - 1) * 10) + base_stats[1]
    max_mp = 50 + ((level - 1) * 5) + base_stats[2]

    attribute_thresholds = [max_hp, max_mp, *base_stats]
    attributes = encode_frame(1039, [byte(1), *(integer(value) for value in attribute_thresholds)])

    divine_values = [int(role['id']), level, level, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    divine = encode_frame(1039, [byte(2), *(integer(value) for value in divine_values)])
    return attributes, divine


def role_items(role: dict[str, object]) -> list[dict[str, object]]:
    items = role.get('items', [])
    if not isinstance(items, list):
        return []
    # Keep the original list object: discard/use operations must also mutate the
    # list held by the role before RoleStore.save() serializes it.
    if any(not isinstance(item, dict) for item in items):
        items = [item for item in items if isinstance(item, dict)]
        role['items'] = items
    return items  # type: ignore[return-value]


def bag_capacity(role: dict[str, object]) -> int:
    """Return the persisted personal-inventory slot limit."""
    try:
        return max(0, int(role.get('bag_capacity', DEFAULT_BAG_CAPACITY)))
    except (TypeError, ValueError):
        return DEFAULT_BAG_CAPACITY


def bag_item_count(role: dict[str, object]) -> int:
    """Count occupied bag slots; stack quantity does not consume extra slots."""
    return sum(item.get('location', 'bag') == 'bag' for item in role_items(role))


def try_move_item_to_bag(role: dict[str, object], item: dict[str, object]) -> bool:
    """Move one owned item into the bag only when a slot is available."""
    if item.get('location', 'bag') == 'bag':
        return True
    if bag_item_count(role) >= bag_capacity(role):
        return False
    item['location'] = 'bag'
    return True


def item_action_location_valid(action: int, item: dict[str, object]) -> bool:
    """Match 1009 bag/equipment actions to the APK's item containers."""
    location = str(item.get('location', 'bag'))
    if int(action) in {3, 4, 5}:
        return location == 'bag'
    if int(action) == 6:
        return location == 'equipped'
    return True


def ensure_weapon_base_attributes(
    item: dict[str, object],
    registry: ItemRegistry | None = None,
) -> None:
    """Ensure a weapon item has base_equipment_attributes and strengthen_level.

    This is used when tests or callers work with minimal item instances that
    may not have gone through RoleStore._ensure_items() yet.
    """
    if not is_strengthenable_weapon(item):
        return
    if registry is None:
        registry = default_item_registry()
    resolved = registry.resolve(item)
    if 'base_equipment_attributes' not in item:
        # Use the template's equipment_attributes as the base.
        current_attributes = list(resolved.get('equipment_attributes', [0, 0, 0, 0]))
        base_attributes = [
            (
                current_attributes[index]
                if index < len(current_attributes)
                and type(current_attributes[index]) is int
                and current_attributes[index] >= 0
                else 0
            )
            for index in range(4)
        ]
        raw_level = item.get('strengthen_level', 0)
        level = normalized_strengthen_level(item)
        if type(raw_level) is int and 0 < raw_level <= 9:
            base_attributes[0] = max(
                0,
                base_attributes[0] - STRENGTHENING_ATTACK_BONUSES[level],
            )
        item['base_equipment_attributes'] = base_attributes
    if 'strengthen_level' not in item:
        item['strengthen_level'] = 0
    recalculate_equipment_attributes(item)


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
        appearance = resolved.get('appearance_properties', {})
        if not isinstance(appearance, dict):
            continue
        for property_index, value in appearance.items():
            index = int(property_index)
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


def level_experience_required(level: int) -> int:
    """Return the deterministic local EXP cost for the next level."""
    return max(100, max(1, int(level)) * 100)


def role_level_properties(role: dict[str, object]) -> dict[int, int]:
    """Return the level-dependent properties shown by the APK character UI."""
    level = max(1, min(MAX_ROLE_LEVEL, int(role.get('level', 1))))
    raw_stats = [int(value) for value in list(role.get('stats', []))]
    base_stats = [max(0, value) for value in (raw_stats + [10, 10, 10, 10, 10])[:5]]
    max_hp = 100 + ((level - 1) * 10) + base_stats[1]
    max_mp = 50 + ((level - 1) * 5) + base_stats[2]
    return {
        11: level,
        31: max(0, int(role.get('experience', 0))),
        32: level_experience_required(level),
        40: max_hp,
        41: max_hp,
        42: max_mp,
        43: max_mp,
        **{property_index: value for property_index, value in enumerate(base_stats, start=44)},
        80: level,
        # ``main/e.O`` treats 85/86 as the high-word refresh for the 64-bit
        # experience fields 31/32.  The low words remain in 31/32; keeping
        # both halves in the frame mirrors the APK's incremental update path.
        85: max(0, int(role.get('experience', 0))) >> 32,
        86: level_experience_required(level) >> 32,
    }


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
    """Ask the APK to redraw the open equipment tab without changing sprites.

    The original client refreshes the equipment-page widgets from its 1017
    character-update callback.  Accessory-only slots (belt, necklace, ring,
    coat, accessory and magic treasure) have no character sprite property, so
    their 1008 operation=3 update alone leaves an already-open panel stale.
    Re-sending the effective appearance values is visually a no-op but enters
    that callback and redraws the equipment vector.
    """
    return character_appearance_frame(int(role['id']), character_appearance(role, registry))


def find_item(role: dict[str, object], item_id: int) -> dict[str, object] | None:
    return next((item for item in role_items(role) if int(item.get('id', 0)) == item_id), None)


def item_slot(item: dict[str, object], registry: ItemRegistry | None = None) -> int:
    if 'equipment_slot' in item:
        return int(item['equipment_slot'])
    if registry is not None:
        resolved = registry.resolve(item)
        if 'equipment_slot' in resolved:
            return int(resolved['equipment_slot'])
    category = (int(item.get('template_id', 0)) // 10_000_000) % 100
    return category if 1 <= category <= 14 else 0


def is_equipment(item: dict[str, object]) -> bool:
    category = (int(item.get('template_id', 0)) // 10_000_000) % 100
    return 1 <= category <= 21


def is_strengthenable_weapon(item: dict[str, object]) -> bool:
    return is_equipment(item) and item_slot(item) == 10


def item_display_name(item: dict[str, object]) -> str:
    name = str(item.get('name', '未命名物品'))
    level = normalized_strengthen_level(item) if is_strengthenable_weapon(item) else 0
    return f'{name} +{level}' if level > 0 else name


def item_display_description(item: dict[str, object]) -> str:
    description = str(item.get('description', item.get('name', '物品')))
    if not is_strengthenable_weapon(item):
        return description
    level = normalized_strengthen_level(item)
    attributes = list(item.get('equipment_attributes', [0, 0, 0, 0]))
    attack = int(attributes[0]) if attributes else 0
    return f'{description}_强化：+{level}_当前攻击：{attack}'


def strengthening_open_frame() -> bytes:
    return encode_frame(1009, [
        short(97),
        string('请选择需要强化的装备和强化宝石。'),
    ])


def strengthening_equipment_frame(item: dict[str, object]) -> bytes:
    registry = default_item_registry()
    resolved = registry.resolve(item)
    attributes = list(resolved.get('equipment_attributes', [0, 0, 0, 0]))
    attack = int(attributes[0]) if attributes else 0
    level = normalized_strengthen_level(item)
    summary = f'{item_display_name(resolved)}_强化 +{level}，当前攻击：{attack}'
    return encode_frame(1009, [short(75), string(summary)])


def strengthening_equipment_error_frame(message: str) -> bytes:
    return encode_frame(1009, [short(75), string(message)])


def strengthening_rate_frame(
    item: dict[str, object],
    stone: dict[str, object],
) -> bytes:
    definition = stone_definition_for(stone)
    level = normalized_strengthen_level(item)
    rate = 0
    if definition is not None and level < 9:
        rate = rate_for(definition, level)
    text = f'单颗成功率：{rate / 100:.2f}%'
    return encode_frame(1009, [short(74), short(rate), string(text)])


def strengthening_rate_error_frame(message: str) -> bytes:
    return encode_frame(1009, [short(74), short(0), string(message)])


def strengthening_stone_selection_frame(valid: bool) -> bytes:
    fields = [short(77), byte(1 if valid else 0)]
    if valid:
        fields.append(byte(1))
    return encode_frame(1009, fields)


def strengthening_reset_frame() -> bytes:
    return encode_frame(1009, [short(78)])


STRENGTHENING_ACTIONS = {74, 75, 77, 92, 97}


@dataclass(frozen=True)
class StrengtheningActionResult:
    frames: tuple[bytes, ...]
    changed: bool
    message: str = ''


def _invalid_strengthening_result(message: str) -> StrengtheningActionResult:
    return StrengtheningActionResult(
        (top_message_frame(message), strengthening_reset_frame()),
        False,
        message,
    )


def strengthening_action_result(
    role: dict[str, object],
    values: list[object],
    rng=random,
) -> StrengtheningActionResult:
    """Apply one confirmed protocol-1009 strengthening action atomically."""
    if not values:
        return _invalid_strengthening_result('强化请求缺少操作类型')
    try:
        action = int(values[0])
    except (TypeError, ValueError):
        return _invalid_strengthening_result('强化请求格式错误')

    if action == 97:
        return StrengtheningActionResult((strengthening_open_frame(),), False)
    if action not in STRENGTHENING_ACTIONS:
        return StrengtheningActionResult((), False)

    try:
        weapon_id = int(values[1])
    except (IndexError, TypeError, ValueError):
        if action == 75:
            return StrengtheningActionResult(
                (strengthening_equipment_error_frame('请选择需要强化的武器'),),
                False,
                '请选择需要强化的武器',
            )
        if action == 74:
            return StrengtheningActionResult(
                (strengthening_rate_error_frame('请选择需要强化的武器'),),
                False,
                '请选择需要强化的武器',
            )
        return _invalid_strengthening_result('请选择需要强化的武器')
    weapon = find_item(role, weapon_id)
    valid_weapon = (
        weapon is not None
        and is_strengthenable_weapon(weapon)
        and str(weapon.get('location', 'bag')) in {'bag', 'equipped'}
    )
    if not valid_weapon or weapon is None:
        if action == 75:
            return StrengtheningActionResult(
                (strengthening_equipment_error_frame('只能强化背包或已装备的武器'),),
                False,
                '只能强化背包或已装备的武器',
            )
        if action == 74:
            return StrengtheningActionResult(
                (strengthening_rate_error_frame('只能强化背包或已装备的武器'),),
                False,
                '只能强化背包或已装备的武器',
            )
        return _invalid_strengthening_result('只能强化背包或已装备的武器')
    if action == 75:
        return StrengtheningActionResult((strengthening_equipment_frame(weapon),), False)

    try:
        stone_id = int(values[2])
    except (IndexError, TypeError, ValueError):
        if action == 77:
            return StrengtheningActionResult(
                (strengthening_stone_selection_frame(False),),
                False,
                '请选择强化石',
            )
        if action == 74:
            return StrengtheningActionResult(
                (strengthening_rate_error_frame('请选择强化石'),),
                False,
                '请选择强化石',
            )
        return _invalid_strengthening_result('请选择强化石')
    stone = find_item(role, stone_id)
    definition = stone_definition_for(stone) if stone is not None else None
    valid_stone = (
        stone is not None
        and definition is not None
        and is_strengthening_stone(stone)
        and str(stone.get('location', 'bag')) == 'bag'
        and type(stone.get('quantity')) is int
        and int(stone.get('quantity', 0)) > 0
    )
    if action == 77:
        if valid_stone:
            # The APK sends action 77 immediately before action 74. Its S→C
            # action-77/status=1 branch calls bw.n(), which clears both chosen
            # item slots; a valid selection must therefore be acknowledged by
            # the following action-74 rate frame only. Status 0 remains the
            # native directive for rejecting and clearing an invalid stone.
            return StrengtheningActionResult((), False)
        return StrengtheningActionResult(
            (strengthening_stone_selection_frame(False),),
            False,
            '强化石无效',
        )
    if not valid_stone or stone is None or definition is None:
        if action == 74:
            return StrengtheningActionResult(
                (strengthening_rate_error_frame('强化石无效或数量不足'),),
                False,
                '强化石无效或数量不足',
            )
        return _invalid_strengthening_result('强化石无效或数量不足')
    if action == 74:
        return StrengtheningActionResult(
            (strengthening_rate_frame(weapon, stone),),
            False,
        )

    try:
        count = int(values[3])
    except (IndexError, TypeError, ValueError):
        return _invalid_strengthening_result('强化石数量无效')
    level = normalized_strengthen_level(weapon)
    quantity = int(stone['quantity'])
    if type(values[3]) is bool or not 1 <= count <= 5 or count > quantity:
        return _invalid_strengthening_result('每次需投入 1 至 5 颗强化石，且不能超过持有数量')
    if level >= 9:
        return _invalid_strengthening_result('武器已达到最高强化等级 +9')

    succeeded = strengthening_success(definition, level, count, rng)
    next_level = level + 1 if succeeded else strengthening_failure_level(level)
    weapon['strengthen_level'] = next_level
    recalculate_equipment_attributes(weapon)
    remaining = quantity - count
    stone['quantity'] = remaining

    frames = [item_frame(weapon, operation=3), item_frame(stone, operation=3)]
    if remaining == 0:
        role_items(role).remove(stone)
        frames.append(encode_frame(1009, [short(3), integer(stone_id)]))
    resolved_weapon = default_item_registry().resolve(weapon)
    if succeeded:
        message = f'强化成功，{item_display_name(resolved_weapon)}'
    elif next_level == level:
        message = f'强化失败，等级保持 +{level}'
    else:
        message = f'强化失败，等级降至 +{next_level}'
    frames.extend((top_message_frame(message), strengthening_reset_frame()))
    return StrengtheningActionResult(tuple(frames), True, message)


def item_frame(
    item: dict[str, object],
    registry: ItemRegistry | None = None,
    operation: int = 1,
) -> bytes:
    """Encode the original client's complete 1008 item-instance record.

    The local protocol uses operation ``3`` for an equipment state update.
    This is the operation already understood by the bundled APK for both
    equip and unequip; changing it to another operation breaks the item's
    equip action menu.
    """
    if registry is None:
        registry = default_item_registry()
    resolved = registry.resolve(item)
    location = str(item.get('location', 'bag'))
    location_code = {'bag': 50, 'warehouse': 51}.get(location, item_slot(item, registry))
    fields = [
        byte(operation),
        integer(int(item['id'])),
        short(int(item.get('quantity', 1))),
        short(int(resolved.get('max_quantity', 1))),
        byte(location_code),
        integer(int(item.get('state_flags', 0))),
        integer(int(resolved.get('price', 0))),
        integer(int(item['template_id'])),
        string(item_display_name(resolved)),
        short(int(resolved.get('item_flags', 0))),
        short(int(resolved.get('action_flags', 0))),
        byte(int(resolved.get('level_required', 1))),
        short(int(resolved.get('icon_code', resolved.get('quality', 0)))),
        integer(int(item.get('expires_at', -1))),
        short(int(resolved.get('sort_group', 0))),
        short(int(resolved.get('sort_order', 0))),
    ]
    if is_equipment(item):
        base_attributes = list(resolved.get('equipment_attributes', [0, 0, 0, 0]))
        innate_attributes = list(item.get('innate_attributes', resolved.get('innate_attributes', [0, 0, 0, 0, 0])))
        acquired_attributes = list(item.get('acquired_attributes', resolved.get('acquired_attributes', [0, 0, 0, 0, 0])))
        extra_attributes = list(item.get('extra_attributes', resolved.get('extra_attributes', [0, 0, 0, 0, 0])))
        fields.extend(short(int(value)) for value in (base_attributes + [0] * 4)[:4])
        fields.extend(byte(int(value)) for value in (innate_attributes + [0] * 5)[:5])
        fields.extend(byte(int(value)) for value in (acquired_attributes + [0] * 5)[:5])
        fields.extend(short(int(value)) for value in (extra_attributes + [0] * 5)[:5])
    return encode_frame(1008, fields)


def item_description_frame(item: dict[str, object]) -> bytes:
    registry = default_item_registry()
    resolved = registry.resolve(item)
    return encode_frame(1009, [
        short(82),
        integer(int(item['id'])),
        string(item_display_description(resolved)),
    ])


def item_detail_frame(item: dict[str, object]) -> bytes:
    registry = default_item_registry()
    resolved = registry.resolve(item)
    return encode_frame(1032, [
        byte(1),
        integer(int(item.get('template_id', 0))),
        short(int(resolved.get('icon_code', resolved.get('quality', 0)))),
        string(item_display_description(resolved)),
    ])


def battle_reward_notice(experience: int, item: dict[str, object], level_up: bool = False) -> bytes:
    """Persist the deterministic result in the APK's notice cache.

    Protocol 1123 is not a visible notification: ``main/e.C`` only stores
    its version and text for the notice screen.  Keep it as a durable record,
    and use :func:`battle_reward_popup` for the immediate on-screen result.
    """
    level_text = '，升级了' if level_up else ''
    resolved = default_item_registry().resolve(item)
    name = resolved.get('name', '未知物品')
    text = f'战斗胜利{level_text}！获得经验 {experience}，获得 {name} x{item.get("quantity_gained", 1)}'
    # 1123/action 0 is the client's normal notice channel.  A timestamp-like
    # version makes each victory visible even when the previous notice was
    # already acknowledged locally.
    return encode_frame(1123, [byte(0), integer(int(time.time())), string(text)])


def battle_reward_popup(experience: int, item: dict[str, object], level_up: bool = False) -> bytes:
    """Open the APK's native top-of-map reward overlay (protocol 1049).

    ``main/e`` handles 1049/action 3 by passing the next five fields to the
    map screen's embedded ``e/bs`` overlay.  Its fixed layout is experience,
    pet experience, silver, cultivation and an item-count marker.  The
    overlay slides down from the top, remains visible for three seconds, and
    slides away; unlike protocol 1512 it does not open the centred ``br``
    prompt and therefore does not interrupt the map screen.

    The bundled client renders the length of the last string after ``获得``.
    Encode one marker character per awarded item so a single drop is shown as
    ``获得 1`` while the complete item instance is still delivered by 1008.
    """
    quantity = max(0, int(item.get('quantity_gained', 1)))
    item_count_marker = 'x' * quantity
    return encode_frame(1049, [
        byte(3),
        integer(max(0, int(experience))),
        integer(0),
        integer(0),
        integer(0),
        string(item_count_marker),
    ])


def top_message_frame(text: str) -> bytes:
    """Show one non-blocking message in the APK's native top map overlay."""
    return encode_frame(1049, [byte(4), string(text)])


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


def apply_one_level(role: dict[str, object]) -> bool:
    """Consume EXP for one level and persist deterministic base-stat growth."""
    level = max(1, int(role.get('level', 1)))
    experience = max(0, int(role.get('experience', 0)))
    if level >= MAX_ROLE_LEVEL or experience < level_experience_required(level):
        return False
    role['experience'] = experience - level_experience_required(level)
    role['level'] = level + 1
    raw_stats = [int(value) for value in list(role.get('stats', []))]
    base_stats = (raw_stats + [0] * 8)[:8]
    for index in range(5):
        base_stats[index] += LEVEL_BASE_STAT_GAIN
    role['stats'] = base_stats
    return True


def apply_battle_rewards(
    role: dict[str, object],
    experience: int = BATTLE_EXP_REWARD,
    registry: ItemRegistry | None = None,
) -> tuple[dict[str, object] | None, bool]:
    """Persist one trial victory and return the changed item plus level-up flag."""
    old_level = max(1, int(role.get('level', 1)))
    role['experience'] = max(0, int(role.get('experience', 0))) + max(0, experience)
    if bool(role.get('auto_level', True)):
        while int(role.get('level', 1)) < MAX_ROLE_LEVEL and apply_one_level(role):
            pass

    if registry is None:
        registry = default_item_registry()
    item = next(
        (candidate for candidate in role_items(role)
         if int(candidate.get('template_id', 0)) == BATTLE_DROP_TEMPLATE_ID
         and str(candidate.get('location', 'bag')) == 'bag'),
        None,
    )
    level_up = int(role.get('level', 1)) > old_level
    if item is None:
        if bag_item_count(role) >= bag_capacity(role):
            return None, level_up
        definition = registry.require(BATTLE_DROP_TEMPLATE_ID)
        item = {
            'id': (int(role.get('id', 0)) * 100) + 17,
            'template_id': BATTLE_DROP_TEMPLATE_ID,
            'quantity': 1,
            'location': 'bag',
        }
        role_items(role).append(item)
    else:
        definition = registry.require(BATTLE_DROP_TEMPLATE_ID)
        item['quantity'] = min(
            definition.max_quantity,
            int(item.get('quantity', 0)) + 1,
        )
    return item, level_up


def notice_and_world(settings: Settings, role: dict[str, object] | None = None) -> list[bytes]:
    role = role if role is not None else default_role(settings)
    current_map = settings_for_role(settings, role)
    notice = encode_frame(1123, [byte(0), integer(0), string('本地服务正常')])
    # 1110 字段 1/2 are the logical map id used by the client. The patched
    # APK carries the matching 50000.map.ref alias for the target map.
    client_map_id = current_map.id
    world = encode_frame(1110, [
        integer(0),
        integer(client_map_id),
        integer(client_map_id),
        string(current_map.name),
    ])
    return [notice, world]


def map_action(
    definition: MapDefinition,
    action: int,
    status: int = 0,
    role_id: int | None = None,
) -> bytes:
    # 游戏端读取 1010 应答时固定从字段 5 取动作码。
    return encode_frame(1010, [
        integer(10001 if role_id is None else role_id),
        short(definition.spawn_x),
        short(definition.spawn_y),
        integer(0),
        integer(status),
        # 客户端在 1010 响应中用 w.b(5) 读取动作码，必须是 short。
        short(action),
    ])


# 1126 subtype=1 (local-compat extension) sets the facing of an existing generic
# map actor (pmsj.work.b/n) in place.  The client looks the actor up by id in the
# same container that 1126 subtype=0 used (b/m.u), then calls b/n.q(direction) and
# b/n.I().  Facing values match the APK's b/n.n byte (four cardinal directions).
NPC_DIRECTION_DOWN = 0
NPC_DIRECTION_RIGHT = 1
NPC_DIRECTION_UP = 2
NPC_DIRECTION_LEFT = 3

_DIRECTION_RANGE = (NPC_DIRECTION_DOWN, NPC_DIRECTION_RIGHT, NPC_DIRECTION_UP, NPC_DIRECTION_LEFT)
NPC_STREAM_RADIUS = 20
SECT_MENTOR_LEARN_OPTION = 1

# 1005 path directions are produced by APK a/c/x.a(x1, y1, x2, y2).
_MAP_PATH_DELTAS = {
    0: (0, 1),
    1: (-1, 1),
    2: (-1, 0),
    3: (-1, -1),
    4: (0, -1),
    5: (1, -1),
    6: (1, 0),
    7: (1, 1),
    8: (0, 0),
}


def map_movement_final_tile(values: list[object]) -> tuple[int, int]:
    """Decode the final tile from the APK's compact 1005 movement path."""
    if len(values) < 2:
        raise ValueError('map movement requires a starting tile')
    x, y = int(values[0]), int(values[1])
    step_count = min(max(0, int(values[2])) if len(values) > 2 else 0, max(0, len(values) - 3))
    for raw_direction in values[3:3 + step_count]:
        direction = int(raw_direction)
        try:
            dx, dy = _MAP_PATH_DELTAS[direction]
        except KeyError as exc:
            raise ValueError(f'unsupported map movement direction {direction}') from exc
        x += dx
        y += dy
    return x, y


def update_role_position(
    role: dict[str, object],
    x: int,
    y: int,
) -> bool:
    """Update the role's in-memory map tile.

    Returns True only when the saved tile actually changed.
    Persistence is intentionally handled by the connection lifecycle so
    normal movement does not write roles.json for every 1005 packet.
    """
    new_x = int(x)
    new_y = int(y)

    old_x = int(role.get('map_x', new_x))
    old_y = int(role.get('map_y', new_y))

    if old_x == new_x and old_y == new_y:
        return False

    role['map_x'] = new_x
    role['map_y'] = new_y
    return True


def map_actor_direction_frame(object_id: int, direction: int) -> bytes:
    """Return a 1126 subtype=1 frame setting one actor's facing in place.

    Strict wire format: [byte(1), byte(1), integer(object_id), byte(direction)].
    The client never moves, recreates, or renames the actor -- it only calls
    b/n.q(direction) then b/n.I() on the existing entity.
    """
    if direction not in _DIRECTION_RANGE:
        raise ValueError(f'NPC direction must be 0..3, got {direction}')
    return encode_frame(1126, [
        byte(1),
        byte(1),
        integer(int(object_id)),
        byte(direction),
    ])


def map_actor_selection_frame(object_id: int) -> bytes:
    """Select one generic actor through the local APK compatibility branch.

    The patched client resolves the id in the same generic actor container used
    by subtype=0 and assigns it as the current target. The original entity
    renderer then draws its bundled 0x203230 selection ring beneath the actor.
    """
    return encode_frame(1126, [
        byte(2),
        integer(int(object_id)),
    ])


def map_actor_directions_frame(items: list[tuple[int, int]]) -> bytes:
    """Batch form of map_actor_direction_frame.

    Wire format: [byte(1), byte(count), integer(id1), byte(dir1), ...].
    """
    if not items:
        raise ValueError('direction frame requires at least one actor')
    encoded = [byte(1), byte(len(items))]
    for object_id, direction in items:
        if direction not in _DIRECTION_RANGE:
            raise ValueError(f'NPC direction must be 0..3, got {direction}')
        encoded.append(integer(int(object_id)))
        encoded.append(byte(direction))
    return encode_frame(1126, encoded)


def map_monster_frame(definition: MapDefinition) -> bytes:
    """Return the verified 1126 actor-spawn frame for the local monster.

    ``pmsj.work.main.e.Q`` decodes subtype 0 as a list of generic map actors:
    field 0 is the subtype, field 1 the count, then each record contains
    id/x/y/raw-model/name.  The client adds 0x200b20 to raw-model before
    loading the sprite resource.
    """
    monster = definition.monster
    if monster is None:
        raise ValueError(f'map {definition.id} has no monster')
    return encode_frame(1126, [
        byte(0),
        byte(1),
        integer(monster.id),
        integer(monster.x),
        integer(monster.y),
        integer(monster.model),
        string(monster.name),
    ])


def map_portal_frame(portal: PortalDefinition) -> bytes:
    """Return the verified 1126 generic-actor shape for the test portal."""
    return encode_frame(1126, [
        byte(0),
        byte(1),
        integer(portal.id),
        integer(portal.x),
        integer(portal.y),
        # Reuse the known-good local actor sprite.  The important part of the
        # portal is its actor id/position; no new client resource is required.
        integer(portal.model),
        string(portal.name),
    ])


def map_portal_frames(definition: MapDefinition) -> list[bytes]:
    """Spawn every portal registered for one map, in configuration order."""
    return [map_portal_frame(portal) for portal in definition.portals]


def map_return_portal_frame(definition: MapDefinition) -> bytes:
    """Compatibility helper for the first portal on a return map."""
    try:
        portal = definition.portals[0]
    except IndexError as exc:
        raise ValueError(f'map {definition.id} has no return portal') from exc
    return map_portal_frame(portal)


def map_npc_frame(definition: MapDefinition, npc: MapActorDefinition) -> bytes:
    """Spawn one map-58 NPC through the client's native 2030 NPC path.

    ``main/e.X`` constructs ``pmsj.work.b/t`` from this record.  Unlike the
    generic 1126 actor, that class participates in the map's built-in target
    selection, draws the bundled selection ring, and supplies the portrait and
    title used by the native NPC dialogue overlay.
    """
    return encode_frame(2030, [
        integer(npc.id),
        integer(npc.x),
        integer(npc.y),
        integer(npc.dat_id),
        integer(npc.direction),
        integer(0),
        string(npc.name),
        integer(0),
        string(npc.label),
    ])


def map_npc_frames(definition: MapDefinition) -> list[bytes]:
    """Return native NPC spawn frames for the current map definition."""
    return [map_npc_frame(definition, npc) for npc in definition.npcs]


def map_npcs_near(definition: MapDefinition, x: int, y: int) -> list[MapActorDefinition]:
    """Return NPCs retained by the client's native 20-tile stream window."""
    return [
        npc for npc in definition.npcs
        if abs(npc.x - int(x)) <= NPC_STREAM_RADIUS
        and abs(npc.y - int(y)) <= NPC_STREAM_RADIUS
    ]


def map_npc_for_object_id(
    definition: MapDefinition,
    object_id: int,
) -> MapActorDefinition | None:
    """Return the current map's NPC matching a clicked actor id."""
    return next(
        (npc for npc in definition.npcs if npc.id == int(object_id)),
        None,
    )


def map_npc_dialogue_frames(
    npc: MapActorDefinition,
    role: dict[str, object] | None = None,
) -> list[bytes]:
    """Open the compact map-overlay NPC dialogue used by the original client.

    Protocol 2032 opens screen 6 (``pmsj.work.e.cb`` / ``6.ui``).  Its records
    are eight fields wide: type 1 supplies the wrapped introduction text, type
    2 supplies an option row, and type 100 finalizes layout after resolving the
    native 2030 NPC by id for its title and portrait.
    """
    npc_id = npc.id
    is_sect_mentor = npc.service == 'sect_skill_mentor' and npc.sect_id is not None
    sect_matches = (
        is_sect_mentor
        and role is not None
        and normalized_sect_id(role) == npc.sect_id
    )
    if is_sect_mentor and not sect_matches:
        introduction = f'仅限{SECTS.get(npc.sect_id, "本门")}弟子学习。'
    else:
        introduction = npc.introduction or npc.label or npc.name

    def dialogue_record(kind: int, *, option_id: int = 0, text: str = '', icon: int = 0) -> list[Field]:
        return [
            integer(0),
            integer(0),
            integer(0),
            short(0),
            integer(option_id),
            byte(kind),
            string(text),
            integer(icon),
        ]

    records = [*dialogue_record(1, text=introduction)]
    if sect_matches:
        records.extend(dialogue_record(
            2,
            option_id=SECT_MENTOR_LEARN_OPTION,
            text='学习门派技能',
        ))
    records.extend(dialogue_record(2, option_id=0, text='结束对话'))
    records.extend(dialogue_record(100))
    return [encode_frame(2032, [
        integer(npc_id),
        byte(len(records) // 8),
        *records,
    ])]


def sect_skill_screen_frame(mode: int = 1) -> bytes:
    """Open external screen 179, remapped by the APK to sect screen 602.

    ``main/e`` dispatches the generic UI action from short field 5, reads the
    external screen id from integer field 4 and the mode from integer field 3.
    It maps external id 0xb3 to 0x25a; mode 1 is the mentor learning variant
    rather than the remote view variant.
    """
    return encode_frame(1010, [
        integer(0),
        short(0),
        short(0),
        integer(mode),
        integer(179),
        short(69),
    ])


def map_object_remove_frame(object_id: int) -> bytes:
    """Remove a generic 1126 actor via verified ``1010/action=18``.

    ``main/e`` dispatches protocol 1010 using short field 5. Action 18 reads
    the actor id from integer field 0 and removes ids >= 1_000_000 from the
    generic-actor container. It is not a standalone protocol number 18.
    """
    return encode_frame(1010, [
        integer(object_id),
        short(0),
        short(0),
        integer(0),
        integer(0),
        short(18),
    ])


def map_object_interaction_ack_frame(object_id: int) -> bytes:
    """Release the APK wait overlay after suppressing a 1010/action=7 re-tap.

    The inbound 1010 dispatcher clears its wait flags before checking action
    field 5. Action 7 has no inbound map mutation branch, so this complete
    six-field record acknowledges the interaction without moving or removing
    the actor.
    """
    return encode_frame(1010, [
        integer(object_id),
        short(0),
        short(0),
        integer(0),
        integer(0),
        short(7),
    ])


def npc_dialogue_option_frames(
    settings: Settings,
    role: dict[str, object] | None,
    state: LocalNpcDialogueState,
    option_id: int,
) -> list[bytes]:
    """Acknowledge one 2032 option and open mentor mode only if still valid."""
    frames = [map_object_interaction_ack_frame(0)]
    try:
        if role is None or int(option_id) != SECT_MENTOR_LEARN_OPTION:
            return frames
        try:
            definition = settings_for_role(settings, role)
        except ValueError:
            return frames
        if state.map_id != definition.id or state.npc_id is None:
            return frames
        npc = map_npc_for_object_id(definition, state.npc_id)
        if (
            npc is None
            or npc.service != 'sect_skill_mentor'
            or npc.sect_id is None
            or normalized_sect_id(role) != npc.sect_id
        ):
            return frames
        frames.append(sect_skill_screen_frame(1))
        return frames
    finally:
        state.clear()


def map_object_interaction_values(values: list[object]) -> tuple[int, int | None, int | None, int | None]:
    """Decode the active APK's 2031 map-object request.

    ``main/e.a(IISS)`` writes ``[object_id, 0, x, y, action, 0]``.  Keep
    the optional fields tolerant because older builds omit the trailing
    values when an actor has no interaction metadata.
    """
    if not values:
        raise ValueError('map object interaction requires an object id')
    object_id = int(values[0])
    object_x = int(values[2]) if len(values) > 2 else None
    object_y = int(values[3]) if len(values) > 3 else None
    action = int(values[4]) if len(values) > 4 else None
    return object_id, object_x, object_y, action


def battle_reset_frame() -> bytes:
    """Return the APK-verified 1040 action=0 battle reset frame.

    Action 0 is parsed by the client as the battle-state reset/open path.  It
    removes stale map/battle state and creates screen 20, which must precede
    the action=1 first-round payload on a fresh map session.
    """
    return encode_frame(1040, [byte(0)])


def battle_start_frame(role: dict[str, object], settings: Settings) -> bytes:
    """Build the APK-confirmed 1040/action=1 battle-state frame.

    ``main/e`` reads the following fixed types for action 1:
    byte(action), int(round), byte(reserved), int(timer), short(menu-state),
    string(reserved), short(target-state), string(reserved), byte(ready).
    The two strings and the reserved byte are intentionally empty/zero because
    the client parser only consumes them in this action; no server semantics
    are inferred from their names.
    """
    return encode_frame(1040, [
        byte(1),
        integer(1),
        byte(0),
        integer(30),
        short(0),
        string(''),
        short(0),
        string(''),
        byte(1),
    ])


def battle_actor_source_model_for_debug(
    model: int,
    kind: int,
    model_is_battle_base: bool = False,
) -> int:
    """Read-only copy of the 1048 source_model formula for diagnostic logs.

    The encoder in ``battle_actor_frame`` keeps its own identical expression
    and does not call this helper.  Do not use this return value to decide
    protocol output.
    """
    return model if model_is_battle_base else (model * 10 if kind == 1 else model - 1)


def battle_actor_debug_snapshot(
    *,
    actor_id: int,
    model: int,
    name: str,
    kind: int,
    side_code: int,
    slot: int = 1,
    model_is_battle_base: bool = False,
    appearance: dict[int, int] | None = None,
    fields: list | None = None,
    trace_id: str = '',
) -> dict[str, object]:
    """Return a read-only 1048 diagnostic snapshot.  Not used for encoding."""
    visible_layers = dict(appearance or {})
    return {
        'trace_id': trace_id,
        'actor_id': actor_id,
        'name': name,
        'role_model': model,
        'kind': kind,
        'side': side_code,
        'slot': slot,
        'appearance_preset': model if kind == 1 else 0,
        'model_is_battle_base': model_is_battle_base,
        'source_model': battle_actor_source_model_for_debug(model, kind, model_is_battle_base),
        'appearance': visible_layers,
        'visible_layers': visible_layers,
        'fields': field_debug_entries(fields or ()),
    }


def format_battle_actor_1048_log(snapshot: dict[str, object]) -> str:
    """Format a PLAYER or MONSTER 1048 diagnostic block."""
    kind = int(snapshot['kind'])
    fields = snapshot.get('fields') or []
    field_lines = []
    if isinstance(fields, list):
        for entry in fields:
            if not isinstance(entry, dict):
                continue
            field_lines.append(
                f"  {{index: {entry['index']}, type: {entry['type']}, value: {entry['value']!r}}}"
            )
    fields_text = '[\n' + ',\n'.join(field_lines) + '\n]' if field_lines else '[]'
    trace = str(snapshot.get('trace_id') or '')
    trace_line = f"battle_trace={trace}\n" if trace else ''
    if kind == 1:
        return (
            "BATTLE_ACTOR_1048 PLAYER\n"
            f"{trace_line}"
            f"role_id={snapshot['actor_id']}\n"
            f"role_model={snapshot['role_model']}\n"
            f"source_model={snapshot['source_model']}\n"
            f"side={snapshot['side']}\n"
            f"kind={snapshot['kind']}\n"
            f"slot={snapshot['slot']}\n"
            f"appearance_preset={snapshot.get('appearance_preset', snapshot['role_model'])}\n"
            f"model_is_battle_base={snapshot['model_is_battle_base']}\n"
            f"appearance={snapshot['appearance']}\n"
            f"visible_layers={snapshot['visible_layers']}\n"
            f"fields={fields_text}"
        )
    return (
        "BATTLE_ACTOR_1048 MONSTER\n"
        f"{trace_line}"
        f"entity_id={snapshot['actor_id']}\n"
        f"model={snapshot['role_model']}\n"
        f"source_model={snapshot['source_model']}\n"
        f"kind={snapshot['kind']}\n"
        f"side={snapshot['side']}\n"
        f"slot={snapshot['slot']}\n"
        f"fields={fields_text}"
    )


def battle_actor_frame(
    *,
    actor_id: int,
    model: int,
    name: str,
    kind: int,
    side_code: int,
    slot: int = 1,
    model_is_battle_base: bool = False,
    appearance: dict[int, int] | None = None,
    current_hp: int = 100,
    max_hp: int = 100,
    trace_id: str = '',
) -> bytes:
    """Build the APK's 1048 actor record used to populate battle slots.

    ``main/e.af`` constructs ``work/b/h`` from field 7 (kind), field 9 (id),
    field 2/0 (model source), field 5 (side/category), and field 8 (battle
    station).  Field 21 is the face/body appearance preset: kind=1 reads it as
    the constructor's fourth argument and ``h.r()`` applies ``y(f(21))`` /
    ``M(f(21))``.  The remaining numeric fields are the zero/default stat
    block; keeping them present is important because the renderer reads the
    sparse record by index.
    """
    # kind=2: APK e.af does field[0]+1. Keep signed model-1 so negative
    # map models such as -2004250 round-trip; do not clamp to 0.
    source_model = model if model_is_battle_base else (model * 10 if kind == 1 else model - 1)
    visible_layers = appearance or {}
    # kind=1: APK h.r() uses Vector[21] as the same selector map v.r() reads
    # from property 6.  Monsters keep the previous zero unless a caller
    # supplies appearance 21.
    appearance_preset = int(model) if kind == 1 else int(visible_layers.get(21, 0))
    fields: list[Field] = [
        integer(source_model),  # 0: flags/model source
        integer(0),              # 1
        integer(source_model if kind == 1 else 0),  # 2: player model source
        integer(max(0, current_hp)),  # 3: current hp/status (used by h.d())
        integer(0),              # 4
        integer(side_code),      # 5: side/category
        string(name),            # 6: battle name
        short(kind),              # 7: actor kind
        integer(slot),            # 8: one-based battle station
        integer(actor_id),        # 9: actor id
        integer(max(0, current_hp)),  # 10: current hp
        integer(max(1, max_hp)),      # 11: max hp
        integer(100),             # 12: current mp
        integer(100),             # 13: max mp/status
        integer(int(visible_layers.get(14, 0))),  # 14: trousers layer
        short(int(visible_layers.get(15, 0))),     # 15: armour/base layer
        integer(int(visible_layers.get(16, 0))),   # 16: shoulder layer
        integer(int(visible_layers.get(17, 0))),   # 17: wrist layer
        integer(int(visible_layers.get(18, 0))),   # 18: boot layer
        integer(int(visible_layers.get(19, 0))),   # 19: cape layer
        integer(int(visible_layers.get(20, 0))),   # 20: helmet layer
        # kind=1: short face/body selector.  e.af reads w.b(21) into h.<init>
        # p4; h.r() then calls y(f(21)) and M(f(21)).  Not a battle station.
        short(appearance_preset),
    ]
    LOG.info(
        '%s',
        format_battle_actor_1048_log(
            battle_actor_debug_snapshot(
                actor_id=actor_id,
                model=model,
                name=name,
                kind=kind,
                side_code=side_code,
                slot=slot,
                model_is_battle_base=model_is_battle_base,
                appearance=dict(visible_layers),
                fields=fields,
                trace_id=trace_id,
            )
        ),
    )
    return encode_frame(1048, fields)


def battle_actor_frames(
    role: dict[str, object],
    settings: Settings | MapDefinition,
    trace_id: str = '',
    state: LocalBattleState | None = None,
) -> list[bytes]:
    """Return one player and one monster record for the local battle probe."""
    if isinstance(settings, MapDefinition):
        monster = settings.monster
        if monster is None:
            raise ValueError(f'map {settings.id} has no battle monster')
        default_role_model = 2000
        default_role_name = '本地侠客'
    else:
        monster = MapActorDefinition(
            id=int(settings.monster_id),
            name=str(settings.monster_name),
            model=int(settings.monster_model),
            x=int(settings.monster_x),
            y=int(settings.monster_y),
            direction=int(settings.monster_direction),
        )
        default_role_model = settings.role_model
        default_role_name = settings.role_name
    return [
        battle_actor_frame(
            actor_id=int(role['id']),
            model=int(role.get('model', default_role_model)),
            name=str(role.get('name', default_role_name)),
            kind=1,
            # main/b.h.e() treats the local fighter's side as grid 0. Side 3
            # is a special non-grid list and cannot be resolved by normal
            # attack actions, so the player must use the ordinary side 2.
            side_code=2,
            slot=1,
            appearance=character_appearance(role, getattr(settings, 'item_registry', None)),
            current_hp=state.player_hp if state is not None else 100,
            max_hp=state.player_max_hp if state is not None else 100,
            trace_id=trace_id,
        ),
        battle_actor_frame(
            actor_id=monster.id,
            model=monster.model,
            name=monster.name,
            kind=2,
            side_code=1,
            slot=1,
            current_hp=state.monster_hp if state is not None else 100,
            max_hp=state.monster_max_hp if state is not None else 100,
            trace_id=trace_id,
        ),
    ]


def battle_actor_update_frame(
    role: dict[str, object],
    settings: Settings,
    state: LocalBattleState,
    actor_id: int,
) -> bytes:
    """Re-send one 1048 record with the actor's current HP.

    The 1042 action packet drives animation and damage numbers, but the APK's
    visible life bar is read from actor field 3 (and the current/max stat pair
    at fields 10/11).  A small 1048 state refresh keeps those values in sync.
    """
    if actor_id == state.player_id:
        return battle_actor_frame(
            actor_id=state.player_id,
            model=int(role.get('model', settings.role_model)),
            name=str(role.get('name', settings.role_name)),
            kind=1,
            side_code=2,
            slot=1,
            appearance=character_appearance(role, getattr(settings, 'item_registry', None)),
            current_hp=state.player_hp,
            max_hp=state.player_max_hp,
            trace_id=state.trace_id,
        )
    return battle_actor_frame(
        actor_id=state.monster_id,
        model=int(settings.monster_model),
        name=str(settings.monster_name),
        kind=2,
        side_code=1,
        slot=1,
        current_hp=state.monster_hp,
        max_hp=state.monster_max_hp,
        trace_id=state.trace_id,
    )


def _battle_role_resource_candidates(model_id: int) -> list[tuple[str, int, Path]]:
    project_dir = Path(__file__).resolve().parent
    role_dirs = (
        project_dir / 'data' / 'role',
        project_dir / 'build' / 'weapon-apk-extracted' / 'assets' / 'res' / 'role',
    )
    alias = BATTLE_RESOURCE_ALIASES.get(model_id)
    mapped = model_id + BATTLE_RESOURCE_MODEL_OFFSET
    ids: list[tuple[str, int]] = [('direct', model_id)]
    if alias is not None:
        ids.append(('alias', alias))
    if mapped != model_id:
        ids.append(('offset', mapped))
    return [
        (branch, resolved_id, role_dir / f'{resolved_id}.dat')
        for branch, resolved_id in ids
        for role_dir in role_dirs
    ]


def battle_resource_resolution(model_id: int) -> dict[str, object]:
    """Describe which 1502 action=1 lookup branch would be used.

    Read-only: this function does not encode 1503 and is not consulted by
    ``battle_resource_path`` when building a response.
    """
    alias = BATTLE_RESOURCE_ALIASES.get(model_id)
    mapped = model_id + BATTLE_RESOURCE_MODEL_OFFSET
    for branch, resolved_id, path in _battle_role_resource_candidates(model_id):
        if path.is_file():
            return {
                'requested_id': model_id,
                'alias': alias,
                'offset_id': mapped if mapped != model_id else None,
                'branch': branch,
                'resolved_id': resolved_id,
                'resolved_path': str(path),
                'empty': False,
                'missing': False,
            }
    empty = model_id in BATTLE_EMPTY_RESOURCE_IDS
    return {
        'requested_id': model_id,
        'alias': alias,
        'offset_id': mapped if mapped != model_id else None,
        'branch': 'empty' if empty else 'missing',
        'resolved_id': None,
        'resolved_path': None,
        'empty': empty,
        'missing': not empty,
    }


def format_battle_resource_query_log(
    *,
    username: str,
    query_action: int,
    resource_ids: list[int],
    battle_active: bool,
    round_number: int,
    trace_id: str,
    resource_id: int,
    resolution: dict[str, object],
    response_type: int | None,
    chunks: int,
) -> str:
    """Format the BATTLE_RESOURCE_QUERY diagnostic block."""
    trace = f"battle_trace={trace_id}\n" if trace_id else ''
    return (
        "BATTLE_RESOURCE_QUERY\n"
        f"{trace}"
        f"user={username!r}\n"
        f"action={query_action}\n"
        f"ids={resource_ids}\n"
        f"battle_active={battle_active}\n"
        f"round={round_number}\n"
        f"resource_id={resource_id}\n"
        f"alias={resolution.get('alias')!r}\n"
        f"branch={resolution.get('branch')!r}\n"
        f"offset_id={resolution.get('offset_id')!r}\n"
        f"jar_fallback={resolution.get('jar_fallback', False)}\n"
        f"resolved_id={resolution.get('resolved_id')!r}\n"
        f"resolved_path={resolution.get('resolved_path')!r}\n"
        f"response_type={response_type}\n"
        f"chunks={chunks}"
    )


def battle_resource_path(model_id: int) -> Path | None:
    """Resolve a logical model to a local override or bundled APK role .dat."""
    for _branch, _resolved_id, candidate in _battle_role_resource_candidates(model_id):
        if candidate.is_file():
            return candidate
    return None


def battle_resource_frames(model_id: int) -> list[bytes]:
    """Return the two 1503 chunks expected by ``main/e.ao`` for a .dat query."""
    path = battle_resource_path(model_id)
    if path is None:
        if model_id in BATTLE_EMPTY_RESOURCE_IDS:
            LOG.info('battle resource empty model=%d', model_id)
            empty = [integer(model_id), short(0), short(0), binary(b'')]
            return [
                encode_frame(1503, [byte(0), *empty]),
                encode_frame(1503, [byte(2), *empty]),
            ]
        LOG.warning('battle resource missing model=%d', model_id)
        return []
    data = path.read_bytes()
    if len(data) > 0xFFFF:
        LOG.warning('battle resource too large model=%d bytes=%d', model_id, len(data))
        return []
    # status 0 allocates and copies the first chunk.  The APK's status-2
    # handler also appends its declared chunk before finalising the cache;
    # repeating ``data`` there would overflow the client's fixed buffer.
    fields = [integer(model_id), short(len(data)), short(len(data)), binary(data)]
    finish_fields = [integer(model_id), short(len(data)), short(0), binary(b'')]
    return [
        encode_frame(1503, [byte(0), *fields]),
        encode_frame(1503, [byte(2), *finish_fields]),
    ]


def _signed_int32(value: int) -> int:
    """Return an unsigned APK integer in Java's signed-int representation."""
    value &= 0xFFFFFFFF
    return value - 0x100000000 if value >= 0x80000000 else value


def battle_image_resource(image_id: int) -> tuple[int, int, int, int, int, int, int, int, int, bytes] | None:
    """Read one proprietary image record from the APK/JAR image sets.

    The client reconstructs a regular indexed PNG from the RGB565 palette and
    the stored IDAT bytes. Some role layers request a direction/variant id 100
    above the base atlas id; the bundled index only stores that base id. The
    APK is a thin client and omits some player images which remain available
    in the original client JAR, so that extracted set is used as a fallback.
    """
    build_dir = Path(__file__).resolve().parent / 'build'
    image_dirs = (
        build_dir / 'weapon-apk-extracted' / 'assets' / 'res' / 'images',
        build_dir / 'jar-images' / 'res' / 'images',
    )

    source_id = image_id
    image_dir: Path | None = None
    record: tuple[int, int] | None = None
    # Prefer an exact id from either resource set before trying the directional
    # id alias. This prevents an APK alias from masking an exact JAR resource.
    for candidate_id in (image_id, image_id - 100):
        if candidate_id < 0:
            continue
        for candidate_dir in image_dirs:
            index_path = candidate_dir / 'images.o'
            if not index_path.is_file():
                continue
            index = index_path.read_bytes()
            if len(index) < 2:
                continue
            index_size = struct.unpack_from('>H', index, 0)[0]
            records = index[2:2 + index_size]
            for offset in range(0, len(records) - 6, 7):
                record_id, container_number, data_offset = struct.unpack_from('>IBH', records, offset)
                if record_id != candidate_id:
                    continue
                container_path = candidate_dir / f'png{container_number}.p'
                if not container_path.is_file():
                    continue
                source_id = candidate_id
                image_dir = candidate_dir
                record = (container_number, data_offset)
                break
            if record is not None:
                break
        if record is not None:
            break
    if record is None or image_dir is None:
        return None

    container_number, data_offset = record
    container_path = image_dir / f'png{container_number}.p'
    if not container_path.is_file():
        # The original JAR index contains a few combat-effect records that
        # reuse container numbers shipped by the APK.  Keep the JAR index
        # metadata (including the correct record offset), but transparently
        # source the matching container from the APK when the JAR omitted it.
        for candidate_dir in image_dirs:
            candidate_path = candidate_dir / f'png{container_number}.p'
            if candidate_path.is_file():
                container_path = candidate_path
                break
        else:
            return None
    container = container_path.read_bytes()
    if data_offset + 24 > len(container):
        return None

    position = data_offset
    group_count, group_index = container[position], container[position + 1]
    position += 2
    if group_count:
        position += (group_count - group_index - 1) * 2
    if position + 22 > len(container):
        return None
    (
        width,
        height,
        bit_depth,
        transparent_index,
        palette_crc,
        transparency_crc,
        header_crc,
        palette_length,
        idat_length,
    ) = struct.unpack_from('>HHBBIIIHH', container, position)
    position += 22

    if group_count:
        position += group_index * palette_length
        palette = container[position:position + palette_length]
        position += palette_length
        position += (group_count - group_index - 1) * palette_length
    else:
        palette = container[position:position + palette_length]
        position += palette_length
    idat = container[position:position + idat_length]
    if len(palette) != palette_length or len(idat) != idat_length:
        return None

    if source_id != image_id:
        LOG.info('battle image alias requested=%d source=%d', image_id, source_id)
    if 'jar-images' in image_dir.parts:
        LOG.info('battle image JAR fallback image=%d source=%d', image_id, source_id)
    return (
        width,
        height,
        bit_depth,
        transparent_index,
        palette_crc,
        transparency_crc,
        header_crc,
        palette_length,
        idat_length,
        palette + idat,
    )


def battle_image_resolve_debug(image_id: int) -> dict[str, object]:
    """Describe which 1502 action=0/2 image lookup branch would be used.

    Read-only locate of the images.o record.  It does not encode 1501/1502
    and is not used by ``battle_image_resource`` to choose a payload.
    """
    build_dir = Path(__file__).resolve().parent / 'build'
    image_dirs = (
        build_dir / 'weapon-apk-extracted' / 'assets' / 'res' / 'images',
        build_dir / 'jar-images' / 'res' / 'images',
    )
    for candidate_id in (image_id, image_id - 100):
        if candidate_id < 0:
            continue
        for candidate_dir in image_dirs:
            index_path = candidate_dir / 'images.o'
            if not index_path.is_file():
                continue
            index = index_path.read_bytes()
            if len(index) < 2:
                continue
            index_size = struct.unpack_from('>H', index, 0)[0]
            records = index[2:2 + index_size]
            for offset in range(0, len(records) - 6, 7):
                record_id, container_number, _data_offset = struct.unpack_from('>IBH', records, offset)
                if record_id != candidate_id:
                    continue
                container_path = candidate_dir / f'png{container_number}.p'
                if not container_path.is_file():
                    continue
                jar_fallback = 'jar-images' in candidate_dir.parts
                aliased = candidate_id != image_id
                if aliased and jar_fallback:
                    branch = 'alias_jar'
                elif aliased:
                    branch = 'alias'
                elif jar_fallback:
                    branch = 'jar_fallback'
                else:
                    branch = 'direct'
                return {
                    'requested_id': image_id,
                    'alias': candidate_id if aliased else None,
                    'resolved_id': candidate_id,
                    'resolved_path': str(container_path),
                    'branch': branch,
                    'jar_fallback': jar_fallback,
                    'missing': False,
                }
    return {
        'requested_id': image_id,
        'alias': None,
        'resolved_id': None,
        'resolved_path': None,
        'branch': 'missing',
        'jar_fallback': False,
        'missing': True,
    }


def battle_image_frames(query_action: int, image_id: int) -> list[bytes]:
    """Return 1501 image chunks followed by the client's 1502 redraw signal."""
    resource = battle_image_resource(image_id)
    if resource is None:
        LOG.warning('battle image resource missing image=%d action=%d', image_id, query_action)
        return []
    (
        width,
        height,
        bit_depth,
        transparent_index,
        palette_crc,
        transparency_crc,
        header_crc,
        palette_length,
        idat_length,
        data,
    ) = resource

    # Action 2 originates from a/a/a's role-image cache. main/e.ap selects
    # that cache with response field 0 == 1; batched action 0 uses cache 0.
    cache_selector = 1 if query_action == PNG_QUERY_ROLE_CACHE else 0
    if palette_length + idat_length != len(data) or len(data) > 0xFFFF:
        LOG.warning('battle image resource invalid image=%d bytes=%d', image_id, len(data))
        return []

    def frame(status: int, chunk: bytes) -> bytes:
        return encode_frame(1501, [
            integer(cache_selector),
            integer(len(data)),
            byte(0),
            byte(status),
            integer(image_id),
            short(width),
            short(height),
            byte(bit_depth),
            byte(transparent_index),
            short(palette_length),
            short(idat_length),
            integer(_signed_int32(palette_crc)),
            integer(_signed_int32(transparency_crc)),
            integer(_signed_int32(header_crc)),
            short(len(chunk)),
            binary(chunk),
        ])

    # As with 1503, status 0 allocates and copies the complete payload while
    # status 2 finalises with an empty chunk, avoiding a client buffer overflow.
    # main/e.ap stores action-2 resources in the role cache without invalidating
    # the current canvas. Server protocol 1502 is the separate processPngQuery
    # completion signal which forces the map/battle scene to redraw.
    return [frame(0, data), frame(2, b''), encode_frame(1502)]


def battle_action_frame(
    state: LocalBattleState,
    round_number: int | None = None,
    *,
    actor_id: int | None = None,
    target_id: int | None = None,
    damage: int = 10,
    label: str = '普通攻击',
) -> bytes:
    """Queue one native APK basic attack, including its damage effect.

    The decompiled ``pmsj.work.main.b`` controller identifies action type 1
    as ``ACTION_ATTACK``. It moves the sender to ``target.g()``, waits for
    arrival, switches to the attack pose, applies the embedded BattleEffect,
    and only then queues the sender's return movement. Effect type 22 calls
    ``target.a(delta, flags)`` and updates HP immediately.

    Types 7 and 8 are summon/call-back actions. Using type 8 as an attack was
    the reason HP changed after the return animation and could strand actors.
    """
    sender_id = state.player_id if actor_id is None else actor_id
    victim_id = state.monster_id if target_id is None else target_id
    return encode_frame(1042, [
        integer(state.round if round_number is None else round_number),
        integer(sender_id),
        integer(victim_id),
        byte(1),                 # ACTION_ATTACK
        byte(1),                 # one hit
        byte(0),
        integer(0),              # sender visual effect id
        integer(0),              # target visual effect id
        string(label),
        integer(1),              # BattleEffect count
        integer(victim_id),      # effect target
        integer(0),              # normal hit reaction and damage number
        integer(22),             # HP delta effect
        integer(-max(1, damage)),
        string(''),
    ])


def battle_defend_frame(
    state: LocalBattleState,
    round_number: int | None = None,
) -> bytes:
    """Queue the native defence action without applying an HP effect."""
    return encode_frame(1042, [
        integer(state.round if round_number is None else round_number),
        integer(state.player_id),
        integer(state.player_id),
        byte(2),                 # ACTION_DEFEND
        byte(1),
        byte(0),
        integer(0),
        integer(0),
        string('防御'),
        integer(0),              # no BattleEffect
    ])


def battle_round_action_frames(
    state: LocalBattleState,
    command_code: int,
    round_number: int | None = None,
) -> tuple[list[bytes], bool]:
    """Resolve one supported player command and keep wire HP effects in sync."""
    action_round = state.round if round_number is None else round_number
    if command_code == 1:
        player_damage = state.player_basic_attack_damage()
        monster_defeated = state.apply_basic_attack(player_damage)
        frames = [battle_action_frame(state, action_round, damage=player_damage)]
    elif command_code == 2:
        monster_defeated = False
        frames = [battle_defend_frame(state, action_round)]
    else:
        return [], False

    if not monster_defeated:
        monster_damage = state.monster_basic_attack_damage(defending=command_code == 2)
        state.player_hp = max(0, state.player_hp - monster_damage)
        frames.append(battle_action_frame(
            state,
            action_round,
            actor_id=state.monster_id,
            target_id=state.player_id,
            damage=monster_damage,
            label='妖兽攻击',
        ))
    return frames, monster_defeated


def battle_move_frame(
    state: LocalBattleState,
    round_number: int | None = None,
    *,
    actor_id: int | None = None,
    target_id: int | None = None,
) -> bytes:
    """Build a raw effect-free ACTION_ATTACK record for diagnostics.

    Gameplay uses :func:`battle_action_frame`; this record approaches and
    returns but intentionally performs no damage.
    """
    return encode_frame(1042, [
        integer(state.round if round_number is None else round_number),
        integer(state.player_id if actor_id is None else actor_id),
        integer(state.monster_id if target_id is None else target_id),
        byte(1),
        byte(0),
        byte(0),
        integer(0),
        integer(0),
        string(''),
        integer(0),
    ])


def battle_action_show_frame(state: LocalBattleState, round_number: int | None = None) -> bytes:
    """Advance the APK battle UI (1040/action=2) for a specific round.

    The client sends its completion acknowledgement only after it has
    finished the action animation.  The server may already have advanced its
    internal HP/turn state by then, so the frame must carry the round that the
    client just executed rather than blindly using the post-action counter.
    """
    shown_round = state.round if round_number is None else round_number
    return encode_frame(1040, [
        byte(2),
        integer(shown_round),
        byte(0),
        integer(0),
        short(0),
        string(''),
        short(0),
        string(''),
        byte(1),
    ])


def battle_escape_frame(player_id: int) -> bytes:
    """Start the APK's dedicated smooth escape-and-close transition.

    S->C 1041/10 calls ``pmsj.work.e.j.escapeStart()``. The client moves the
    local fighter to its off-screen escape point over 1300 ms, blocks further
    battle input during that movement, and closes the battle as soon as the
    fighter reports ``escapeDone()``.
    """
    return encode_frame(1041, [integer(10), integer(player_id)])


def battle_escape_request_frames(
    state: LocalBattleState,
    round_number: int | None = None,
) -> list[bytes]:
    """Settle escape once and immediately start the client's native transition."""
    del round_number  # Escape protocol 1041 has no round field.
    player_id = state.player_id
    if not state.escape():
        return []
    return [battle_escape_frame(player_id)]


def battle_end_frame() -> bytes:
    """End the local battle through the APK's verified action=4 branch."""
    return encode_frame(1040, [byte(4)])


def map_data_frames(definition: MapDefinition, role_id: int | None = None) -> list[bytes]:
    configured = Path(definition.map_o_file)
    map_path = configured if configured.is_absolute() else Path(__file__).resolve().parent / configured
    try:
        generated = MapO.from_file(map_path.read_bytes())
    except (OSError, MapOError) as exc:
        LOG.warning('cannot load generated map %s; using flat fallback: %s', map_path, exc)
        width = definition.fallback_width
        height = definition.fallback_height
        generated = MapO(
            width=width,
            height=height,
            map_type=0,
            tile_definitions=[0],
            tiles=[0] * (width * height),
            collision=[False] * (width * height),
            mirror=[False] * (width * height),
        )
    sections = generated.to_1407_sections()
    map_type = int(sections['map_type'])
    width = int(sections['width'])
    height = int(sections['height'])
    tile_definitions = sections['definitions']
    encoded_tiles = sections['tiles_rle']
    collision = sections['collision']
    mirror = sections['mirror']
    assert isinstance(tile_definitions, bytes)
    assert isinstance(encoded_tiles, bytes)
    assert isinstance(collision, bytes)
    assert isinstance(mirror, bytes)

    return [
        map_action(definition, 11, role_id=role_id),
        encode_frame(1407, [byte(0), byte(map_type), byte(width), byte(height)]),
        encode_frame(1407, [byte(1), short(len(tile_definitions)), binary(tile_definitions)]),
        encode_frame(1407, [byte(3), short(len(encoded_tiles)), binary(encoded_tiles)]),
        encode_frame(1407, [byte(5), short(len(collision)), binary(collision)]),
        encode_frame(1407, [byte(7), short(len(mirror)), binary(mirror)]),
        # status=1 skips the APK-local map.o lookup; 1407 still supplies the
        # authoritative logical map data used by the server transition.
        map_action(definition, 12, status=1, role_id=role_id),
    ]


def map_enter_frames(definition: MapDefinition, role_id: int | None = None) -> list[bytes]:
    # Distinct drawable map ids must carry matching APK-local map.ref/map.o
    # resources.  status=0 asks the client to load those resources before it
    # acknowledges entry; status=1 is reserved for definitions without them.
    ref_status = 0 if definition.map_ref_available else 1
    frames = [
        map_action(definition, 13, status=ref_status, role_id=role_id),
        map_action(definition, 14, role_id=role_id),
        map_action(definition, 105, role_id=role_id),
    ]
    if definition.monster is not None:
        frames.append(map_monster_frame(definition))
    frames.extend(map_portal_frames(definition))
    frames.extend(map_npc_frames(definition))
    # After every 1126 subtype=0 actor is created, set their initial facing with
    # 1126 subtype=1 (local-compat extension): the client finds the actor by id in
    # the same generic container and rotates it in place.  The direction frame is
    # never appended to the subtype=0 record (that would break its fixed field read).
    if definition.monster is not None:
        frames.append(map_actor_direction_frame(definition.monster.id, definition.monster.direction))
    frames.extend(
        map_actor_direction_frame(portal.id, portal.direction)
        for portal in definition.portals
    )
    return frames


def heartbeat_challenge(nonce: int) -> bytes:
    """Ask the original client for its built-in 1012 heartbeat response."""
    return encode_frame(1012, [integer(nonce)])


class LocalGameServer:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.roles = RoleStore(settings)
        self._next_session_id = 1000
        self._sessions: dict[tuple[int, int], str] = {}

    def handle_sect_skill_request(
        self,
        role: dict[str, object],
        values: list[object],
    ) -> tuple[bytes, ...]:
        """Apply one 1103 transition and persist any resulting level change."""
        before_level = sect_skill_level(role)
        response_frames = sect_skill_request_frames(role, values)
        if sect_skill_level(role) != before_level:
            self.roles.save()
        return response_frames

    def handle_strengthening_request(
        self,
        role: dict[str, object],
        values: list[object],
        rng=random,
    ) -> tuple[bytes, ...]:
        """Apply one 1009 strengthening transition and persist mutations only."""
        snapshot = copy.deepcopy(role)
        try:
            result = strengthening_action_result(role, values, rng)
            if result.changed:
                self.roles.save()
        except Exception:
            role.clear()
            role.update(snapshot)
            raise
        return result.frames

    def handle_shop_purchase(
        self,
        role: dict[str, object],
        fields: list[Field],
        mode: int = 0,
        category_id: int = 0,
    ) -> ShopPurchaseResult:
        """Apply one 1033 mall purchase and persist mutations only.

        ``mode``/``category_id`` are the connection-level mall state tracked
        by the 1067 handlers; the request's shop_id must match the shop the
        connection is currently browsing.
        """
        if not is_shop_purchase_request(fields):
            return ShopPurchaseResult((), False, '购买请求格式非法')
        shop = self.settings.shop_registry.by_mode(mode)
        if shop is None:
            return ShopPurchaseResult((), False, '当前不在商城')
        shop_id = int(fields[0].value)
        if shop_id != shop.shop_id:
            return ShopPurchaseResult((), False, '商店与当前商城不匹配')
        item_id = int(fields[2].value)
        quantity = int(fields[3].value)
        snapshot = copy.deepcopy(role)
        try:
            result = shop_purchase_result(
                role,
                shop,
                category_id,
                item_id,
                quantity,
                item_registry=self.settings.item_registry,
            )
            if result.changed:
                self.roles.save()
        except Exception:
            role.clear()
            role.update(snapshot)
            raise
        return result

    def handle_life_craft(
        self,
        role: dict[str, object],
        fields: list[Field],
    ) -> LifeTransactionResult:
        """Apply one 1143/action-5 craft and persist mutations only."""
        recipe_id = int(fields[1].value)
        slots = [int(field.value) for field in fields[2:6]]
        quantity = int(fields[6].value)
        recipe = self.settings.life_registry.recipe(recipe_id)
        snapshot = copy.deepcopy(role)
        try:
            result = craft_result(
                role,
                recipe,
                slots,
                quantity,
                life_registry=self.settings.life_registry,
                item_registry=self.settings.item_registry,
            )
            if result.changed:
                self.roles.save()
        except Exception:
            role.clear()
            role.update(snapshot)
            raise
        return result

    def handle_life_learn(
        self,
        role: dict[str, object],
        fields: list[Field],
        trainer_id: int = 0,
    ) -> LifeTransactionResult:
        """Apply one 1143/action-3 trainer learn and persist mutations only."""
        entry_id = int(fields[1].value)
        trainer = self.settings.life_registry.trainers.get(int(trainer_id))
        entry = self.settings.life_registry.learnable.get(entry_id)
        snapshot = copy.deepcopy(role)
        try:
            result = learn_result(
                role, trainer, entry, life_registry=self.settings.life_registry,
            )
            if result.changed:
                self.roles.save()
        except Exception:
            role.clear()
            role.update(snapshot)
            raise
        return result

    def handle_life_upgrade(
        self,
        role: dict[str, object],
        fields: list[Field],
    ) -> LifeTransactionResult:
        """Apply one 1132/action-6 skill upgrade and persist mutations only."""
        skill_id = int(fields[1].value)
        skill = self.settings.life_registry.skills.get(skill_id)
        snapshot = copy.deepcopy(role)
        try:
            result = upgrade_result(
                role, skill, life_registry=self.settings.life_registry,
            )
            if result.changed:
                self.roles.save()
        except Exception:
            role.clear()
            role.update(snapshot)
            raise
        return result

    def handle_gather_completion(
        self,
        role: dict[str, object],
        target,
    ) -> LifeTransactionResult:
        """Apply one gather reward and persist mutations only."""
        snapshot = copy.deepcopy(role)
        try:
            result = gathering_reward_result(
                role,
                target,
                life_registry=self.settings.life_registry,
                item_registry=self.settings.item_registry,
            )
            if result.changed:
                self.roles.save()
        except Exception:
            role.clear()
            role.update(snapshot)
            raise
        return result

    async def _finish_gathering_later(
        self,
        writer: asyncio.StreamWriter,
        cipher: GameCipher | None,
        lock: asyncio.Lock | None,
        username: str,
        active_role: dict[str, object],
        gathering: ConnectionGathering,
        session: dict[str, object],
        target,
        delay: float,
    ) -> None:
        """Complete a gather after `delay` seconds unless the session stale."""
        try:
            if delay > 0:
                await asyncio.sleep(delay)
            if not gathering.is_current(session):
                return
            if int(session.get('role_id', 0)) != int(active_role.get('id', 0)):
                return
            if not gathering.consume(session):
                return
            result = self.handle_gather_completion(active_role, target)
            if not result.changed:
                return
            LOG.info(
                'GATHER_COMPLETE user=%r role_id=%d target_id=%d stamina=%d proficiency=%d',
                username,
                int(active_role.get('id', 0)),
                int(session.get('target_id', 0)),
                life_stamina(active_role),
                (life_skill_state(active_role, target.skill_id) or {}).get('proficiency', 0),
            )
            await self._send(writer, *result.frames, cipher=cipher, lock=lock)
        except asyncio.CancelledError:
            raise
        except (ConnectionResetError, BrokenPipeError, OSError):
            return

    async def _send(
        self,
        writer: asyncio.StreamWriter,
        *frames: bytes,
        cipher: GameCipher | None = None,
        lock: asyncio.Lock | None = None,
    ) -> None:
        async def send_frames() -> None:
            for frame in frames:
                writer.write(cipher.encrypt_server_frame(frame) if cipher is not None else frame)
            await writer.drain()

        if lock is None:
            await send_frames()
        else:
            # GameCipher is stateful. Keep encryption and socket writes in one
            # critical section so heartbeat and request replies cannot interleave.
            async with lock:
                await send_frames()

    async def _heartbeat_loop(
        self,
        writer: asyncio.StreamWriter,
        cipher: GameCipher,
        send_lock: asyncio.Lock,
        peer: object,
    ) -> None:
        nonce = 0
        try:
            while True:
                await asyncio.sleep(self.settings.heartbeat_interval_seconds)
                nonce = 1 if nonce >= 0x7FFFFFFF else nonce + 1
                await self._send(
                    writer,
                    heartbeat_challenge(nonce),
                    cipher=cipher,
                    lock=send_lock,
                )
                LOG.info('heartbeat sent to %s nonce=%d', peer, nonce)
        except (ConnectionResetError, BrokenPipeError, OSError):
            return

    async def _handle_map_object_interaction(
        self,
        *,
        username: str,
        active_role: dict[str, object] | None,
        object_id: int,
        object_x: int | None,
        object_y: int | None,
        action: int | None,
        source: str,
        writer: asyncio.StreamWriter,
        cipher: GameCipher | None,
        send_lock: asyncio.Lock,
        battle_state: LocalBattleState,
        npc_dialogue_state: LocalNpcDialogueState,
    ) -> None:
        """Handle a map actor request without guessing battle data.

        Native 2030 NPCs use action 0; generic actors use action 6, and both
        payloads include the actor id and tile. Portal activation is a complete
        transition. A monster starts the local single-target battle probe using
        the confirmed 1040/action=1 shape.
        """
        current_settings = settings_for_role(self.settings, active_role)
        LOG.info(
            'map object interaction source=%s user=%r map=%d object_id=%d tile=%s,%s action=%s',
            source,
            username,
            current_settings.id,
            object_id,
            object_x,
            object_y,
            action,
        )

        if active_role is not None:
            target_settings = apply_portal_transition(self.settings, active_role, object_id)
        else:
            target_settings = None
        if target_settings is not None:
            npc_dialogue_state.clear()
            self.roles.save()
            LOG.info(
                'portal activated user=%r role_id=%d object_id=%d map %d -> %d',
                username,
                int(active_role['id']),
                object_id,
                current_settings.id,
                target_settings.id,
            )
            # 1110 is the same world/map descriptor used by the original map
            # transition. The client then requests 1010/12 and 1010/13.
            await self._send(
                writer,
                notice_and_world(self.settings, active_role)[1],
                cipher=cipher,
                lock=send_lock,
            )
            return

        npc = map_npc_for_object_id(current_settings, object_id)
        if npc is not None:
            npc_dialogue_state.select(current_settings.id, npc.id)
            LOG.info(
                'npc interaction user=%r npc_id=%d name=%r source=%s; opening native map dialogue',
                username,
                object_id,
                npc.name,
                source,
            )
            await self._send(
                writer,
                *map_npc_dialogue_frames(npc, active_role),
                cipher=cipher,
                lock=send_lock,
            )
            return

        monster = current_settings.monster
        if monster is not None and object_id == monster.id:
            if should_suppress_escape_retrigger(
                battle_state.escape_guard,
                current_settings.id,
                object_id,
            ):
                LOG.info(
                    'BATTLE_ESCAPE_RETRIGGER_SUPPRESSED user=%r player_id=%d monster_id=%d map_id=%d source=%s',
                    username,
                    int(active_role['id']) if active_role is not None else battle_state.player_id,
                    object_id,
                    current_settings.id,
                    source,
                )
                await self._send(
                    writer,
                    map_object_interaction_ack_frame(object_id),
                    cipher=cipher,
                    lock=send_lock,
                )
                return
            if battle_state.monster_defeated:
                LOG.info(
                    'suppressed stale monster interaction user=%r monster_id=%d; encounter already settled',
                    username,
                    object_id,
                )
                await self._send(
                    writer,
                    map_object_remove_frame(object_id),
                    cipher=cipher,
                    lock=send_lock,
                )
                return
            if battle_state.active:
                LOG.info(
                    'ignored duplicate monster interaction user=%r monster_id=%d; battle already active battle_trace=%s',
                    username,
                    object_id,
                    battle_state.trace_id,
                )
                return
            role = active_role if active_role is not None else default_role(self.settings)
            battle_state.begin(
                int(role['id']),
                object_id,
                player_stats=combat_stats(role),
            )
            battle_state.map_id = current_settings.id
            battle_state.contact_tile = (
                (int(object_x), int(object_y))
                if object_x is not None and object_y is not None
                else None
            )
            if battle_state.contact_tile is not None:
                battle_state.player_tile = battle_state.contact_tile
            LOG.info(
                'monster interaction recorded user=%r monster_id=%d; starting local battle battle_trace=%s',
                username,
                object_id,
                battle_state.trace_id,
            )
            # The APK's 1040/action=1 handler only updates an already-created
            # battle screen (d/n.d(20)).  A fresh map session has no screen 20
            # yet, so action=1 alone is silently ignored and the UI remains on
            # its loading prompt.  Action 0 is the original reset/open path:
            # it removes any stale map/battle state and then creates screen
            # 20 before action 1 fills in the first round.  The battle screen
            # also builds its grid from 1048 actor records; without these the
            # scene opens but has no drawable player/monster and appears blank.
            LOG.info(
                'sending battle reset/start user=%r player_id=%d monster_id=%d battle_trace=%s',
                username,
                int(role['id']),
                object_id,
                battle_state.trace_id,
            )
            LOG.info(
                'BATTLE_1040 action=0 battle_trace=%s user=%r',
                battle_state.trace_id,
                username,
            )
            await self._send(
                writer,
                battle_reset_frame(),
                *battle_actor_frames(
                    role,
                    current_settings,
                    trace_id=battle_state.trace_id,
                    state=battle_state,
                ),
                battle_start_frame(role, current_settings),
                cipher=cipher,
                lock=send_lock,
            )
            LOG.info(
                'BATTLE_1040 action=1 battle_trace=%s user=%r round=1',
                battle_state.trace_id,
                username,
            )
            return

        LOG.info('ignored map object action id=%d map=%d', object_id, current_settings.id)

    async def handle(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        peer = writer.get_extra_info('peername')
        LOG.info('client connected: %s', peer)
        username = ''
        world_sent = False
        active_role: dict[str, object] | None = None
        game_cipher: GameCipher | None = None
        battle_state = LocalBattleState()
        team_state = LocalTeamState()
        npc_dialogue_state = LocalNpcDialogueState()
        streamed_npc_ids: set[int] = set()
        send_lock = asyncio.Lock()
        heartbeat_task: asyncio.Task[None] | None = None
        position_dirty = False
        last_position_checkpoint_at = time.monotonic()
        # Connection-level mall state (screen 611 tab + selected category).
        # Never persisted to the role; cleared implicitly on disconnect.
        current_shop_mode = 0
        current_shop_category = 0
        # Connection-level gathering state (one active 2027 gather at most).
        gathering = ConnectionGathering()
        try:
            while True:
                header = await reader.readexactly(2)
                frame_length = struct.unpack('>H', header)[0]
                if frame_length < 4:
                    raise ProtocolError(f'invalid frame length {frame_length}')
                payload = await reader.readexactly(frame_length - 2)
                if len(payload) < 2:
                    raise ProtocolError('payload is missing the message id')
                message_hint = struct.unpack_from('>H', payload, 0)[0]
                if game_cipher is None and message_hint == 1052:
                    game_cipher = GameCipher()
                    LOG.info('game cipher enabled for %s', peer)
                decoded_payload = payload
                if game_cipher is not None:
                    decoded_payload = payload[:2] + game_cipher.decrypt(payload[2:])
                try:
                    message_id, fields = decode_payload(decoded_payload)
                except ProtocolError:
                    LOG.warning('raw payload message_hint=%d hex=%s', message_hint, payload.hex())
                    raise
                values = field_values(fields)
                LOG.info('received message=%d field_types=%s', message_id, [x.type_id for x in fields])

                if message_id == 1077:
                    username = str(values[3]) if len(values) > 3 else ''
                    password = str(values[4]) if len(values) > 4 else ''
                    version = int(values[0]) if values else -1
                    LOG.info('login request user=%r password=%s version=%s', username, '*' * len(password), version)
                    if not username or not password:
                        await self._send(writer, encode_frame(1055, [byte(5), string('账号或密码不能为空')]))
                    elif version != self.settings.expected_client_version:
                        await self._send(writer, encode_frame(1055, [byte(6), string('客户端版本不匹配')]))
                    else:
                        await self._send(writer, login_server_list(self.settings))

                elif message_id == 1051:
                    username = str(values[0]) if values else username
                    selected = str(values[2]) if len(values) > 2 else ''
                    self._next_session_id += 1
                    session_id = self._next_session_id
                    account_id = session_id + 100000
                    self._sessions[(session_id, account_id)] = username
                    LOG.info('server selected user=%r address=%r session=%d', username, selected, session_id)
                    await self._send(writer, game_server_redirect(self.settings, session_id, account_id))

                elif message_id == 1052:
                    session_id = int(values[0]) if values else 0
                    account_id = int(values[1]) if len(values) > 1 else 0
                    username = self._sessions.get((session_id, account_id), 'local-player')
                    LOG.info('game handshake user=%r session=%d account=%d', username, session_id, account_id)
                    await self._send(
                        writer,
                        role_list(self.settings, self.roles.roles_for(username)),
                        cipher=game_cipher,
                        lock=send_lock,
                    )
                    if heartbeat_task is None and game_cipher is not None:
                        heartbeat_task = asyncio.create_task(
                            self._heartbeat_loop(writer, game_cipher, send_lock, peer)
                        )

                elif message_id == 1080 and values:
                    action = int(values[0])
                    if action == 0:
                        role_id = int(values[1]) if len(values) > 1 else 0
                        if position_dirty:
                            self.roles.save()
                            position_dirty = False
                        last_position_checkpoint_at = time.monotonic()
                        active_role = self.roles.find(username, role_id)
                        if active_role is None:
                            LOG.warning('unknown role selected user=%r role_id=%d', username, role_id)
                        else:
                            team_state.leader_id = 0
                            world_sent = False
                            streamed_npc_ids.clear()
                            LOG.info('role selected user=%r role_id=%d name=%r', username, role_id, active_role['name'])
                            sect_id = normalized_sect_id(active_role)
                            LOG.info(
                                'ROLE_SECT role_id=%d name=%r sect_id=%d sect_name=%r race=%d',
                                role_id,
                                active_role['name'],
                                sect_id,
                                SECTS[sect_id],
                                int(active_role.get('race', 0)),
                            )
                            LOG.info('%s', format_map_player_appearance_log(username, active_role, self.settings))
                            role_map_id = int(active_role.get('map_id', self.settings.default_map_id))
                            gather_targets = self.settings.life_registry.gather_targets_for(role_map_id)
                            await self._send(
                                writer,
                                player_info(self.settings, active_role),
                                character_extension_info(),
                                life_skill_list_frame(active_role, self.settings),
                                sect_skill_list(active_role),
                                *(item_frame(item) for item in role_items(active_role)),
                                gather_catalog_frame(gather_targets),
                                *(gather_spawn_frame(target) for target in gather_targets),
                                cipher=game_cipher,
                                lock=send_lock,
                            )
                    elif action == 1:
                        role_id = int(values[1]) if len(values) > 1 else 0
                        deleted = self.roles.delete(username, role_id)
                        LOG.info('role delete user=%r role_id=%d deleted=%s', username, role_id, deleted)
                        await self._send(writer, deletion_result(role_id), cipher=game_cipher, lock=send_lock)
                    elif action == 2:
                        name = str(values[1]) if len(values) > 1 else ''
                        model = int(values[2]) if len(values) > 2 else 0
                        slot = int(values[3]) if len(values) > 3 else 0
                        created = self.roles.create(username, name, model, slot)
                        LOG.info(
                            'role created user=%r role_id=%d name=%r model=%d slot=%d race=%d gender=%d',
                            username,
                            created['id'],
                            created['name'],
                            created['model'],
                            created['slot'],
                            created['race'],
                            created['gender'],
                        )
                        await self._send(
                            writer,
                            role_list(self.settings, self.roles.roles_for(username)),
                            cipher=game_cipher,
                            lock=send_lock,
                        )
                    elif action == 4:
                        LOG.info('creation names requested user=%r', username)
                        await self._send(writer, creation_names(), cipher=game_cipher, lock=send_lock)
                    else:
                        LOG.info('ignored role action=%d values=%r', action, values)

                elif message_id == 1123 and not world_sent:
                    world_sent = True
                    current = active_role if active_role is not None else default_role(self.settings)
                    LOG.info('client initialized; sending world %d %s', current['map_id'], current['map_name'])
                    await self._send(
                        writer,
                        *notice_and_world(self.settings, current),
                        cipher=game_cipher,
                        lock=send_lock,
                    )

                elif message_id == 1005 and len(values) >= 2:
                    movement_interrupt = gathering.cancel()
                    if movement_interrupt is not None:
                        LOG.info(
                            'GATHER_CANCEL user=%r role_id=%d reason=movement',
                            username,
                            int(active_role.get('id', 0)) if active_role is not None else 0,
                        )
                        await self._send(
                            writer, movement_interrupt, cipher=game_cipher, lock=send_lock,
                        )
                    old_tile = battle_state.player_tile
                    movement_x, movement_y = map_movement_final_tile(values)
                    guard_had_no_origin = bool(
                        battle_state.escape_guard
                        and battle_state.escape_guard.get('origin') is None
                    )
                    guard_cleared = update_escape_guard_for_movement(
                        battle_state,
                        movement_x,
                        movement_y,
                    )
                    if guard_cleared:
                        LOG.info(
                            'BATTLE_ESCAPE_GUARD_CLEARED user=%r old_tile=%s new_tile=%s reason=real_1005_movement',
                            username,
                            old_tile,
                            battle_state.player_tile,
                        )
                    elif guard_had_no_origin and battle_state.escape_guard:
                        LOG.info(
                            'BATTLE_ESCAPE_GUARD_ORIGIN_ESTABLISHED user=%r tile=%s',
                            username,
                            battle_state.player_tile,
                        )
                    if active_role is not None:
                        if update_role_position(active_role, movement_x, movement_y):
                            position_dirty = True
                            now = time.monotonic()
                            if now - last_position_checkpoint_at >= POSITION_CHECKPOINT_SECONDS:
                                self.roles.save()
                                position_dirty = False
                                last_position_checkpoint_at = now
                                LOG.info(
                                    'ROLE_POSITION_CHECKPOINT user=%r role_id=%d map=%d tile=%d,%d',
                                    username,
                                    int(active_role.get('id', 0)),
                                    int(active_role.get('map_id', self.settings.default_map_id)),
                                    movement_x,
                                    movement_y,
                                )
                    current_settings = settings_for_role(self.settings, active_role)
                    nearby_npcs = map_npcs_near(current_settings, movement_x, movement_y)
                    nearby_ids = {npc.id for npc in nearby_npcs}
                    entered_npcs = [
                        npc for npc in nearby_npcs
                        if npc.id not in streamed_npc_ids
                    ]
                    streamed_npc_ids.intersection_update(nearby_ids)
                    if entered_npcs:
                        LOG.info(
                            'NPC_REGION_STREAM user=%r map=%d tile=%d,%d ids=%r',
                            username,
                            current_settings.id,
                            movement_x,
                            movement_y,
                            [npc.id for npc in entered_npcs],
                        )
                        await self._send(
                            writer,
                            *(map_npc_frame(current_settings, npc) for npc in entered_npcs),
                            cipher=game_cipher,
                            lock=send_lock,
                        )
                        streamed_npc_ids.update(npc.id for npc in entered_npcs)

                elif message_id == 1010 and values:
                    action = int(values[0])
                    if action == 36 and active_role is not None:
                        # The character panel sends
                        # [short(36), int(0=automatic, 1=manual)].
                        manual = bool(int(values[1])) if len(values) > 1 else False
                        active_role['auto_level'] = not manual
                        self.roles.save()
                        LOG.info('level mode changed user=%r automatic=%s', username, not manual)
                    elif action == 12:
                        current_settings = settings_for_role(self.settings, active_role)
                        LOG.info('client requested map data map=%d', current_settings.id)
                        role_id = int(active_role['id']) if active_role is not None else self.settings.role_id
                        await self._send(
                            writer,
                            *map_data_frames(current_settings, role_id),
                            cipher=game_cipher,
                            lock=send_lock,
                        )
                    elif action == 13:
                        current_settings = settings_for_role(self.settings, active_role)
                        # Map entry is the respawn boundary for the local
                        # encounter; never carry a completed battle into the
                        # newly loaded scene.
                        battle_state.reset_encounter()
                        npc_dialogue_state.clear()
                        gather_transition = gathering.cancel()
                        if gather_transition is not None:
                            LOG.info(
                                'GATHER_CANCEL user=%r role_id=%d reason=map_transition',
                                username,
                                int(active_role.get('id', 0)) if active_role is not None else 0,
                            )
                        monster = current_settings.monster
                        LOG.info(
                            'client requested map reference; map=%d entering at %d,%d; monster=%s',
                            current_settings.id,
                            current_settings.spawn_x,
                            current_settings.spawn_y,
                            (
                                f'id={monster.id} model={monster.model} at {monster.x},{monster.y}'
                                if monster is not None
                                else 'disabled'
                            ),
                        )
                        role_id = int(active_role['id']) if active_role is not None else self.settings.role_id
                        enter_frames = list(map_enter_frames(current_settings, role_id))
                        if gather_transition is not None:
                            enter_frames.insert(0, gather_transition)
                        enter_frames.extend(
                            gather_spawn_frame(target)
                            for target in self.settings.life_registry.gather_targets_for(
                                current_settings.id
                            )
                        )
                        await self._send(
                            writer,
                            *enter_frames,
                            cipher=game_cipher,
                            lock=send_lock,
                        )
                        streamed_npc_ids.clear()
                        streamed_npc_ids.update(npc.id for npc in current_settings.npcs)
                    elif action == 7 and len(values) > 1:
                        # Compatibility with an older map-object path seen in
                        # some client builds. The active APK uses 2031 below.
                        await self._handle_map_object_interaction(
                            username=username,
                            active_role=active_role,
                            object_id=int(values[1]),
                            object_x=None,
                            object_y=None,
                            action=action,
                            source='1010/7',
                            writer=writer,
                            cipher=game_cipher,
                            send_lock=send_lock,
                            battle_state=battle_state,
                            npc_dialogue_state=npc_dialogue_state,
                        )
                    elif action == 15:
                        # Sent by the APK after it receives action=105
                        # (actionEnterMapOK).  This is a client acknowledgement,
                        # not a request for another map frame.
                        LOG.info('map entry acknowledged by client map=%d', settings_for_role(self.settings, active_role).id)
                    else:
                        LOG.info('ignored client map action=%d', action)
                elif message_id == 2031 and values:
                    # main/k encodes [object_id, 0, x, y, action, 0]. Native
                    # 2030 NPCs use action 0; generic 1126 actors use action 6.
                    gather_interrupt = gathering.cancel()
                    if gather_interrupt is not None:
                        LOG.info(
                            'GATHER_CANCEL user=%r role_id=%d reason=map_interaction',
                            username,
                            int(active_role.get('id', 0)) if active_role is not None else 0,
                        )
                    object_id, object_x, object_y, object_action = map_object_interaction_values(values)
                    await self._handle_map_object_interaction(
                        username=username,
                        active_role=active_role,
                        object_id=object_id,
                        object_x=object_x,
                        object_y=object_y,
                        action=object_action,
                        source='2031',
                        writer=writer,
                        cipher=game_cipher,
                        send_lock=send_lock,
                        battle_state=battle_state,
                        npc_dialogue_state=npc_dialogue_state,
                    )
                elif message_id == 1533 and values:
                    # The native dialogue sends [byte(0), int(option_id)]
                    # when a row is tapped.  The local NPC currently exposes
                    # only the terminal option, so acknowledge it in the log
                    # and let the client keep the panel open until Back is
                    # pressed (the APK closes the panel locally on Back).
                    LOG.info('npc dialogue option selected user=%r values=%r', username, values)
                elif message_id == 2032 and values:
                    # Screen 6 closes the compact native NPC overlay locally,
                    # then reports [byte(option_id), byte(101), string(input)]
                    # and enables the global wait overlay. S->C 1010 clears
                    # that overlay before dispatching action 7. A validated
                    # sect mentor selection appends action 69 to open the
                    # native learning-mode screen; all other paths are ACK-only.
                    option_id = int(values[0])
                    response_frames = npc_dialogue_option_frames(
                        self.settings,
                        active_role,
                        npc_dialogue_state,
                        option_id,
                    )
                    LOG.info(
                        'native npc dialogue option selected user=%r option=%d values=%r mentor_mode=%s',
                        username,
                        option_id,
                        values,
                        len(response_frames) > 1,
                    )
                    await self._send(
                        writer,
                        *response_frames,
                        cipher=game_cipher,
                        lock=send_lock,
                    )
                elif message_id == 1500 and active_role is not None and values:
                    response_frames, changed = mail_request_frames(active_role, values)
                    if changed:
                        self.roles.save()
                    LOG.info(
                        'mail action user=%r role_id=%d action=%d replies=%d changed=%s',
                        username,
                        int(active_role['id']),
                        int(values[0]),
                        len(response_frames),
                        changed,
                    )
                    if response_frames:
                        await self._send(
                            writer,
                            *response_frames,
                            cipher=game_cipher,
                            lock=send_lock,
                        )
                elif message_id == 1023 and active_role is not None and values:
                    action = int(values[0])
                    response_frames = team_request_frames(active_role, values, team_state)
                    LOG.info(
                        'team action user=%r role_id=%d action=%d active=%s replies=%d',
                        username,
                        int(active_role['id']),
                        action,
                        team_state.active,
                        len(response_frames),
                    )
                    if response_frames:
                        await self._send(
                            writer,
                            *response_frames,
                            cipher=game_cipher,
                            lock=send_lock,
                        )
                elif message_id == 1502 and len(values) >= 3:
                    # Fields are [action, count, id...]. Action 1 requests a
                    # role .dat (1503); actions 0/2 request a PNG payload
                    # (1501). Treating all three as .dat leaves actor records
                    # alive but permanently invisible.
                    query_action = int(values[0])
                    resource_count = int(values[1])
                    resource_ids = [int(value) for value in values[2:2 + resource_count]]
                    LOG.info(
                        'battle resource query action=%d count=%d ids=%r battle_trace=%s',
                        query_action,
                        resource_count,
                        resource_ids,
                        battle_state.trace_id,
                    )
                    for resource_id in resource_ids:
                        if query_action == 1:
                            resource_frames = battle_resource_frames(resource_id)
                            resolution = battle_resource_resolution(resource_id)
                            response_type = 1503 if resource_frames else None
                        elif query_action in (PNG_QUERY_MAIN_CACHE, PNG_QUERY_ROLE_CACHE):
                            resource_frames = battle_image_frames(query_action, resource_id)
                            resolution = battle_image_resolve_debug(resource_id)
                            response_type = 1501 if resource_frames else None
                        else:
                            LOG.warning(
                                'unsupported battle resource action=%d id=%d',
                                query_action,
                                resource_id,
                            )
                            resource_frames = []
                            resolution = {
                                'alias': None,
                                'branch': 'unsupported',
                                'offset_id': None,
                                'resolved_id': None,
                                'resolved_path': None,
                            }
                            response_type = None
                        LOG.info(
                            'battle resource response action=%d id=%d chunks=%d battle_trace=%s',
                            query_action,
                            resource_id,
                            len(resource_frames),
                            battle_state.trace_id,
                        )
                        LOG.info(
                            '%s',
                            format_battle_resource_query_log(
                                username=username,
                                query_action=query_action,
                                resource_ids=resource_ids,
                                battle_active=battle_state.active,
                                round_number=battle_state.round,
                                trace_id=battle_state.trace_id,
                                resource_id=resource_id,
                                resolution=resolution,
                                response_type=response_type,
                                chunks=len(resource_frames),
                            ),
                        )
                        if resource_frames:
                            await self._send(
                                writer,
                                *resource_frames,
                                cipher=game_cipher,
                                lock=send_lock,
                            )
                elif message_id == 1040 and values:
                    # After the client drains its local action queue it sends
                    # BATTLE_ACTION_SHOW back as a two-field acknowledgement
                    # [action=2, round].  It is the barrier between the player
                    # action, the monster counterattack, and the next round.
                    ack_action = int(values[0])
                    ack_round = int(values[1]) if len(values) > 1 else None
                    if battle_state.active and ack_action == 2 and ack_round is not None:
                        LOG.info(
                            'BATTLE_1040 action=2 ack battle_trace=%s user=%r round=%d server_round=%d',
                            battle_state.trace_id,
                            username,
                            ack_round,
                            battle_state.round,
                        )
                        if battle_state.phase == 'round_ack':
                            if battle_state.monster_hp <= 0:
                                reward_item = None
                                level_up = False
                                if active_role is not None:
                                    reward_item, level_up = apply_battle_rewards(active_role, registry=self.settings.item_registry)
                                    self.roles.save()
                                battle_state.finish()
                                battle_state.monster_defeated = True
                                # Send removal before the reward UI. In
                                # automatic mode the APK can otherwise send a
                                # new object interaction immediately after the
                                # end frame and start a second battle.
                                result_frames = [
                                    battle_end_frame(),
                                    map_object_remove_frame(battle_state.monster_id),
                                ]
                                if active_role is not None and reward_item is not None:
                                    result_frames.extend((
                                        battle_progress_frame(active_role),
                                        item_frame(reward_item, operation=3),
                                        battle_reward_notice(BATTLE_EXP_REWARD, reward_item, level_up),
                                    ))
                                    if level_up:
                                        result_frames.append(level_up_effect_frame(active_role))
                                    else:
                                        result_frames.append(
                                            battle_reward_popup(BATTLE_EXP_REWARD, reward_item, level_up)
                                        )
                                LOG.info(
                                    'BATTLE_1040 action=4 settlement battle_trace=%s user=%r reason=monster_dead top_protocol=%s monster_hp=%d player_hp=%d',
                                    battle_state.trace_id,
                                    username,
                                    '1129/level-up' if level_up else '1049/3',
                                    battle_state.monster_hp,
                                    battle_state.player_hp,
                                )
                                await self._send(writer, *result_frames, cipher=game_cipher, lock=send_lock)
                            elif battle_state.player_hp <= 0:
                                battle_state.finish()
                                LOG.info(
                                    'BATTLE_1040 action=4 battle_trace=%s user=%r reason=player_dead monster_hp=%d player_hp=%d',
                                    battle_state.trace_id,
                                    username,
                                    battle_state.monster_hp,
                                    battle_state.player_hp,
                                )
                                await self._send(writer, battle_end_frame(), cipher=game_cipher, lock=send_lock)
                            else:
                                # Playback was started by the action=2 frame
                                # sent after the 1042 batch. This short client
                                # response means both attacks, effects and
                                # return movements are now complete.
                                battle_state.round = ack_round + 1
                                battle_state.phase = 'idle'
                                LOG.info(
                                    'battle round ready battle_trace=%s user=%r round=%d monster_hp=%d player_hp=%d',
                                    battle_state.trace_id,
                                    username,
                                    battle_state.round,
                                    battle_state.monster_hp,
                                    battle_state.player_hp,
                                )
                            continue
                    else:
                        LOG.info('ignored client battle state values=%r active=%s', values, battle_state.active)
                elif message_id == 1041 and values:
                    # C->S command 6 is the APK's player escape request.
                    # Command 10 is quit-spectator and must never enter escape.
                    command_code = int(values[0])
                    LOG.info(
                        'BATTLE_1041 battle_trace=%s user=%r values=%r active=%s command=%d',
                        battle_state.trace_id,
                        username,
                        values,
                        battle_state.active,
                        command_code,
                    )
                    if is_player_escape_command(command_code):
                        if not battle_state.active:
                            LOG.info('ignored escape request without active battle user=%r', username)
                            continue
                        if battle_state.phase != 'idle':
                            LOG.info('ignored battle escape while awaiting action acknowledgement')
                            continue
                        client_round = int(values[1]) if len(values) > 1 else battle_state.round
                        if client_round > 0:
                            battle_state.round = client_round
                        escape_frames = battle_escape_request_frames(
                            battle_state,
                            battle_state.round,
                        )
                        LOG.info(
                            'BATTLE_ESCAPE_START battle_trace=%s user=%r player_id=%d round=%d active=%s phase=%s protocol=1041/10',
                            battle_state.trace_id,
                            username,
                            battle_state.player_id,
                            battle_state.round,
                            battle_state.active,
                            battle_state.phase,
                        )
                        await self._send(
                            writer,
                            *escape_frames,
                            cipher=game_cipher,
                            lock=send_lock,
                        )
                        continue
                    if battle_state.active:
                        if battle_state.phase != 'idle':
                            LOG.info('ignored battle command while awaiting action acknowledgement')
                            continue
                        if command_code not in (1, 2):
                            LOG.info('ignored unsupported battle command=%d', command_code)
                            continue
                        client_round = int(values[1]) if len(values) > 1 else battle_state.round
                        if client_round > 0:
                            battle_state.round = client_round
                        action_round = battle_state.round
                        action_frames, ended = battle_round_action_frames(
                            battle_state,
                            command_code,
                            action_round,
                        )
                        battle_state.phase = 'round_ack'
                        LOG.info(
                            'battle send player-action battle_trace=%s user=%r command=%d round=%d monster_hp=%d player_hp=%d ended=%s',
                            battle_state.trace_id,
                            username,
                            command_code,
                            action_round,
                            battle_state.monster_hp,
                            battle_state.player_hp,
                            ended,
                        )
                        await self._send(
                            writer,
                            *action_frames,
                            battle_action_show_frame(battle_state, action_round),
                            cipher=game_cipher,
                            lock=send_lock,
                        )
                        LOG.info(
                            'BATTLE_1040 action=2 show battle_trace=%s user=%r round=%d phase=round_ack',
                            battle_state.trace_id,
                            username,
                            action_round,
                        )
                        continue
                elif message_id == 1129 and active_role is not None and values:
                    # The APK's manual Upgrade button sends [short(3)].
                    action = int(values[0])
                    if action == 3:
                        if apply_one_level(active_role):
                            self.roles.save()
                            LOG.info(
                                'manual level-up user=%r role_id=%d level=%d experience=%d',
                                username,
                                int(active_role['id']),
                                int(active_role['level']),
                                int(active_role['experience']),
                            )
                            await self._send(
                                writer,
                                battle_progress_frame(active_role),
                                level_up_effect_frame(active_role),
                                cipher=game_cipher,
                                lock=send_lock,
                            )
                        else:
                            await self._send(
                                writer,
                                top_message_frame('经验不足，无法升级'),
                                cipher=game_cipher,
                                lock=send_lock,
                            )
                    else:
                        LOG.info('ignored level action=%d values=%r', action, values)
                elif message_id == 1012:
                    LOG.info('heartbeat response from %s values=%r', peer, values)
                elif message_id == 1039 and active_role is not None and values:
                    action = int(values[0])
                    attributes, divine = character_panel_frames(active_role)
                    if action == 1:
                        LOG.info('character panel requested; sending level/EXP sync plus attributes and divine-power summary')
                        await self._send(
                            writer,
                            battle_progress_frame(active_role),
                            attributes,
                            divine,
                            cipher=game_cipher,
                            lock=send_lock,
                        )
                    elif action == 2:
                        LOG.info('character divine-power detail requested values=%r', values)
                        await self._send(writer, divine, cipher=game_cipher, lock=send_lock)
                    else:
                        LOG.info('ignored character panel action=%d values=%r', action, values)
                elif message_id == 1089 and active_role is not None:
                    LOG.info('character extension data requested values=%r', values)
                    await self._send(
                        writer,
                        character_extension_info(),
                        cipher=game_cipher,
                        lock=send_lock,
                    )
                elif message_id == 1103 and active_role is not None and values:
                    action = int(values[0])
                    before_level = sect_skill_level(active_role)
                    response_frames = self.handle_sect_skill_request(active_role, values)
                    after_level = sect_skill_level(active_role)
                    LOG.info(
                        'sect skill request action=%d values=%r response_count=%d level=%d->%d',
                        action,
                        values,
                        len(response_frames),
                        before_level,
                        after_level,
                    )
                    await self._send(
                        writer,
                        *response_frames,
                        cipher=game_cipher,
                        lock=send_lock,
                    )
                elif message_id == 1132 and active_role is not None:
                    if is_life_skill_list_request(fields):
                        LOG.info(
                            'character skill list requested user=%r role_id=%d',
                            username,
                            int(active_role.get('id', 0)),
                        )
                        await self._send(
                            writer,
                            life_skill_list_frame(active_role, self.settings),
                            cipher=game_cipher,
                            lock=send_lock,
                        )
                    elif is_life_skill_open_request(fields):
                        skill_id = int(fields[1].value)
                        skill = self.settings.life_registry.skills.get(skill_id)
                        if skill is None:
                            LOG.info(
                                'LIFE_SKILL_OPEN_REJECT user=%r skill_id=%d reason=unknown_skill',
                                username,
                                skill_id,
                            )
                        else:
                            LOG.info(
                                'LIFE_SKILL_OPEN user=%r role_id=%d skill_id=%d',
                                username,
                                int(active_role.get('id', 0)),
                                skill_id,
                            )
                            await self._send(
                                writer,
                                life_tier_frame(skill, self.settings.life_registry),
                                life_skill_info_frame(
                                    skill_id,
                                    int((life_skill_state(active_role, skill_id) or {}).get('level', 0)),
                                    f'{skill.name} 熟练度 '
                                    f'{int((life_skill_state(active_role, skill_id) or {}).get("proficiency", 0))}',
                                ),
                                cipher=game_cipher,
                                lock=send_lock,
                            )
                    elif is_life_recipe_list_request(fields):
                        skill_id = int(fields[1].value)
                        tier = int(fields[2].value)
                        skill = self.settings.life_registry.skills.get(skill_id)
                        recipes = self.settings.life_registry.recipes_for(skill_id, tier)
                        if skill is None or not recipes:
                            LOG.info(
                                'LIFE_SKILL_LIST_REJECT user=%r skill_id=%d tier=%d reason=no_recipes',
                                username,
                                skill_id,
                                tier,
                            )
                        else:
                            LOG.info(
                                'LIFE_SKILL_LIST user=%r role_id=%d skill_id=%d tier=%d count=%d',
                                username,
                                int(active_role.get('id', 0)),
                                skill_id,
                                tier,
                                len(recipes),
                            )
                            await self._send(
                                writer,
                                life_recipe_list_frame(skill, tier, recipes, self.settings.life_registry),
                                cipher=game_cipher,
                                lock=send_lock,
                            )
                    elif is_life_skill_info_request(fields):
                        skill_id = int(fields[1].value)
                        skill = self.settings.life_registry.skills.get(skill_id)
                        state = life_skill_state(active_role, skill_id) or {}
                        text = f'{skill.name} 等级 {state.get("level", 0)}' if skill else '未知技能'
                        await self._send(
                            writer,
                            life_skill_info_frame(
                                skill_id, int(state.get('level', 0)), text,
                            ),
                            cipher=game_cipher,
                            lock=send_lock,
                        )
                    elif is_life_skill_upgrade_request(fields):
                        skill_id = int(fields[1].value)
                        skill = self.settings.life_registry.skills.get(skill_id)
                        if skill is None:
                            LOG.info(
                                'LIFE_SKILL_UPGRADE_REJECT user=%r skill_id=%d reason=unknown_skill',
                                username,
                                skill_id,
                            )
                        else:
                            LOG.info(
                                'LIFE_SKILL_UPGRADE_REQUEST user=%r role_id=%d skill_id=%d',
                                username,
                                int(active_role.get('id', 0)),
                                skill_id,
                            )
                            result = self.handle_life_upgrade(active_role, fields)
                            if result.changed:
                                state = life_skill_state(active_role, skill_id) or {}
                                LOG.info(
                                    'LIFE_SKILL_UPGRADE_SUCCESS user=%r skill_id=%d level=%d '
                                    'silver=%d experience=%d',
                                    username,
                                    skill_id,
                                    int(state.get('level', 0)),
                                    int(active_role.get('currencies', {}).get('silver', 0)),
                                    int(active_role.get('experience', 0)),
                                )
                                await self._send(writer, *result.frames, cipher=game_cipher, lock=send_lock)
                            else:
                                LOG.info(
                                    'LIFE_SKILL_UPGRADE_REJECT user=%r skill_id=%d reason=%s',
                                    username,
                                    skill_id,
                                    result.reason or 'unknown',
                                )
                                await self._send(
                                    writer,
                                    life_skill_info_frame(skill_id, 0, result.reason),
                                    cipher=game_cipher,
                                    lock=send_lock,
                                )
                    else:
                        LOG.info('ignored skill message=%d values=%r', message_id, values)
                elif message_id in MENU_PREFETCH_EMPTY_SUBTYPES:
                    LOG.info('menu prefetch acknowledged as empty message=%d values=%r', message_id, values)
                    await self._send(
                        writer,
                        menu_prefetch_empty_ack(message_id),
                        cipher=game_cipher,
                        lock=send_lock,
                    )
                elif message_id == 1032 and active_role is not None and len(values) >= 2:
                    item_id = int(values[1])
                    # Different item-detail screens in this client send either
                    # the instance id or the shared template id.
                    item = find_item(active_role, item_id)
                    if item is None:
                        item = next(
                            (
                                candidate
                                for candidate in role_items(active_role)
                                if int(candidate.get('template_id', 0)) == item_id
                            ),
                            None,
                        )
                    if item is not None:
                        LOG.info('item detail requested item_id=%d name=%r', item_id, item.get('name'))
                        await self._send(
                            writer,
                            item_detail_frame(item),
                            cipher=game_cipher,
                            lock=send_lock,
                        )
                    else:
                        LOG.info('item detail requested for unknown item_id=%d', item_id)
                elif message_id == 1009 and active_role is not None and values:
                    action = int(values[0])
                    if action in STRENGTHENING_ACTIONS:
                        response_frames = self.handle_strengthening_request(active_role, values)
                        LOG.info(
                            'weapon strengthening request action=%d values=%r response_count=%d',
                            action,
                            values,
                            len(response_frames),
                        )
                        await self._send(
                            writer,
                            *response_frames,
                            cipher=game_cipher,
                            lock=send_lock,
                        )
                        continue
                    item_id = int(values[1]) if len(values) > 1 else 0
                    item = find_item(active_role, item_id)
                    if action == 82 and item is not None:
                        await self._send(
                            writer,
                            item_description_frame(item),
                            cipher=game_cipher,
                            lock=send_lock,
                        )
                    elif action == 3 and item is not None and item_action_location_valid(action, item):
                        previous_appearance = character_appearance(active_role, self.settings.item_registry)
                        role_items(active_role).remove(item)
                        self.roles.save()
                        LOG.info('item discarded item_id=%d name=%r', item_id, item.get('name'))
                        replies = [encode_frame(1009, [short(3), integer(item_id)])]
                        appearance_frame = character_appearance_change_frame(active_role, previous_appearance, self.settings.item_registry)
                        if appearance_frame is not None:
                            replies.append(appearance_frame)
                        await self._send(writer, *replies, cipher=game_cipher, lock=send_lock)
                    elif action == 4 and item is not None and item_action_location_valid(action, item):
                        resolved_item = self.settings.item_registry.resolve(item)
                        mount_model = resolved_item.get('mount_model')
                        if mount_model:
                            current_mount = int(active_role.get('mount_model', 0))
                            next_mount = 0 if item.get('location') == 'equipped' or current_mount else int(mount_model)
                            item['location'] = 'equipped' if next_mount else 'bag'
                            active_role['mount_model'] = next_mount
                            self.roles.save()
                            LOG.info(
                                'mount %s item_id=%d model=%d',
                                'equipped' if next_mount else 'unequipped',
                                item_id,
                                next_mount,
                            )
                            replies = [
                                item_frame(item, operation=3),
                                encode_frame(1009, [short(4)]),
                                mount_update_frame(active_role),
                            ]
                            await self._send(writer, *replies, cipher=game_cipher, lock=send_lock)
                            continue
                        quantity = max(0, int(item.get('quantity', 1)) - 1)
                        item['quantity'] = quantity
                        item['last_heal'] = int(resolved_item.get('heal', 0))
                        replies = [item_frame(item, operation=3), encode_frame(1009, [short(4)])]
                        if quantity == 0:
                            role_items(active_role).remove(item)
                            replies.insert(1, encode_frame(1009, [short(3), integer(item_id)]))
                        self.roles.save()
                        LOG.info('item used item_id=%d name=%r remaining=%d', item_id, resolved_item.get('name'), quantity)
                        await self._send(writer, *replies, cipher=game_cipher, lock=send_lock)
                    elif (
                        action == 5
                        and item is not None
                        and is_equipment(item)
                        and item_action_location_valid(action, item)
                    ):
                        resolved_item = self.settings.item_registry.resolve(item)
                        mount_model = resolved_item.get('mount_model')
                        if mount_model:
                            updates: list[bytes] = []
                            for equipped in role_items(active_role):
                                resolved_equipped = self.settings.item_registry.resolve(equipped)
                                if (
                                    equipped is not item
                                    and equipped.get('location') == 'equipped'
                                    and resolved_equipped.get('mount_model')
                                ):
                                    equipped['location'] = 'bag'
                                    updates.append(item_frame(equipped, operation=3))
                            item['location'] = 'equipped'
                            active_role['mount_model'] = int(mount_model)
                            updates.extend([
                                item_frame(item, operation=3),
                                encode_frame(1009, [short(5)]),
                                mount_update_frame(active_role),
                            ])
                            self.roles.save()
                            LOG.info('mount equipped item_id=%d model=%d slot=%d', item_id, int(mount_model), MOUNT_EQUIPMENT_SLOT)
                            await self._send(writer, *updates, cipher=game_cipher, lock=send_lock)
                            continue
                        updates: list[bytes] = []
                        previous_appearance = character_appearance(active_role, self.settings.item_registry)
                        slot = item_slot(item, self.settings.item_registry)
                        for equipped in role_items(active_role):
                            if (
                                equipped is not item
                                and equipped.get('location') == 'equipped'
                                and item_slot(equipped, self.settings.item_registry) == slot
                            ):
                                equipped['location'] = 'bag'
                                updates.append(item_frame(equipped, operation=3))
                        item['location'] = 'equipped'
                        updates.append(item_frame(item, operation=3))
                        updates.append(encode_frame(1009, [short(5)]))
                        appearance_frame = character_appearance_change_frame(active_role, previous_appearance, self.settings.item_registry)
                        updates.append(
                            appearance_frame
                            if appearance_frame is not None
                            else equipment_panel_refresh_frame(active_role, self.settings.item_registry)
                        )
                        self.roles.save()
                        LOG.info('item equipped item_id=%d name=%r slot=%d', item_id, resolved_item.get('name'), slot)
                        await self._send(writer, *updates, cipher=game_cipher, lock=send_lock)
                    elif action == 6 and item is not None and item_action_location_valid(action, item):
                        previous_appearance = character_appearance(active_role, self.settings.item_registry)
                        if not try_move_item_to_bag(active_role, item):
                            LOG.info(
                                'item unequip rejected full_bag item_id=%d occupied=%d capacity=%d',
                                item_id,
                                bag_item_count(active_role),
                                bag_capacity(active_role),
                            )
                            await self._send(
                                writer,
                                top_message_frame('背包已满，无法卸下装备'),
                                cipher=game_cipher,
                                lock=send_lock,
                            )
                            continue
                        resolved_item = self.settings.item_registry.resolve(item)
                        mount_model = resolved_item.get('mount_model')
                        if mount_model:
                            active_role['mount_model'] = 0
                            self.roles.save()
                            LOG.info('mount unequipped item_id=%d model=0 slot=%d', item_id, MOUNT_EQUIPMENT_SLOT)
                            await self._send(
                                writer,
                                item_frame(item, operation=3),
                                encode_frame(1009, [short(6)]),
                                mount_update_frame(active_role),
                                cipher=game_cipher,
                                lock=send_lock,
                            )
                            continue
                        self.roles.save()
                        LOG.info('item unequipped item_id=%d name=%r', item_id, item.get('name'))
                        replies = [item_frame(item, operation=3), encode_frame(1009, [short(6)])]
                        appearance_frame = character_appearance_change_frame(active_role, previous_appearance, self.settings.item_registry)
                        replies.append(
                            appearance_frame
                            if appearance_frame is not None
                            else equipment_panel_refresh_frame(active_role, self.settings.item_registry)
                        )
                        await self._send(writer, *replies, cipher=game_cipher, lock=send_lock)
                    else:
                        LOG.info('ignored item action=%d item_id=%d values=%r', action, item_id, values)

                elif message_id == 1067 and len(fields) >= 3 and fields[0].type_id == TYPE_BYTE:
                    if is_mall_category_request(fields) or is_mall_title_request(fields):
                        tab_mode = int(values[2])
                        shop = self.settings.shop_registry.find_bk_mode(tab_mode)
                        if shop is None:
                            LOG.info(
                                'SHOP_OPEN_REJECT user=%r reason=unknown_mall_mode mode=%d',
                                username,
                                tab_mode,
                            )
                        else:
                            current_shop_mode = MALL_TAB_TO_DP_MODE[tab_mode]
                            current_shop_category = 0
                            LOG.info(
                                'SHOP_OPEN user=%r role_id=%d mode=%d currency_property=%d',
                                username,
                                int(active_role.get('id', 0)) if active_role is not None else 0,
                                current_shop_mode,
                                shop.currency_property,
                            )
                            if is_mall_category_request(fields):
                                await self._send(
                                    writer,
                                    mall_category_list_frame(shop.categories),
                                    cipher=game_cipher,
                                    lock=send_lock,
                                )
                            else:
                                await self._send(
                                    writer,
                                    mall_title_frame(shop.name),
                                    cipher=game_cipher,
                                    lock=send_lock,
                                )
                    elif is_mall_open_category_request(fields):
                        shop = self.settings.shop_registry.by_mode(current_shop_mode)
                        category_id = int(values[2])
                        if shop is None or shop.category(category_id) is None:
                            LOG.info(
                                'SHOP_CATEGORY_REJECT user=%r mode=%d category_id=%d',
                                username,
                                current_shop_mode,
                                category_id,
                            )
                        else:
                            current_shop_category = category_id
                            LOG.info(
                                'SHOP_CATEGORY user=%r mode=%d category_id=%d',
                                username,
                                current_shop_mode,
                                category_id,
                            )
                            # The client drops 1067 action-1 responses; the
                            # screen-7 shop page opens only via this bridge.
                            await self._send(
                                writer,
                                shop_screen_bridge_frame(current_shop_mode),
                                cipher=game_cipher,
                                lock=send_lock,
                            )
                    else:
                        LOG.info('ignored mall message=%d values=%r', message_id, values)

                elif message_id == 1033 and is_shop_list_request(fields):
                    shop = self.settings.shop_registry.by_mode(current_shop_mode)
                    category = (
                        shop.category(current_shop_category) if shop is not None else None
                    )
                    if active_role is None or shop is None or category is None:
                        LOG.info(
                            'SHOP_LIST_REJECT user=%r mode=%d category=%d reason=no_mall_session',
                            username,
                            current_shop_mode,
                            current_shop_category,
                        )
                    elif int(values[0]) != shop.shop_id:
                        LOG.info(
                            'SHOP_LIST_REJECT user=%r shop_id=%d expected=%d reason=shop_mismatch',
                            username,
                            int(values[0]),
                            shop.shop_id,
                        )
                    else:
                        LOG.info(
                            'SHOP_LIST user=%r mode=%d category=%d count=%d',
                            username,
                            current_shop_mode,
                            current_shop_category,
                            len(category.goods),
                        )
                        await self._send(
                            writer,
                            shop_goods_list_frame(
                                shop, category, self.settings.item_registry
                            ),
                            cipher=game_cipher,
                            lock=send_lock,
                        )

                elif message_id == 1033 and is_shop_purchase_request(fields):
                    if active_role is None:
                        LOG.info(
                            'SHOP_PURCHASE_REJECT user=%r reason=no_active_role',
                            username,
                        )
                    else:
                        shop = self.settings.shop_registry.by_mode(current_shop_mode)
                        if shop is None:
                            LOG.info(
                                'SHOP_PURCHASE_REJECT user=%r reason=no_mall_session',
                                username,
                            )
                        else:
                            item_id = int(fields[2].value)
                            quantity = int(fields[3].value)
                            goods = shop.find_goods(
                                current_shop_category, item_id
                            )
                            price = goods.price if goods is not None else 0
                            currencies = active_role.get('currencies')
                            balance_before = normalized_currency_balance(
                                (currencies or {}).get(shop.currency_name)
                            )
                            LOG.info(
                                'SHOP_PURCHASE_REQUEST user=%r shop_id=%d mode=%d '
                                'item_id=%d quantity=%d price=%d total=%d',
                                username,
                                shop.shop_id,
                                current_shop_mode,
                                item_id,
                                quantity,
                                price,
                                price * quantity,
                            )
                            result = self.handle_shop_purchase(
                                active_role,
                                fields,
                                mode=current_shop_mode,
                                category_id=current_shop_category,
                            )
                            if result.changed:
                                currencies_after = active_role.get('currencies')
                                LOG.info(
                                    'SHOP_PURCHASE_SUCCESS user=%r role_id=%d '
                                    'item_id=%d quantity=%d currency_property=%d '
                                    'currency_before=%d currency_after=%d',
                                    username,
                                    int(active_role.get('id', 0)),
                                    item_id,
                                    quantity,
                                    shop.currency_property,
                                    balance_before,
                                    normalized_currency_balance(
                                        (currencies_after or {}).get(shop.currency_name)
                                    ),
                                )
                                await self._send(writer, *result.frames, cipher=game_cipher, lock=send_lock)
                            else:
                                LOG.info(
                                    'SHOP_PURCHASE_REJECT user=%r item_id=%d quantity=%d reason=%s',
                                    username,
                                    item_id,
                                    quantity,
                                    result.reason or 'unknown',
                                )

                elif message_id == 1143 and active_role is not None and fields:
                    action = int(fields[0].value) if fields[0].type_id == TYPE_BYTE else -1
                    if is_life_trainer_list_request(fields):
                        trainer_id = int(fields[1].value)
                        trainer = self.settings.life_registry.trainers.get(trainer_id)
                        if trainer is None:
                            LOG.info(
                                'LIFE_SKILL_LEARN_REJECT user=%r trainer_id=%d reason=unknown_trainer',
                                username,
                                trainer_id,
                            )
                        else:
                            LOG.info(
                                'LIFE_SKILL_LEARN_LIST user=%r role_id=%d trainer_id=%d count=%d',
                                username,
                                int(active_role.get('id', 0)),
                                trainer_id,
                                len(trainer.entry_ids),
                            )
                            await self._send(
                                writer,
                                life_learnable_list_frame(trainer, active_role, self.settings),
                                cipher=game_cipher,
                                lock=send_lock,
                            )
                    elif is_life_learnable_detail_request(fields):
                        entry = self.settings.life_registry.learnable.get(int(fields[1].value))
                        if entry is None:
                            LOG.info(
                                'LIFE_SKILL_LEARN_REJECT user=%r reason=unknown_entry id=%d',
                                username,
                                int(fields[1].value),
                            )
                        else:
                            await self._send(
                                writer,
                                life_learnable_detail_frame(entry),
                                cipher=game_cipher,
                                lock=send_lock,
                            )
                    elif is_life_learn_request(fields):
                        entry_id = int(fields[1].value)
                        entry = self.settings.life_registry.learnable.get(entry_id)
                        trainer = next(
                            (
                                candidate for candidate in self.settings.life_registry.trainers.values()
                                if candidate.teaches(entry_id)
                            ),
                            None,
                        )
                        LOG.info(
                            'LIFE_SKILL_LEARN_REQUEST user=%r role_id=%d entry_id=%d',
                            username,
                            int(active_role.get('id', 0)),
                            entry_id,
                        )
                        result = self.handle_life_learn(
                            active_role, fields, trainer_id=trainer.trainer_id if trainer else 0,
                        )
                        if result.changed:
                            LOG.info(
                                'LIFE_SKILL_LEARN_SUCCESS user=%r role_id=%d entry_id=%d skill_id=%d',
                                username,
                                int(active_role.get('id', 0)),
                                entry_id,
                                entry.skill_id if entry is not None else 0,
                            )
                            await self._send(
                                writer,
                                *result.frames,
                                life_trainer_page_frame(trainer),
                                cipher=game_cipher,
                                lock=send_lock,
                            )
                        else:
                            LOG.info(
                                'LIFE_SKILL_LEARN_REJECT user=%r entry_id=%d reason=%s',
                                username,
                                entry_id,
                                result.reason or 'unknown',
                            )
                            # Failure must still clear the APK wait state: the
                            # router only clears it when a 1143 frame arrives,
                            # so echo the unchanged row (confirmed wire shape).
                            if entry is not None and trainer is not None:
                                await self._send(
                                    writer,
                                    life_learn_result_frame(0, entry, False, entry),
                                    cipher=game_cipher,
                                    lock=send_lock,
                                )
                    elif is_life_craft_detail_request(fields):
                        recipe = self.settings.life_registry.recipe(int(fields[1].value))
                        if recipe is None:
                            LOG.info(
                                'LIFE_CRAFT_REJECT user=%r recipe_id=%d reason=unknown_recipe',
                                username,
                                int(fields[1].value),
                            )
                        else:
                            LOG.info(
                                'LIFE_CRAFT_OPEN user=%r role_id=%d recipe_id=%d',
                                username,
                                int(active_role.get('id', 0)),
                                recipe.recipe_id,
                            )
                            await self._send(
                                writer,
                                life_craft_detail_frame(recipe, active_role, self.settings),
                                life_craft_text_frame(recipe.description),
                                cipher=game_cipher,
                                lock=send_lock,
                            )
                    elif is_life_craft_request(fields) or is_life_direct_use_request(fields):
                        recipe_id = int(fields[1].value)
                        if is_life_direct_use_request(fields):
                            slots = [0, 0, 0, 0]
                            quantity = 1
                        else:
                            slots = [int(field.value) for field in fields[2:6]]
                            quantity = int(fields[6].value)
                        recipe = self.settings.life_registry.recipe(recipe_id)
                        LOG.info(
                            'LIFE_CRAFT_REQUEST user=%r role_id=%d recipe_id=%d quantity=%d vitality=%d',
                            username,
                            int(active_role.get('id', 0)),
                            recipe_id,
                            quantity,
                            life_vitality(active_role),
                        )
                        result = self.handle_life_craft(active_role, fields) if (
                            is_life_craft_request(fields)
                        ) else LifeTransactionResult((), False, '该配方不支持直接使用')
                        if result.changed:
                            LOG.info(
                                'LIFE_CRAFT_SUCCESS user=%r role_id=%d recipe_id=%d '
                                'vitality=%d proficiency=%d',
                                username,
                                int(active_role.get('id', 0)),
                                recipe_id,
                                life_vitality(active_role),
                                int((life_skill_state(active_role, recipe.skill_id) or {}).get('proficiency', 0))
                                if recipe is not None else 0,
                            )
                            await self._send(writer, *result.frames, cipher=game_cipher, lock=send_lock)
                        else:
                            LOG.info(
                                'LIFE_CRAFT_REJECT user=%r recipe_id=%d reason=%s',
                                username,
                                recipe_id,
                                result.reason or 'unknown',
                            )
                            # The APK craft handler has no failure branch; the
                            # confirmed action-6 text channel reports the
                            # reason and the empty action-5 ack rescans the bag.
                            await self._send(
                                writer,
                                life_craft_text_frame(result.reason or '无法制造'),
                                life_craft_ack_frame(),
                                cipher=game_cipher,
                                lock=send_lock,
                            )
                    elif is_life_craft_text_request(fields):
                        recipe = self.settings.life_registry.recipe(int(fields[1].value))
                        text = recipe.description if recipe is not None else ''
                        await self._send(
                            writer,
                            life_craft_text_frame(text),
                            cipher=game_cipher,
                            lock=send_lock,
                        )
                    else:
                        LOG.info('ignored life skill message=%d values=%r', message_id, values)

                elif message_id == 2027 and is_gather_start_request(fields) and active_role is not None:
                    target_id = int(fields[1].value)
                    target = self.settings.life_registry.gather_target(target_id)
                    reason = (
                        gather_start_check(
                            active_role,
                            target,
                            gathering.session is not None,
                            self.settings.life_registry,
                        )
                        if target is not None
                        else '采集目标不存在'
                    )
                    if reason:
                        LOG.info(
                            'GATHER_REJECT user=%r target_id=%d reason=%s',
                            username,
                            target_id,
                            reason,
                        )
                        await self._send(writer, gather_interrupt_frame(), cipher=game_cipher, lock=send_lock)
                    elif int(active_role.get('map_id', self.settings.default_map_id)) != int(target.map_id):
                        LOG.info(
                            'GATHER_REJECT user=%r target_id=%d reason=wrong_map',
                            username,
                            target_id,
                        )
                        await self._send(writer, gather_interrupt_frame(), cipher=game_cipher, lock=send_lock)
                    else:
                        frames, session = gathering.start(active_role, target, int(target.map_id))
                        if session is None:
                            LOG.info(
                                'GATHER_REJECT user=%r target_id=%d reason=already_gathering',
                                username,
                                target_id,
                            )
                            await self._send(writer, gather_interrupt_frame(), cipher=game_cipher, lock=send_lock)
                        else:
                            LOG.info(
                                'GATHER_START user=%r role_id=%d target_id=%d duration=%d stamina=%d',
                                username,
                                int(active_role.get('id', 0)),
                                target_id,
                                int(target.duration_seconds),
                                life_stamina(active_role),
                            )
                            task = asyncio.create_task(self._finish_gathering_later(
                                writer,
                                game_cipher,
                                send_lock,
                                username=username,
                                active_role=active_role,
                                gathering=gathering,
                                session=session,
                                target=target,
                                delay=max(0.0, float(target.duration_seconds)),
                            ))
                            gathering.task = task
                            await self._send(writer, *frames, cipher=game_cipher, lock=send_lock)

                elif message_id == 1145 and is_map_pathfind_request(fields) and active_role is not None:
                    map_id = int(fields[1].value)
                    target_x = int(fields[2].value)
                    target_y = int(fields[3].value)
                    current_map = int(active_role.get('map_id', self.settings.default_map_id))
                    known = any(
                        target.map_id == map_id and target.x == target_x and target.y == target_y
                        for target in self.settings.life_registry.gather_targets
                    )
                    if map_id != current_map or not known:
                        LOG.info(
                            'GATHER_REJECT user=%r pathfind map=%d tile=%d,%d reason=unknown_target',
                            username,
                            map_id,
                            target_x,
                            target_y,
                        )
                    else:
                        await self._send(
                            writer,
                            map_pathfind_frame(map_id, target_x, target_y),
                            cipher=game_cipher,
                            lock=send_lock,
                        )

                elif message_id == 1084 and fields and fields[0].type_id == TYPE_BYTE:
                    # 1084 forging: the C->S request shapes are APK-confirmed
                    # but the S->C recipe-list record semantics are not fully
                    # locked, so no response is fabricated (see
                    # docs/protocol/life-skills.md). Requests are validated
                    # and logged only.
                    action = int(fields[0].value)
                    if is_forge_list_request(fields):
                        LOG.info('FORGE_OPEN user=%r context=%d', username, int(fields[1].value))
                    elif is_forge_select_request(fields):
                        LOG.info('FORGE_REQUEST user=%r recipe_id=%d', username, int(fields[1].value))
                    elif is_forge_collect_request(fields):
                        LOG.info(
                            'FORGE_REQUEST user=%r recipe_id=%d slots=%r kind=collect',
                            username,
                            int(fields[1].value),
                            [int(field.value) for field in fields[2:]],
                        )
                    elif is_forge_confirm_request(fields):
                        LOG.info(
                            'FORGE_REQUEST user=%r recipe_id=%d slots=%r kind=confirm',
                            username,
                            int(fields[1].value),
                            [int(field.value) for field in fields[2:]],
                        )
                    else:
                        LOG.info('ignored forge message=%d values=%r', message_id, values)

                elif message_id == 1054 and is_logout_page_request(fields):
                    # APK logout step 1: open the logout confirmation page.
                    LOG.info('logout page requested user=%r', username)
                    await self._send(
                        writer,
                        logout_page_frame(),
                        cipher=game_cipher,
                        lock=send_lock,
                    )

                elif message_id == 1003 and is_logout_confirm_request(fields):
                    # APK logout step 2: clean logout. Persist any position
                    # change that has not been checkpointed yet, then ack.
                    if position_dirty:
                        self.roles.save()
                        position_dirty = False
                        last_position_checkpoint_at = time.monotonic()
                        if active_role is not None:
                            LOG.info(
                                'ROLE_POSITION_LOGOUT_SAVE '
                                'user=%r role_id=%d map=%d tile=%d,%d',
                                username,
                                int(active_role.get('id', 0)),
                                int(active_role.get('map_id', self.settings.default_map_id)),
                                int(active_role.get('map_x', 0)),
                                int(active_role.get('map_y', 0)),
                            )
                    LOG.info(
                        'ROLE_LOGOUT_ACK user=%r role_id=%d',
                        username,
                        int(active_role.get('id', 0)) if active_role is not None else 0,
                    )
                    # Keep the loop alive after the ack: the original APK
                    # waits about one second, cleans up role/UI state, then
                    # closes the connection itself. Never break/return/close
                    # here; the finally block only runs on real disconnect.
                    await self._send(
                        writer,
                        logout_ack_frame(),
                        cipher=game_cipher,
                        lock=send_lock,
                    )

                else:
                    LOG.info('ignored unimplemented message=%d values=%r', message_id, values)
        except (asyncio.IncompleteReadError, ConnectionResetError):
            LOG.info('client disconnected: %s', peer)
        except (ProtocolError, UnicodeDecodeError, ValueError) as exc:
            LOG.warning('protocol error from %s: %s', peer, exc)
        finally:
            # Cancel any active gather; the socket is closing so the 2027
            # interrupt frame must NOT be sent.
            gathering.cancel()
            if position_dirty:
                try:
                    self.roles.save()
                    if active_role is not None:
                        LOG.info(
                            'ROLE_POSITION_DISCONNECT_SAVE '
                            'user=%r role_id=%d map=%d tile=%d,%d',
                            username,
                            int(active_role.get('id', 0)),
                            int(active_role.get('map_id', self.settings.default_map_id)),
                            int(active_role.get('map_x', 0)),
                            int(active_role.get('map_y', 0)),
                        )
                    position_dirty = False
                except OSError as exc:
                    LOG.error(
                        'ROLE_POSITION_SAVE_FAILED user=%r peer=%s error=%s',
                        username,
                        peer,
                        exc,
                    )
            if heartbeat_task is not None:
                heartbeat_task.cancel()
                with contextlib.suppress(asyncio.CancelledError):
                    await heartbeat_task
            writer.close()
            try:
                await writer.wait_closed()
            except (ConnectionResetError, OSError):
                pass


async def run(settings: Settings) -> None:
    handler = LocalGameServer(settings)
    server = await asyncio.start_server(handler.handle, settings.host, settings.port)
    addresses = ', '.join(str(sock.getsockname()) for sock in server.sockets or [])
    LOG.info('listening on %s; advertising %s:%d', addresses, settings.advertise_host, settings.port)
    async with server:
        await server.serve_forever()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Piao Miao San Jie 2 local login/game prototype')
    parser.add_argument('--config', type=Path, default=Path(__file__).with_name('config.json'))
    parser.add_argument('--host')
    parser.add_argument('--port', type=int)
    parser.add_argument('--advertise-host')
    parser.add_argument('--server-name')
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    settings = Settings.load(args.config)
    for name in ('host', 'port', 'advertise_host', 'server_name'):
        value = getattr(args, name)
        if value is not None:
            setattr(settings, name, value)
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    try:
        asyncio.run(run(settings))
    except KeyboardInterrupt:
        LOG.info('server stopped')


if __name__ == '__main__':
    main()
