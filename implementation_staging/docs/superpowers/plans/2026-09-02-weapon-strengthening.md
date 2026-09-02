# Weapon Strengthening Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the APK-native message-1009 weapon-strengthening flow with two 1,000-count stone stacks, persistent levels, deterministic attribute recalculation, material consumption, client refreshes, and the live `月华` role returned to Chang'an.

**Architecture:** Put all adjustable strengthening rules in a new standard-library-only `strengthening.py` module. Keep ownership validation, persistence, protocol encoding, and routing in `server.py`; expose one pure request-transition function so unit tests can inject deterministic RNG without opening a socket.

**Tech Stack:** Python 3 standard library, `unittest`, the existing typed-frame helpers in `protocol.py`, JSON `RoleStore` persistence.

**Spec:** `docs/superpowers/specs/2026-09-02-weapon-strengthening-design.md`

## Global Constraints

- Do not modify the APK, add a message ID, or change the existing 1008 field count/type layout.
- All strengthening requests and responses use message ID 1009 with the exact APK-confirmed byte/short/int/string types.
- Never send S→C action 92; finish an execution request with action 78.
- Only equipment slot 10 is strengthenable in this iteration.
- Template IDs `322260000` and `322261000`, both rate tables, multi-stone addition, and the attack-bonus table are explicitly local compatibility rules, not confirmed official values.
- Preserve `data/roles.json` and all pre-existing user edits in the dirty worktree.
- Do not start or restart `server.py`, connect to port 6805, install an APK, or perform device acceptance testing.
- Core server code remains standard-library-only.

## File Map

- Create `strengthening.py`: definitions, constants, rates, failure rule, attribute recalculation, injected-RNG success decision.
- Create `tests/test_strengthening.py`: pure rules, migration, transaction, persistence, and combat-impact tests.
- Modify `server.py`: item bootstrap/migration, text/frame builders, transition orchestration, 1009 routing, combat stat integration.
- Modify `tests/test_protocol.py`: exact request/response types and final frame ordering; retain the current uncommitted team/currency tests.
- Modify `PROTOCOL_LOCK.md`: record the locked 1009 layouts and label local rules.
- Modify `README.md`: document stone availability and the non-device verification boundary.
- Modify `data/roles.json`: add both 1,000-count stacks to account `1` role `10003` and move it to Chang'an `(60,67)`.
- Leave `protocol.py` and `data/roles.example.json` wire/schema structure unchanged unless a failing test proves an existing helper is insufficient.

---

### Task 1: Pure Strengthening Rule Module

**Files:**
- Create: `strengthening.py`
- Create: `tests/test_strengthening.py`

**Interfaces:**
- Consumes: plain item dictionaries containing `template_id`, `strengthen_level`, `equipment_attributes`, and optionally `base_equipment_attributes`.
- Produces:
  - `StrengtheningStoneDefinition(template_id: int, name: str, grade: str, success_rates: tuple[int, ...])`
  - `INITIAL_STRENGTHEN_STONE_TEMPLATE_ID: int`
  - `MIDDLE_STRENGTHEN_STONE_TEMPLATE_ID: int`
  - `STRENGTHENING_STONE_DEFINITIONS: dict[int, StrengtheningStoneDefinition]`
  - `stone_definition_for(item: dict[str, object]) -> StrengtheningStoneDefinition | None`
  - `is_strengthening_stone(item: dict[str, object]) -> bool`
  - `normalized_strengthen_level(item: dict[str, object]) -> int`
  - `rate_for(definition: StrengtheningStoneDefinition, level: int) -> int`
  - `total_strengthening_rate(per_stone_rate: int, count: int) -> int`
  - `strengthening_failure_level(level: int) -> int`
  - `recalculate_equipment_attributes(item: dict[str, object]) -> list[int]`
  - `strengthening_success(equipment: dict[str, object], definition: StrengtheningStoneDefinition, count: int, rng: object = random) -> bool`

- [ ] **Step 1: Write failing recognition and rate-table tests**

Add these tests to `tests/test_strengthening.py`:

```python
import unittest

from strengthening import (
    INITIAL_STRENGTHEN_STONE_TEMPLATE_ID,
    MIDDLE_STRENGTHEN_STONE_TEMPLATE_ID,
    STRENGTHENING_STONE_DEFINITIONS,
    is_strengthening_stone,
    rate_for,
    stone_definition_for,
    total_strengthening_rate,
)


class StrengtheningRuleTests(unittest.TestCase):
    def test_only_configured_apk_range_templates_are_strengthening_stones(self):
        self.assertTrue(is_strengthening_stone({'template_id': INITIAL_STRENGTHEN_STONE_TEMPLATE_ID}))
        self.assertTrue(is_strengthening_stone({'template_id': MIDDLE_STRENGTHEN_STONE_TEMPLATE_ID}))
        self.assertFalse(is_strengthening_stone({'template_id': 322_259_999}))
        self.assertFalse(is_strengthening_stone({'template_id': 322_261_003}))
        self.assertFalse(is_strengthening_stone({'template_id': 322_260_001}))

    def test_middle_rate_is_never_below_initial_and_all_levels_exist(self):
        initial = STRENGTHENING_STONE_DEFINITIONS[INITIAL_STRENGTHEN_STONE_TEMPLATE_ID]
        middle = STRENGTHENING_STONE_DEFINITIONS[MIDDLE_STRENGTHEN_STONE_TEMPLATE_ID]
        self.assertEqual(len(initial.success_rates), 9)
        self.assertEqual(len(middle.success_rates), 9)
        for level in range(9):
            self.assertGreaterEqual(rate_for(middle, level), rate_for(initial, level))

    def test_multi_stone_rate_caps_at_ten_thousand(self):
        self.assertEqual(total_strengthening_rate(1_200, 5), 6_000)
        self.assertEqual(total_strengthening_rate(8_500, 2), 10_000)
```

