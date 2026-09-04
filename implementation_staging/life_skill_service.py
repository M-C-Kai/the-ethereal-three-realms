"""Life skill business layer: learn / upgrade / craft / gathering rewards.

Pure-transaction functions.  server.py stays responsible for parsing,
TLV guards, session state, persistence and sending; every mutation here
goes through explicit before-values so a failed RoleStore.save() can roll
the whole role back (the boundary snapshots with copy.deepcopy).

Frame builders for the 1132 skill container records also live here so
both server.py and this module share one wire representation.
"""
from __future__ import annotations

from dataclasses import dataclass

from life_skill_registry import (
    GatherTargetDefinition,
    LearnableEntryDefinition,
    LifeRecipeDefinition,
    LifeSkillDefinition,
    LifeSkillRegistry,
    LifeSkillTrainerDefinition,
)

# Wire constants (docs/protocol/life-skills.md).
SKILL_RECORD_WIDTH = 14
PROGRESS_RECORD_WIDTH = 10
PROFICIENCY_BIT = 1


# ---------------------------------------------------------------------------
# Player state (role['life_skills']) — the single persisted truth mapped to
# properties 55..58 by server.player_info.  Never persisted anywhere else.
# ---------------------------------------------------------------------------
def ensure_life_skills(
    role: dict[str, object],
    registry: LifeSkillRegistry | None = None,
) -> dict[str, object]:
    """Migrate an old role to the minimal life-skill state (idempotent)."""
    state = role.get('life_skills')
    if isinstance(state, dict):
        state.setdefault('skills', {})
        state.setdefault('learned_recipes', [])
        return state
    stamina_max = registry.stamina_max if registry is not None else 100
    vitality_max = registry.vitality_max if registry is not None else 100
    state = {
        'stamina': stamina_max,
        'stamina_max': stamina_max,
        'vitality': vitality_max,
        'vitality_max': vitality_max,
        'skills': {},
        'learned_recipes': [],
    }
    role['life_skills'] = state
    return state


def life_stamina(role: dict[str, object]) -> int:
    return max(0, int(role.get('life_skills', {}).get('stamina', 0)))  # type: ignore[union-attr]


def life_stamina_max(role: dict[str, object]) -> int:
    return max(0, int(role.get('life_skills', {}).get('stamina_max', 0)))  # type: ignore[union-attr]


def life_vitality(role: dict[str, object]) -> int:
    return max(0, int(role.get('life_skills', {}).get('vitality', 0)))  # type: ignore[union-attr]


def life_vitality_max(role: dict[str, object]) -> int:
    return max(0, int(role.get('life_skills', {}).get('vitality_max', 0)))  # type: ignore[union-attr]


def life_skill_state(role: dict[str, object], skill_id: int) -> dict[str, object] | None:
    state = role.get('life_skills', {}).get('skills', {}).get(str(skill_id))  # type: ignore[union-attr]
    return state if isinstance(state, dict) else None


def life_skill_record(
    skill: LifeSkillDefinition,
    state: dict[str, object] | None,
) -> list[object]:
    """Build one 14-field 1132 action-0 skill container record."""
    if state is None:
        state = {'level': 0, 'proficiency': 0}
    level = int(state.get('level', 0))
    proficiency = int(state.get('proficiency', 0))
    return [
        skill.name,
        int(skill.skill_id),
        level,
        int(skill.max_level),
        proficiency,
        int(skill.upgrade_proficiency_required),
        PROFICIENCY_BIT,
        int(skill.icon),
        *(0 for _ in range(SKILL_RECORD_WIDTH - 8)),
    ]


def life_progress_record(
    skill: LifeSkillDefinition,
    state: dict[str, object] | None,
) -> list[object]:
    """Build one 10-field 1132 action-4 proficiency record."""
    if state is None:
        state = {'level': 0, 'proficiency': 0}
    return [
        skill.name,
        int(skill.skill_id),
        int(state.get('level', 0)),
        int(skill.max_level),
        int(state.get('proficiency', 0)),
        int(skill.upgrade_proficiency_required),
        PROFICIENCY_BIT,
        int(skill.icon),
        0,
        0,
    ]


# ---------------------------------------------------------------------------
# Transaction results
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class LifeTransactionResult:
    frames: tuple[bytes, ...]
    changed: bool
    reason: str = ''


def _rejected(reason: str) -> LifeTransactionResult:
    return LifeTransactionResult((), False, reason)


def _server_helpers():
    """Deferred import: server.py imports this module at load time."""
    from server import (
        allocate_item_instance_id,
        bag_capacity,
        bag_item_count,
        character_appearance_frame,
        ensure_weapon_base_attributes,
        item_frame,
        role_items,
    )
    return {
        'allocate_item_instance_id': allocate_item_instance_id,
        'bag_capacity': bag_capacity,
        'bag_item_count': bag_item_count,
        'character_appearance_frame': character_appearance_frame,
        'ensure_weapon_base_attributes': ensure_weapon_base_attributes,
        'item_frame': item_frame,
        'role_items': role_items,
    }


