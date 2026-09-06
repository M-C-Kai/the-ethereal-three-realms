"""Tests for the Item Catalog data layer.

Verifies that:
- ItemRegistry loads and validates catalog JSON correctly.
- resolve() merges template defaults with instance overrides.
- starter_instances() produces minimal item dicts.
- _ensure_items() never leaks template fields into role items.
- apply_battle_rewards() creates minimal instances.
- equipped_weapon_attack() reads instance state, not template.
"""
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from item_registry import (
    ItemCatalogError,
    ItemRegistry,
    PREVIEW_SLOT_APPEARANCE_PROPERTY,
    PREVIEW_SLOTS_WITHOUT_APPEARANCE,
    armor_resource_preview_template_mapping,
    deprecated_armor_template_ids,
    battle_weapon_field2_from_icon,
    default_item_registry,
    preview_appearance_properties,
    synthetic_preview_template_id,
)
from server import (
    Settings,
    RoleStore,
    apply_battle_rewards,
    character_appearance,
    default_role,
    equipped_weapon_attack,
    item_frame,
    item_slot,
    role_items,
)
from protocol import decode_frame, field_values


TEMPLATE_FIELDS = frozenset({
    'name', 'description', 'max_quantity', 'price', 'level_required',
    'icon_code', 'quality', 'sort_group', 'sort_order',
    'equipment_slot', 'innate_attributes',
    'acquired_attributes', 'extra_attributes', 'appearance_properties',
    'action_flags', 'heal', 'mount_model',
})

INSTANCE_FIELDS = frozenset({
    'id', 'template_id', 'quantity', 'location',
    'last_heal', 'strengthen_level', 'base_equipment_attributes',
    'equipment_attributes', 'state_flags', 'item_flags',
})

WEAPON_TEMPLATE_ID = 10_000_1001
ARMOUR_TEMPLATE_ID = 30_001_001
POTION_TEMPLATE_ID = 260_000_001
MOUNT_TEMPLATE_ID = 170_410_004
STONE_TEMPLATE_ID = 322_260_000


class ItemRegistryLoadTests(unittest.TestCase):
    def test_default_registry_loads_all_templates(self):
        registry = default_item_registry()
        for tid in (WEAPON_TEMPLATE_ID, ARMOUR_TEMPLATE_ID, POTION_TEMPLATE_ID,
                    MOUNT_TEMPLATE_ID, STONE_TEMPLATE_ID):
            definition = registry.require(tid)
            self.assertEqual(definition.template_id, tid)
            self.assertTrue(len(definition.name) > 0)

    def test_require_raises_for_unknown_template(self):
        registry = default_item_registry()
        with self.assertRaises(KeyError):
            registry.require(999_999_999)

    def test_starter_instances_are_minimal(self):
        registry = default_item_registry()
        instances = registry.starter_instances(role_id=1)
        self.assertTrue(len(instances) > 0)
        allowed_keys = {'id', 'template_id', 'quantity', 'location'}
        for item in instances:
            self.assertEqual(set(item.keys()), allowed_keys)
            self.assertIsInstance(item['id'], int)
            self.assertIsInstance(item['template_id'], int)
            self.assertIsInstance(item['quantity'], int)
            self.assertIsInstance(item['location'], str)


class ItemRegistryResolveTests(unittest.TestCase):
    def test_resolve_merges_template_and_instance(self):
        registry = default_item_registry()
        instance = {'id': 1001, 'template_id': WEAPON_TEMPLATE_ID, 'quantity': 5, 'location': 'bag'}
        resolved = registry.resolve(instance)
        self.assertEqual(resolved['template_id'], WEAPON_TEMPLATE_ID)
        self.assertEqual(resolved['name'], '青锋剑')
        self.assertEqual(resolved['equipment_slot'], 10)
        self.assertEqual(resolved['quantity'], 5)
        self.assertEqual(resolved['location'], 'bag')
        self.assertEqual(resolved['id'], 1001)

    def test_resolve_overrides_template_with_instance(self):
        registry = default_item_registry()
        instance = {
            'id': 1001,
            'template_id': WEAPON_TEMPLATE_ID,
            'quantity': 1,
            'location': 'equipped',
            'strengthen_level': 4,
            'equipment_attributes': [8, 0, 0, 0],
        }
        resolved = registry.resolve(instance)
        self.assertEqual(resolved['strengthen_level'], 4)
        self.assertEqual(resolved['equipment_attributes'], [8, 0, 0, 0])
        self.assertEqual(resolved['name'], '青锋剑')

    def test_resolve_returns_copy_for_unknown_template(self):
        registry = default_item_registry()
        instance = {'id': 1, 'template_id': 999_999_999, 'quantity': 1, 'location': 'bag'}
        resolved = registry.resolve(instance)
        self.assertEqual(resolved['template_id'], 999_999_999)
        self.assertEqual(resolved['quantity'], 1)