- [ ] **Step 2: Run the focused tests and verify RED**

Run:

```powershell
D:\python\python.exe -m unittest tests.test_strengthening.StrengtheningRuleTests -v
```

Expected: import failure because `strengthening.py` does not exist.

- [ ] **Step 3: Implement definitions and rate helpers**

Create `strengthening.py` with the exact local defaults:

```python
from __future__ import annotations

import random
from dataclasses import dataclass

INITIAL_STRENGTHEN_STONE_TEMPLATE_ID = 322_260_000
MIDDLE_STRENGTHEN_STONE_TEMPLATE_ID = 322_261_000
STRENGTHENING_STONE_TEMPLATE_MIN = 322_260_000
STRENGTHENING_STONE_TEMPLATE_MAX = 322_261_002
MAX_STRENGTHEN_LEVEL = 9
MAX_STRENGTHEN_STONE_COUNT = 5
WEAPON_STRENGTHEN_ATTACK_BONUSES = (0, 1, 2, 3, 5, 7, 10, 14, 19, 25)


@dataclass(frozen=True)
class StrengtheningStoneDefinition:
    template_id: int
    name: str
    grade: str
    success_rates: tuple[int, ...]


# Template IDs are a local compatibility mapping inside the APK-native
# accepted range. The old official name-to-ID relationship is not yet
# statically confirmed.
STRENGTHENING_STONE_DEFINITIONS = {
    INITIAL_STRENGTHEN_STONE_TEMPLATE_ID: StrengtheningStoneDefinition(
        INITIAL_STRENGTHEN_STONE_TEMPLATE_ID,
        '初级强化宝石',
        'initial',
        (2_000, 1_800, 1_600, 1_400, 1_200, 1_000, 800, 600, 400),
    ),
    MIDDLE_STRENGTHEN_STONE_TEMPLATE_ID: StrengtheningStoneDefinition(
        MIDDLE_STRENGTHEN_STONE_TEMPLATE_ID,
        '中级强化宝石',
        'middle',
        (2_500, 2_200, 2_000, 1_800, 1_600, 1_400, 1_200, 900, 600),
    ),
}
```

Implement lookup, range checking, rate lookup, and `min(10_000, per_stone_rate * count)` without embedding rate values elsewhere.

Place these comments beside the rate and socket rules:

```python
# Multiple-stone rate addition is a strong static inference from the APK's
# quantity-control algorithm, not a confirmed old-official probability rule.
# TODO: APK help confirms lucky socket creation during strengthening,
# but socket field/probability are not yet protocol-locked.
```

- [ ] **Step 4: Run recognition tests and verify GREEN**

Run the Step 2 command. Expected: three tests pass.

- [ ] **Step 5: Write failing failure-level, recalculation, and RNG tests**

Append:

```python
class FixedRng:
    def __init__(self, value: int):
        self.value = value

    def randrange(self, upper: int) -> int:
        if upper != 10_000:
            raise AssertionError(f'unexpected RNG upper bound: {upper}')
        return self.value


class StrengtheningStateRuleTests(unittest.TestCase):
    def test_failure_tiers_match_apk_help(self):
        expected = {0: 0, 1: 1, 2: 2, 3: 3, 4: 3, 5: 3, 6: 6, 7: 6, 8: 6}
        self.assertEqual({level: strengthening_failure_level(level) for level in expected}, expected)

    def test_weapon_attributes_recalculate_from_stable_base_without_drift(self):
        weapon = {
            'strengthen_level': 4,
            'base_equipment_attributes': [3, 0, 0, 0],
            'equipment_attributes': [999, 0, 0, 0],
        }
        self.assertEqual(recalculate_equipment_attributes(weapon), [8, 0, 0, 0])
        self.assertEqual(recalculate_equipment_attributes(weapon), [8, 0, 0, 0])

    def test_success_uses_injected_roll_and_total_rate(self):
        definition = stone_definition_for({'template_id': INITIAL_STRENGTHEN_STONE_TEMPLATE_ID})
        self.assertIsNotNone(definition)
        equipment = {'strengthen_level': 8}
        self.assertTrue(strengthening_success(equipment, definition, 1, rng=FixedRng(599)))
        self.assertFalse(strengthening_success(equipment, definition, 1, rng=FixedRng(600)))
```

Import `recalculate_equipment_attributes`, `strengthening_failure_level`, and `strengthening_success` in the test module.

- [ ] **Step 6: Run state-rule tests and verify RED**

Run:

```powershell
D:\python\python.exe -m unittest tests.test_strengthening.StrengtheningStateRuleTests -v
```

Expected: import/name failures for the three unimplemented helpers.

- [ ] **Step 7: Implement normalization, failure, recalculation, and injected RNG**

Implement level normalization as an integer-only clamp to `0..9`; booleans and malformed values become 0. `recalculate_equipment_attributes()` copies or normalizes four stable base shorts, adds only `WEAPON_STRENGTHEN_ATTACK_BONUSES[level]` to index 0, writes the resulting list back to `equipment_attributes`, and returns it. `strengthening_success()` calls `rng.randrange(10_000)` and compares the roll with the capped total rate.

