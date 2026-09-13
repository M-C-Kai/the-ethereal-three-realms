from __future__ import annotations

import asyncio
import logging
import time
from dataclasses import dataclass
from typing import Any, Optional

from app.context import SystemContext
from app.router import RouteResult, SystemRouter
from systems.battle.service import (
    CONTACT_RADIUS_TILES, battle_state_for, update_escape_guard_for_movement,
)
from systems.map.protocol import (
    ROAMING_BOSS_ID, ROAMING_BOSS_MAP_ID, ROAMING_BOSS_MOVE_DELAY_SECONDS,
    ROAMING_BOSS_TARGET_X, ROAMING_BOSS_TARGET_Y,
    dynamic_map_enter_frames, is_map_pathfind_request,
    is_roaming_boss_definition, map_actor_move_frame,
    map_data_frames, map_movement_final_tile, map_npc_frame,
    map_npc_dialogue_frames, map_npc_for_object_id, map_monster_for_object_id,
    map_npcs_near, map_object_interaction_ack_frame, map_object_interaction_values,
    map_object_remove_frame, map_pathfind_frame, npc_dialogue_option_frames,
    notice_and_world, player_actor_object_id,
    roaming_boss_move_frame,
)
from systems.map.service import (
    apply_portal_transition, settings_for_role, update_role_position,
)
from systems.role.protocol import (
    character_appearance, character_appearance_frame, player_appear_frame,
)
from systems.role.registry import mount_ride_code_for_role
from systems.skill.protocol import gather_spawn_frame


LOG = logging.getLogger('piaomiao-local')

POSITION_CHECKPOINT_SECONDS = 5.0

# APK 1005/1014 玩家对象（b/v）的邻近阈值：接收端逐轴 |Δ| ≤ 20 才走路/出现，
# 超出即移除对象（pmsj/work/main/e.smali 1005 内联处理的 cond_15..cond_18）。
PLAYER_STREAM_RADIUS = 20


@dataclass(frozen=True)
class MapHandleResult:
    handled: bool
    frames: tuple[bytes, ...] = ()
    reason: str = ''


@dataclass(frozen=True)
class MapInteractionResult:
    kind: str
    current_map: object
    entity: object | None = None
    target_map: object | None = None


class LocalNpcDialogueState:
    """Connection-local guard for one native 2032 NPC dialogue."""

    def __init__(self) -> None:
        self.map_id: int | None = None
        self.npc_id: int | None = None

    def select(self, map_id: int, npc_id: int) -> None:
        self.map_id = int(map_id)
        self.npc_id = int(npc_id)

    def clear(self) -> None:
        self.map_id = None
        self.npc_id = None


def dialogue_for(session: dict[str, object]) -> LocalNpcDialogueState:
    state = session.get('map.dialogue')
    if not isinstance(state, LocalNpcDialogueState):
        state = LocalNpcDialogueState()
        session['map.dialogue'] = state
    return state


