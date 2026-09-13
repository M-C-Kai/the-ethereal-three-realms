# Resource Generator

`resource_generator` is the project for visualizing and generating local game
resources. It sits beside `implementation_staging` so resource tooling can grow
without becoming part of the local server runtime.

## Current Scope

- Character appearance diagnostics and visual comparison sheets.
- A stable home for future map preview and resource visualization tools.
- Generated preview output under `outputs/` unless a script is explicitly
  refreshing committed diagnostic evidence under `docs/diagnostics/`.

## Planned Scope

- Visual map preview from `implementation_staging/maps/`.
- Editable map layout, collision, mirror, portals, and NPC placement.
- Character, equipment, and role resource preview/edit flows.
- Export paths that can be reviewed before syncing back into
  `implementation_staging`.

## Directory Layout

```text
resource_generator/
├─ tools/
│  ├─ characters/       Character and equipment appearance diagnostics
│  ├─ maps/             Future map visualization and editing tools
│  └─ common/           Shared resource parsing helpers
├─ outputs/
│  ├─ characters/       Generated character previews
│  └─ maps/             Generated map previews
└─ docs/                Tooling notes and editor design notes
```

## Boundaries

The server continues to read live data from `implementation_staging`. Resource
generator tools may read from that directory, but they should write generated
work to `resource_generator/outputs/` by default. Moving a generated resource
back into the server project should be a deliberate review step.

The first migration only moves root-level character diagnostic scripts here.
Map tools remain in `implementation_staging/tools/` until their imports and
tests are split cleanly from server modules such as `map_o.py`.
