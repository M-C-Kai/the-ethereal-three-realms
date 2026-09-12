from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from protocol import byte, decode_frame, encode_frame, field_values, integer, short, string
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
        definition = SimpleNamespace(id=60010)
        with tempfile.TemporaryDirectory() as tmp:
            missing = Path(tmp) / '60010.map.ref'
            with patch.object(dynamic, 'map_ref_path', return_value=missing), patch.object(
                dynamic, '_ORIGINAL_MAP_ENTER_FRAMES', return_value=[b'old-13', b'old-14']
            ):
                self.assertEqual(
                    dynamic.dynamic_map_enter_frames(definition, 10001),
                    [b'old-13', b'old-14'],
                )

    def test_streamed_ref_enters_transition_before_parsing_new_ref(self):
        definition = SimpleNamespace(id=60010)
        with patch.object(dynamic, 'map_ref_transfer_frames', return_value=[b'ref-chunk']), patch.object(
            dynamic, '_ORIGINAL_MAP_ENTER_FRAMES', return_value=[b'old-13', b'old-14', b'old-105']
        ), patch.object(dynamic._server, 'map_action', return_value=b'new-13') as map_action:
            frames = dynamic.dynamic_map_enter_frames(definition, 10001)

        # Working APK-local maps receive action 13 before their target map.ref is
        # parsed.  Keep the same ordering for streamed refs so m.C() runs while
        # the client is already inside its native map-transition state instead
        # of repainting the active scene from the top edge.
        self.assertEqual(frames, [b'new-13', b'ref-chunk', b'old-14', b'old-105'])
        map_action.assert_called_once_with(definition, 13, status=1, role_id=10001)

    def test_boss_effect_carrier_uses_render_only_2030_bucket(self):
        definition = SimpleNamespace(id=58)
        carrier = SimpleNamespace(
            id=1_900_099,
            x=9,
            y=28,
            dat_id=3_000_100,
            direction=0,
            name='',
            label='',
        )

        message_id, fields = decode_frame(dynamic.map_npc_frame_with_effect(definition, carrier))

        self.assertEqual(message_id, 2030)
        self.assertEqual(
            field_values(fields),
            [1_900_099, 9, 28, 3_000_100, 0, 3_000_000, '', 2, ''],
        )
        self.assertEqual(
            [field.type_id for field in fields],
            [4, 4, 4, 4, 4, 4, 6, 4, 6],
        )

    def test_non_effect_npc_keeps_original_2030_encoder(self):
        definition = SimpleNamespace(id=58)
        npc = SimpleNamespace(dat_id=95_750)
        with patch.object(dynamic, '_ORIGINAL_MAP_NPC_FRAME', return_value=b'original') as original:
            frame = dynamic.map_npc_frame_with_effect(definition, npc)

        self.assertEqual(frame, b'original')
        original.assert_called_once_with(definition, npc)

    def test_roaming_boss_spawn_uses_native_2028_q_layout_with_attached_ring_flag(self):
        definition = SimpleNamespace(
            id=58,
            monster=SimpleNamespace(id=700_001, model=-2_004_250, x=9, y=28),
        )

        message_id, fields = decode_frame(dynamic.roaming_boss_spawn_frame(definition))

        self.assertEqual(message_id, 2028)
        self.assertEqual(
            field_values(fields),
            [700_001, 9, 28, 95_750, 0, 0, 0x800000],
        )
        self.assertEqual([field.type_id for field in fields], [4, 3, 3, 4, 4, 4, 4])

    def test_roaming_boss_effect_image_70600_reuses_verified_apk_70000_pixels(self):
        marker = object()
        with patch.object(dynamic, '_ORIGINAL_BATTLE_IMAGE_RESOURCE', return_value=marker) as original:
            self.assertIs(dynamic.roaming_boss_image_resource(70_600), marker)

        original.assert_called_once_with(70_000)

    def test_non_boss_effect_image_keeps_original_resolution(self):
        marker = object()
        with patch.object(dynamic, '_ORIGINAL_BATTLE_IMAGE_RESOURCE', return_value=marker) as original:
            self.assertIs(dynamic.roaming_boss_image_resource(70_500), marker)

        original.assert_called_once_with(70_500)

    def test_roaming_boss_move_uses_native_1005_target_short_layout(self):
        message_id, fields = decode_frame(
            dynamic.roaming_boss_move_frame(700_001, 9, 28, 12, 28)
        )

        self.assertEqual(message_id, 1005)
        self.assertEqual(field_values(fields), [700_001, 9, 28, 12, 28])
        self.assertEqual([field.type_id for field in fields], [4, 3, 3, 3, 3])

    def test_map58_replaces_generic_1126_boss_with_native_2028_q(self):
        definition = SimpleNamespace(
            id=58,
            monster=SimpleNamespace(
                id=700_001,
                name='试炼妖兽',
                model=-2_004_250,
                x=9,
                y=28,
            ),
        )
        generic = encode_frame(1126, [
            byte(0),
            byte(1),
            integer(700_001),
            integer(9),
            integer(28),
            integer(-2_004_250),
            string('试炼妖兽'),
        ])
        with patch.object(dynamic, '_ORIGINAL_MAP_ENTER_FRAMES', return_value=[b'action-13', generic]), patch.object(
            dynamic, 'map_ref_transfer_frames', return_value=[]
        ):
            frames = dynamic.dynamic_map_enter_frames(definition, 10001)

        self.assertEqual(frames[0], b'action-13')
        message_id, fields = decode_frame(frames[1])
        self.assertEqual(message_id, 2028)
        self.assertEqual(
            field_values(fields),
            [700_001, 9, 28, 95_750, 0, 0, 0x800000],
        )


if __name__ == '__main__':
    unittest.main()
