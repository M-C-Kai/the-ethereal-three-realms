from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from consignment_service import ConsignmentService
from tests.test_trade_system import FakeRegistry, FakeRoleStore, make_role


class TradeOrderHistoryTests(unittest.TestCase):
    def test_listing_lifecycle_is_queryable_as_order_history(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            seller = make_role(12001, '卖家')
            buyer = make_role(12002, '买家')
            store = FakeRoleStore(root / 'roles.json', [seller, buyer])
            service = ConsignmentService(store, FakeRegistry(), root / 'trade-system.json')

            cancelled_item = {
                'id': 801,
                'template_id': 70001,
                'quantity': 1,
                'location': 'bag',
                'kind': '材料',
                'name': '取消订单物品',
            }
            sold_item = {
                'id': 802,
                'template_id': 70002,
                'quantity': 1,
                'location': 'bag',
                'kind': '材料',
                'name': '成交订单物品',
            }
            seller['items'].extend([cancelled_item, sold_item])

            cancelled_listing = service.list_item(seller, 801, 1, 90)
            sold_listing = service.list_item(seller, 802, 1, 120)
            self.assertTrue(service.unlist(seller, int(cancelled_listing.listing['item_instance_id'])).ok)
            self.assertTrue(service.buy(buyer, int(sold_listing.listing['item_instance_id'])).ok)

            history = service.order_history(12001)
            self.assertEqual([row['status'] for row in history], ['cancelled', 'sold'])
            self.assertEqual(
                [row['item_instance_id'] for row in service.order_history(12001, status='sold')],
                [802],
            )
            self.assertEqual(service.order_history(99999), [])
            with self.assertRaises(ValueError):
                service.order_history(12001, status='unknown')


if __name__ == '__main__':
    unittest.main()
