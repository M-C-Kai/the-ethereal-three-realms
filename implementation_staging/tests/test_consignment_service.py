from __future__ import annotations

import copy
import tempfile
import unittest
from pathlib import Path

from consignment_service import ConsignmentService, consignment_category_id


class Registry:
    def __init__(self):
        self.defs = {
            10_000_001: {'equipment_slot': 10, 'kind': 'equipment', 'icon_code': 21001, 'quality': 1, 'name': '长枪'},
            17_090_100: {'equipment_slot': 17, 'kind': 'equipment', 'icon_code': 41002, 'quality': 2, 'name': '辟邪'},
            30_140_011: {'equipment_slot': 3, 'kind': 'equipment', 'icon_code': 14001, 'quality': 1, 'name': '铠甲'},
            260_000_001: {'equipment_slot': 0, 'kind': 'material', 'icon_code': 30001, 'quality': 0, 'name': '材料'},
            250_000_001: {'equipment_slot': 0, 'kind': 'consumable', 'icon_code': 30002, 'quality': 0, 'name': '道具'},
        }

    def resolve(self, item):
        return {**self.defs[int(item['template_id'])], **item}


class RoleStore:
    def __init__(self, roles):
        self.data = {'accounts': {'seller': [roles[0]], 'buyer': [roles[1]]}}
        self.save_count = 0

    def save(self):
        self.save_count += 1


def make_role(role_id: int, name: str, silver: int = 10_000, capacity: int = 20):
    return {
        'id': role_id,
        'name': name,
        'bag_capacity': capacity,
        'currencies': {'silver': silver},
        'items': [],
    }


class ConsignmentServiceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / 'consignment_listings.json'
        self.registry = Registry()
        self.seller = make_role(10001, '卖家')
        self.buyer = make_role(10002, '买家')
        self.roles = RoleStore([self.seller, self.buyer])
        self.service = ConsignmentService(self.path, self.roles, self.registry)

    def tearDown(self):
        self.tmp.cleanup()

    def test_whole_item_is_escrowed_and_survives_reload(self):
        item = {'id': 9001, 'template_id': 17_090_100, 'quantity': 1, 'location': 'bag'}
        self.seller['items'].append(item)
        result = self.service.list_item(self.seller, 9001, 1, 500)
        self.assertTrue(result.changed, result.reason)
        self.assertEqual(self.seller['items'], [])
        self.assertEqual(result.listing['item_instance_id'], 9001)
        self.assertEqual(result.listing['item']['id'], 9001)
        self.assertEqual(result.listing['item']['location'], 'consignment')

        reloaded = ConsignmentService(self.path, self.roles, self.registry)
        rows = reloaded.my_listings(10001)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['item_instance_id'], 9001)

    def test_partial_stack_splits_unique_escrow_instance(self):
        self.seller['items'].append({'id': 9001, 'template_id': 260_000_001, 'quantity': 10, 'location': 'bag'})
        self.buyer['items'].append({'id': 9002, 'template_id': 250_000_001, 'quantity': 1, 'location': 'bag'})
        result = self.service.list_item(self.seller, 9001, 3, 50)
        self.assertTrue(result.changed, result.reason)
        self.assertEqual(self.seller['items'][0]['quantity'], 7)
        escrow_id = result.listing['item_instance_id']
        self.assertNotIn(escrow_id, {9001, 9002})
        self.assertEqual(result.listing['item']['quantity'], 3)

    def test_unlist_returns_same_instance_and_full_bag_is_atomic(self):
        self.seller['items'].append({'id': 9001, 'template_id': 17_090_100, 'quantity': 1, 'location': 'bag'})
        listed = self.service.list_item(self.seller, 9001, 1, 500)
        item_id = listed.listing['item_instance_id']
        self.seller['bag_capacity'] = 0
        failed = self.service.unlist(self.seller, item_id)
        self.assertFalse(failed.changed)
        self.assertEqual(self.service.my_listings(10001)[0]['status'], 'active')

        self.seller['bag_capacity'] = 20
        result = self.service.unlist(self.seller, item_id)
        self.assertTrue(result.changed, result.reason)
        returned = next(item for item in self.seller['items'] if int(item['id']) == item_id)
        self.assertEqual(returned['location'], 'bag')
        self.assertEqual(result.listing['status'], 'cancelled')

    def test_buy_transfers_same_instance_and_silver_once(self):
        self.seller['items'].append({'id': 9001, 'template_id': 17_090_100, 'quantity': 2, 'location': 'bag'})
        listed = self.service.list_item(self.seller, 9001, 2, 500)
        item_id = listed.listing['item_instance_id']
        result = self.service.buy(self.buyer, item_id)
        self.assertTrue(result.changed, result.reason)
        self.assertEqual(self.buyer['currencies']['silver'], 9000)
        self.assertEqual(self.seller['currencies']['silver'], 11000)
        bought = next(item for item in self.buyer['items'] if int(item['id']) == item_id)
        self.assertEqual(bought['location'], 'bag')
        self.assertEqual(bought['quantity'], 2)
        self.assertEqual(result.listing['status'], 'sold')

        buyer_snapshot = copy.deepcopy(self.buyer)
        seller_snapshot = copy.deepcopy(self.seller)
        repeated = self.service.buy(self.buyer, item_id)
        self.assertFalse(repeated.changed)
        self.assertEqual(self.buyer, buyer_snapshot)
        self.assertEqual(self.seller, seller_snapshot)

    def test_self_buy_insufficient_silver_and_full_bag_do_not_mutate(self):
        self.seller['items'].append({'id': 9001, 'template_id': 17_090_100, 'quantity': 1, 'location': 'bag'})
        listed = self.service.list_item(self.seller, 9001, 1, 5000)
        item_id = listed.listing['item_instance_id']
        self.assertFalse(self.service.buy(self.seller, item_id).changed)
        self.buyer['currencies']['silver'] = 1
        self.assertFalse(self.service.buy(self.buyer, item_id).changed)
        self.buyer['currencies']['silver'] = 10_000
        self.buyer['bag_capacity'] = 0
        self.assertFalse(self.service.buy(self.buyer, item_id).changed)
        self.assertEqual(self.service.my_listings(10001)[0]['status'], 'active')

    def test_search_quality_counts_and_categories(self):
        weapon = {'id': 9001, 'template_id': 10_000_001, 'quantity': 1, 'location': 'bag'}
        mount = {'id': 9002, 'template_id': 17_090_100, 'quantity': 1, 'location': 'bag'}
        armor = {'id': 9003, 'template_id': 30_140_011, 'quantity': 1, 'location': 'bag'}
        material = {'id': 9004, 'template_id': 260_000_001, 'quantity': 1, 'location': 'bag'}
        tool = {'id': 9005, 'template_id': 250_000_001, 'quantity': 1, 'location': 'bag'}
        self.assertEqual(consignment_category_id(weapon, self.registry), 1)
        self.assertEqual(consignment_category_id(mount, self.registry), 24)
        self.assertEqual(consignment_category_id(armor, self.registry), 16)
        self.assertEqual(consignment_category_id(material, self.registry), 27)
        self.assertEqual(consignment_category_id(tool, self.registry), 26)

        self.seller['items'].extend([weapon, mount, armor])
        self.service.list_item(self.seller, 9001, 1, 100)
        self.service.list_item(self.seller, 9002, 1, 200)
        self.service.list_item(self.seller, 9003, 1, 300)
        self.assertEqual(len(self.service.search(0)), 1)  # all weapons
        self.assertEqual(len(self.service.search(24)), 1)
        self.assertEqual(self.service.quality_counts(24), [1, 0, 0, 1, 0, 0])


if __name__ == '__main__':
    unittest.main()
