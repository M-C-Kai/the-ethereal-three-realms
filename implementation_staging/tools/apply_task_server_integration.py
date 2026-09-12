from __future__ import annotations

from pathlib import Path


SERVER = Path(__file__).resolve().parents[1] / 'server.py'


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f'{label}: expected exactly one match, got {count}')
    return text.replace(old, new, 1)


def replace_exact_count(text: str, old: str, new: str, expected: int, label: str) -> str:
    count = text.count(old)
    if count != expected:
        raise RuntimeError(f'{label}: expected {expected} matches, got {count}')
    return text.replace(old, new)


def main() -> None:
    text = SERVER.read_text(encoding='utf-8')

    text = replace_once(
        text,
        "from character_update_bus import CharacterUpdateBus, CharacterUpdateEvent\n",
        "from character_update_bus import CharacterUpdateBus, CharacterUpdateEvent\n"
        "from task_protocol import parse_task_1145_request\n"
        "from task_server_support import default_task_server_support\n"
        "from task_service import ensure_task_state\n",
        'task imports',
    )

    text = replace_once(
        text,
        "MENU_PREFETCH_EMPTY_SUBTYPES = {\n    1403: 1,\n",
        "MENU_PREFETCH_EMPTY_SUBTYPES = {\n",
        'remove task empty prefetch',
    )

    text = replace_exact_count(
        text,
        "    role['bag_reset_version'] = ROLE_BAG_RESET_VERSION\n    fuyuan.ensure_state(role)\n",
        "    role['bag_reset_version'] = ROLE_BAG_RESET_VERSION\n    ensure_task_state(role)\n    fuyuan.ensure_state(role)\n",
        2,
        'initialize task state for new/default roles',
    )

    text = replace_once(
        text,
        "        changed = False\n        for role in roles:\n            if fuyuan.settle(role):\n",
        "        changed = False\n        for role in roles:\n            if ensure_task_state(role):\n                changed = True\n            if fuyuan.settle(role):\n",
        'legacy task-state migration',
    )

    text = replace_once(
        text,
        "        self.roles = RoleStore(settings)\n        self.character_update_bus = build_character_update_bus()\n        self._next_session_id = 1000\n",
        "        self.roles = RoleStore(settings)\n        self.character_update_bus = build_character_update_bus()\n"
        "        self.task_support = default_task_server_support(settings.item_registry)\n"
        "        self.task_runtime = self.task_support.runtime\n"
        "        self._next_session_id = 1000\n",
        'task runtime initialization',
    )

    text = replace_once(
        text,
        "    def handle_sect_skill_request(\n",
        "    def handle_task_1403(\n"
        "        self,\n"
        "        role: dict[str, object],\n"
        "        fields: list[Field],\n"
        "        *,\n"
        "        today: str | None = None,\n"
        "    ) -> tuple[bytes, ...]:\n"
        "        result = self.task_runtime.handle_1403(role, fields, today=today)\n"
        "        if result.changed:\n"
        "            self.roles.save()\n"
        "        return result.frames\n\n"
        "    def handle_task_1145(\n"
        "        self,\n"
        "        role: dict[str, object],\n"
        "        fields: list[Field],\n"
        "        *,\n"
        "        now: int | float = 0,\n"
        "        today: str | None = None,\n"
        "    ) -> tuple[bytes, ...] | None:\n"
        "        result = self.task_runtime.handle_1145(\n"
        "            role,\n"
        "            fields,\n"
        "            reward_applier=self.task_support.apply_rewards,\n"
        "            now=now,\n"
        "            today=today,\n"
        "        )\n"
        "        if result is None:\n"
        "            return None\n"
        "        if result.changed:\n"
        "            self.roles.save()\n"
        "        return result.frames\n\n"
        "    def record_task_event(\n"
        "        self,\n"
        "        role: dict[str, object],\n"
        "        kind: str,\n"
        "        *,\n"
        "        target_id: int = 0,\n"
        "        amount: int = 1,\n"
        "        now: int | float = 0,\n"
        "        today: str | None = None,\n"
        "    ) -> tuple[bytes, ...]:\n"
        "        result = self.task_runtime.record_event(\n"
        "            role,\n"
        "            kind,\n"
        "            target_id=target_id,\n"
        "            amount=amount,\n"
        "            now=now,\n"
        "            today=today,\n"
        "        )\n"
        "        if result.changed:\n"
        "            self.roles.save()\n"
        "        return result.frames\n\n"
        "    def handle_sect_skill_request(\n",
        'task server methods',
    )

    text = replace_once(
        text,
        "                    else:\n                        LOG.info('ignored skill message=%d values=%r', message_id, values)\n                elif message_id in MENU_PREFETCH_EMPTY_SUBTYPES:\n",
        "                    else:\n                        LOG.info('ignored skill message=%d values=%r', message_id, values)\n"
        "                elif message_id == 1403 and active_role is not None:\n"
        "                    response_frames = self.handle_task_1403(active_role, fields)\n"
        "                    LOG.info(\n"
        "                        'task protocol 1403 user=%r role_id=%d values=%r replies=%d',\n"
        "                        username,\n"
        "                        int(active_role.get('id', 0)),\n"
        "                        values,\n"
        "                        len(response_frames),\n"
        "                    )\n"
        "                    if response_frames:\n"
        "                        await self._send(\n"
        "                            writer,\n"
        "                            *response_frames,\n"
        "                            cipher=game_cipher,\n"
        "                            lock=send_lock,\n"
        "                        )\n"
        "                elif message_id in MENU_PREFETCH_EMPTY_SUBTYPES:\n",
        'route protocol 1403',
    )

    text = replace_once(
        text,
        "                elif message_id == 1145 and is_map_pathfind_request(fields) and active_role is not None:\n",
        "                elif (\n"
        "                    message_id == 1145\n"
        "                    and active_role is not None\n"
        "                    and parse_task_1145_request(fields) is not None\n"
        "                ):\n"
        "                    response_frames = self.handle_task_1145(\n"
        "                        active_role, fields, now=time.time(),\n"
        "                    )\n"
        "                    LOG.info(\n"
        "                        'task protocol 1145 user=%r role_id=%d values=%r replies=%d',\n"
        "                        username,\n"
        "                        int(active_role.get('id', 0)),\n"
        "                        values,\n"
        "                        len(response_frames or ()),\n"
        "                    )\n"
        "                    if response_frames:\n"
        "                        await self._send(\n"
        "                            writer,\n"
        "                            *response_frames,\n"
        "                            cipher=game_cipher,\n"
        "                            lock=send_lock,\n"
        "                        )\n\n"
        "                elif message_id == 1145 and is_map_pathfind_request(fields) and active_role is not None:\n",
        'route task-shaped 1145 before map pathfind',
    )

    text = replace_once(
        text,
        "                        enter_frames.extend(\n"
        "                            gather_spawn_frame(target)\n"
        "                            for target in self.settings.life_registry.gather_targets_for(\n"
        "                                current_settings.id\n"
        "                            )\n"
        "                        )\n"
        "                        await self._send(\n",
        "                        enter_frames.extend(\n"
        "                            gather_spawn_frame(target)\n"
        "                            for target in self.settings.life_registry.gather_targets_for(\n"
        "                                current_settings.id\n"
        "                            )\n"
        "                        )\n"
        "                        if active_role is not None:\n"
        "                            enter_frames.extend(self.record_task_event(\n"
        "                                active_role,\n"
        "                                'map_entered',\n"
        "                                target_id=current_settings.id,\n"
        "                                now=time.time(),\n"
        "                            ))\n"
        "                        await self._send(\n",
        'map-enter task event',
    )

    text = replace_once(
        text,
        "            await self._send(\n"
        "                writer,\n"
        "                *map_npc_dialogue_frames(npc, active_role, self.settings),\n"
        "                cipher=cipher,\n"
        "                lock=send_lock,\n"
        "            )\n"
        "            return\n\n"
        "        monster = map_monster_for_object_id(current_settings, object_id)\n",
        "            task_frames = (\n"
        "                self.record_task_event(\n"
        "                    active_role,\n"
        "                    'npc_talked',\n"
        "                    target_id=npc.id,\n"
        "                    now=time.time(),\n"
        "                )\n"
        "                if active_role is not None\n"
        "                else ()\n"
        "            )\n"
        "            await self._send(\n"
        "                writer,\n"
        "                *map_npc_dialogue_frames(npc, active_role, self.settings),\n"
        "                *task_frames,\n"
        "                cipher=cipher,\n"
        "                lock=send_lock,\n"
        "            )\n"
        "            return\n\n"
        "        monster = map_monster_for_object_id(current_settings, object_id)\n",
        'npc-talk task event',
    )

    text = replace_once(
        text,
        "                                if active_role is not None:\n"
        "                                    awarded_experience = fuyuan.experience_reward(active_role, BATTLE_EXP_REWARD)\n"
        "                                    reward_item, level_up = apply_battle_rewards(active_role, registry=self.settings.item_registry)\n"
        "                                    self.roles.save()\n"
        "                                battle_state.finish()\n"
        "                                battle_state.monster_defeated = True\n",
        "                                task_frames: tuple[bytes, ...] = ()\n"
        "                                if active_role is not None:\n"
        "                                    awarded_experience = fuyuan.experience_reward(active_role, BATTLE_EXP_REWARD)\n"
        "                                    reward_item, level_up = apply_battle_rewards(active_role, registry=self.settings.item_registry)\n"
        "                                    killed_frames = self.record_task_event(\n"
        "                                        active_role,\n"
        "                                        'monster_killed',\n"
        "                                        target_id=battle_state.monster_id,\n"
        "                                        now=time.time(),\n"
        "                                    )\n"
        "                                    won_frames = self.record_task_event(\n"
        "                                        active_role,\n"
        "                                        'battle_won',\n"
        "                                        target_id=battle_state.monster_id,\n"
        "                                        now=time.time(),\n"
        "                                    )\n"
        "                                    task_frames = (*killed_frames, *won_frames)\n"
        "                                    self.roles.save()\n"
        "                                battle_state.finish()\n"
        "                                battle_state.monster_defeated = True\n",
        'battle task events',
    )

    text = replace_once(
        text,
        "                                result_frames = [\n"
        "                                    battle_end_frame(),\n"
        "                                    map_object_remove_frame(battle_state.monster_id),\n"
        "                                ]\n",
        "                                result_frames = [\n"
        "                                    battle_end_frame(),\n"
        "                                    map_object_remove_frame(battle_state.monster_id),\n"
        "                                    *task_frames,\n"
        "                                ]\n",
        'send battle task refresh frames',
    )

    SERVER.write_text(text, encoding='utf-8')
    print('task server integration patch applied')


if __name__ == '__main__':
    main()
