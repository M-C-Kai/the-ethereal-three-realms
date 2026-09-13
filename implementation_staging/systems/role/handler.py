from __future__ import annotations

import hmac
import logging
import time
from dataclasses import dataclass

from app.context import SystemContext
from app.router import RouteResult, SystemRouter
from app.notify import top_message_frame
from systems.role.events import CharacterUpdateEvent
from systems.role.protocol import (
    is_mount_atlas_request, load_mount_atlas_entries, mount_atlas_frame,
)
from systems.map.service import relocate_role_for_cold_login
from systems.role.protocol import (
    MENU_PREFETCH_EMPTY_SUBTYPES, account_result, battle_progress_frame,
    character_extension_info, character_panel_frames, creation_names,
    deletion_result, is_logout_confirm_request, is_logout_page_request,
    level_up_effect_frame, login_server_list, logout_ack_frame,
    logout_page_frame, mail_request_frames, menu_prefetch_empty_ack,
    role_list, game_server_redirect,
)
from systems.role.service import (
    _get_sect_skill_level, apply_one_level, normalized_sect_id,
    sect_skill_request_frames,
)


LOG = logging.getLogger('piaomiao-local')

# 账号操作结果码：注册/改密/找回共用 1055 应答。
_ACCOUNT_REGISTER_CODES = {'ok': 0, 'invalid': 1, 'exists': 2}
_ACCOUNT_CHANGE_CODES = {'ok': 3, 'invalid': 1, 'denied': 5}


@dataclass(frozen=True)
class RoleActionResult:
    handled: bool
    event: str = ''
    role: dict[str, object] | None = None
    frames: tuple[bytes, ...] = ()
    role_id: int = 0


