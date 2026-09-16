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
            self.assertEqual(manifest['scene_size'], [1040, 743])
            self.assertEqual(manifest['grid'], [18, 7])
            self.assertEqual(manifest['collision_source'], 'walkable_reference.png')
            self.assertEqual(len(manifest['resources']), 126)
            canvas = Image.new('RGB', (1040, 743))
            covered = Image.new('L', (1040, 743))
            for item in manifest['resources']:
                tile = Image.open(io.BytesIO(archive.read(f"slices/{item['file']}"))).convert('RGB')
                self.assertEqual(tile.size, (item['width'], item['height']))
                canvas.paste(tile, (item['x'], item['y']))
                ref = json.loads((MAP_DIR / 'map.ref.json').read_text(encoding='utf-8'))
                layer = ref['composite_tiles'][item['image_id'] - 60011000]['layers'][0]
                self.assertEqual(10 * (item['tile_x'] - item['tile_y']) + layer['x'], item['screen_x'])
                self.assertEqual(5 * (item['tile_x'] + item['tile_y'] + 2) + layer['y'], item['screen_y'])
                covered.paste(255, (item['x'], item['y'],
                                    item['x'] + item['width'], item['y'] + item['height']))
            self.assertIsNone(ImageChops.invert(covered).getbbox())
            expected = Image.open(MAP_DIR / 'preview.png').convert('RGB')
            source = Image.open(MAP_DIR / 'source_scene.png').convert('RGB')
            self.assertEqual(source.size, (1040, 743))
            self.assertIsNone(ImageChops.difference(expected, source.resize((1040, 743), Image.Resampling.LANCZOS)).getbbox())
            self.assertIsNone(ImageChops.difference(canvas, expected).getbbox())
            clean = Image.open(MAP_DIR / 'source_art.png').convert('RGB')
            self.assertIsNone(ImageChops.difference(expected.crop((180,180,860,563)), clean.resize((680,383), Image.Resampling.LANCZOS)).getbbox())

    def test_walkable_cells_keep_scenery_margin_on_every_side(self):
        spec = json.loads((MAP_DIR / 'map.json').read_text(encoding='utf-8'))
        count = 0
        for y, row in enumerate(spec['collision']):
            for x, cell in enumerate(row):
                if cell != '.':
                    continue
                px, py = 10 * (x-y) + 520, 5 * (x+y+2) - 270
                self.assertTrue(180 <= px < 860 and 180 <= py < 563, (x,y,px,py))
                count += 1
        self.assertGreater(count, 100)

    def test_flat_scene_slices_use_apk_background_pass(self):
        # APK b/o.a()Z checks flags & 4. b/m draws those composites into
        # its background; otherwise they become b/l objects mixed with actors.
        from tools.map_ref_generator import from_spec, serialize_map_ref, parse_map_ref
        spec = json.loads((MAP_DIR / 'map.ref.json').read_text(encoding='utf-8'))
        records, tiles = parse_map_ref(serialize_map_ref(*from_spec(spec)))
        self.assertEqual(len(tiles), 126)
        self.assertTrue(all(tile.flags & 4 for tile in tiles))

    def test_cold_login_moves_old_blocked_position_to_current_spawn(self):
        from systems.map.service import relocate_role_for_cold_login

        settings = server.Settings.load(ROOT / 'config.json')
        role = {'id': 10084, 'map_id': 60011, 'map_x': 18, 'map_y': 30}
        self.assertTrue(relocate_role_for_cold_login(settings, role))
        self.assertEqual((role['map_x'], role['map_y']), (71, 58))
        self.assertFalse(relocate_role_for_cold_login(settings, role))

    def test_cold_login_shifts_positions_saved_by_the_90x90_layout(self):
        from systems.map.service import relocate_role_for_cold_login

        settings = server.Settings.load(ROOT / 'config.json')
        role = {'id': 10084, 'map_id': 60011, 'map_x': 50, 'map_y': 33}
        self.assertTrue(relocate_role_for_cold_login(settings, role))
        self.assertEqual((role['map_x'], role['map_y']), (71, 58))

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
            self.assertFalse(map_o.collision[(58 * 127) + 71])
            self.assertFalse(map_o.collision[(59 * 127) + 72])
            self.assertTrue(map_o.collision[0])
            for x, y in ((61, 66), (62, 51), (92, 106)):
                self.assertTrue(map_o.collision[(y * 127) + x], (x, y))
            for x, y in ((71, 58), (73, 59), (81, 75)):
                self.assertFalse(map_o.collision[(y * 127) + x], (x, y))

            pending = deque([(71, 58)])
            reachable = {(71, 58)}
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
            self.assertIn((72, 59), reachable)
            self.assertIn((81, 75), reachable)
            # Cross the central stepping-stone shoal to the left-bank road.
            self.assertIn((55, 70), reachable)
            self.assertIn((61, 63), reachable)
            self.assertIn((37, 57), reachable)
            self.assertIn((58, 42), reachable)
            # Open river away from the shoal stays impassable.
            self.assertTrue(map_o.collision[66 * 127 + 61])

        settings = server.Settings.load(ROOT / 'config.json')
        definition = settings.map_registry.require(60011)
        self.assertEqual(definition.name, '翠溪村')
        self.assertFalse(definition.map_ref_available)
        self.assertEqual(
            (definition.fallback_width, definition.fallback_height),
            (127, 127),
        )
        self.assertEqual((definition.spawn_x, definition.spawn_y), (71, 58))

        entry = settings.map_registry.portal(58, 580007)
        self.assertIsNotNone(entry)
        self.assertEqual((entry.x, entry.y), (50, 70))
        self.assertEqual(
            (entry.target_map_id, entry.target_x, entry.target_y),
            (60011, 71, 58),
        )

        back = settings.map_registry.portal(60011, 6001101)
        self.assertIsNotNone(back)
        self.assertEqual((back.x, back.y), (72, 59))
        self.assertEqual(
            (back.target_map_id, back.target_x, back.target_y),
            (58, 60, 67),
        )


if __name__ == '__main__':
    unittest.main()
