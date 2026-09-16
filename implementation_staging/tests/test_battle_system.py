"""统一测试：战斗系统（状态机、逃跑保护、回合、结算、会话共享）。"""
from __future__ import annotations

import tempfile
import time
import unittest
from pathlib import Path

from app.context import SystemContext
from protocol import decode_frame
from systems.battle.handler import BattleSystem
from systems.battle.service import (
    LocalBattleState, apply_battle_rewards, battle_command_target_id,
    battle_state_for, is_player_escape_command, should_suppress_escape_retrigger,
    update_escape_guard_for_movement,
)
from systems.role.service import RoleStore


ROOT = Path(__file__).resolve().parent.parent


def make_game():
    import server

    settings = server.Settings.load(server.Path(ROOT) / 'config.json')
    return settings, server.LocalGameServer(settings)


class LocalBattleStateTests(unittest.TestCase):
    def test_all_living_monsters_act_in_speed_order(self):
        from systems.battle.protocol import battle_round_action_frames
        state = LocalBattleState()
        state.begin(7, 100, monster_ids=(100, 101, 102))
        state.initiative = {7: (10, 2), 100: (20, 0), 101: (10, 3), 102: (10, 2)}
        frames, ended = battle_round_action_frames(state, 1, target_id=102)
        self.assertEqual([decode_frame(f)[1][1].value for f in frames], [100, 101, 7, 102])
        self.assertEqual(state.player_hp, 70)
        self.assertFalse(ended)

    def test_dead_monster_and_player_do_not_act(self):
        from systems.battle.protocol import battle_round_action_frames
        state = LocalBattleState()
        state.begin(7, 100, monster_ids=(100, 101))
        state.player_attack = 1000
        frames, _ = battle_round_action_frames(state, 1, target_id=100)
        self.assertEqual([decode_frame(f)[1][1].value for f in frames], [7, 101])
        state.begin(7, 100, monster_ids=(100, 101))
        state.player_hp = 1
        state.initiative = {100: (1, 0)}
        frames, _ = battle_round_action_frames(state, 1, target_id=101)
        self.assertEqual([decode_frame(f)[1][1].value for f in frames], [100])

    def test_image_resolution_diagnostic_handles_map_image(self):
        from systems.battle.protocol import battle_image_resolve_debug

        result = battle_image_resolve_debug(60011000)
        self.assertEqual(result['requested_id'], 60011000)

    def test_begin_and_basic_attack(self):
        state = LocalBattleState()
        state.begin(7, 100, player_stats=None, monster_ids=(100, 101))
        self.assertTrue(state.active)
        self.assertEqual(state.monster_ids, (100, 101))
        finished = state.apply_basic_attack(damage=10 ** 6, target_id=100)
        self.assertFalse(finished)
        self.assertEqual(state.monster_hp_for(100), 0)
        state.apply_basic_attack(damage=10 ** 6, target_id=101)
        self.assertTrue(state.all_monsters_defeated())
        state.finish()
        self.assertFalse(state.active)

    def test_escape_guard_stamp_and_timeout(self):
        state = LocalBattleState()
        state.begin(7, 100)
        state.set_escape_guard(58, 100, 7, (6, 6))
        self.assertIsNotNone(state.escape_guard.get('created_at'))
        self.assertTrue(should_suppress_escape_retrigger(state.escape_guard, 58, 100))
        self.assertFalse(should_suppress_escape_retrigger(state.escape_guard, 58, 999))
        # 两秒超时后放行
        state.escape_guard['created_at'] -= 3.0
        self.assertFalse(should_suppress_escape_retrigger(state.escape_guard, 58, 100))
        # 离开半径也会清除
        state.escape_guard['created_at'] = time.monotonic()
        self.assertTrue(update_escape_guard_for_movement(state, 20, 20))
        self.assertIsNone(state.escape_guard)

    def test_escape_command(self):
        self.assertTrue(is_player_escape_command(6))
        self.assertFalse(is_player_escape_command(10))
        state = LocalBattleState()
        state.begin(7, 100, monster_ids=(100, 101))
        state.player_tile = (6, 6)
        self.assertTrue(state.escape())
        self.assertFalse(state.active)
        self.assertIsNotNone(state.escape_guard)

    def test_command_target_validation(self):
        state = LocalBattleState()
        state.begin(7, 100, monster_ids=(100, 101))
        self.assertEqual(battle_command_target_id([1, 1, 0, 0, 101], state), 101)
        self.assertIsNone(battle_command_target_id([1, 1, 0, 0, 999], state))


