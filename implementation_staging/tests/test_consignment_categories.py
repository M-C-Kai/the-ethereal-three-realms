from __future__ import annotations

import unittest

from consignment_protocol import (
    CONSIGNMENT_ITEM_CATEGORIES,
    consignment_category_frame,
    is_consignment_browse_request,
    is_consignment_category_request,
)
from protocol import byte, decode_frame, field_values


class ConsignmentCategoryTests(unittest.TestCase):
    def test_apk_native_item_categories_are_downlinked_in_order(self):
        message_id, fields = decode_frame(consignment_category_frame())
        values = field_values(fields)
        self.assertEqual(message_id, 1138)
        self.assertEqual(values[:2], [3, 28])
        records = values[2:]
        self.assertEqual(len(records), 56)
        self.assertEqual(records[0:4], [0, '所有武器', 1, '长枪'])
        self.assertEqual(records[-4:], [26, '道具', 27, '材料'])
        self.assertEqual(len(CONSIGNMENT_ITEM_CATEGORIES), 28)

    def test_native_request_shapes_are_strict(self):
        self.assertTrue(is_consignment_category_request([byte(3)]))
        self.assertTrue(is_consignment_browse_request([byte(13), byte(27)]))
        self.assertFalse(is_consignment_browse_request([byte(13), byte(28)]))


if __name__ == '__main__':
    unittest.main()
