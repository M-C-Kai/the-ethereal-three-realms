from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass

from app.context import SystemContext
from app.router import RouteResult, SystemRouter
import systems.skill.protocol as protocol
from systems.skill.protocol import gather_interrupt_frame, gather_start_frame
from systems.skill.service import (
    SkillService, gather_start_check, life_skill_state, life_stamina,
)


LOG = logging.getLogger('piaomiao-local')


@dataclass(frozen=True)
class SkillHandleResult:
    handled: bool
    frames: tuple[bytes, ...] = ()
    reason: str = ''


@dataclass(frozen=True)
class GatherStartResult:
    handled: bool
    frames: tuple[bytes, ...] = ()
    session: dict[str, object] | None = None
    target: object | None = None
    reason: str = ''

class ConnectionGathering:
    """Connection-scoped gathering state: one active gather, token-guarded.

    The asyncio completion task closes over the session; every wakeup must
    pass `is_current` (same token/role/target) and `consume` before any
    reward is applied, so a stale task can never pay out twice.
    """

    def __init__(self) -> None:
        self.session: dict[str, object] | None = None
        self.task: asyncio.Task | None = None
        self._token = 0

    def start(
        self,
        role: dict[str, object],
        target,
        map_id: int,
    ) -> tuple[tuple[bytes, ...], dict[str, object] | None]:
        if self.session is not None:
            return (), None
        self._token += 1
        self.session = {
            'token': self._token,
            'role_id': int(role.get('id', 0)),
            'target_id': int(target.target_id),
            'map_id': int(map_id),
            'x': int(target.x),
            'y': int(target.y),
        }
        return (gather_start_frame(int(target.duration_seconds), int(target.target_id)),), self.session

    def is_current(self, session: dict[str, object] | None) -> bool:
        return (
            self.session is not None
            and session is not None
            and self.session is session
            and self.session.get('token') == self._token
        )

    def consume(self, session: dict[str, object] | None) -> bool:
        """Atomically claim the reward right for a current session."""
        if not self.is_current(session):
            return False
        self.session = None
        return True

    def cancel(self) -> bytes | None:
        """Stop any active gather; returns the 2027 interrupt frame if one ran."""
        had_session = self.session is not None
        self.session = None
        if self.task is not None:
            self.task.cancel()
            self.task = None
        return gather_interrupt_frame() if had_session else None




