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
