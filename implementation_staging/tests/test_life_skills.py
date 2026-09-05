"""APK-confirmed life skill protocol tests (1132 skill container, 1143 trainer/craft).

Wire schemas are reverse-engineered from the original APK (see
docs/protocol/life-skills.md). Numeric game data (skill/recipe ids, costs,
durations, gains) is local-compatibility data; the protocol shapes are not.
"""
import copy
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from protocol import (  # noqa: E402
    TYPE_BYTE,
    TYPE_INT,
    TYPE_STRING,
    byte,
    decode_frame,
    encode_frame,
    field_values,
    integer,
    short,
    string,
)
import server as server_module  # noqa: E402
from server import (  # noqa: E402
    LocalGameServer,
    RoleStore,
    Settings,
    default_role,
    life_stamina,
    life_stamina_max,
    life_vitality,
    life_vitality_max,
    life_skill_state,
    ensure_life_skills,
    is_life_craft_detail_request,
    is_life_craft_request,
    is_life_craft_text_request,
    is_life_direct_use_request,
    is_life_learn_request,
    is_life_learnable_detail_request,
    is_life_recipe_list_request,
    is_life_skill_info_request,
    is_life_skill_list_request,
    is_life_skill_open_request,
    is_life_skill_upgrade_request,
    is_life_trainer_list_request,
    is_forge_collect_request,
    is_forge_confirm_request,
    is_forge_list_request,
    is_forge_select_request,
    life_craft_ack_frame,
    life_craft_detail_frame,
    life_craft_text_frame,
    life_learn_result_frame,
    life_learnable_detail_frame,
    life_learnable_list_frame,
    life_proficiency_frame,
    life_recipe_list_frame,
    life_skill_info_frame,
    life_skill_list_frame,
    life_skill_upgrade_frame,
    life_trainer_page_frame,
    role_items,
)
from life_skill_registry import (  # noqa: E402
    LifeSkillCatalogError,
    LifeSkillRegistry,
    default_life_skill_registry,
)
from life_skill_service import (  # noqa: E402
    craft_result,
    learn_result,
    upgrade_result,
)

POTION_TEMPLATE_ID = 260_000_001
INITIAL_STONE_TEMPLATE_ID = 322_260_000
MIDDLE_STONE_TEMPLATE_ID = 322_261_000
WEAPON_TEMPLATE_ID = 10_000_1001
ALCHEMY_SKILL_ID = 2003
FORGE_SKILL_ID = 2004
REFINE_RECIPE_ID = 4001   # 3x initial stone -> potion
STONE_RECIPE_ID = 4002    # 4x initial stone -> middle stone
WEAPON_RECIPE_ID = 4003   # 2x middle stone -> weapon


def _ids(fields):
    return [field.type_id for field in fields]


class LifeSkillPlayerStateTests(unittest.TestCase):
    def setUp(self):
        self.settings = Settings()
        self.role = default_role(self.settings)

    def test_old_role_gets_default_life_skill_state(self):
        self.role.pop('life_skills', None)
        state = ensure_life_skills(self.role, self.settings.life_registry)
        self.assertEqual(state['stamina'], 100)
        self.assertEqual(state['stamina_max'], 100)
        self.assertEqual(state['vitality'], 100)
        self.assertEqual(state['vitality_max'], 100)
        self.assertEqual(state['skills'], {})
        self.assertEqual(state['learned_recipes'], [])

    def test_existing_state_is_preserved(self):
        self.role['life_skills'] = {
            'stamina': 3, 'stamina_max': 100,
            'vitality': 4, 'vitality_max': 100,
            'skills': {'2001': {'level': 2, 'proficiency': 7}},
            'learned_recipes': [4001],
        }
        state = ensure_life_skills(self.role, self.settings.life_registry)
        self.assertEqual(state['stamina'], 3)
        self.assertEqual(state['skills']['2001']['proficiency'], 7)

    def test_property_accessors(self):
        ensure_life_skills(self.role, self.settings.life_registry)
        self.assertEqual(life_stamina(self.role), 100)
        self.assertEqual(life_stamina_max(self.role), 100)
        self.assertEqual(life_vitality(self.role), 100)
        self.assertEqual(life_vitality_max(self.role), 100)


