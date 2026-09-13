"""social 系统边界：点击玩家菜单（查看/私聊/交易/赠送/加友/切磋/PK）。

全部协议下标与接收分支来自 APK 反编译证据（见 docs/protocol/15-玩家交互协议.md）。
跨连接的定向推送通过注入的 ``push_to_role`` 完成，好友关系落盘到角色数据。
"""
from __future__ import annotations

import logging
from typing import Callable

from app.context import SystemContext
from app.notify import top_message_frame
from app.router import RouteResult, SystemRouter
from protocol import TYPE_BYTE, Field, byte, encode_frame, integer
from systems.inventory.protocol import find_item, item_display_name, role_items
from systems.social import service
from systems.social.protocol import (
    CHAT_CHANNEL_PRIVATE, character_view_rows_frame, chat_frame,
    empty_enemy_list_frame, friend_list_frame, friend_request_prompt_frame,
    pk_request_prompt_frame, player_view_frame, spar_ack_frame,
    trade_close_frames, trade_complete_frame, trade_enable_confirm_frame,
    trade_open_frame, trade_peer_items_frame, trade_peer_money_frame,
    trade_request_frame,
)
from systems.social.registry import SocialRegistry

LOG = logging.getLogger('piaomiao-local')

FRIEND_LIST_ACTION = 15
ENEMY_LIST_ACTION = 28
GIFT_ACTION = 81
SILVER_PROPERTY = 50

# social 必须先于 role/inventory 注册：1089/byte-2 与
# 1009/81 从角色/背包系统的全量认领中精确剥离（can_handle 逐项收紧）。
HANDLED_MESSAGE_IDS = (1004, 1009, 1019, 1056, 1089, 1157, 1158, 1303)


