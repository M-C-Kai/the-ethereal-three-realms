from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from protocol import decode_frame, field_values
import server_dynamic_maps as dynamic


class DynamicMapRefTransferTests(unittest.TestCase):
    def test_map_ref_is_split_into_native_1407_11_12_frames(self):
        payload = b'ABCDEFGHIJKLM'
        definition = SimpleNamespace(id=60010)
        with tempfile.TemporaryDirectory() as tmp:
            resource = Path(tmp) / '60010.map.ref'
            resource.write_bytes(payload)
            with patch.object(dynamic, 'map_ref_path', return_value=resource):
                frames = dynamic.map_ref_transfer_frames(definition, chunk_size=5)

        self.assertEqual(len(frames), 3)
        decoded = [decode_frame(frame) for frame in frames]
        self.assertTrue(all(message_id == 1407 for message_id, _ in decoded))

        values = [field_values(fields) for _, fields in decoded]
        self.assertEqual([row[0] for row in values], [11, 12, 12])
        self.assertEqual([row[1] for row in values], [len(payload)] * 3)
        self.assertEqual([row[3] for row in values], [0, 5, 10])
        self.assertEqual(b''.join(row[2] for row in values), payload)

    def test_missing_server_ref_preserves_old_apk_local_entry_path(self):
        definition = SimpleNamespace(id=58)
        with tempfile.TemporaryDirectory() as tmp:
            missing = Path(tmp) / '58.map.ref'
            with patch.object(dynamic, 'map_ref_path', return_value=missing), patch.object(
                dynamic, '_ORIGINAL_MAP_ENTER_FRAMES', return_value=[b'old-13', b'old-14']
            ):
                self.assertEqual(
                    dynamic.dynamic_map_enter_frames(definition, 10001),
                    [b'old-13', b'old-14'],
                )

    def test_streamed_ref_switches_action_13_to_status_1(self):
        definition = SimpleNamespace(id=60010)
        with patch.object(dynamic, 'map_ref_transfer_frames', return_value=[b'ref-chunk']), patch.object(
            dynamic, '_ORIGINAL_MAP_ENTER_FRAMES', return_value=[b'old-13', b'old-14', b'old-105']
        ), patch.object(dynamic._server, 'map_action', return_value=b'new-13') as map_action:
            frames = dynamic.dynamic_map_enter_frames(definition, 10001)

        self.assertEqual(frames, [b'ref-chunk', b'new-13', b'old-14', b'old-105'])
        map_action.assert_called_once_with(definition, 13, status=1, role_id=10001)


if __name__ == '__main__':
    unittest.main()