def _normalized_currency_balance(value: object) -> int:
    from server import normalized_currency_balance
    return normalized_currency_balance(value)


def _encode_proficiency_frame(
    role: dict[str, object],
    skill: LifeSkillDefinition,
    state: dict[str, object] | None,
) -> bytes:
    from protocol import byte, encode_frame, integer, string
    record = life_progress_record(skill, state)
    return encode_frame(1132, [
        byte(4),
        byte(1),
        string(record[0]),
        *(integer(int(value)) for value in record[1:]),
    ])


def _material_instances(
    role: dict[str, object],
    recipe: LifeRecipeDefinition,
    slots: list[int],
    quantity: int,
    helpers,
) -> tuple[list[dict[str, object]], dict[int, int], str]:
    """Validate the four client slot instance ids and plan deductions.

    Returns (ordered instances to draw from, per-template totals, reason).
    The client sends item *instance* ids (b/j.e); the server re-validates
    every one against the role inventory and the recipe's template ids.
    """
    slot_templates, _used, _free = recipe.material_slots()
    role_items = helpers['role_items']
    planned: list[dict[str, object]] = []
    needed: dict[int, int] = {}
    for index in range(4):
        template_id, per_craft = slot_templates[index]
        instance_id = int(slots[index]) if index < len(slots) else 0
        if template_id <= 0:
            continue
        needed[template_id] = needed.get(template_id, 0) + per_craft * quantity
        if instance_id <= 0:
            continue
        instance = next(
            (
                item for item in role_items(role)
                if int(item.get('id', 0)) == instance_id
                and item.get('location', 'bag') == 'bag'
            ),
            None,
        )
        if instance is None:
            return [], {}, '材料物品不存在'
        if int(instance.get('template_id', 0)) != template_id:
            return [], {}, '材料种类不符'
        if instance not in planned:
            planned.append(instance)
    # Top up the deduction pool with other stacks of the same templates so a
    # partially filled selection still satisfies the server-side totals.
    for template_id in needed:
        for item in role_items(role):
            if (
                item.get('location', 'bag') == 'bag'
                and int(item.get('template_id', 0)) == template_id
                and item not in planned
            ):
                planned.append(item)
    for template_id, total in needed.items():
        available = sum(
            int(item.get('quantity', 0))
            for item in planned
            if int(item.get('template_id', 0)) == template_id
        )
        if available < total:
            return [], {}, '材料数量不足'
    return planned, needed, ''