class MapSystem:
    """map 系统边界：地图目录、进入/寻路、对象交互与动态地图。"""

    system_name = 'map'

    def __init__(
        self,
        pathfind_target_checker: Optional[Any] = None,
        *,
        settings=None,
        save=None,
        battle=None,
        task_event_recorder=None,
        npc_dialogue_frames_hook=None,
        npc_dialogue_option_hook=None,
        online_roles_hook=None,
        push_to_role=None,
        team_movement_frame_hook=None,
    ) -> None:
        self._pathfind_target_checker = pathfind_target_checker
        self.settings = settings
        self.save = save
        self.battle = battle
        self.task_event_recorder = task_event_recorder
        self._npc_dialogue_frames_hooks = self._as_hook_list(npc_dialogue_frames_hook)
        self._npc_dialogue_option_hooks = self._as_hook_list(npc_dialogue_option_hook)
        # 同图可见性：在线角色快照（role_id -> 在线连接登记的存档 dict）与
        # 跨连接推送（server._push_to_role）。为 None 时退化为单机独立世界。
        self._online_roles_hook = online_roles_hook
        self._push_to_role = push_to_role
        self._team_movement_frame_hook = team_movement_frame_hook
        # role_id -> 该客户端当前视野内持有的其他玩家 actor id 集合
        # （镜像 APK 的 b/m.U 容器）。role_id 不在表中 = 尚未进图或已离场，
        # 不向其发送可见性帧。
        self._visible_roles: dict[int, set[int]] = {}

    @staticmethod
    def _as_hook_list(hook) -> list:
        """对话 hook 支持单个回调或按序尝试的回调列表（寄售/帮派等按 service 认领）。"""
        if hook is None:
            return []
        if isinstance(hook, (list, tuple)):
            return [entry for entry in hook if entry is not None]
        return [hook]

    # ------------------------------------------------------------------
    # 路由入口
    # ------------------------------------------------------------------
    def can_handle(self, _context: SystemContext, message_id: int, _fields: list[object]) -> bool:
        return message_id in (1005, 1010, 1123, 1145, 1533, 2029, 2031, 2032)

    def handle(self, context: SystemContext, message_id: int, fields: list[object]) -> RouteResult:
        values = [field.value for field in fields]
        if message_id == 1123:
            return self._handle_world_init(context)
        if message_id == 1005:
            return self._handle_movement(context, values)
        if message_id == 1010:
            return self._handle_map_request(context, values)
        if message_id == 1145:
            return self._handle_pathfind(context, fields)
        if message_id == 1533:
            LOG.info('npc dialogue option selected user=%r values=%r', context.username, values)
            return RouteResult.handled()
        if message_id in (2029, 2031):
            return self._handle_object_message(context, message_id, fields, values)
        if message_id == 2032:
            return self._handle_dialogue_option(context, values)
        return RouteResult.not_handled()

    # ------------------------------------------------------------------
    # 1123 世界初始化
    # ------------------------------------------------------------------
    def _handle_world_init(self, context: SystemContext) -> RouteResult:
        session = context.session
        if session.get('map.world_sent'):
            return RouteResult.not_handled(reason='world_already_sent')
        session['map.world_sent'] = True
        role = context.active_role
        current = role if role is not None else self._default_role()
        LOG.info(
            'client initialized; sending world %d %s',
            current['map_id'], current['map_name'],
        )
        return RouteResult.handled(tuple(notice_and_world(self.settings, current)))

    def _default_role(self):
        from systems.role.service import default_role
        return default_role(self.settings)

    # ------------------------------------------------------------------
    # 1005 移动
    # ------------------------------------------------------------------
    def _handle_movement(self, context: SystemContext, values: list[object]) -> RouteResult:
        session = context.session
        role = context.active_role
        frames: list[bytes] = []

        gathering = session.get('gathering')
        movement_interrupt = gathering.cancel() if gathering is not None else None
        if movement_interrupt is not None:
            LOG.info(
                'GATHER_CANCEL user=%r role_id=%d reason=movement',
                context.username,
                int(role.get('id', 0)) if role is not None else 0,
            )
            frames.append(movement_interrupt)

        battle_state = battle_state_for(session)
        movement_x, movement_y = map_movement_final_tile(values)
        guard_had_no_origin = bool(
            battle_state.escape_guard
            and battle_state.escape_guard.get('origin') is None
        )
        guard_cleared = update_escape_guard_for_movement(battle_state, movement_x, movement_y)
        if guard_cleared:
            LOG.info(
                'BATTLE_ESCAPE_GUARD_CLEARED user=%r new_tile=%s reason=real_1005_movement',
                context.username,
                battle_state.player_tile,
            )
        elif guard_had_no_origin and battle_state.escape_guard:
            LOG.info(
                'BATTLE_ESCAPE_GUARD_ORIGIN_ESTABLISHED user=%r tile=%s',
                context.username,
                battle_state.player_tile,
            )

        position_dirty = bool(session.get('map.position_dirty'))
        checkpoint_at = float(session.get('map.position_checkpoint_at') or 0.0)
        if role is not None:
            previous_tile = self._role_tile(role)
            if update_role_position(role, movement_x, movement_y):
                position_dirty = True
                now = time.monotonic()
                if now - checkpoint_at >= POSITION_CHECKPOINT_SECONDS:
                    if self.save is not None:
                        self.save()
                    position_dirty = False
                    checkpoint_at = now
                    LOG.info(
                        'ROLE_POSITION_CHECKPOINT user=%r role_id=%d map=%d tile=%d,%d',
                        context.username,
                        int(role.get('id', 0)),
                        int(role.get('map_id', self.settings.default_map_id)),
                        movement_x,
                        movement_y,
                    )
                session['map.position_dirty'] = position_dirty
                session['map.position_checkpoint_at'] = checkpoint_at
                self._update_player_visibility(
                    role, previous_tile[0], previous_tile[1], movement_x, movement_y,
                )

        # 巡逻 Boss 接触战：靠近 Boss 触点时把 1005 改写为对象交互。
        contact_frames = self._maybe_roaming_boss_contact(context, role, movement_x, movement_y)
        if contact_frames is not None:
            return RouteResult.handled(tuple(contact_frames))

        current_settings = settings_for_role(self.settings, role)
        streamed = session.get('map.streamed_npcs')
        if not isinstance(streamed, set):
            streamed = set()
            session['map.streamed_npcs'] = streamed
        nearby_npcs = map_npcs_near(current_settings, movement_x, movement_y)
        nearby_ids = {npc.id for npc in nearby_npcs}
        entered_npcs = [npc for npc in nearby_npcs if npc.id not in streamed]
        streamed.intersection_update(nearby_ids)
        if entered_npcs:
            LOG.info(
                'NPC_REGION_STREAM user=%r map=%d tile=%d,%d ids=%r',
                context.username,
                current_settings.id,
                movement_x,
                movement_y,
                [npc.id for npc in entered_npcs],
            )
            frames.extend(map_npc_frame(current_settings, npc) for npc in entered_npcs)
            streamed.update(npc.id for npc in entered_npcs)
        return RouteResult.handled(tuple(frames))

    def _maybe_roaming_boss_contact(self, context: SystemContext, role, x: int, y: int):
        """Rewrite in-range movement into a Boss interaction (1005 -> 2031)."""
        if role is None or int(role.get('map_id', -1)) != ROAMING_BOSS_MAP_ID:
            return None
        session = context.session
        entered_at = session.get('map.boss_entered_at')
        spawn_tile = session.get('map.boss_spawn_tile')
        if entered_at is None or spawn_tile is None:
            return None
        current = time.monotonic()
        if current - float(entered_at) < ROAMING_BOSS_MOVE_DELAY_SECONDS:
            boss_tile = (int(spawn_tile[0]), int(spawn_tile[1]))
        else:
            boss_tile = (ROAMING_BOSS_TARGET_X, ROAMING_BOSS_TARGET_Y)
        if max(abs(x - boss_tile[0]), abs(y - boss_tile[1])) > CONTACT_RADIUS_TILES:
            return None
        if self.save is not None:
            self.save()
        LOG.info(
            'MAP_BOSS_CONTACT_BATTLE player=(%d,%d) boss=(%d,%d) radius=%d protocol=1005->2031',
            x, y, boss_tile[0], boss_tile[1], CONTACT_RADIUS_TILES,
        )
        result = self._handle_object_interaction(
            context,
            role,
            object_id=ROAMING_BOSS_ID,
            object_x=boss_tile[0],
            object_y=boss_tile[1],
            action=6,
            source='1005',
        )
        return list(result.frames) if result.handled else []

    # ------------------------------------------------------------------
    # 1010 地图请求
    # ------------------------------------------------------------------
    def _handle_map_request(self, context: SystemContext, values: list[object]) -> RouteResult:
        role = context.active_role
        if not values:
            return RouteResult.not_handled()
        action = int(values[0])
        if action == 12:
            current_settings = settings_for_role(self.settings, role)
            LOG.info('client requested map data map=%d', current_settings.id)
            role_id = int(role['id']) if role is not None else self.settings.role_id
            return RouteResult.handled(tuple(map_data_frames(current_settings, role_id)))
        if action == 13:
            return self._handle_map_enter(context)
        if action == 7 and len(values) > 1:
            # Compatibility with an older map-object path seen in
            # some client builds. The active APK uses 2031 below.
            return self._handle_object_message(
                context,
                2031,
                None,
                [values[1]],
                legacy_object_id=int(values[1]),
            )
        if action == 15:
            # Sent by the APK after it receives action=105
            # (actionEnterMapOK).  This is a client acknowledgement,
            # not a request for another map frame.
            LOG.info('map entry acknowledged by client map=%d', settings_for_role(self.settings, role).id)
            return RouteResult.handled()
        LOG.info('ignored client map action=%d', action)
        return RouteResult.handled()

    def _handle_map_enter(self, context: SystemContext) -> RouteResult:
        session = context.session
        role = context.active_role
        frames: list[bytes] = []

        battle_state = battle_state_for(session)
        # Map entry is the respawn boundary for the local
        # encounter; never carry a completed battle into the
        # newly loaded scene.
        battle_state.reset_encounter()
        dialogue_for(session).clear()
        gathering = session.get('gathering')
        gather_transition = gathering.cancel() if gathering is not None else None
        if gather_transition is not None:
            LOG.info(
                'GATHER_CANCEL user=%r role_id=%d reason=map_transition',
                context.username,
                int(role.get('id', 0)) if role is not None else 0,
            )

        current_settings = settings_for_role(self.settings, role)
        monster = current_settings.monster
        LOG.info(
            'client requested map reference; map=%d entering at %d,%d; monster=%s',
            current_settings.id,
            current_settings.spawn_x,
            current_settings.spawn_y,
            (
                f'id={monster.id} model={monster.model} at {monster.x},{monster.y}'
                if monster is not None
                else 'disabled'
            ),
        )
        role_id = int(role['id']) if role is not None else self.settings.role_id
        enter_frames = list(dynamic_map_enter_frames(current_settings, role_id))
        if gather_transition is not None:
            enter_frames.insert(0, gather_transition)
        enter_frames.extend(
            gather_spawn_frame(target)
            for target in self.settings.life_registry.gather_targets_for(
                current_settings.id
            )
        )
        if role is not None and self.task_event_recorder is not None:
            enter_frames.extend(self.task_event_recorder(
                role,
                'map_entered',
                target_id=current_settings.id,
                now=time.time(),
            ))
        frames.extend(enter_frames)

        # 巡逻 Boss 进图跟踪：记录出生触点并安排一次原生 1005 移动探针。
        if is_roaming_boss_definition(current_settings) and monster is not None:
            session['map.boss_entered_at'] = time.monotonic()
            session['map.boss_spawn_tile'] = (int(monster.x), int(monster.y))
            LOG.info(
                'MAP_BOSS_CONTACT_TRACK_START actor=%d spawn=%s target=(%d,%d) delay=%.1f',
                monster.id, (int(monster.x), int(monster.y)),
                ROAMING_BOSS_TARGET_X, ROAMING_BOSS_TARGET_Y,
                ROAMING_BOSS_MOVE_DELAY_SECONDS,
            )
            asyncio.create_task(self._send_roaming_boss_probe(context, int(monster.x), int(monster.y)))
        else:
            session['map.boss_entered_at'] = None
            session['map.boss_spawn_tile'] = None

        streamed = session.get('map.streamed_npcs')
        if not isinstance(streamed, set):
            streamed = set()
            session['map.streamed_npcs'] = streamed
        streamed.clear()
        streamed.update(npc.id for npc in current_settings.npcs)
        self._announce_player_entry(session, role)
        return RouteResult.handled(tuple(frames))

    async def _send_roaming_boss_probe(self, context: SystemContext, source_x: int, source_y: int) -> None:
        """After map entry, issue one movement target to prove native q walking."""
        try:
            await asyncio.sleep(ROAMING_BOSS_MOVE_DELAY_SECONDS)
            frame = roaming_boss_move_frame(
                ROAMING_BOSS_ID,
                source_x,
                source_y,
                ROAMING_BOSS_TARGET_X,
                ROAMING_BOSS_TARGET_Y,
            )
            push = context.session.get('push_frames')
            if push is not None:
                await push(frame)
            LOG.info(
                'MAP_BOSS_NATIVE_MOVE from=(%d,%d) to=(%d,%d) protocol=1005',
                source_x,
                source_y,
                ROAMING_BOSS_TARGET_X,
                ROAMING_BOSS_TARGET_Y,
            )
        except asyncio.CancelledError:
            raise
        except (ConnectionError, OSError):
            LOG.info('MAP_BOSS_NATIVE_MOVE skipped connection_closed=1')

    # ------------------------------------------------------------------
    # 1145 寻路
    # ------------------------------------------------------------------
    def _handle_pathfind(self, context: SystemContext, fields: list[object]) -> RouteResult:
        role = context.active_role
        current_map_id = (
            int(role.get('map_id', self.settings.default_map_id))
            if role is not None
            else self.settings.default_map_id
        )
        result = self.handle_pathfind(fields, current_map_id=current_map_id)
        if result.frames:
            return RouteResult.handled(result.frames)
        return RouteResult.handled(reason=result.reason)

    def handle_pathfind(self, fields, *, current_map_id: int) -> MapHandleResult:
        if not is_map_pathfind_request(fields):
            return MapHandleResult(False)
        map_id, x, y = (int(fields[index].value) for index in (1, 2, 3))
        if map_id != int(current_map_id) or not self.is_known_pathfind_target(map_id, x, y):
            return MapHandleResult(True, reason='unknown_target')
        return MapHandleResult(True, (map_pathfind_frame(map_id, x, y),))

    def is_known_pathfind_target(self, map_id: int, x: int, y: int) -> bool:
        if self._pathfind_target_checker is None:
            return False
        return bool(self._pathfind_target_checker(map_id, x, y))

    # ------------------------------------------------------------------
    # 2029/2031 对象交互
    # ------------------------------------------------------------------
    def _handle_object_message(
        self,
        context: SystemContext,
        message_id: int,
        fields,
        values: list[object],
        legacy_object_id: int | None = None,
    ) -> RouteResult:
        role = context.active_role
        if legacy_object_id is not None:
            object_id = legacy_object_id
            object_x = object_y = None
            object_action = None
        elif message_id == 2029:
            # 巡逻 Boss 原生战斗入口：2029/1[BYTE 1, INT boss_id] 等价 2031。
            if len(fields) < 2 or int(fields[0].value) != 1:
                LOG.info('ignored 2029 message values=%r', values)
                return RouteResult.handled()
            object_id = int(fields[1].value)
            object_x = object_y = None
            object_action = 6
            LOG.info(
                'MAP_BOSS_NATIVE_FIGHT_BRIDGE protocol=2029 action=1 actor=%d -> protocol=2031',
                object_id,
            )
        else:
            # main/k encodes [object_id, 0, x, y, action, 0]. Native
            # 2030 NPCs use action 0; generic 1126 actors use action 6.
            gathering = context.session.get('gathering')
            gather_interrupt = gathering.cancel() if gathering is not None else None
            if gather_interrupt is not None:
                LOG.info(
                    'GATHER_CANCEL user=%r role_id=%d reason=map_interaction',
                    context.username,
                    int(role.get('id', 0)) if role is not None else 0,
                )
            object_id, object_x, object_y, object_action = map_object_interaction_values(values)
        result = self._handle_object_interaction(
            context,
            role,
            object_id=object_id,
            object_x=object_x,
            object_y=object_y,
            action=object_action,
            source=str(message_id),
        )
        if not result.handled:
            return RouteResult.not_handled(reason=result.reason)
        if result.frames:
            return RouteResult.handled(result.frames)
        return RouteResult.handled(reason=result.reason)

    def _handle_object_interaction(
        self,
        context: SystemContext,
        role,
        *,
        object_id: int,
        object_x: int | None,
        object_y: int | None,
        action: int | None,
        source: str,
    ) -> MapHandleResult:
        """Handle a map actor request without guessing battle data.

        Native 2030 NPCs use action 0; generic actors use action 6, and both
        payloads include the actor id and tile. Portal activation is a complete
        transition. A monster starts the local single-target battle probe using
        the confirmed 1040/action=1 shape.
        """
        username = context.username
        session = context.session
        interaction = self.resolve_interaction(role, object_id, dialogue_for(session))
        current_settings = interaction.current_map
        LOG.info(
            'map object interaction source=%s user=%r map=%d object_id=%d tile=%s,%s action=%s',
            source,
            username,
            current_settings.id,
            object_id,
            object_x,
            object_y,
            action,
        )

        target_settings = interaction.target_map
        if target_settings is not None:
            LOG.info(
                'portal activated user=%r role_id=%d object_id=%d map %d -> %d',
                username,
                int(role['id']),
                object_id,
                current_settings.id,
                target_settings.id,
            )
            # 1110 is the same world/map descriptor used by the original map
            # transition. The client then requests 1010/12 and 1010/13.
            return MapHandleResult(True, (notice_and_world(self.settings, role)[1],))

        npc = interaction.entity if interaction.kind == 'npc' else None
        if npc is not None:
            LOG.info(
                'npc interaction user=%r npc_id=%d name=%r source=%s; opening native map dialogue',
                username,
                object_id,
                npc.name,
                source,
            )
            task_frames: tuple[bytes, ...] = ()
            if role is not None and self.task_event_recorder is not None:
                task_frames = tuple(self.task_event_recorder(
                    role,
                    'npc_talked',
                    target_id=npc.id,
                    now=time.time(),
                ))
            dialogue_frames = None
            for hook in self._npc_dialogue_frames_hooks:
                dialogue_frames = hook(npc, role, self.settings)
                if dialogue_frames is not None:
                    break
            if dialogue_frames is None:
                dialogue_frames = map_npc_dialogue_frames(npc, role, self.settings)
            return MapHandleResult(True, tuple(dialogue_frames) + task_frames)

        monster = interaction.entity if interaction.kind == 'monster' else None
        if monster is not None and self.battle is not None:
            encounter = self.battle.handle_monster_encounter(
                username=username,
                role=role,
                battle_state=battle_state_for(session),
                map_settings=current_settings,
                object_id=object_id,
                object_x=object_x,
                object_y=object_y,
                source=source,
            )
            if encounter.log:
                LOG.info('%s', encounter.log)
            return MapHandleResult(True, encounter.frames)

        LOG.info('ignored map object action id=%d map=%d', object_id, current_settings.id)
        return MapHandleResult(True)

    def resolve_interaction(self, role, object_id: int, dialogue: LocalNpcDialogueState) -> MapInteractionResult:
        if self.settings is None:
            raise RuntimeError('map settings are not configured')
        current = settings_for_role(self.settings, role)
        target = apply_portal_transition(self.settings, role, object_id) if role is not None else None
        if target is not None:
            dialogue.clear()
            if self.save is not None:
                self.save()
            return MapInteractionResult('portal', current, target_map=target)
        npc = map_npc_for_object_id(current, object_id)
        if npc is not None:
            dialogue.select(current.id, npc.id)
            return MapInteractionResult('npc', current, entity=npc)
        monster = map_monster_for_object_id(current, object_id)
        if monster is not None:
            return MapInteractionResult('monster', current, entity=monster)
        return MapInteractionResult('unknown', current)

    # ------------------------------------------------------------------
    # 2032 原生对话选项
    # ------------------------------------------------------------------
    def _handle_dialogue_option(self, context: SystemContext, values: list[object]) -> RouteResult:
        role = context.active_role
        # Screen 6 closes the compact native NPC overlay locally,
        # then reports [byte(option_id), byte(101), string(input)]
        # and enables the global wait overlay. S->C 1010 clears
        # that overlay before dispatching action 7. A validated
        # sect mentor selection appends action 69 to open the
        # native learning-mode screen; all other paths are ACK-only.
        if not values:
            return RouteResult.not_handled()
        option_id = int(values[0])
        # 客户端 screen 6 提交格式为 [byte option_id, byte 101, string 输入内容]；
        # kind 3 记录打开输入框后提交会携带输入文本。
        input_text = values[2] if len(values) > 2 and isinstance(values[2], str) else ''
        dialogue = dialogue_for(context.session)
        response_frames = None
        for hook in self._npc_dialogue_option_hooks:
            response_frames = hook(self.settings, role, dialogue, option_id, input_text)
            if response_frames is not None:
                break
        if response_frames is None:
            response_frames = npc_dialogue_option_frames(self.settings, role, dialogue, option_id, input_text)
        LOG.info(
            'native npc dialogue option selected user=%r option=%d values=%r mentor_mode=%s',
            context.username,
            option_id,
            values,
            len(response_frames) > 1,
        )
        return RouteResult.handled(tuple(response_frames))

    # ------------------------------------------------------------------
    # 同图在线玩家可见性（1014 出现 / 1005 走路 / 1010+18 移除，20 格流式）
    # ------------------------------------------------------------------
    def _same_map_online_roles(self, role) -> list[dict[str, object]]:
        """Other online roles whose stored map equals this role's map."""
        if self._online_roles_hook is None or role is None:
            return []
        try:
            own_id = int(role.get('id', 0) or 0)
            map_id = int(role.get('map_id', self.settings.default_map_id))
        except (TypeError, ValueError):
            return []
        others: list[dict[str, object]] = []
        for other in self._online_roles_hook():
            try:
                other_id = int(other.get('id', 0) or 0)
                other_map = int(other.get('map_id', -1))
            except (TypeError, ValueError, AttributeError):
                continue
            if other_id and other_id != own_id and other_map == map_id:
                others.append(other)
        return others

    def _in_stream_range(self, ax: int, ay: int, bx: int, by: int) -> bool:
        return (
            abs(ax - bx) <= PLAYER_STREAM_RADIUS
            and abs(ay - by) <= PLAYER_STREAM_RADIUS
        )

    def _role_tile(self, role) -> tuple[int, int]:
        try:
            return (
                int(role.get('map_x', self.settings.spawn_x)),
                int(role.get('map_y', self.settings.spawn_y)),
            )
        except (TypeError, ValueError):
            return self.settings.spawn_x, self.settings.spawn_y

    def can_players_see_each_other(self, left_role_id: int, right_role_id: int) -> bool:
        """Only issue team follow links after both native player actors exist."""
        left_view = self._visible_roles.get(int(left_role_id))
        right_view = self._visible_roles.get(int(right_role_id))
        return bool(
            left_view is not None and right_view is not None
            and player_actor_object_id(right_role_id) in left_view
            and player_actor_object_id(left_role_id) in right_view
        )

    def _update_player_visibility(self, role, from_x: int, from_y: int, to_x: int, to_y: int) -> None:
        """Mirror the APK's 20-tile b/v streaming for the moving role.

        对每对（移动者, 同图在线者）双向维护三态：进入 20 格发 1014 出现帧
        （携带完整属性表，客户端建 b/v 并落格）；格内移动发 1005 走路帧；
        离开 20 格发 1010/action=18 移除。只服务已进图（存在于
        _visible_roles）的接收端，集合状态即 APK U 容器的服务端镜像。
        """
        if self._push_to_role is None or self._online_roles_hook is None:
            return
        try:
            mover_role_id = int(role.get('id', 0) or 0)
        except (TypeError, ValueError):
            return
        mover_actor = player_actor_object_id(mover_role_id)
        for other in self._same_map_online_roles(role):
            try:
                other_role_id = int(other.get('id', 0) or 0)
            except (TypeError, ValueError):
                continue
            mover_view = self._visible_roles.get(mover_role_id)
            other_view = self._visible_roles.get(other_role_id)
            if mover_view is None or other_view is None:
                continue  # 任一端尚未进图
            other_actor = player_actor_object_id(other_role_id)
            ox, oy = self._role_tile(other)
            near = self._in_stream_range(to_x, to_y, ox, oy)
            # 对方视角中的移动者
            if near:
                if mover_actor in other_view:
                    follow_frame = (
                        self._team_movement_frame_hook(
                            mover_role_id, other_role_id, to_x, to_y,
                        ) if self._team_movement_frame_hook is not None else None
                    )
                    self._push_to_role(other_role_id, (
                        follow_frame or map_actor_move_frame(
                            mover_actor, from_x, from_y, to_x, to_y,
                        ),
                    ))
                else:
                    self._push_to_role(other_role_id, (
                        player_appear_frame(self.settings, role, mover_actor, to_x, to_y),
                    ))
                    other_view.add(mover_actor)
            elif mover_actor in other_view:
                self._push_to_role(other_role_id, (map_object_remove_frame(mover_actor),))
                other_view.discard(mover_actor)
            # 移动者视角中的对方（对方静止时同样随移动者跨界增减）
            if near:
                if other_actor not in mover_view:
                    self._push_to_role(mover_role_id, (
                        player_appear_frame(self.settings, other, other_actor, ox, oy),
                    ))
                    mover_view.add(other_actor)
            elif other_actor in mover_view:
                self._push_to_role(mover_role_id, (map_object_remove_frame(other_actor),))
                mover_view.discard(other_actor)

    def _announce_player_entry(self, session: dict[str, object], role) -> None:
        """Reconcile this role's visibility after its client entered a map.

        Portal transitions first broadcast 1010/action=18 to clients on the
        previously announced map, then the fresh 20-tile neighbourhood is
        established in both directions. ``map.visible_map_id`` tracks the
        announced map so ``depart_map`` knows where to despawn the actor.
        """
        if role is None or self._push_to_role is None or self._online_roles_hook is None:
            return
        try:
            own_role_id = int(role.get('id', 0) or 0)
            map_id = int(role.get('map_id', self.settings.default_map_id))
        except (TypeError, ValueError):
            return
        if not own_role_id:
            return
        own_actor = player_actor_object_id(own_role_id)
        announced = session.get('map.visible_map_id')
        if announced is not None and int(announced) != map_id:
            remove_frame = map_object_remove_frame(own_actor)
            for other in self._online_roles_hook():
                try:
                    other_id = int(other.get('id', 0) or 0)
                    other_map = int(other.get('map_id', -1))
                except (TypeError, ValueError, AttributeError):
                    continue
                if other_id and other_id != own_role_id and other_map == int(announced):
                    self._push_to_role(other_id, (remove_frame,))
                    self._visible_roles.get(other_id, set()).discard(own_actor)
        session['map.visible_map_id'] = map_id
        # 进图后自身视野清空，再按 20 格邻近双向建立可见性。
        own_view: set[int] = set()
        self._visible_roles[own_role_id] = own_view
        x, y = self._role_tile(role)
        for other in self._same_map_online_roles(role):
            try:
                other_role_id = int(other.get('id', 0) or 0)
            except (TypeError, ValueError):
                continue
            other_view = self._visible_roles.get(other_role_id)
            if other_view is None:
                continue  # 对方尚未进图
            other_actor = player_actor_object_id(other_role_id)
            ox, oy = self._role_tile(other)
            if not self._in_stream_range(x, y, ox, oy):
                continue
            self._push_to_role(other_role_id, (
                player_appear_frame(self.settings, role, own_actor, x, y),
            ))
            other_view.add(own_actor)
            self._push_to_role(own_role_id, (
                player_appear_frame(self.settings, other, other_actor, ox, oy),
            ))
            own_view.add(other_actor)
        LOG.info(
            'PLAYER_MAP_ENTER_VISIBILITY role_id=%d map=%d visible=%d',
            own_role_id,
            map_id,
            len(own_view),
        )

    def broadcast_player_appearance(self, role) -> None:
        """外观/装备变更后，向视野内持有该角色对象的其他客户端重发 1017。

        APK ``main/e.O`` 用 ``m.o(field1)`` 定位角色：命中自身 role_id 走
        自身访问器，否则按 id 查 U 容器里的 b/v。因此把帧的 target 换成
        1_000_000+role_id，即可对持有该对象的其他客户端做带图层重载的
        定向属性刷新（O 的 sparse-switch 逐属性重载装备/炫光图层）。
        """
        if self._push_to_role is None or self._online_roles_hook is None:
            return
        try:
            role_id = int(role.get('id', 0) or 0)
        except (TypeError, ValueError):
            return
        view = self._visible_roles.get(role_id)
        if not view:
            return
        actor_id = player_actor_object_id(role_id)
        # 外观表之外补属性 22（坐骑骑乘码）：1017 走 O 的 0x16 分支（v.I(I)），
        # 其他客户端据此重载 b/v 的精灵族（步姿/坐骑外观）。
        properties = character_appearance(role, self.settings.item_registry)
        properties[22] = mount_ride_code_for_role(role, self.settings.item_registry)
        frame = character_appearance_frame(actor_id, properties)
        receivers = [
            receiver_id
            for receiver_id, actors in self._visible_roles.items()
            if receiver_id != role_id and actor_id in actors
        ]
        for receiver_id in receivers:
            self._push_to_role(receiver_id, (frame,))
        if receivers:
            LOG.info(
                'PLAYER_APPEARANCE_BROADCAST role_id=%d actor=%d receivers=%d',
                role_id,
                actor_id,
                len(receivers),
            )

    def depart_map(self, session: dict[str, object], *, role=None) -> None:
        """Broadcast this role's actor removal on its last announced map.

        Called from the network layer on disconnect and role switch; pops
        ``map.visible_map_id`` so a later re-entry re-announces cleanly.
        """
        announced = session.pop('map.visible_map_id', None)
        if role is None:
            role = session.get('active_role')
        if announced is None or role is None:
            return
        if self._push_to_role is None or self._online_roles_hook is None:
            return
        try:
            own_id = int(role.get('id', 0) or 0)
        except (TypeError, ValueError):
            return
        if not own_id:
            return
        own_actor = player_actor_object_id(own_id)
        remove_frame = map_object_remove_frame(own_actor)
        for other in self._online_roles_hook():
            try:
                other_id = int(other.get('id', 0) or 0)
                other_map = int(other.get('map_id', -1))
            except (TypeError, ValueError, AttributeError):
                continue
            if other_id and other_id != own_id and other_map == int(announced):
                self._push_to_role(other_id, (remove_frame,))
        # 清理离场者自身的视野集合，并从所有在线客户端视野集中移除该 actor。
        self._visible_roles.pop(own_id, None)
        for view in self._visible_roles.values():
            view.discard(own_actor)
        LOG.info(
            'PLAYER_MAP_DEPART role_id=%d announced_map=%s', own_id, announced,
        )

    # ------------------------------------------------------------------
    # 位置落盘（登出/断线时由网络层调用）
    # ------------------------------------------------------------------
    def flush_position(self, session: dict[str, object]) -> bool:
        """Persist a dirty position checkpoint; returns whether a save happened."""
        if not session.get('map.position_dirty'):
            return False
        if self.save is not None:
            self.save()
        session['map.position_dirty'] = False
        session['map.position_checkpoint_at'] = time.monotonic()
        return True


def register_map_routes(router: SystemRouter, system: MapSystem) -> None:
    router.register(system.system_name, system.can_handle, system.handle)
