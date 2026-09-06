from __future__ import annotations

import hashlib
import unittest

from generate_map_60010 import (
    EXPECTED_MAP_O_SHA256,
    EXPECTED_REF_SHA256,
    build_map_o,
    build_map_ref,
)
from map_o import MapO, inspect_map_ref


class GeneratedMap60010Tests(unittest.TestCase):
    def test_map_ref_is_small_independent_six_composite_resource(self):
        data = build_map_ref()
        info = inspect_map_ref(data)
        self.assertEqual(hashlib.sha256(data).hexdigest(), EXPECTED_REF_SHA256)
        self.assertEqual(info.composite_tile_count, 6)
        self.assertEqual(info.image_record_count, 6)
        self.assertEqual(set(info.image_ids), {160, 161, 162, 172, 310, 326})
        self.assertEqual(len(data), 122)

    def test_map_o_has_24_by_24_layout_and_blocked_boundary(self):
        data = build_map_o()
        parsed = MapO.from_file(data)
        self.assertEqual(hashlib.sha256(data).hexdigest(), EXPECTED_MAP_O_SHA256)
        self.assertEqual((parsed.width, parsed.height), (24, 24))
        self.assertEqual(parsed.tile_definitions, [0, 1, 2, 3, 4, 5])
        self.assertEqual(len(data), 738)
        self.assertTrue(all(parsed.collision[x] for x in range(24)))
        self.assertTrue(all(parsed.collision[(23 * 24) + x] for x in range(24)))
        self.assertFalse(parsed.collision[(12 * 24) + 12])


if __name__ == '__main__':
    unittest.main()