class SkillSystem:
    """skill 系统边界。"""

    system_name = 'skill'

    def __init__(self, settings=None, item_registry=None, save=None) -> None:
        self.settings = settings
        life_registry = getattr(settings, 'life_registry', None)
        resolved_items = getattr(settings, 'item_registry', item_registry)
        self.service = SkillService(life_registry, resolved_items, save) if life_registry is not None else None

    def can_handle(self, _context: SystemContext, message_id: int, _fields: list[object]) -> bool:
        return message_id in (1132, 1143, 2027, 1084)

    def handle(self, context: SystemContext, message_id: int, fields: list[object]) -> RouteResult:
        """生活技能与打造的统一协议入口。"""
        role = context.active_role
        if message_id == 1084:
            return self._handle_forge(context, fields)
        if role is None:
            return RouteResult.not_handled(reason='no_active_role')
        if message_id in (1132, 1143):
            result = self.handle_message(message_id, fields, role)
            if result.frames:
                return RouteResult.handled(result.frames)
            LOG.info('ignored skill message=%d values=%r', message_id, [f.value for f in fields])
            return RouteResult.not_handled(reason=result.reason)
        if message_id == 2027:
            return self._handle_gather_start(context, role, fields)
        return RouteResult.not_handled()

    def _handle_forge(self, context: SystemContext, fields: list[object]) -> RouteResult:
        """1084 打造请求只做校验与记录，APK 的配方语义未完全锁定。"""
        username = context.username
        if protocol.is_forge_list_request(fields):
            LOG.info('FORGE_OPEN user=%r context=%d', username, int(fields[1].value))
            return RouteResult.handled()
        if protocol.is_forge_select_request(fields):
            LOG.info('FORGE_REQUEST user=%r recipe_id=%d', username, int(fields[1].value))
            return RouteResult.handled()
        if protocol.is_forge_collect_request(fields):
            LOG.info(
                'FORGE_REQUEST user=%r recipe_id=%d slots=%r kind=collect',
                username,
                int(fields[1].value),
                [int(field.value) for field in fields[2:]],
            )
            return RouteResult.handled()
        if protocol.is_forge_confirm_request(fields):
            LOG.info(
                'FORGE_REQUEST user=%r recipe_id=%d slots=%r kind=confirm',
                username,
                int(fields[1].value),
                [int(field.value) for field in fields[2:]],
            )
            return RouteResult.handled()
        LOG.info('ignored forge message=1084 fields=%r', [f.type_id for f in fields])
        return RouteResult.not_handled()

    def _handle_gather_start(self, context: SystemContext, role, fields: list[object]) -> RouteResult:
        gathering = context.session.get('gathering')
        if not isinstance(gathering, ConnectionGathering):
            gathering = ConnectionGathering()
            context.session['gathering'] = gathering
        gather_result = self.start_gathering(role, fields, gathering)
        if not gather_result.handled:
            return RouteResult.not_handled(reason=gather_result.reason)
        if gather_result.session is not None:
            self.schedule_gathering_completion(context, gather_result)
        if gather_result.frames:
            return RouteResult.handled(gather_result.frames, reason=gather_result.reason)
        return RouteResult.handled(reason=gather_result.reason)

    def schedule_gathering_completion(
        self,
        context: SystemContext,
        gather_result: GatherStartResult,
    ) -> None:
        """Start the delayed gather completion task for a successful 2027."""
        if gather_result.session is None or gather_result.target is None:
            return
        session = context.session
        gathering = session.get('gathering')
        if not isinstance(gathering, ConnectionGathering):
            return
        task = asyncio.create_task(self._finish_gathering_later(
            context,
            gathering,
            gather_result.session,
            gather_result.target,
            delay=max(0.0, float(gather_result.target.duration_seconds)),
        ))
        gathering.task = task

    async def _finish_gathering_later(
        self,
        context: SystemContext,
        gathering: ConnectionGathering,
        gather_session: dict[str, object],
        target,
        *,
        delay: float,
    ) -> None:
        """Complete a gather after `delay` seconds unless the session went stale."""
        try:
            if delay > 0:
                await asyncio.sleep(delay)
            if not gathering.is_current(gather_session):
                return
            active_role = context.session.get('active_role')
            if active_role is None or int(gather_session.get('role_id', 0)) != int(active_role.get('id', 0)):
                return
            if not gathering.consume(gather_session):
                return
            result = self.handle_gather_completion(active_role, target)
            if not result.changed:
                return
            LOG.info(
                'GATHER_COMPLETE user=%r role_id=%d target_id=%d stamina=%d proficiency=%d',
                context.username,
                int(gather_session.get('role_id', 0)),
                int(gather_session.get('target_id', 0)),
                life_stamina(active_role),
                (life_skill_state(active_role, target.skill_id) or {}).get('proficiency', 0),
            )
            push = context.session.get('push_frames')
            if push is not None:
                await push(*result.frames)
        except asyncio.CancelledError:
            raise
        except (ConnectionResetError, BrokenPipeError, OSError):
            return

    def handle_life_craft(self, role: dict[str, object], fields: list[object]) -> object:
        if self.service is None:
            raise RuntimeError('skill service is not configured')
        return self.service.craft(role, fields, protocol)

    def handle_life_learn(self, role, fields, trainer_id=0):
        return self.service.learn(role, fields, trainer_id)

    def handle_life_upgrade(self, role, fields):
        return self.service.upgrade(role, fields)

    def handle_gather_completion(self, role, target):
        return self.service.complete_gathering(role, target)

    def handle_message(self, message_id, fields, role) -> SkillHandleResult:
        if self.service is None or role is None:
            return SkillHandleResult(False)
        registry = self.service.life_registry
        if message_id == 1132:
            if protocol.is_life_skill_list_request(fields):
                return SkillHandleResult(True, (protocol.life_skill_list_frame(role, self.settings),))
            if protocol.is_life_skill_open_request(fields):
                skill_id = int(fields[1].value); skill = registry.skills.get(skill_id)
                if skill is None: return SkillHandleResult(True, reason='unknown_skill')
                state = protocol.life_skill_state(role, skill_id) or {}
                return SkillHandleResult(True, (protocol.life_tier_frame(skill, registry), protocol.life_skill_info_frame(skill_id, int(state.get('level', 0)), f'{skill.name} 熟练度 {int(state.get("proficiency", 0))}')))
            if protocol.is_life_recipe_list_request(fields):
                skill_id, tier = int(fields[1].value), int(fields[2].value)
                skill = registry.skills.get(skill_id); recipes = registry.recipes_for(skill_id, tier)
                return SkillHandleResult(True, (protocol.life_recipe_list_frame(skill, tier, recipes, registry),) if skill is not None and recipes else (), 'no_recipes' if not recipes else '')
            if protocol.is_life_skill_info_request(fields):
                skill_id = int(fields[1].value); skill = registry.skills.get(skill_id); state = protocol.life_skill_state(role, skill_id) or {}
                text = f'{skill.name} 等级 {state.get("level", 0)}' if skill else '未知技能'
                return SkillHandleResult(True, (protocol.life_skill_info_frame(skill_id, int(state.get('level', 0)), text),))
            if protocol.is_life_skill_upgrade_request(fields):
                skill_id = int(fields[1].value)
                if registry.skills.get(skill_id) is None: return SkillHandleResult(True, reason='unknown_skill')
                result = self.handle_life_upgrade(role, fields)
                return SkillHandleResult(True, result.frames if result.changed else (protocol.life_skill_info_frame(skill_id, 0, result.reason),), result.reason)
            return SkillHandleResult(False)
        if message_id == 1143 and fields:
            if protocol.is_life_trainer_list_request(fields):
                trainer = registry.trainers.get(int(fields[1].value))
                return SkillHandleResult(True, (protocol.life_learnable_list_frame(trainer, role, self.settings),) if trainer else (), 'unknown_trainer' if trainer is None else '')
            if protocol.is_life_learnable_detail_request(fields):
                entry = registry.learnable.get(int(fields[1].value))
                return SkillHandleResult(True, (protocol.life_learnable_detail_frame(entry),) if entry else (), 'unknown_entry' if entry is None else '')
            if protocol.is_life_learn_request(fields):
                entry_id = int(fields[1].value); entry = registry.learnable.get(entry_id)
                trainer = next((candidate for candidate in registry.trainers.values() if candidate.teaches(entry_id)), None)
                result = self.handle_life_learn(role, fields, trainer.trainer_id if trainer else 0)
                if result.changed: return SkillHandleResult(True, (*result.frames, protocol.life_trainer_page_frame(trainer)))
                frames = (protocol.life_learn_result_frame(0, entry, False, entry),) if entry and trainer else ()
                return SkillHandleResult(True, frames, result.reason)
            if protocol.is_life_craft_detail_request(fields):
                recipe = registry.recipe(int(fields[1].value))
                return SkillHandleResult(True, (protocol.life_craft_detail_frame(recipe, role, self.settings), protocol.life_craft_text_frame(recipe.description)) if recipe else (), 'unknown_recipe' if recipe is None else '')
            if protocol.is_life_craft_request(fields) or protocol.is_life_direct_use_request(fields):
                result = self.handle_life_craft(role, fields)
                frames = result.frames if result.changed else (protocol.life_craft_text_frame(result.reason or '无法制造'), protocol.life_craft_ack_frame())
                return SkillHandleResult(True, frames, result.reason)
            if protocol.is_life_craft_text_request(fields):
                recipe = registry.recipe(int(fields[1].value)); text = recipe.description if recipe else ''
                return SkillHandleResult(True, (protocol.life_craft_text_frame(text),))
        return SkillHandleResult(False)

    def start_gathering(self, role, fields, gathering: ConnectionGathering) -> GatherStartResult:
        if self.service is None or role is None or not protocol.is_gather_start_request(fields):
            return GatherStartResult(False)
        target = self.service.life_registry.gather_target(int(fields[1].value))
        reason = gather_start_check(role, target, gathering.session is not None, self.service.life_registry) if target is not None else '采集目标不存在'
        if not reason and int(role.get('map_id', self.settings.default_map_id)) != int(target.map_id):
            reason = '地图不匹配'
        if reason:
            return GatherStartResult(True, (protocol.gather_interrupt_frame(),), target=target, reason=reason)
        frames, session = gathering.start(role, target, int(target.map_id))
        if session is None:
            return GatherStartResult(True, (protocol.gather_interrupt_frame(),), target=target, reason='已有采集任务')
        return GatherStartResult(True, frames, session, target)


def register_skill_routes(router: SystemRouter, system: SkillSystem) -> None:
    router.register(system.system_name, system.can_handle, system.handle)