class LifeSkillRegistryTests(unittest.TestCase):
    def test_default_registry_loads_skills_recipes_and_targets(self):
        registry = default_life_skill_registry()
        self.assertIn(ALCHEMY_SKILL_ID, registry.skills)
        self.assertIn(REFINE_RECIPE_ID, registry.recipes)
        self.assertTrue(registry.gather_targets)
        self.assertIn(5001, registry.learnable)
        self.assertTrue(registry.trainers)

    def test_every_recipe_output_and_material_exists_in_item_registry(self):
        registry = default_life_skill_registry()
        for recipe in registry.recipes.values():
            registry.item_registry.require(recipe.output_template_id)
            for template_id, _quantity in recipe.materials:
                registry.item_registry.require(template_id)

    def test_every_gather_reward_exists_in_item_registry(self):
        registry = default_life_skill_registry()
        for target in registry.gather_targets:
            registry.item_registry.require(target.reward_template_id)

    def test_registry_rejects_unknown_output_template(self):
        with tempfile.TemporaryDirectory() as directory:
            catalog = Path(directory) / 'life_skills.json'
            catalog.write_text(
                '{"version": 1,'
                ' "defaults": {"stamina_max": 100, "vitality_max": 100},'
                ' "skills": [{"skill_id": 2003, "name": "炼药术", "icon": 0,'
                '  "max_level": 3, "tier_count": 1}],'
                ' "recipes": [{"recipe_id": 4001, "skill_id": 2003, "tier": 0,'
                '  "name": "x", "output_template_id": 999999999,'
                '  "output_quantity": 1, "materials": [], "vitality_cost": 1,'
                '  "required_level": 1, "proficiency_gain": 1, "description": ""}],'
                ' "gather_targets": [], "learnable": [], "trainers": []}',
                encoding='utf-8',
            )
            with self.assertRaises(LifeSkillCatalogError):
                LifeSkillRegistry(catalog, default_life_skill_registry().item_registry)

    def test_recipes_for_skill_and_tier(self):
        registry = default_life_skill_registry()
        recipes = registry.recipes_for(FORGE_SKILL_ID, 0)
        self.assertEqual(
            sorted(recipe.recipe_id for recipe in recipes),
            [STONE_RECIPE_ID, WEAPON_RECIPE_ID],
        )


class LifeSkillRequestGuardTests(unittest.TestCase):
    """TLV type guards: value alone never identifies a life skill action."""

    def test_skill_list_request_byte_zero_only(self):
        fields = decode_frame(encode_frame(1132, [byte(0)]))[1]
        self.assertTrue(is_life_skill_list_request(fields))
        fields = decode_frame(encode_frame(1132, [integer(0)]))[1]
        self.assertFalse(is_life_skill_list_request(fields))

    def test_skill_open_request(self):
        fields = decode_frame(encode_frame(1132, [byte(1), integer(2003)]))[1]
        self.assertTrue(is_life_skill_open_request(fields))
        for bad in ([byte(1)], [byte(1), byte(2003)], [integer(1), integer(2003)]):
            fields = decode_frame(encode_frame(1132, bad))[1]
            self.assertFalse(is_life_skill_open_request(fields), bad)

    def test_recipe_list_request(self):
        fields = decode_frame(encode_frame(1132, [
            byte(2), integer(2003), byte(0), byte(0), byte(0),
        ]))[1]
        self.assertTrue(is_life_recipe_list_request(fields))
        fields = decode_frame(encode_frame(1132, [
            byte(2), integer(2003), integer(0), byte(0), byte(0),
        ]))[1]
        self.assertFalse(is_life_recipe_list_request(fields))

    def test_skill_info_request(self):
        fields = decode_frame(encode_frame(1132, [byte(3), integer(2003), byte(1)]))[1]
        self.assertTrue(is_life_skill_info_request(fields))
        fields = decode_frame(encode_frame(1132, [byte(3), integer(2003), integer(1)]))[1]
        self.assertFalse(is_life_skill_info_request(fields))

    def test_upgrade_request(self):
        fields = decode_frame(encode_frame(1132, [byte(6), integer(2003)]))[1]
        self.assertTrue(is_life_skill_upgrade_request(fields))
        fields = decode_frame(encode_frame(1132, [byte(6), byte(2003)]))[1]
        self.assertFalse(is_life_skill_upgrade_request(fields))

    def test_trainer_list_request(self):
        fields = decode_frame(encode_frame(1143, [
            byte(1), integer(7001), byte(0), byte(0),
        ]))[1]
        self.assertTrue(is_life_trainer_list_request(fields))
        fields = decode_frame(encode_frame(1143, [
            integer(1), integer(7001), byte(0), byte(0),
        ]))[1]
        self.assertFalse(is_life_trainer_list_request(fields))

    def test_learnable_detail_and_learn_requests(self):
        fields = decode_frame(encode_frame(1143, [byte(2), integer(5001)]))[1]
        self.assertTrue(is_life_learnable_detail_request(fields))
        fields = decode_frame(encode_frame(1143, [byte(3), integer(5001)]))[1]
        self.assertTrue(is_life_learn_request(fields))
        fields = decode_frame(encode_frame(1143, [byte(3), byte(5001)]))[1]
        self.assertFalse(is_life_learn_request(fields))

    def test_craft_detail_request(self):
        fields = decode_frame(encode_frame(1143, [byte(4), integer(4001)]))[1]
        self.assertTrue(is_life_craft_detail_request(fields))

    def test_normal_craft_and_direct_use_never_confused(self):
        normal = decode_frame(encode_frame(1143, [
            byte(5), integer(4001), integer(101), integer(102),
            integer(0), integer(0), byte(2),
        ]))[1]
        direct = decode_frame(encode_frame(1143, [
            byte(5), integer(4001), integer(0), integer(0), integer(0), integer(0),
        ]))[1]
        self.assertEqual(_ids(normal), [TYPE_BYTE, TYPE_INT, TYPE_INT, TYPE_INT, TYPE_INT, TYPE_INT, TYPE_BYTE])
        self.assertEqual(_ids(direct), [TYPE_BYTE, TYPE_INT, TYPE_INT, TYPE_INT, TYPE_INT, TYPE_INT])
        self.assertTrue(is_life_craft_request(normal))
        self.assertFalse(is_life_direct_use_request(normal))
        self.assertTrue(is_life_direct_use_request(direct))
        self.assertFalse(is_life_craft_request(direct))

    def test_craft_request_quantity_bounds(self):
        for quantity in (0, -1, 100):
            fields = decode_frame(encode_frame(1143, [
                byte(5), integer(4001), integer(0), integer(0),
                integer(0), integer(0), byte(quantity),
            ]))[1]
            self.assertFalse(is_life_craft_request(fields), quantity)

    def test_craft_text_request(self):
        fields = decode_frame(encode_frame(1143, [byte(6), integer(4001)]))[1]
        self.assertTrue(is_life_craft_text_request(fields))


