from __future__ import annotations

import unittest

from tools.patch_equipment_details import (
    CATEGORY_MARKER,
    VIEW_MARKER,
    patch_full_equipment_categories,
    patch_self_equipment_view,
)


class EquipmentDetailPatchTests(unittest.TestCase):
    def test_self_equipment_view_uses_native_tooltip(self):
        source = """.method public final b(Ljava/lang/String;)Z
    .locals 5

    invoke-direct {p0}, Lpmsj/work/e/af;->i()Z

    move-result v1

    if-eqz v1, :cond_1

    iget v0, v0, Lpmsj/work/b/g;->e:I

    invoke-static {v0}, Lpmsj/work/main/e;->c(I)V

    :cond_1
    return v2
.end method
"""
        patched = patch_self_equipment_view(source)
        self.assertIn(VIEW_MARKER, patched)
        self.assertIn(
            "Lpmsj/work/e/b;->a(Lpmsj/work/d/l;Lpmsj/work/b/j;Lpmsj/work/d/c;II)V",
            patched,
        )
        self.assertNotIn("Lpmsj/work/main/e;->c(I)V", patched)
        self.assertEqual(patch_self_equipment_view(patched), patched)

    def test_equipment_categories_extend_through_slot_14(self):
        source = """.method public final c()Z
    .locals 2

    if-lez v0, :cond_0

    const/16 v1, 0xb

    if-ge v0, v1, :cond_0

    const/4 v0, 0x1

    :cond_0
    return v0
.end method
"""
        patched = patch_full_equipment_categories(source)
        self.assertIn(CATEGORY_MARKER, patched)
        self.assertIn("const/16 v1, 0xf", patched)
        self.assertNotIn("const/16 v1, 0xb", patched)
        self.assertEqual(patch_full_equipment_categories(patched), patched)


if __name__ == "__main__":
    unittest.main()
