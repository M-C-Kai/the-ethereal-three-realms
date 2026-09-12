from __future__ import annotations

import unittest

import consignment_protocol as c
from protocol import decode_frame, field_values


class ConsignmentCategoryEntryTests(unittest.TestCase):
    def test_empty_category_still_has_screen_44_count_vector(self):
        self.assertTrue(hasattr(c, 'consignment_category_counts_frame'))
        mid, fields = decode_frame(c.consignment_category_counts_frame([0]))
        self.assertEqual(mid, 1138)
        self.assertEqual(field_values(fields), [13, 1, 0])


if __name__ == '__main__':
    unittest.main()
