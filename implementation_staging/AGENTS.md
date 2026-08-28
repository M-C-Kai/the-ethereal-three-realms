# OpenCode working rules

Read `OPENCODE_HANDOFF.md`, `README.md`, `EQUIPMENT_RESOURCE_CATALOG.md`, and the relevant tests before making changes.

## Scope

- Work only on the local compatibility server, its local APK patch, tests, and bundled resources.
- Do not probe, scan, authenticate to, modify, or retrieve code/data from official or third-party servers.
- Do not expose port 6805 to the public Internet.

## Required workflow

1. Reproduce the current behavior and inspect the last server log.
2. Confirm protocol field order and types from smali/JAR evidence before implementing a handler.
3. Add or update a unit test for every new encoder, decoder, migration, and state transition.
4. Run `D:\python\python.exe -m unittest discover -s tests -v`.
5. Run `test_client.py` against the restarted service when the change affects the network flow.
6. Restart the service only after tests pass, then verify PID, port 6805, and the newest log timestamp.

## Compatibility constraints

- Preserve `data/roles.json` and implement migrations for schema changes.
- Preserve exact protocol field types. A numerically equal byte/short/int is not interchangeable.
- Keep item template id, icon code, quality, and equipment slot as separate fields.
- Never write an item template id into character appearance properties.
- Keep core server code standard-library-only. Pillow is allowed only for offline map/resource tools.
- Do not change APK package identity or signing key. Use the existing local test keystore for overlay installs.
- Do not rebuild/reinstall the APK for server-only changes.

## Canonical validation

```powershell
D:\python\python.exe -m unittest discover -s tests -v
D:\python\python.exe test_client.py --host 127.0.0.1 --port 6805 --exercise-role-crud
```

Current baseline: 14 unit tests pass and the complete login/role/item/map integration test prints `OK`.