class EnsureItemsTemplateFieldLeakTests(unittest.TestCase):
    """Lock down: roles.json must never contain template fields."""

    def _get_item_keys(self, template_id):
        settings = Settings()
        role = default_role(settings)
        RoleStore(settings)._ensure_items(role)
        items = [i for i in role['items'] if i.get('template_id') == template_id]
        self.assertTrue(len(items) >= 1, f'no item with template_id={template_id}')
        return items[0].keys()

    def test_weapon_item_has_no_name(self):
        keys = self._get_item_keys(WEAPON_TEMPLATE_ID)
        self.assertNotIn('name', keys)

    def test_weapon_item_has_no_description(self):
        keys = self._get_item_keys(WEAPON_TEMPLATE_ID)
        self.assertNotIn('description', keys)

    def test_weapon_item_has_no_max_quantity(self):
        keys = self._get_item_keys(WEAPON_TEMPLATE_ID)
        self.assertNotIn('max_quantity', keys)

    def test_weapon_item_has_no_price(self):
        keys = self._get_item_keys(WEAPON_TEMPLATE_ID)
        self.assertNotIn('price', keys)

    def test_weapon_item_has_no_icon_code(self):
        keys = self._get_item_keys(WEAPON_TEMPLATE_ID)
        self.assertNotIn('icon_code', keys)

    def test_weapon_item_has_no_quality(self):
        keys = self._get_item_keys(WEAPON_TEMPLATE_ID)
        self.assertNotIn('quality', keys)

    def test_weapon_item_has_no_sort_group(self):
        keys = self._get_item_keys(WEAPON_TEMPLATE_ID)
        self.assertNotIn('sort_group', keys)

    def test_weapon_item_has_no_sort_order(self):
        keys = self._get_item_keys(WEAPON_TEMPLATE_ID)
        self.assertNotIn('sort_order', keys)

    def test_weapon_item_has_no_equipment_slot(self):
        keys = self._get_item_keys(WEAPON_TEMPLATE_ID)
        self.assertNotIn('equipment_slot', keys)

    def test_weapon_item_has_no_appearance_properties(self):
        keys = self._get_item_keys(WEAPON_TEMPLATE_ID)
        self.assertNotIn('appearance_properties', keys)

    def test_weapon_item_has_no_action_flags(self):
        keys = self._get_item_keys(WEAPON_TEMPLATE_ID)
        self.assertNotIn('action_flags', keys)

    def test_weapon_item_has_no_heal(self):
        keys = self._get_item_keys(WEAPON_TEMPLATE_ID)
        self.assertNotIn('heal', keys)

    def test_weapon_item_has_no_mount_model(self):
        keys = self._get_item_keys(WEAPON_TEMPLATE_ID)
        self.assertNotIn('mount_model', keys)

    def test_deprecated_starter_armour_is_not_granted(self):
        settings = Settings()
        role = default_role(settings)
        self.assertNotIn(ARMOUR_TEMPLATE_ID, {int(item.get('template_id', 0)) for item in role['items']})

    def test_potion_item_has_no_template_fields(self):
        keys = self._get_item_keys(POTION_TEMPLATE_ID)
        for field in TEMPLATE_FIELDS:
            self.assertNotIn(field, keys, f'potion item should not have template field {field!r}')

    def test_mount_item_has_no_template_fields(self):
        keys = self._get_item_keys(MOUNT_TEMPLATE_ID)
        for field in TEMPLATE_FIELDS:
            self.assertNotIn(field, keys, f'mount item should not have template field {field!r}')

    def test_stone_item_has_no_template_fields(self):
        keys = self._get_item_keys(STONE_TEMPLATE_ID)
        for field in TEMPLATE_FIELDS:
            self.assertNotIn(field, keys, f'stone item should not have template field {field!r}')

    def test_all_starter_items_are_minimal(self):
        settings = Settings()
        role = default_role(settings)
        RoleStore(settings)._ensure_items(role)
        for item in role['items']:
            for field in TEMPLATE_FIELDS:
                self.assertNotIn(
                    field, item,
                    f'item template_id={item.get("template_id")} has template field {field!r}',
                )


