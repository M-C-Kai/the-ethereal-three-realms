import unittest

from item_registry import default_item_registry, deprecated_mount_template_ids
from mount_constructor import (
    MOUNT_STAGE_DIVINE,
    MOUNT_STAGE_IMMORTAL,
    MOUNT_STAGE_NORMAL,
    MOUNT_STAGE_SPIRIT,
    construct_mount_state,
    create_mount_item_instance,
    mount_ride_code_for_role,
)


class MountConstructorTests(unittest.TestCase):
    def setUp(self):
        self.registry = default_item_registry()

    def test_41010_four_stage_chain(self):
        expected = [1010, 1020, 1030, 4010]
        for stage, ride_code in enumerate(expected):
            item = create_mount_item_instance(
                instance_id=10000 + stage,
                series_id=41010,
                stage=stage,
            )
            state = construct_mount_state(item, self.registry)
            self.assertIsNotNone(state)
            self.assertEqual(state.ride_code, ride_code)

    def test_42004_reuses_normal_until_divine(self):
        expected = {
            MOUNT_STAGE_NORMAL: 2004,
            MOUNT_STAGE_SPIRIT: 2004,
            MOUNT_STAGE_IMMORTAL: 2004,
            MOUNT_STAGE_DIVINE: 3002,
        }
        for stage, ride_code in expected.items():
            item = create_mount_item_instance(
                instance_id=11000 + stage,
                series_id=42004,
                stage=stage,
            )
            state = construct_mount_state(item, self.registry)
            self.assertEqual(state.ride_code, ride_code)

    def test_same_series_can_exist_at_different_stages(self):
        bag_mount = create_mount_item_instance(
            instance_id=12001,
            series_id=41004,
            stage=MOUNT_STAGE_SPIRIT,
            grade=8,
            location='bag',
        )
        equipped_mount = create_mount_item_instance(
            instance_id=12002,
            series_id=41004,
            stage=MOUNT_STAGE_DIVINE,
            grade=18,
            location='equipped',
        )
        bag_state = construct_mount_state(bag_mount, self.registry)
        equipped_state = construct_mount_state(equipped_mount, self.registry)
        self.assertEqual(bag_state.ride_code, 1014)
        self.assertEqual(equipped_state.ride_code, 1034)
        self.assertEqual(bag_state.grade, 8)
        self.assertEqual(equipped_state.grade, 18)
        role = {'id': 10001, 'items': [bag_mount, equipped_mount], 'mount_model': 0}
        self.assertEqual(mount_ride_code_for_role(role, self.registry), 1034)

    def test_mount_is_a_real_bag_item_until_equipped(self):
        item = create_mount_item_instance(instance_id=13001, series_id=41002)
        self.assertEqual(item['location'], 'bag')
        self.assertIn('mount_state', item)
        item['location'] = 'equipped'
        role = {'id': 10001, 'items': [item], 'mount_model': 0}
        self.assertEqual(mount_ride_code_for_role(role, self.registry), 1002)

    def test_future_mount_items_are_not_permanently_deprecated(self):
        self.assertEqual(deprecated_mount_template_ids(), frozenset())


if __name__ == '__main__':
    unittest.main()
