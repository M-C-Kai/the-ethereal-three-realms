import unittest
from pathlib import Path

import server
from server import Settings, map_npc_frames, map_enter_frames, settings_for_map

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
            1900002: (95750, -2004250),
            1900003: (96010, -2003990),
            1900004: (95520, -2004480),
        }
        for npc_id, (dat_id, model) in expected.items():
            self.assertEqual(by_id[npc_id]["dat_id"], dat_id)
            self.assertEqual(by_id[npc_id]["model"], model)
        models = {n["model"] for n in self.settings.npcs}
        self.assertEqual(len(models), 3)

    def test_map_npc_frames_only_on_map_58(self):
        self.assertEqual(len(map_npc_frames(settings_for_map(self.settings, 58))), 3)
        self.assertEqual(map_npc_frames(settings_for_map(self.settings, 50000)), [])
        kunlun = settings_for_map(self.settings, 60001)
        self.assertEqual([npc.id for npc in kunlun.npcs], [1900101])
        self.assertEqual(len(map_npc_frames(kunlun)), 1)
        self.assertIsNone(kunlun.monster)

    def test_map_enter_frames_includes_npc_frames_on_map_58(self):
        changan = settings_for_map(self.settings, 58)
        frames = map_enter_frames(changan)
        self.assertGreaterEqual(len(frames), 3 + 1)  # 3 npc + monster (at least)
        self.assertEqual(len(map_npc_frames(changan)), 3)


if __name__ == "__main__":
    unittest.main(verbosity=2)