def _plan_output_slots(
    role: dict[str, object],
    template_id: int,
    units: int,
    item_registry,
    helpers,
) -> str:
    """Verify the bag can hold `units` of template_id; '' when possible."""
    definition = item_registry.require(template_id)
    max_quantity = int(definition.max_quantity)
    role_items = helpers['role_items']
    occupied = 0
    if max_quantity > 1:
        room = 0
        for item in role_items(role):
            if (
                item.get('location', 'bag') == 'bag'
                and int(item.get('template_id', 0)) == template_id
            ):
                room += max_quantity - int(item.get('quantity', 0))
        occupied = -(-max(0, units - room) // max_quantity)
    else:
        occupied = units
    free = helpers['bag_capacity'](role) - helpers['bag_item_count'](role)
    if occupied > free:
        return '背包已满'
    return ''


def _grant_output_units(
    role: dict[str, object],
    template_id: int,
    units: int,
    item_registry,
    helpers,
) -> list[dict[str, object]]:
    """Add `units` of template_id to the bag, stacking where possible."""
    definition = item_registry.require(template_id)
    max_quantity = int(definition.max_quantity)
    role_items = helpers['role_items']
    touched: list[dict[str, object]] = []
    remaining = units
    if max_quantity > 1:
        for item in role_items(role):
            if remaining <= 0:
                break
            if (
                item.get('location', 'bag') == 'bag'
                and int(item.get('template_id', 0)) == template_id
                and int(item.get('quantity', 0)) < max_quantity
            ):
                space = max_quantity - int(item.get('quantity', 0))
                added = min(space, remaining)
                item['quantity'] = int(item.get('quantity', 0)) + added
                remaining -= added
                if item not in touched:
                    touched.append(item)
    while remaining > 0:
        quantity = min(max_quantity, remaining)
        instance = {
            'id': helpers['allocate_item_instance_id'](role),
            'template_id': int(template_id),
            'quantity': quantity,
            'location': 'bag',
        }
        role_items(role).append(instance)
        helpers['ensure_weapon_base_attributes'](instance, item_registry)
        remaining -= quantity
        touched.append(instance)
    return touched


def craft_result(
    role: dict[str, object],
    recipe: LifeRecipeDefinition | None,
    slots: list[int],
    quantity: int,
    life_registry: LifeSkillRegistry,
    item_registry,
) -> LifeTransactionResult:
    """Apply one 1143/action-5 craft transaction atomically."""
    helpers = _server_helpers()
    if recipe is None:
        return _rejected('配方不存在')
    if type(quantity) is not int or quantity < 1 or quantity > 99:
        return _rejected('制造数量非法')
    state = life_skill_state(role, recipe.skill_id)
    if state is None:
        return _rejected('尚未学习该生活技能')
    if int(state.get('level', 0)) < recipe.required_level:
        return _rejected('生活技能等级不足')
    learned = role.get('life_skills', {}).get('learned_recipes', [])  # type: ignore[union-attr]
    if recipe.recipe_id not in learned:
        return _rejected('尚未学习该配方')
    vitality_cost = recipe.vitality_cost * quantity
    if life_vitality(role) < vitality_cost:
        return _rejected('活力不足')

    planned, needed, reason = _material_instances(role, recipe, slots, quantity, helpers)
    if reason:
        return _rejected(reason)

    total_output = recipe.output_quantity * quantity
    reason = _plan_output_slots(role, recipe.output_template_id, total_output, item_registry, helpers)
    if reason:
        return _rejected(reason)

    skill = life_registry.skills[recipe.skill_id]
    # ---- apply ----
    role['life_skills']['vitality'] = life_vitality(role) - vitality_cost  # type: ignore[union-attr]
    state['proficiency'] = int(state.get('proficiency', 0)) + recipe.proficiency_gain * quantity
    frames: list[bytes] = []
    consumed_instances: list[int] = []
    for template_id, total in needed.items():
        remaining = total
        for instance in planned:
            if remaining <= 0:
                break
            if int(instance.get('template_id', 0)) != template_id:
                continue
            available = int(instance.get('quantity', 0))
            if available <= 0:
                continue
            used = min(available, remaining)
            instance['quantity'] = available - used
            remaining -= used
            if instance['quantity'] <= 0:
                consumed_instances.append(int(instance['id']))
            else:
                frames.append(helpers['item_frame'](instance))
    for instance_id in consumed_instances:
        role['items'] = [  # type: ignore[assignment]
            item for item in helpers['role_items'](role)
            if int(item.get('id', 0)) != instance_id
        ]
        from protocol import encode_frame, integer, short
        frames.append(encode_frame(1009, [short(3), integer(instance_id)]))
    outputs = _grant_output_units(
        role, recipe.output_template_id, total_output, item_registry, helpers,
    )
    for output in outputs:
        frames.append(helpers['item_frame'](output))
    frames.append(
        helpers['character_appearance_frame'](
            int(role.get('id', 0)), {57: life_vitality(role)},
        )
    )
    frames.append(_encode_proficiency_frame(role, skill, state))
    from protocol import byte, encode_frame
    frames.append(encode_frame(1143, [byte(5)]))
    return LifeTransactionResult(tuple(frames), True, '')


def learn_result(
    role: dict[str, object],
    trainer: LifeSkillTrainerDefinition | None,
    entry: LearnableEntryDefinition | None,
    life_registry: LifeSkillRegistry,
) -> LifeTransactionResult:
    """Apply one 1143/action-3 trainer learn transaction atomically."""
    helpers = _server_helpers()
    if entry is None:
        return _rejected('学习条目不存在')
    if trainer is None or not trainer.teaches(entry.entry_id):
        return _rejected('导师上下文不符')
    if life_skill_state(role, entry.skill_id) is not None:
        return _rejected('已学习该技能')
    if max(1, int(role.get('level', 1))) < entry.level_requirement:
        return _rejected('等级不足')
    currencies = role.get('currencies')
    if not isinstance(currencies, dict):
        currencies = {}
        role['currencies'] = currencies
    silver = _normalized_currency_balance(currencies.get('silver'))
    if silver < entry.silver_cost:
        return _rejected('银两不足')
    experience = max(0, int(role.get('experience', 0)))
    if experience < entry.experience_cost:
        return _rejected('经验不足')

    skill = life_registry.skills[entry.skill_id]
    currencies['silver'] = silver - entry.silver_cost
    role['experience'] = experience - entry.experience_cost
    ensure_life_skills(role, life_registry)['skills'][str(entry.skill_id)] = {
        'level': 1,
        'proficiency': 0,
    }
    learned = ensure_life_skills(role, life_registry)['learned_recipes']  # type: ignore[union-attr]
    for recipe in life_registry.recipes.values():
        if recipe.skill_id == entry.skill_id and recipe.recipe_id not in learned:
            learned.append(recipe.recipe_id)

    frames = [
        _encode_proficiency_frame(role, skill, life_skill_state(role, entry.skill_id)),
        helpers['character_appearance_frame'](
            int(role.get('id', 0)),
            {50: silver - entry.silver_cost,
             31: experience - entry.experience_cost,
             85: (experience - entry.experience_cost) >> 32},
        ),
        learn_result_frame(0, entry, True, None),
    ]
    return LifeTransactionResult(tuple(frames), True, '')


def learn_result_frame(
    page: int,
    entry: LearnableEntryDefinition,
    learned: bool,
    next_entry: LearnableEntryDefinition | None,
) -> bytes:
    """1143 action 3: result 0 removes the row; non-zero replaces it."""
    from protocol import byte, encode_frame, integer, string
    fields: list[object] = [byte(3), byte(page), integer(entry.entry_id)]
    if learned or next_entry is None:
        fields.append(integer(0))
    else:
        fields.append(integer(1))
        fields.extend([
            integer(next_entry.entry_id),
            integer(0),
            integer(next_entry.level_requirement),
            integer(next_entry.silver_cost),
            integer(next_entry.experience_cost),
            string(next_entry.display),
            string(next_entry.detail),
        ])
    return encode_frame(1143, fields)  # type: ignore[arg-type]


def upgrade_result(
    role: dict[str, object],
    skill: LifeSkillDefinition,
    life_registry: LifeSkillRegistry,
) -> LifeTransactionResult:
    """Apply one 1132/action-6 skill upgrade transaction atomically."""
    helpers = _server_helpers()
    state = life_skill_state(role, skill.skill_id)
    if state is None:
        return _rejected('尚未学习该技能')
    level = int(state.get('level', 0))
    if level >= skill.max_level:
        return _rejected('已达等级上限')
    next_level = level + 1
    if int(state.get('proficiency', 0)) < skill.upgrade_proficiency_required:
        return _rejected('熟练度不足')
    if max(1, int(role.get('level', 1))) < skill.upgrade_required_role_level:
        return _rejected('角色等级不足')
    currencies = role.get('currencies')
    if not isinstance(currencies, dict):
        currencies = {}
        role['currencies'] = currencies
    silver = _normalized_currency_balance(currencies.get('silver'))
    silver_cost = skill.upgrade_silver_cost(next_level)
    if silver < silver_cost:
        return _rejected('银两不足')
    experience = max(0, int(role.get('experience', 0)))
    exp_cost = skill.upgrade_exp_cost(next_level)
    if experience < exp_cost:
        return _rejected('经验不足')

    currencies['silver'] = silver - silver_cost
    role['experience'] = experience - exp_cost
    state['level'] = next_level
    state['proficiency'] = 0
    frames = (
        helpers['character_appearance_frame'](
            int(role.get('id', 0)),
            {50: silver - silver_cost,
             31: experience - exp_cost,
             85: (experience - exp_cost) >> 32},
        ),
        _encode_proficiency_frame(role, skill, state),
    )
    return LifeTransactionResult(tuple(frames), True, '')


def gather_start_check(
    role: dict[str, object],
    target: GatherTargetDefinition,
    busy: bool,
    life_registry: LifeSkillRegistry,
) -> str:
    """Validate a 2027 gather start; '' when allowed, else the reason."""
    if busy:
        return '已有进行中的采集'
    state = life_skill_state(role, target.skill_id)
    if state is None:
        return '尚未学习对应生活技能'
    if int(state.get('level', 0)) < target.required_level:
        return '生活技能等级不足'
    if life_stamina(role) < target.stamina_cost:
        return '体力不足'
    return ''


def gathering_reward_result(
    role: dict[str, object],
    target: GatherTargetDefinition,
    life_registry: LifeSkillRegistry,
    item_registry,
) -> LifeTransactionResult:
    """Apply one gather completion: stamina, proficiency and the reward."""
    helpers = _server_helpers()
    skill = life_registry.skills[target.skill_id]
    state = life_skill_state(role, target.skill_id)
    if state is None:
        return _rejected('尚未学习对应生活技能')

    role['life_skills']['stamina'] = life_stamina(role) - target.stamina_cost  # type: ignore[union-attr]
    state['proficiency'] = int(state.get('proficiency', 0)) + target.proficiency_gain
    outputs = _grant_output_units(
        role, target.reward_template_id, target.reward_quantity, item_registry, helpers,
    )
    frames: list[bytes] = [helpers['item_frame'](output) for output in outputs]
    frames.append(
        helpers['character_appearance_frame'](
            int(role.get('id', 0)), {55: life_stamina(role)},
        )
    )
    frames.append(_encode_proficiency_frame(role, skill, state))
    from protocol import encode_frame, integer, byte
    frames.append(encode_frame(2027, [byte(3), integer(target.target_id)]))
    return LifeTransactionResult(tuple(frames), True, '')
