from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path('implementation_staging')
SERVER = ROOT / 'server.py'


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{label}: expected exactly one match, got {count}')
    return text.replace(old, new, 1)


def replace_top_level_function(source: str, name: str, replacement: str) -> str:
    tree = ast.parse(source)
    lines = source.splitlines(keepends=True)
    matches = [
        node for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name
    ]
    if len(matches) != 1:
        raise SystemExit(f'{name}: expected one top-level function, got {len(matches)}')
    node = matches[0]
    start = sum(len(line) for line in lines[: node.lineno - 1])
    end = sum(len(line) for line in lines[: node.end_lineno])
    suffix = '\n\n' if not replacement.endswith('\n\n') else ''
    return source[:start] + replacement.rstrip() + suffix + source[end:]


source = SERVER.read_text(encoding='utf-8')

# ---------------------------------------------------------------------------
# 1) 1080 role-selection preview: APK main/e.K proves the 15-field record is
#    role_id, level, weapon/property7, model, race*10+gender, name, slot,
#    then property2 and property14..20.  The old server incorrectly put race,
#    level and role.stats into those appearance fields.
# ---------------------------------------------------------------------------
source = replace_top_level_function(source, 'role_list', '''def role_list(settings: Settings, roles: list[dict[str, object]] | None = None) -> bytes:
    roles = roles if roles is not None else [default_role(settings)]
    records = []
    preview_properties = (2, 14, 15, 16, 17, 18, 19, 20)
    for role in roles:
        race = int(role.get('race', 0))
        gender = int(role.get('gender', 0))
        appearance = character_appearance(role, settings.item_registry)
        record = [
            integer(int(role['id'])),
            # APK main/e.K: field 1 -> character property 11 (level).
            integer(int(role.get('level', 1))),
            # field 2 -> property7 and v.e(I): current equipped weapon preview.
            integer(int(appearance.get(7, 0))),
            integer(int(role.get('model', settings.role_model))),
            integer((race * 10) + gender),
            string(str(role.get('name', settings.role_name))),
            integer(int(role.get('slot', 0))),
        ]
        # Fields 7..14 are not role stats.  main/e.K feeds them directly to
        # v.d/z/A/B/C/D/E/F, i.e. armor body and the seven visible overlays.
        record.extend(integer(int(appearance.get(index, 0))) for index in preview_properties)
        records.extend(record)
    # S->C action is SHORT while the C->S 1080 request action is BYTE.
    return encode_frame(1080, [short(0), byte(len(roles)), *records])
''')

# ---------------------------------------------------------------------------
# 2) One equipment-stat source of truth.  The compatibility item record has
#    four SHORT equipment attributes.  Existing recovered data confirms the
#    first field as attack (weapon) and the second as defence (armor pieces).
#    Fields 2/3 remain aggregated but are not assigned new semantics here.
# ---------------------------------------------------------------------------
source = replace_top_level_function(source, 'equipped_weapon_attack', '''def equipped_attribute_totals(
    role: dict[str, object],
    registry: ItemRegistry | None = None,
) -> tuple[int, int, int, int]:
    """Aggregate the four protocol equipment attributes of all equipped items."""
    if registry is None:
        registry = default_item_registry()
    totals = [0, 0, 0, 0]
    for item in role_items(role):
        if item.get('location') != 'equipped':
            continue
        try:
            resolved = registry.resolve(item)
        except Exception:
            continue
        if int(resolved.get('equipment_slot', 0)) <= 0:
            continue
        attributes = list(resolved.get('equipment_attributes', [0, 0, 0, 0]))
        for index, value in enumerate((attributes + [0, 0, 0, 0])[:4]):
            if type(value) is int:
                totals[index] += max(0, int(value))
    return tuple(totals)


def effective_character_stats(
    role: dict[str, object],
    registry: ItemRegistry | None = None,
) -> list[int]:
    """Return the five character-panel values after confirmed equipment bonuses."""
    raw_stats = [int(value) for value in list(role.get('stats', []))]
    values = [max(0, value) for value in (raw_stats + [10, 10, 10, 10, 10])[:5]]
    equipment = equipped_attribute_totals(role, registry)
    # Compatibility evidence: equipment attribute[0] is attack and [1] is
    # defence.  Do not invent meanings for the remaining two fields.
    values[0] += equipment[0]
    values[1] += equipment[1]
    return values


def equipped_weapon_attack(
    role: dict[str, object],
    registry: ItemRegistry | None = None,
) -> int:
    """Return the effective first attribute of the equipped slot-10 weapon."""
    if registry is None:
        registry = default_item_registry()
    for item in role_items(role):
        if item.get('location') != 'equipped':
            continue
        resolved = registry.resolve(item)
        if int(resolved.get('equipment_slot', 0)) != 10:
            continue
        attributes = list(resolved.get('equipment_attributes', [0, 0, 0, 0]))
        if not attributes or type(attributes[0]) is not int:
            return 0
        return max(0, int(attributes[0]))
    return 0
''')