class ForgeRequestGuardTests(unittest.TestCase):
    """1084 C->S request shapes are APK-confirmed; guards lock the TLV types."""

    def test_forge_list_request(self):
        fields = decode_frame(encode_frame(1084, [
            byte(0), integer(2000), short(0), short(0), byte(0),
        ]))[1]
        self.assertTrue(is_forge_list_request(fields))
        fields = decode_frame(encode_frame(1084, [
            integer(0), integer(2000), short(0), short(0), byte(0),
        ]))[1]
        self.assertFalse(is_forge_list_request(fields))

    def test_forge_select_request(self):
        fields = decode_frame(encode_frame(1084, [byte(2), integer(4003)]))[1]
        self.assertTrue(is_forge_select_request(fields))

    def test_forge_collect_and_confirm_requests(self):
        collect = decode_frame(encode_frame(1084, [
            byte(3), integer(4003), integer(1), integer(2), integer(0), integer(0),
        ]))[1]
        confirm = decode_frame(encode_frame(1084, [
            byte(5), integer(4003), integer(1), integer(2), integer(0), integer(0),
        ]))[1]
        self.assertEqual(_ids(collect), [TYPE_BYTE, *([TYPE_INT] * 5)])
        self.assertTrue(is_forge_collect_request(collect))
        self.assertTrue(is_forge_confirm_request(confirm))
        self.assertFalse(is_forge_confirm_request(collect))
        self.assertFalse(is_forge_collect_request(confirm))


