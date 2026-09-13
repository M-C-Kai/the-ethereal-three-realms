"""宠物系统协议入口：1127 详情、1103 技能、1128 加点、1130 控制。"""
from __future__ import annotations

import logging

from app.context import SystemContext
from app.router import RouteResult, SystemRouter
from systems.pet.registry import (
    PetRegistry,
    PetSkillRegistry,
    default_pet_registry,
    default_pet_skill_registry,
)
from systems.pet.service import (
    allocate_stats,
    find_pet,
    learn_pet_skill,
    release_pet,
    rename_pet,
)
from systems.pet.protocol import (
    apply_pet_state_request,
    is_pet_detail_request,
    is_pet_skill_request,
    is_pet_state_request,
    parse_pet_release_request,
    parse_pet_rename_request,
    parse_pet_skill_learn_request,
    parse_pet_stat_request,
    pet_detail_frame,
    pet_map_detach_frame,
    pet_property_update_frame,
    pet_release_frame,
    pet_rename_frame,
    pet_skill_learn_result_frame,
    pet_skill_list_frame,
    pet_state_response_frames,
    role_pet_frames,
)

LOG = logging.getLogger('piaomiao-local')


class PetSystem:
    """pet 系统边界：原生宠物协议入口、状态迁移与持久化。"""

    system_name = 'pet'

    def __init__(
        self,
        settings=None,
        save=None,
        registry: PetRegistry | None = None,
        skill_registry: PetSkillRegistry | None = None,
    ) -> None:
        self.settings = settings
        self.save = save
        self.registry = registry or default_pet_registry()
        self.skill_registry = skill_registry or default_pet_skill_registry()

    def ensure_role_pets(self, role: dict[str, object]) -> bool:
        from systems.pet.service import ensure_pet_schema
        return ensure_pet_schema(role, self.registry)

    def role_entry_frames(self, role: dict[str, object]) -> tuple[bytes, ...]:
        frames = role_pet_frames(role, self.registry)
        LOG.info(
            'PET_1127_DOWNLINK role_id=%d pet_count=%d ids=%r',
            int(role.get('id', 0)), len(frames),
            [int(pet.get('id', 0)) for pet in role.get('pets', []) if isinstance(pet, dict)],
        )
        return tuple(frames)

    def can_handle(self, context: SystemContext, message_id: int, fields: list[object]) -> bool:
        role = context.active_role
        if role is None:
            return False
        if message_id == 1128:
            parsed = parse_pet_stat_request(fields)
            return parsed is not None and find_pet(role, parsed[0]) is not None
        if len(fields) < 2:
            return False
        if message_id == 1127:
            return is_pet_detail_request(fields) and find_pet(role, int(fields[1].value)) is not None
        if message_id == 1103:
            return is_pet_skill_request(fields) and find_pet(role, int(fields[1].value)) is not None
        if message_id == 1130:
            learned = parse_pet_skill_learn_request(fields)
            if learned is not None:
                return find_pet(role, learned[0]) is not None
            renamed = parse_pet_rename_request(fields)
            if renamed is not None:
                return find_pet(role, renamed[0]) is not None
            released = parse_pet_release_request(fields)
            if released is not None:
                return find_pet(role, released) is not None
            if is_pet_state_request(fields):
                return find_pet(role, int(fields[1].value)) is not None
        return False

    def handle(self, context: SystemContext, message_id: int, fields: list[object]) -> RouteResult:
        role = context.active_role
        if role is None:
            return RouteResult.not_handled()

        if message_id == 1127:
            pet_id = int(fields[1].value)
            pet = find_pet(role, pet_id)
            LOG.info('PET_1127_DETAIL role_id=%d pet_id=%d properties=30..90', int(role.get('id', 0)), pet_id)
            return RouteResult.handled((pet_detail_frame(pet, self.registry),))

        if message_id == 1103:
            pet_id = int(fields[1].value)
            pet = find_pet(role, pet_id)
            frame = pet_skill_list_frame(pet, self.skill_registry)
            LOG.info(
                'PET_1103_SKILLS role_id=%d pet_id=%d count=%d',
                int(role.get('id', 0)), pet_id,
                len(pet.get('skill_ids', [])) if isinstance(pet.get('skill_ids'), list) else 0,
            )
            return RouteResult.handled((frame,))

        if message_id == 1128:
            parsed = parse_pet_stat_request(fields)
            if parsed is None:
                return RouteResult.not_handled()
            pet_id, deltas = parsed
            mutation = allocate_stats(role, pet_id, deltas, self.registry)
            if not mutation.changed:
                LOG.info('PET_1128_STATS_REJECTED role_id=%d pet_id=%d reason=%s', int(role.get('id', 0)), pet_id, mutation.reason)
                return RouteResult.handled(reason=mutation.reason)
            if self.save is not None:
                self.save()
            LOG.info('PET_1128_STATS role_id=%d pet_id=%d updates=%r', int(role.get('id', 0)), pet_id, mutation.updates)
            return RouteResult.handled((pet_property_update_frame(pet_id, mutation.updates),), changed=True)

        if message_id == 1130:
            learned = parse_pet_skill_learn_request(fields)
            if learned is not None:
                pet_id, book_template_id, book_instance_id = learned
                mutation = learn_pet_skill(
                    role,
                    pet_id,
                    book_template_id,
                    book_instance_id,
                    self.skill_registry,
                )
                if not mutation.changed:
                    LOG.info(
                        'PET_1130_SKILL_REJECTED role_id=%d pet_id=%d book=%d instance=%d reason=%s',
                        int(role.get('id', 0)), pet_id, book_template_id, book_instance_id, mutation.reason,
                    )
                    return RouteResult.handled(reason=mutation.reason)
                if self.save is not None:
                    self.save()
                pet = find_pet(role, pet_id)
                LOG.info(
                    'PET_1130_SKILL role_id=%d pet_id=%d skill_id=%d book_instance=%d remaining=%d',
                    int(role.get('id', 0)), pet_id, mutation.skill_id,
                    mutation.consumed_item_id, mutation.item_remaining,
                )
                return RouteResult.handled((
                    pet_skill_learn_result_frame(
                        pet_id,
                        success=True,
                        forgotten_skill_id=mutation.forgotten_skill_id,
                    ),
                    pet_skill_list_frame(pet, self.skill_registry),
                ), changed=True)

            renamed = parse_pet_rename_request(fields)
            if renamed is not None:
                pet_id, new_name = renamed
                mutation = rename_pet(role, pet_id, new_name)
                if not mutation.changed:
                    return RouteResult.handled(reason=mutation.reason)
                if self.save is not None:
                    self.save()
                LOG.info('PET_1130_RENAME role_id=%d pet_id=%d name=%r', int(role.get('id', 0)), pet_id, mutation.name)
                return RouteResult.handled((pet_rename_frame(pet_id, mutation.name),), changed=True)

            released = parse_pet_release_request(fields)
            if released is not None:
                mutation = release_pet(role, released)
                if not mutation.changed:
                    return RouteResult.handled(reason=mutation.reason)
                frames: list[bytes] = []
                if mutation.was_walking:
                    frames.append(pet_map_detach_frame(int(role.get('id', 0))))
                frames.append(pet_release_frame(released))
                if self.save is not None:
                    self.save()
                LOG.info(
                    'PET_1130_RELEASE role_id=%d pet_id=%d walking=%s deployed=%s',
                    int(role.get('id', 0)), released,
                    mutation.was_walking, mutation.was_deployed,
                )
                return RouteResult.handled(tuple(frames), changed=True)

            if is_pet_state_request(fields):
                result = apply_pet_state_request(role, fields)
                if result.changed and self.save is not None:
                    self.save()
                frames = pet_state_response_frames(int(role.get('id', 0)), result)
                LOG.info(
                    'PET_1130_STATE role_id=%d pet_id=%d action=%d enabled=%s changed=%s updates=%r reason=%s',
                    int(role.get('id', 0)), result.pet_id, result.action, result.enabled,
                    result.changed, result.updates, result.reason,
                )
                return RouteResult.handled(tuple(frames), changed=result.changed, reason=result.reason)

        return RouteResult.not_handled()


def register_pet_routes(router: SystemRouter, system: PetSystem) -> None:
    router.register(system.system_name, system.can_handle, system.handle)
