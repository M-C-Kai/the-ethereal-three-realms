from __future__ import annotations

from types import ModuleType
from typing import Any

from . import encounter, engine, protocol, resources, rewards, state


def _legacy_should_suppress_escape_retrigger(
    guard: dict[str, object] | None,
    map_id: int,
    monster_id: int,
) -> bool:
    return state.should_suppress_guard(guard, map_id, monster_id)


def _legacy_update_escape_guard_for_movement(
    battle_state: state.LocalBattleState,
    x: int,
    y: int,
) -> bool:
    return encounter.update_player_tile(battle_state, x, y)


def _legacy_battle_round_action_frames(
    battle_state: state.LocalBattleState,
    command_code: int,
    round_number: int | None = None,
    *,
    target_id: int | None = None,
) -> tuple[list[bytes], bool]:
    """Adapt the domain engine result to the server's existing frame API."""
    resolution = engine.resolve_round(
        battle_state,
        command_code,
        target_id=target_id,
    )
    if not resolution.accepted:
        return [], False

    action_round = battle_state.round if round_number is None else round_number
    frames: list[bytes] = []
    for action in resolution.actions:
        if action.kind == 'defend':
            frames.append(protocol.battle_defend_frame(battle_state, action_round))
            continue
        if action.kind == 'attack':
            frames.append(protocol.battle_action_frame(
                battle_state,
                action_round,
                actor_id=action.actor_id,
                target_id=action.target_id,
                damage=action.damage,
                label=action.label,
            ))
            continue
        raise ValueError(f'unsupported battle action kind {action.kind!r}')
    return frames, resolution.monster_defeated


def _encounter_source(
    source: str,
    object_x: int | None,
    object_y: int | None,
    object_id: int,
) -> str:
    """Normalize legacy map transports into the three battle entry sources."""
    if source == '2031' and 700_001 <= int(object_id) <= 799_999:
        if object_x is None or object_y is None:
            return 'q_action'
        return 'proximity'
    return 'map_interaction'


def _install_map_encounter_adapter(server_module: ModuleType | Any) -> None:
    """Move the monster branch of map interaction behind encounter.py.

    Portals and NPCs still belong to the map/server layer and delegate to the
    original method unchanged. This adapter can disappear once server.py is
    physically reduced to a thin battle call site.
    """
    server_class = getattr(server_module, 'LocalGameServer', None)
    if server_class is None:
        return
    original = getattr(server_class, '_handle_map_object_interaction', None)
    if original is None or getattr(original, '_battle_encounter_adapter', False):
        return

    async def handle_map_object_interaction(
        self,
        *,
        username: str,
        active_role: dict[str, object] | None,
        object_id: int,
        object_x: int | None,
        object_y: int | None,
        action: int | None,
        source: str,
        writer,
        cipher,
        send_lock,
        battle_state: state.LocalBattleState,
        npc_dialogue_state,
    ) -> None:
        current_settings = server_module.settings_for_role(self.settings, active_role)

        # Preserve the original map-layer precedence: portal -> NPC -> monster.
        if any(int(portal.id) == int(object_id) for portal in current_settings.portals):
            return await original(
                self,
                username=username,
                active_role=active_role,
                object_id=object_id,
                object_x=object_x,
                object_y=object_y,
                action=action,
                source=source,
                writer=writer,
                cipher=cipher,
                send_lock=send_lock,
                battle_state=battle_state,
                npc_dialogue_state=npc_dialogue_state,
            )
        if server_module.map_npc_for_object_id(current_settings, object_id) is not None:
            return await original(
                self,
                username=username,
                active_role=active_role,
                object_id=object_id,
                object_x=object_x,
                object_y=object_y,
                action=action,
                source=source,
                writer=writer,
                cipher=cipher,
                send_lock=send_lock,
                battle_state=battle_state,
                npc_dialogue_state=npc_dialogue_state,
            )

        monster = server_module.map_monster_for_object_id(current_settings, object_id)
        if monster is None:
            return await original(
                self,
                username=username,
                active_role=active_role,
                object_id=object_id,
                object_x=object_x,
                object_y=object_y,
                action=action,
                source=source,
                writer=writer,
                cipher=cipher,
                send_lock=send_lock,
                battle_state=battle_state,
                npc_dialogue_state=npc_dialogue_state,
            )

        role = active_role if active_role is not None else server_module.default_role(self.settings)
        player_tile = (
            (int(role.get('map_x', 0)), int(role.get('map_y', 0)))
            if role is not None
            else battle_state.player_tile
        )
        monster_tile = (
            (int(object_x), int(object_y))
            if object_x is not None and object_y is not None
            else (int(monster.x), int(monster.y))
        )
        request = encounter.EncounterRequest(
            map_id=int(current_settings.id),
            monster_id=int(object_id),
            player_id=int(role['id']),
            player_tile=player_tile,
            monster_tile=monster_tile,
            source=_encounter_source(source, object_x, object_y, object_id),
        )
        decision = encounter.request_encounter(
            battle_state,
            request,
            player_stats=server_module.combat_stats(role),
            monster_ids=tuple(item.id for item in current_settings.monsters),
        )

        if not decision.start:
            if decision.reason == 'escape_guard':
                server_module.LOG.info(
                    'BATTLE_ESCAPE_RETRIGGER_SUPPRESSED user=%r player_id=%d monster_id=%d map_id=%d source=%s',
                    username,
                    int(role['id']),
                    object_id,
                    current_settings.id,
                    request.source,
                )
                await self._send(
                    writer,
                    server_module.map_object_interaction_ack_frame(object_id),
                    cipher=cipher,
                    lock=send_lock,
                )
                return
            if decision.reason == 'monster_defeated':
                server_module.LOG.info(
                    'suppressed stale monster interaction user=%r monster_id=%d; encounter already settled',
                    username,
                    object_id,
                )
                await self._send(
                    writer,
                    server_module.map_object_remove_frame(object_id),
                    cipher=cipher,
                    lock=send_lock,
                )
                return
            server_module.LOG.info(
                'ignored duplicate monster interaction user=%r monster_id=%d reason=%s battle_trace=%s',
                username,
                object_id,
                decision.reason,
                battle_state.trace_id,
            )
            return

        server_module.LOG.info(
            'BATTLE_ENCOUNTER_START source=%s user=%r map=%d player_id=%d monster_id=%d player_tile=%s monster_tile=%s battle_trace=%s',
            request.source,
            username,
            request.map_id,
            request.player_id,
            request.monster_id,
            request.player_tile,
            request.monster_tile,
            battle_state.trace_id,
        )
        await self._send(
            writer,
            protocol.battle_reset_frame(),
            *server_module.battle_actor_frames(
                role,
                current_settings,
                trace_id=battle_state.trace_id,
                state=battle_state,
            ),
            protocol.battle_start_frame(role, current_settings),
            cipher=cipher,
            lock=send_lock,
        )

    handle_map_object_interaction._battle_encounter_adapter = True
    server_class._handle_map_object_interaction = handle_map_object_interaction


