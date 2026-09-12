from __future__ import annotations

import unittest

from consignment_protocol import (
    CONSIGNMENT_ACTION_BROWSE_LIST,
    CONSIGNMENT_ACTION_BUY,
    CONSIGNMENT_ACTION_LIST,
    CONSIGNMENT_ACTION_MY_LISTINGS,
    CONSIGNMENT_ACTION_QUALITY_COUNTS,
    CONSIGNMENT_ACTION_UNLIST,
    consignment_browse_frame,
    consignment_listed_frame,
    consignment_my_listings_frame,
    consignment_purchase_removed_frame,
    consignment_quality_counts_frame,
    consignment_unlisted_frame,
    parse_consignment_request,
)
from protocol import byte, integer, short, string, decode_frame, field_values


LISTING = {
    'object_type': 1,
    'item_instance_id': 9001,
    'template_id': 170901002,
    'quantity': 2,
    'unit_price': 500,
    'seller_role_id': 10001,
    'seller_name': '卖家',
    'item': {'id': 9001, 'template_id': 170901002, 'quantity': 2, 'location': 'consignment'},
}


class Registry:
    def resolve(self, item):
        return {
            **item,
            'icon_code': 41002,
            'quality': 2,
            'name': '辟邪',
        }


class ConsignmentProtocolTests(unittest.TestCase):
    def test_parse_confirmed_requests(self):
        request = parse_consignment_request([
            byte(9), integer(9001), byte(1), integer(10001), byte(2), integer(500)
        ])
        self.assertEqual(request.action, CONSIGNMENT_ACTION_LIST)
        self.assertEqual(request.item_instance_id, 9001)
        self.assertEqual(request.object_type, 1)
        self.assertEqual(request.role_id, 10001)
        self.assertEqual(request.quantity, 2)
        self.assertEqual(request.unit_price, 500)

        request = parse_consignment_request([byte(13), byte(24)])
        self.assertEqual(request.action, CONSIGNMENT_ACTION_QUALITY_COUNTS)
        self.assertEqual(request.category_id, 24)

        request = parse_consignment_request([
            byte(1), integer(10001), integer(249), short(0), byte(10)
        ])
        self.assertEqual(request.action, CONSIGNMENT_ACTION_BROWSE_LIST)
        self.assertEqual(request.mode, 249)
        self.assertEqual(request.page, 0)
        self.assertEqual(request.page_size, 10)

        request = parse_consignment_request([byte(7), integer(10001)])
        self.assertEqual(request.action, CONSIGNMENT_ACTION_MY_LISTINGS)
        request = parse_consignment_request([byte(2), integer(9001), byte(1), integer(10001)])
        self.assertEqual(request.action, CONSIGNMENT_ACTION_UNLIST)
        self.assertEqual(request.item_instance_id, 9001)
        request = parse_consignment_request([byte(4), integer(9001), integer(10002)])
        self.assertEqual(request.action, CONSIGNMENT_ACTION_BUY)
        self.assertEqual(request.item_instance_id, 9001)

    def test_quality_count_response_matches_screen44_reader(self):
        message_id, fields = decode_frame(consignment_quality_counts_frame([5, 2, 1, 1, 1, 0]))
        self.assertEqual(message_id, 1138)
        self.assertEqual(field_values(fields), [13, 6, 5, 2, 1, 1, 1, 0])

    def test_browse_response_uses_confirmed_eight_field_records(self):
        message_id, fields = decode_frame(consignment_browse_frame([LISTING], Registry(), total=1))
        values = field_values(fields)
        self.assertEqual(message_id, 1138)
        self.assertEqual(values[:4], [1, 1, 0, 1])
        self.assertEqual(values[4:], [1, 9001, 170901002, 2, 1000, '卖家', 41002, '卖家'])
        self.assertEqual(len(values[4:]), 8)

    def test_my_and_listed_responses_use_seven_field_records(self):
        for frame, action in (
            (consignment_my_listings_frame([LISTING], Registry()), 7),
            (consignment_listed_frame(LISTING, Registry()), 9),
        ):
            message_id, fields = decode_frame(frame)
            values = field_values(fields)
            self.assertEqual(message_id, 1138)
            self.assertEqual(values[:2], [action, 1])
            self.assertEqual(values[2:], [1, 9001, 170901002, 2, 1000, '卖家', 41002])
            self.assertEqual(len(values[2:]), 7)

    def test_purchase_and_unlist_removal_frames_target_item_instance_id(self):
        self.assertEqual(field_values(decode_frame(consignment_purchase_removed_frame(9001))[1]), [12, 9001])
        self.assertEqual(field_values(decode_frame(consignment_unlisted_frame(9001))[1]), [14, 9001])


if __name__ == '__main__':
    unittest.main()
