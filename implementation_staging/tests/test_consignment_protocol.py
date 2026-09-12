from __future__ import annotations
import unittest
from consignment_protocol import (
    ConsignmentWireRecord,
    consignment_market_list_frame,
    consignment_my_listings_frame,
    is_consignment_buy_request,
    is_consignment_list_item_request,
    is_consignment_my_listings_request,
    is_consignment_unlist_request,
)
from protocol import byte, integer, decode_frame, field_values

class ConsignmentProtocolTests(unittest.TestCase):
    def test_exact_native_request_shapes(self):
        self.assertTrue(is_consignment_list_item_request([
            byte(9), integer(1234), byte(1), integer(10001), byte(2), integer(500),
        ]))
        self.assertTrue(is_consignment_my_listings_request([byte(7), integer(10001)]))
        self.assertTrue(is_consignment_unlist_request([
            byte(2), integer(1234), byte(1), integer(10001),
        ]))
        self.assertTrue(is_consignment_buy_request([
            byte(4), integer(1234), integer(10002),
        ]))

    def test_market_record_is_eight_fields_and_own_record_is_seven(self):
        record = ConsignmentWireRecord(1, 1234, 170901002, 2, 1000, '辟邪', 10001, '卖家')
        mid, fields = decode_frame(consignment_market_list_frame([record]))
        self.assertEqual(mid, 1138)
        values = field_values(fields)
        self.assertEqual(values[:4], [1, 1, 0, 1])
        self.assertEqual(values[4:], [1, 1234, 170901002, 2, 1000, '辟邪', 10001, '卖家'])
        mid, fields = decode_frame(consignment_my_listings_frame([record]))
        self.assertEqual(mid, 1138)
        values = field_values(fields)
        self.assertEqual(values[:2], [7, 1])
        self.assertEqual(values[2:], [1, 1234, 170901002, 2, 1000, '辟邪', 10001])

if __name__ == '__main__':
    unittest.main()
