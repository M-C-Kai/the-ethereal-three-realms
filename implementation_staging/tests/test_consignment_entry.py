from __future__ import annotations

import unittest
from types import SimpleNamespace
from unittest.mock import patch

from protocol import decode_frame, field_values
import server_dynamic_maps as dynamic
from consignment_protocol import CONSIGNMENT_ITEM_MODE, consignment_screen_frame


class _DialogueState:
    def __init__(self, map_id: int, npc_id: int):
        self.map_id = map_id
        self.npc_id = npc_id
        self.cleared = False

    def clear(self) -> None:
        self.cleared = True
        self.map_id = None
        self.npc_id = None


class ConsignmentEntryTests(unittest.TestCase):
    def test_native_consignment_screen_is_apk_screen_613_in_item_mode(self):
        message_id, fields = decode_frame(consignment_screen_frame())
        self.assertEqual(message_id, 1010)
        self.assertEqual(field_values(fields), [0, 0, 0, CONSIGNMENT_ITEM_MODE, 613, 69])
        self.assertEqual(CONSIGNMENT_ITEM_MODE, 2809)
        self.assertEqual([field.type_id for field in fields], [4, 3, 3, 4, 4, 3])

    def test_consignment_merchant_dialogue_exposes_consignment_option(self):
        npc = SimpleNamespace(
            id=1_900_004,
            name='赵公明',
            label='寄售商人',
            introduction='财货流通，自有章法。',
            service='consignment_merchant',
        )
        frames = dynamic.consignment_map_npc_dialogue_frames(npc, {'id': 10001}, SimpleNamespace())
        self.assertEqual(len(frames), 1)

        message_id, fields = decode_frame(frames[0])
        values = field_values(fields)
        self.assertEqual(message_id, 2032)
        self.assertEqual(values[0], 1_900_004)
        self.assertIn('寄售', values)
        self.assertIn('结束对话', values)

    def test_selecting_consignment_opens_screen_613_in_item_mode_and_clears_dialogue_state(self):
        npc = SimpleNamespace(id=1_900_004, service='consignment_merchant')
        definition = SimpleNamespace(id=58)
        state = _DialogueState(58, npc.id)
        role = {'id': 10001}
        settings = SimpleNamespace()

        with patch.object(dynamic._server, 'settings_for_role', return_value=definition), patch.object(
            dynamic._server, 'map_npc_for_object_id', return_value=npc
        ), patch.object(dynamic._server, 'map_object_interaction_ack_frame', return_value=b'ack'):
            frames = dynamic.consignment_npc_dialogue_option_frames(
                settings,
                role,
                state,
                dynamic.CONSIGNMENT_MERCHANT_OPTION,
            )

        self.assertEqual(frames[0], b'ack')
        message_id, fields = decode_frame(frames[1])
        self.assertEqual(message_id, 1010)
        self.assertEqual(field_values(fields)[3:], [CONSIGNMENT_ITEM_MODE, 613, 69])
        self.assertTrue(state.cleared)


if __name__ == '__main__':
    unittest.main()
