from __future__ import annotations

import io
import struct
import unittest

from PIL import Image

from tools.build_map_60011_apk import (
    pack_png_for_client_bytes,
    patch_images_index,
    rebuild_client_png,
)


class BuildMap60011ApkTests(unittest.TestCase):
    def test_client_image_pack_roundtrip_keeps_dimensions(self):
        image = Image.new("RGB", (135, 113), (12, 180, 90))
        source = io.BytesIO()
        image.save(source, format="PNG")
        packed = pack_png_for_client_bytes(source.getvalue())
        rebuilt = Image.open(io.BytesIO(rebuild_client_png(packed)))
        self.assertEqual(rebuilt.size, (135, 113))

    def test_images_index_append_preserves_suffix(self):
        old_record = struct.pack(">IBH", 100, 3, 25)
        original = struct.pack(">H", len(old_record)) + old_record + b"TAIL"
        patched = patch_images_index(original, [(60011000, 201, 0)])
        records_length = struct.unpack_from(">H", patched, 0)[0]
        self.assertEqual(records_length, 14)
        self.assertEqual(
            patched[2 + 7:2 + 14],
            struct.pack(">IBH", 60011000, 201, 0),
        )
        self.assertEqual(patched[2 + records_length:], b"TAIL")


if __name__ == "__main__":
    unittest.main()
