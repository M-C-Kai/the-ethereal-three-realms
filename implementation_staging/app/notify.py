"""跨系统共享的 1129 顶部提示帧。"""
from __future__ import annotations

from protocol import byte, encode_frame, short, string

def top_message_frame(text: str) -> bytes:
    """Show one non-blocking message in the APK's native top map overlay."""
    return encode_frame(1049, [byte(4), string(text)])


