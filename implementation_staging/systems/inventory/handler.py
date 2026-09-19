from __future__ import annotations

import copy
import logging
import random

from app.context import SystemContext
from app.router import RouteResult, SystemRouter
from app.notify import top_message_frame
from systems.role.events import CharacterUpdateEvent
from systems.role.registry import mount_ride_code_from_item
from protocol import byte, encode_frame, integer, short
from systems.inventory.protocol import (
    client_template_id, item_description_frame, item_detail_frame, item_frame,
)
from systems.inventory.service import (
    bag_capacity, bag_item_count, find_item, is_equipment, is_role_item_equipped,
    gem_embedding_action_result, item_action_location_valid, item_slot,
    role_items, try_move_item_to_bag, socket_opening_action_result,
    strengthening_action_result,
)
from systems.role.service import MOUNT_EQUIPMENT_SLOT


LOG = logging.getLogger('piaomiao-local')


class InventorySystem:
    """inventory 系统边界：1009 物品操作与 1032 物品详情。"""

    system_name = 'inventory'

    def __init__(self, settings=None, save=None, character_update_bus=None, appearance_broadcast_hook=None) -> None:
        self.settings = settings
        self.save = save
        self.character_update_bus = character_update_bus
        # 坐骑穿/卸分支不经过更新总线（自身帧单独构造），通过该钩子把
        # 属性 22（骑乘码=精灵族）的变更同步给视野内的其他客户端。
        self.appearance_broadcast_hook = appearance_broadcast_hook

    def can_handle(self, _context: SystemContext, message_id: int, fields: list[object]) -> bool:
        if message_id == 1032:
            return len(fields) >= 2
        if message_id == 1009:
            return bool(fields)
        return False

    def handle(self, context: SystemContext, message_id: int, fields: list[object]) -> RouteResult:
        role = context.active_role
        values = [field.value for field in fields]
        if message_id == 1032:
            return self._handle_item_detail(context, role, values)
        if message_id == 1009:
            return self._handle_item_action(context, role, values)
        return RouteResult.not_handled()

    # ------------------------------------------------------------------
    # 1032 物品详情
    # ------------------------------------------------------------------
    def _handle_item_detail(self, context: SystemContext, role, values: list[object]) -> RouteResult:
        if role is None or len(values) < 2:
            return RouteResult.not_handled()
        item_id = int(values[1])
        # Different item-detail screens in this client send either
        # the instance id or the shared template id.
        item = find_item(role, item_id)
        if item is None:
            item = next(
                (
                    candidate
                    for candidate in role_items(role)
                    if int(candidate.get('template_id', 0)) == item_id
                    or client_template_id(
                        self.settings.item_registry.resolve(candidate)
                    ) == item_id
                ),
                None,
            )
        if item is None:
            LOG.info('item detail requested for unknown item_id=%d', item_id)
            return RouteResult.handled()
        LOG.info('item detail requested item_id=%d name=%r', item_id, item.get('name'))
        return RouteResult.handled((item_detail_frame(item),))

    # ------------------------------------------------------------------
    # 1009 物品操作
    # ------------------------------------------------------------------
    def _handle_item_action(self, context: SystemContext, role, values: list[object]) -> RouteResult:
        if role is None or not values:
            return RouteResult.not_handled()
        action = int(values[0])
        if action in self._socket_opening_actions():
            return self._handle_socket_opening(context, role, values)
        if action in self._gem_embedding_actions():
            return self._handle_gem_embedding(context, role, values)
        if action in self._strengthening_actions():
            return self._handle_strengthening(context, role, values)
        if len(values) < 2:
            return RouteResult.handled()
        item_id = int(values[1]) if len(values) > 1 else 0
        item = find_item(role, item_id)
        if action == 82 and item is not None:
            return RouteResult.handled((item_description_frame(item),))
        if action == 3 and item is not None and item_action_location_valid(action, item):
            return self._handle_discard(context, role, item, item_id)
        if action == 4 and item is not None and item_action_location_valid(action, item):
            return self._handle_use(context, role, item, item_id)
        if (
            action == 5
            and item is not None
            and is_equipment(item)
            and item_action_location_valid(action, item)
        ):
            return self._handle_equip(context, role, item, item_id)
        if action == 6 and item is not None and item_action_location_valid(action, item):
            return self._handle_unequip(context, role, item, item_id)
        LOG.info(
            'ignored item action=%d item_id=%d values=%r',
            action, item_id, values,
        )
        return RouteResult.handled()

    # ------------------------------------------------------------------
    # 装备开孔（1009/action 95 打开；90 确认）
    # ------------------------------------------------------------------
    def _socket_opening_actions(self):
        from systems.inventory.protocol import SOCKET_OPENING_ACTIONS
        return SOCKET_OPENING_ACTIONS

    def _handle_socket_opening(self, context: SystemContext, role, values: list[object]) -> RouteResult:
        snapshot = copy.deepcopy(role)
        try:
            result = socket_opening_action_result(
                role,
                values,
                random,
                self.settings.item_registry,
            )
            if result.changed:
                self.save()
        except Exception:
            role.clear()
            role.update(snapshot)
            raise
        LOG.info('socket opening action=%r changed=%s message=%r', values, result.changed, result.message)
        return RouteResult.handled(result.frames)

    # ------------------------------------------------------------------
    # 宝石镶嵌（1009/action 98 打开；93 确认）
    # ------------------------------------------------------------------
    def _gem_embedding_actions(self):
        from systems.inventory.protocol import GEM_EMBEDDING_ACTIONS
        return GEM_EMBEDDING_ACTIONS

    def _handle_gem_embedding(self, context: SystemContext, role, values: list[object]) -> RouteResult:
        snapshot = copy.deepcopy(role)
        try:
            result = gem_embedding_action_result(
                role,
                values,
                self.settings.item_registry,
            )
            if result.changed:
                self.save()
        except Exception:
            role.clear()
            role.update(snapshot)
            raise
        LOG.info(
            'gem embedding action=%r changed=%s message=%r',
            values, result.changed, result.message,
        )
        return RouteResult.handled(result.frames)

    # ------------------------------------------------------------------
    # 强化（1009 强化动作）
    # ------------------------------------------------------------------
    def _strengthening_actions(self):
        from systems.inventory.protocol import STRENGTHENING_ACTIONS
        return STRENGTHENING_ACTIONS

    def _handle_strengthening(self, context: SystemContext, role, values: list[object]) -> RouteResult:
        """Apply one 1009 strengthening transition and persist mutations only."""
        snapshot = copy.deepcopy(role)
        try:
            result = strengthening_action_result(role, values, random)
            if result.changed:
                self.save()
        except Exception:
            role.clear()
            role.update(snapshot)
            raise
        if result.changed:
            target_item_id = int(values[1]) if len(values) > 1 else 0
            refresh = self.character_update_bus.publish(
                CharacterUpdateEvent.EQUIPMENT_STRENGTHENED,
                role=role,
                registry=self.settings.item_registry,
                item_id=target_item_id,
            )
            return RouteResult.handled((*result.frames, *refresh.frames))
        return RouteResult.handled(result.frames)

    # ------------------------------------------------------------------
    # 丢弃
    # ------------------------------------------------------------------
    def _handle_discard(self, context: SystemContext, role, item, item_id: int) -> RouteResult:
        was_equipped = is_equipment(item) and item.get('location') == 'equipped'
        role_items(role).remove(item)
        replies = [encode_frame(1009, [short(3), integer(item_id)])]
        if was_equipped:
            refresh = self.character_update_bus.publish(
                CharacterUpdateEvent.EQUIPMENT_CHANGED,
                role=role,
                registry=self.settings.item_registry,
            )
            replies.extend(refresh.frames)
        self.save()
        LOG.info('item discarded item_id=%d name=%r', item_id, item.get('name'))
        return RouteResult.handled(tuple(replies))

    # ------------------------------------------------------------------
    # 使用
    # ------------------------------------------------------------------
    def _handle_use(self, context: SystemContext, role, item, item_id: int) -> RouteResult:
        resolved_item = self.settings.item_registry.resolve(item)
        mount_model = mount_ride_code_from_item(item, self.settings.item_registry)
        if mount_model:
            current_mount = int(role.get('mount_model', 0))
            next_mount = 0 if item.get('location') == 'equipped' or current_mount else int(mount_model)
            item['location'] = 'equipped' if next_mount else 'bag'
            role['mount_model'] = next_mount
            self.save()
            LOG.info(
                'mount %s item_id=%d model=%d',
                'equipped' if next_mount else 'unequipped',
                item_id,
                next_mount,
            )
            replies = (
                item_frame(item, operation=3),
                encode_frame(1009, [short(4)]),
                self._mount_update_frame(role),
            )
            return RouteResult.handled(replies)
        quantity = max(0, int(item.get('quantity', 1)) - 1)
        item['quantity'] = quantity
        item['last_heal'] = int(resolved_item.get('heal', 0))
        replies = [item_frame(item, operation=3), encode_frame(1009, [short(4)])]
        if quantity == 0:
            role_items(role).remove(item)
            replies.insert(1, encode_frame(1009, [short(3), integer(item_id)]))
        self.save()
        LOG.info(
            'item used item_id=%d name=%r remaining=%d',
            item_id, resolved_item.get('name'), quantity,
        )
        return RouteResult.handled(tuple(replies))

    # ------------------------------------------------------------------
    # 装备
    # ------------------------------------------------------------------
    def _handle_equip(self, context: SystemContext, role, item, item_id: int) -> RouteResult:
        resolved_item = self.settings.item_registry.resolve(item)
        mount_model = mount_ride_code_from_item(item, self.settings.item_registry)
        if mount_model:
            updates: list[bytes] = []
            for equipped in role_items(role):
                resolved_equipped = self.settings.item_registry.resolve(equipped)
                if (
                    equipped is not item
                    and equipped.get('location') == 'equipped'
                    and resolved_equipped.get('mount_model')
                ):
                    equipped['location'] = 'bag'
                    updates.append(item_frame(equipped, operation=3))
            item['location'] = 'equipped'
            role['mount_model'] = int(mount_model)
            updates.extend([
                item_frame(item, operation=3),
                encode_frame(1009, [short(5)]),
                self._mount_update_frame(role),
            ])
            if self.appearance_broadcast_hook is not None:
                self.appearance_broadcast_hook(role)
            self.save()
            LOG.info(
                'mount equipped item_id=%d model=%d slot=%d',
                item_id, int(mount_model), MOUNT_EQUIPMENT_SLOT,
            )
            return RouteResult.handled(tuple(updates))
        updates = []
        slot = item_slot(item, self.settings.item_registry)
        for equipped in role_items(role):
            if (
                equipped is not item
                and equipped.get('location') == 'equipped'
                and item_slot(equipped, self.settings.item_registry) == slot
            ):
                equipped['location'] = 'bag'
                updates.append(item_frame(equipped, operation=3))
        item['location'] = 'equipped'
        updates.append(item_frame(item, operation=3))
        updates.append(encode_frame(1009, [short(5)]))
        refresh = self.character_update_bus.publish(
            CharacterUpdateEvent.EQUIPMENT_CHANGED,
            role=role,
            registry=self.settings.item_registry,
        )
        updates.extend(refresh.frames)
        self.save()
        LOG.info(
            'item equipped item_id=%d name=%r slot=%d',
            item_id, resolved_item.get('name'), slot,
        )
        return RouteResult.handled(tuple(updates))

    # ------------------------------------------------------------------
    # 卸下
    # ------------------------------------------------------------------
    def _handle_unequip(self, context: SystemContext, role, item, item_id: int) -> RouteResult:
        if not try_move_item_to_bag(role, item):
            LOG.info(
                'item unequip rejected full_bag item_id=%d occupied=%d capacity=%d',
                item_id,
                bag_item_count(role),
                bag_capacity(role),
            )
            return RouteResult.handled((top_message_frame('背包已满，无法卸下装备'),))
        resolved_item = self.settings.item_registry.resolve(item)
        mount_model = mount_ride_code_from_item(item, self.settings.item_registry)
        if mount_model:
            role['mount_model'] = 0
            if self.appearance_broadcast_hook is not None:
                self.appearance_broadcast_hook(role)
            self.save()
            LOG.info(
                'mount unequipped item_id=%d model=0 slot=%d',
                item_id, MOUNT_EQUIPMENT_SLOT,
            )
            return RouteResult.handled((
                item_frame(item, operation=3),
                encode_frame(1009, [short(6)]),
                self._mount_update_frame(role),
            ))
        refresh = self.character_update_bus.publish(
            CharacterUpdateEvent.EQUIPMENT_CHANGED,
            role=role,
            registry=self.settings.item_registry,
        )
        self.save()
        LOG.info(
            'item unequipped item_id=%d name=%r',
            item_id, item.get('name'),
        )
        replies = [item_frame(item, operation=3), encode_frame(1009, [short(6)])]
        replies.extend(refresh.frames)
        return RouteResult.handled(tuple(replies))

    def _mount_update_frame(self, role):
        from systems.role.protocol import mount_update_frame
        return mount_update_frame(role)


def register_inventory_routes(router: SystemRouter, system: InventorySystem) -> None:
    router.register(system.system_name, system.can_handle, system.handle)