- [ ] **Step 8: Run the complete new rule test module**

Run:

```powershell
D:\python\python.exe -m unittest tests.test_strengthening -v
```

Expected: all rule tests pass.

- [ ] **Step 9: Commit only the new isolated files**

```powershell
git add -- strengthening.py tests/test_strengthening.py
git commit -m "feat: add deterministic strengthening rules"
```

---

### Task 2: Stone Bootstrap and Equipment Schema Migration

**Files:**
- Modify: `server.py:590-1040`
- Modify: `tests/test_strengthening.py`

**Interfaces:**
- Consumes Task 1 constants, definitions, `is_strengthening_stone()`, `normalized_strengthen_level()`, and `recalculate_equipment_attributes()`.
- Produces:
  - `strengthening_stone_items(role_id: int) -> list[dict[str, object]]`
  - `strengthening_stones_initialized: bool` on roles
  - normalized `strengthen_level` and `base_equipment_attributes` on equipment items.

- [ ] **Step 1: Write failing bootstrap and idempotence tests**

Add this class to `tests/test_strengthening.py` (with `json`, `tempfile`, `Path`, `RoleStore`, `Settings`, `default_role`, and `role_items` imports):

```python
class StrengtheningBootstrapTests(unittest.TestCase):
    def test_new_role_receives_two_thousand_count_stone_stacks(self):
        role = default_role(Settings())
        stones = [item for item in role_items(role) if is_strengthening_stone(item)]
        self.assertTrue(role['strengthening_stones_initialized'])
        self.assertEqual(
            {(item['template_id'], item['quantity'], item['max_quantity'], item['location'], item['sort_group']) for item in stones},
            {
                (INITIAL_STRENGTHEN_STONE_TEMPLATE_ID, 1_000, 9_999, 'bag', 150),
                (MIDDLE_STRENGTHEN_STONE_TEMPLATE_ID, 1_000, 9_999, 'bag', 150),
            },
        )

    def test_legacy_bootstrap_is_once_only_and_preserves_quantity(self):
        with tempfile.TemporaryDirectory() as directory:
            role_path = Path(directory) / 'roles.json'
            role = default_role(Settings())
            role['items'] = [item for item in role['items'] if not is_strengthening_stone(item)]
            role.pop('strengthening_stones_initialized')
            role_path.write_text(json.dumps({'next_role_id': 10002, 'accounts': {'legacy': [role]}}, ensure_ascii=False), encoding='utf-8')
            settings = Settings(role_data_file=str(role_path))

            store = RoleStore(settings)
            migrated = store.roles_for('legacy')[0]
            stones = [item for item in role_items(migrated) if is_strengthening_stone(item)]
            self.assertEqual([item['quantity'] for item in stones], [1_000, 1_000])
            stones[0]['quantity'] = 321
            store.save()
            reloaded = RoleStore(settings).roles_for('legacy')[0]
            self.assertEqual(next(item for item in role_items(reloaded) if item['template_id'] == stones[0]['template_id'])['quantity'], 321)

            store = RoleStore(settings)
            stored_role = store.roles_for('legacy')[0]
            stored_role['items'] = [item for item in role_items(stored_role) if item['template_id'] != stones[0]['template_id']]
            store.save()
            final_role = RoleStore(settings).roles_for('legacy')[0]
            self.assertFalse(any(item['template_id'] == stones[0]['template_id'] for item in role_items(final_role)))
```

- [ ] **Step 2: Run bootstrap tests and verify RED**

Run the individual new test names with:

```powershell
D:\python\python.exe -m unittest tests.test_strengthening.StrengtheningBootstrapTests -v
```

Expected: failures because starter roles contain no strengthening stones or marker.

- [ ] **Step 3: Implement fixed-ID stone records and role marker**

Use role-derived instance IDs `(role_id * 100) + 18` and `+19`; retain `+17` for battle drops. Generate names from `STRENGTHENING_STONE_DEFINITIONS`, use icon 6109 as the existing verified generic local icon, `item_flags=0`, `action_flags=0`, `sort_order=18/19`, and the exact 1000/9999 counts.

Extend `starter_items()` with both records. Set `strengthening_stones_initialized=True` in both `default_role()` and `RoleStore.create()`.

In `_ensure_items()`:

- if the marker is absent/false, append missing fixed-ID stone records and set the marker true;
- if the marker is true, never recreate a missing stone;
- when a stone already exists, preserve its `quantity` and `location` while refreshing non-state metadata;
- never reset a consumed stack back to 1000.

- [ ] **Step 4: Run bootstrap tests and verify GREEN**

Run the Step 2 command. Expected: all bootstrap tests pass.

- [ ] **Step 5: Write failing equipment migration tests**

Add concrete migration cases:

```python
class StrengtheningMigrationTests(unittest.TestCase):
    def test_legacy_weapon_captures_base_and_defaults_to_level_zero(self):
        role = default_role(Settings())
        weapon = next(item for item in role_items(role) if item.get('equipment_slot') == 10)
        weapon.pop('base_equipment_attributes', None)
        weapon.pop('strengthen_level', None)
        RoleStore._ensure_items(role)
        self.assertEqual(weapon['base_equipment_attributes'], [3, 0, 0, 0])
        self.assertEqual(weapon['strengthen_level'], 0)
        self.assertEqual(weapon['equipment_attributes'], [3, 0, 0, 0])

    def test_level_four_reloads_from_base_without_attribute_drift(self):
        with tempfile.TemporaryDirectory() as directory:
            role_path = Path(directory) / 'roles.json'
            role = default_role(Settings())
            weapon = next(item for item in role_items(role) if item.get('equipment_slot') == 10)
            weapon['strengthen_level'] = 4
            weapon['base_equipment_attributes'] = [3, 0, 0, 0]
            weapon['equipment_attributes'] = [999, 0, 0, 0]
            role_path.write_text(json.dumps({'next_role_id': 10002, 'accounts': {'legacy': [role]}}, ensure_ascii=False), encoding='utf-8')
            loaded = RoleStore(Settings(role_data_file=str(role_path))).roles_for('legacy')[0]
            loaded_weapon = next(item for item in role_items(loaded) if item.get('equipment_slot') == 10)
            self.assertEqual(loaded_weapon['strengthen_level'], 4)
            self.assertEqual(loaded_weapon['base_equipment_attributes'], [3, 0, 0, 0])
            self.assertEqual(loaded_weapon['equipment_attributes'], [8, 0, 0, 0])
```

Add `subTest` inputs `True`, `'bad'`, `-1`, and `10` to prove malformed levels normalize to 0 rather than becoming Python integer aliases or out-of-range levels. Add a custom slot-10 item with instance ID outside starter IDs and assert `_ensure_items()` adds the same three schema fields without deleting it.

- [ ] **Step 6: Run migration tests and verify RED**

```powershell
D:\python\python.exe -m unittest tests.test_strengthening.StrengtheningMigrationTests -v
```

Expected: missing `base_equipment_attributes`/`strengthen_level` assertions fail.

- [ ] **Step 7: Implement schema migration without losing current state**

Before merging a default item over an existing item, preserve `strengthen_level`, `base_equipment_attributes`, `location`, `quantity`, and `last_heal`. If base attributes are missing, snapshot the pre-merge `equipment_attributes`. After catalog merging, normalize every ordinary equipment item and recalculate effective attributes. Do not treat mount slot 17 as a strengthenable weapon.

- [ ] **Step 8: Run migration, inventory, and existing item-layout tests**

```powershell
D:\python\python.exe -m unittest tests.test_strengthening.StrengtheningMigrationTests tests.test_inventory tests.test_protocol.ProtocolTests.test_item_records_match_original_client_layout tests.test_protocol.ProtocolTests.test_legacy_starter_items_migrate_to_complete_set -v
```

Expected: all selected tests pass; current 1008 field counts remain unchanged.

- [ ] **Step 9: Stage only this task's hunks if they do not include pre-existing edits**

Review with `git diff -- server.py tests/test_strengthening.py`. Use `git add -p server.py` to select only bootstrap/migration hunks and `git add tests/test_strengthening.py`; commit as `feat: persist strengthening inventory state`. If a hunk contains unrelated pre-existing code, leave that hunk uncommitted rather than absorbing user work.

---

### Task 3: Exact 1009 Strengthening Response Frames and UI Text

**Files:**
- Modify: `server.py:1614-1735`
- Modify: `tests/test_protocol.py`

**Interfaces:**
- Produces:
  - `item_display_name(item: dict[str, object]) -> str`
  - `item_display_description(item: dict[str, object]) -> str`
  - `strengthening_open_frame() -> bytes`
  - `strengthening_equipment_frame(equipment: dict[str, object]) -> bytes`
  - `strengthening_rate_frame(equipment: dict[str, object], definition: StrengtheningStoneDefinition) -> bytes`
  - `strengthening_stone_selection_frame(valid: bool) -> bytes`
  - `strengthening_reset_frame() -> bytes`

- [ ] **Step 1: Write failing exact-layout tests**

Add protocol tests using `decode_frame()`, `field_values()`, and `field.type_id`:

```python
def test_strengthening_open_and_equipment_frames_use_exact_fields(self):
    message_id, fields = decode_frame(strengthening_open_frame())
    self.assertEqual((message_id, field_values(fields)), (1009, [97, '请选择需要强化的装备和强化宝石。']))
    self.assertEqual([field.type_id for field in fields], [3, 6])

    weapon = next(item for item in role_items(default_role(Settings())) if item_slot(item) == 10)
    message_id, fields = decode_frame(strengthening_equipment_frame(weapon))
    self.assertEqual(message_id, 1009)
    self.assertEqual(field_values(fields)[0], 75)
    self.assertEqual([field.type_id for field in fields], [3, 6])

def test_strengthening_rate_selection_and_reset_frames_use_exact_fields(self):
    role = default_role(Settings())
    weapon = next(item for item in role_items(role) if item_slot(item) == 10)
    definition = STRENGTHENING_STONE_DEFINITIONS[INITIAL_STRENGTHEN_STONE_TEMPLATE_ID]

    message_id, fields = decode_frame(strengthening_rate_frame(weapon, definition))
    self.assertEqual(message_id, 1009)
    self.assertEqual(field_values(fields)[:2], [74, 10_000])
    self.assertEqual([field.type_id for field in fields], [3, 3, 6])

    _, fields = decode_frame(strengthening_stone_selection_frame(True))
    self.assertEqual(field_values(fields), [77, 1, 1])
    self.assertEqual([field.type_id for field in fields], [3, 2, 2])

    _, fields = decode_frame(strengthening_stone_selection_frame(False))
    self.assertEqual(field_values(fields), [77, 0])
    self.assertEqual([field.type_id for field in fields], [3, 2])

    _, fields = decode_frame(strengthening_reset_frame())
    self.assertEqual(field_values(fields), [78])
    self.assertEqual([field.type_id for field in fields], [3])

def test_strengthening_execution_request_reads_short_int_int_byte(self):
    request = encode_frame(1009, [short(92), integer(1000301), integer(1000318), byte(3)])
    message_id, fields = decode_frame(request)
    self.assertEqual(message_id, 1009)
    self.assertEqual(field_values(fields), [92, 1000301, 1000318, 3])
    self.assertEqual([field.type_id for field in fields], [3, 4, 4, 2])
```