class LifeSkillFrameTests(unittest.TestCase):
    def setUp(self):
        self.settings = Settings()
        self.registry = self.settings.life_registry
        self.role = default_role(self.settings)
        ensure_life_skills(self.role, self.settings.life_registry)
        self.role['life_skills']['skills'][str(ALCHEMY_SKILL_ID)] = {
            'level': 1, 'proficiency': 30,
        }

    def test_skill_list_frame_merges_sect_and_life_records_with_equal_width(self):
        message_id, fields = decode_frame(life_skill_list_frame(self.role, self.settings))
        self.assertEqual(message_id, 1132)
        values = field_values(fields)
        self.assertEqual(values[0], 0)
        count = values[1]
        # APK screen 603 allocates exactly seven entries and dereferences all
        # of them without null checks while constructing the life-skill page.
        self.assertEqual(count, 7)
        size = len(values)
        self.assertEqual((size - 2) % count, 0)
        width = (size - 2) // count
        self.assertEqual(width, 14)
        records = [
            values[2 + i * width:2 + (i + 1) * width]
            for i in range(count)
        ]
        self.assertEqual(len({record[1] for record in records}), 7)
        self.assertEqual(
            [(record[0], record[2]) for record in records[-2:]],
            [('未开放', 0), ('未开放', 0)],
        )
        first = values[2:2 + width]
        # Life skills are 2001-2004, first should be one of them
        self.assertIn(first[0], ('采药术', '采矿术', '炼药术', '锻造术'))
        # Find the alchemy record by skill_id across all records
        alchemy_record = None
        for i in range(1, count):
            record = values[2 + i * width:2 + (i + 1) * width]
            if record[1] == ALCHEMY_SKILL_ID:
                alchemy_record = record
                break
        self.assertIsNotNone(alchemy_record)
        self.assertEqual(alchemy_record[2], 1)
        self.assertEqual(alchemy_record[4], 30)

    def test_skill_list_frame_only_contains_life_skills(self):
        """1132/action=0 should only contain life skills, not sect skills."""
        role = copy.deepcopy(self.role)
        role['sect_id'] = 1

        message_id, fields = decode_frame(life_skill_list_frame(role, self.settings))
        values = field_values(fields)

        self.assertEqual(message_id, 1132)
        # Should contain 7 records (4 life skills + 3 placeholders)
        self.assertEqual(values[1], 7)
        # Extract all skill IDs from records
        skill_ids = [values[2 + i * 14 + 1] for i in range(7)]
        # Should not contain sect skill 10001
        self.assertNotIn(10001, skill_ids)
        # Should contain life skills 2001-2004
        self.assertIn(2001, skill_ids)
        self.assertIn(2002, skill_ids)
        self.assertIn(2003, skill_ids)
        self.assertIn(2004, skill_ids)

    def test_recipe_list_frame_layout(self):
        skill = self.registry.skills[ALCHEMY_SKILL_ID]
        recipes = self.registry.recipes_for(ALCHEMY_SKILL_ID, 0)
        message_id, fields = decode_frame(
            life_recipe_list_frame(skill, 0, recipes, self.registry)
        )
        self.assertEqual(message_id, 1132)
        values = field_values(fields)
        self.assertEqual(_ids(fields[:6]), [TYPE_BYTE, TYPE_INT, TYPE_STRING, TYPE_STRING, TYPE_BYTE, TYPE_BYTE])
        self.assertEqual(values[0], 2)
        self.assertEqual(values[1], ALCHEMY_SKILL_ID)
        self.assertEqual(values[5], len(recipes))
        record = values[6:10]
        self.assertEqual(_ids(fields[6:10]), [TYPE_INT, TYPE_INT, TYPE_STRING, TYPE_STRING])
        self.assertEqual(record[0], recipes[0].recipe_id)
        self.assertEqual(record[2], recipes[0].name)

    def test_proficiency_frame_layout(self):
        message_id, fields = decode_frame(life_proficiency_frame(self.role, self.settings))
        self.assertEqual(message_id, 1132)
        values = field_values(fields)
        self.assertEqual(values[0], 4)
        self.assertEqual(values[1], 1)
        record = values[2:12]
        self.assertEqual(_ids(fields[2:12]), [TYPE_STRING] + [TYPE_INT] * 9)
        self.assertEqual(record[1], ALCHEMY_SKILL_ID)
        self.assertEqual(record[2], 1)
        self.assertEqual(record[4], 30)

    def test_upgrade_frame_layout(self):
        skill = self.registry.skills[ALCHEMY_SKILL_ID]
        message_id, fields = decode_frame(life_skill_upgrade_frame(skill, self.role, self.settings))
        self.assertEqual(message_id, 1132)
        values = field_values(fields)
        self.assertEqual(_ids(fields), [
            TYPE_BYTE, TYPE_INT, TYPE_STRING, TYPE_BYTE, TYPE_BYTE,
            TYPE_BYTE, TYPE_INT, TYPE_INT, TYPE_STRING, TYPE_STRING, TYPE_INT,
        ])
        self.assertEqual(values[0], 6)
        self.assertEqual(values[1], ALCHEMY_SKILL_ID)
        self.assertEqual(values[2], skill.name)
        self.assertEqual(values[3], 1)
        self.assertEqual(values[4], skill.max_level)
        self.assertEqual(values[5], skill.upgrade_required_role_level)

    def test_trainer_page_and_learnable_list_frames(self):
        trainer = self.registry.trainers[7001]
        message_id, fields = decode_frame(life_trainer_page_frame(trainer))
        self.assertEqual(message_id, 1143)
        values = field_values(fields)
        self.assertEqual(_ids(fields), [TYPE_BYTE, TYPE_INT, TYPE_STRING, TYPE_BYTE, TYPE_STRING, TYPE_STRING])
        self.assertEqual(values[0], 0)
        self.assertEqual(values[1], 7001)

        message_id, fields = decode_frame(
            life_learnable_list_frame(trainer, self.role, self.settings)
        )
        self.assertEqual(message_id, 1143)
        values = field_values(fields)
        self.assertEqual(values[0], 1)
        self.assertEqual(values[1], 0)  # page
        self.assertEqual(values[2], len(trainer.entry_ids))
        record = values[3:10]
        self.assertEqual(_ids(fields[3:10]), [TYPE_INT, TYPE_INT, TYPE_INT, TYPE_INT, TYPE_INT, TYPE_STRING, TYPE_STRING])
        self.assertEqual(record[0], 5001)
        self.assertEqual(record[2], 1)  # level requirement

    def test_craft_detail_frame_layout(self):
        recipe = self.registry.recipes[REFINE_RECIPE_ID]
        message_id, fields = decode_frame(
            life_craft_detail_frame(recipe, self.role, self.settings)
        )
        self.assertEqual(message_id, 1143)
        values = field_values(fields)
        self.assertEqual(_ids(fields[:5]), [TYPE_BYTE, TYPE_INT, TYPE_STRING, TYPE_INT, TYPE_STRING])
        self.assertEqual(values[0], 4)
        self.assertEqual(values[1], recipe.output_template_id)
        self.assertEqual(values[2], recipe.name)
        material_ids = values[5:9]
        self.assertEqual(_ids(fields[5:9]), [TYPE_INT] * 4)
        self.assertEqual(material_ids[0], INITIAL_STONE_TEMPLATE_ID)
        self.assertEqual(_ids(fields[9:13]), [TYPE_STRING] * 4)
        self.assertEqual(_ids(fields[13:17]), [TYPE_BYTE] * 4)
        self.assertEqual(values[13], 3)  # required quantity

    def test_learn_result_frame_success_removes_row(self):
        entry = self.registry.learnable[5001]
        message_id, fields = decode_frame(life_learn_result_frame(0, entry, True, None))
        self.assertEqual(message_id, 1143)
        values = field_values(fields)
        self.assertEqual(_ids(fields), [TYPE_BYTE, TYPE_BYTE, TYPE_INT, TYPE_INT])
        self.assertEqual(values, [3, 0, 5001, 0])

    def test_learn_result_frame_failure_replaces_row(self):
        entry = self.registry.learnable[5001]
        message_id, fields = decode_frame(life_learn_result_frame(0, entry, False, entry))
        self.assertEqual(message_id, 1143)
        values = field_values(fields)
        self.assertEqual(values[:4], [3, 0, 5001, 1])
        self.assertEqual(len(values), 4 + 7)
        self.assertEqual(values[4], 5001)

    def test_craft_ack_and_text_frames(self):
        message_id, fields = decode_frame(life_craft_ack_frame())
        self.assertEqual((message_id, field_values(fields)), (1143, [5]))
        message_id, fields = decode_frame(life_craft_text_frame('活力不足'))
        self.assertEqual(message_id, 1143)
        self.assertEqual(_ids(fields), [TYPE_BYTE, TYPE_STRING])
        self.assertEqual(field_values(fields), [6, '活力不足'])


