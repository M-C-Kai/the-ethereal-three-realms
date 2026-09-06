from __future__ import annotations

from pathlib import Path
import textwrap


ROOT = Path(__file__).resolve().parents[1]
SERVER_PATH = ROOT / 'server.py'
BUS_PATH = ROOT / 'character_update_bus.py'
TEST_PATH = ROOT / 'tests' / 'test_character_update_bus.py'


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f'{label}: expected exactly one match, found {count}')
    return text.replace(old, new, 1)


BUS_SOURCE = '''\
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Callable


class CharacterUpdateEvent(str, Enum):
    """会改变客户端人物可见状态的领域事件。"""

    EQUIPMENT_CHANGED = 'equipment.changed'
    EQUIPMENT_STRENGTHENED = 'equipment.strengthened'
    CHARACTER_LEVEL_CHANGED = 'character.level_changed'
    CHARACTER_STATS_CHANGED = 'character.stats_changed'
    CHARACTER_APPEARANCE_CHANGED = 'character.appearance_changed'


@dataclass(frozen=True)
class CharacterUpdateResult:
    """一次同步人物刷新需要下发的协议帧。"""

    event: CharacterUpdateEvent
    frames: tuple[bytes, ...]
    refresh_scope: tuple[str, ...]


class CharacterUpdateBus:
    """同步、进程内的人物状态更新总线。

    总线只决定事件需要刷新哪些范围；人物公式与协议编码通过回调注入，
    因此该模块不会反向依赖 server.py，也不会持有网络连接。
    """

    def __init__(
        self,
        build_full_refresh: Callable[[dict[str, object], object], tuple[bytes, ...]],
        build_appearance_refresh: Callable[[dict[str, object], object], tuple[bytes, ...]],
        is_item_equipped: Callable[[dict[str, object], int], bool],
    ) -> None:
        self._build_full_refresh = build_full_refresh
        self._build_appearance_refresh = build_appearance_refresh
        self._is_item_equipped = is_item_equipped

    def publish(
        self,
        event: CharacterUpdateEvent | str,
        *,
        role: dict[str, object],
        registry: object,
        item_id: int | None = None,
    ) -> CharacterUpdateResult:
        try:
            normalized = event if isinstance(event, CharacterUpdateEvent) else CharacterUpdateEvent(event)
        except ValueError as exc:
            raise ValueError(f'unsupported character update event: {event!r}') from exc

        if normalized is CharacterUpdateEvent.EQUIPMENT_STRENGTHENED:
            if item_id is None:
                raise ValueError('equipment.strengthened requires item_id')
            if not self._is_item_equipped(role, int(item_id)):
                return CharacterUpdateResult(normalized, (), ())
            return CharacterUpdateResult(
                normalized,
                tuple(self._build_full_refresh(role, registry)),
                ('appearance', 'attributes'),
            )

        if normalized in {
            CharacterUpdateEvent.EQUIPMENT_CHANGED,
            CharacterUpdateEvent.CHARACTER_LEVEL_CHANGED,
            CharacterUpdateEvent.CHARACTER_STATS_CHANGED,
        }:
            return CharacterUpdateResult(
                normalized,
                tuple(self._build_full_refresh(role, registry)),
                ('appearance', 'attributes'),
            )

        if normalized is CharacterUpdateEvent.CHARACTER_APPEARANCE_CHANGED:
            return CharacterUpdateResult(
                normalized,
                tuple(self._build_appearance_refresh(role, registry)),
                ('appearance',),
            )

        raise ValueError(f'unsupported character update event: {normalized!r}')
'''


