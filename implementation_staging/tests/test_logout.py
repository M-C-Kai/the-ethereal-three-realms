"""APK-confirmed in-game logout protocol tests.

Reverse-engineered from the original APK (no 1074 involvement):
- C->S 1054 [BYTE 8] opens the logout page;
  S->C 1054 [BYTE 8, BYTE flag, STRING text] is the page reply.
- C->S 1003 [INT 0] (INT, not byte) confirms logout;
  S->C 1003 [BYTE 0] acknowledges; the client then closes the connection
  itself after ~1s, so the server must never hard-close the socket here.
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import test_client as test_client_module  # noqa: E402
from protocol import (  # noqa: E402
    TYPE_BYTE,
    TYPE_INT,
    TYPE_STRING,
    byte,
    decode_frame,
    encode_frame,
    field_values,
    integer,
    string,
)
from server import (  # noqa: E402
    is_logout_confirm_request,
    is_logout_page_request,
    logout_ack_frame,
    logout_page_frame,
)

LOGOUT_PAGE_TEXT = '是否确认退出游戏？'


def _type_ids(fields):
    return [field.type_id for field in fields]


class LogoutPageFrameTests(unittest.TestCase):
    """S->C 1054 must be exactly BYTE 8, BYTE flag, STRING text."""

    def test_logout_page_frame_matches_apk_layout(self):
        message_id, fields = decode_frame(logout_page_frame())
        self.assertEqual(message_id, 1054)
        self.assertEqual(field_values(fields), [8, 0, LOGOUT_PAGE_TEXT])
        self.assertEqual(_type_ids(fields), [TYPE_BYTE, TYPE_BYTE, TYPE_STRING])

    def test_logout_page_frame_supports_custom_flag_and_text(self):
        message_id, fields = decode_frame(logout_page_frame(text='服务器维护中', flag=1))
        self.assertEqual(message_id, 1054)
        self.assertEqual(field_values(fields), [8, 1, '服务器维护中'])
        self.assertEqual(_type_ids(fields), [TYPE_BYTE, TYPE_BYTE, TYPE_STRING])


class LogoutAckFrameTests(unittest.TestCase):
    """S->C 1003 must be exactly a single BYTE 0."""

    def test_logout_ack_frame_is_single_byte_zero(self):
        message_id, fields = decode_frame(logout_ack_frame())
        self.assertEqual(message_id, 1003)
        self.assertEqual(field_values(fields), [0])
        self.assertEqual(_type_ids(fields), [TYPE_BYTE])


class LogoutRequestHelpersTests(unittest.TestCase):
    """test_client request builders must mirror the exact APK TLV types."""

    def test_client_logout_page_request_is_byte_8(self):
        message_id, fields = decode_frame(test_client_module.logout_page_request())
        self.assertEqual(message_id, 1054)
        self.assertEqual(field_values(fields), [8])
        self.assertEqual(_type_ids(fields), [TYPE_BYTE])

    def test_client_logout_confirm_request_is_int_zero_not_byte(self):
        message_id, fields = decode_frame(test_client_module.logout_confirm_request())
        self.assertEqual(message_id, 1003)
        self.assertEqual(field_values(fields), [0])
        self.assertEqual(_type_ids(fields), [TYPE_INT])

    def test_page_predicate_accepts_apk_frame(self):
        fields = decode_frame(encode_frame(1054, [byte(8)]))[1]
        self.assertTrue(is_logout_page_request(fields))

    def test_confirm_predicate_accepts_apk_frame(self):
        fields = decode_frame(encode_frame(1003, [integer(0)]))[1]
        self.assertTrue(is_logout_confirm_request(fields))


class LogoutRequestTypeGuardTests(unittest.TestCase):
    """Value alone is not enough: wrong TLV types must not count as logout."""

    def test_page_request_with_int_type_is_rejected(self):
        fields = decode_frame(encode_frame(1054, [integer(8)]))[1]
        self.assertEqual(field_values(fields), [8])
        self.assertFalse(is_logout_page_request(fields))

    def test_confirm_request_with_byte_type_is_rejected(self):
        fields = decode_frame(encode_frame(1003, [byte(0)]))[1]
        self.assertEqual(field_values(fields), [0])
        self.assertFalse(is_logout_confirm_request(fields))

    def test_confirm_request_with_nonzero_value_is_rejected(self):
        fields = decode_frame(encode_frame(1003, [integer(1)]))[1]
        self.assertFalse(is_logout_confirm_request(fields))

    def test_page_request_with_wrong_action_is_rejected(self):
        fields = decode_frame(encode_frame(1054, [byte(7)]))[1]
        self.assertFalse(is_logout_page_request(fields))

    def test_empty_fields_are_rejected(self):
        self.assertFalse(is_logout_page_request(decode_frame(encode_frame(1054))[1]))
        self.assertFalse(is_logout_confirm_request(decode_frame(encode_frame(1003))[1]))

    def test_string_typed_page_request_is_rejected(self):
        fields = decode_frame(encode_frame(1054, [string('8')]))[1]
        self.assertFalse(is_logout_page_request(fields))


if __name__ == '__main__':
    unittest.main()
