# Battle System Consolidation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将当前散落在 `server.py`、`server_pets.py`、`battle_escape_guard.py` 和协议测试中的战斗逻辑拆分为独立 `battle` 子系统，同时保持当前 APK 协议与真机行为不变。

**Architecture:** 新增 `battle` 包，按状态、协议、回合引擎、遭遇生命周期、奖励、资源六个职责拆分。`server.py` 保留网络循环和薄适配，`server_pets.py` 只负责识别移动 Boss 地图事件，不再 monkey-patch 战斗内部状态。迁移期间 `server.py` 允许兼容 re-export 旧函数名，保证调用方逐步迁移。

**Tech Stack:** Python 3 标准库、`unittest`、现有 TLV `protocol.py`、现有本地兼容服。

**Spec:** `implementation_staging/docs/superpowers/specs/2026-09-12-battle-system-consolidation-design.md`

## Global Constraints

- 仅整理本地兼容服，不修改官方/第三方服务。
- 不修改 APK，不发明新协议字段。
- 保持 1040/1041/1042/1048/1049 已确认字段顺序和 byte/short/int 类型。
- 逃跑仍为 C→S 1041 command=6；成功 S→C `1041 [INT 10, INT player_id]`。
- 逃跑不发胜利奖励、不移除怪物。
- 胜利仍在动作 ACK 后结束战斗并结算奖励。
- Boss 游荡属于地图系统；战斗系统只决定是否进入战斗及战斗生命周期。
- 每个迁移步骤先加/迁移测试，再改实现。
- Windows 最终验证命令：`D:\python\python.exe -m unittest discover -s tests -v`。
- 网络流最终验证命令：`D:\python\python.exe test_client.py --host 127.0.0.1 --port 6805 --exercise-role-crud`。

---

### Task 1: 建立 battle 包并迁移战斗状态与逃跑保护

**Files:**
- Create: `implementation_staging/battle/__init__.py`
- Create: `implementation_staging/battle/state.py`
- Modify: `implementation_staging/server.py`
- Modify: `implementation_staging/server_pets.py`
- Delete after compatibility migration: `implementation_staging/battle_escape_guard.py`
- Create: `implementation_staging/tests/battle/__init__.py`
- Create: `implementation_staging/tests/battle/test_state.py`
- Modify: `implementation_staging/tests/test_battle_escape_guard.py`

**Interfaces:**
- Produces: `CombatStats`, `LocalBattleState`, `CONTACT_RADIUS_TILES`, `RETRIGGER_TIMEOUT_SECONDS`.
- Produces methods on `LocalBattleState`: `begin()`, `finish()`, `reset_encounter()`, `escape()`, `should_suppress_retrigger(map_id, monster_id, now=None)`, `update_player_tile(x, y, now=None)`.
- `server.py` re-exports `CombatStats` and `LocalBattleState` during migration.

- [ ] **Step 1: Write failing state tests**

Create tests asserting: begin resets guard; escape stores map/monster/player/contact tile and monotonic timestamp; moving outside one-tile radius clears guard; staying inside does not; two-second timeout suppresses before deadline and permits after deadline.

- [ ] **Step 2: Run focused test and verify RED**

Run: `D:\python\python.exe -m unittest tests.battle.test_state -v`
Expected: FAIL because `battle.state` does not exist.

- [ ] **Step 3: Implement `battle/state.py`**

Move existing `CombatStats` / `LocalBattleState` behavior from `server.py`, fold `battle_escape_guard.py` policy into the state object, and keep existing field names so callers remain compatible.

- [ ] **Step 4: Replace battle-state monkey patches**

In `server_pets.py`, remove `_ORIGINAL_SET_ESCAPE_GUARD` and the three battle hook replacements. Calls needing guard behavior must use `LocalBattleState` methods directly.

- [ ] **Step 5: Add compatibility re-exports in `server.py`**

Use imports from `battle.state` instead of local duplicate definitions. Remove duplicate local implementations only after imports compile.

- [ ] **Step 6: Run focused tests**

Run: `D:\python\python.exe -m unittest tests.battle.test_state tests.test_battle_escape_guard -v`
Expected: PASS.

- [ ] **Step 7: Commit**

Commit message: `refactor: centralize battle state and escape guard`

---

### Task 2: 迁移战斗协议编码到 `battle/protocol.py`

**Files:**
- Create: `implementation_staging/battle/protocol.py`
- Modify: `implementation_staging/server.py`
- Create: `implementation_staging/tests/battle/test_protocol.py`
- Modify: `implementation_staging/tests/test_protocol.py`

**Interfaces:**
- Produces existing public names: `battle_reset_frame`, `battle_start_frame`, `battle_progress_frame`, `battle_end_frame`, `battle_escape_frame`, `battle_actor_frame`, `battle_actor_frames`, `battle_actor_update_frame`, `battle_action_frame`, `battle_action_show_frame`, `battle_move_frame`, `battle_reward_popup`, `is_player_escape_command`.
- All functions return exactly the same bytes as before.

