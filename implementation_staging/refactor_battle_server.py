from __future__ import annotations

import ast
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SERVER_PATH = ROOT / 'server.py'
PETS_PATH = ROOT / 'server_pets.py'
WORKFLOW_PATH = ROOT.parent / '.github' / 'workflows' / 'battle-system.yml'
INTEGRATION_TEST_PATH = ROOT / 'tests' / 'battle' / 'test_integration.py'


BATTLE_IMPORTS = """from battle.encounter import (
    EncounterRequest,
    request_encounter,
    update_player_tile as update_escape_guard_for_movement,
)
from battle.engine import battle_command_target_id
from battle.protocol import (
    battle_action_frame,
    battle_action_show_frame,
    battle_actor_debug_snapshot,
    battle_actor_frame,
    battle_actor_source_model_for_debug,
    battle_defend_frame,
    battle_end_frame,
    battle_escape_frame,
    battle_escape_request_frames,
    battle_move_frame,
    battle_reset_frame,
    battle_reward_popup,
    battle_start_frame,
    format_battle_actor_1048_log,
    is_player_escape_command,
)
from battle.resources import (
    BATTLE_EMPTY_RESOURCE_IDS,
    BATTLE_RESOURCE_ALIASES,
    BATTLE_RESOURCE_MODEL_OFFSET,
    PNG_QUERY_MAIN_CACHE,
    PNG_QUERY_ROLE_CACHE,
    battle_image_frames,
    battle_image_resolve_debug,
    battle_image_resource,
    battle_resource_frames,
    battle_resource_path,
    battle_resource_resolution,
    format_battle_resource_query_log,
)
from battle.rewards import (
    BATTLE_DROP_TEMPLATE_ID,
    BATTLE_EXP_REWARD,
    RewardServices,
    apply_battle_rewards as apply_battle_rewards_core,
)
from battle.service import battle_round_action_frames
from battle.state import (
    CombatStats,
    LocalBattleState,
    should_suppress_guard as should_suppress_escape_retrigger,
)

"""


REMOVE_DEFINITIONS = {
    'CombatStats',
    'LocalBattleState',
    'is_player_escape_command',
    'battle_command_target_id',
    'should_suppress_escape_retrigger',
    'update_escape_guard_for_movement',
    'battle_reset_frame',
    'battle_start_frame',
    'battle_actor_source_model_for_debug',
    'battle_actor_debug_snapshot',
    'format_battle_actor_1048_log',
    'battle_actor_frame',
    'battle_action_frame',
    'battle_defend_frame',
    'battle_round_action_frames',
    'battle_move_frame',
    'battle_action_show_frame',
    'battle_escape_frame',
    'battle_escape_request_frames',
    'battle_end_frame',
    'battle_reward_popup',
    '_battle_role_resource_candidates',
    'battle_resource_resolution',
    'format_battle_resource_query_log',
    'battle_resource_path',
    'battle_resource_frames',
    '_signed_int32',
    'battle_image_resource',
    'battle_image_resolve_debug',
    'battle_image_frames',
}

REMOVE_ASSIGNMENTS = {
    'BATTLE_EXP_REWARD',
    'BATTLE_DROP_TEMPLATE_ID',
    'BATTLE_RESOURCE_MODEL_OFFSET',
    'BATTLE_RESOURCE_ALIASES',
    'BATTLE_EMPTY_RESOURCE_IDS',
    'PNG_QUERY_MAIN_CACHE',
    'PNG_QUERY_ROLE_CACHE',
}


APPLY_REWARDS_WRAPPER = '''def apply_battle_rewards(
    role: dict[str, object],
    experience: int = BATTLE_EXP_REWARD,
    registry: ItemRegistry | None = None,
) -> tuple[dict[str, object] | None, bool]:
    """Delegate battle settlement to the authoritative battle reward module."""
    services = RewardServices(
        role_items=role_items,
        bag_item_count=bag_item_count,
        bag_capacity=bag_capacity,
        apply_one_level=apply_one_level,
        max_role_level=MAX_ROLE_LEVEL,
    )
    return apply_battle_rewards_core(
        role,
        services,
        experience=experience,
        registry=registry,
    )

'''


