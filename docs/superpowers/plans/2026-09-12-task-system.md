# Task System Implementation Plan

> **For implementation:** execute this plan task-by-task with test-first changes.

**Goal:** Add a persistent, server-authoritative task system that drives the APK's existing task UI through confirmed 1403/1145 protocol paths.

**Architecture:** Static task definitions live in a validated JSON catalog loaded by `TaskRegistry`. `TaskService` owns all state transitions and event-driven objective progress inside each role's persisted `tasks` object. `task_protocol.py` isolates the APK-specific 1403/1145 request validators and response record encoders. `server.py` remains an orchestration layer: route packets, persist successful transitions, and publish existing game events.

**Tech Stack:** Python 3 standard library, JSON catalog, existing `protocol.py` TLV helpers, `unittest`.

**Spec:** `docs/superpowers/specs/2026-09-12-task-system-design.md`

**Global Constraints:** Do not access official servers. Preserve `data/roles.json`. Exact C->S TLV types must match APK evidence. No new APK message IDs. Unknown protocol actions are side-effect free. Every state transition/encoder/migration gets a unit test. Network and phone validation are not claimed by this plan.

---

### Task 1: Task catalog registry

**Files:**
- Create: `implementation_staging/task_registry.py`
- Create: `implementation_staging/data/catalog/tasks.json`
- Test: `implementation_staging/tests/test_task_registry.py`

1. Write failing tests for valid loading, duplicate ids, invalid category/objective/reward, broken prerequisite, and unknown item reward.
2. Run `python -m unittest tests.test_task_registry -v`; confirm failures are due to missing module/behavior.
3. Implement frozen task/objective/reward dataclasses, category constants, validation, lookup and availability ordering.
4. Add five local compatibility seed tasks (main/side/cycle/daily/divine) using only local maps/monster/item ids.
5. Re-run the focused tests and keep them green.

### Task 2: Persistent task state machine

**Files:**
- Create: `implementation_staging/task_service.py`
- Test: `implementation_staging/tests/test_task_service.py`

1. Write failing tests for migration, prerequisite/level gating, accept, abandon, event progress, ready transition, claim, repeat reset, daily limit/reset, and idempotency.
2. Confirm RED.
3. Implement `ensure_task_state`, `available_tasks`, `accept_task`, `abandon_task`, `record_event`, `claim_task`, plus result dataclasses/exceptions.
4. Keep reward application injectable so server inventory/EXP functions stay authoritative.
5. Re-run focused tests.

### Task 3: APK task protocol adapter

**Files:**
- Create: `implementation_staging/task_protocol.py`
- Test: `implementation_staging/tests/test_task_protocol.py`
- Create: `implementation_staging/docs/protocol/tasks.md`

1. Write failing tests for exact 1403 request shapes: action 6 `[BYTE,BYTE,BYTE,BYTE]`, action 50 `[BYTE,BYTE,BYTE]`, action 15/22/52 `[BYTE,INT]`, action 7 `[BYTE,INT,INT,BYTE,BYTE]`; and 1145 action-0 variants.
2. Write failing decode tests for action-6 and action-50 response headers and records.
3. Implement strict validators/parsers and response builders using existing `Field`, `byte`, `short`, `integer`, `string`, `encode_frame`.
4. Document each confirmed APK callsite and each compatibility-only response field assumption.
5. Re-run focused tests.

### Task 4: Role migration and server routing

**Files:**
- Modify: `implementation_staging/server.py`
- Test: `implementation_staging/tests/test_task_server_integration.py`

1. Add failing tests that a legacy role gains `tasks` without losing existing fields, and that task menu/accept/abandon/claim handlers mutate state only on valid typed requests.
2. Remove 1403 from `MENU_PREFETCH_EMPTY_SUBTYPES`; load default task registry once on server construction.
3. Ensure task state during role migration in `RoleStore.roles_for` and role creation.
4. Route 1403 requests to list/detail/operation handlers and 1145 task action requests to the task service before unrelated 1145 behavior.
5. Save role state after successful mutation and send task snapshot/detail frames.
6. Re-run integration tests.

### Task 5: Progress hooks and rewards

**Files:**
- Modify: `implementation_staging/server.py`
- Test: `implementation_staging/tests/test_task_server_integration.py`

1. Add failing tests for battle victory (`monster_killed`, `battle_won`), map entry (`map_entered`) and item reward (`item_gained`) hooks.
2. Publish task events only after the underlying game action succeeds.
3. On task claim, grant EXP/silver/items through existing role/inventory helpers, fail atomically when item capacity prevents reward creation, then save.
4. Send refreshed task snapshots and existing character/item update frames as applicable.
5. Re-run integration tests.

### Task 6: Full verification and handoff

**Files:**
- Update: `implementation_staging/README.md` only if necessary to add the task test flow.

1. Run `python -m unittest discover -s tests -v`.
2. Run syntax compilation for all new modules.
3. Inspect branch diff for accidental protocol/APK changes.
4. Do not claim `test_client.py` or phone validation unless actually run in the user's local environment.
5. Report exact protocol coverage, test results, branch/commit/PR, and a short phone validation script: open task page -> accept seed task -> trigger objective -> submit -> relog and verify persistence.