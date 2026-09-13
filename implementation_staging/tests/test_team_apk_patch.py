"""Team roster downlinks must not navigate away from the active map UI."""
from __future__ import annotations

import unittest

from tools.patch_team_roster_ui import patch_team_roster_ui


class TeamApkPatchTests(unittest.TestCase):
    def test_removes_only_action_zero_roster_navigation(self):
        source = '''
.method private static aj(Lpmsj/work/main/w;)V
    :pswitch_1
    sget-object v0, Lpmsj/work/b/aa;->a:Ljava/util/Vector;
    invoke-virtual {v0, v1}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;
    const/16 v0, 0x5c
    invoke-static {v0}, Lpmsj/work/d/n;->h(I)V
    aget-object v0, v1, v4
    :pswitch_2
    const/16 v0, 0x51
    invoke-static {v0}, Lpmsj/work/d/n;->h(I)V
.end method
'''
        patched = patch_team_roster_ui(source)
        self.assertIn('addElement(Ljava/lang/Object;)V', patched)
        self.assertNotIn('const/16 v0, 0x5c', patched)
        self.assertIn('const/16 v0, 0x51', patched)
        self.assertEqual(patch_team_roster_ui(patched), patched)