- [ ] **Step 2: Run the two protocol tests and verify RED**

Expected: imports fail because frame builders do not exist.

- [ ] **Step 3: Implement exact frame builders**

Use only existing `short()`, `byte()`, `string()`, and `encode_frame()` helpers. The action 74 rate comes from `rate_for(definition, normalized_strengthen_level(equipment))`. Include weapon name, `+N`, and effective attack in action 75/74 text without adding fields.

- [ ] **Step 4: Run the two protocol tests and verify GREEN**

Run the exact test names with `D:\python\python.exe -m unittest ... -v`. Expected: pass.

- [ ] **Step 5: Write failing display-text tests**

Add this exact regression:

```python
def test_strengthening_level_uses_existing_item_text_fields_only(self):
    role = default_role(Settings())
    weapon = next(item for item in role_items(role) if item_slot(item) == 10)
    self.assertEqual(field_values(decode_frame(item_frame(weapon))[1])[8], '青锋剑')
    weapon['strengthen_level'] = 4
    weapon['base_equipment_attributes'] = [3, 0, 0, 0]
    recalculate_equipment_attributes(weapon)

    item_values = field_values(decode_frame(item_frame(weapon, operation=3))[1])
    self.assertEqual(item_values[8], '青锋剑 +4')
    self.assertEqual(len(item_values), 35)
    description = field_values(decode_frame(item_description_frame(weapon))[1])[2]
    detail = field_values(decode_frame(item_detail_frame(weapon))[1])[3]
    self.assertIn('强化 +4', description)
    self.assertIn('当前攻击：8', description)
    self.assertIn('强化 +4', detail)
```

- [ ] **Step 6: Implement display-only name/description helpers**

Change only the string values supplied to existing fields in `item_frame()`, `item_description_frame()`, and `item_detail_frame()`. Keep persisted `item['name']` unchanged and leave every field count and type untouched.

- [ ] **Step 7: Run display tests plus the full item-layout regression**

Expected: new display tests and `test_item_records_match_original_client_layout` pass.

- [ ] **Step 8: Stage only strengthening-related protocol hunks**

Use interactive staging for `server.py` and `tests/test_protocol.py`; do not stage the existing team/currency hunks. Commit as `feat: encode native strengthening responses` only if the selected index diff contains no unrelated changes.

---

### Task 4: Validated Strengthening Transaction and 1009 Router

**Files:**
- Modify: `server.py:3091-4200`
- Modify: `tests/test_strengthening.py`
- Modify: `tests/test_protocol.py`

**Interfaces:**
- Produces:
  - `StrengtheningActionResult(frames: tuple[bytes, ...], changed: bool, message: str)`
  - `strengthening_action_result(role: dict[str, object], values: list[object], rng: object = random) -> StrengtheningActionResult`
  - `STRENGTHENING_ACTIONS = {74, 75, 77, 92, 97}`

- [ ] **Step 1: Write failing read-only action tests**

Add a reusable fixture and explicit read-only assertions:

```python
def strengthening_fixture():
    role = default_role(Settings())
    weapon = next(item for item in role_items(role) if item.get('equipment_slot') == 10)
    initial = next(item for item in role_items(role) if item.get('template_id') == INITIAL_STRENGTHEN_STONE_TEMPLATE_ID)
    return role, weapon, initial


class StrengtheningActionTests(unittest.TestCase):
    def test_read_only_actions_return_native_frames_without_mutating_role(self):
        role, weapon, stone = strengthening_fixture()
        before = copy.deepcopy(role)
        cases = (
            ([97], [97]),
            ([75, weapon['id']], [75]),
            ([74, weapon['id'], stone['id']], [74, 10_000]),
        )
        for request, expected_prefix in cases:
            with self.subTest(action=request[0]):
                result = strengthening_action_result(role, request, rng=FixedRng(0))
                self.assertFalse(result.changed)
                values = field_values(decode_frame(result.frames[0])[1])
                self.assertEqual(values[:len(expected_prefix)], expected_prefix)
        self.assertEqual(role, before)

    def test_valid_action_77_is_silent_until_the_following_rate_response(self):
        role, weapon, stone = strengthening_fixture()
        result = strengthening_action_result(role, [77, weapon['id'], stone['id']])
        self.assertEqual(result.frames, ())

    def test_invalid_stone_selection_returns_status_zero(self):
        role, weapon, stone = strengthening_fixture()
        stone['location'] = 'warehouse'
        result = strengthening_action_result(role, [77, weapon['id'], stone['id']])
        self.assertEqual(field_values(decode_frame(result.frames[0])[1]), [77, 0])
        stone['location'] = 'bag'
        stone['template_id'] = 322_260_001
        result = strengthening_action_result(role, [77, weapon['id'], stone['id']])
        self.assertEqual(field_values(decode_frame(result.frames[0])[1]), [77, 0])
```