class SocialSystem:
    """玩家对玩家交互：原生点击菜单的请求/确认/推送闭环。"""

    system_name = 'social'

    def __init__(
        self,
        settings=None,
        save: Callable[[], None] | None = None,
        find_role: Callable[[int], dict[str, object] | None] | None = None,
        online_role_ids: Callable[[], set[int]] | None = None,
        push_to_role: Callable[[int, tuple[bytes, ...]], None] | None = None,
        battle_system=None,
    ) -> None:
        self.settings = settings
        self.save = save or (lambda: None)
        self.find_role = find_role or (lambda role_id: None)
        self.online_role_ids = online_role_ids or (lambda: set())
        self.push_to_role = push_to_role or (lambda role_id, frames: None)
        self.battle_system = battle_system
        self.registry = SocialRegistry()

    # ------------------------------------------------------------------
    # 路由判定
    # ------------------------------------------------------------------
    def can_handle(self, context: SystemContext, message_id: int, fields: list[object]) -> bool:
        if context.active_role is None or message_id not in HANDLED_MESSAGE_IDS:
            return False
        if not fields:
            return False
        values = [field.value for field in fields]
        if message_id == 1004:
            # [int, short channel, short, int, string 对象, string 说话人, string 正文]
            return len(values) >= 7
        if message_id == 1009:
            # 赠送：[short 81, int 物品实例, int 对方 actor id]
            return len(values) >= 3 and int(values[0]) == GIFT_ACTION
        if message_id == 1089:
            # 仅剥离"查看他人"动作 2；角色页扩展信息(0)仍归 role 系统。
            first = fields[0]
            return bool(
                isinstance(first, Field) and first.type_id == TYPE_BYTE and int(first.value) == 2,
            )
        if message_id == 1303:
            # 查看请求固定 byte 2 开头（带 int id 或 int 0 + string 名字）。
            first = fields[0]
            return bool(
                isinstance(first, Field) and first.type_id == TYPE_BYTE and int(first.value) == 2,
            )
        if message_id == 1056:
            return int(values[0]) in (1, 2, 3, 4, 10, 20)
        return True

    def handle(self, context: SystemContext, message_id: int, fields: list[object]) -> RouteResult:
        values = [field.value for field in fields]
        role = context.active_role
        if message_id == 1303:
            return self._handle_view(context, values)
        if message_id == 1089:
            return RouteResult.handled((character_view_rows_frame(),))
        if message_id == 1019:
            return self._handle_friend(context, values)
        if message_id == 1056:
            return self._handle_trade(context, values)
        if message_id == 1009:
            return self._handle_gift(context, values)
        if message_id == 1157:
            return self._handle_spar(context, values)
        if message_id == 1158:
            return self._handle_pk(context, values)
        if message_id == 1004:
            return self._handle_chat(context, values)
        return RouteResult.not_handled()

    # ------------------------------------------------------------------
    # 解析辅助
    # ------------------------------------------------------------------
    def _role_by_actor_id(self, actor_id: int) -> dict[str, object] | None:
        from systems.map.protocol import PLAYER_ACTOR_ID_BASE
        role_id = int(actor_id) - PLAYER_ACTOR_ID_BASE
        if role_id <= 0:
            return None
        return self.find_role(role_id)

    def _resolve_target(self, values: list[object], actor_index: int = 1, name_index: int | None = None):
        """Resolve a clicked target from an actor id (or name) field pair."""
        actor_id = int(values[actor_index]) if len(values) > actor_index else 0
        target = self._role_by_actor_id(actor_id)
        if target is None and name_index is not None and len(values) > name_index:
            target = self._find_role_by_name(str(values[name_index]))
        return target

    def _find_role_by_name(self, name: str) -> dict[str, object] | None:
        if not name:
            return None
        for role_id in list(self.online_role_ids()):
            role = self.find_role(int(role_id))
            if role is not None and str(role.get('name', '')) == name:
                return role
        return None

    def _actor_id(self, role: dict[str, object]) -> int:
        from systems.map.protocol import player_actor_object_id
        return player_actor_object_id(int(role.get('id', 0)))

    def _level_of(self, role_id: int) -> int:
        role = self.find_role(int(role_id))
        if role is None:
            return 1
        return max(1, int(role.get('level', 1)))

    # ------------------------------------------------------------------
    # 1303/1089 查看
    # ------------------------------------------------------------------
    def _handle_view(self, context: SystemContext, values: list[object]) -> RouteResult:
        # C→S 1303/2 两种形态：[byte 2, int actor_id] 与 [byte 2, int 0, string 名字]。
        target = self._resolve_target(values, name_index=2)
        if target is None:
            LOG.info('VIEW_1303 target not found values=%r', values)
            return RouteResult.handled((top_message_frame('对方不在线'),))
        frame = player_view_frame(self.settings, target, self._actor_id(target))
        LOG.info(
            'VIEW_1303 user=%r role_id=%s target=%s(%s)',
            context.username, context.active_role.get('id'), target.get('name'), target.get('id'),
        )
        return RouteResult.handled((frame, character_view_rows_frame()))

    # ------------------------------------------------------------------
    # 1019 好友
    # ------------------------------------------------------------------
    def _handle_friend(self, context: SystemContext, values: list[object]) -> RouteResult:
        action = int(values[0])
        role = context.active_role
        role_id = int(role['id'])
        now = service.now()
        if action == 10:
            # 加友请求：C→S [byte 10, int 对方 actor id, string 对方名字]
            target = self._resolve_target(values, name_index=2)
            if target is None:
                return RouteResult.handled((top_message_frame('对方不在线'),))
            target_id = int(target['id'])
            if target_id == role_id:
                return RouteResult.handled((top_message_frame('您不可以加自己为好友'),))
            if any(int(row.get('id', 0)) == target_id for row in service.friends_of(role)):
                return RouteResult.handled((top_message_frame('对方已经在您的好友列表中'),))
            if target_id not in self.online_role_ids():
                return RouteResult.handled((top_message_frame('对方不在线'),))
            self.registry.friend_requests[target_id] = (role_id, now)
            prompt = friend_request_prompt_frame(
                role_id, str(role.get('name', '')), int(role.get('level', 1)),
            )
            self.push_to_role(target_id, (prompt,))
            LOG.info('FRIEND_1019 request user=%r role_id=%d target=%d', context.username, role_id, target_id)
            return RouteResult.handled((top_message_frame('好友请求已发送'),))
        if action == 11:
            # 接受：C→S [byte 11, int 请求方 role_id, string 名字]
            requester_id = int(values[1]) if len(values) > 1 else 0
            verified = self.registry.pop_friend_request(role_id, now)
            if verified is None or int(verified) != requester_id:
                return RouteResult.handled((top_message_frame('好友请求已过期'),))
            requester = self.find_role(requester_id)
            if requester is None:
                return RouteResult.handled((top_message_frame('对方不在线'),))
            service.add_friend(role, requester_id, str(requester.get('name', '')))
            service.add_friend(requester, role_id, str(role.get('name', '')))
            self.save()
            list_frame = friend_list_frame(
                service.friends_of(role), self.online_role_ids(), self._level_of,
            )
            requester_frame = friend_list_frame(
                service.friends_of(requester), self.online_role_ids(), self._level_of,
            )
            self.push_to_role(requester_id, (
                requester_frame, top_message_frame(f"{role.get('name', '')}同意了您的好友请求"),
            ))
            LOG.info('FRIEND_1019 accepted role_id=%d friend=%d', role_id, requester_id)
            return RouteResult.handled((
                list_frame, top_message_frame('添加好友成功'),
            ))
        if action == 20:
            # 拒绝：C→S [byte 20, int 请求方 role_id, string 名字]
            requester_id = int(values[1]) if len(values) > 1 else 0
            self.registry.friend_requests.pop(role_id, None)
            if requester_id in self.online_role_ids():
                self.push_to_role(requester_id, (
                    top_message_frame(f"{role.get('name', '')}拒绝了您的好友请求"),
                ))
            return RouteResult.handled()
        if action == 18:
            # 删除好友：C→S [byte 18, int 好友 role_id, string 名字]
            friend_id = int(values[1]) if len(values) > 1 else 0
            service.remove_friend(role, friend_id)
            self.save()
            return RouteResult.handled((
                friend_list_frame(service.friends_of(role), self.online_role_ids(), self._level_of),
                top_message_frame('已删除该好友'),
            ))
        if action == FRIEND_LIST_ACTION:
            return RouteResult.handled((
                friend_list_frame(service.friends_of(role), self.online_role_ids(), self._level_of),
            ))
        if action == ENEMY_LIST_ACTION:
            return RouteResult.handled((empty_enemy_list_frame(),))
        LOG.info('ignored friend action=%d values=%r', action, values)
        return RouteResult.handled()

    # ------------------------------------------------------------------
    # 1056 交易
    # ------------------------------------------------------------------
    def _handle_trade(self, context: SystemContext, values: list[object]) -> RouteResult:
        action = int(values[0])
        role = context.active_role
        role_id = int(role['id'])
        now = service.now()
        if action == 1:
            # 请求交易：C→S [byte 1, int 对方 actor id]
            target = self._resolve_target(values)
            if target is None:
                return RouteResult.handled((top_message_frame('对方不在线'),))
            target_id = int(target['id'])
            if target_id == role_id:
                return RouteResult.handled((top_message_frame('不能与自己交易'),))
            if target_id not in self.online_role_ids():
                return RouteResult.handled((top_message_frame('对方不在线'),))
            self.registry.trade_requests[target_id] = (role_id, now)
            self.push_to_role(target_id, (trade_request_frame(self._actor_id(role), str(role.get('name', ''))),))
            LOG.info('TRADE_1056 request user=%r role_id=%d target=%d', context.username, role_id, target_id)
            return RouteResult.handled((top_message_frame('交易请求已发送'),))
        if action == 2:
            # 接受：C→S [byte 2, int 发起人 actor id]
            requester_actor = int(values[1]) if len(values) > 1 else 0
            requester = self._role_by_actor_id(requester_actor)
            if requester is None:
                return RouteResult.handled((top_message_frame('交易请求已过期'),))
            verified = self.registry.pop_trade_request(role_id, now)
            if verified is None or int(verified) != int(requester['id']):
                return RouteResult.handled((top_message_frame('交易请求已过期'),))
            requester_id = int(requester['id'])
            self.registry.open_trade(requester_id, role_id)
            # e/eu 窗口标题读取 c(1) 作为"对方" actor id：
            # 接受方的窗口显示发起人，发起方的窗口显示接受人。
            open_frames = (
                trade_open_frame(self._actor_id(requester)),
                trade_open_frame(self._actor_id(role)),
            )
            self.push_to_role(requester_id, (open_frames[1],))
            LOG.info('TRADE_1056 accepted role_id=%d peer=%d', role_id, requester_id)
            return RouteResult.handled((open_frames[0],))
        if action == 3:
            # 拒绝：C→S [byte 3, int 发起人 actor id]
            requester = self._role_by_actor_id(int(values[1]) if len(values) > 1 else 0)
            self.registry.trade_requests.pop(role_id, None)
            if requester is not None and int(requester['id']) in self.online_role_ids():
                self.push_to_role(int(requester['id']), (top_message_frame('对方拒绝了交易请求'),))
            return RouteResult.handled()
        if action in (4, 3):
            # 关闭窗口(4)/拒绝(3)：C→S [byte 4|3, int 对方 actor id]
            peer_id = self.registry.trade_peer(role_id)
            self.registry.close_trade(role_id)
            if peer_id is not None and peer_id in self.online_role_ids():
                self.push_to_role(peer_id, (
                    top_message_frame('对方取消了交易'), *trade_close_frames(),
                ))
            LOG.info('TRADE_1056 cancel action=%d role_id=%d peer=%s', action, role_id, peer_id)
            return RouteResult.handled((*trade_close_frames(),))
        if action == 10:
            # 最终确认：e/eu 锁定后启用的确认按钮（0x3e92）发送。
            # C→S [byte 10, int 对方 actor id]
            return self._handle_trade_confirm(context, values)
        if action == 20:
            # 锁定：C→S [byte 20, int 银两, int 物品数, int*实例id, ...]
            return self._handle_trade_lock(context, values)
        return RouteResult.handled()

    def _handle_trade_lock(self, context: SystemContext, values: list[object]) -> RouteResult:
        role = context.active_role
        role_id = int(role['id'])
        peer_id = self.registry.trade_peer(role_id)
        if peer_id is None:
            return RouteResult.handled((top_message_frame('当前没有进行中的交易'),))
        money = int(values[1]) if len(values) > 1 else 0
        item_count = int(values[2]) if len(values) > 2 else 0
        item_ids = [int(x) for x in values[3:3 + max(0, item_count)]]
        offer = {'money': max(0, money), 'item_ids': item_ids}
        self.registry.trade_locks[role_id] = offer
        self.registry.trade_confirms.discard(role_id)
        peer = self.find_role(peer_id)
        if peer is None:
            return RouteResult.handled((top_message_frame('对方不在线，交易取消'),))
        # 对方窗口：显示锁定物品行（1056/8）+ 锁定金额（1056/6），
        # 并启用对方的最终确认按钮（1056/10，e/eu.c 初始禁用）。
        rows = self._staged_item_rows(role, item_ids)
        self.push_to_role(peer_id, (
            trade_peer_items_frame(rows),
            trade_peer_money_frame(money),
            trade_enable_confirm_frame(),
        ))
        LOG.info('TRADE_1056 locked role_id=%d offer=%r', role_id, offer)
        return RouteResult.handled((top_message_frame('已锁定，等待双方确认'),))

    def _staged_item_rows(self, role: dict[str, object], item_ids: list[int]) -> list[tuple[int, int, str, int, int, int]]:
        registry = self.settings.item_registry
        rows = []
        for item_id in item_ids:
            item = find_item(role, item_id)
            if item is None or item.get('location', 'bag') != 'bag':
                continue
            resolved = registry.resolve(item)
            rows.append((
                int(item.get('id', 0)),
                int(resolved.get('template_id', 0)),
                item_display_name(resolved),
                int(resolved.get('icon_code', 0)),
                int(item.get('quantity', 1)),
                int(resolved.get('equipment_slot', 0)),
            ))
        return rows

    def _handle_trade_confirm(self, context: SystemContext, values: list[object]) -> RouteResult:
        role = context.active_role
        role_id = int(role['id'])
        peer_id = self.registry.trade_peer(role_id)
        if peer_id is None:
            return RouteResult.handled((top_message_frame('当前没有进行中的交易'),))
        if role_id not in self.registry.trade_locks:
            return RouteResult.handled((top_message_frame('请先锁定交易物品'),))
        self.registry.trade_confirms.add(role_id)
        peer_lock = self.registry.trade_locks.get(peer_id)
        peer_confirmed = peer_id in self.registry.trade_confirms
        if not (peer_confirmed and peer_lock is not None):
            LOG.info('TRADE_1056 confirmed role_id=%d waiting peer=%d', role_id, peer_id)
            return RouteResult.handled((top_message_frame('已确认，等待对方确认'),))
        peer_offer = {
            'money': int(peer_lock.get('money', 0)),
            'item_ids': [int(x) for x in peer_lock.get('item_ids', [])],
        }
        my_lock = self.registry.trade_locks.get(role_id) or {}
        offer = {
            'money': int(my_lock.get('money', 0)),
            'item_ids': [int(x) for x in my_lock.get('item_ids', [])],
        }
        self.registry.trade_locks.pop(role_id, None)
        self.registry.trade_locks.pop(peer_id, None)
        self.registry.trade_confirms.discard(role_id)
        self.registry.trade_confirms.discard(peer_id)
        peer = self.find_role(peer_id)
        if peer is None:
            return RouteResult.handled((top_message_frame('对方不在线，交易取消'),))
        settlement = service.settle_trade(role, peer, offer, peer_offer)
        if not settlement.ok:
            self.registry.close_trade(role_id)
            self.push_to_role(peer_id, (
                top_message_frame(f'交易失败：{settlement.reason}'), *trade_close_frames(),
            ))
            LOG.info('TRADE_1056 failed role_id=%d peer=%d reason=%s', role_id, peer_id, settlement.reason)
            return RouteResult.handled((
                top_message_frame(f'交易失败：{settlement.reason}'), *trade_close_frames(),
            ))

        from systems.inventory.protocol import item_frame

        def side_frames(my_id: int, my_role) -> tuple[bytes, ...]:
            removed, added, silver_delta = settlement.sides[my_id]
            frames: list[bytes] = []
            for item in removed:
                frames.append(encode_frame(1009, [byte(3), integer(int(item.get('id', 0)))]))
            for item in added:
                frames.append(item_frame(item, operation=3))
            if silver_delta:
                frames.append(service.currency_frame(
                    my_id, SILVER_PROPERTY, service.currency_balance(my_role, 'silver'),
                ))
            frames.append(trade_complete_frame())
            frames.extend(trade_close_frames())
            frames.append(top_message_frame('交易完成'))
            return tuple(frames)

        my_frames = side_frames(role_id, role)
        peer_frames = side_frames(peer_id, peer)
        self.registry.close_trade(role_id)
        self.save()
        self.push_to_role(peer_id, peer_frames)
        LOG.info(
            'TRADE_1056 settled role_id=%d peer=%d items=%d/%d silver=%d/%d',
            role_id, peer_id,
            len(offer['item_ids']), len(peer_offer['item_ids']),
            offer['money'], peer_offer['money'],
        )
        return RouteResult.handled(my_frames)

    # ------------------------------------------------------------------
    # 1009/81 赠送
    # ------------------------------------------------------------------
    def _handle_gift(self, context: SystemContext, values: list[object]) -> RouteResult:
        role = context.active_role
        role_id = int(role['id'])
        item_id = int(values[1]) if len(values) > 1 else 0
        target = self._role_by_actor_id(int(values[2]) if len(values) > 2 else 0)
        if target is None or int(target['id']) not in self.online_role_ids():
            return RouteResult.handled((top_message_frame('对方不在线'),))
        target_id = int(target['id'])
        if target_id == role_id:
            return RouteResult.handled((top_message_frame('不能赠送给自己'),))
        item = find_item(role, item_id)
        if item is None or item.get('location', 'bag') != 'bag':
            return RouteResult.handled((top_message_frame('物品已不在背包中'),))
        from systems.inventory.protocol import item_frame
        from systems.inventory.service import bag_capacity, bag_item_count
        if bag_item_count(target) + 1 > bag_capacity(target):
            return RouteResult.handled((top_message_frame('对方背包已满'),))
        role_items(role).remove(item)
        role_items(target).append(item)
        self.save()
        display = item_display_name(self.settings.item_registry.resolve(item))
        removal = encode_frame(1009, [byte(3), integer(item_id)])
        self.push_to_role(target_id, (
            item_frame(item, operation=3),
            top_message_frame(f"收到来自 {role.get('name', '')} 的赠送：{display}"),
        ))
        LOG.info(
            'GIFT_1009 user=%r role_id=%d item=%d target=%d',
            context.username, role_id, item_id, target_id,
        )
        return RouteResult.handled((
            removal, top_message_frame(f"已将 {display} 赠送给 {target.get('name', '')}"),
        ))

    # ------------------------------------------------------------------
    # 1157 切磋 / 1158 PK（双方确认后进入战斗系统的双人对决）
    # ------------------------------------------------------------------
    def _handle_spar(self, context: SystemContext, values: list[object]) -> RouteResult:
        action = int(values[0])
        role = context.active_role
        if action == 2:
            # C→S [byte 2, int 自己 role_id, int 对方 actor id]
            target = self._resolve_target(values, actor_index=2)
            if target is None or int(target['id']) not in self.online_role_ids():
                return RouteResult.handled((top_message_frame('对方不在线'),))
            target_id = int(target['id'])
            self.push_to_role(target_id, (spar_ack_frame(self._actor_id(role), self._actor_id(target)),))
            LOG.info('SPAR_1157 request role_id=%d target=%d', int(role['id']), target_id)
            return RouteResult.handled((top_message_frame('切磋请求已发送，等待对方应答'),))
        if action == 4:
            # 目标客户端 e/cu 的自动应答：C→S [byte 4, int 发起人 actor, int 自己 actor]
            requester = self._role_by_actor_id(int(values[1]) if len(values) > 1 else 0)
            if requester is None or int(requester['id']) not in self.online_role_ids():
                return RouteResult.handled()
            return self._start_duel(context, requester, '切磋')
        return RouteResult.handled()

    def _handle_pk(self, context: SystemContext, values: list[object]) -> RouteResult:
        action = int(values[0])
        role = context.active_role
        if action == 2:
            # C→S [byte 2, int 自己 role_id, int 对方 actor id]
            target = self._resolve_target(values, actor_index=2)
            if target is None or int(target['id']) not in self.online_role_ids():
                return RouteResult.handled((top_message_frame('对方不在线'),))
            target_id = int(target['id'])
            self.push_to_role(target_id, (pk_request_prompt_frame(self._actor_id(role)),))
            LOG.info('PK_1158 request role_id=%d target=%d', int(role['id']), target_id)
            return RouteResult.handled((top_message_frame('PK请求已发送，等待对方应答'),))
        if action == 6:
            # 目标确认：C→S [byte 6, int 自己 role_id, int 发起人 actor id]
            requester = self._role_by_actor_id(int(values[2]) if len(values) > 2 else 0)
            if requester is None or int(requester['id']) not in self.online_role_ids():
                return RouteResult.handled()
            return self._start_duel(context, requester, 'PK')
        return RouteResult.handled()

    def _start_duel(
        self,
        context: SystemContext,
        challenger: dict[str, object],
        kind: str,
    ) -> RouteResult:
        """双方确认后进入战斗系统的共享对决：应答方帧入应答，挑战方帧推送。"""
        defender = context.active_role
        if self.battle_system is None:
            LOG.warning('duel requested without battle system wired')
            return RouteResult.handled((top_message_frame('战斗系统未就绪'),))
        frames = self.battle_system.start_duel(challenger, defender, kind=kind)
        if not frames:
            return RouteResult.handled((top_message_frame('对方正在战斗中'),))
        LOG.info(
            'DUEL_ACCEPT kind=%s challenger=%d defender=%d',
            kind, int(challenger['id']), int(defender['id']),
        )
        return RouteResult.handled(frames)

    # ------------------------------------------------------------------
    # 1004 聊天中继（私聊定向，同图广播）
    # ------------------------------------------------------------------
    def _handle_chat(self, context: SystemContext, values: list[object]) -> RouteResult:
        channel = int(values[1])
        target_name = str(values[4] or '')
        speaker = str(values[5] or context.username)
        text = str(values[6] or '')
        if not text:
            return RouteResult.handled()
        frame = chat_frame(channel, speaker, target_name, text)
        role = context.active_role
        if channel == CHAT_CHANNEL_PRIVATE:
            target = self._find_role_by_name(target_name)
            if target is None or int(target['id']) not in self.online_role_ids():
                return RouteResult.handled((top_message_frame('对方不在线，私聊未送达'),))
            self.push_to_role(int(target['id']), (frame,))
            LOG.info('CHAT_1004 private speaker=%r target=%r', speaker, target_name)
            return RouteResult.handled()
        for receiver_id in list(self.online_role_ids()):
            receiver = self.find_role(int(receiver_id))
            if receiver is None:
                continue
            if int(receiver.get('map_id', -1)) != int(role.get('map_id', -2)):
                continue
            self.push_to_role(int(receiver_id), (frame,))
        LOG.info('CHAT_1004 broadcast channel=%d speaker=%r', channel, speaker)
        return RouteResult.handled()


def register_social_routes(router: SystemRouter, system: SocialSystem) -> None:
    router.register(system.system_name, system.can_handle, system.handle)
