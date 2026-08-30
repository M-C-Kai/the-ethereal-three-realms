from __future__ import annotations

import sys
import unittest
from pathlib import Path


TOOLS_DIR = Path(__file__).resolve().parents[1] / 'tools'
sys.path.insert(0, str(TOOLS_DIR))

from patch_npc_direction import patch_e_smali  # noqa: E402


STALE_PATCHED_Q = """\
.method private static Q(Lpmsj/work/main/w;)V
    .registers 14
    const/4 v0, 0x0
    invoke-virtual {p0, v0}, Lpmsj/work/main/w;->a(I)B
    move-result v0
    packed-switch v0, :pswitch_data_0
    :cond_0
    return-void
    :pswitch_0
    goto :cond_0
    :pswitch_dir
    const/4 v0, 0x1
    invoke-virtual {p0, v0}, Lpmsj/work/main/w;->b(I)S
    move-result v0
    const/4 v2, 0x0
    :goto_dir
    if-ge v2, v0, :cond_8
    add-int/lit8 v2, v2, 0x1
    goto :goto_dir
    nop
    :pswitch_data_0
    .packed-switch 0x0
        :pswitch_0
        :pswitch_dir
    .end packed-switch
.end method
"""


class NpcDirectionPatchTests(unittest.TestCase):
    def test_existing_stale_handler_is_upgraded_to_current_wire_layout(self):
        patched = patch_e_smali(STALE_PATCHED_Q)
        handler = patched[patched.index('    :pswitch_dir'):patched.index('    :pswitch_data_0')]

        self.assertIn('Lpmsj/work/main/w;->a(I)B', handler)
        self.assertNotIn('Lpmsj/work/main/w;->b(I)S', handler)
        self.assertIn('if-ge v2, v0, :dir_done', handler)
        self.assertIn(':dir_done\n    return-void', handler)
        self.assertEqual(patched.count('        :pswitch_dir'), 1)


if __name__ == '__main__':
    unittest.main(verbosity=2)