class EnsureItemsPreservesInstanceStateTests(unittest.TestCase):
    """Lock down: instance state must survive _ensure_items."""

    def test_weapon_strengthen_level_preserved(self):
        settings = Settings()
        role = default_role(settings)
        weapon = next(i for i in role['items'] if i.get('template_id') == WEAPON_TEMPLATE_ID)
        weapon['strengthen_level'] = 5
        weapon['base_equipment_attributes'] = [3, 0, 0, 0]
        RoleStore(settings)._ensure_items(role)
        migrated = next(i for i in role['items'] if i.get('template_id') == WEAPON_TEMPLATE_ID)
        self.assertEqual(migrated['strengthen_level'], 5)
        self.assertEqual(migrated['base_equipment_attributes'], [3, 0, 0, 0])

    def test_stone_quantity_preserved(self):
        settings = Settings()
        role = default_role(settings)
        stone = next(i for i in role['items'] if i.get('template_id') == STONE_TEMPLATE_ID)
        stone['quantity'] = 42
        RoleStore(settings)._ensure_items(role)
        migrated = next(i for i in role['items'] if i.get('template_id') == STONE_TEMPLATE_ID)
        self.assertEqual(migrated['quantity'], 42)

    def test_stone_location_preserved(self):
        settings = Settings()
        role = default_role(settings)
        stone = next(i for i in role['items'] if i.get('template_id') == STONE_TEMPLATE_ID)
        stone['location'] = 'warehouse'
        RoleStore(settings)._ensure_items(role)
        migrated = next(i for i in role['items'] if i.get('template_id') == STONE_TEMPLATE_ID)
        self.assertEqual(migrated['location'], 'warehouse')

    def test_stone_item_flags_resolved_from_template(self):
        settings = Settings()
        role = default_role(settings)
        stone = next(i for i in role['items'] if i.get('template_id') == STONE_TEMPLATE_ID)
        stone['item_flags'] = 0x02
        RoleStore(settings)._ensure_items(role)
        migrated = next(i for i in role['items'] if i.get('template_id') == STONE_TEMPLATE_ID)
        # item_flags is a template field — it is stripped from the instance
        # and resolved from the catalogue at read time.
        self.assertNotIn('item_flags', migrated)
        resolved = settings.item_registry.resolve(migrated)
        self.assertEqual(resolved['item_flags'], 0x40)


class BattleRewardsMinimalInstanceTests(unittest.TestCase):
    def _fresh_role(self):
        settings = Settings()
        role = default_role(settings)
        # Remove existing potions so battle reward creates a new instance.
        role['items'] = [
            i for i in role['items']
            if i.get('template_id') != POTION_TEMPLATE_ID
        ]
        return role, settings

    def test_battle_reward_creates_minimal_instance(self):
        role, settings = self._fresh_role()
        item, level_up = apply_battle_rewards(role, registry=settings.item_registry)
        self.assertIsNotNone(item)
        self.assertFalse(level_up)
        for field in TEMPLATE_FIELDS:
            self.assertNotIn(field, item, f'battle reward should not have template field {field!r}')
        self.assertIn('id', item)
        self.assertIn('template_id', item)
        self.assertIn('quantity', item)
        self.assertIn('location', item)

    def test_battle_reward_quantity_is_one(self):
        role, settings = self._fresh_role()
        item, _ = apply_battle_rewards(role, registry=settings.item_registry)
        self.assertEqual(item['quantity'], 1)

    def test_battle_reward_increments_quantity_using_registry(self):
        role, settings = self._fresh_role()
        apply_battle_rewards(role, registry=settings.item_registry)
        item, _ = apply_battle_rewards(role, registry=settings.item_registry)
        self.assertEqual(item['quantity'], 2)

    def test_battle_reward_caps_at_registry_max_quantity(self):
        role, settings = self._fresh_role()
        item, _ = apply_battle_rewards(role, registry=settings.item_registry)
        definition = settings.item_registry.require(POTION_TEMPLATE_ID)
        item['quantity'] = definition.max_quantity
        apply_battle_rewards(role, registry=settings.item_registry)
        self.assertEqual(item['quantity'], definition.max_quantity)


