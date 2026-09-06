from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from dynamic_map_builder import (
    discover_dynamic_maps,
    materialize_dynamic_map,
    merge_dynamic_maps_into_registry_payload,
)
from map_o import MapO, inspect_map_ref


EXPECTED_REF_SHA256 = '7eb419659ca28a006bc0c1a0980e863472fcdd45149c5e90076e1f991c7afceb'
EXPECTED_MAP_O_SHA256 = 'f92cb8de6d5816e3311c2ad73f2ebfcbd069526da4349aa81855fda8ed8b3a4a'


class DynamicMapBuilderTests(unittest.TestCase):
    def test_repository_package_60010_materializes_original_verified_bytes(self):
        root = Path(__file__).resolve().parents[1] / 'maps'
        packages = discover_dynamic_maps(root)
        package = next(item for item in packages if item.map_id == 60010)
        built = materialize_dynamic_map(package)

        ref_data = built.map_ref_path.read_bytes()
        map_o_data = built.map_o_path.read_bytes()
        info = inspect_map_ref(ref_data)
        parsed = MapO.from_file(map_o_data)

        self.assertEqual(hashlib.sha256(ref_data).hexdigest(), EXPECTED_REF_SHA256)
        self.assertEqual(hashlib.sha256(map_o_data).hexdigest(), EXPECTED_MAP_O_SHA256)
        self.assertEqual(info.composite_tile_count, 6)
        self.assertEqual(set(info.image_ids), {160, 161, 162, 172, 310, 326})
        self.assertEqual((parsed.width, parsed.height), (24, 24))
        self.assertFalse(parsed.collision[(12 * 24) + 12])

    def test_discovery_ignores_flat_files_and_non_numeric_directories(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / '60020').mkdir()
            (root / '60020' / 'map.json').write_text('{}', encoding='utf-8')
            (root / '60020' / 'map.ref.json').write_text('{}', encoding='utf-8')
            (root / 'notes').mkdir()
            (root / '60021.map.json').write_text('{}', encoding='utf-8')

            packages = discover_dynamic_maps(root)

        self.assertEqual([item.map_id for item in packages], [60020])

    def test_registry_merge_adds_dynamic_map_and_inbound_portal(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            package_dir = root / '60020'
            package_dir.mkdir()
            (package_dir / 'map.ref.json').write_text(json.dumps({
                'format': 'piaomiao-map-ref-v1',
                'map_id': 60020,
                'image_records': [],
                'composite_tiles': [],
            }), encoding='utf-8')
            (package_dir / 'map.json').write_text(json.dumps({
                'format': 'piaomiao-dynamic-map-v1',
                'map_id': 60020,
                'width': 8,
                'height': 8,
                'map_type': 0,
                'tile_definitions': [0],
                'tiles': [[0] * 8 for _ in range(8)],
                'collision': ['........'] * 8,
                'mirror': ['........'] * 8,
                'registry': {
                    'name': '自动地图',
                    'spawn': {'x': 3, 'y': 4},
                    'npcs': [],
                    'portals': [],
                    'inbound_portals': [{
                        'source_map_id': 58,
                        'id': 580020,
                        'name': '自动入口',
                        'model': -2043000,
                        'x': 10,
                        'y': 10,
                    }],
                },
            }), encoding='utf-8')
            base = {
                'default_map_id': 58,
                'maps': {
                    '58': {
                        'name': '长安',
                        'map_o_file': 'maps/58.map.o',
                        'map_ref_available': True,
                        'fallback_width': 96,
                        'fallback_height': 96,
                        'spawn': {'x': 60, 'y': 67},
                        'npcs': [],
                        'portals': [],
                    }
                },
            }

            merged = merge_dynamic_maps_into_registry_payload(base, root)

        dynamic = merged['maps']['60020']
        self.assertEqual(dynamic['name'], '自动地图')
        self.assertEqual(dynamic['map_o_file'], 'maps/60020.map.o')
        self.assertFalse(dynamic['map_ref_available'])
        self.assertEqual((dynamic['fallback_width'], dynamic['fallback_height']), (8, 8))
        portal = merged['maps']['58']['portals'][0]
        self.assertEqual(portal['target_map_id'], 60020)
        self.assertEqual((portal['target_x'], portal['target_y']), (3, 4))


if __name__ == '__main__':
    unittest.main()