- [ ] **Step 2: Run read-only action tests and verify RED**

Expected: missing `StrengtheningActionResult`/transition function.

- [ ] **Step 3: Implement lookup and read-only transitions**

Resolve IDs only through `find_item(role, id)`. Weapon validation requires `is_equipment`, `item_slot==10`, and location in `{'bag','equipped'}`. Stone validation requires `location=='bag'`, configured definition, and positive quantity. Invalid action 77 returns `[77,0]`; invalid action 74 still returns `[74,0,error_text]`; invalid action 75 returns its normal two-field shape with an error string.

- [ ] **Step 4: Run read-only tests and verify GREEN**

Expected: pass without changing role data.

- [ ] **Step 5: Write failing execution tests one rule at a time**

Add these concrete tests, using `strengthening_fixture()`:

```python
def decoded_actions(frames):
    return [(message_id, field_values(fields)) for message_id, fields in map(decode_frame, frames)]


class StrengtheningExecutionTests(unittest.TestCase):
    def test_success_increments_level_consumes_count_and_ends_with_reset(self):
        role, weapon, stone = strengthening_fixture()
        result = strengthening_action_result(role, [92, weapon['id'], stone['id'], 2], rng=FixedRng(0))
        decoded = decoded_actions(result.frames)
        self.assertTrue(result.changed)
        self.assertEqual(weapon['strengthen_level'], 1)
        self.assertEqual(weapon['equipment_attributes'][0], 4)
        self.assertEqual(stone['quantity'], 998)
        self.assertEqual(decoded[0][0], 1008)
        self.assertEqual(decoded[0][1][0], 3)
        self.assertEqual(decoded[-1], (1009, [78]))
        self.assertFalse(any(message_id == 1009 and values and values[0] == 92 for message_id, values in decoded))

    def test_failure_levels_and_consumption_follow_apk_help(self):
        for starting_level, expected_level in ((2, 2), (4, 3), (7, 6)):
            with self.subTest(starting_level=starting_level):
                role, weapon, stone = strengthening_fixture()
                weapon['strengthen_level'] = starting_level
                weapon['base_equipment_attributes'] = [3, 0, 0, 0]
                recalculate_equipment_attributes(weapon)
                result = strengthening_action_result(role, [92, weapon['id'], stone['id'], 1], rng=FixedRng(9_999))
                self.assertTrue(result.changed)
                self.assertEqual(weapon['strengthen_level'], expected_level)
                self.assertEqual(stone['quantity'], 999)

    def test_invalid_execution_never_consumes_or_mutates(self):
        mutators = (
            lambda role, weapon, stone: [92, weapon['id'], stone['id'], 0],
            lambda role, weapon, stone: [92, weapon['id'], stone['id'], 6],
            lambda role, weapon, stone: [92, 999_999, stone['id'], 1],
            lambda role, weapon, stone: [92, weapon['id'], 999_999, 1],
        )
        for build_request in mutators:
            role, weapon, stone = strengthening_fixture()
            before = copy.deepcopy(role)
            result = strengthening_action_result(role, build_request(role, weapon, stone), rng=FixedRng(0))
            self.assertFalse(result.changed)
            self.assertEqual(role, before)
            self.assertEqual(decoded_actions(result.frames)[-1], (1009, [78]))

    def test_level_nine_and_insufficient_or_wrong_container_stones_are_rejected(self):
        for configure in (
            lambda weapon, stone: weapon.update(strengthen_level=9),
            lambda weapon, stone: weapon.update(equipment_slot=3),
            lambda weapon, stone: weapon.update(location='warehouse'),
            lambda weapon, stone: stone.update(quantity=0),
            lambda weapon, stone: stone.update(quantity=1),
            lambda weapon, stone: stone.update(location='warehouse'),
            lambda weapon, stone: stone.update(template_id=322_260_001),
        ):
            role, weapon, stone = strengthening_fixture()
            configure(weapon, stone)
            before = copy.deepcopy(role)
            count = 2 if stone.get('quantity') == 1 else 1
            result = strengthening_action_result(role, [92, weapon['id'], stone['id'], count], rng=FixedRng(0))
            self.assertFalse(result.changed)
            self.assertEqual(role, before)

    def test_zero_remaining_stack_uses_existing_update_then_delete_protocol(self):
        role, weapon, stone = strengthening_fixture()
        stone['quantity'] = 1
        stone_id = stone['id']
        result = strengthening_action_result(role, [92, weapon['id'], stone_id, 1], rng=FixedRng(0))
        decoded = decoded_actions(result.frames)
        self.assertNotIn(stone, role_items(role))
        self.assertIn((1009, [3, stone_id]), decoded)
        zero_update = next(values for message_id, values in decoded if message_id == 1008 and values[1] == stone_id)
        self.assertEqual((zero_update[0], zero_update[2]), (3, 0))
        self.assertEqual(decoded[-1], (1009, [78]))
```

- [ ] **Step 6: Run execution tests and verify RED**

Expected: action 92 is unimplemented and assertions fail without mutating fixtures.

- [ ] **Step 7: Implement atomic in-memory transition**

Parse action 92 indexes exactly as `values[1]=equipment_id`, `values[2]=stone_id`, `values[3]=count`. Complete every validation before mutation. On success, increment; on failure, call `strengthening_failure_level()`. Recalculate from base, decrement the stone, build its update before removing a zero stack, and return frames in this order:

