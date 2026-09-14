"""Regression for the APK-local 60011 map draw-range correction."""
import json
from pathlib import Path
import unittest

from tools.patch_map_60011_render_range import patch_smali


class Map60011RenderPatchTests(unittest.TestCase):
    def test_expands_only_the_90_by_90_map_draw_range(self):
        source = (Path(__file__).resolve().parents[1] / 'build_artifacts' /
                  'build' / 'dex-smali' / 'pmsj' / 'work' / 'b' / 'm.smali').read_text()
        patched = patch_smali(source)
        self.assertIn('const/16 v4, 0x5a', patched)
        self.assertIn('iget-byte v3, v0, Lpmsj/work/b/m;->g:B', patched)
        self.assertIn('iget-byte v3, v0, Lpmsj/work/b/m;->h:B', patched)
        self.assertIn('add-int/lit16 v4, v4, -0x100', patched)
        self.assertIn('add-int/lit16 v4, v4, 0x200', patched)
        self.assertEqual(patch_smali(patched), patched)

        ref = json.loads((Path(__file__).resolve().parents[1] / 'maps' / '60011' /
                          'map.ref.json').read_text(encoding='utf-8'))
        for record, tile in zip(ref['image_records'], ref['composite_tiles']):
            layer = tile['layers'][0]
            for offset, size in ((layer['x'], record['width']),
                                 (layer['y'], record['height'])):
                self.assertLessEqual(max(-offset, offset + size), 256)


if __name__ == '__main__':
    unittest.main()