TEST_SOURCE = '''\
import copy
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from character_update_bus import CharacterUpdateBus, CharacterUpdateEvent
from protocol import decode_frame
from server import (
    Settings,
    build_character_update_bus,
    combat_stats,
    default_role,
    effective_character_stats,
    item_slot,
    role_items,
)


class CharacterUpdateBusRoutingTests(unittest.TestCase):
    def setUp(self):
        self.calls = []

        def full(role, registry):
            self.calls.append(('full', role['id']))
            return (b'full-1017', b'full-1039')

        def appearance(role, registry):
            self.calls.append(('appearance', role['id']))
            return (b'appearance-1017',)

        def equipped(role, item_id):
            return any(
                int(item.get('id', 0)) == int(item_id)
                and item.get('location') == 'equipped'
                for item in role.get('items', [])
            )

        self.bus = CharacterUpdateBus(full, appearance, equipped)
        self.role = {'id': 10001, 'items': []}
        self.registry = object()

    def test_equipment_changed_builds_full_refresh(self):
        result = self.bus.publish(
            CharacterUpdateEvent.EQUIPMENT_CHANGED,
            role=self.role,
            registry=self.registry,
        )
        self.assertEqual(result.frames, (b'full-1017', b'full-1039'))
        self.assertEqual(result.refresh_scope, ('appearance', 'attributes'))

    def test_strengthened_bag_item_returns_empty_frames(self):
        self.role['items'] = [{'id': 7, 'location': 'bag'}]
        result = self.bus.publish(
            CharacterUpdateEvent.EQUIPMENT_STRENGTHENED,
            role=self.role,
            registry=self.registry,
            item_id=7,
        )
        self.assertEqual(result.frames, ())
        self.assertEqual(self.calls, [])

    def test_strengthened_equipped_item_builds_full_refresh(self):
        self.role['items'] = [{'id': 7, 'location': 'equipped'}]
        result = self.bus.publish(
            CharacterUpdateEvent.EQUIPMENT_STRENGTHENED,
            role=self.role,
            registry=self.registry,
            item_id=7,
        )
        self.assertEqual(result.frames, (b'full-1017', b'full-1039'))

    def test_level_and_stats_changes_build_full_refresh(self):
        for event in (
            CharacterUpdateEvent.CHARACTER_LEVEL_CHANGED,
            CharacterUpdateEvent.CHARACTER_STATS_CHANGED,
        ):
            result = self.bus.publish(event, role=self.role, registry=self.registry)
            self.assertEqual(result.frames, (b'full-1017', b'full-1039'))

    def test_appearance_changed_builds_only_appearance_refresh(self):
        result = self.bus.publish(
            CharacterUpdateEvent.CHARACTER_APPEARANCE_CHANGED,
            role=self.role,
            registry=self.registry,
        )
        self.assertEqual(result.frames, (b'appearance-1017',))
        self.assertEqual(result.refresh_scope, ('appearance',))

    def test_unknown_event_raises(self):
        with self.assertRaises(ValueError):
            self.bus.publish('unknown.event', role=self.role, registry=self.registry)

    def test_strengthened_requires_item_id(self):
        with self.assertRaises(ValueError):
            self.bus.publish(
                CharacterUpdateEvent.EQUIPMENT_STRENGTHENED,
                role=self.role,
                registry=self.registry,
            )

    def test_bus_module_has_no_server_dependency(self):
        source = (Path(__file__).resolve().parents[1] / 'character_update_bus.py').read_text(encoding='utf-8')
        self.assertNotIn('import server', source)
        self.assertNotIn('from server', source)


class CharacterEquipmentSwitchBusTests(unittest.TestCase):
    def setUp(self):
        self.settings = Settings()

    def _clear_equipment(self, role):
        for item in role_items(role):
            if item.get('location') == 'equipped':
                item['location'] = 'bag'

    def _copy_item_for_slot(self, role, slot, attributes):
        source = next(
            item for item in role_items(role)
            if item_slot(item, self.settings.item_registry) == slot
        )
        duplicate = copy.deepcopy(source)
        duplicate['id'] = max(int(item.get('id', 0)) for item in role_items(role)) + 1
        duplicate['location'] = 'bag'
        duplicate['equipment_attributes'] = list(attributes)
        role_items(role).append(duplicate)
        return source, duplicate

    def test_weapon_a_to_b_uses_only_new_attack(self):
        role = default_role(self.settings)
        self._clear_equipment(role)
        first, second = self._copy_item_for_slot(role, 10, [25, 0, 0, 0])
        first['equipment_attributes'] = [10, 0, 0, 0]
        first['location'] = 'equipped'
        base_attack = int(role['stats'][0])

        # 模拟真实 action=5：先卸掉同槽旧装备，再装上新装备，最后只发布一次事件。
        first['location'] = 'bag'
        second['location'] = 'equipped'
        result = build_character_update_bus().publish(
            CharacterUpdateEvent.EQUIPMENT_CHANGED,
            role=role,
            registry=self.settings.item_registry,
        )

        display = effective_character_stats(role, self.settings.item_registry)
        battle = combat_stats(role, self.settings.item_registry)
        self.assertEqual(display[0], base_attack + 25)
        self.assertNotEqual(display[0], base_attack + 35)
        self.assertEqual(battle.physical_attack, 10 + base_attack + 25)
        self.assertEqual([decode_frame(frame)[0] for frame in result.frames], [1017, 1039])

    def test_armor_a_to_b_uses_only_new_defence(self):
        role = default_role(self.settings)
        self._clear_equipment(role)
        first, second = self._copy_item_for_slot(role, 3, [0, 12, 0, 0])
        first['equipment_attributes'] = [0, 7, 0, 0]
        first['location'] = 'equipped'
        base_defence = int(role['stats'][1])

        first['location'] = 'bag'
        second['location'] = 'equipped'
        result = build_character_update_bus().publish(
            CharacterUpdateEvent.EQUIPMENT_CHANGED,
            role=role,
            registry=self.settings.item_registry,
        )

        display = effective_character_stats(role, self.settings.item_registry)
        battle = combat_stats(role, self.settings.item_registry)
        self.assertEqual(display[1], base_defence + 12)
        self.assertNotEqual(display[1], base_defence + 19)
        self.assertEqual(battle.physical_defence, base_defence + 12)
        self.assertEqual([decode_frame(frame)[0] for frame in result.frames], [1017, 1039])

    def test_unequip_immediately_reverts_attribute_bonus(self):
        role = default_role(self.settings)
        self._clear_equipment(role)
        weapon = next(
            item for item in role_items(role)
            if item_slot(item, self.settings.item_registry) == 10
        )
        weapon['equipment_attributes'] = [18, 0, 0, 0]
        weapon['location'] = 'equipped'
        base_attack = int(role['stats'][0])
        self.assertEqual(effective_character_stats(role, self.settings.item_registry)[0], base_attack + 18)

        weapon['location'] = 'bag'
        result = build_character_update_bus().publish(
            CharacterUpdateEvent.EQUIPMENT_CHANGED,
            role=role,
            registry=self.settings.item_registry,
        )
        self.assertEqual(effective_character_stats(role, self.settings.item_registry)[0], base_attack)
        self.assertEqual([decode_frame(frame)[0] for frame in result.frames], [1017, 1039])

    def test_strengthening_bag_item_does_not_refresh_character(self):
        role = default_role(self.settings)
        self._clear_equipment(role)
        weapon = next(
            item for item in role_items(role)
            if item_slot(item, self.settings.item_registry) == 10
        )
        weapon['location'] = 'bag'
        result = build_character_update_bus().publish(
            CharacterUpdateEvent.EQUIPMENT_STRENGTHENED,
            role=role,
            registry=self.settings.item_registry,
            item_id=int(weapon['id']),
        )
        self.assertEqual(result.frames, ())

    def test_strengthening_equipped_item_refreshes_character(self):
        role = default_role(self.settings)
        self._clear_equipment(role)
        weapon = next(
            item for item in role_items(role)
            if item_slot(item, self.settings.item_registry) == 10
        )
        weapon['location'] = 'equipped'
        result = build_character_update_bus().publish(
            CharacterUpdateEvent.EQUIPMENT_STRENGTHENED,
            role=role,
            registry=self.settings.item_registry,
            item_id=int(weapon['id']),
        )
        self.assertEqual([decode_frame(frame)[0] for frame in result.frames], [1017, 1039])

    def test_level_changed_refreshes_character_and_open_panel(self):
        role = default_role(self.settings)
        role['level'] = int(role.get('level', 1)) + 1
        result = build_character_update_bus().publish(
            CharacterUpdateEvent.CHARACTER_LEVEL_CHANGED,
            role=role,
            registry=self.settings.item_registry,
        )
        self.assertEqual([decode_frame(frame)[0] for frame in result.frames], [1017, 1039])


if __name__ == '__main__':
    unittest.main()
'''


