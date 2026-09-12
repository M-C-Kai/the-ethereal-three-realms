from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from protocol import byte, decode_frame, field_values, integer, short
from server import LocalGameServer, Settings


class ConsignmentServerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.settings = Settings(
            role_data_file=str(root / 'roles.json'),
            consignment_data_file=str(root / 'consignment_listings.json'),
        )
        self.server = LocalGameServer(self.settings)
        self.seller = {
            'id': 10001,
            'name': '卖家',
            'bag_capacity': 20,
            'currencies': {'silver': 10000, 'immortal_stones': 0, 'immortal_crystals': 0},
            'items': [
                {'id': 9001, 'template_id': 260_000_001, 'quantity': 3, 'location': 'bag'},
            ],
        }
        self.buyer = {
            'id': 10002,
            'name': '买家',
            'bag_capacity': 20,
            'currencies': {'silver': 10000, 'immortal_stones': 0, 'immortal_crystals': 0},
            'items': [],
        }
        self.server.roles.data['accounts'] = {
            'seller': [self.seller],
            'buyer': [self.buyer],
        }
        self.server.roles.save()

    def tearDown(self):
        self.tmp.cleanup()

    @staticmethod
    def decoded(frames):
        return [(message_id, field_values(fields)) for message_id, fields in map(decode_frame, frames)]

    def test_list_quality_browse_my_unlist_flow(self):
        frames = self.server.handle_consignment_request(
            self.seller,
            [byte(9), integer(9001), byte(1), integer(10001), byte(3), integer(100)],
        )
        decoded = self.decoded(frames)
        self.assertIn((1009, [3, 9001]), decoded)
        self.assertTrue(any(mid == 1138 and values[:2] == [9, 1] for mid, values in decoded))
        self.assertEqual(self.seller['items'], [])

        quality = self.server.handle_consignment_request(self.seller, [byte(13), byte(27)])
        self.assertEqual(self.decoded(quality), [(1138, [13, 6, 1, 1, 0, 0, 0, 0])])

        browse = self.server.handle_consignment_request(
            self.buyer,
            [byte(1), integer(10002), integer(279), short(0), byte(10)],
        )
        browse_values = self.decoded(browse)[0][1]
        self.assertEqual(browse_values[:4], [1, 1, 0, 1])
        self.assertEqual(browse_values[4], 1)
        self.assertEqual(browse_values[5], 9001)
        self.assertEqual(browse_values[6], 260_000_001)
        self.assertEqual(browse_values[7], 3)
        self.assertEqual(browse_values[8], 300)

        mine = self.server.handle_consignment_request(
            self.seller, [byte(7), integer(10001)]
        )
        self.assertEqual(self.decoded(mine)[0][1][:2], [7, 1])

        unlisted = self.server.handle_consignment_request(
            self.seller, [byte(2), integer(9001), byte(1), integer(10001)]
        )
        decoded_unlisted = self.decoded(unlisted)
        self.assertIn((1138, [14, 9001]), decoded_unlisted)
        self.assertTrue(any(mid == 1008 and values[1] == 9001 for mid, values in decoded_unlisted))
        self.assertEqual(self.seller['items'][0]['id'], 9001)

    def test_purchase_moves_instance_and_refreshes_buyer_currency(self):
        self.server.handle_consignment_request(
            self.seller,
            [byte(9), integer(9001), byte(1), integer(10001), byte(3), integer(100)],
        )
        frames = self.server.handle_consignment_request(
            self.buyer, [byte(4), integer(9001), integer(10002)]
        )
        decoded = self.decoded(frames)
        self.assertIn((1138, [12, 9001]), decoded)
        self.assertTrue(any(mid == 1008 and values[1] == 9001 for mid, values in decoded))
        self.assertTrue(any(mid == 1006 for mid, _values in decoded))
        self.assertEqual(self.buyer['currencies']['silver'], 9700)
        self.assertEqual(self.seller['currencies']['silver'], 10300)
        self.assertEqual(self.buyer['items'][0]['id'], 9001)

    def test_pet_listing_request_is_rejected_without_state_change(self):
        before = list(self.seller['items'])
        frames = self.server.handle_consignment_request(
            self.seller,
            [byte(9), integer(9001), byte(3), integer(10001), byte(1), integer(100)],
        )
        decoded = self.decoded(frames)
        self.assertEqual(decoded[0], (1138, [9, 0]))
        self.assertTrue(any(mid == 1049 for mid, _values in decoded))
        self.assertEqual(self.seller['items'], before)
        self.assertEqual(self.server.consignment.listings, [])

    def test_role_id_spoof_is_rejected(self):
        frames = self.server.handle_consignment_request(
            self.seller,
            [byte(7), integer(99999)],
        )
        decoded = self.decoded(frames)
        self.assertEqual(decoded[0], (1138, [7, 0]))
        self.assertTrue(any(mid == 1049 for mid, _values in decoded))


if __name__ == '__main__':
    unittest.main()
