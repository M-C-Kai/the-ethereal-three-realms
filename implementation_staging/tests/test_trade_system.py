from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from consignment_service import ConsignmentService


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
    def __init__(self, path: Path, roles: list[dict[str, object]]):
        self.path = path
        self.data = {'next_role_id': 20000, 'accounts': {'trade-test': roles}}
        self.fail_next_save = False

    def save(self):
        if self.fail_next_save:
            self.fail_next_save = False
            raise OSError('forced trade save failure')
        self.path.write_text(json.dumps(self.data, ensure_ascii=False), encoding='utf-8')


def make_role(role_id: int, name: str, *, silver: int = 10_000) -> dict[str, object]:
    return {
        'id': role_id,
        'name': name,
        'items': [],
        'bag_capacity': 50,
        'currencies': {'silver': silver},
    }


class TradeSystemTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.seller = make_role(10001, '卖家')
        self.buyer = make_role(10002, '买家')
        self.store = FakeRoleStore(root / 'roles.json', [self.seller, self.buyer])
        self.market_path = root / 'trade-system.json'
        self.registry = FakeRegistry()
        self.service = ConsignmentService(self.store, self.registry, self.market_path)

    def tearDown(self):
        self.tmp.cleanup()

    def _list_material(self, item_id: int = 501, *, quantity: int = 2, unit_price: int = 300):
        item = {
            'id': item_id,
            'template_id': 60001,
            'quantity': quantity,
            'location': 'bag',
            'kind': '材料',
            'name': '玄铁',
        }
        self.seller['items'].append(item)
        listed = self.service.list_item(self.seller, item_id, quantity, unit_price)
        self.assertTrue(listed.ok)
        return item, listed

    def test_successful_purchase_creates_durable_completed_transaction(self):
        item, listed = self._list_material()

        bought = self.service.buy(self.buyer, int(listed.listing['item_instance_id']))

        self.assertTrue(bought.ok)
        self.assertIsNotNone(bought.transaction)
        receipt = bought.transaction
        self.assertEqual(receipt['status'], 'completed')
        self.assertEqual(receipt['listing_id'], listed.listing['listing_id'])
        self.assertEqual(receipt['seller_role_id'], 10001)
        self.assertEqual(receipt['seller_name'], '卖家')
        self.assertEqual(receipt['buyer_role_id'], 10002)
        self.assertEqual(receipt['buyer_name'], '买家')
        self.assertEqual(receipt['item_instance_id'], item['id'])
        self.assertEqual(receipt['quantity'], 2)
        self.assertEqual(receipt['unit_price'], 300)
        self.assertEqual(receipt['total_price'], 600)
        self.assertGreater(receipt['completed_at'], 0)
        self.assertEqual(bought.listing['status'], 'sold')
        self.assertEqual(self.seller['currencies']['silver'], 10_600)
        self.assertEqual(self.buyer['currencies']['silver'], 9_400)
        self.assertIn(item, self.buyer['items'])
        self.assertNotIn(item, self.seller['items'])

        seller_history = self.service.trade_history(10001, side='seller')
        buyer_history = self.service.trade_history(10002, side='buyer')
        self.assertEqual([row['transaction_id'] for row in seller_history], [receipt['transaction_id']])
        self.assertEqual([row['transaction_id'] for row in buyer_history], [receipt['transaction_id']])

        restarted = ConsignmentService(self.store, self.registry, self.market_path)
        persisted = restarted.trade_history(10001)
        self.assertEqual(len(persisted), 1)
        self.assertEqual(persisted[0], receipt)

    def test_double_purchase_cannot_duplicate_receipt_or_move_money_twice(self):
        _, listed = self._list_material(item_id=502, quantity=1, unit_price=250)
        item_id = int(listed.listing['item_instance_id'])

        first = self.service.buy(self.buyer, item_id)
        second = self.service.buy(self.buyer, item_id)

        self.assertTrue(first.ok)
        self.assertFalse(second.ok)
        self.assertEqual(second.reason, 'listing_not_found')
        self.assertEqual(self.buyer['currencies']['silver'], 9_750)
        self.assertEqual(self.seller['currencies']['silver'], 10_250)
        self.assertEqual(len(self.service.trade_history(10001)), 1)

    def test_failed_purchase_never_creates_completed_transaction(self):
        _, listed = self._list_material(item_id=503, quantity=1, unit_price=20_000)
        failed = self.service.buy(self.buyer, int(listed.listing['item_instance_id']))

        self.assertFalse(failed.ok)
        self.assertEqual(failed.reason, 'insufficient_silver')
        self.assertEqual(self.service.trade_history(10001), [])
        self.assertEqual(self.service.trade_history(10002), [])
        self.assertEqual(listed.listing['status'], 'active')

    def test_cancelled_listing_is_order_history_but_not_successful_trade(self):
        item, listed = self._list_material(item_id=504, quantity=1, unit_price=100)
        cancelled = self.service.unlist(self.seller, int(listed.listing['item_instance_id']))

        self.assertTrue(cancelled.ok)
        self.assertEqual(cancelled.listing['status'], 'cancelled')
        self.assertEqual(item['location'], 'bag')
        self.assertEqual(self.service.trade_history(10001), [])

    def test_trade_history_side_filter_only_returns_matching_role(self):
        _, first_listing = self._list_material(item_id=505, quantity=1, unit_price=100)
        self.assertTrue(self.service.buy(self.buyer, int(first_listing.listing['item_instance_id'])).ok)

        third = make_role(10003, '第三人')
        self.store.data['accounts']['trade-test'].append(third)
        third_item = {
            'id': 506,
            'template_id': 60002,
            'quantity': 1,
            'location': 'bag',
            'kind': '材料',
            'name': '精铁',
        }
        third['items'].append(third_item)
        third_listing = self.service.list_item(third, 506, 1, 80)
        self.assertTrue(third_listing.ok)
        self.assertTrue(self.service.buy(self.seller, int(third_listing.listing['item_instance_id'])).ok)

        self.assertEqual(len(self.service.trade_history(10001)), 2)
        self.assertEqual(len(self.service.trade_history(10001, side='seller')), 1)
        self.assertEqual(len(self.service.trade_history(10001, side='buyer')), 1)
        self.assertEqual(self.service.trade_history(99999), [])
        with self.assertRaises(ValueError):
            self.service.trade_history(10001, side='invalid')

    def test_buy_save_failure_rolls_back_every_part_of_transaction(self):
        item, listed = self._list_material(item_id=507, quantity=1, unit_price=400)
        item_id = int(listed.listing['item_instance_id'])
        self.store.fail_next_save = True

        with self.assertRaises(OSError):
            self.service.buy(self.buyer, item_id)

        self.assertEqual(self.seller['currencies']['silver'], 10_000)
        self.assertEqual(self.buyer['currencies']['silver'], 10_000)
        self.assertIn(item, self.seller['items'])
        self.assertNotIn(item, self.buyer['items'])
        self.assertEqual(item['location'], 'consignment')
        self.assertEqual([row['item_instance_id'] for row in self.service.search(27)], [item_id])
        self.assertEqual(self.service.trade_history(10001), [])
        self.assertEqual(self.service.trade_history(10002), [])


if __name__ == '__main__':
    unittest.main()
