from __future__ import annotations

import struct
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from battle import resources
from protocol import decode_frame, field_values


class BattleResourceTests(unittest.TestCase):
    def test_empty_role_resource_finishes_with_two_native_1503_chunks(self):
        frames = resources.battle_resource_frames(0)

        self.assertEqual(len(frames), 2)
        first_id, first_fields = decode_frame(frames[0])
        last_id, last_fields = decode_frame(frames[1])
        self.assertEqual(first_id, 1503)
        self.assertEqual(last_id, 1503)
        self.assertEqual(field_values(first_fields), [0, 0, 0, 0, b''])
        self.assertEqual(field_values(last_fields), [2, 0, 0, 0, b''])
        self.assertEqual(
            [field.type_id for field in first_fields],
            [2, 4, 3, 3, 8],
        )

    def test_role_alias_and_offset_resolution_use_implementation_root(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            role_dir = root / 'data' / 'role'
            role_dir.mkdir(parents=True)
            (role_dir / '100000.dat').write_bytes(b'alias-role')
            offset_id = 77 + resources.BATTLE_RESOURCE_MODEL_OFFSET
            (role_dir / f'{offset_id}.dat').write_bytes(b'offset-role')

            with patch.object(resources, 'PROJECT_DIR', root):
                alias = resources.battle_resource_resolution(6)
                offset = resources.battle_resource_resolution(77)

            self.assertEqual(alias['branch'], 'alias')
            self.assertEqual(alias['resolved_id'], 100000)
            self.assertEqual(offset['branch'], 'offset')
            self.assertEqual(offset['resolved_id'], offset_id)

    def test_role_dat_response_keeps_status_zero_then_status_two(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            role_dir = root / 'data' / 'role'
            role_dir.mkdir(parents=True)
            payload = b'role-data'
            (role_dir / '123.dat').write_bytes(payload)

            with patch.object(resources, 'PROJECT_DIR', root):
                frames = resources.battle_resource_frames(123)

            first_id, first_fields = decode_frame(frames[0])
            last_id, last_fields = decode_frame(frames[1])
            self.assertEqual(first_id, 1503)
            self.assertEqual(last_id, 1503)
            self.assertEqual(field_values(first_fields), [0, 123, len(payload), len(payload), payload])
            self.assertEqual(field_values(last_fields), [2, 123, len(payload), 0, b''])

    def test_image_response_preserves_1501_field_types_and_redraw(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            image_dir = root / 'build' / 'weapon-apk-extracted' / 'assets' / 'res' / 'images'
            image_dir.mkdir(parents=True)
            image_id = 70000
            index_record = struct.pack('>IBH', image_id, 0, 0)
            (image_dir / 'images.o').write_bytes(struct.pack('>H', len(index_record)) + index_record)

            palette = b'abc'
            idat = b'data'
            container = bytes([0, 0]) + struct.pack(
                '>HHBBIIIHH',
                2,
                3,
                8,
                1,
                0x01020304,
                0x05060708,
                0x090A0B0C,
                len(palette),
                len(idat),
            ) + palette + idat
            (image_dir / 'png0.p').write_bytes(container)

            with patch.object(resources, 'PROJECT_DIR', root):
                raw = resources.battle_image_resource(image_id)
                frames = resources.battle_image_frames(resources.PNG_QUERY_ROLE_CACHE, image_id)

            self.assertIsNotNone(raw)
            assert raw is not None
            self.assertEqual(raw[:4], (2, 3, 8, 1))
            self.assertEqual(raw[-1], palette + idat)
            self.assertEqual(len(frames), 3)

            first_id, first_fields = decode_frame(frames[0])
            finish_id, finish_fields = decode_frame(frames[1])
            redraw_id, redraw_fields = decode_frame(frames[2])
            self.assertEqual(first_id, 1501)
            self.assertEqual(finish_id, 1501)
            self.assertEqual(redraw_id, 1502)
            self.assertEqual(redraw_fields, [])
            self.assertEqual(field_values(first_fields)[:5], [1, 7, 0, 0, image_id])
            self.assertEqual(field_values(finish_fields)[3], 2)
            self.assertEqual(field_values(finish_fields)[14:16], [0, b''])
            self.assertEqual(
                [field.type_id for field in first_fields],
                [4, 4, 2, 2, 4, 3, 3, 2, 2, 3, 3, 4, 4, 4, 3, 8],
            )


if __name__ == '__main__':
    unittest.main()
