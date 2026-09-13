from __future__ import annotations

import logging
from dataclasses import dataclass

from app.context import SystemContext
from app.notify import top_message_frame
from app.router import RouteResult, SystemRouter
from protocol import byte, encode_frame, integer, short, string
from systems.battle.registry import (
    PNG_QUERY_MAIN_CACHE, PNG_QUERY_ROLE_CACHE, battle_resource_resolution,
)
from systems.battle.service import (
    BATTLE_EXP_REWARD, PvpDuel, apply_battle_rewards, battle_command_target_id,
    battle_state_for, is_player_escape_command, should_suppress_escape_retrigger,
)
from systems.battle.protocol import (
    battle_action_show_frame, battle_actor_frames, battle_end_frame,
    battle_escape_frame, battle_escape_request_frames, battle_image_frames,
    battle_image_resolve_debug, battle_reset_frame, battle_resource_frames,
    battle_reward_notice, battle_reward_popup, battle_round_action_frames,
    battle_start_frame, duel_action_frame, duel_defend_frame,
    duel_hp_refresh_frames, duel_start_frames,
    format_battle_resource_query_log,
)
from systems.inventory.protocol import item_frame
from systems.map.protocol import map_object_interaction_ack_frame, map_object_remove_frame
from systems.role.protocol import battle_progress_frame, level_up_effect_frame


LOG = logging.getLogger('piaomiao-local')


@dataclass(frozen=True)
class EncounterResult:
    """Monster contact outcome: frames to send plus one log line."""

    frames: tuple[bytes, ...] = ()
    log: str = ''