def install(server_module: ModuleType | Any) -> None:
    """Install extracted battle components behind the legacy server API.

    This compatibility layer lets the active launcher use one authoritative
    battle implementation while the large ``server.py`` file is being reduced.
    Once server.py imports battle directly, this module can be deleted without
    changing battle behavior.
    """
    server_module.CombatStats = state.CombatStats
    server_module.LocalBattleState = state.LocalBattleState
    server_module.should_suppress_escape_retrigger = _legacy_should_suppress_escape_retrigger
    server_module.update_escape_guard_for_movement = _legacy_update_escape_guard_for_movement

    server_module.battle_command_target_id = engine.battle_command_target_id
    server_module.battle_round_action_frames = _legacy_battle_round_action_frames

    reward_services = rewards.RewardServices(
        role_items=server_module.role_items,
        bag_item_count=server_module.bag_item_count,
        bag_capacity=server_module.bag_capacity,
        apply_one_level=server_module.apply_one_level,
        max_role_level=server_module.MAX_ROLE_LEVEL,
    )

    def legacy_apply_battle_rewards(
        role: dict[str, object],
        experience: int = rewards.BATTLE_EXP_REWARD,
        registry=None,
    ):
        return rewards.apply_battle_rewards(
            role,
            reward_services,
            experience=experience,
            registry=registry,
        )

    server_module.apply_battle_rewards = legacy_apply_battle_rewards
    server_module.BATTLE_EXP_REWARD = rewards.BATTLE_EXP_REWARD
    server_module.BATTLE_DROP_TEMPLATE_ID = rewards.BATTLE_DROP_TEMPLATE_ID

    for name in (
        'battle_reset_frame',
        'battle_start_frame',
        'battle_actor_source_model_for_debug',
        'battle_actor_debug_snapshot',
        'format_battle_actor_1048_log',
        'battle_actor_frame',
        'battle_action_frame',
        'battle_defend_frame',
        'battle_move_frame',
        'battle_action_show_frame',
        'battle_escape_frame',
        'battle_escape_request_frames',
        'battle_end_frame',
        'battle_reward_popup',
        'is_player_escape_command',
    ):
        setattr(server_module, name, getattr(protocol, name))

    for name in (
        'battle_resource_resolution',
        'format_battle_resource_query_log',
        'battle_resource_path',
        'battle_resource_frames',
        'battle_image_resource',
        'battle_image_resolve_debug',
        'battle_image_frames',
    ):
        setattr(server_module, name, getattr(resources, name))
    server_module.BATTLE_RESOURCE_MODEL_OFFSET = resources.BATTLE_RESOURCE_MODEL_OFFSET
    server_module.BATTLE_RESOURCE_ALIASES = resources.BATTLE_RESOURCE_ALIASES
    server_module.BATTLE_EMPTY_RESOURCE_IDS = resources.BATTLE_EMPTY_RESOURCE_IDS
    server_module.PNG_QUERY_MAIN_CACHE = resources.PNG_QUERY_MAIN_CACHE
    server_module.PNG_QUERY_ROLE_CACHE = resources.PNG_QUERY_ROLE_CACHE

    _install_map_encounter_adapter(server_module)