source = replace_top_level_function(source, 'combat_stats', '''def combat_stats(
    role: dict[str, object],
    registry: ItemRegistry | None = None,
) -> CombatStats:
    """Derive battle values from the same equipped state shown by the character UI."""
    level = max(1, int(role.get('level', 1)))
    raw_stats = [int(value) for value in list(role.get('stats', []))]
    base_stats = [max(0, value) for value in (raw_stats + [10, 10, 10, 10, 10])[:5]]
    equipment = equipped_attribute_totals(role, registry)
    return CombatStats(
        max_hp=100 + ((level - 1) * 10) + base_stats[1],
        physical_attack=(10 + base_stats[0] + ((level - 1) * 2) + equipment[0]),
        physical_defence=base_stats[1] + (level - 1) + equipment[1],
    )
''')

# Full-login 1006 must initialize the same effective panel values that 1017
# will later refresh after equipment operations.
source = replace_once(
    source,
    "    raw_stats = [int(value) for value in list(role.get('stats', []))]\n"
    "    base_stats = (raw_stats + [10, 10, 10, 10, 10])[:5]\n"
    "    max_hp = 100 + ((level - 1) * 10) + max(0, base_stats[1])\n"
    "    max_mp = 50 + ((level - 1) * 5) + max(0, base_stats[2])\n"
    "    properties[40] = integer(max_hp)\n"
    "    properties[41] = integer(max_hp)\n"
    "    properties[42] = integer(max_mp)\n"
    "    properties[43] = integer(max_mp)\n"
    "    for index, value in enumerate(base_stats, start=44):\n"
    "        properties[index] = integer(max(0, value))",
    "    raw_stats = [int(value) for value in list(role.get('stats', []))]\n"
    "    base_stats = [max(0, value) for value in (raw_stats + [10, 10, 10, 10, 10])[:5]]\n"
    "    display_stats = effective_character_stats(role, settings.item_registry)\n"
    "    max_hp = 100 + ((level - 1) * 10) + base_stats[1]\n"
    "    max_mp = 50 + ((level - 1) * 5) + base_stats[2]\n"
    "    properties[40] = integer(max_hp)\n"
    "    properties[41] = integer(max_hp)\n"
    "    properties[42] = integer(max_mp)\n"
    "    properties[43] = integer(max_mp)\n"
    "    for index, value in enumerate(display_stats, start=44):\n"
    "        properties[index] = integer(max(0, value))",
    'player_info effective equipment attributes',
)

# ---------------------------------------------------------------------------
# 3) Character panel 1039 and the world character 1017 are refreshed from the
#    same current equipment snapshot.  Do not resend 1006 during gameplay: it
#    is the full initializer and recreates the local world player.
# ---------------------------------------------------------------------------
source = replace_top_level_function(source, 'character_panel_frames', '''def character_panel_frames(
    role: dict[str, object],
    registry: ItemRegistry | None = None,
) -> tuple[bytes, bytes]:
    """Return live attribute and divine-power datasets requested by UI 31."""
    level = max(1, int(role.get('level', 1)))
    raw_stats = [int(value) for value in list(role.get('stats', []))]
    base_stats = [max(0, value) for value in (raw_stats + [10, 10, 10, 10, 10])[:5]]
    display_stats = effective_character_stats(role, registry)
    max_hp = 100 + ((level - 1) * 10) + base_stats[1]
    max_mp = 50 + ((level - 1) * 5) + base_stats[2]

    attribute_thresholds = [max_hp, max_mp, *display_stats]
    attributes = encode_frame(1039, [byte(1), *(integer(value) for value in attribute_thresholds)])

    divine_values = [int(role['id']), level, level, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    divine = encode_frame(1039, [byte(2), *(integer(value) for value in divine_values)])
    return attributes, divine
''')

