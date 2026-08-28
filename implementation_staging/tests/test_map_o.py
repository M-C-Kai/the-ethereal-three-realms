import struct
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from map_o import MapO, decode_tile_rle, encode_tile_rle, inspect_map_ref


class MapOTests(unittest.TestCase):
    def test_map_ref_record_boundaries(self):
        image = struct.pack('>Ibbbb', 118, 1, 2, 3, 4)
        composite = bytes([0, 7, 8, 9, 1]) + struct.pack('>hbbb', 0, 10, 11, 1)
        data = struct.pack('>HH', 1, 1) + image + composite
        info = inspect_map_ref(data)
        self.assertEqual(info.composite_tile_count, 1)
        self.assertEqual(info.image_record_count, 1)
        self.assertEqual(info.image_ids, (118,))
        self.assertEqual(info.consumed_bytes, len(data))

    def test_rle_round_trip_and_exact_length(self):
        values = ([0] * 192) + ([-1] * 3) + [1, 2, 2] + ([3] * 300)
        encoded = encode_tile_rle(values)
        self.assertEqual(decode_tile_rle(encoded, len(values)), [value & 0xFF for value in values])
        self.assertEqual(encoded[:4], bytes([255, 255, 192, 0]))

    def test_map_o_round_trip(self):
        original = MapO(
            width=4,
            height=3,
            map_type=2,
            tile_definitions=[0, 114],
            tiles=[0, 0, 1, -1] * 3,
            collision=[False, True, False, False] * 3,
            mirror=[False, False, True, False] * 3,
            tile_pixel_width=20,
            tile_pixel_height=10,
        )
        encoded = original.to_file()
        decoded = MapO.from_file(encoded)
        self.assertEqual(decoded.to_spec(), original.to_spec())
        self.assertEqual(encoded[5:10], bytes((2, 4, 3, 20, 10)))
        sections = decoded.to_1407_sections()
        self.assertEqual(
            decode_tile_rle(sections['tiles_rle'], 12),
            [value & 0xFF for value in original.tiles],
        )


if __name__ == '__main__':
    unittest.main()
