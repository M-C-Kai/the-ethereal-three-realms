from __future__ import annotations

import unittest
from dataclasses import dataclass

from battle.rewards import (
    BATTLE_DROP_TEMPLATE_ID,
    RewardServices,
    apply_battle_rewards,
)


@dataclass(frozen=True)
class _Definition:
    max_quantity: int = 99


class _Registry:
    def require(self, template_id: int):
        if int(template_id) != BATTLE_DROP_TEMPLATE_ID:
            raise KeyError(template_id)
        return _Definition()


class BattleRewardTests(unittest.TestCase):
    def make_services(self) -> RewardServices:
        def role_items(role):
            return role.setdefault('items', [])

        def bag_item_count(role):
            return sum(
                str(item.get('location', 'bag')) == 'bag'
                for item in role_items(role)
            )

        def bag_capacity(role):
            return int(role.get('bag_capacity', 20))

        def apply_one_level(role):
            level = int(role.get('level', 1))
            needed = level * 100
            experience = int(role.get('experience', 0))
            if experience < needed:
                return False
            role['experience'] = experience - needed
            role['level'] = level + 1
            return True

        return RewardServices(
            role_items=role_items,
            bag_item_count=bag_item_count,
            bag_capacity=bag_capacity,
            apply_one_level=apply_one_level,
            max_role_level=99,
        )

    def test_victory_adds_experience_and_new_drop(self):
        role = {
            'id': 10001,
            'level': 1,
            'experience': 0,
            'auto_level': False,
            'bag_capacity': 20,
            'items': [],
        }

        item, level_up = apply_battle_rewards(
            role,
            self.make_services(),
            registry=_Registry(),
        )

        self.assertFalse(level_up)
        self.assertEqual(role['experience'], 50)
        self.assertIsNotNone(item)
        assert item is not None
        self.assertEqual(item['template_id'], BATTLE_DROP_TEMPLATE_ID)
        self.assertEqual(item['quantity'], 1)
        self.assertIs(role['items'][0], item)

    def test_existing_drop_stacks_without_allocating_new_slot(self):
        existing = {
            'id': 1,
            'template_id': BATTLE_DROP_TEMPLATE_ID,
            'quantity': 3,
            'location': 'bag',
        }
        role = {
            'id': 10001,
            'level': 1,
            'experience': 0,
            'auto_level': False,
            'items': [existing],
        }

        item, _ = apply_battle_rewards(
            role,
            self.make_services(),
            registry=_Registry(),
        )

        self.assertIs(item, existing)
        self.assertEqual(existing['quantity'], 4)
        self.assertEqual(len(role['items']), 1)

    def test_auto_level_uses_shared_role_level_service(self):
        role = {
            'id': 10001,
            'level': 1,
            'experience': 75,
            'auto_level': True,
            'items': [],
        }

        _, level_up = apply_battle_rewards(
            role,
            self.make_services(),
            experience=50,
            registry=_Registry(),
        )

        self.assertTrue(level_up)
        self.assertEqual(role['level'], 2)
        self.assertEqual(role['experience'], 25)

    def test_full_bag_blocks_new_drop_but_not_experience(self):
        role = {
            'id': 10001,
            'level': 1,
            'experience': 0,
            'auto_level': False,
            'bag_capacity': 1,
            'items': [{'id': 2, 'template_id': 123, 'quantity': 1, 'location': 'bag'}],
        }

        item, level_up = apply_battle_rewards(
            role,
            self.make_services(),
            registry=_Registry(),
        )

        self.assertIsNone(item)
        self.assertFalse(level_up)
        self.assertEqual(role['experience'], 50)
        self.assertEqual(len(role['items']), 1)


if __name__ == '__main__':
    unittest.main()