source = replace_top_level_function(source, 'equipment_panel_refresh_frame', '''def equipment_panel_refresh_frame(
    role: dict[str, object],
    registry: ItemRegistry | None = None,
) -> bytes:
    """Enter the APK's verified 1017 redraw callback with the full appearance."""
    return character_appearance_frame(int(role['id']), character_appearance(role, registry))


def character_equipment_refresh_frames(
    role: dict[str, object],
    registry: ItemRegistry | None = None,
) -> tuple[bytes, bytes]:
    """Refresh world appearance plus the open character panel after equipment changes.

    ``main/e.O`` applies 1017 property pairs to the live world character and
    invokes the native dependent-UI redraws. ``main/e.ae`` action 1 is the
    character-panel data path and redraws UI 0x166 when that panel is open.
    """
    if registry is None:
        registry = default_item_registry()
    level = max(1, int(role.get('level', 1)))
    raw_stats = [int(value) for value in list(role.get('stats', []))]
    base_stats = [max(0, value) for value in (raw_stats + [10, 10, 10, 10, 10])[:5]]
    display_stats = effective_character_stats(role, registry)
    max_hp = 100 + ((level - 1) * 10) + base_stats[1]
    max_mp = 50 + ((level - 1) * 5) + base_stats[2]

    properties = character_appearance(role, registry)
    properties.update({
        40: max_hp,
        41: max_hp,
        42: max_mp,
        43: max_mp,
        **{index: value for index, value in enumerate(display_stats, start=44)},
    })
    attributes, _ = character_panel_frames(role, registry)
    return character_appearance_frame(int(role['id']), properties), attributes
''')

# Equip: always send a complete appearance+attribute snapshot, not just an
# appearance diff.  This refreshes both the map actor and an already-open
# basic character/equipment panel.
source = replace_once(
    source,
    "                        appearance_frame = character_appearance_change_frame(active_role, previous_appearance, self.settings.item_registry)\n"
    "                        updates.append(\n"
    "                            appearance_frame\n"
    "                            if appearance_frame is not None\n"
    "                            else equipment_panel_refresh_frame(active_role, self.settings.item_registry)\n"
    "                        )",
    "                        updates.extend(\n"
    "                            character_equipment_refresh_frames(active_role, self.settings.item_registry)\n"
    "                        )",
    'equip full character refresh',
)

# Unequip: same full refresh.
source = replace_once(
    source,
    "                        appearance_frame = character_appearance_change_frame(active_role, previous_appearance, self.settings.item_registry)\n"
    "                        replies.append(\n"
    "                            appearance_frame\n"
    "                            if appearance_frame is not None\n"
    "                            else equipment_panel_refresh_frame(active_role, self.settings.item_registry)\n"
    "                        )",
    "                        replies.extend(\n"
    "                            character_equipment_refresh_frames(active_role, self.settings.item_registry)\n"
    "                        )",
    'unequip full character refresh',
)

# Discarding an equipment instance must also refresh if it was equipped.  A
# full current snapshot is harmless for a bag item and prevents stale panels.
source = replace_once(
    source,
    "                        replies = [encode_frame(1009, [short(3), integer(item_id)])]\n"
    "                        appearance_frame = character_appearance_change_frame(active_role, previous_appearance, self.settings.item_registry)\n"
    "                        if appearance_frame is not None:\n"
    "                            replies.append(appearance_frame)",
    "                        replies = [encode_frame(1009, [short(3), integer(item_id)])]\n"
    "                        if is_equipment(item):\n"
    "                            replies.extend(\n"
    "                                character_equipment_refresh_frames(active_role, self.settings.item_registry)\n"
    "                            )",
    'discard character refresh',
)

# Strengthening mutates equipment_attributes.  Append live appearance/stat and
# 1039 panel refresh after the mutation; if the weapon is in the bag the
# recomputed equipped totals are unchanged, so this remains a safe redraw.
source = replace_once(
    source,
    "        return result.frames\n\n    def handle_shop_purchase(",
    "        if result.changed:\n"
    "            return (*result.frames, *character_equipment_refresh_frames(role, self.settings.item_registry))\n"
    "        return result.frames\n\n    def handle_shop_purchase(",
    'strengthening live character refresh',
)

SERVER.write_text(source, encoding='utf-8')