```python
(
    item_frame(equipment, operation=3),
    item_frame(stone, operation=3),
    # encode_frame(1009, [short(3), integer(stone_id)]) only at zero,
    top_message_frame(result_text),
    strengthening_reset_frame(),
)
```

Invalid executions return `(top_message_frame(error), strengthening_reset_frame())` with `changed=False`.

- [ ] **Step 8: Run execution tests and verify GREEN**

Expected: all validation, consumption, downgrade, and ordering tests pass.

- [ ] **Step 9: Write a failing persistence-boundary test**

Add the persistence boundary test:

```python
def test_server_strengthening_transition_persists_level_attributes_and_stones(self):
    with tempfile.TemporaryDirectory() as directory:
        settings = Settings(role_data_file=str(Path(directory) / 'roles.json'))
        server = LocalGameServer(settings)
        role = server.roles.roles_for('persist')[0]
        weapon = next(item for item in role_items(role) if item.get('equipment_slot') == 10)
        stone = next(item for item in role_items(role) if item.get('template_id') == INITIAL_STRENGTHEN_STONE_TEMPLATE_ID)
        server.handle_strengthening_request(role, [92, weapon['id'], stone['id'], 2], rng=FixedRng(0))

        reloaded = RoleStore(settings).roles_for('persist')[0]
        reloaded_weapon = find_item(reloaded, weapon['id'])
        reloaded_stone = find_item(reloaded, stone['id'])
        self.assertEqual((reloaded_weapon['strengthen_level'], reloaded_weapon['equipment_attributes'][0]), (1, 4))
        self.assertEqual(reloaded_stone['quantity'], 998)
```

- [ ] **Step 10: Implement server persistence boundary and router branch**

Add `LocalGameServer.handle_strengthening_request()` that calls the pure transition and calls `self.roles.save()` exactly when `changed` is true. In the existing message-1009 branch, route `STRENGTHENING_ACTIONS` before the legacy item branches, send all returned frames, log the outcome, and `continue`. Do not alter the existing code paths for actions 3, 4, 5, 6, or 82.

- [ ] **Step 11: Run persistence and legacy 1009 regressions**

Run all strengthening tests plus the existing behavior tests
`test_item_actions_require_the_apk_location_they_operate_on`,
`test_item_records_match_original_client_layout`, and
`test_legacy_starter_items_migrate_to_complete_set`. The complete suite is
the regression gate for existing 1009 actions 3/4/5/6/82; do not add a
source-text grep test because it would not exercise observable behavior.

- [ ] **Step 12: Review and stage only transaction/router hunks**

Use `git diff` and interactive staging. Commit as `feat: execute native weapon strengthening` only when unrelated dirty hunks are excluded.

---

### Task 5: Make Strengthened Weapon Attack Affect Battle State

**Files:**
- Modify: `server.py:272-289`
- Modify: `tests/test_strengthening.py`
- Modify: `tests/test_protocol.py`

**Interfaces:**
- Produces `equipped_weapon_attack(role: dict[str, object]) -> int` and updates `combat_stats()` to add it to `physical_attack`.

- [ ] **Step 1: Write failing combat-impact tests**

Add this exact test:

```python
def test_only_equipped_weapon_effective_attack_contributes_to_battle(self):
    bag_role, bag_weapon, _ = strengthening_fixture()
    base_attack = combat_stats(bag_role).physical_attack

    equipped_role = copy.deepcopy(bag_role)
    equipped_weapon = next(item for item in role_items(equipped_role) if item.get('equipment_slot') == 10)
    equipped_weapon['location'] = 'equipped'
    self.assertEqual(combat_stats(equipped_role).physical_attack, base_attack + 3)

    strengthened_role = copy.deepcopy(bag_role)
    strengthened_weapon = next(item for item in role_items(strengthened_role) if item.get('equipment_slot') == 10)
    strengthened_weapon['location'] = 'equipped'
    strengthened_weapon['strengthen_level'] = 4
    strengthened_weapon['base_equipment_attributes'] = [3, 0, 0, 0]
    recalculate_equipment_attributes(strengthened_weapon)
    strengthened_stats = combat_stats(strengthened_role)
    self.assertEqual(strengthened_stats.physical_attack, base_attack + 8)

    state = LocalBattleState()
    state.begin(10001, 1900001, strengthened_stats)
    self.assertEqual(state.player_attack, base_attack + 8)
    self.assertEqual(state.player_basic_attack_damage(), base_attack + 8)
```

- [ ] **Step 2: Run the focused tests and verify RED**

Expected: current `combat_stats()` ignores all equipment, so equipped roles have equal attack.

- [ ] **Step 3: Implement equipped weapon contribution**

Scan `role_items(role)` for `location=='equipped'`, `is_equipment(item)`, and `item_slot(item)==10`; return the nonnegative first effective `equipment_attributes` value, otherwise zero. Add it once to the existing physical-attack formula. Do not change HP or defence formulas.

- [ ] **Step 4: Run combat-impact and existing battle-stat tests**

Run the new tests plus `test_character_panel_stats_drive_battle_hp_attack_and_defence`, `test_initial_battle_actor_uses_character_panel_max_hp`, and `test_attack_round_uses_panel_damage_in_state_and_wire_effects`. Adjust only fixtures whose weapon location unintentionally makes the new equipment contribution part of the expected result.

- [ ] **Step 5: Stage only combat-related hunks**

Interactive-stage the helper, formula line, and corresponding tests. Commit as `feat: apply strengthened weapon attack in battle` only without unrelated hunks.