class LifeCraftBusinessTests(unittest.TestCase):
    def setUp(self):
        self.settings = Settings()
        self.registry = self.settings.life_registry
        self.recipe = self.registry.recipes[REFINE_RECIPE_ID]
        self.role = default_role(self.settings)
        ensure_life_skills(self.role, self.settings.life_registry)
        self.role['life_skills']['skills'][str(ALCHEMY_SKILL_ID)] = {
            'level': 1, 'proficiency': 0,
        }
        self.role['life_skills']['learned_recipes'] = [REFINE_RECIPE_ID]
        # Remove starter_inventory stones so the craft material pool only
        # contains the stacks we add explicitly for each test.
        self.role['items'] = [
            item for item in self.role['items']
            if item.get('template_id') != INITIAL_STONE_TEMPLATE_ID
        ]
        # materials: four initial stones across two stacks, so one craft
        # leaves a partial stack behind (1008 update) and one consumed
        # instance (1009 removal)
        self.materials = [
            {'id': 100, 'template_id': INITIAL_STONE_TEMPLATE_ID, 'quantity': 2, 'location': 'bag'},
            {'id': 101, 'template_id': INITIAL_STONE_TEMPLATE_ID, 'quantity': 2, 'location': 'bag'},
        ]
        self.role['items'] = self.role['items'] + self.materials

    def _craft(self, quantity=1, slots=None):
        if slots is None:
            slots = [100, 101, 0, 0]
        return craft_result(
            self.role, self.recipe, slots, quantity,
            life_registry=self.registry,
            item_registry=self.settings.item_registry,
        )

    def test_successful_craft_consumes_materials_and_grants_output(self):
        result = self._craft()
        self.assertTrue(result.changed)
        self.assertEqual(result.reason, '')
        stones = [i for i in role_items(self.role) if i.get('template_id') == INITIAL_STONE_TEMPLATE_ID]
        self.assertEqual(sum(int(i['quantity']) for i in stones), 1)
        self.assertNotIn(
            100, {int(i['id']) for i in role_items(self.role)},
            'exhausted instance must be removed',
        )
        frame_ids = [decode_frame(f)[0] for f in result.frames]
        self.assertEqual(frame_ids[0], 1008)
        self.assertIn(1009, frame_ids)
        potion = next(
            i for i in role_items(self.role)
            if i.get('template_id') == POTION_TEMPLATE_ID and i.get('location') == 'bag'
        )
        self.assertEqual(potion['quantity'], 10 + 1)
        self.assertEqual(self.role['life_skills']['vitality'], 90)
        state = self.role['life_skills']['skills'][str(ALCHEMY_SKILL_ID)]
        self.assertEqual(state['proficiency'], 5)
        frame_ids = [decode_frame(f)[0] for f in result.frames]
        self.assertEqual(frame_ids[0], 1008)
        self.assertIn(1017, frame_ids)
        self.assertIn(1132, frame_ids)
        ack_id, ack_fields = decode_frame(result.frames[-1])
        self.assertEqual((ack_id, field_values(ack_fields)), (1143, [5]))

    def test_craft_stacks_into_existing_output_stack(self):
        self._add_extra_stones([(102, 3), (103, 3)])
        before = len(role_items(self.role))
        self._craft(quantity=1, slots=[102, 0, 0, 0])
        self._craft(quantity=1, slots=[103, 0, 0, 0])
        potions = [
            i for i in role_items(self.role)
            if i.get('template_id') == POTION_TEMPLATE_ID and i.get('location') == 'bag'
        ]
        self.assertEqual(len(potions), 1)
        self.assertEqual(potions[0]['quantity'], 10 + 2)

    def test_craft_multi_quantity(self):
        self._add_extra_stones([(104, 3), (105, 3)])
        self._craft(quantity=1, slots=[104, 0, 0, 0])
        result = self._craft(quantity=1, slots=[105, 0, 0, 0])
        self.assertTrue(result.changed)
        state = self.role['life_skills']['skills'][str(ALCHEMY_SKILL_ID)]
        self.assertEqual(state['proficiency'], 10)
        self.assertEqual(self.role['life_skills']['vitality'], 80)

    def _add_extra_stones(self, stacks):
        for stack_id, qty in stacks:
            self.role['items'].append(
                {'id': stack_id, 'template_id': INITIAL_STONE_TEMPLATE_ID, 'quantity': qty, 'location': 'bag'},
            )

    def test_craft_equipment_output_seeds_weapon_base(self):
        recipe = self.registry.recipes[WEAPON_RECIPE_ID]
        self.role['life_skills']['learned_recipes'] = [WEAPON_RECIPE_ID]
        self.role['life_skills']['skills'][str(FORGE_SKILL_ID)] = {'level': 1, 'proficiency': 0}
        self.role['items'] = self.role['items'] + [
            {'id': 200, 'template_id': MIDDLE_STONE_TEMPLATE_ID, 'quantity': 2, 'location': 'bag'},
        ]
        result = craft_result(
            self.role, recipe, [200, 0, 0, 0], 1,
            life_registry=self.registry,
            item_registry=self.settings.item_registry,
        )
        self.assertTrue(result.changed)
        weapon = next(
            i for i in role_items(self.role)
            if i.get('template_id') == WEAPON_TEMPLATE_ID and int(i.get('id', 0)) > 1000120
        )
        self.assertEqual(weapon['base_equipment_attributes'], [3, 0, 0, 0])

    def test_craft_unknown_recipe_rejected(self):
        result = craft_result(
            self.role, None, [0, 0, 0, 0], 1,
            life_registry=self.registry,
            item_registry=self.settings.item_registry,
        )
        self.assertFalse(result.changed)

    def test_craft_skill_not_learned_rejected(self):
        del self.role['life_skills']['skills'][str(ALCHEMY_SKILL_ID)]
        result = self._craft()
        self.assertFalse(result.changed)
        self.assertEqual(self.role['life_skills']['vitality'], 100)

    def test_craft_recipe_not_learned_rejected(self):
        self.role['life_skills']['learned_recipes'] = []
        result = self._craft()
        self.assertFalse(result.changed)

    def test_craft_wrong_material_template_rejected(self):
        self.role['items'] = self.role['items'] + [
            {'id': 300, 'template_id': POTION_TEMPLATE_ID, 'quantity': 5, 'location': 'bag'},
        ]
        result = self._craft(slots=[300, 0, 0, 0])
        self.assertFalse(result.changed)

    def test_craft_unknown_instance_rejected(self):
        result = self._craft(slots=[999999, 0, 0, 0])
        self.assertFalse(result.changed)

    def test_craft_insufficient_materials_rejected(self):
        result = self._craft(quantity=2)
        self.assertFalse(result.changed)
        self.assertEqual(
            sum(int(i['quantity']) for i in role_items(self.role)
                if i.get('template_id') == INITIAL_STONE_TEMPLATE_ID),
            4,
        )

    def test_craft_insufficient_vitality_rejected(self):
        self.role['life_skills']['vitality'] = 5
        result = self._craft()
        self.assertFalse(result.changed)
        self.assertEqual(self.role['life_skills']['vitality'], 5)

    def test_craft_quantity_zero_and_over_limit_rejected(self):
        for quantity in (0, -1, 100):
            result = self._craft(quantity=quantity)
            self.assertFalse(result.changed, quantity)

    def test_craft_bag_full_rejected_without_mutation(self):
        capacity = int(self.role['bag_capacity'])
        self.role['items'] = self.role['items'] + [
            {'id': 900000 + index, 'template_id': 260_000_200 + index,
             'quantity': 1, 'location': 'bag'}
            for index in range(capacity)
        ]
        # remove the existing potion stack so the output needs a new slot
        self.role['items'] = [
            i for i in self.role['items']
            if not (i.get('template_id') == POTION_TEMPLATE_ID and i.get('location') == 'bag')
        ]
        before = copy.deepcopy(self.role)
        result = self._craft()
        self.assertFalse(result.changed)
        self.assertEqual(self.role, before)

    def test_craft_save_failure_rolls_back_completely(self):
        with tempfile.TemporaryDirectory() as directory:
            settings = Settings(role_data_file=str(Path(directory) / 'roles.json'))
            server = LocalGameServer(settings)
            role = server.roles.roles_for('life-craft')[0]
            ensure_life_skills(role, settings.life_registry)
            role['life_skills']['skills'][str(ALCHEMY_SKILL_ID)] = {'level': 1, 'proficiency': 0}
            role['life_skills']['learned_recipes'] = [REFINE_RECIPE_ID]
            role['items'] = role['items'] + [
                {'id': 100, 'template_id': INITIAL_STONE_TEMPLATE_ID, 'quantity': 3, 'location': 'bag'},
            ]
            recipe = settings.life_registry.recipes[REFINE_RECIPE_ID]
            before = copy.deepcopy(role)
            fields = decode_frame(encode_frame(1143, [
                byte(5), integer(REFINE_RECIPE_ID),
                integer(100), integer(0), integer(0), integer(0), byte(1),
            ]))[1]
            with mock.patch.object(server.roles, 'save', side_effect=OSError('disk full')):
                with self.assertRaises(OSError):
                    server.handle_life_craft(role, fields)
            self.assertEqual(role, before)