class BattleSessionTests(unittest.TestCase):
    def test_session_shared_object(self):
        session = {}
        a = battle_state_for(session)
        b = battle_state_for(session)
        self.assertIs(a, b)


class BattleHandlerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        import server

        self.settings = server.Settings.load(server.Path(ROOT) / 'config.json')
        self.settings.role_data_file = str(Path(self.tmp.name) / 'roles.json')
        self.store = RoleStore(self.settings)
        self.role = self.store.create('tester', '测试角色', 0, 0)
        self.game = server.LocalGameServer(self.settings)
        self.system = self.game.battle_system
        self.session = {}

    def tearDown(self):
        self.tmp.cleanup()

    def _context(self):
        return SystemContext(username='tester', active_role=self.role, session=self.session)

    def test_encounter_starts_then_suppresses_after_escape(self):
        map_settings = self.settings.map_registry.require(self.settings.default_map_id)
        result = self.system.handle_monster_encounter(
            username='tester', role=self.role,
            battle_state=battle_state_for(self.session),
            map_settings=map_settings,
            object_id=map_settings.monster.id, object_x=10, object_y=6,
            source='2031',
        )
        message_ids = [decode_frame(frame)[0] for frame in result.frames]
        self.assertIn(1040, message_ids)
        self.assertIn(1048, message_ids)
        # 逃跑后立即再触发应被抑制并回 1010 交互 ack
        state = battle_state_for(self.session)
        state.escape()
        result = self.system.handle_monster_encounter(
            username='tester', role=self.role,
            battle_state=state,
            map_settings=map_settings,
            object_id=map_settings.monster.id, object_x=10, object_y=6,
            source='2031',
        )
        message_id, _ = decode_frame(result.frames[0])
        self.assertEqual(message_id, 1010)

    def test_attack_and_settle_rounds(self):
        from protocol import encode_frame, field_values, short
        map_settings = self.settings.map_registry.require(self.settings.default_map_id)
        monster_id = map_settings.monster.id
        self.system.handle_monster_encounter(
            username='tester', role=self.role,
            battle_state=battle_state_for(self.session),
            map_settings=map_settings,
            object_id=monster_id, object_x=10, object_y=6,
            source='2031',
        )
        state = battle_state_for(self.session)
        # 1041 普攻：命令 1 + 回合 + ... + 目标
        request = [1, 1, 0, 0, monster_id]
        frames = []
        class _F:
            def __init__(self, value):
                self.value = value
                self.type_id = None
        result = self.system.handle(self._context(), 1041, [_F(v) for v in request])
        self.assertTrue(result.handled)
        state.phase = 'round_ack'
        # 1040 action=2 ack（怪物血量归零）
        state.apply_basic_attack(damage=10 ** 6, target_id=monster_id)
        result = self.system.handle(self._context(), 1040, [_F(2), _F(1)])
        if not state.all_monsters_defeated():
            self.assertEqual(result.frames, ())
            self.assertTrue(state.active)
        for actor in state.monster_ids:
            state.apply_basic_attack(damage=10 ** 6, target_id=actor)
        state.phase = 'round_ack'
        result = self.system.handle(self._context(), 1040, [_F(2), _F(2)])
        self.assertTrue(result.handled)
        message_ids = [decode_frame(frame)[0] for frame in result.frames]
        self.assertIn(1040, message_ids)   # battle_end
        self.assertIn(1008, message_ids)   # 掉落物品
        self.assertFalse(state.active)
        self.assertTrue(state.monster_defeated)

    def test_resource_query_unsupported_action(self):
        class _F:
            def __init__(self, value):
                self.value = value
                self.type_id = None
        result = self.system.handle(self._context(), 1502, [_F(9), _F(1), _F(123)])
        self.assertTrue(result.handled)
        self.assertEqual(result.frames, ())

    def test_map_image_query_completes_without_disconnect_exception(self):
        class _F:
            def __init__(self, value):
                self.value = value
                self.type_id = None

        result = self.system.handle(self._context(), 1502,
                                    [_F(0), _F(1), _F(60011000)])
        self.assertTrue(result.handled)
        self.assertEqual([decode_frame(frame)[0] for frame in result.frames],
                         [1501, 1501, 1502])


if __name__ == '__main__':
    unittest.main()
