"""social 系统内存注册表：好友请求与交易会话。

全部状态保存在进程内（服务器重启即清空），与协议生命周期一致：
交易请求是在线会话之间的瞬时握手，好友关系落盘到角色数据。
"""
from __future__ import annotations

# 好友与交易请求的有效期。
PENDING_REQUEST_TTL_SECONDS = 60.0


class SocialRegistry:
    """进程内的好友请求与交易会话簿记。"""

    def __init__(self) -> None:
        # target_role_id -> (requester_role_id, timestamp)
        self.friend_requests: dict[int, tuple[int, float]] = {}
        # 发起方 role_id -> (目标 role_id, timestamp)
        self.trade_requests: dict[int, tuple[int, float]] = {}
        # role_id -> 对方 role_id（交易窗口打开中，双向登记）
        self.active_trades: dict[int, int] = {}
        # role_id -> {"money": int, "item_ids": [int]}（锁定后的暂存）
        self.trade_locks: dict[int, dict[str, object]] = {}
        # 已点击最终确认（1056/10）的 role_id 集合
        self.trade_confirms: set[int] = set()

    # ------------------------------------------------------------------
    @staticmethod
    def _pop_pending(
        table: dict[int, tuple[int, float]],
        key: int,
        now: float,
    ) -> int | None:
        entry = table.pop(key, None)
        if entry is None:
            return None
        requester_id, created_at = entry
        if now - created_at > PENDING_REQUEST_TTL_SECONDS:
            return None
        return int(requester_id)

    def pop_friend_request(self, target_role_id: int, now: float) -> int | None:
        return self._pop_pending(self.friend_requests, int(target_role_id), now)

    def pop_trade_request(self, target_role_id: int, now: float) -> int | None:
        return self._pop_pending(self.trade_requests, int(target_role_id), now)

    # ------------------------------------------------------------------
    def open_trade(self, left_role_id: int, right_role_id: int) -> None:
        self.active_trades[int(left_role_id)] = int(right_role_id)
        self.active_trades[int(right_role_id)] = int(left_role_id)

    def close_trade(self, role_id: int) -> int | None:
        """Remove one side and return the peer role id (symmetric teardown)."""
        peer = self.active_trades.pop(int(role_id), None)
        if peer is not None:
            self.active_trades.pop(int(peer), None)
        self.trade_locks.pop(int(role_id), None)
        self.trade_confirms.discard(int(role_id))
        if peer is not None:
            self.trade_locks.pop(int(peer), None)
            self.trade_confirms.discard(int(peer))
        return int(peer) if peer is not None else None

    def trade_peer(self, role_id: int) -> int | None:
        peer = self.active_trades.get(int(role_id))
        return int(peer) if peer is not None else None