MAP_INTERACTION_METHOD = '''    async def _handle_map_object_interaction(
        self,
        *,
        username: str,
        active_role: dict[str, object] | None,
        object_id: int,
        object_x: int | None,
        object_y: int | None,
        action: int | None,
        source: str,
        writer: asyncio.StreamWriter,
        cipher: GameCipher | None,
        send_lock: asyncio.Lock,
        battle_state: LocalBattleState,
        npc_dialogue_state: LocalNpcDialogueState,
    ) -> None:
        """Handle map actors and delegate every monster entry to battle.encounter."""
        current_settings = settings_for_role(self.settings, active_role)
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

        if active_role is not None:
            target_settings = apply_portal_transition(self.settings, active_role, object_id)
        else:
            target_settings = None
        if target_settings is not None:
            npc_dialogue_state.clear()
            self.roles.save()
            LOG.info(
                'portal activated user=%r role_id=%d object_id=%d map %d -> %d',
                username,
                int(active_role['id']),
                object_id,
                current_settings.id,
                target_settings.id,
            )
            await self._send(
                writer,
                notice_and_world(self.settings, active_role)[1],
                cipher=cipher,
                lock=send_lock,
            )
            return

        npc = map_npc_for_object_id(current_settings, object_id)
        if npc is not None:
            npc_dialogue_state.select(current_settings.id, npc.id)
            LOG.info(
                'npc interaction user=%r npc_id=%d name=%r source=%s; opening native map dialogue',
                username,
                object_id,
                npc.name,
                source,
            )
            task_frames = (
                self.record_task_event(
                    active_role,
                    'npc_talked',
                    target_id=npc.id,
                    now=time.time(),
                )
                if active_role is not None
                else ()
            )
            await self._send(
                writer,
                *map_npc_dialogue_frames(npc, active_role, self.settings),
                *task_frames,
                cipher=cipher,
                lock=send_lock,
            )
            return

        monster = map_monster_for_object_id(current_settings, object_id)
        if monster is None:
            LOG.info('ignored map object action id=%d map=%d', object_id, current_settings.id)
            return

        role = active_role if active_role is not None else default_role(self.settings)
        encounter_source = 'map_interaction'
        if source == '2031' and 700_001 <= int(object_id) <= 799_999:
            encounter_source = (
                'q_action'
                if object_x is None or object_y is None
                else 'proximity'
            )
        player_tile = (
            int(role.get('map_x', 0)),
            int(role.get('map_y', 0)),
        )
        monster_tile = (
            (int(object_x), int(object_y))
            if object_x is not None and object_y is not None
            else None
        )
        request = EncounterRequest(
            map_id=int(current_settings.id),
            monster_id=int(object_id),
            player_id=int(role['id']),
            player_tile=player_tile,
            monster_tile=monster_tile,
            source=encounter_source,
        )
        decision = request_encounter(
            battle_state,
            request,
            player_stats=combat_stats(role),
            monster_ids=tuple(item.id for item in current_settings.monsters),
        )

        if not decision.start:
            if decision.reason == 'escape_guard':
                LOG.info(
                    'BATTLE_ESCAPE_RETRIGGER_SUPPRESSED user=%r player_id=%d monster_id=%d map_id=%d source=%s',
                    username,
                    int(role['id']),
                    object_id,
                    current_settings.id,
                    request.source,
                )
                await self._send(
                    writer,
                    map_object_interaction_ack_frame(object_id),
                    cipher=cipher,
                    lock=send_lock,
                )
                return
            if decision.reason == 'monster_defeated':
                LOG.info(
                    'suppressed stale monster interaction user=%r monster_id=%d; encounter already settled',
                    username,
                    object_id,
                )
                await self._send(
                    writer,
                    map_object_remove_frame(object_id),
                    cipher=cipher,
                    lock=send_lock,
                )
                return
            LOG.info(
                'ignored duplicate monster interaction user=%r monster_id=%d reason=%s battle_trace=%s',
                username,
                object_id,
                decision.reason,
                battle_state.trace_id,
            )
            return

        LOG.info(
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
            battle_reset_frame(),
            *battle_actor_frames(
                role,
                current_settings,
                trace_id=battle_state.trace_id,
                state=battle_state,
            ),
            battle_start_frame(role, current_settings),
            cipher=cipher,
            lock=send_lock,
        )

'''