class LifeLearnBusinessTests(unittest.TestCase):
    def setUp(self):
        self.settings = Settings()
        self.registry = self.settings.life_registry
        self.entry = self.registry.learnable[5001]
        self.trainer = self.registry.trainers[7001]
        self.role = default_role(self.settings)
        self.role['experience'] = 10_000
        ensure_life_skills(self.role, self.settings.life_registry)

    def test_successful_learn_grants_skill_and_deducts_costs(self):
        silver_before = self.role['currencies']['silver']
        exp_before = int(self.role['experience'])
        result = learn_result(self.role, self.trainer, self.entry, life_registry=self.registry)
        self.assertTrue(result.changed)
        self.assertEqual(self.role['currencies']['silver'], silver_before - self.entry.silver_cost)
        self.assertEqual(int(self.role['experience']), exp_before - self.entry.experience_cost)
        self.assertEqual(
            self.role['life_skills']['skills'][str(5001 and self.entry.skill_id)],
            {'level': 1, 'proficiency': 0},
        )
        frame_ids = [decode_frame(f)[0] for f in result.frames]
        self.assertEqual(frame_ids[-1], 1143)
        _, fields = decode_frame(result.frames[-1])
        self.assertEqual(field_values(fields), [3, 0, self.entry.entry_id, 0])
        self.assertIn(1132, frame_ids)

    def test_learn_already_learned_rejected(self):
        learn_result(self.role, self.trainer, self.entry, life_registry=self.registry)
        state_before = copy.deepcopy(self.role['life_skills'])
        result = learn_result(self.role, self.trainer, self.entry, life_registry=self.registry)
        self.assertFalse(result.changed)
        self.assertEqual(self.role['life_skills'], state_before)

    def test_learn_level_requirement_rejected(self):
        object.__setattr__(self.entry, 'level_requirement', 2)
        try:
            self.role['level'] = 1
            result = learn_result(self.role, self.trainer, self.entry, life_registry=self.registry)
            self.assertFalse(result.changed)
        finally:
            object.__setattr__(self.entry, 'level_requirement', 1)

    def test_learn_insufficient_silver_rejected(self):
        self.role['currencies']['silver'] = self.entry.silver_cost - 1
        result = learn_result(self.role, self.trainer, self.entry, life_registry=self.registry)
        self.assertFalse(result.changed)

    def test_learn_insufficient_experience_rejected(self):
        # Use entry 5003 which has experience_cost=200 (non-zero) to test the guard.
        entry = self.registry.learnable[5003]
        trainer = next(t for t in self.registry.trainers.values() if t.teaches(5003))
        self.role['experience'] = 0
        result = learn_result(self.role, trainer, entry, life_registry=self.registry)
        self.assertFalse(result.changed)

    def test_learn_wrong_trainer_context_rejected(self):
        other = self.registry.trainers[7001]
        wrong = copy.deepcopy(other)
        object.__setattr__(wrong, 'entry_ids', ())
        result = learn_result(self.role, wrong, self.entry, life_registry=self.registry)
        self.assertFalse(result.changed)

    def test_learn_save_failure_rolls_back(self):
        with tempfile.TemporaryDirectory() as directory:
            settings = Settings(role_data_file=str(Path(directory) / 'roles.json'))
            server = LocalGameServer(settings)
            role = server.roles.roles_for('life-learn')[0]
            role['experience'] = 10_000
            ensure_life_skills(role, settings.life_registry)
            before = copy.deepcopy(role)
            fields = decode_frame(encode_frame(1143, [byte(3), integer(5001)]))[1]
            with mock.patch.object(server.roles, 'save', side_effect=OSError('disk full')):
                with self.assertRaises(OSError):
                    server.handle_life_learn(role, fields, trainer_id=7001)
            self.assertEqual(role, before)


