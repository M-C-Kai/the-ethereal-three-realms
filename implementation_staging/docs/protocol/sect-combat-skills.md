# 战斗门派技能数据库

本目录建立的是七大门派战斗技能静态库，不与 `systems/skill` 的生活技能系统混用。

## 数据来源边界

- 技能名称与 1 级效果：用户提供的九游 2014 玩家评测整理资料。
- APK 参考：当前 APK 没有发现明文七门派技能数值表；仅用来确认客户端存在技能记录字段、学习/升级 UI、战斗快捷键限制、法力/生命不足、缴械、未装备剑/红符/黄符等使用限制提示。
- 技能 ID：本地兼容 ID，规则为 `skill_id = sect_id * 10000 + sequence`。官方原始技能 ID 仍未确认。
- 技能树前置：`relation_type = inferred_prerequisite` 为按技能效果与门派定位推导，不能当作官方前置关系。

## 文件

- `data/catalog/sect_combat_skill_catalog.bundle.json`：七大门派战斗技能数据库快照。
- `tools/materialize_sect_skill_catalog.py`：把 bundle 解包成普通 `sects.json`、`sect_skills.json`、`sect_skill_rules.json`。
- `systems/role/sect_skill_registry.py`：只读加载器和交叉引用校验。
- `tests/test_sect_skill_catalog.py`：静态库冒烟测试。

## 物化普通 JSON

默认不会覆盖当前旧目录文件。需要生成普通 JSON 时执行：

```bash
cd implementation_staging
python tools/materialize_sect_skill_catalog.py
```

会输出：

- `data/catalog/sects.json`
- `data/catalog/sect_skills.json`
- `data/catalog/sect_skill_rules.json`

## 主要逻辑表

### sect_skills

技能身份与展示字段。

关键字段：

- `skill_id`
- `sect_id`
- `name`
- `skill_kind`: `active` / `follow_up` / `teleport`
- `category`
- `damage_type`: `physical` / `magic` / `none`
- `element_type`
- `tree_line`
- `tree_order`
- `source`

### cast_rules

技能能否施放，以及对谁施放。

关键字段：

- `usable_in_battle`
- `usable_out_of_battle`
- `shortcut_scope`
- `target_side`
- `target_type`
- `target_count`
- `target_count_formula`
- `mp_cost`
- `hp_cost`
- `hp_percent_cost_bp`
- `max_hp_percent_cost_bp`
- `blocked_by_disarm`
- `required_weapon_type`
- `required_talisman_type`
- `pvp_allowed`
- `pve_allowed`

### effects

真正的技能结算单元。一个技能可以有多个效果。

关键字段：

- `phase`: `instant` / `turn_start` / `on_damaged` / `follow_up`
- `effect_type`: `damage` / `heal` / `revive` / `apply_status` / `cleanse` / `restore_mp` / `death_check` / `teleport`
- `target_selector`
- `stat_basis`
- `rate_bp`
- `flat_value`
- `chance_bp`
- `duration_rounds`
- `cannot_kill`
- `status_key`
- `params_json`

百分比统一使用 basis points：`10000 = 100%`，`9000 = 90%`，`2500 = 25%`。

## 后续接入战斗结算建议

后续不要在 `1041` 分支里硬编码每个技能，而是：

1. 从 `player_sect_skills` 判断角色是否学会技能。
2. 从 `cast_rules` 校验战斗内/外、目标、法力、生命、缴械、武器/符条件。
3. 用 `effects` 顺序结算伤害、治疗、状态、复活、净化。
4. 用 `scaling_rules` 处理武器品质、等级、叠层。
5. 用 `relations` 处理互斥姿态、后续技、延迟触发。
6. 最后统一输出 `1048` 战斗帧。
