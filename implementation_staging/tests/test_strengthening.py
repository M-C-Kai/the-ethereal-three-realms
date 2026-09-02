import copy
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from strengthening import (  # noqa: E402
    INITIAL_STRENGTHEN_STONE_TEMPLATE_ID,
    MIDDLE_STRENGTHEN_STONE_TEMPLATE_ID,
    is_strengthening_stone,
    normalized_strengthen_level,
    rate_for,
    recalculate_equipment_attributes,
    stone_definition_for,
    strengthening_failure_level,
    strengthening_success,
    total_strengthening_rate,
)
from protocol import decode_frame, field_values  # noqa: E402
from server import (  # noqa: E402
    RoleStore,
    Settings,
    combat_stats,
    default_role,
    equipped_weapon_attack,
    item_description_frame,
    item_detail_frame,
    item_frame,
    strengthening_equipment_frame,
    strengthening_open_frame,
    strengthening_rate_frame,
    strengthening_action_result,
    strengthening_reset_frame,
    strengthening_stone_selection_frame,
)


class StrengtheningRuleTests(unittest.TestCase):
    def test_only_configured_stones_in_apk_range_are_recognized(self):
        initial = {"template_id": INITIAL_STRENGTHEN_STONE_TEMPLATE_ID}
        middle = {"template_id": MIDDLE_STRENGTHEN_STONE_TEMPLATE_ID}

        self.assertTrue(is_strengthening_stone(initial))
        self.assertTrue(is_strengthening_stone(middle))
        self.assertEqual(stone_definition_for(initial).name, "初级强化石")
        self.assertEqual(stone_definition_for(middle).name, "中级强化石")
        self.assertFalse(is_strengthening_stone({"template_id": 322_260_001}))
        self.assertFalse(is_strengthening_stone({"template_id": 322_259_999}))
        self.assertFalse(is_strengthening_stone({"template_id": 322_261_003}))

    def test_rate_tables_keep_five_stones_selectable_at_every_level(self):
        initial = stone_definition_for(
            {"template_id": INITIAL_STRENGTHEN_STONE_TEMPLATE_ID}
        )
        middle = stone_definition_for(
            {"template_id": MIDDLE_STRENGTHEN_STONE_TEMPLATE_ID}
        )

        initial_rates = [rate_for(initial, level) for level in range(9)]
        middle_rates = [rate_for(middle, level) for level in range(9)]
        self.assertEqual(initial_rates, [
            2000,
            1800,
            1600,
            1400,
            1200,
            1000,
            800,
            600,
            400,
        ])
        self.assertEqual(middle_rates, [
            2500,
            2200,
            2000,
            1800,
            1600,
            1400,
            1200,
            900,
            600,
        ])
        for rate in initial_rates + middle_rates:
            apk_maximum = 1 if rate >= 10000 else min(5, 10000 // rate + 1)
            self.assertEqual(apk_maximum, 5)

    def test_one_to_five_stones_increase_displayed_and_actual_rate(self):
        initial = stone_definition_for(
            {"template_id": INITIAL_STRENGTHEN_STONE_TEMPLATE_ID}
        )
        middle = stone_definition_for(
            {"template_id": MIDDLE_STRENGTHEN_STONE_TEMPLATE_ID}
        )

        self.assertEqual(
            [total_strengthening_rate(rate_for(initial, 0), count) for count in range(1, 6)],
            [2000, 4000, 6000, 8000, 10000],
        )
        self.assertEqual(
            [total_strengthening_rate(rate_for(middle, 0), count) for count in range(1, 6)],
            [2500, 5000, 7500, 10000, 10000],
        )

    def test_multiple_stones_add_rate_and_cap_at_one_hundred_percent(self):
        self.assertEqual(total_strengthening_rate(1200, 3), 3600)
        self.assertEqual(total_strengthening_rate(7000, 2), 10000)

    def test_malformed_strengthen_levels_normalize_to_zero(self):
        self.assertEqual(normalized_strengthen_level({}), 0)
        self.assertEqual(normalized_strengthen_level({"strengthen_level": True}), 0)
        self.assertEqual(normalized_strengthen_level({"strengthen_level": "6"}), 0)
        self.assertEqual(normalized_strengthen_level({"strengthen_level": -1}), 0)
        self.assertEqual(normalized_strengthen_level({"strengthen_level": 10}), 0)
        self.assertEqual(normalized_strengthen_level({"strengthen_level": 6}), 6)

    def test_failure_floors_match_apk_help_tiers(self):
        expected = {
            0: 0,
            1: 1,
            2: 2,
            3: 3,
            4: 3,
            5: 3,
            6: 6,
            7: 6,
            8: 6,
            9: 9,
        }
        self.assertEqual(
            {level: strengthening_failure_level(level) for level in expected},
            expected,
        )

    def test_recalculation_preserves_base_and_applies_attack_bonus(self):
        weapon = {
            "equipment_attributes": [3, 2, 1, 0],
            "strengthen_level": 4,
        }

        recalculate_equipment_attributes(weapon)

        self.assertEqual(weapon["base_equipment_attributes"], [3, 2, 1, 0])
        self.assertEqual(weapon["equipment_attributes"], [8, 2, 1, 0])

        weapon["strengthen_level"] = 6
        recalculate_equipment_attributes(weapon)
        self.assertEqual(weapon["base_equipment_attributes"], [3, 2, 1, 0])
        self.assertEqual(weapon["equipment_attributes"], [13, 2, 1, 0])

    def test_success_uses_zero_based_random_boundary(self):
        initial = stone_definition_for(
            {"template_id": INITIAL_STRENGTHEN_STONE_TEMPLATE_ID}
        )

        self.assertTrue(strengthening_success(initial, 8, 1, FixedRng(399)))
        self.assertFalse(strengthening_success(initial, 8, 1, FixedRng(400)))
        self.assertTrue(strengthening_success(initial, 8, 5, FixedRng(1999)))
        self.assertFalse(strengthening_success(initial, 8, 5, FixedRng(2000)))


class StrengtheningInventoryMigrationTests(unittest.TestCase):
    def test_new_role_receives_one_thousand_of_each_stone(self):
        role = default_role(Settings())

        stones = self._stones_by_template(role)

        self.assertTrue(role.get("strengthening_stones_initialized"))
        self.assertEqual(set(stones), {
            INITIAL_STRENGTHEN_STONE_TEMPLATE_ID,
            MIDDLE_STRENGTHEN_STONE_TEMPLATE_ID,
        })
        self.assertEqual(
            [stones[template_id]["quantity"] for template_id in sorted(stones)],
            [1000, 1000],
        )
        self.assertEqual(
            [stones[template_id]["max_quantity"] for template_id in sorted(stones)],
            [9999, 9999],
        )
        for stone in stones.values():
            _, fields = decode_frame(item_frame(stone))
            values = field_values(fields)
            self.assertEqual(values[2], 1000)
            self.assertEqual(values[9] & 0x40, 0x40)

    def test_legacy_stones_gain_stackable_flag_without_losing_other_flags(self):
        role = default_role(Settings())
        stones = self._stones_by_template(role)
        for stone in stones.values():
            stone["item_flags"] = 0x02

        self.assertTrue(RoleStore._ensure_items(role))

        for stone in stones.values():
            self.assertEqual(stone["item_flags"], 0x42)

    def test_legacy_role_gets_only_missing_stone_and_is_marked_initialized(self):
        role = default_role(Settings())
        role.pop("strengthening_stones_initialized")
        initial = self._stones_by_template(role)[INITIAL_STRENGTHEN_STONE_TEMPLATE_ID]
        initial["quantity"] = 7
        initial["location"] = "warehouse"
        role["items"] = [
            item
            for item in role["items"]
            if item.get("template_id") != MIDDLE_STRENGTHEN_STONE_TEMPLATE_ID
        ]

        self.assertTrue(RoleStore._ensure_items(role))
        stones = self._stones_by_template(role)

        self.assertTrue(role.get("strengthening_stones_initialized"))
        self.assertEqual(initial["quantity"], 7)
        self.assertEqual(initial["location"], "warehouse")
        self.assertEqual(stones[MIDDLE_STRENGTHEN_STONE_TEMPLATE_ID]["quantity"], 1000)

    def test_initialized_role_does_not_regain_a_deleted_stone(self):
        role = default_role(Settings())
        role["items"] = [
            item
            for item in role["items"]
            if item.get("template_id") != INITIAL_STRENGTHEN_STONE_TEMPLATE_ID
        ]

        RoleStore._ensure_items(role)

        self.assertNotIn(
            INITIAL_STRENGTHEN_STONE_TEMPLATE_ID,
            self._stones_by_template(role),
        )

    def test_strengthening_state_survives_default_catalogue_merge(self):
        role = default_role(Settings())
        weapon = next(item for item in role["items"] if item.get("equipment_slot") == 10)
        weapon["strengthen_level"] = 4
        weapon["base_equipment_attributes"] = [3, 0, 0, 0]
        weapon["equipment_attributes"] = [8, 0, 0, 0]

        RoleStore._ensure_items(role)
        migrated_weapon = next(
            item for item in role["items"] if item.get("equipment_slot") == 10
        )

        self.assertEqual(migrated_weapon["strengthen_level"], 4)
        self.assertEqual(migrated_weapon["base_equipment_attributes"], [3, 0, 0, 0])
        self.assertEqual(migrated_weapon["equipment_attributes"], [8, 0, 0, 0])

    def test_legacy_weapon_current_attributes_become_stable_strengthening_base(self):
        role = default_role(Settings())
        weapon = next(item for item in role["items"] if item.get("equipment_slot") == 10)
        weapon.pop("strengthen_level")
        weapon.pop("base_equipment_attributes")
        weapon["equipment_attributes"] = [9, 2, 1, 0]

        RoleStore._ensure_items(role)

        self.assertEqual(weapon["strengthen_level"], 0)
        self.assertEqual(weapon["base_equipment_attributes"], [9, 2, 1, 0])
        self.assertEqual(weapon["equipment_attributes"], [9, 2, 1, 0])

    def test_legacy_starter_weapon_derives_missing_base_from_effective_level(self):
        role = default_role(Settings())
        weapon = next(item for item in role["items"] if item.get("equipment_slot") == 10)
        weapon.pop("base_equipment_attributes")
        weapon["strengthen_level"] = 4
        weapon["equipment_attributes"] = [16, 2, 1, 0]

        RoleStore._ensure_items(role)

        self.assertEqual(weapon["strengthen_level"], 4)
        self.assertEqual(weapon["base_equipment_attributes"], [11, 2, 1, 0])
        self.assertEqual(weapon["equipment_attributes"], [16, 2, 1, 0])

    def test_custom_id_weapon_is_migrated_and_recalculated_without_drift(self):
        role = default_role(Settings())
        custom_weapon = {
            "id": 987654321,
            "template_id": 100_001_001,
            "name": "旧档自制剑",
            "location": "bag",
            "equipment_slot": 10,
            "strengthen_level": 4,
            "equipment_attributes": [16, 2, 1, 0],
        }
        role["items"].append(custom_weapon)

        RoleStore._ensure_items(role)

        self.assertEqual(custom_weapon["strengthen_level"], 4)
        self.assertEqual(custom_weapon["base_equipment_attributes"], [11, 2, 1, 0])
        self.assertEqual(custom_weapon["equipment_attributes"], [16, 2, 1, 0])
        RoleStore._ensure_items(role)
        self.assertEqual(custom_weapon["equipment_attributes"], [16, 2, 1, 0])

    def test_fixed_stone_id_collision_reassigns_old_item_and_keeps_ids_unique(self):
        role = default_role(Settings())
        role.pop("strengthening_stones_initialized")
        role["items"] = [
            item for item in role["items"] if not is_strengthening_stone(item)
        ]
        conflicting_item = {
            "id": int(role["id"]) * 100 + 18,
            "template_id": 260_000_001,
            "name": "旧档冲突道具",
            "quantity": 4,
            "location": "bag",
        }
        role["items"].append(conflicting_item)

        RoleStore._ensure_items(role)

        item_ids = [int(item["id"]) for item in role["items"]]
        stones = self._stones_by_template(role)
        self.assertEqual(len(item_ids), len(set(item_ids)))
        self.assertNotEqual(conflicting_item["id"], int(role["id"]) * 100 + 18)
        self.assertEqual(conflicting_item["quantity"], 4)
        self.assertEqual(
            stones[INITIAL_STRENGTHEN_STONE_TEMPLATE_ID]["id"],
            int(role["id"]) * 100 + 18,
        )

    @staticmethod
    def _stones_by_template(role):
        return {
            item["template_id"]: item
            for item in role.get("items", [])
            if isinstance(item, dict) and is_strengthening_stone(item)
        }


class StrengtheningFrameTests(unittest.TestCase):
    def setUp(self):
        self.role = default_role(Settings())
        self.weapon = next(
            item for item in self.role["items"] if item.get("equipment_slot") == 10
        )
        self.initial_stone = next(
            item
            for item in self.role["items"]
            if item.get("template_id") == INITIAL_STRENGTHEN_STONE_TEMPLATE_ID
        )

    def test_open_select_rate_and_reset_frames_match_apk_actions(self):
        self.weapon["strengthen_level"] = 4
        recalculate_equipment_attributes(self.weapon)

        _, open_fields = decode_frame(strengthening_open_frame())
        self.assertEqual(
            self._decoded_values(strengthening_open_frame()),
            (1009, [97, "请选择需要强化的装备和强化宝石。"]),
        )
        self.assertEqual([field.type_id for field in open_fields], [3, 6])
        equipment_message, equipment_values = self._decoded_values(
            strengthening_equipment_frame(self.weapon)
        )
        _, equipment_fields = decode_frame(strengthening_equipment_frame(self.weapon))
        self.assertEqual(equipment_message, 1009)
        self.assertEqual(equipment_values[0], 75)
        self.assertEqual([field.type_id for field in equipment_fields], [3, 6])
        self.assertIn("青锋剑 +4", equipment_values[1])
        self.assertIn("当前攻击：8", equipment_values[1])

        rate_message, rate_values = self._decoded_values(
            strengthening_rate_frame(self.weapon, self.initial_stone)
        )
        _, rate_fields = decode_frame(
            strengthening_rate_frame(self.weapon, self.initial_stone)
        )
        self.assertEqual(rate_message, 1009)
        self.assertEqual(rate_values[:2], [74, 1200])
        self.assertEqual([field.type_id for field in rate_fields], [3, 3, 6])
        self.assertIn("12.00%", rate_values[2])

        _, reset_fields = decode_frame(strengthening_reset_frame())
        self.assertEqual(
            self._decoded_values(strengthening_reset_frame()),
            (1009, [78]),
        )
        self.assertEqual([field.type_id for field in reset_fields], [3])

    def test_action77_clear_directives_use_confirmed_shapes(self):
        _, valid_fields = decode_frame(strengthening_stone_selection_frame(True))
        _, invalid_fields = decode_frame(strengthening_stone_selection_frame(False))
        self.assertEqual(
            self._decoded_values(strengthening_stone_selection_frame(True)),
            (1009, [77, 1, 1]),
        )
        self.assertEqual(
            self._decoded_values(strengthening_stone_selection_frame(False)),
            (1009, [77, 0]),
        )
        self.assertEqual([field.type_id for field in valid_fields], [3, 2, 2])
        self.assertEqual([field.type_id for field in invalid_fields], [3, 2])

    def test_invalid_selection_actions_keep_their_native_response_shapes(self):
        invalid_equipment = strengthening_action_result(self.role, [75, 999999999])
        invalid_rate = strengthening_action_result(
            self.role,
            [74, self.weapon["id"], 999999999],
        )

        equipment_message, equipment_fields = decode_frame(invalid_equipment.frames[0])
        rate_message, rate_fields = decode_frame(invalid_rate.frames[0])
        self.assertEqual(equipment_message, 1009)
        self.assertEqual(field_values(equipment_fields)[0], 75)
        self.assertEqual([field.type_id for field in equipment_fields], [3, 6])
        self.assertEqual(rate_message, 1009)
        self.assertEqual(field_values(rate_fields)[:2], [74, 0])
        self.assertEqual([field.type_id for field in rate_fields], [3, 3, 6])

    def test_strengthening_is_visible_without_extending_1008_layout(self):
        self.weapon["strengthen_level"] = 4
        recalculate_equipment_attributes(self.weapon)

        item_message, item_values = self._decoded_values(item_frame(self.weapon))
        self.assertEqual(item_message, 1008)
        self.assertEqual(len(item_values), 35)
        self.assertEqual(item_values[8], "青锋剑 +4")
        self.assertEqual(item_values[16:20], [8, 0, 0, 0])

        description = self._decoded_values(item_description_frame(self.weapon))[1][2]
        detail = self._decoded_values(item_detail_frame(self.weapon))[1][3]
        self.assertIn("强化：+4", description)
        self.assertIn("当前攻击：8", description)
        self.assertIn("强化：+4", detail)

    @staticmethod
    def _decoded_values(frame):
        message_id, fields = decode_frame(frame)
        return message_id, field_values(fields)


class StrengtheningTransactionTests(unittest.TestCase):
    def setUp(self):
        self.role = default_role(Settings())
        self.weapon = next(
            item for item in self.role["items"] if item.get("equipment_slot") == 10
        )
        self.armour = next(
            item for item in self.role["items"] if item.get("equipment_slot") == 3
        )
        self.stone = next(
            item
            for item in self.role["items"]
            if item.get("template_id") == INITIAL_STRENGTHEN_STONE_TEMPLATE_ID
        )

    def test_read_only_actions_return_native_frames_without_mutating_role(self):
        requests = (
            ([97], [97]),
            ([75, self.weapon["id"]], [75]),
            ([74, self.weapon["id"], self.stone["id"]], [74, 2000]),
        )

        for request, expected_prefix in requests:
            with self.subTest(action=request[0]):
                result = strengthening_action_result(self.role, request)
                self.assertFalse(result.changed)
                values = field_values(decode_frame(result.frames[0])[1])
                self.assertEqual(values[:len(expected_prefix)], expected_prefix)

    def test_valid_action77_is_silent_so_apk_keeps_both_selected_items(self):
        result = strengthening_action_result(
            self.role,
            [77, self.weapon["id"], self.stone["id"]],
        )

        self.assertFalse(result.changed)
        self.assertEqual(result.frames, ())

    def test_success_consumes_stones_levels_weapon_and_refreshes_before_reset(self):
        self.weapon["strengthen_level"] = 4
        recalculate_equipment_attributes(self.weapon)
        self.stone["quantity"] = 3

        result = strengthening_action_result(
            self.role,
            [92, self.weapon["id"], self.stone["id"], 2],
            rng=FixedRng(0),
        )

        self.assertTrue(result.changed)
        self.assertEqual(self.weapon["strengthen_level"], 5)
        self.assertEqual(self.weapon["equipment_attributes"], [10, 0, 0, 0])
        self.assertEqual(self.stone["quantity"], 1)
        decoded = [self._decoded(frame) for frame in result.frames]
        self.assertEqual([message_id for message_id, _ in decoded], [1008, 1008, 1049, 1009])
        self.assertEqual(decoded[-1], (1009, [78]))
        self.assertNotIn((1009, [92]), decoded)
        self.assertIn("成功", result.message)

    def test_failure_consumes_stone_and_drops_to_confirmed_tier_floor(self):
        self.weapon["strengthen_level"] = 5
        recalculate_equipment_attributes(self.weapon)

        result = strengthening_action_result(
            self.role,
            [92, self.weapon["id"], self.stone["id"], 1],
            rng=FixedRng(9999),
        )

        self.assertTrue(result.changed)
        self.assertEqual(self.weapon["strengthen_level"], 3)
        self.assertEqual(self.weapon["equipment_attributes"], [6, 0, 0, 0])
        self.assertEqual(self.stone["quantity"], 999)
        self.assertIn("失败", result.message)

    def test_last_stone_sends_zero_quantity_update_then_existing_delete_action(self):
        self.weapon["strengthen_level"] = 8
        recalculate_equipment_attributes(self.weapon)
        self.stone["quantity"] = 1

        result = strengthening_action_result(
            self.role,
            [92, self.weapon["id"], self.stone["id"], 1],
            rng=FixedRng(9999),
        )

        self.assertNotIn(self.stone, self.role["items"])
        decoded = [self._decoded(frame) for frame in result.frames]
        self.assertEqual([message_id for message_id, _ in decoded], [
            1008,
            1008,
            1009,
            1049,
            1009,
        ])
        self.assertEqual(decoded[1][1][2], 0)
        self.assertEqual(decoded[2], (1009, [3, self.stone["id"]]))
        self.assertEqual(decoded[-1], (1009, [78]))

    def test_invalid_execution_is_atomic_and_resets_ui(self):
        invalid_requests = (
            [92, self.armour["id"], self.stone["id"], 1],
            [92, self.weapon["id"], self.stone["id"], 0],
            [92, self.weapon["id"], self.stone["id"], 6],
            [92, self.weapon["id"], 999999999, 1],
        )

        for request in invalid_requests:
            with self.subTest(request=request):
                before_level = self.weapon["strengthen_level"]
                before_quantity = self.stone["quantity"]
                result = strengthening_action_result(self.role, request, rng=FixedRng(0))
                self.assertFalse(result.changed)
                self.assertEqual(self.weapon["strengthen_level"], before_level)
                self.assertEqual(self.stone["quantity"], before_quantity)
                self.assertEqual(self._decoded(result.frames[-1]), (1009, [78]))

    def test_execution_rejects_max_level_warehouse_items_and_short_stack(self):
        cases = []

        self.weapon["strengthen_level"] = 9
        recalculate_equipment_attributes(self.weapon)
        cases.append(("max-level", [92, self.weapon["id"], self.stone["id"], 1]))

        for label, request in cases:
            with self.subTest(case=label):
                before = copy.deepcopy(self.role)
                result = strengthening_action_result(self.role, request, rng=FixedRng(0))
                self.assertFalse(result.changed)
                self.assertEqual(self.role, before)
                self.assertEqual(self._decoded(result.frames[-1]), (1009, [78]))

        self.weapon["strengthen_level"] = 0
        recalculate_equipment_attributes(self.weapon)
        for label, location_target, location in (
            ("warehouse-weapon", self.weapon, "warehouse"),
            ("warehouse-stone", self.stone, "warehouse"),
        ):
            with self.subTest(case=label):
                location_target["location"] = location
                before = copy.deepcopy(self.role)
                result = strengthening_action_result(
                    self.role,
                    [92, self.weapon["id"], self.stone["id"], 1],
                    rng=FixedRng(0),
                )
                self.assertFalse(result.changed)
                self.assertEqual(self.role, before)
                self.assertEqual(self._decoded(result.frames[-1]), (1009, [78]))
                location_target["location"] = "bag"

        self.stone["quantity"] = 4
        before = copy.deepcopy(self.role)
        result = strengthening_action_result(
            self.role,
            [92, self.weapon["id"], self.stone["id"], 5],
            rng=FixedRng(0),
        )
        self.assertFalse(result.changed)
        self.assertEqual(self.role, before)
        self.assertEqual(self._decoded(result.frames[-1]), (1009, [78]))

    def test_server_boundary_persists_only_mutating_execution(self):
        with tempfile.TemporaryDirectory() as directory:
            role_path = Path(directory) / "roles.json"
            settings = Settings(role_data_file=str(role_path))
            game_server = __import__("server").LocalGameServer(settings)
            role = game_server.roles.roles_for("strengthening-persistence")[0]
            weapon = next(item for item in role["items"] if item.get("equipment_slot") == 10)
            stone = next(
                item
                for item in role["items"]
                if item.get("template_id") == INITIAL_STRENGTHEN_STONE_TEMPLATE_ID
            )

            with mock.patch.object(
                game_server.roles,
                "save",
                wraps=game_server.roles.save,
            ) as save:
                game_server.handle_strengthening_request(role, [97])
                save.assert_not_called()
                game_server.handle_strengthening_request(
                    role,
                    [92, weapon["id"], stone["id"], 1],
                    rng=FixedRng(0),
                )
                save.assert_called_once_with()

            reloaded = RoleStore(settings).find(
                "strengthening-persistence", int(role["id"])
            )
            reloaded_weapon = next(
                item for item in reloaded["items"] if item.get("equipment_slot") == 10
            )
            self.assertEqual(reloaded_weapon["strengthen_level"], 1)

    def test_server_boundary_rolls_back_memory_when_save_fails(self):
        game_server = __import__("server").LocalGameServer(Settings())
        role = default_role(Settings())
        weapon = next(item for item in role["items"] if item.get("equipment_slot") == 10)
        stone = next(
            item
            for item in role["items"]
            if item.get("template_id") == INITIAL_STRENGTHEN_STONE_TEMPLATE_ID
        )
        before = copy.deepcopy(role)

        with mock.patch.object(game_server.roles, "save", side_effect=OSError("disk full")):
            with self.assertRaises(OSError):
                game_server.handle_strengthening_request(
                    role,
                    [92, weapon["id"], stone["id"], 1],
                    rng=FixedRng(0),
                )

        self.assertEqual(role, before)

    @staticmethod
    def _decoded(frame):
        message_id, fields = decode_frame(frame)
        return message_id, field_values(fields)


class StrengtheningCombatTests(unittest.TestCase):
    def test_only_equipped_weapon_effective_attack_contributes_to_combat(self):
        role = default_role(Settings())
        weapon = next(item for item in role["items"] if item.get("equipment_slot") == 10)
        unarmed_attack = combat_stats(role).physical_attack

        self.assertEqual(equipped_weapon_attack(role), 0)

        weapon["location"] = "equipped"
        self.assertEqual(equipped_weapon_attack(role), 3)
        self.assertEqual(combat_stats(role).physical_attack, unarmed_attack + 3)

        weapon["strengthen_level"] = 4
        recalculate_equipment_attributes(weapon)
        self.assertEqual(equipped_weapon_attack(role), 8)
        self.assertEqual(combat_stats(role).physical_attack, unarmed_attack + 8)

        weapon["location"] = "bag"
        self.assertEqual(combat_stats(role).physical_attack, unarmed_attack)


class FixedRng:
    def __init__(self, value):
        self.value = value

    def randrange(self, upper):
        if upper != 10000:
            raise AssertionError(f"unexpected random upper bound: {upper}")
        return self.value


if __name__ == "__main__":
    unittest.main()
