"""Regression contract for standalone image-backed dynamic map 60011 (翠溪村)."""
from __future__ import annotations

import tempfile
import unittest
import io
import json
import zipfile
from collections import deque
from pathlib import Path

from PIL import Image, ImageChops

import server
from systems.map.protocol import MapO, inspect_map_ref
from systems.map.service import DynamicMapPackage, materialize_dynamic_map


ROOT = Path(__file__).resolve().parent.parent
MAP_DIR = ROOT / 'maps' / '60011'


class Map60011PackageTests(unittest.TestCase):
    def test_asset_bundle_reassembles_the_complete_scene_without_gaps(self):
        bundle = MAP_DIR / '60011_apk_assets.zip'
        with zipfile.ZipFile(bundle) as archive:
            manifest = json.loads(archive.read('resource_manifest.json'))
            self.assertEqual(manifest['scene_size'], [675, 900])
            self.assertEqual(manifest['grid'], [9, 14])
            self.assertEqual(manifest['collision_source'], 'source_scene.png')
            self.assertEqual(len(manifest['resources']), 126)
            canvas = Image.new('RGB', (675, 900))
            covered = Image.new('L', (675, 900))
            for item in manifest['resources']:
                tile = Image.open(io.BytesIO(archive.read(f"slices/{item['file']}"))).convert('RGB')
                self.assertEqual(tile.size, (item['width'], item['height']))
                canvas.paste(tile, (item['x'], item['y']))
                covered.paste(255, (item['x'], item['y'],
                                    item['x'] + item['width'], item['y'] + item['height']))
            self.assertIsNone(ImageChops.invert(covered).getbbox())
            expected = Image.open(MAP_DIR / 'preview.png').convert('RGB')
            self.assertIsNone(ImageChops.difference(canvas, expected).getbbox())

    def test_cold_login_moves_old_blocked_position_to_current_spawn(self):
        from systems.map.service import relocate_role_for_cold_login

        settings = server.Settings.load(ROOT / 'config.json')
        role = {'id': 10084, 'map_id': 60011, 'map_x': 18, 'map_y': 30}
        self.assertTrue(relocate_role_for_cold_login(settings, role))
        self.assertEqual((role['map_x'], role['map_y']), (59, 42))
        self.assertFalse(relocate_role_for_cold_login(settings, role))

    def test_cold_login_shifts_positions_saved_by_the_90x90_layout(self):
        from systems.map.service import relocate_role_for_cold_login

        settings = server.Settings.load(ROOT / 'config.json')
        role = {'id': 10084, 'map_id': 60011, 'map_x': 50, 'map_y': 33}
        self.assertTrue(relocate_role_for_cold_login(settings, role))
        self.assertEqual((role['map_x'], role['map_y']), (59, 42))

    def test_scene_images_answer_native_1502_requests(self):
        from protocol import decode_frame
        from systems.battle.protocol import battle_image_frames

        for image_id in range(60011000, 60011126):
            frames = battle_image_frames(0, image_id)
            self.assertEqual(len(frames), 3, f'image {image_id} must answer 1502')
            message_id, fields = decode_frame(frames[0])
            self.assertEqual(message_id, 1501)
            self.assertEqual(fields[4].value, image_id)
            self.assertGreater(len(fields[-1].value), 0)

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
            self.assertEqual(ref_info.image_ids, tuple(range(60011000, 60011126)))
            self.assertEqual(ref_info.image_record_count, 126)
            self.assertEqual(ref_info.composite_tile_count, 126)

            map_o = MapO.from_file(built.map_o_path.read_bytes())
            self.assertEqual((map_o.width, map_o.height), (127, 127))
            self.assertFalse(map_o.collision[(42 * 127) + 59])
            self.assertFalse(map_o.collision[(44 * 127) + 61])
            self.assertTrue(map_o.collision[0])
            for x, y in ((26, 50), (51, 25), (76, 80)):
                self.assertTrue(map_o.collision[(y * 127) + x], (x, y))
            for x, y in ((59, 42), (61, 45), (117, 89)):
                self.assertFalse(map_o.collision[(y * 127) + x], (x, y))

            pending = deque([(59, 42)])
            reachable = {(59, 42)}
            while pending:
                x, y = pending.popleft()
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    point = (x + dx, y + dy)
                    if not (0 <= point[0] < 127 and 0 <= point[1] < 127):
                        continue
                    if point in reachable or map_o.collision[(point[1] * 127) + point[0]]:
                        continue
                    reachable.add(point)
                    pending.append(point)
            self.assertIn((61, 44), reachable)
            self.assertIn((117, 89), reachable)

        settings = server.Settings.load(ROOT / 'config.json')
        definition = settings.map_registry.require(60011)
        self.assertEqual(definition.name, '翠溪村')
        self.assertFalse(definition.map_ref_available)
        self.assertEqual(
            (definition.fallback_width, definition.fallback_height),
            (127, 127),
        )
        self.assertEqual((definition.spawn_x, definition.spawn_y), (59, 42))

        entry = settings.map_registry.portal(58, 580007)
        self.assertIsNotNone(entry)
        self.assertEqual((entry.x, entry.y), (50, 70))
        self.assertEqual(
            (entry.target_map_id, entry.target_x, entry.target_y),
            (60011, 59, 42),
        )

        back = settings.map_registry.portal(60011, 6001101)
        self.assertIsNotNone(back)
        self.assertEqual((back.x, back.y), (61, 44))
        self.assertEqual(
            (back.target_map_id, back.target_x, back.target_y),
            (58, 60, 67),
        )


if __name__ == '__main__':
    unittest.main()