INTEGRATION_TEST = '''from __future__ import annotations

import inspect
import unittest

from battle import encounter, protocol, resources, rewards, service, state
import server


class BattleServerIntegrationTests(unittest.TestCase):
    def test_server_exports_authoritative_battle_objects_directly(self):
        self.assertIs(server.LocalBattleState, state.LocalBattleState)
        self.assertIs(server.CombatStats, state.CombatStats)
        self.assertIs(server.should_suppress_escape_retrigger, state.should_suppress_guard)
        self.assertIs(server.update_escape_guard_for_movement, encounter.update_player_tile)
        self.assertIs(server.battle_command_target_id, __import__('battle.engine', fromlist=['battle_command_target_id']).battle_command_target_id)
        self.assertIs(server.battle_round_action_frames, service.battle_round_action_frames)
        self.assertIs(server.battle_reset_frame, protocol.battle_reset_frame)
        self.assertIs(server.battle_actor_frame, protocol.battle_actor_frame)
        self.assertIs(server.battle_escape_frame, protocol.battle_escape_frame)
        self.assertIs(server.battle_resource_frames, resources.battle_resource_frames)
        self.assertIs(server.battle_image_frames, resources.battle_image_frames)
        self.assertEqual(server.BATTLE_EXP_REWARD, rewards.BATTLE_EXP_REWARD)
        self.assertEqual(server.BATTLE_DROP_TEMPLATE_ID, rewards.BATTLE_DROP_TEMPLATE_ID)

    def test_server_map_handler_calls_shared_encounter_entry(self):
        source = inspect.getsource(server.LocalGameServer._handle_map_object_interaction)
        self.assertIn('request_encounter(', source)
        self.assertIn('EncounterRequest(', source)
        self.assertNotIn('battle_state.begin(', source)


if __name__ == '__main__':
    unittest.main()
'''


def _node_start(node: ast.AST) -> int:
    starts = [int(getattr(node, 'lineno'))]
    starts.extend(
        int(decorator.lineno)
        for decorator in getattr(node, 'decorator_list', ())
    )
    return min(starts)


def _assignment_names(node: ast.AST) -> set[str]:
    targets: list[ast.AST] = []
    if isinstance(node, ast.Assign):
        targets = list(node.targets)
    elif isinstance(node, ast.AnnAssign):
        targets = [node.target]
    names: set[str] = set()
    for target in targets:
        if isinstance(target, ast.Name):
            names.add(target.id)
    return names


