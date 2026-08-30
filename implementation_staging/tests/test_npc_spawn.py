import unittest
from pathlib import Path

import server
from server import Settings, map_npc_frames, map_enter_frames

REPO_ROOT = Path(__file__).resolve().parent.parent
CONFIG = REPO_ROOT / "config.json"
NPC_CATALOG = REPO_ROOT / "data" / "npcs.json"


class NpcSpawnTests(unittest.TestCase):
    def setUp(self):
        self.settings = Settings.load(CONFIG)

    def test_config_is_npc_baseline(self):
        self.assertTrue(self.settings.npc_enabled)
        self.assertEqual(len(self.settings.npcs), 3)
        ids = [n["id"] for n in self.settings.npcs]
        self.assertEqual(ids, [1900002, 1900003, 1900004])

    def test_npc_catalog_supplements_models_without_touching_config(self):
        by_id = {n["id"]: n for n in self.settings.npcs}
        expected = {
            1900002: (90000, -2010000),
            1900003: (90010, -2009990),
            1900004: (90020, -2009980),
        }
        for npc_id, (dat_id, model) in expected.items():
            self.assertEqual(by_id[npc_id]["dat_id"], dat_id)
            self.assertEqual(by_id[npc_id]["model"], model)
        models = {n["model"] for n in self.settings.npcs}
        self.assertEqual(len(models), 3)

    def test_map_npc_frames_only_on_map_58(self):
        self.settings.map_id = 58
        self.assertEqual(len(map_npc_frames(self.settings)), 3)
        self.settings.map_id = 57
        self.assertEqual(map_npc_frames(self.settings), [])
        self.settings.map_id = 58
        self.settings.npc_enabled = False
        self.assertEqual(map_npc_frames(self.settings), [])

    def test_map_enter_frames_includes_npc_frames_on_map_58(self):
        self.settings.map_id = 58
        frames = map_enter_frames(self.settings)
        self.assertGreaterEqual(len(frames), 3 + 1)  # 3 npc + monster (at least)
        self.assertEqual(len(map_npc_frames(self.settings)), 3)


if __name__ == "__main__":
    unittest.main(verbosity=2)
