# OpenCode working rules

> **MANDATORY — every agent must read first:** repository root `../AGENTS.md` and `../docs/development/APK_PROTOCOL_FIRST.md`. These rules apply to every change, including bug fixes, refactors, migrations, protocol routing, resources, tests, and documentation. This file may add stricter implementation rules but may not relax the APK evidence gate.

Read `../AGENTS.md`, `../docs/development/APK_PROTOCOL_FIRST.md`, `OPENCODE_HANDOFF.md`, `README.md`, `systems/README.md`, `EQUIPMENT_RESOURCE_CATALOG.md`, and the relevant protocol evidence/tests before making changes.

## Architecture

- All gameplay protocol entries live in `systems/<name>/` (handler/service/protocol/registry/events). `server.py` keeps only dependency assembly, `app.router.SystemRouter` dispatch, and network I/O.
- Cross-system dependencies are injected in `server.py` at assembly time; never import another system's handler directly.
- Do not add monkey patches; the former pet/dynamic-map compatibility layers are gone.

## Scope

- Work only on the local compatibility server, its local APK patch, tests, and bundled resources.
- Do not probe, scan, authenticate to, modify, or retrieve code/data from official or third-party servers.
- Do not expose port 6805 to the public Internet.

## APK Verification Gate

Before **every** modification, explicitly perform the APK impact review defined in `../docs/development/APK_PROTOCOL_FIRST.md`.

- If the change affects client-visible behavior, identify the affected MessageID / Action / Property / field / resource / UI path and record APK evidence grade A/B/C/D.
- Protocol or client-visible behavior requires at least **B-grade** evidence before implementation. C/D-grade evidence permits reverse engineering, diagnostics, and evidence documentation only — no business semantics.
- Never guess field order, TLV type, Action, Property, resource ID, or state-machine meaning.
- Unknown fields may remain at an APK-safe default only when explicitly marked unknown; do not invent names or semantics for them.
- Internal refactors must prove that existing wire frames, field types/order, client-observable state transitions, and resource mappings are unchanged. Preserve or add regression/golden-frame tests for that proof.
- Tests do not substitute for APK evidence. CI passing only proves the implementation matches the asserted contract.
- Do not claim real-device success unless the user has actually confirmed it; otherwise record `pending real-device verification`.

## Required workflow

1. Read the mandatory project rules and relevant module/protocol evidence.
2. Reproduce the current behavior and inspect the last server log when applicable.
3. Complete APK Verification: identify impact, evidence source, evidence grade, unknowns, tests, and real-device status.
4. If evidence is below B for a client-visible behavior, stop implementation and continue reverse engineering/diagnostics instead.
5. Add or update a failing unit test for every new encoder, decoder, migration, state transition, or compatibility rule.
6. Implement the smallest change consistent with the verified APK contract.
7. Run `D:\python\python.exe -m unittest discover -s tests -v`.
8. Run `test_client.py` against the restarted service when the change affects the network flow.
9. Restart the service only after tests pass, then verify PID, port 6805, and the newest log timestamp.
10. In the completion summary include `APK evidence`, `Protocol impact`, `Tests`, and `Real-device` status.

## Compatibility constraints

- Preserve `data/roles.json` and implement migrations for schema changes.
- Preserve exact protocol field types. A numerically equal byte/short/int is not interchangeable.
- Keep item template id, icon code, quality, equipment slot, logical/model IDs, and resource IDs as separate namespaces unless APK evidence proves a mapping.
- Never write an item template id into character appearance properties.
- Static definitions for item/skill/pet/NPC/map/buff/task data belong in catalogs/registries rather than scattered handler/service ID branches.
- Keep core server code standard-library-only. Pillow is allowed only for offline map/resource tools.
- Do not change APK package identity or signing key. Use the existing local test keystore for overlay installs.
- Do not rebuild/reinstall the APK for server-only changes.

## Canonical validation

```powershell
D:\python\python.exe -m unittest discover -s tests -v
D:\python\python.exe test_client.py --host 127.0.0.1 --port 6805 --exercise-role-crud
```

Current baseline: the unified suite in `tests/` passes (`python -m unittest discover -s tests`); the login/role/item/map integration flow is validated with `test_client.py`.