def _rewrite_server() -> None:
    original = SERVER_PATH.read_text(encoding='utf-8')
    tree = ast.parse(original)
    replacements: list[tuple[int, int, str]] = []

    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if node.name in REMOVE_DEFINITIONS:
                replacements.append((_node_start(node), int(node.end_lineno), ''))
            elif node.name == 'apply_battle_rewards':
                replacements.append((_node_start(node), int(node.end_lineno), APPLY_REWARDS_WRAPPER))
        if _assignment_names(node) & REMOVE_ASSIGNMENTS:
            replacements.append((_node_start(node), int(node.end_lineno), ''))
        if isinstance(node, ast.ClassDef) and node.name == 'LocalGameServer':
            method = next(
                (
                    item
                    for item in node.body
                    if isinstance(item, ast.AsyncFunctionDef)
                    and item.name == '_handle_map_object_interaction'
                ),
                None,
            )
            if method is None:
                raise RuntimeError('LocalGameServer._handle_map_object_interaction not found')
            replacements.append((_node_start(method), int(method.end_lineno), MAP_INTERACTION_METHOD))

    lines = original.splitlines(keepends=True)
    occupied: set[int] = set()
    for start, end, _replacement in replacements:
        overlap = occupied.intersection(range(start, end + 1))
        if overlap:
            raise RuntimeError(f'overlapping rewrite span at line {min(overlap)}')
        occupied.update(range(start, end + 1))

    for start, end, replacement in sorted(replacements, reverse=True):
        replacement_lines = replacement.splitlines(keepends=True)
        if replacement and replacement_lines and not replacement_lines[-1].endswith('\n'):
            replacement_lines[-1] += '\n'
        lines[start - 1:end] = replacement_lines
    rewritten = ''.join(lines)

    if 'from battle.state import (' not in rewritten:
        marker = 'import fuyuan\n\n'
        if marker not in rewritten:
            raise RuntimeError('server import marker not found')
        rewritten = rewritten.replace(marker, marker + BATTLE_IMPORTS, 1)

    rewritten = re.sub(
        r'\n# Protocol 1502 multiplexes two different resource requests\..*?\n(?=# The player sprite)',
        '\n',
        rewritten,
        flags=re.S,
    )
    rewritten = rewritten.replace(
        '# The APK does not contain the authoritative server-side reward table.  Keep\n'
        '# the local trial encounter deterministic, but persist its result through the\n'
        '# same role/inventory records used by the rest of the service.\n',
        '',
    )
    rewritten = rewritten.replace(
        '# 1042 only appends records to the APK\'s battle queue. The following full\n'
        '# 1040/action=2 calls the battle screen\'s i() method and starts playback. The\n'
        '# client then returns the short [action=2, round] acknowledgement after the\n'
        '# complete queue has drained, so the server never guesses sprite timings.\n',
        '# Character creation model/race tables shared by map and battle appearance.\n',
    )

    ast.parse(rewritten)
    SERVER_PATH.write_text(rewritten, encoding='utf-8')


def _rewrite_pets() -> None:
    source = PETS_PATH.read_text(encoding='utf-8')
    source = source.replace('from battle import integration as _battle_integration\n', '')
    source = source.replace(
        '    # Keep battle compatibility inside the battle subsystem, not the pet layer.\n'
        '    _battle_integration.install(_server)\n\n',
        '',
    )
    if '_battle_integration' in source or 'battle.integration' in source:
        raise RuntimeError('server_pets still references battle integration')
    PETS_PATH.write_text(source, encoding='utf-8')


def _rewrite_workflow() -> None:
    source = WORKFLOW_PATH.read_text(encoding='utf-8')
    source = source.replace("      - 'implementation_staging/battle_escape_guard.py'\n", '')
    source = source.replace(
        'run: python -m py_compile battle/*.py battle_escape_guard.py server.py server_pets.py',
        'run: python -m py_compile battle/*.py server.py server_pets.py',
    )
    source = source.replace('Escape guard compatibility tests', 'Escape guard state tests')
    if "test_protocol.py" not in source:
        source += (
            "      - name: Server protocol regression tests\n"
            "        working-directory: implementation_staging\n"
            "        run: python -m unittest discover -s tests -p 'test_protocol.py' -v\n"
        )
    WORKFLOW_PATH.write_text(source, encoding='utf-8')


def main() -> None:
    _rewrite_server()
    _rewrite_pets()
    _rewrite_workflow()
    INTEGRATION_TEST_PATH.write_text(INTEGRATION_TEST, encoding='utf-8')
    (ROOT / 'battle' / 'integration.py').unlink(missing_ok=True)
    (ROOT / 'battle_escape_guard.py').unlink(missing_ok=True)


if __name__ == '__main__':
    main()