def apply_server_patch() -> None:
    text = SERVER_PATH.read_text(encoding='utf-8')

    mount_block = """from mount_protocol import (\n    is_mount_atlas_request,\n    load_mount_atlas_entries,\n    mount_atlas_frame,\n)\n"""
    if 'from character_update_bus import CharacterUpdateBus, CharacterUpdateEvent' not in text:
        text = replace_once(
            text,
            mount_block,
            mount_block + "from character_update_bus import CharacterUpdateBus, CharacterUpdateEvent\n",
            'character update bus import',
        )

    class_anchor = """class LocalGameServer:\n    def __init__(self, settings: Settings):\n        self.settings = settings\n        self.roles = RoleStore(settings)\n        self._next_session_id = 1000\n"""
    helper_block = """def is_role_item_equipped(role: dict[str, object], item_id: int) -> bool:\n    \"\"\"Return whether one concrete item instance is currently equipped.\"\"\"\n    for item in role_items(role):\n        try:\n            current_id = int(item.get('id', 0))\n        except (TypeError, ValueError):\n            continue\n        if current_id == int(item_id) and item.get('location') == 'equipped':\n            return True\n    return False\n\n\ndef build_character_update_bus() -> CharacterUpdateBus:\n    \"\"\"Bind the generic update bus to the server's verified refresh builders.\"\"\"\n    return CharacterUpdateBus(\n        build_full_refresh=character_equipment_refresh_frames,\n        build_appearance_refresh=lambda role, registry: (\n            equipment_panel_refresh_frame(role, registry),\n        ),\n        is_item_equipped=is_role_item_equipped,\n    )\n\n\nclass LocalGameServer:\n    def __init__(self, settings: Settings):\n        self.settings = settings\n        self.roles = RoleStore(settings)\n        self.character_update_bus = build_character_update_bus()\n        self._next_session_id = 1000\n"""
    if 'def build_character_update_bus()' not in text:
        text = replace_once(text, class_anchor, helper_block, 'server bus adapter and constructor')

    strengthening_old = """        if result.changed:\n            return (*result.frames, *character_equipment_refresh_frames(role, self.settings.item_registry))\n        return result.frames\n"""
    strengthening_new = """        if result.changed:\n            target_item_id = int(values[1]) if len(values) > 1 else 0\n            refresh = self.character_update_bus.publish(\n                CharacterUpdateEvent.EQUIPMENT_STRENGTHENED,\n                role=role,\n                registry=self.settings.item_registry,\n                item_id=target_item_id,\n            )\n            return (*result.frames, *refresh.frames)\n        return result.frames\n"""
    text = replace_once(text, strengthening_old, strengthening_new, 'strengthening refresh')

    discard_old = """                    elif action == 3 and item is not None and item_action_location_valid(action, item):\n                        previous_appearance = character_appearance(active_role, self.settings.item_registry)\n                        role_items(active_role).remove(item)\n                        self.roles.save()\n                        LOG.info('item discarded item_id=%d name=%r', item_id, item.get('name'))\n                        replies = [encode_frame(1009, [short(3), integer(item_id)])]\n                        if is_equipment(item):\n                            replies.extend(\n                                character_equipment_refresh_frames(active_role, self.settings.item_registry)\n                            )\n"""
    discard_new = """                    elif action == 3 and item is not None and item_action_location_valid(action, item):\n                        was_equipped = is_equipment(item) and item.get('location') == 'equipped'\n                        role_items(active_role).remove(item)\n                        replies = [encode_frame(1009, [short(3), integer(item_id)])]\n                        if was_equipped:\n                            refresh = self.character_update_bus.publish(\n                                CharacterUpdateEvent.EQUIPMENT_CHANGED,\n                                role=active_role,\n                                registry=self.settings.item_registry,\n                            )\n                            replies.extend(refresh.frames)\n                        self.roles.save()\n                        LOG.info('item discarded item_id=%d name=%r', item_id, item.get('name'))\n"""
    text = replace_once(text, discard_old, discard_new, 'discard equipped refresh')

    equip_old = """                        updates.append(encode_frame(1009, [short(5)]))\n                        updates.extend(\n                            character_equipment_refresh_frames(active_role, self.settings.item_registry)\n                        )\n                        self.roles.save()\n"""
    equip_new = """                        updates.append(encode_frame(1009, [short(5)]))\n                        refresh = self.character_update_bus.publish(\n                            CharacterUpdateEvent.EQUIPMENT_CHANGED,\n                            role=active_role,\n                            registry=self.settings.item_registry,\n                        )\n                        updates.extend(refresh.frames)\n                        self.roles.save()\n"""
    text = replace_once(text, equip_old, equip_new, 'equip refresh')

    unequip_old = """                        self.roles.save()\n                        LOG.info('item unequipped item_id=%d name=%r', item_id, item.get('name'))\n                        replies = [item_frame(item, operation=3), encode_frame(1009, [short(6)])]\n                        replies.extend(\n                            character_equipment_refresh_frames(active_role, self.settings.item_registry)\n                        )\n"""
    unequip_new = """                        refresh = self.character_update_bus.publish(\n                            CharacterUpdateEvent.EQUIPMENT_CHANGED,\n                            role=active_role,\n                            registry=self.settings.item_registry,\n                        )\n                        self.roles.save()\n                        LOG.info('item unequipped item_id=%d name=%r', item_id, item.get('name'))\n                        replies = [item_frame(item, operation=3), encode_frame(1009, [short(6)])]\n                        replies.extend(refresh.frames)\n"""
    text = replace_once(text, unequip_old, unequip_new, 'unequip refresh')

    # 旧的差量外观快照在改成“最终状态总线”后已经不再需要。
    stale_snapshot = "                        previous_appearance = character_appearance(active_role, self.settings.item_registry)\n"
    stale_count = text.count(stale_snapshot)
    if stale_count != 2:
        raise RuntimeError(f'expected two stale equipment appearance snapshots after discard migration, found {stale_count}')
    text = text.replace(stale_snapshot, '')

    manual_level_old = """                            await self._send(\n                                writer,\n                                battle_progress_frame(active_role),\n                                level_up_effect_frame(active_role),\n                                cipher=game_cipher,\n                                lock=send_lock,\n                            )\n"""
    manual_level_new = """                            refresh = self.character_update_bus.publish(\n                                CharacterUpdateEvent.CHARACTER_LEVEL_CHANGED,\n                                role=active_role,\n                                registry=self.settings.item_registry,\n                            )\n                            await self._send(\n                                writer,\n                                battle_progress_frame(active_role),\n                                level_up_effect_frame(active_role),\n                                *refresh.frames,\n                                cipher=game_cipher,\n                                lock=send_lock,\n                            )\n"""
    text = replace_once(text, manual_level_old, manual_level_new, 'manual level-up refresh')

    battle_level_old = """                                    if level_up:\n                                        result_frames.append(level_up_effect_frame(active_role))\n                                    else:\n"""
    battle_level_new = """                                    if level_up:\n                                        result_frames.append(level_up_effect_frame(active_role))\n                                        refresh = self.character_update_bus.publish(\n                                            CharacterUpdateEvent.CHARACTER_LEVEL_CHANGED,\n                                            role=active_role,\n                                            registry=self.settings.item_registry,\n                                        )\n                                        result_frames.extend(refresh.frames)\n                                    else:\n"""
    text = replace_once(text, battle_level_old, battle_level_new, 'battle auto-level refresh')

    if text.count('character_equipment_refresh_frames(') != 1:
        raise RuntimeError(
            'direct character_equipment_refresh_frames calls remain after bus migration: '
            f"{text.count('character_equipment_refresh_frames(')}"
        )

    SERVER_PATH.write_text(text, encoding='utf-8')


def main() -> None:
    if BUS_PATH.exists():
        raise RuntimeError('character_update_bus.py already exists; refusing to double-apply')
    if TEST_PATH.exists():
        raise RuntimeError('test_character_update_bus.py already exists; refusing to overwrite')

    BUS_PATH.write_text(textwrap.dedent(BUS_SOURCE), encoding='utf-8')
    TEST_PATH.write_text(textwrap.dedent(TEST_SOURCE), encoding='utf-8')
    apply_server_patch()
    print('character update bus implementation applied')


if __name__ == '__main__':
    main()
