from __future__ import annotations

import unittest
import zipfile
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[1]


class ApkMapResourceTests(unittest.TestCase):
    def test_final_apk_contains_drawable_kunlun_map_resources(self):
        apk_path = PROJECT_DIR / 'piaomiao_local_login.apk'
        kunlun_map_o = (PROJECT_DIR / 'maps' / '60001.map.o').read_bytes()

        with zipfile.ZipFile(apk_path) as apk:
            changan_ref = apk.read('assets/res/map/58.map.ref')
            kunlun_ref = apk.read('assets/res/map/60001.map.ref')
            packaged_map_o = apk.read('assets/res/map/60001.map.o')

        self.assertEqual(kunlun_ref, changan_ref)
        self.assertEqual(packaged_map_o, kunlun_map_o)


if __name__ == '__main__':
    unittest.main()
