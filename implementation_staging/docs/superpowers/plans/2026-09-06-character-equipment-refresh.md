# Character Equipment Refresh Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 修复登录选角人物预览，并让装备、卸下和强化后的人物外观、人物属性面板与战斗属性立即从当前装备状态同步。

**Architecture:** `character_appearance()` 保持人物外观唯一来源；新增装备属性汇总作为人物属性与战斗属性的共同来源；所有装备状态变化集中调用 `character_equipment_refresh_frames()` 下发完整 1017 与 1039/action=1。1080 登录角色记录直接从同一外观状态构造。

**Tech Stack:** Python 3 标准库、项目 TLV 协议编码器、unittest、GitHub Actions。

**Spec:** `implementation_staging/docs/superpowers/specs/2026-09-06-character-equipment-refresh-design.md`

## Global Constraints

- 直接修改 `master`，不创建 PR。
- 保持协议字段类型和消息号不变。
- 不修改 APK，不改存档结构，不覆盖 `data/roles.json`。
- `equipment_attributes[2]/[3]` 没有证据时不赋予新语义。
- 自动测试与静态协议验证不能冒充真机验收。

---

### Task 1: 1080 登录人物预览

**Files:**
- Modify: `implementation_staging/server.py`
- Test: `implementation_staging/tests/test_character_equipment_refresh.py`

**Interfaces:**
- Consumes: `character_appearance(role, registry) -> dict[int, int]`
- Produces: `role_list(settings, roles) -> bytes`，单角色记录固定 15 字段。

- [ ] **Step 1: Write the failing test**

验证 `role_list()` 的 field1=level、field2=property7、field7..14=property2/property14..20，而不是 `race/level/role.stats`。

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m unittest tests.test_character_equipment_refresh.CharacterEquipmentRefreshTests.test_role_list_uses_apk_appearance_contract_not_role_stats -v`
Expected: FAIL，因为旧实现仍把 race/level/stats 写入这些位置。

- [ ] **Step 3: Write minimal implementation**

将 `role_list()` 改为从 `character_appearance()` 读取 property7、2、14..20，并保持 S->C action 为 SHORT、count 为 BYTE、记录字段为既有类型。

- [ ] **Step 4: Run test to verify it passes**

Run: 同 Step 2。
Expected: PASS。

### Task 2: 装备属性唯一计算源

**Files:**
- Modify: `implementation_staging/server.py`
- Test: `implementation_staging/tests/test_character_equipment_refresh.py`

**Interfaces:**
- Produces: `equipped_attribute_totals(role, registry=None) -> tuple[int,int,int,int]`
- Produces: `effective_character_stats(role, registry=None) -> list[int]`
- Updates: `combat_stats(role, registry=None) -> CombatStats`

- [ ] **Step 1: Write failing tests**

验证只有 `equipped` 装备被汇总；attribute[0] 同时影响人物显示攻击来源与战斗攻击，attribute[1] 同时影响人物显示防御来源与战斗防御。

- [ ] **Step 2: Verify RED**

Run focused test file before production patch; expected missing helper/import or incorrect values.

- [ ] **Step 3: Implement minimal shared aggregation**

遍历当前角色物品，仅汇总已装备装备实例的四个 `equipment_attributes`；人物/战斗只消费已确认的前两项语义。

- [ ] **Step 4: Verify GREEN**

Run focused test file; expected PASS。

### Task 3: 统一实时刷新链

**Files:**
- Modify: `implementation_staging/server.py`
- Test: `implementation_staging/tests/test_character_equipment_refresh.py`
- Test: `implementation_staging/tests/test_strengthening.py`

**Interfaces:**
- Produces: `character_equipment_refresh_frames(role, registry=None) -> tuple[bytes, bytes]`

- [ ] **Step 1: Write failing test**

验证 1017 包含完整当前外观及人物属性，第二帧为 1039/action=1；装备状态改变后 `character_panel_frames()` 立即反映当前属性。

- [ ] **Step 2: Verify RED**

Run focused tests before patch; expected helper不存在或属性不变化。

- [ ] **Step 3: Implement refresh helper and wire mutations**

装备、卸下、丢弃装备和强化 changed 分支统一追加 `character_equipment_refresh_frames()`；游戏过程中不重发 1006。

- [ ] **Step 4: Verify focused tests**

Run `test_character_equipment_refresh.py`、`test_strengthening.py` 及装备外观映射测试。

### Task 4: 回归与清理

**Files:**
- Delete after successful run: `.github/scripts/apply_character_panel_refresh.py`
- Delete after successful run: `.github/workflows/diag-character-refresh.yml`
- Delete after successful run: temporary apply workflow

- [ ] **Step 1: Run syntax and diff checks**

Run: `python -m py_compile server.py` and `git diff --check`.

- [ ] **Step 2: Run affected regression suite**

Run focused refresh, strengthening, inventory and appearance mapping tests.

- [ ] **Step 3: Run full unittest discovery**

Run: `python -m unittest discover -s tests -v` and record exact pass/fail summary; pre-existing unrelated failures must be reported separately, not hidden.

- [ ] **Step 4: Commit production patch and clean temporary CI helpers**

Commit production `server.py` + focused test, then remove diagnostic/apply workflow helpers from final tree.
