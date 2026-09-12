# Pet Skills Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the empty pet skill probe with a persisted APK-native pet skill list and native skill-book learning flow.

**Architecture:** Skill definitions live in `data/pet_skills.json`; `pet_skill_service.py` owns skill state and skill-book consumption; `pet_protocol_skill.py` owns `1103/action10` skill records and `1130/action50` learning requests/results; `pet_skill_bridge.py` composes into `server_pet_system.py` without growing `server_pets.py`.

**Tech Stack:** Python standard library, unittest, existing typed TLV protocol, APK DEX evidence.

**Spec:** `docs/superpowers/specs/2026-09-12-pet-system-design.md`

## Global protocol locks

- Skill list request: `1103 [BYTE 10, INT petId]`.
- Skill list response action 10: field 1 is pet id, field 2 is BYTE pet skill mode/state, field 3 is BYTE record count, records start at field 4 and have equal widths. Client builds `b/w` from each record and uses record property 1 as skill id.
- Skill-book selection accepts item template ids `399010011..399050321`.
- Skill learn request: `1130 [BYTE 50, INT petId, INT skillBookTemplateId, INT skillBookInstanceId]`.
- Skill learn result action 50: field 1 is pet id; field 2 INT equals 1 on success; field 3 INT may identify a replaced/forgotten skill and may be 0 when none.
- After learning, client refreshes the skill list with `1103/action10`.
- No invented message IDs or field types.

---

### Task 1: Skill registry and record model
- Create `implementation_staging/data/pet_skills.json` with one local-server test skill and a mapping from verified skill-book range entry `399010011`.
- Create `pet_skill_registry.py` validating unique skill ids/book template ids.
- Unit-test loading and lookup.

### Task 2: Native action10 skill records
- Create `pet_protocol_skill.py`.
- Encode action10 as `[BYTE10, INT petId, BYTE mode, BYTE count, flattened records...]`.
- Use a 27-property record compatible with `b/w`; property0 STRING name, property1 INT skill id, properties2..26 INT.
- Set property2 enabled/type, property3 level, property4 icon id, property5 HP cost, property6 MP cost, property10 category/probability as confirmed runtime-safe values.
- Unit-test exact field types and equal record widths.

### Task 3: Skill-book state transition
- Create `pet_skill_service.py`.
- Validate pet is owned/in bag, item is in bag, item template is registered to a pet skill, and request instance/template match exactly.
- Consume one quantity from the real item instance; remove stack at zero.
- Add the mapped skill id to `pet['skill_ids']` idempotently; first implementation does not randomly forget skills because the original probability rule is not yet server-confirmed.
- Return a result containing `forgotten_skill_id=0`.
- Unit-test success and all no-mutation failures.

### Task 4: Skill bridge
- Create `pet_skill_bridge.py` and install it from `server_pet_system.py` after core bridge.
- Intercept native `1103/action10` and return real skill list from persisted `skill_ids`.
- Intercept exact `1130/action50` learn request, call service, save on success, return `1130 [BYTE50, INT petId, INT 1, INT 0]` and updated `1103/action10` list.
- Preserve every unrelated `1103/1130` action.
- Unit-test translation/routing.

### Task 5: Skill-book inventory integration
- Add template `399010011` to the local item catalog with a server-provided name/description and existing safe icon resource.
- Add an idempotent migration grant of a small test stack to existing roles, using the existing item-instance allocator and normal 1008 item downlink.
- The template id is inside the APK-native skill-book filter range so the original pet-skill UI will display it.
- Unit-test migration idempotence and inventory visibility.

### Task 6: Regression
- Run pet skill tests plus all existing pet tests.
- Run Python syntax compilation for new modules.
- On Windows later run full unittest discover and TCP regression.
- Phone acceptance: pet skill page lists persisted skills; selecting `399010011` skill book and confirming learning consumes one book, shows native success UI, and refreshed skill list contains the skill after relog.
