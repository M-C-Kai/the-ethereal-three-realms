from __future__ import annotations

import unittest

import consignment_protocol as c
from protocol import byte, decode_frame, field_values, integer


class ConsignmentProtocolTests(unittest.TestCase):
    def test_full_native_request_api_exists(self):
        required = (
            'ConsignmentWireRecord',
            'is_consignment_my_listings_request',
            'is_consignment_list_item_request',
            'is_consignment_unlist_request',
            'is_consignment_buy_request',
            'is_consignment_market_list_request',
            'consignment_category_counts_frame',
            'consignment_market_list_frame',
            'consignment_my_listings_frame',
            'consignment_remove_owned_frame',
            'consignment_remove_market_frame',
            'wire_record_from_listing',
        )
        for name in required:
            self.assertTrue(hasattr(c, name), name)

    def test_exact_native_request_shapes(self):
        self.assertTrue(c.is_consignment_category_request([byte(3)]))
        self.assertTrue(c.is_consignment_browse_request([byte(13), byte(27)]))
        self.assertTrue(c.is_consignment_my_listings_request([byte(7), integer(10001)]))
        self.assertTrue(c.is_consignment_list_item_request([
            byte(9), integer(1234), byte(1), integer(10001), byte(2), integer(500),
        ]))
        self.assertTrue(c.is_consignment_unlist_request([
            byte(2), integer(1234), byte(1), integer(10001),
        ]))
        self.assertTrue(c.is_consignment_buy_request([
            byte(4), integer(1234), integer(10002),
        ]))
        self.assertTrue(c.is_consignment_market_list_request([byte(0)]))
        self.assertTrue(c.is_consignment_market_list_request([byte(23)]))

        # Numeric values with the wrong TLV type are invalid. The APK uses
        # concrete BYTE/INT readers; accepting a SHORT here hides wire bugs.
        self.assertFalse(c.is_consignment_browse_request([byte(13), integer(27)]))
        self.assertFalse(c.is_consignment_my_listings_request([byte(7), byte(1)]))
        self.assertFalse(c.is_consignment_buy_request([byte(4), integer(1234), byte(2)]))

    def test_action_13_count_vector_opens_native_screen_44(self):
        mid, fields = decode_frame(c.consignment_category_counts_frame([0]))
        self.assertEqual(mid, 1138)
        self.assertEqual(field_values(fields), [13, 1, 0])
        self.assertEqual([f.type_id for f in fields], [1, 1, 4])

    def test_market_and_own_rows_match_native_record_widths(self):
        row = c.ConsignmentWireRecord(
            object_type=1,
            item_instance_id=1234,
            template_id=170901002,
            quantity=2,
            price=1000,
            display_name='辟邪',
            seller_role_id=10001,
            seller_name='卖家',
        )
        mid, fields = decode_frame(c.consignment_market_list_frame([row]))
        self.assertEqual(mid, 1138)
        self.assertEqual(field_values(fields), [
            1, 1, 0, 1,
            1, 1234, 170901002, 2, 1000, '辟邪', 10001, '卖家',
        ])

        mid, fields = decode_frame(c.consignment_my_listings_frame([row]))
        self.assertEqual(mid, 1138)
        self.assertEqual(field_values(fields), [
            7, 1,
            1, 1234, 170901002, 2, 1000, '辟邪', 10001,
        ])

    def test_remove_frames_target_native_screen_rows(self):
        mid, fields = decode_frame(c.consignment_remove_owned_frame(1234))
        self.assertEqual(mid, 1138)
        self.assertEqual(field_values(fields), [15, 1234])
        mid, fields = decode_frame(c.consignment_remove_market_frame(1234))
        self.assertEqual(mid, 1138)
        self.assertEqual(field_values(fields), [16, 1234])


if __name__ == '__main__':
    unittest.main()
