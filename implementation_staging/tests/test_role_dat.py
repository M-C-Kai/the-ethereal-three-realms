import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.role_dat import (
    MODEL_OFFSET,
    dat_id_to_raw_model,
    parse_role_dat,
    raw_model_to_dat_id,
    validate_all,
)

ASSET_ROOT = Path(__file__).resolve().parents[1] / "build" / "weapon-apk-extracted"


class RoleDatTests(unittest.TestCase):
    def test_model_dat_id_round_trip(self):
        self.assertEqual(raw_model_to_dat_id(-2004250), 95750)
        self.assertEqual(dat_id_to_raw_model(95750), -2004250)
        self.assertEqual(raw_model_to_dat_id(3_760_000), 5_860_000)
        for dat_id in (2000, 95750, 5860000, 6100001):
            self.assertEqual(dat_id_to_raw_model(raw_model_to_dat_id(dat_id - MODEL_OFFSET)), dat_id - MODEL_OFFSET)

    def test_header_decode_of_known_sprite(self):
        path = ASSET_ROOT / "assets" / "res" / "role" / "95750.dat"
        if not path.exists():
            self.skipTest("extracted APK assets not present")
        meta = parse_role_dat(path.read_bytes())
        self.assertEqual(meta["image_index_count"], 2)
        self.assertEqual(meta["frame_count"], 8)
        self.assertEqual(meta["direction_group_count"], 5)
        self.assertEqual(meta["frame_sequence_count"], 1)
        # header/frames/groups must not overrun the file.
        self.assertLessEqual(meta["trailing_bytes"], 64)

    def test_every_bundled_sprite_parses(self):
        if not ASSET_ROOT.exists():
            self.skipTest("extracted APK assets not present")
        catalog = validate_all(str(ASSET_ROOT))
        self.assertEqual(len(catalog), 376)
        for entry in catalog:
            self.assertGreater(entry["frame_count"], 0)
            self.assertIn("dat_id", entry)


if __name__ == "__main__":
    unittest.main()
