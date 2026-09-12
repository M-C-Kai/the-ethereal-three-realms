from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


class FakeRegistry:
    def resolve(self, item):
        return {
            'name': item.get('name', '物品'),
            'equipment_slot': item.get('equipment_slot', 0),
            'icon_code': item.get('icon_code', 0),
            'kind': item.get('kind', 'item'),
            'max_quantity': item.get('max_quantity', 99),
            'tradable': item.get('tradable', True),
        }


class FakeRoleStore:
    def __init__(self, path, roles):
        self.path = Path(path)
        self.data = {'next_role_id': 20000, 'accounts': {'a': roles}}
        self.fail_next_save = False

    def save(self):
        if self.fail_next_save:
            self.fail_next_save = False
            raise OSError('forced save failure')
        self.path.write_text(json.dumps(self.data, ensure_ascii=False), encoding='utf-8')


def role(rid, name, silver=10000, cap=20):
    return {
        'id': rid,
        'name': name,
        'items': [],
        'bag_capacity': cap,
        'currencies': {'silver': silver},
    }


class ConsignmentServiceContractTests(unittest.TestCase):
    def test_service_module_exists(self):
        self.assertIsNotNone(importlib.util.find_spec('consignment_service'))


class ConsignmentServiceTests(unittest.TestCase):
    def setUp(self):
        if importlib.util.find_spec('consignment_service') is None:
            self.skipTest('consignment_service not implemented yet')
        from consignment_service import ConsignmentService

        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.seller = role(10001, '卖家')
        self.buyer = role(10002, '买家')
        self.other = role(10003, '其他')
        self.store = FakeRoleStore(root / 'roles.json', [self.seller, self.buyer, self.other])
        self.market_path = root / 'consignment.json'
        self.registry = FakeRegistry()
        self.service = ConsignmentService(self.store, self.registry, self.market_path)

    def tearDown(self):
        if hasattr(self, 'tmp'):
            self.tmp.cleanup()

    def test_whole_item_is_escrowed_and_restart_persists(self):
        item = {'id': 501, 'template_id': 1, 'quantity': 1, 'location': 'bag',
                'equipment_slot': 1, 'name': '头盔'}
        self.seller['items'].append(item)
        result = self.service.list_item(self.seller, 501, 1, 500)
        self.assertTrue(result.ok)
        self.assertEqual(item['location'], 'consignment')
        self.assertEqual(self.service.search(14)[0]['item_instance_id'], 501)

        from consignment_service import ConsignmentService
        again = ConsignmentService(self.store, self.registry, self.market_path)
        self.assertEqual(again.my_listings(10001)[0]['item_instance_id'], 501)

    def test_partial_stack_allocates_globally_unique_escrow_instance(self):
        # Existing IDs span multiple roles; the split instance must not collide
        # with any role or any active escrow instance.
        self.other['items'].append({'id': 9999, 'template_id': 90, 'quantity': 1, 'location': 'bag'})
        item = {'id': 600, 'template_id': 2, 'quantity': 10, 'location': 'bag',
                'kind': '材料', 'name': '玄铁'}
        self.seller['items'].append(item)
        result = self.service.list_item(self.seller, 600, 3, 25)
        self.assertTrue(result.ok)
        self.assertEqual(item['quantity'], 7)
        self.assertGreater(result.item['id'], 9999)
        self.assertEqual(result.item['quantity'], 3)
        self.assertEqual(result.item['location'], 'consignment')
        self.assertIn(result.item, self.seller['items'])

    def test_my_listings_and_category_search_only_return_active_rows(self):
        a = {'id': 701, 'template_id': 3, 'quantity': 1, 'location': 'bag',
             'equipment_slot': 1, 'name': '头盔A'}
        b = {'id': 702, 'template_id': 4, 'quantity': 1, 'location': 'bag',
             'equipment_slot': 1, 'name': '头盔B'}
        self.seller['items'].extend([a, b])
        self.service.list_item(self.seller, 701, 1, 100)
        self.service.list_item(self.seller, 702, 1, 200)
        self.assertEqual(len(self.service.search(14)), 2)
        self.assertEqual(len(self.service.my_listings(10001)), 2)
        self.assertTrue(self.service.unlist(self.seller, 701).ok)
        self.assertEqual([r['item_instance_id'] for r in self.service.search(14)], [702])
        self.assertEqual([r['item_instance_id'] for r in self.service.my_listings(10001)], [702])

    def test_unlist_restores_same_instance_and_full_bag_rejects(self):
        item = {'id': 800, 'template_id': 5, 'quantity': 1, 'location': 'bag', 'name': '道具'}
        self.seller['items'].append(item)
        self.service.list_item(self.seller, 800, 1, 100)
        self.seller['bag_capacity'] = 0
        failed = self.service.unlist(self.seller, 800)
        self.assertFalse(failed.ok)
        self.assertEqual(item['location'], 'consignment')
        self.seller['bag_capacity'] = 20
        ok = self.service.unlist(self.seller, 800)
        self.assertTrue(ok.ok)
        self.assertIs(ok.item, item)
        self.assertEqual(item['location'], 'bag')

    def test_buy_moves_same_instance_and_silver_once(self):
        item = {'id': 900, 'template_id': 6, 'quantity': 2, 'location': 'bag',
                'kind': '材料', 'name': '仙石碎片'}
        self.seller['items'].append(item)
        self.service.list_item(self.seller, 900, 2, 300)
        bought = self.service.buy(self.buyer, 900)
        self.assertTrue(bought.ok)
        self.assertIs(bought.item, item)
        self.assertNotIn(item, self.seller['items'])
        self.assertIn(item, self.buyer['items'])
        self.assertEqual(item['location'], 'bag')
        self.assertEqual(self.buyer['currencies']['silver'], 9400)
        self.assertEqual(self.seller['currencies']['silver'], 10600)
        self.assertFalse(self.service.buy(self.buyer, 900).ok)
        self.assertEqual(self.buyer['currencies']['silver'], 9400)

    def test_buy_rejects_self_insufficient_silver_and_full_bag_without_state_change(self):
        item = {'id': 1000, 'template_id': 7, 'quantity': 1, 'location': 'bag', 'name': '道具'}
        self.seller['items'].append(item)
        self.service.list_item(self.seller, 1000, 1, 20000)
        self.assertFalse(self.service.buy(self.seller, 1000).ok)
        self.assertFalse(self.service.buy(self.buyer, 1000).ok)
        self.buyer['currencies']['silver'] = 30000
        self.buyer['bag_capacity'] = 0
        self.assertFalse(self.service.buy(self.buyer, 1000).ok)
        self.assertEqual(item['location'], 'consignment')
        self.assertEqual(self.service.my_listings(10001)[0]['status'], 'active')

    def test_rejects_equipped_bound_task_and_untradable_items(self):
        cases = [
            {'id': 1101, 'location': 'equipped'},
            {'id': 1102, 'location': 'bag', 'bound': True},
            {'id': 1103, 'location': 'bag', 'kind': '任务'},
            {'id': 1104, 'location': 'bag', 'tradable': False},
        ]
        for item in cases:
            item.update(template_id=item['id'], quantity=1, name='不可交易')
            self.seller['items'].append(item)
            self.assertFalse(self.service.list_item(self.seller, item['id'], 1, 100).ok)

    def test_save_failure_rolls_back_role_and_listing_state(self):
        item = {'id': 1200, 'template_id': 8, 'quantity': 1, 'location': 'bag', 'name': '道具'}
        self.seller['items'].append(item)
        self.store.fail_next_save = True
        with self.assertRaises(OSError):
            self.service.list_item(self.seller, 1200, 1, 100)
        self.assertEqual(item['location'], 'bag')
        self.assertEqual(self.service.search(26), [])

    def test_category_mapping_covers_weapon_mount_material_and_generic(self):
        from consignment_service import consignment_category_for_item
        self.assertEqual(consignment_category_for_item(
            {'equipment_slot': 10, 'icon_code': 2100}, self.registry), 1)
        self.assertEqual(consignment_category_for_item(
            {'equipment_slot': 17}, self.registry), 24)
        self.assertEqual(consignment_category_for_item(
            {'kind': '材料'}, self.registry), 27)
        self.assertEqual(consignment_category_for_item({}, self.registry), 26)


if __name__ == '__main__':
    unittest.main()
