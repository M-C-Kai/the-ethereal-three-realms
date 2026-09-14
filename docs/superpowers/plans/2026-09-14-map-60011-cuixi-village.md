# Map 60011 Cuixi Village Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a new standalone dynamic map `60011` (“翠溪村”) without modifying map 58 or the existing 60010 regression map.

**Architecture:** Reuse the existing server-side dynamic-map package pipeline under `implementation_staging/maps/<mapId>/`. `60011/map.ref.json` will reference only APK image IDs already exercised by the 60010 dynamic-map baseline; `60011/map.json` will own the tile layout, collision mask, spawn point, return portal, and one inbound portal attached to map 58 at runtime. No APK rebuild and no new protocol action are introduced.

**Tech Stack:** Python 3 standard library, existing `systems.map` dynamic-map compiler/registry, JSON map specs, unittest.

**Spec:** `implementation_staging/DYNAMIC_MAPS.md` and `implementation_staging/docs/protocol/map-ref-streaming.md`

## Global Constraints

- Keep `58` and `60010` unchanged.
- Use new map id `60011` and display name `翠溪村`.
- Use only existing APK image IDs already present in the 60010 dynamic-map baseline: `160`, `161`, `162`, `172`, `310`, `326`.
- Do not add or change MessageID, Action, Property, TLV field ordering, or APK resources.
- Dynamic map ref must remain below the client signed-short transfer limit of 32767 bytes.
- Source-map entry portal is local compatibility data, not original-server restoration.
- Real-device status remains `pending real-device verification` until the user confirms it on the phone.

## APK Verification Gate

- Client-visible impact: yes; entering the new map changes map rendering, collision, spawn, and portal routing.
- Protocol path: existing `1110 -> 1010/12 -> 1010/13 -> 1407 subtype 11/12 -> 1010/14 -> 1010/105`, plus existing `1126` portal actor interaction.
- Resource path: existing `map.ref` parser (`pmsj.work.b.m.z -> m.C()`) and APK `images.o` image IDs.
- Evidence grade: **B** for this new layout. The transport/parser/resource mechanism is already statically locked and exercised by 60010; only the newly composed 60011 layout remains pending phone verification.
- Unknowns: exact visual identity of each reused image tile on the target device is not promoted to original-game semantics; the map is explicitly local compatibility content.
- Regression protection: compile the two JSON specs through the existing dynamic-map materializer and assert registry/portal wiring.

---

### Task 1: Add the 60011 package regression test

**Files:**
- Create: `implementation_staging/tests/test_map_60011_package.py`

**Interfaces:**
- Consumes: `server.Settings.load`, `systems.map.service.DynamicMapPackage`, `materialize_dynamic_map`.
- Produces: a data-level regression gate proving the new package compiles and wires both portals without editing `config.json`.

- [ ] **Step 1: Write the failing test**

Create a unittest that requires `maps/60011/map.json` and `maps/60011/map.ref.json`, materializes them into a temporary directory, asserts both generated binaries are non-empty and the ref is `< 32768` bytes, then loads `config.json` and checks:

```python
definition = settings.map_registry.require(60011)
self.assertEqual(definition.name, '翠溪村')
self.assertFalse(definition.map_ref_available)
self.assertEqual((definition.fallback_width, definition.fallback_height), (36, 36))
self.assertEqual((definition.spawn_x, definition.spawn_y), (18, 30))

entry = settings.map_registry.portal(58, 580007)
self.assertIsNotNone(entry)
self.assertEqual((entry.target_map_id, entry.target_x, entry.target_y), (60011, 18, 30))

back = settings.map_registry.portal(60011, 6001101)
self.assertIsNotNone(back)
self.assertEqual((back.target_map_id, back.target_x, back.target_y), (58, 60, 67))
```

- [ ] **Step 2: Verify the test fails before the map package exists**

Run:

```powershell
D:\python\python.exe -m unittest tests.test_map_60011_package -v
```

Expected before Task 2: FAIL because `implementation_staging/maps/60011/` is absent.

- [ ] **Step 3: Commit the failing regression test**

```bash
git add implementation_staging/tests/test_map_60011_package.py
git commit -m "test: define map 60011 package contract"
```

### Task 2: Add the standalone dynamic map package

**Files:**
- Create: `implementation_staging/maps/60011/map.ref.json`
- Create: `implementation_staging/maps/60011/map.json`

**Interfaces:**
- Consumes: existing `piaomiao-map-ref-v1` and `piaomiao-dynamic-map-v1` compilers.
- Produces: runtime `maps/60011.map.ref`, `maps/60011.map.o`, registry entry `60011`, inbound portal `580007`, return portal `6001101`.

- [ ] **Step 1: Add `map.ref.json` using only known APK image IDs**

Reuse the six image records and six composite definitions already proven by the 60010 baseline, changing only `map_id` to `60011`.

- [ ] **Step 2: Add `map.json` as a 36×36 village/stream layout**

Use local tile definitions `[0,1,2,3,4,5]`. Compose grass variants with a blocked stream/cliff band and sparse large decoration tiles. Encode all impassable water, outer boundary, and decoration anchor cells in `collision`; leave walkable roads and spawn area open.

Registry values are fixed:

```json
{
  "name": "翠溪村",
  "spawn": {"x": 18, "y": 30},
  "npcs": [],
  "portals": [
    {
      "id": 6001101,
      "name": "返回长安",
      "model": -2043000,
      "x": 18,
      "y": 31,
      "direction": 0,
      "target_map_id": 58,
      "target_x": 60,
      "target_y": 67
    }
  ],
  "inbound_portals": [
    {
      "source_map_id": 58,
      "id": 580007,
      "name": "翠溪村传送阵",
      "model": -2043000,
      "x": 66,
      "y": 67,
      "direction": 0
    }
  ]
}
```

- [ ] **Step 3: Run package and map-system tests**

```powershell
D:\python\python.exe -m unittest tests.test_map_60011_package -v
D:\python\python.exe -m unittest tests.test_map_system -v
```

Expected: PASS.

- [ ] **Step 4: Run the unified suite**

```powershell
D:\python\python.exe -m unittest discover -s tests -v
```

Expected: PASS with no regression to 58 or 60010.

- [ ] **Step 5: Commit the map package**

Commit message must record protocol evidence and device status:

```text
feat: add standalone dynamic map 60011

APK evidence: B - existing 1407/11+12 map.ref path and 60010 resource baseline
Protocol impact: no new message/action/property; adds dynamic map package and existing 1126 portals
Tests: test_map_60011_package, test_map_system, unified unittest suite
Real-device: pending real-device verification
```

### Task 3: Phone acceptance

**Files:** none

**Interfaces:**
- Consumes: committed 60011 dynamic-map package.
- Produces: user real-device verdict.

- [ ] **Step 1: Restart only after automated tests pass**

Use the repository launcher so it closes the previous `server.py` process by port/process detection before starting a fresh server.

- [ ] **Step 2: Verify the new map on the phone**

Expected behavior:

1. Enter map 58 and interact with `翠溪村传送阵` near `(66,67)`.
2. Native map transition completes into `翠溪村` at `(18,30)`.
3. Character can move on open ground but cannot cross blocked stream/cliff/decoration cells.
4. `返回长安` at `(18,31)` returns to map 58 `(60,67)`.
5. Re-entering 60011 works without reinstalling the APK.

Until the user reports these results, status is `pending real-device verification`.
