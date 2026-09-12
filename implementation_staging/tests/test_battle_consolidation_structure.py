from __future__ import annotations

import ast
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SERVER_PATH = ROOT / 'server.py'
PETS_PATH = ROOT / 'server_pets.py'


class BattleConsolidationStructureTests(unittest.TestCase):
    def server_tree(self) -> ast.Module:
        return ast.parse(SERVER_PATH.read_text(encoding='utf-8'))

    def test_server_no_longer_defines_battle_domain_or_protocol_duplicates(self):
        forbidden = {
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
        defined = {
            node.name
            for node in self.server_tree().body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
        }
        self.assertEqual(sorted(forbidden & defined), [])

    def test_server_no_longer_owns_battle_constants(self):
        forbidden = {
            'BATTLE_EXP_REWARD',
            'BATTLE_DROP_TEMPLATE_ID',
            'BATTLE_RESOURCE_MODEL_OFFSET',
            'BATTLE_RESOURCE_ALIASES',
            'BATTLE_EMPTY_RESOURCE_IDS',
            'PNG_QUERY_MAIN_CACHE',
            'PNG_QUERY_ROLE_CACHE',
        }
        assigned: set[str] = set()
        for node in self.server_tree().body:
            targets = []
            if isinstance(node, ast.Assign):
                targets = node.targets
            elif isinstance(node, ast.AnnAssign):
                targets = [node.target]
            for target in targets:
                if isinstance(target, ast.Name):
                    assigned.add(target.id)
        self.assertEqual(sorted(forbidden & assigned), [])

    def test_battle_package_is_imported_directly_by_server(self):
        imported_modules: set[str] = set()
        for node in self.server_tree().body:
            if isinstance(node, ast.ImportFrom) and node.module:
                imported_modules.add(node.module)
        self.assertTrue({'battle.state', 'battle.protocol', 'battle.resources', 'battle.encounter', 'battle.rewards'} <= imported_modules)

    def test_legacy_battle_monkeypatch_and_escape_shim_are_gone(self):
        self.assertFalse((ROOT / 'battle' / 'integration.py').exists())
        self.assertFalse((ROOT / 'battle_escape_guard.py').exists())
        pets_source = PETS_PATH.read_text(encoding='utf-8')
        self.assertNotIn('_battle_integration', pets_source)
        self.assertNotIn('battle.integration', pets_source)


if __name__ == '__main__':
    unittest.main()
