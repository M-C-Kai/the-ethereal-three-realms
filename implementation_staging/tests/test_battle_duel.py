"""统一测试：战斗系统双人即时对决（切磋/PK 的 PVP 接入）。"""
from __future__ import annotations

import unittest

from app.context import SystemContext
from protocol import decode_frame, integer
from systems.battle.handler import BattleSystem
from systems.role.service import default_role

import server as server_module
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def make_role(role_id: int, name: str, attack: int) -> dict:
    settings = server_module.Settings.load(server_module.Path(ROOT) / 'config.json')
    role = default_role(settings)
    role['id'] = role_id
    role['name'] = name
    role['level'] = 10
    role['stats'] = [attack, 5, 10, 10, 10]
    role['items'] = []
    return role


class DuelEngineTests(unittest.TestCase):
    def setUp(self):
        self.settings = server_module.Settings.load(server_module.Path(ROOT) / 'config.json')
        self.pushed: dict[int, list] = {}
        self.roles = {
            10001: make_role(10001, '甲', attack=30),
            10002: make_role(10002, '乙', attack=20),
        }
        self.system = BattleSystem(
            self.settings,
            push_to_role=lambda role_id, frames: self.pushed.setdefault(int(role_id), []).extend(frames),
            online_role_ids=lambda: {10001, 10002},
            find_role=lambda role_id: self.roles.get(int(role_id)),
        )
        self.alice_ctx = SystemContext(username='甲', active_role=self.roles[10001], session={})
        self.bob_ctx = SystemContext(username='乙', active_role=self.roles[10002], session={})

    def _ids(self, role_id):
        return [decode_frame(frame)[0] for frame in self.pushed.get(role_id, [])]

    def test_start_duel_pushes_battle_entry_to_both_sides(self):
        frames = self.system.start_duel(self.roles[10001], self.roles[10002], kind='切磋')
        self.assertTrue(frames)  # 乙（应答方）的进入帧
        self.assertIn(1040, self._ids(10001))  # 甲（挑战方）收到推送
        self.assertIn(1048, self._ids(10001))
        self.assertIs(self.system.duels[10001], self.system.duels[10002])

    def test_start_duel_rejects_when_either_side_busy(self):
        self.assertTrue(self.system.start_duel(self.roles[10001], self.roles[10002]))
        self.assertIsNone(self.system.start_duel(self.roles[10001], self.roles[10002]))

    def test_duel_round_applies_damage_to_both_sides(self):
        self.system.start_duel(self.roles[10001], self.roles[10002])
        self.pushed.clear()
        result = self.system.handle(self.alice_ctx, 1041, [integer(1)])
        message_ids = [decode_frame(frame)[0] for frame in result.frames]
        self.assertIn(1042, message_ids)  # 攻击 + 反击动作
        self.assertIn(1040, message_ids)  # 播放推进帧
        duel = self.system.duels[10001]
        self.assertEqual(duel.round, 1)
        self.assertLess(duel.hp[10002], duel.stats[10002].max_hp)  # 乙被攻击
        self.assertLess(duel.hp[10001], duel.stats[10001].max_hp)  # 甲被反击
        # 乙同样收到同一回合的 1042
        self.assertIn(1042, self._ids(10002))

    def test_duel_ends_when_opponent_dies(self):
        self.system.start_duel(self.roles[10001], self.roles[10002])
        duel = self.system.duels[10001]
        duel.hp[10002] = 1  # 下一击必倒
        self.pushed.clear()
        result = self.system.handle(self.alice_ctx, 1041, [integer(1)])
        message_ids = [decode_frame(frame)[0] for frame in result.frames]
        self.assertIn(1040, message_ids)  # 1040/4 结束帧
        self.assertEqual(self.system.duels, {})
        self.assertIn(1049, self._ids(10002))  # 乙收到落败提示

    def test_escape_forfeits_duel(self):
        self.system.start_duel(self.roles[10001], self.roles[10002])
        self.pushed.clear()
        result = self.system.handle(self.bob_ctx, 1041, [integer(6)])
        message_ids = [decode_frame(frame)[0] for frame in result.frames]
        self.assertIn(1041, message_ids)  # 逃跑动画帧
        self.assertIn(1040, message_ids)  # 结束帧
        self.assertIn(1049, self._ids(10001))
        self.assertEqual(self.system.duels, {})

    def test_abandon_duels_on_disconnect(self):
        self.system.start_duel(self.roles[10001], self.roles[10002])
        abandoned = self.system.abandon_duels(10001)
        self.assertIsNotNone(abandoned)
        peer_id, frames = abandoned
        self.assertEqual(peer_id, 10002)
        self.assertEqual(self.system.duels, {})
        self.assertEqual([decode_frame(f)[0] for f in frames][0], 1040)


if __name__ == '__main__':
    unittest.main()