- [ ] **Step 1: Move representative protocol assertions into new focused tests**

Cover 1040 action 0/1/2/4, 1041 escape result, 1042 action/effect layout, 1048 actor layout, 1049 reward popup. Assert message id, values and type ids.

- [ ] **Step 2: Run focused tests and verify RED**

Run: `D:\python\python.exe -m unittest tests.battle.test_protocol -v`
Expected: FAIL because `battle.protocol` does not exist.

- [ ] **Step 3: Move protocol-only builders**

Copy implementation without semantic changes. Dependencies may import `Field`/encoders and state data types, but must not import `LocalGameServer` or socket code.

- [ ] **Step 4: Re-export protocol helpers from `server.py`**

Replace local definitions with imports where safe; keep public names stable for legacy tests and callers.

- [ ] **Step 5: Remove duplicated battle protocol tests from monolithic test file**

Only remove tests now covered by `tests/battle/test_protocol.py`; leave non-battle protocol tests intact.

- [ ] **Step 6: Run focused tests**

Run: `D:\python\python.exe -m unittest tests.battle.test_protocol -v`
Expected: PASS.

- [ ] **Step 7: Commit**

Commit message: `refactor: extract battle protocol builders`

---

### Task 3: 统一 encounter 生命周期与所有开战入口

**Files:**
- Create: `implementation_staging/battle/encounter.py`
- Modify: `implementation_staging/server.py`
- Modify: `implementation_staging/server_pets.py`
- Create: `implementation_staging/tests/battle/test_encounter.py`
- Modify: `implementation_staging/tests/test_roaming_boss_interaction.py`

**Interfaces:**

```python
@dataclass(frozen=True)
class EncounterRequest:
    map_id: int
    monster_id: int
    player_id: int
    player_tile: tuple[int, int] | None
    monster_tile: tuple[int, int] | None
    source: str

@dataclass(frozen=True)
class EncounterDecision:
    start: bool
    suppressed: bool
    reason: str


def request_encounter(state: LocalBattleState, request: EncounterRequest, *, now: float | None = None) -> EncounterDecision: ...

def update_player_tile(state: LocalBattleState, x: int, y: int, *, now: float | None = None) -> bool: ...
```

- [ ] **Step 1: Add encounter tests**

Cover map interaction, q-action, proximity, active battle suppression, defeated monster suppression, escape guard under 2 seconds, leaving one-tile radius, two-second timeout.

- [ ] **Step 2: Verify RED**

Run: `D:\python\python.exe -m unittest tests.battle.test_encounter -v`
Expected: FAIL because encounter API does not exist.

- [ ] **Step 3: Implement encounter policy**

`request_encounter()` validates source, checks `active`, `monster_defeated`, and `state.should_suppress_retrigger()`. On start, set `state.map_id`, `state.contact_tile`, `state.player_tile`, then call `state.begin()` with caller-provided stats/monster set through the existing server integration path.

- [ ] **Step 4: Route 2031/1010 battle starts through encounter**

In `server.py`, replace duplicate suppress checks with one encounter call before `battle_state.begin()`.

- [ ] **Step 5: Route q-action/proximity through encounter**

In `server_pets.py`, keep q 2029 recognition and Boss tile tracking, but stop synthesizing policy. Produce a normalized battle-entry request through the shared encounter path. No battle-state monkey patch remains.

- [ ] **Step 6: Run focused tests**

Run: `D:\python\python.exe -m unittest tests.battle.test_encounter tests.test_roaming_boss_interaction -v`
Expected: PASS.

- [ ] **Step 7: Commit**

Commit message: `refactor: unify battle encounter lifecycle`

---

### Task 4: 迁移回合和伤害裁决到 `battle/engine.py`

**Files:**
- Create: `implementation_staging/battle/engine.py`
- Modify: `implementation_staging/server.py`
- Create: `implementation_staging/tests/battle/test_engine.py`
- Modify: `implementation_staging/tests/test_protocol.py`

**Interfaces:**
- Produces: `battle_command_target_id(values, state)`, player basic attack calculation, monster basic attack calculation, defence handling, round advancement decision helpers.
- Engine mutates/returns battle-domain state only; it does not encode frames or access sockets.

- [ ] **Step 1: Add focused engine tests**

Cover valid/invalid targets, damage floors, defence halving, monster/player death, and round advancement conditions.

- [ ] **Step 2: Verify RED**

Run: `D:\python\python.exe -m unittest tests.battle.test_engine -v`
Expected: FAIL because engine module does not exist.

- [ ] **Step 3: Move engine-only helpers**

Move current calculation/state-transition helpers without changing formulas.

- [ ] **Step 4: Replace server implementations with imports**

`server.py` keeps orchestration: decode command → call engine → ask protocol module for frames.

- [ ] **Step 5: Run focused tests**