class LifeUpgradeBusinessTests(unittest.TestCase):
    def setUp(self):
        self.settings = Settings()
        self.registry = self.settings.life_registry
        self.skill = self.registry.skills[ALCHEMY_SKILL_ID]
        self.role = default_role(self.settings)
        self.role['experience'] = 100_000
        ensure_life_skills(self.role, self.settings.life_registry)
        self.role['life_skills']['skills'][str(ALCHEMY_SKILL_ID)] = {
            'level': 1, 'proficiency': self.skill.upgrade_proficiency_required,
        }

    def test_successful_upgrade_deducts_silver_exp_and_resets_proficiency(self):
        silver_before = self.role['currencies']['silver']
        exp_before = int(self.role['experience'])
        result = upgrade_result(self.role, self.skill, life_registry=self.registry)
        self.assertTrue(result.changed)
        state = self.role['life_skills']['skills'][str(ALCHEMY_SKILL_ID)]
        self.assertEqual(state['level'], 2)
        self.assertEqual(state['proficiency'], 0)
        self.assertEqual(self.role['currencies']['silver'], silver_before - self.skill.upgrade_silver_cost(2))
        self.assertEqual(int(self.role['experience']), exp_before - self.skill.upgrade_exp_cost(2))
        frame_ids = [decode_frame(f)[0] for f in result.frames]
        self.assertIn(1132, frame_ids)
        self.assertIn(1017, frame_ids)

    def test_upgrade_without_skill_rejected(self):
        del self.role['life_skills']['skills'][str(ALCHEMY_SKILL_ID)]
        result = upgrade_result(self.role, self.skill, life_registry=self.registry)
        self.assertFalse(result.changed)

    def test_upgrade_proficiency_insufficient_rejected(self):
        self.role['life_skills']['skills'][str(ALCHEMY_SKILL_ID)]['proficiency'] = 0
        result = upgrade_result(self.role, self.skill, life_registry=self.registry)
        self.assertFalse(result.changed)

    def test_upgrade_at_level_cap_rejected(self):
        self.role['life_skills']['skills'][str(ALCHEMY_SKILL_ID)] = {
            'level': self.skill.max_level, 'proficiency': 9999,
        }
        result = upgrade_result(self.role, self.skill, life_registry=self.registry)
        self.assertFalse(result.changed)

    def test_upgrade_insufficient_silver_and_exp_rejected(self):
        self.role['currencies']['silver'] = 0
        result = upgrade_result(self.role, self.skill, life_registry=self.registry)
        self.assertFalse(result.changed)
        self.role['currencies']['silver'] = 10_000_000
        self.role['experience'] = 0
        result = upgrade_result(self.role, self.skill, life_registry=self.registry)
        self.assertFalse(result.changed)

    def test_upgrade_save_failure_rolls_back(self):
        with tempfile.TemporaryDirectory() as directory:
            settings = Settings(role_data_file=str(Path(directory) / 'roles.json'))
            server = LocalGameServer(settings)
            role = server.roles.roles_for('life-upgrade')[0]
            role['experience'] = 100_000
            ensure_life_skills(role, settings.life_registry)
            skill = settings.life_registry.skills[ALCHEMY_SKILL_ID]
            role['life_skills']['skills'][str(ALCHEMY_SKILL_ID)] = {
                'level': 1, 'proficiency': skill.upgrade_proficiency_required,
            }
            before = copy.deepcopy(role)
            fields = decode_frame(encode_frame(1132, [byte(6), integer(ALCHEMY_SKILL_ID)]))[1]
            with mock.patch.object(server.roles, 'save', side_effect=OSError('disk full')):
                with self.assertRaises(OSError):
                    server.handle_life_upgrade(role, fields)
            self.assertEqual(role, before)


if __name__ == '__main__':
    unittest.main()
