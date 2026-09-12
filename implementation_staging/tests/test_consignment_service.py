from __future__ import annotations
import json
import tempfile
import unittest
from pathlib import Path
from consignment_service import ConsignmentService, consignment_category_for_item

class FakeRegistry:
    def resolve(self, item):
        base = {
            'name': item.get('name', '物品'),
            'equipment_slot': item.get('equipment_slot', 0),
            'icon_code': item.get('icon_code', 0),
            'kind': item.get('kind', 'item'),
            'max_quantity': item.get('max_quantity', 99),
        }
        return base

class FakeRoleStore:
    def __init__(self, path, roles):
        self.path = Path(path)
        self.data = {'next_role_id': 20000, 'accounts': {'a': roles}}
    def save(self):
        self.path.write_text(json.dumps(self.data, ensure_ascii=False), encoding='utf-8')

def role(rid, name, silver=10000, cap=20):
    return {'id': rid, 'name': name, 'items': [], 'bag_capacity': cap,
            'currencies': {'silver': silver}}

class ConsignmentServiceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.seller = role(10001, '卖家')
        self.buyer = role(10002, '买家')
        self.store = FakeRoleStore(root/'roles.json', [self.seller, self.buyer])
        self.market_path = root/'consignment.json'
        self.registry = FakeRegistry()
        self.service = ConsignmentService(self.store, self.registry, self.market_path)
    def tearDown(self):
        self.tmp.cleanup()

    def test_whole_item_is_escrowed_and_restart_persists(self):
        item = {'id': 501, 'template_id': 1, 'quantity': 1, 'location': 'bag',
                'equipment_slot': 1, 'name': '头盔'}
        self.seller['items'].append(item)
        result = self.service.list_item(self.seller, 501, 1, 500)
        self.assertTrue(result.ok)
        self.assertEqual(item['location'], 'consignment')
        self.assertEqual(self.service.search(14)[0]['item_instance_id'], 501)
        again = ConsignmentService(self.store, self.registry, self.market_path)
        self.assertEqual(again.my_listings(10001)[0]['item_instance_id'], 501)

    def test_partial_stack_allocates_unique_escrow_instance(self):
        item = {'id': 600, 'template_id': 2, 'quantity': 10, 'location': 'bag',
                'kind': '材料', 'name': '玄铁'}
        self.seller['items'].append(item)
        result = self.service.list_item(self.seller, 600, 3, 25)
        self.assertTrue(result.ok)
        self.assertEqual(item['quantity'], 7)
        self.assertNotEqual(result.item['id'], 600)
        self.assertEqual(result.item['quantity'], 3)
        self.assertEqual(result.item['location'], 'consignment')
        self.assertIn(result.item, self.seller['items'])

    def test_unlist_restores_same_instance_and_full_bag_rejects(self):
        item = {'id': 700, 'template_id': 3, 'quantity': 1, 'location': 'bag', 'name':'道具'}
        self.seller['items'].append(item)
        listed = self.service.list_item(self.seller, 700, 1, 100)
        self.seller['bag_capacity'] = 0
        failed = self.service.unlist(self.seller, listed.listing['item_instance_id'])
        self.assertFalse(failed.ok)
        self.assertEqual(item['location'], 'consignment')
        self.seller['bag_capacity'] = 20
        ok = self.service.unlist(self.seller, listed.listing['item_instance_id'])
        self.assertTrue(ok.ok)
        self.assertIs(ok.item, item)
        self.assertEqual(item['location'], 'bag')

    def test_buy_moves_same_instance_and_silver_once(self):
        item = {'id': 800, 'template_id': 4, 'quantity': 2, 'location': 'bag',
                'kind':'材料', 'name':'仙石碎片'}
        self.seller['items'].append(item)
        listed = self.service.list_item(self.seller, 800, 2, 300)
        bought = self.service.buy(self.buyer, listed.listing['item_instance_id'])
        self.assertTrue(bought.ok)
        self.assertIs(bought.item, item)
        self.assertNotIn(item, self.seller['items'])
        self.assertIn(item, self.buyer['items'])
        self.assertEqual(item['location'], 'bag')
        self.assertEqual(self.buyer['currencies']['silver'], 9400)
        self.assertEqual(self.seller['currencies']['silver'], 10600)
        again = self.service.buy(self.buyer, 800)
        self.assertFalse(again.ok)
        self.assertEqual(self.buyer['currencies']['silver'], 9400)

    def test_buy_rejects_self_insufficient_silver_and_full_bag(self):
        item = {'id': 900, 'template_id': 5, 'quantity': 1, 'location':'bag', 'name':'道具'}
        self.seller['items'].append(item)
        listed = self.service.list_item(self.seller, 900, 1, 20000)
        self.assertFalse(self.service.buy(self.seller, 900).ok)
        self.assertFalse(self.service.buy(self.buyer, 900).ok)
        self.buyer['currencies']['silver'] = 30000
        self.buyer['bag_capacity'] = 0
        self.assertFalse(self.service.buy(self.buyer, 900).ok)
        self.assertEqual(item['location'], 'consignment')

    def test_category_mapping_covers_weapon_mount_material_and_generic(self):
        self.assertEqual(consignment_category_for_item(
            {'equipment_slot':10,'icon_code':2100}, self.registry), 1)
        self.assertEqual(consignment_category_for_item(
            {'equipment_slot':17}, self.registry), 24)
        self.assertEqual(consignment_category_for_item(
            {'kind':'材料'}, self.registry), 27)
        self.assertEqual(consignment_category_for_item({}, self.registry), 26)

if __name__ == '__main__':
    unittest.main()