class BattleSystem:
    """battle 系统边界：1040/1041 战斗流程与 1502 资源下发。"""

    system_name = 'battle'

    def __init__(
        self,
        settings=None,
        save=None,
        task_event_recorder=None,
        character_update_bus=None,
        push_to_role=None,
        online_role_ids=None,
        find_role=None,
    ) -> None:
        self.settings = settings
        self.save = save
        self.task_event_recorder = task_event_recorder
        self.character_update_bus = character_update_bus
        self.push_to_role = push_to_role or (lambda role_id, frames: None)
        self.online_role_ids = online_role_ids or (lambda: set())
        self.find_role = find_role or (lambda role_id: None)
        # role_id -> PvpDuel（两名参与者各持同一对象引用）
        self.duels: dict[int, PvpDuel] = {}

    def can_handle(self, _context: SystemContext, message_id: int, _fields: list[object]) -> bool:
        return message_id in (1040, 1041, 1502)

    def handle(self, context: SystemContext, message_id: int, fields: list[object]) -> RouteResult:
        values = [field.value for field in fields]
        if message_id in (1040, 1041) and context.active_role is not None:
            duel = self.duels.get(int(context.active_role.get('id', 0)))
            if duel is not None:
                return self._handle_duel_message(context, duel, message_id, values)
        if message_id == 1502:
            return self._handle_resource_query(context, values)
        if message_id == 1040:
            return self._handle_round_ack(context, values)
        if message_id == 1041:
            return self._handle_command(context, values)
        return RouteResult.not_handled()

    # ------------------------------------------------------------------
    # 双人即时对决（切磋/PK）：start_duel 由 social 系统在双方确认后调用
    # ------------------------------------------------------------------
    def start_duel(
        self,
        challenger: dict[str, object],
        defender: dict[str, object],
        kind: str = '切磋',
    ) -> tuple[bytes, ...] | None:
        """Create a shared duel and return the defender's entry frames.

        挑战者的进入帧由本方法直接经 ``push_to_role`` 推送；应答方的帧
        作为返回值并入其请求应答。任一方已在对决中时返回 None。
        """
        challenger_id = int(challenger['id'])
        defender_id = int(defender['id'])
        if challenger_id in self.duels or defender_id in self.duels:
            return None
        stats = {
            challenger_id: self._combat_stats(challenger),
            defender_id: self._combat_stats(defender),
        }
        duel = PvpDuel(
            kind=kind,
            a_id=challenger_id,
            b_id=defender_id,
            stats=stats,
            hp={
                challenger_id: stats[challenger_id].max_hp,
                defender_id: stats[defender_id].max_hp,
            },
        )
        duel.seq += 1
        self.duels[challenger_id] = duel
        self.duels[defender_id] = duel
        challenger_frames = duel_start_frames(challenger, defender, duel, self.settings)
        defender_frames = duel_start_frames(defender, challenger, duel, self.settings)
        self.push_to_role(challenger_id, challenger_frames)
        LOG.info(
            'DUEL_START kind=%s challenger=%d defender=%d trace=%s',
            kind, challenger_id, defender_id, duel.trace_id,
        )
        return defender_frames

    def abandon_duels(self, role_id: int) -> tuple[int, tuple[bytes, ...]] | None:
        """End any duel involving role_id (disconnect/cleanup); notify the peer."""
        duel = self.duels.pop(int(role_id), None)
        if duel is None or duel.finished:
            return None
        duel.finished = True
        peer_id = duel.opponent_of(int(role_id))
        self.duels.pop(peer_id, None)
        return peer_id, (battle_end_frame(), top_message_frame('对方离开了战斗'))

    def _finish_duel(self, duel: PvpDuel, *, winner_id: int, escaper_id: int | None = None) -> tuple[bytes, ...]:
        """Close the duel for the requesting side; the peer's frames are pushed.

        请求方（发起本条 1041/逃逸或致命一击的连接）的结束帧作为返回值，
        对方的帧经 push_to_role 定向发送。
        """
        duel.finished = True
        a_id, b_id = duel.participants()
        self.duels.pop(a_id, None)
        self.duels.pop(b_id, None)
        requester_id = escaper_id if escaper_id is not None else winner_id
        peer_id = duel.opponent_of(requester_id)
        requester_frames: list[bytes] = [battle_end_frame()]
        peer_frames: list[bytes] = [battle_end_frame()]
        if escaper_id is not None:
            requester_frames.insert(0, battle_escape_frame(int(escaper_id)))
            peer_frames.append(top_message_frame('对方逃离了战斗'))
        else:
            requester_frames.append(top_message_frame(f'{duel.kind}结束：你获胜了'))
            peer_frames.append(top_message_frame(f'{duel.kind}结束：你落败了'))
        self.push_to_role(int(peer_id), tuple(peer_frames))
        LOG.info(
            'DUEL_END kind=%s winner=%d loser=%d escaper=%s trace=%s',
            duel.kind, winner_id, duel.opponent_of(winner_id), escaper_id, duel.trace_id,
        )
        return tuple(requester_frames)

    def _handle_duel_message(
        self,
        context: SystemContext,
        duel: PvpDuel,
        message_id: int,
        values: list[object],
    ) -> RouteResult:
        role_id = int(context.active_role.get('id', 0))
        if duel.finished:
            self.duels.pop(role_id, None)
            return RouteResult.handled((battle_end_frame(),))
        if message_id == 1040:
            # 1040/2 播放完毕确认：对决回合由指令驱动，确认本身无需推进。
            return RouteResult.handled()
        command_code = int(values[0]) if values else 0
        if is_player_escape_command(command_code):
            LOG.info('DUEL_ESCAPE trace=%s escaper=%d', duel.trace_id, role_id)
            return RouteResult.handled(
                self._finish_duel(duel, winner_id=duel.opponent_of(role_id), escaper_id=role_id),
            )
        if command_code not in (1, 2):
            return RouteResult.handled()
        duel.round += 1
        action_round = duel.round
        attacker_id = role_id
        defender_id = duel.opponent_of(role_id)
        attacker = self.find_role(attacker_id)
        defender = self.find_role(defender_id)
        if attacker is None or defender is None:
            duel.finished = True
            self.duels.pop(duel.a_id, None)
            self.duels.pop(duel.b_id, None)
            return RouteResult.handled((battle_end_frame(),))
        frames: list[bytes] = []
        if command_code == 1:
            damage = duel.attack_damage(attacker_id, defender_id)
            duel.apply_damage(defender_id, damage)
            frames.append(duel_action_frame(
                duel, action_round,
                actor_id=attacker_id, target_id=defender_id,
                damage=damage, label='普通攻击',
            ))
        else:
            frames.append(duel_defend_frame(duel, action_round, actor_id=attacker_id))
        if duel.hp[defender_id] > 0:
            counter = duel.attack_damage(defender_id, attacker_id)
            if command_code == 2:
                counter = max(1, counter // 2)
            duel.apply_damage(attacker_id, counter)
            frames.append(duel_action_frame(
                duel, action_round,
                actor_id=defender_id, target_id=attacker_id,
                damage=counter, label='反击',
            ))
        for viewer, opponent in (
            (attacker, defender),
            (defender, attacker),
        ):
            frames.extend(duel_hp_refresh_frames(viewer, opponent, duel, self.settings))
        show = encode_frame(1040, [
            byte(2),
            integer(action_round),
            byte(0),
            integer(0),
            short(0),
            string(''),
            short(0),
            string(''),
            byte(1),
        ])
        # 双方各自追加自己的 1040/2 播放推进帧（show 帧内容一致）。
        self.push_to_role(defender_id, (*frames, show))
        frames.append(show)
        LOG.info(
            'DUEL_ROUND trace=%s attacker=%d defender=%d round=%d hp=%r command=%d',
            duel.trace_id, attacker_id, defender_id, action_round, dict(duel.hp), command_code,
        )
        if duel.someone_dead():
            winner_id = attacker_id if duel.hp[defender_id] <= 0 else defender_id
            frames.extend(self._finish_duel(duel, winner_id=winner_id))
        return RouteResult.handled(tuple(frames))

    # ------------------------------------------------------------------
    # 1502 战斗资源
    # ------------------------------------------------------------------
    def _handle_resource_query(self, context: SystemContext, values: list[object]) -> RouteResult:
        if len(values) < 3:
            return RouteResult.not_handled()
        # Fields are [action, count, id...]. Action 1 requests a role .dat
        # (1503); actions 0/2 request a PNG payload (1501). Treating all three
        # as .dat leaves actor records alive but permanently invisible.
        query_action = int(values[0])
        resource_count = int(values[1])
        resource_ids = [int(value) for value in values[2:2 + resource_count]]
        battle_state = battle_state_for(context.session)
        username = context.username
        frames: list[bytes] = []
        for resource_id in resource_ids:
            if query_action == 1:
                resource_frames = battle_resource_frames(resource_id)
                resolution = battle_resource_resolution(resource_id)
                response_type = 1503 if resource_frames else None
            elif query_action in (PNG_QUERY_MAIN_CACHE, PNG_QUERY_ROLE_CACHE):
                resource_frames = battle_image_frames(query_action, resource_id)
                resolution = battle_image_resolve_debug(resource_id)
                response_type = 1501 if resource_frames else None
            else:
                LOG.warning('unsupported battle resource action=%d id=%d', query_action, resource_id)
                resource_frames = []
                resolution = {
                    'alias': None,
                    'branch': 'unsupported',
                    'offset_id': None,
                    'resolved_id': None,
                    'resolved_path': None,
                }
                response_type = None
            LOG.info(
                'battle resource response action=%d id=%d chunks=%d battle_trace=%s',
                query_action,
                resource_id,
                len(resource_frames),
                battle_state.trace_id,
            )
            LOG.info(
                '%s',
                format_battle_resource_query_log(
                    username=username,
                    query_action=query_action,
                    resource_ids=resource_ids,
                    battle_active=battle_state.active,
                    round_number=battle_state.round,
                    trace_id=battle_state.trace_id,
                    resource_id=resource_id,
                    resolution=resolution,
                    response_type=response_type,
                    chunks=len(resource_frames),
                ),
            )
            frames.extend(resource_frames)
        return RouteResult.handled(tuple(frames))

    # ------------------------------------------------------------------
    # 1040 回合确认与结算
    # ------------------------------------------------------------------
    def _handle_round_ack(self, context: SystemContext, values: list[object]) -> RouteResult:
        if not values:
            return RouteResult.not_handled()
        battle_state = battle_state_for(context.session)
        role = context.active_role
        # After the client drains its local action queue it sends
        # BATTLE_ACTION_SHOW back as a two-field acknowledgement
        # [action=2, round].  It is the barrier between the player
        # action, the monster counterattack, and the next round.
        ack_action = int(values[0])
        ack_round = int(values[1]) if len(values) > 1 else None
        if not (battle_state.active and ack_action == 2 and ack_round is not None):
            LOG.info(
                'ignored client battle state values=%r active=%s',
                values,
                battle_state.active,
            )
            return RouteResult.handled()
        LOG.info(
            'BATTLE_1040 action=2 ack battle_trace=%s user=%r round=%d server_round=%d',
            battle_state.trace_id,
            context.username,
            ack_round,
            battle_state.round,
        )
        if battle_state.phase != 'round_ack':
            return RouteResult.handled()
        if battle_state.monster_hp <= 0:
            frames = self._settle_victory(context, role, battle_state)
            return RouteResult.handled(frames)
        if battle_state.player_hp <= 0:
            battle_state.finish()
            LOG.info(
                'BATTLE_1040 action=4 battle_trace=%s user=%r reason=player_dead monster_hp=%d player_hp=%d',
                battle_state.trace_id,
                context.username,
                battle_state.monster_hp,
                battle_state.player_hp,
            )
            return RouteResult.handled((battle_end_frame(),))
        # Playback was started by the action=2 frame
        # sent after the 1042 batch. This short client
        # response means both attacks, effects and
        # return movements are now complete.
        battle_state.round = ack_round + 1
        battle_state.phase = 'idle'
        LOG.info(
            'battle round ready battle_trace=%s user=%r round=%d monster_hp=%d player_hp=%d',
            battle_state.trace_id,
            context.username,
            battle_state.round,
            battle_state.monster_hp,
            battle_state.player_hp,
        )
        return RouteResult.handled()

    def _settle_victory(self, context: SystemContext, role, battle_state) -> tuple[bytes, ...]:
        """Monster defeated: grant rewards, notify task progress and end the fight."""
        reward_item = None
        level_up = False
        awarded_experience = BATTLE_EXP_REWARD
        task_frames: tuple[bytes, ...] = ()
        if role is not None:
            awarded_experience = self._experience_reward(role, BATTLE_EXP_REWARD)
            reward_item, level_up = apply_battle_rewards(
                role, registry=self.settings.item_registry,
            )
            if self.task_event_recorder is not None:
                killed_frames = self.task_event_recorder(
                    role,
                    'monster_killed',
                    target_id=battle_state.monster_id,
                )
                won_frames = self.task_event_recorder(
                    role,
                    'battle_won',
                    target_id=battle_state.monster_id,
                )
                task_frames = (*killed_frames, *won_frames)
            if self.save is not None:
                self.save()
        battle_state.finish()
        battle_state.monster_defeated = True
        # Send removal before the reward UI. In
        # automatic mode the APK can otherwise send a
        # new object interaction immediately after the
        # end frame and start a second battle.
        result_frames = [
            battle_end_frame(),
            map_object_remove_frame(battle_state.monster_id),
            *task_frames,
        ]
        if role is not None and reward_item is not None:
            result_frames.extend((
                battle_progress_frame(role),
                item_frame(reward_item, operation=3),
                battle_reward_notice(awarded_experience, reward_item, level_up),
            ))
            if level_up:
                result_frames.append(level_up_effect_frame(role))
                if self.character_update_bus is not None:
                    refresh = self.character_update_bus.publish(
                        self._character_level_changed_event(),
                        role=role,
                        registry=self.settings.item_registry,
                    )
                    result_frames.extend(refresh.frames)
            else:
                result_frames.append(
                    battle_reward_popup(awarded_experience, reward_item, level_up)
                )
        LOG.info(
            'BATTLE_1040 action=4 settlement battle_trace=%s user=%r reason=monster_dead top_protocol=%s monster_hp=%d player_hp=%d',
            battle_state.trace_id,
            context.username,
            '1129/level-up' if level_up else '1049/3',
            battle_state.monster_hp,
            battle_state.player_hp,
        )
        return tuple(result_frames)

    def _experience_reward(self, role, base: int) -> int:
        from systems.fuyuan.service import experience_reward
        return experience_reward(role, base)

    def _character_level_changed_event(self):
        from systems.role.events import CharacterUpdateEvent
        return CharacterUpdateEvent.CHARACTER_LEVEL_CHANGED

    # ------------------------------------------------------------------
    # 1041 战斗指令
    # ------------------------------------------------------------------
    def _handle_command(self, context: SystemContext, values: list[object]) -> RouteResult:
        if not values:
            return RouteResult.not_handled()
        battle_state = battle_state_for(context.session)
        username = context.username
        # C->S command 6 is the APK's player escape request.
        # Command 10 is quit-spectator and must never enter escape.
        command_code = int(values[0])
        LOG.info(
            'BATTLE_1041 battle_trace=%s user=%r values=%r active=%s command=%d',
            battle_state.trace_id,
            username,
            values,
            battle_state.active,
            command_code,
        )
        if is_player_escape_command(command_code):
            if not battle_state.active:
                LOG.info('ignored escape request without active battle user=%r', username)
                return RouteResult.handled()
            if battle_state.phase != 'idle':
                LOG.info('ignored battle escape while awaiting action acknowledgement')
                return RouteResult.handled()
            client_round = int(values[1]) if len(values) > 1 else battle_state.round
            if client_round > 0:
                battle_state.round = client_round
            escape_frames = battle_escape_request_frames(
                battle_state,
                battle_state.round,
            )
            LOG.info(
                'BATTLE_ESCAPE_START battle_trace=%s user=%r player_id=%d round=%d active=%s phase=%s protocol=1041/10',
                battle_state.trace_id,
                username,
                battle_state.player_id,
                battle_state.round,
                battle_state.active,
                battle_state.phase,
            )
            return RouteResult.handled(tuple(escape_frames))
        if not battle_state.active:
            return RouteResult.handled()
        if battle_state.phase != 'idle':
            LOG.info('ignored battle command while awaiting action acknowledgement')
            return RouteResult.handled()
        if command_code not in (1, 2):
            LOG.info('ignored unsupported battle command=%d', command_code)
            return RouteResult.handled()
        client_round = int(values[1]) if len(values) > 1 else battle_state.round
        if client_round > 0:
            battle_state.round = client_round
        action_round = battle_state.round
        target_id = (
            battle_command_target_id(values, battle_state)
            if command_code == 1
            else None
        )
        if command_code == 1 and target_id is None:
            LOG.info('ignored attack with unavailable target values=%r', values)
            return RouteResult.handled()
        action_frames, ended = battle_round_action_frames(
            battle_state,
            command_code,
            action_round,
            target_id=target_id,
        )
        battle_state.phase = 'round_ack'
        LOG.info(
            'battle send player-action battle_trace=%s user=%r command=%d round=%d monster_hp=%d player_hp=%d ended=%s',
            battle_state.trace_id,
            username,
            command_code,
            action_round,
            battle_state.monster_hp,
            battle_state.player_hp,
            ended,
        )
        return RouteResult.handled(
            tuple(action_frames) + (battle_action_show_frame(battle_state, action_round),)
        )

    # ------------------------------------------------------------------
    # 遭遇战入口（由地图系统的对象交互触发）
    # ------------------------------------------------------------------
    def handle_monster_encounter(
        self,
        *,
        username: str,
        role,
        battle_state,
        map_settings,
        object_id: int,
        object_x: int | None,
        object_y: int | None,
        source: str,
    ) -> EncounterResult:
        if should_suppress_escape_retrigger(
            battle_state.escape_guard,
            map_settings.id,
            object_id,
        ):
            log = (
                f'BATTLE_ESCAPE_RETRIGGER_SUPPRESSED user={username!r} '
                f'player_id={battle_state.player_id} monster_id={object_id} '
                f'map_id={map_settings.id} source={source}'
            )
            return EncounterResult((map_object_interaction_ack_frame(object_id),), log)
        if battle_state.monster_defeated:
            log = (
                f'suppressed stale monster interaction user={username!r} '
                f'monster_id={object_id}; encounter already settled'
            )
            return EncounterResult((map_object_remove_frame(object_id),), log)
        if battle_state.active:
            log = (
                f'ignored duplicate monster interaction user={username!r} '
                f'monster_id={object_id}; battle already active '
                f'battle_trace={battle_state.trace_id}'
            )
            return EncounterResult((), log)
        resolved_role = role
        if resolved_role is None:
            from systems.role.service import default_role
            resolved_role = default_role(self.settings)
        battle_state.begin(
            int(resolved_role['id']),
            object_id,
            player_stats=self._combat_stats(resolved_role),
            monster_ids=tuple(item.id for item in map_settings.monsters),
        )
        battle_state.map_id = map_settings.id
        battle_state.contact_tile = (
            (int(object_x), int(object_y))
            if object_x is not None and object_y is not None
            else None
        )
        if battle_state.contact_tile is not None:
            battle_state.player_tile = battle_state.contact_tile
        # The APK's 1040/action=1 handler only updates an already-created
        # battle screen (d/n.d(20)).  A fresh map session has no screen 20
        # yet, so action=1 alone is silently ignored and the UI remains on
        # its loading prompt.  Action 0 is the original reset/open path:
        # it removes any stale map/battle state and then creates screen
        # 20 before action 1 fills in the first round.  The battle screen
        # also builds its grid from 1048 actor records; without these the
        # scene opens but has no drawable player/monster and appears blank.
        log = (
            f'BATTLE_1040 action=0 battle_trace={battle_state.trace_id} user={username!r} | '
            f'BATTLE_1040 action=1 battle_trace={battle_state.trace_id} user={username!r} round=1'
        )
        frames = (
            battle_reset_frame(),
            *battle_actor_frames(
                resolved_role,
                map_settings,
                trace_id=battle_state.trace_id,
                state=battle_state,
            ),
            battle_start_frame(resolved_role, map_settings),
        )
        return EncounterResult(frames, log)

    def _combat_stats(self, role):
        from systems.role.service import combat_stats
        return combat_stats(role, self.settings.item_registry)


def register_battle_routes(router: SystemRouter, system: BattleSystem) -> None:
    router.register(system.system_name, system.can_handle, system.handle)