---

### Task 6: Documentation, Live Role Adjustment, and Full Verification

**Files:**
- Modify: `PROTOCOL_LOCK.md`
- Modify: `README.md`
- Modify: `data/roles.json`
- Create locally (not commit): `data/roles.before-strengthening-20260902.json`

**Interfaces:**
- Consumes all previous tasks.
- Produces a verified role `account=1, id=10003` at map 58 `(60,67)` with two configured stone stacks of quantity 1000.

- [ ] **Step 1: Update protocol documentation**

Append a `## 武器强化协议` section to `PROTOCOL_LOCK.md` containing these exact contracts:

```text
C→S: 97=[short]; 75=[short,int]; 77/74=[short,int,int]; 92=[short,int,int,byte].
S→C: 97=[short,string]; 75=[short,string]; 74=[short,short,string];
77 valid=静默并等待紧接着的 74 响应，invalid=[short,byte(0)]；
[short,byte(1),byte(1)] 是清空两个选择槽的指令；78=[short].
S→C 不存在 action 92；事务以 1008 operation=3、现有删除动作和 action 78 收尾。
武器槽为 10；客户端材料模板范围为 322260000..322261002。
strengthen_level/base_equipment_attributes 仅为服务端持久化字段，不追加到 1008。
```

Immediately follow it with the spec's list of local compatibility values and this exact sentence:

`TODO: APK help confirms lucky socket creation during strengthening, but socket field/probability are not yet protocol-locked.`

- [ ] **Step 2: Update README local behavior**

Add this paragraph to README's inventory section:

```text
本地服现在通过 APK 原生“装备强化”菜单支持武器强化。新角色及首次迁移的旧角色各获得“初级强化宝石”和“中级强化宝石”1000 颗；发放带持久化标记，消耗完不会在登录时重复补发。本实现保持 1008 原布局，成功率和攻击奖励属于本地兼容数值。本轮只运行离线单元测试，没有启动/重启 6805，也没有代替用户进行真机验收。
```

- [ ] **Step 3: Back up and precisely edit the live role file**

Copy `data/roles.json` to `data/roles.before-strengthening-20260902.json` with `Copy-Item -LiteralPath`. Then use `apply_patch` against the unique account-`1` role block, not a full JSON reserialization, to make these exact changes:

- set `map_id=58`, `map_name='长安'`, `map_x=60`, `map_y=67`;
- add/update fixed instance IDs `1000318` and `1000319` with templates `322260000` and `322261000`, quantities 1000, maximums 9999, and bag metadata from `strengthening_stone_items(10003)`;
- set `strengthening_stones_initialized=true`;
- preserve every other role field and every test account.

After patching, parse the whole file with PowerShell `ConvertFrom-Json`. If parsing fails, restore the explicit backup with `Copy-Item -LiteralPath`; do not attempt partial repair of the 900KB JSON file.

- [ ] **Step 4: Verify live data invariants**

Run this read-only verification shape in PowerShell, filling no dynamic paths other than the two explicit files:

```powershell
$before = Get-Content -Raw data/roles.before-strengthening-20260902.json | ConvertFrom-Json
$after = Get-Content -Raw data/roles.json | ConvertFrom-Json
$beforeRoles = @($before.accounts.PSObject.Properties | ForEach-Object { @($_.Value) }).Count
$afterRoles = @($after.accounts.PSObject.Properties | ForEach-Object { @($_.Value) }).Count
if ($before.accounts.PSObject.Properties.Count -ne $after.accounts.PSObject.Properties.Count) { throw 'account count changed' }
if ($beforeRoles -ne $afterRoles) { throw 'role count changed' }
$role = @($after.accounts.'1') | Where-Object { $_.id -eq 10003 }
if ($role.map_id -ne 58 -or $role.map_name -ne '长安' -or $role.map_x -ne 60 -or $role.map_y -ne 67) { throw 'target role map mismatch' }
$stones = @($role.items | Where-Object { $_.template_id -in 322260000,322261000 })
if ($stones.Count -ne 2 -or @($stones | Where-Object { $_.quantity -ne 1000 }).Count -ne 0) { throw 'stone stacks mismatch' }
```

Then instantiate `RoleStore(Settings()).find('1', 10003)` in a one-line Python read check and assert the same quantities remain 1000 after migration logic runs.

- [ ] **Step 5: Run syntax and complete unit verification**

```powershell
D:\python\python.exe -m py_compile strengthening.py server.py protocol.py
D:\python\python.exe -m unittest discover -s tests -v
```

Expected: syntax succeeds; all prior 123 tests plus new strengthening tests pass with zero failures/errors.

- [ ] **Step 6: Inspect protocol and repository diffs**

Run `git diff --check`, inspect `git diff --stat`, and inspect focused diffs for `server.py`, `strengthening.py`, both test files, documentation, and live data. Confirm no APK, `protocol.py` wire layout, config, server process, PID file, or port state changed.

- [ ] **Step 7: Invoke verification-before-completion**

Use `superpowers:verification-before-completion`, rerun the required proof commands it specifies, and only then report completion.

- [ ] **Step 8: Commit only cleanly separable documentation/source changes**

Do not commit the live `data/roles.json` backup. Because `server.py` and `tests/test_protocol.py` contained user changes before this feature, use interactive staging and inspect `git diff --cached` before any commit. Leave overlapping hunks uncommitted if they cannot be separated safely.
