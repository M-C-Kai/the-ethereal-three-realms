"""Regression contract for standalone dynamic map 60011 (翠溪村)."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import server
from systems.map.protocol import MapO, inspect_map_ref
from systems.map.service import DynamicMapPackage, materialize_dynamic_map


ROOT = Path(__file__).resolve().parent.parent
MAP_DIR = ROOT / 'maps' / '60011'


class Map60011PackageTests(unittest.TestCase):
    def test_package_materializes_and_wires_registry(self):
        map_spec = MAP_DIR / 'map.json'
        map_ref_spec = MAP_DIR / 'map.ref.json'
        self.assertTrue(map_spec.is_file(), '60011/map.json is required')
        self.assertTrue(map_ref_spec.is_file(), '60011/map.ref.json is required')

        with tempfile.TemporaryDirectory() as tmp:
            output_root = Path(tmp)
            package = DynamicMapPackage(
                map_id=60011,
                directory=MAP_DIR,
                map_spec_path=map_spec,
                map_ref_spec_path=map_ref_spec,
                output_map_o_path=output_root / '60011.map.o',
                output_map_ref_path=output_root / '60011.map.ref',
            )
            built = materialize_dynamic_map(package)
            self.assertGreater(built.map_o_bytes, 0)
            self.assertGreater(built.map_ref_bytes, 0)
            self.assertLess(built.map_ref_bytes, 32768)
            self.assertTrue(built.map_o_path.is_file())
            self.assertTrue(built.map_ref_path.is_file())

            ref_info = inspect_map_ref(built.map_ref_path.read_bytes())
            self.assertEqual(ref_info.image_ids, tuple(range(60011000, 60011006)))
            self.assertEqual(ref_info.image_record_count, 6)
            self.assertEqual(ref_info.composite_tile_count, 6)

            map_o = MapO.from_file(built.map_o_path.read_bytes())
            self.assertEqual((map_o.width, map_o.height), (90, 90))
            self.assertFalse(map_o.collision[(35 * 90) + 50])
            self.assertFalse(map_o.collision[(37 * 90) + 52])

        settings = server.Settings.load(ROOT / 'config.json')
        definition = settings.map_registry.require(60011)
        self.assertEqual(definition.name, '翠溪村')
        self.assertFalse(definition.map_ref_available)
        self.assertEqual(
            (definition.fallback_width, definition.fallback_height),
            (90, 90),
        )
        self.assertEqual((definition.spawn_x, definition.spawn_y), (50, 35))

        entry = settings.map_registry.portal(58, 580007)
        self.assertIsNotNone(entry)
        self.assertEqual((entry.x, entry.y), (50, 70))
        self.assertEqual(
            (entry.target_map_id, entry.target_x, entry.target_y),
            (60011, 50, 35),
        )

        back = settings.map_registry.portal(60011, 6001101)
        self.assertIsNotNone(back)
        self.assertEqual((back.x, back.y), (52, 37))
        self.assertEqual(
            (back.target_map_id, back.target_x, back.target_y),
            (58, 60, 67),
        )


if __name__ == '__main__':
    unittest.main()
