from __future__ import annotations

from protocol import Field, TYPE_BYTE, TYPE_INT, TYPE_SHORT, byte, encode_frame, integer, string
from systems.skill.registry import LifeSkillRegistry
from systems.skill.service import ensure_life_skills, learn_result_frame, life_progress_record, life_skill_record, life_skill_state

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


def life_skill_list_frame(role: dict[str, object], settings) -> bytes:
    """S->C 1132 action 0: life skill container list only.

    [compat] Screen 603 expects exactly 7 slots.  Current life skills are
    [compat] {2001, 2002, 2003, 2004} plus locked placeholders to fill to 7.
    Sect skills (e.g. 10001) are NO LONGER included here.
    """
    life_state = ensure_life_skills(role, settings.life_registry)
    records: list[list[object]] = []

    # Add real life skills
    for skill in settings.life_registry.skills.values():
        records.append(life_skill_record(
            skill, life_skill_state(role, skill.skill_id),
        ))

    # Add locked placeholders to reach 7 total records
    while len(records) < LIFE_SKILL_SCREEN_SLOTS:
        records.append([
            LIFE_SKILL_LOCKED_SLOT_NAME,
            LIFE_SKILL_LOCKED_SLOT_ID_BASE + len(records),
            *(0 for _ in range(SKILL_RECORD_WIDTH - 2)),
        ])

    if len(records) > LIFE_SKILL_SCREEN_SLOTS:
        raise ValueError(
            f'life skill screen supports at most {LIFE_SKILL_SCREEN_SLOTS} records'
        )

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


def life_proficiency_frame(role: dict[str, object], settings) -> bytes:
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
    settings,
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
    settings,
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
    settings,
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

# ---------------------------------------------------------------------------
# 打造（1084）请求判定（自 server.py 迁入）。
# ---------------------------------------------------------------------------
from protocol import Field, TYPE_BYTE, TYPE_INT, TYPE_SHORT

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