class WeaponAttackFromInstanceTests(unittest.TestCase):
    def test_weapon_attack_reads_instance_equipment_attributes(self):
        settings = Settings()
        role = default_role(settings)
        weapon = next(i for i in role['items'] if i.get('template_id') == WEAPON_TEMPLATE_ID)
        weapon['location'] = 'equipped'
        weapon['equipment_attributes'] = [15, 0, 0, 0]
        self.assertEqual(equipped_weapon_attack(role), 15)

    def test_weapon_attack_ignores_template_when_instance_has_value(self):
        settings = Settings()
        role = default_role(settings)
        weapon = next(i for i in role['items'] if i.get('template_id') == WEAPON_TEMPLATE_ID)
        weapon['location'] = 'equipped'
        weapon['equipment_attributes'] = [0, 0, 0, 0]
        self.assertEqual(equipped_weapon_attack(role), 0)

    def test_weapon_attack_returns_zero_when_no_weapon_equipped(self):
        settings = Settings()
        role = default_role(settings)
        self.assertEqual(equipped_weapon_attack(role), 0)


class ItemFrameReadsFromRegistryTests(unittest.TestCase):
    def test_item_frame_resolves_name_from_registry(self):
        settings = Settings()
        role = default_role(settings)
        weapon = next(i for i in role['items'] if i.get('template_id') == WEAPON_TEMPLATE_ID)
        _, fields = decode_frame(item_frame(weapon, registry=settings.item_registry))
        values = field_values(fields)
        self.assertEqual(values[8], '青锋剑')

    def test_item_frame_resolves_icon_from_registry(self):
        settings = Settings()
        role = default_role(settings)
        weapon = next(i for i in role['items'] if i.get('template_id') == WEAPON_TEMPLATE_ID)
        _, fields = decode_frame(item_frame(weapon, registry=settings.item_registry))
        values = field_values(fields)
        definition = settings.item_registry.require(WEAPON_TEMPLATE_ID)
        self.assertEqual(values[12], definition.icon_code)

    def test_item_frame_slot_from_registry_for_mount(self):
        settings = Settings()
        role = default_role(settings)
        mount = next(i for i in role['items'] if i.get('template_id') == MOUNT_TEMPLATE_ID)
        mount['location'] = 'equipped'
        _, fields = decode_frame(item_frame(mount, registry=settings.item_registry))
        values = field_values(fields)
        self.assertEqual(values[4], 17)


class CharacterAppearanceFromRegistryTests(unittest.TestCase):
    def test_unresolved_helmet_does_not_apply_unverified_property20(self):
        settings = Settings()
        role = default_role(settings)
        helmet = next(
            i for i in role_items(role)
            if settings.item_registry.resolve(i).get('equipment_slot') == 1
        )
        helmet['location'] = 'equipped'
        appearance = character_appearance(role, settings.item_registry)
        self.assertEqual(appearance.get(20), 0)