Run: `D:\python\python.exe -m unittest tests.battle.test_engine -v`
Expected: PASS.

- [ ] **Step 6: Commit**

Commit message: `refactor: extract battle round engine`

---

### Task 5: 迁移奖励结算到 `battle/rewards.py`

**Files:**
- Create: `implementation_staging/battle/rewards.py`
- Modify: `implementation_staging/server.py`
- Create: `implementation_staging/tests/battle/test_rewards.py`
- Modify: `implementation_staging/tests/test_protocol.py`

**Interfaces:**
- Produces existing reward API names where practical: `apply_battle_rewards` plus battle reward constants/data result types.
- May accept shared callbacks/helpers for generic role level formula rather than importing whole server module.

- [ ] **Step 1: Add reward tests**

Cover experience increment, level-up transition, drop insertion, reward payload values, and no reward on escape path.

- [ ] **Step 2: Verify RED**

Run: `D:\python\python.exe -m unittest tests.battle.test_rewards -v`
Expected: FAIL because rewards module does not exist.

- [ ] **Step 3: Move reward logic without changing values**

Preserve current deterministic local reward values and persistence behavior.

- [ ] **Step 4: Rewire server settlement path**

Victory path calls `battle.rewards`; escape path never does.

- [ ] **Step 5: Run focused tests**

Run: `D:\python\python.exe -m unittest tests.battle.test_rewards -v`
Expected: PASS.

- [ ] **Step 6: Commit**

Commit message: `refactor: extract battle rewards`

---

### Task 6: 迁移战斗资源到 `battle/resources.py`

**Files:**
- Create: `implementation_staging/battle/resources.py`
- Modify: `implementation_staging/server.py`
- Create: `implementation_staging/tests/battle/test_resources.py`
- Modify: `implementation_staging/tests/test_protocol.py`

**Interfaces:**
- Produces: `BATTLE_RESOURCE_MODEL_OFFSET`, `BATTLE_RESOURCE_ALIASES`, `BATTLE_EMPTY_RESOURCE_IDS`, `battle_resource_path`, `battle_resource_resolution`, `battle_resource_frames`, `battle_image_resource`, `battle_image_frames`, related debug helpers.

- [ ] **Step 1: Add focused resource tests**

Cover model offset, aliases, empty role resource, image resolution and 1501/1503 response message/types.

- [ ] **Step 2: Verify RED**

Run: `D:\python\python.exe -m unittest tests.battle.test_resources -v`
Expected: FAIL because resources module does not exist.

- [ ] **Step 3: Move resource helpers**

Keep filesystem behavior and aliases unchanged.

- [ ] **Step 4: Re-export from server during compatibility period**

External test/debug callers keep working.

- [ ] **Step 5: Run focused tests**

Run: `D:\python\python.exe -m unittest tests.battle.test_resources -v`
Expected: PASS.

- [ ] **Step 6: Commit**

Commit message: `refactor: extract battle resources`

---

### Task 7: 清理兼容层、测试归档和完整验证

**Files:**
- Modify: `implementation_staging/server.py`
- Modify: `implementation_staging/server_pets.py`
- Delete if no remaining imports: `implementation_staging/battle_escape_guard.py`
- Modify: `implementation_staging/tests/test_protocol.py`
- Modify: `implementation_staging/tests/test_battle_escape_guard.py`
- Modify: `implementation_staging/tests/test_roaming_boss_interaction.py`
- Modify: `implementation_staging/APK_BATTLE_CATALOG.md`

**Interfaces:**
- `server.py` remains the network adapter and may retain deliberate re-exports only where still used externally.
- `server_pets.py` contains no battle method monkey patches.

- [ ] **Step 1: Search for duplicate battle implementations**

Search names moved in Tasks 1-6 and ensure there is one authoritative implementation per concern.

- [ ] **Step 2: Remove obsolete duplicate tests/files**

Delete only tests duplicated by the new battle suite; keep integration coverage.

- [ ] **Step 3: Update battle catalog architecture notes**

Document `battle/` ownership and the unchanged APK protocol evidence.

- [ ] **Step 4: Run battle suite**

Run: `D:\python\python.exe -m unittest discover -s tests/battle -v`
Expected: PASS.

- [ ] **Step 5: Run canonical unit suite**

Run: `D:\python\python.exe -m unittest discover -s tests -v`
Expected: PASS.

- [ ] **Step 6: Run local network integration**

Restart with the existing script, then run: `D:\python\python.exe test_client.py --host 127.0.0.1 --port 6805 --exercise-role-crud`
Expected: `OK` for existing integration flow.

- [ ] **Step 7: Physical-device regression checklist**

User verifies: Boss moves with attached foot ring; q menu can enter battle; approaching within one tile auto-enters; escape does not reward/remove Boss; leaving one tile or waiting two seconds permits re-entry; basic attack and victory settlement still render correctly.

- [ ] **Step 8: Commit**

Commit message: `refactor: complete battle subsystem consolidation`
