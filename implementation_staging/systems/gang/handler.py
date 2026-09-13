"""Gang system protocol entry routed through app.router.SystemRouter."""

from __future__ import annotations

import logging
from pathlib import Path

from app.context import SystemContext
from app.notify import top_message_frame
from app.router import RouteResult, SystemRouter
from systems.gang.protocol import GangProtocol
from systems.gang.registry import (
    GANG_ADMIN_CREATE_OPTION,
    GANG_ADMIN_DISBAND_CONFIRM_OPTION,
    GANG_ADMIN_DISBAND_OPTION,
    GANG_ADMIN_SERVICE,
    GANG_CREATION_COST_SILVER,
    GANG_MESSAGE_IDS,
    GANG_POSITION_LEADER,
    MAX_GANG_NAME_LENGTH,
)
from systems.gang.service import (
    GangService,
    Notifier,
    OnlineCheck,
    RoleLookup,
    default_gang_service,
)

LOG = logging.getLogger('piaomiao-local')


class GangSystem:
    """帮派系统边界：协议入口委托 service，通知走 notifier 回调。"""

    system_name = 'gang'

    def __init__(
        self,
        store_path: Path | str,
        save_roles,
        role_lookup: RoleLookup,
        online_check: OnlineCheck | None = None,
        notifier: Notifier | None = None,
    ) -> None:
        self.service = default_gang_service(
            Path(store_path),
            save_roles,
            role_lookup,
            online_check=online_check,
            notifier=notifier,
        )
        self.protocol = GangProtocol()

    def can_handle(self, _context: SystemContext, message_id: int, _fields: list[object]) -> bool:
        return message_id in GANG_MESSAGE_IDS

    def handle(self, context: SystemContext, message_id: int, fields: list[object]) -> RouteResult:
        role = context.active_role
        if role is None:
            # Consume the message so the server does not log it as unimplemented.
            return RouteResult.handled(reason='no_active_role')
        result = self.service.handle_message(message_id, fields, role)
        for target_role_id, frames in result.notifications:
            if self.service._notifier is not None:
                self.service._notifier(target_role_id, frames)
        return RouteResult.handled(result.replies, reason=result.reason)

    # ------------------------------------------------------------------
    # 帮派管理员 NPC（长安 12,68）——由地图系统的 2031/2032 交互回调
    # ------------------------------------------------------------------

    @staticmethod
    def _dialogue_record(kind: int, *, option_id: int = 0, text: str = '', icon: int = 0, max_length: int = 0):
        """2032 对话记录为 8 个字段；kind 3 的 short 字段是输入框最大长度
        （客户端 e/cb sswitch_2：d/f.a(true) 打开输入框并注册选项行）。"""
        from protocol import byte, integer, short, string
        return [
            integer(0),
            integer(0),
            integer(0),
            short(max_length),
            integer(option_id),
            byte(kind),
            string(text),
            integer(icon),
        ]

    @classmethod
    def _dialogue_frame(cls, npc_id: int, records: list) -> bytes:
        from protocol import byte, encode_frame, integer
        flat: list = []
        for record in records:
            flat.extend(record)
        return encode_frame(2032, [
            integer(int(npc_id)),
            byte(len(flat) // 8),
            *flat,
        ])

    def npc_dialogue_frames(self, npc, role, settings) -> list[bytes] | None:
        """帮派管理员对话：无帮派提供"创建帮派"（输入框），帮主提供"解散帮派"。"""
        if str(getattr(npc, 'service', '')) != GANG_ADMIN_SERVICE:
            return None

        introduction = str(
            getattr(npc, 'introduction', '') or getattr(npc, 'label', '') or getattr(npc, 'name', '')
        )
        records = [self._dialogue_record(1, text=introduction)]
        if role is not None and not self.service.role_gang_id(role):
            records.append(self._dialogue_record(
                3,
                option_id=GANG_ADMIN_CREATE_OPTION,
                text=f'创建帮派（需{GANG_CREATION_COST_SILVER}两白银）',
                max_length=MAX_GANG_NAME_LENGTH,
            ))
        elif role is not None and self.service.role_position(role) == GANG_POSITION_LEADER:
            records.append(self._dialogue_record(
                2,
                option_id=GANG_ADMIN_DISBAND_OPTION,
                text='解散帮派',
            ))
        records.append(self._dialogue_record(2, option_id=0, text='结束对话'))
        records.append(self._dialogue_record(100))
        return [self._dialogue_frame(int(npc.id), records)]

    def _disband_confirm_frame(self, npc_id: int, gang_name: str) -> bytes:
        records = [
            self._dialogue_record(1, text=f'确定要解散帮派「{gang_name}」吗？此操作不可恢复，全体成员将被移出帮派。'),
            self._dialogue_record(2, option_id=GANG_ADMIN_DISBAND_CONFIRM_OPTION, text='确认解散'),
            self._dialogue_record(2, option_id=0, text='再想想'),
            self._dialogue_record(100),
        ]
        return self._dialogue_frame(npc_id, records)

    def npc_dialogue_option(self, settings, role, state, option_id: int, input_text: str = '') -> list[bytes] | None:
        """处理帮派管理员选项；其余选项交回地图默认 ACK。

        客户端选中选项后回传 2032 [byte option_id, byte 101, string 输入内容]
        （e/cb c() pswitch_1），输入框可见时携带输入文本。
        """
        from systems.map.protocol import map_npc_for_object_id, map_object_interaction_ack_frame
        from systems.map.service import settings_for_role
        if role is None or int(option_id) not in (
            GANG_ADMIN_CREATE_OPTION,
            GANG_ADMIN_DISBAND_OPTION,
            GANG_ADMIN_DISBAND_CONFIRM_OPTION,
        ):
            return None

        try:
            definition = settings_for_role(settings, role)
        except ValueError:
            return None

        if state.map_id != definition.id or state.npc_id is None:
            return None

        npc = map_npc_for_object_id(definition, state.npc_id)
        if npc is None or str(getattr(npc, 'service', '')) != GANG_ADMIN_SERVICE:
            return None

        ack = map_object_interaction_ack_frame(0)

        def fail(message: str) -> list[bytes]:
            return [ack, top_message_frame(message)]

        if int(option_id) == GANG_ADMIN_CREATE_OPTION:
            try:
                name = str(input_text or '').strip()
                if not name:
                    return fail('请在输入框填写帮派名称')
                result = self.service.create_gang(role, name=name)
                if result.reason == 'gang_created':
                    gang = self.service.store.gangs.get(self.service.role_gang_id(role))
                    gang_name = gang.name if gang is not None else name
                    LOG.info(
                        'GANG_CREATED role_id=%d npc_id=%d gang=%r cost=%d',
                        int(role.get('id', 0)),
                        int(npc.id),
                        gang_name,
                        GANG_CREATION_COST_SILVER,
                    )
                    return [
                        ack,
                        top_message_frame(f'帮派「{gang_name}」创建成功！'),
                        *result.replies,
                    ]
                if result.reason == 'insufficient_silver':
                    return fail(f'银两不足，创建帮派需要{GANG_CREATION_COST_SILVER}两白银')
                if result.reason == 'already_in_gang':
                    return fail('你已有帮派，无需重复创建')
                if result.reason == 'name_taken':
                    return fail('该帮派名已被使用')
                if result.reason == 'invalid_name':
                    return fail(f'帮派名称需为1-{MAX_GANG_NAME_LENGTH}个字')
                return fail('帮派创建失败')
            finally:
                state.clear()

        if int(option_id) == GANG_ADMIN_DISBAND_OPTION:
            # 第一步：回发确认对话。保持对话状态选中，等确认选项提交。
            gang = self.service.store.gangs.get(self.service.role_gang_id(role))
            if gang is None:
                state.clear()
                return fail('你还没有加入帮派')
            if self.service.role_position(role) != GANG_POSITION_LEADER:
                state.clear()
                return fail('只有帮主可以解散帮派')
            return [ack, self._disband_confirm_frame(int(npc.id), gang.name)]

        # GANG_ADMIN_DISBAND_CONFIRM_OPTION：第二步确认。
        try:
            result = self.service.disband_gang(role)
            if result.reason == 'disbanded':
                # NPC 对话回调不经 handle()，通知需在此分发给在线成员。
                for target_role_id, frames in result.notifications:
                    if self.service._notifier is not None:
                        self.service._notifier(target_role_id, frames)
                LOG.info(
                    'GANG_DISBANDED role_id=%d npc_id=%d notified=%d',
                    int(role.get('id', 0)),
                    int(npc.id),
                    len(result.notifications),
                )
                return [
                    ack,
                    top_message_frame('帮派已解散'),
                    *result.replies,
                ]
            if result.reason == 'not_leader':
                return fail('只有帮主可以解散帮派')
            return fail('当前没有可解散的帮派')
        finally:
            state.clear()


def register_gang_routes(router: SystemRouter, system: GangSystem) -> None:
    router.register(system.system_name, system.can_handle, system.handle)


__all__ = ['GangSystem', 'GangService', 'register_gang_routes']