# ---------------------------------------------------------------------------
# Focused regressions for the recovered 1080 contract and live equipment sync.
# ---------------------------------------------------------------------------
test_path = ROOT / 'tests/test_character_equipment_refresh.py'
test_path.write_text(r'''import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from protocol import decode_frame, field_values
from server import (
    Settings,
    character_appearance,
    character_equipment_refresh_frames,
    character_panel_frames,
    combat_stats,
    default_role,
    effective_character_stats,
    equipped_attribute_totals,
    item_slot,
    role_items,
    role_list,
)


class CharacterEquipmentRefreshTests(unittest.TestCase):
    def setUp(self):
        self.settings = Settings()
        self.role = default_role(self.settings)

    def _equipment_in_slot(self, slot):
        return next(
            item for item in role_items(self.role)
            if item_slot(item, self.settings.item_registry) == slot
        )

    def test_role_list_uses_apk_appearance_contract_not_role_stats(self):
        armor = self._equipment_in_slot(3)
        weapon = self._equipment_in_slot(10)
        armor['location'] = 'equipped'
        weapon['location'] = 'equipped'
        self.role['level'] = 17
        self.role['race'] = 2
        self.role['gender'] = 1
        self.role['stats'] = [91, 92, 93, 94, 95, 96, 97, 98]

        message_id, fields = decode_frame(role_list(self.settings, [self.role]))
        values = field_values(fields)
        self.assertEqual(message_id, 1080)
        self.assertEqual(values[:2], [0, 1])
        record = values[2:17]
        appearance = character_appearance(self.role, self.settings.item_registry)
        self.assertEqual(record[0], self.role['id'])
        self.assertEqual(record[1], 17)
        self.assertEqual(record[2], appearance[7])
        self.assertEqual(record[3], self.role['model'])
        self.assertEqual(record[4], 21)
        self.assertEqual(record[5], self.role['name'])
        self.assertEqual(record[6], self.role['slot'])
        self.assertEqual(
            record[7:15],
            [appearance[index] for index in (2, 14, 15, 16, 17, 18, 19, 20)],
        )
        self.assertNotEqual(record[7:15], self.role['stats'])

    def test_equipment_attribute_totals_follow_equipped_instances(self):
        weapon = self._equipment_in_slot(10)
        shoulder = self._equipment_in_slot(2)
        weapon['location'] = 'equipped'
        shoulder['location'] = 'equipped'
        weapon['equipment_attributes'] = [15, 0, 0, 0]
        shoulder['equipment_attributes'] = [0, 7, 0, 0]
        self.assertEqual(
            equipped_attribute_totals(self.role, self.settings.item_registry)[:2],
            (15, 7),
        )

    def test_character_and_battle_stats_share_equipped_attack_defence(self):
        weapon = self._equipment_in_slot(10)
        shoulder = self._equipment_in_slot(2)
        weapon['location'] = 'equipped'
        shoulder['location'] = 'equipped'
        weapon['equipment_attributes'] = [15, 0, 0, 0]
        shoulder['equipment_attributes'] = [0, 7, 0, 0]

        raw = [max(0, int(v)) for v in self.role['stats'][:5]]
        display = effective_character_stats(self.role, self.settings.item_registry)
        self.assertEqual(display[0], raw[0] + 15)
        self.assertEqual(display[1], raw[1] + 7)
        battle = combat_stats(self.role, self.settings.item_registry)
        self.assertEqual(battle.physical_attack, 10 + raw[0] + 15)
        self.assertEqual(battle.physical_defence, raw[1] + 7)

    def test_full_refresh_contains_appearance_and_live_panel_stats(self):
        armor = self._equipment_in_slot(3)
        weapon = self._equipment_in_slot(10)
        armor['location'] = 'equipped'
        weapon['location'] = 'equipped'
        weapon['equipment_attributes'] = [13, 0, 0, 0]

        refresh_1017, refresh_1039 = character_equipment_refresh_frames(
            self.role, self.settings.item_registry
        )
        message_id, fields = decode_frame(refresh_1017)
        self.assertEqual(message_id, 1017)
        values = field_values(fields)
        self.assertEqual(values[0], 0)
        self.assertEqual(values[1], self.role['id'])
        pair_count = values[2]
        pairs = {
            int(values[3 + i * 2]): int(values[4 + i * 2])
            for i in range(pair_count)
        }
        appearance = character_appearance(self.role, self.settings.item_registry)
        for index, value in appearance.items():
            self.assertEqual(pairs[index], value)
        display = effective_character_stats(self.role, self.settings.item_registry)
        for index, value in enumerate(display, start=44):
            self.assertEqual(pairs[index], value)

        panel_id, panel_fields = decode_frame(refresh_1039)
        self.assertEqual(panel_id, 1039)
        panel_values = field_values(panel_fields)
        self.assertEqual(panel_values[0], 1)
        self.assertEqual(panel_values[-5:], display)

    def test_character_panel_changes_immediately_when_equipment_changes(self):
        weapon = self._equipment_in_slot(10)
        _, before = character_panel_frames(self.role, self.settings.item_registry)
        before_stats = effective_character_stats(self.role, self.settings.item_registry)
        weapon['location'] = 'equipped'
        weapon['equipment_attributes'] = [21, 0, 0, 0]
        attributes, _ = character_panel_frames(self.role, self.settings.item_registry)
        _, fields = decode_frame(attributes)
        values = field_values(fields)
        self.assertEqual(values[-5], before_stats[0] + 21)


if __name__ == '__main__':
    unittest.main()
''', encoding='utf-8')

print('character panel / equipment refresh patch prepared')