class RoleSystem:
    """role 系统边界：账号、登录跳转、角色、门派技能、面板、邮件与登出。"""

    system_name = 'role'

    def __init__(
        self,
        settings=None,
        store=None,
        accounts=None,
        session_tokens=None,
        role_entry_factory=None,
        role_list_factory=None,
        role_creation_factory=None,
        character_update_bus=None,
        flush_position=None,
    ):
        self.settings = settings
        self.store = store
        self.accounts = accounts
        self.session_tokens = session_tokens
        self.role_entry_factory = role_entry_factory
        self.role_list_factory = role_list_factory
        self.role_creation_factory = role_creation_factory
        self.character_update_bus = character_update_bus
        self.flush_position = flush_position

    # ------------------------------------------------------------------
    # 路由判定
    # ------------------------------------------------------------------
    def can_handle(self, context: SystemContext, message_id: int, fields: list[object]) -> bool:
        values = [field.value for field in fields]
        if message_id == 1010:
            # 人物面板的自动升级开关挂在 1010 通道上（1010/36）。
            return bool(values) and int(values[0]) == 36
        if message_id in (1055, 1051, 1052, 1077, 1054, 1003):
            # 1054 只认 APK 精确的登出页请求；其余 1054 归福缘系统。
            if message_id == 1054:
                return is_logout_page_request(fields)
            if message_id == 1003:
                return is_logout_confirm_request(fields)
            return True
        if message_id in (1080, 1024) and values:
            return True
        if message_id in (1039, 1103, 1129, 1500):
            return context.active_role is not None and bool(values)
        if message_id == 1089:
            return context.active_role is not None
        if message_id in MENU_PREFETCH_EMPTY_SUBTYPES:
            return True
        return False

    def handle(self, context: SystemContext, message_id: int, fields: list[object]) -> RouteResult:
        values = [field.value for field in fields]
        if message_id == 1055:
            return self._handle_account_ops(context, values)
        if message_id == 1077:
            return self._handle_login(context, values)
        if message_id == 1051:
            return self._handle_server_select(context, values)
        if message_id == 1052:
            return self._handle_game_handshake(context, values)
        if message_id == 1080:
            return self._handle_role_action(context, values)
        if message_id == 1039:
            return self._handle_character_panel(context, values)
        if message_id == 1089:
            LOG.info('character extension data requested values=%r', values)
            return RouteResult.handled((character_extension_info(),))
        if message_id == 1103:
            return self._handle_sect_skill(context, values)
        if message_id == 1129:
            return self._handle_manual_level_up(context, values)
        if message_id == 1500:
            return self._handle_mail(context, values)
        if message_id == 1024:
            return self._handle_mount_atlas(context, fields, values)
        if message_id == 1010:
            return self._handle_auto_level_toggle(context, values)
        if message_id == 1054:
            return self._handle_logout_page(context)
        if message_id == 1003:
            return self._handle_logout_confirm(context)
        if message_id in MENU_PREFETCH_EMPTY_SUBTYPES:
            LOG.info(
                'menu prefetch acknowledged as empty message=%d values=%r',
                message_id, values,
            )
            return RouteResult.handled((menu_prefetch_empty_ack(message_id),))
        return RouteResult.not_handled()

    # ------------------------------------------------------------------
    # 1055 账号操作
    # ------------------------------------------------------------------
    def _handle_account_ops(self, context: SystemContext, values: list[object]) -> RouteResult:
        if not values:
            return RouteResult.not_handled()
        action = int(values[0])
        if action == 0:
            requested_username = str(values[1]) if len(values) > 1 else ''
            requested_password = str(values[2]) if len(values) > 2 else ''
            result = self.accounts.register(requested_username, requested_password)
            return RouteResult.handled((account_result(_ACCOUNT_REGISTER_CODES[result]),))
        if action == 3:
            requested_username = str(values[1]) if len(values) > 1 else ''
            old_password = str(values[2]) if len(values) > 2 else ''
            new_password = str(values[3]) if len(values) > 3 else ''
            result = self.accounts.change_password(requested_username, old_password, new_password)
            return RouteResult.handled((account_result(_ACCOUNT_CHANGE_CODES[result]),))
        if action == 7:
            requested_username = str(values[4]) if len(values) > 4 else ''
            phone = str(values[5]) if len(values) > 5 else ''
            result, temporary_password = self.accounts.recover_password(requested_username, phone)
            message = f'临时密码：{temporary_password}' if result == 'ok' else '账号或手机号不匹配'
            return RouteResult.handled((account_result(6, message),))
        return RouteResult.handled((account_result(6, '暂不支持该账号操作'),))

    # ------------------------------------------------------------------
    # 1077 登录
    # ------------------------------------------------------------------
    def _handle_login(self, context: SystemContext, values: list[object]) -> RouteResult:
        requested_username = str(values[3]) if len(values) > 3 else ''
        password = str(values[4]) if len(values) > 4 else ''
        version = int(values[0]) if values else -1
        LOG.info(
            'login request user=%r password=%s version=%s',
            requested_username, '*' * len(password), version,
        )
        if not requested_username or not password:
            context.session['username'] = ''
            return RouteResult.handled((account_result(5),))
        if version != self.settings.expected_client_version:
            context.session['username'] = ''
            return RouteResult.handled((account_result(6, '客户端版本不匹配')))
        if not self.settings.accept_any_credentials and not self.accounts.authenticate(requested_username, password):
            context.session['username'] = ''
            return RouteResult.handled((account_result(5),))
        context.session['username'] = requested_username
        return RouteResult.handled((login_server_list(self.settings),))

    # ------------------------------------------------------------------
    # 1051 选服
    # ------------------------------------------------------------------
    def _handle_server_select(self, context: SystemContext, values: list[object]) -> RouteResult:
        requested_username = str(values[0]) if values else ''
        password = str(values[1]) if len(values) > 1 else ''
        selected = str(values[2]) if len(values) > 2 else ''
        session_username = str(context.session.get('username', ''))
        authenticated = bool(session_username) and hmac.compare_digest(session_username, requested_username)
        if authenticated and not self.settings.accept_any_credentials:
            authenticated = self.accounts.authenticate(requested_username, password)
        if not authenticated:
            return RouteResult.handled((account_result(5),))
        session_id, account_id = self.session_tokens.create(requested_username)
        LOG.info(
            'server selected user=%r address=%r session=%d',
            requested_username, selected, session_id,
        )
        return RouteResult.handled(
            (game_server_redirect(self.settings, session_id, account_id),)
        )

    # ------------------------------------------------------------------
    # 1052 游戏握手
    # ------------------------------------------------------------------
    def _handle_game_handshake(self, context: SystemContext, values: list[object]) -> RouteResult:
        session_id = int(values[0]) if values else 0
        account_id = int(values[1]) if len(values) > 1 else 0
        username = self.session_tokens.pop(session_id, account_id)
        LOG.info(
            'game handshake user=%r session=%d account=%d',
            username, session_id, account_id,
        )
        if not username:
            return RouteResult.handled((account_result(5),))
        context.session['username'] = username
        context.session['game_ready'] = True
        roles = self.store.roles_for(username, create_default=False)
        return RouteResult.handled((role_list(self.settings, roles),))

    # ------------------------------------------------------------------
    # 1080 角色列表/创建/删除/选择
    # ------------------------------------------------------------------
    def _handle_role_action(self, context: SystemContext, values: list[object]) -> RouteResult:
        username = str(context.session.get('username', ''))
        if int(values[0]) == 0 and self.flush_position is not None:
            self.flush_position(context)
        role_result = self.handle_action(username, values)
        if role_result.event == 'selected' and role_result.role is not None:
            context.session['active_role'] = role_result.role
            context.session['role.selected_role_id'] = role_result.role_id
            LOG.info(
                '%s',
                self._appearance_log(username, role_result.role),
            )
        if role_result.frames:
            return RouteResult.handled(role_result.frames)
        if role_result.handled:
            return RouteResult.handled()
        return RouteResult.not_handled()

    def handle_action(self, username: str, values: list[object]) -> RoleActionResult:
        if not values or self.store is None:
            return RoleActionResult(False)
        action = int(values[0])
        if action == 0:
            role_id = int(values[1]) if len(values) > 1 else 0
            role = self.store.find(username, role_id)
            if role is None:
                return RoleActionResult(True, 'unknown', role_id=role_id)
            if relocate_role_for_cold_login(self.settings, role):
                self.store.save()
            frames = tuple(self.role_entry_factory(self.settings, role)) if self.role_entry_factory else ()
            return RoleActionResult(True, 'selected', role, frames, role_id)
        if action == 1:
            role_id = int(values[1]) if len(values) > 1 else 0
            self.store.delete(username, role_id)
            return RoleActionResult(True, 'deleted', frames=(deletion_result(role_id),), role_id=role_id)
        if action == 2:
            name = str(values[1]) if len(values) > 1 else ''
            model = int(values[2]) if len(values) > 2 else 0
            slot = int(values[3]) if len(values) > 3 else 0
            role = self.store.create(username, name, model, slot)
            roles = self.store.roles_for(username)
            frames = tuple(self.role_creation_factory(self.settings, roles)) if self.role_creation_factory else ()
            return RoleActionResult(True, 'created', role, frames, int(role['id']))
        if action == 4:
            return RoleActionResult(True, 'names', frames=(creation_names(),))
        return RoleActionResult(False)

    def _appearance_log(self, username: str, role: dict[str, object]) -> str:
        from systems.role.protocol import format_map_player_appearance_log
        return format_map_player_appearance_log(username, role, self.settings)

    # ------------------------------------------------------------------
    # 1039 人物属性页
    # ------------------------------------------------------------------
    def _handle_character_panel(self, context: SystemContext, values: list[object]) -> RouteResult:
        role = context.active_role
        action = int(values[0])
        attributes, divine = character_panel_frames(role)
        if action == 1:
            LOG.info(
                'character panel requested; sending level/EXP sync plus attributes and divine-power summary',
            )
            return RouteResult.handled((
                battle_progress_frame(role),
                attributes,
                divine,
            ))
        if action == 2:
            LOG.info('character divine-power detail requested values=%r', values)
            return RouteResult.handled((divine,))
        LOG.info('ignored character panel action=%d values=%r', action, values)
        return RouteResult.handled()

    # ------------------------------------------------------------------
    # 1103 门派技能
    # ------------------------------------------------------------------
    def _handle_sect_skill(self, context: SystemContext, values: list[object]) -> RouteResult:
        role = context.active_role
        action = int(values[0])
        skill_id = int(values[1]) if len(values) > 1 else 0
        before_level = _get_sect_skill_level(role, skill_id, self.settings)
        response_frames = sect_skill_request_frames(role, values, self.settings)
        if _get_sect_skill_level(role, skill_id, self.settings) != before_level:
            self.store.save()
        LOG.info(
            'sect skill request action=%d values=%r response_count=%d',
            action,
            values,
            len(response_frames),
        )
        return RouteResult.handled(tuple(response_frames))

    # ------------------------------------------------------------------
    # 1129 手动升级
    # ------------------------------------------------------------------
    def _handle_manual_level_up(self, context: SystemContext, values: list[object]) -> RouteResult:
        role = context.active_role
        action = int(values[0])
        if action != 3:
            LOG.info('ignored level action=%d values=%r', action, values)
            return RouteResult.handled()
        if not apply_one_level(role):
            return RouteResult.handled((top_message_frame('经验不足，无法升级'),))
        self.store.save()
        LOG.info(
            'manual level-up user=%r role_id=%d level=%d experience=%d',
            context.username,
            int(role['id']),
            int(role['level']),
            int(role['experience']),
        )
        refresh = self.character_update_bus.publish(
            CharacterUpdateEvent.CHARACTER_LEVEL_CHANGED,
            role=role,
            registry=self.settings.item_registry,
        )
        return RouteResult.handled((
            battle_progress_frame(role),
            level_up_effect_frame(role),
            *refresh.frames,
        ))

    # ------------------------------------------------------------------
    # 1500 邮件
    # ------------------------------------------------------------------
    def _handle_mail(self, context: SystemContext, values: list[object]) -> RouteResult:
        role = context.active_role
        response_frames, changed = mail_request_frames(role, values)
        if changed:
            self.store.save()
        LOG.info(
            'mail action user=%r role_id=%d action=%d replies=%d changed=%s',
            context.username,
            int(role['id']),
            int(values[0]),
            len(response_frames),
            changed,
        )
        return RouteResult.handled(tuple(response_frames))

    # ------------------------------------------------------------------
    # 1024 坐骑图鉴
    # ------------------------------------------------------------------
    def _handle_mount_atlas(self, context: SystemContext, fields: list[object], values: list[object]) -> RouteResult:
        if is_mount_atlas_request(fields):
            entries = load_mount_atlas_entries()
            LOG.info(
                'MOUNT_1024 action=30 user=%r role_id=%s atlas_count=%d',
                context.username,
                int(context.active_role['id']) if context.active_role is not None else None,
                len(entries),
            )
            return RouteResult.handled((mount_atlas_frame(entries),))
        LOG.info('ignored mount protocol values=%r', values)
        return RouteResult.handled()

    def _fields_ref(self, context: SystemContext, message_id: int):
        return context.session.get(f'fields.{message_id}')

    # ------------------------------------------------------------------
    # 1010/36 自动升级开关
    # ------------------------------------------------------------------
    def _handle_auto_level_toggle(self, context: SystemContext, values: list[object]) -> RouteResult:
        role = context.active_role
        # The character panel sends [short(36), int(0=automatic, 1=manual)].
        manual = bool(int(values[1])) if len(values) > 1 else False
        role['auto_level'] = not manual
        self.store.save()
        LOG.info(
            'level mode changed user=%r automatic=%s',
            context.username, not manual,
        )
        return RouteResult.handled()

    # ------------------------------------------------------------------
    # 1054/1003 登出
    # ------------------------------------------------------------------
    def _handle_logout_page(self, context: SystemContext) -> RouteResult:
        # APK logout step 1: open the logout confirmation page.
        LOG.info('logout page requested user=%r', context.username)
        return RouteResult.handled((logout_page_frame(),))

    def _handle_logout_confirm(self, context: SystemContext) -> RouteResult:
        # APK logout step 2: clean logout. Persist any position
        # change that has not been checkpointed yet, then ack.
        if self.flush_position is not None:
            self.flush_position(context)
        role = context.active_role
        LOG.info(
            'ROLE_LOGOUT_ACK user=%r role_id=%d',
            context.username,
            int(role.get('id', 0)) if role is not None else 0,
        )
        # Keep the loop alive after the ack: the original APK
        # waits about one second, cleans up role/UI state, then
        # closes the connection itself. Never break/return/close
        # here; the finally block only runs on real disconnect.
        return RouteResult.handled((logout_ack_frame(),))


def register_role_routes(router: SystemRouter, system: RoleSystem) -> None:
    router.register(system.system_name, system.can_handle, system.handle)
