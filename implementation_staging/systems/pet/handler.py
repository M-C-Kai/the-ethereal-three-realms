"""宠物系统协议入口：1127 详情、1103 技能、1130 状态。"""
from __future__ import annotations

import logging

from app.context import SystemContext
from app.router import RouteResult, SystemRouter
from systems.pet.registry import PetRegistry, default_pet_registry
from systems.pet.service import find_pet
from systems.pet.protocol import (
    apply_pet_state_request, is_pet_detail_request, is_pet_skill_request,
    is_pet_state_request, pet_detail_frame, pet_skill_list_frame, role_pet_frames,
    pet_state_response_frames,
)


LOG = logging.getLogger('piaomiao-local')


class PetSystem:
    """pet 系统边界：宠物协议入口与角色宠物状态迁移。"""

    system_name = 'pet'

    def __init__(self, settings=None, save=None, registry: PetRegistry | None = None) -> None:
        self.settings = settings
        self.save = save
        self.registry = registry or default_pet_registry()

    # ------------------------------------------------------------------
    # 角色集成钩子（由 server 装配注入角色系统）
    # ------------------------------------------------------------------
    def ensure_role_pets(self, role: dict[str, object]) -> bool:
        """Ensure the role carries the native pet schema; returns changed."""
        from systems.pet.service import ensure_pet_schema
        return ensure_pet_schema(role, self.registry)

    def role_entry_frames(self, role: dict[str, object]) -> tuple[bytes, ...]:
        """Pet container frames appended to the role entry sequence."""
        frames = role_pet_frames(role, self.registry)
        LOG.info(
            'PET_1127_DOWNLINK role_id=%d pet_count=%d ids=%r',
            int(role.get('id', 0)), len(frames),
            [int(pet.get('id', 0)) for pet in role.get('pets', []) if isinstance(pet, dict)],
        )
        return tuple(frames)

    # ------------------------------------------------------------------
    # 路由
    # ------------------------------------------------------------------
    def can_handle(self, context: SystemContext, message_id: int, fields: list[object]) -> bool:
        role = context.active_role
        if role is None or len(fields) < 2:
            return False
        pet_id = int(fields[1].value)
        if find_pet(role, pet_id) is None:
            return False
        if message_id == 1127:
            return is_pet_detail_request(fields)
        if message_id == 1103:
            return is_pet_skill_request(fields)
        if message_id == 1130:
            return is_pet_state_request(fields)
        return False

    def handle(self, context: SystemContext, message_id: int, fields: list[object]) -> RouteResult:
        role = context.active_role
        pet_id = int(fields[1].value)
        if message_id == 1127:
            pet = find_pet(role, pet_id)
            LOG.info(
                'PET_1127_DETAIL role_id=%d pet_id=%d properties=30..90',
                int(role.get('id', 0)), pet_id,
            )
            return RouteResult.handled((pet_detail_frame(pet, self.registry),))
        if message_id == 1103:
            pet = find_pet(role, pet_id)
            LOG.info(
                'PET_1103_SKILLS role_id=%d pet_id=%d count=0',
                int(role.get('id', 0)), pet_id,
            )
            return RouteResult.handled((pet_skill_list_frame(pet),))
        if message_id == 1130:
            result = apply_pet_state_request(role, fields)
            if result.changed and self.save is not None:
                self.save()
            frames = pet_state_response_frames(int(role.get('id', 0)), result)
            LOG.info(
                'PET_1130_STATE role_id=%d pet_id=%d action=%d enabled=%s changed=%s updates=%r reason=%s',
                int(role.get('id', 0)), result.pet_id, result.action, result.enabled,
                result.changed, result.updates, result.reason,
            )
            return RouteResult.handled(tuple(frames))
        return RouteResult.not_handled()


def register_pet_routes(router: SystemRouter, system: PetSystem) -> None:
    router.register(system.system_name, system.can_handle, system.handle)
