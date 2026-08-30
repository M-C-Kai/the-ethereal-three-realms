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
        self.assertEqual(len(self.settings.npcs), 7)
        ids = [n["id"] for n in self.settings.npcs]
        self.assertEqual(
            ids, [1900002, 1900003, 1900004, 1900005, 1900006, 1900007, 1900008]
        )

    def test_npc_catalog_supplements_models_without_touching_config(self):
        by_id = {n["id"]: n for n in self.settings.npcs}
        # 柴荣 comes from config.json (mirrored 96031 / model -2003969), not the catalog.
        self.assertEqual(by_id[1900005]["dat_id"], 96031)
        self.assertEqual(by_id[1900005]["model"], -2003969)
        # The other six get distinct sprites from data/npcs.json overrides.
        expected = {
            1900002: (90000, -2010000),
            1900003: (90010, -2009990),
            1900004: (90020, -2009980),
            1900006: (90040, -2009960),
            1900007: (90050, -2009950),
            1900008: (90060, -2009940),
        }
        for npc_id, (dat_id, model) in expected.items():
            self.assertEqual(by_id[npc_id]["dat_id"], dat_id)
            self.assertEqual(by_id[npc_id]["model"], model)
        # Every NPC must render with its own sprite (no duplicate models).
        models = {n["model"] for n in self.settings.npcs}
        self.assertEqual(len(models), 7)

    def test_map_npc_frames_only_on_map_58(self):
        self.settings.map_id = 58
        self.assertEqual(len(map_npc_frames(self.settings)), 7)
        self.settings.map_id = 57
        self.assertEqual(map_npc_frames(self.settings), [])
        self.settings.map_id = 58
        self.settings.npc_enabled = False
        self.assertEqual(map_npc_frames(self.settings), [])

    def test_map_enter_frames_includes_npc_frames_on_map_58(self):
        self.settings.map_id = 58
        frames = map_enter_frames(self.settings)
        # map-enter sends the monster/portal frames plus one 1126 frame per NPC.
        self.assertGreaterEqual(len(frames), 7 + 1)  # 7 npc + monster (at least)
        self.assertEqual(len(map_npc_frames(self.settings)), 7)


if __name__ == "__main__":
    unittest.main(verbosity=2)