class RegressionTests(unittest.TestCase):
    def test_fresh_weapon_base_attack_is_three(self):
        settings = Settings()
        role = default_role(settings)
        RoleStore(settings)._ensure_items(role)
        weapon = next(i for i in role['items'] if i.get('template_id') == WEAPON_TEMPLATE_ID)
        self.assertEqual(weapon['base_equipment_attributes'], [3, 0, 0, 0])
        self.assertEqual(weapon['equipment_attributes'], [3, 0, 0, 0])

    def test_fresh_weapon_attack_from_catalog_not_hardcoded(self):
        settings = Settings()
        role = default_role(settings)
        RoleStore(settings)._ensure_items(role)
        weapon = next(i for i in role['items'] if i.get('template_id') == WEAPON_TEMPLATE_ID)
        definition = settings.item_registry.require(WEAPON_TEMPLATE_ID)
        self.assertEqual(
            weapon['base_equipment_attributes'][0],
            definition.equipment_attributes[0],
        )

    def test_battle_reward_notice_name_follows_catalog(self):
        from server import battle_reward_notice
        settings = Settings()
        role = default_role(settings)
        role['items'] = [i for i in role['items'] if i.get('template_id') != POTION_TEMPLATE_ID]
        item, _ = apply_battle_rewards(role, registry=settings.item_registry)
        frame = battle_reward_notice(50, item)
        _, fields = decode_frame(frame)
        values = field_values(fields)
        text = values[2]
        self.assertIn('小还丹', text)

    def test_item_flags_is_template_field_not_instance(self):
        settings = Settings()
        role = default_role(settings)
        RoleStore(settings)._ensure_items(role)
        for item in role['items']:
            self.assertNotIn('item_flags', item,
                f'item_flags must not be stored on instance (template_id={item.get("template_id")})')

    def test_item_flags_resolved_from_template_for_stones(self):
        settings = Settings()
        role = default_role(settings)
        RoleStore(settings)._ensure_items(role)
        stone = next(i for i in role['items'] if i.get('template_id') == STONE_TEMPLATE_ID)
        resolved = settings.item_registry.resolve(stone)
        self.assertEqual(resolved['item_flags'], 0x40)

    def test_item_flags_resolved_from_template_for_equipment(self):
        settings = Settings()
        role = default_role(settings)
        RoleStore(settings)._ensure_items(role)
        weapon = next(i for i in role['items'] if i.get('template_id') == WEAPON_TEMPLATE_ID)
        resolved = settings.item_registry.resolve(weapon)
        self.assertEqual(resolved['item_flags'], 0)

    def test_no_template_fields_leak_to_role_items(self):
        settings = Settings()
        role = default_role(settings)
        RoleStore(settings)._ensure_items(role)
        for item in role['items']:
            for field in TEMPLATE_FIELDS:
                self.assertNotIn(field, item,
                    f'template field {field!r} leaked to instance (template_id={item.get("template_id")})')


class EquipmentResourcePreviewCatalogTests(unittest.TestCase):
    def test_preview_catalog_replaces_old_armor_items_with_31_resource_items(self):
        root = Path(__file__).resolve().parents[1]
        resources = json.loads(
            (root / 'data' / 'catalog' / 'apk_equipment_resources.json').read_text(encoding='utf-8')
        )['resources']
        preview = json.loads(
            (root / 'data' / 'catalog' / 'equipment_resource_preview_items.json').read_text(encoding='utf-8')
        )
        items = preview['items']
        self.assertEqual(len(resources), 252)
        self.assertEqual(len(items), 250)
        self.assertEqual(preview.get('status'), 'compatibility_preview')
        self.assertEqual(len({int(item['template_id']) for item in items}), 250)

        armor_items = [item for item in items if int(item['equipment_slot']) == 3]
        self.assertEqual(len(armor_items), 30)
        expected_mapping = armor_resource_preview_template_mapping()
        self.assertEqual(
            {int(item['template_id']): int(item['appearance_properties']['2']) for item in armor_items},
            expected_mapping,
        )
        self.assertEqual({int(item['icon_code']) for item in armor_items}, set(range(300,310)) | set(range(1200,1210)) | set(range(1300,1310)))
        self.assertTrue(
            set(deprecated_armor_template_ids()).isdisjoint(
                {int(item['template_id']) for item in items}
            )
        )

        nonarmor_resources = [
            r for r in resources
            if int(r['equipment_slot']) not in {3, 12, 13, 14}
        ]
        nonarmor_items = [i for i in items if int(i['equipment_slot']) != 3]
        self.assertEqual(len(nonarmor_resources), 220)
        self.assertEqual(len(nonarmor_items), 220)
        self.assertTrue(all(int(i['equipment_slot']) not in {12, 13, 14} for i in items))
        expected_by_icon = {int(r['icon_code']): int(r['equipment_slot']) for r in nonarmor_resources}
        actual_by_icon = {int(i['icon_code']): int(i['equipment_slot']) for i in nonarmor_items}
        self.assertEqual(actual_by_icon, expected_by_icon)

    def test_registry_loads_every_preview_template(self):
        registry = default_item_registry()
        preview_ids = registry.preview_template_ids()
        self.assertEqual(len(preview_ids), 250)
        for template_id in preview_ids:
            registry.require(template_id)


if __name__ == '__main__':
    unittest.main()
