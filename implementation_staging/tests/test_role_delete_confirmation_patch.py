import tempfile
import unittest
from pathlib import Path

from tools.patch_role_delete_confirmation import patch_role_delete_confirmation


class RoleDeleteConfirmationPatchTests(unittest.TestCase):
    def test_confirmation_is_trimmed_before_exact_comparison(self):
        source = '''.method public final a(ILjava/lang/String;)Z
    .locals 4
    const-string v0, "\\u786e\\u8ba4"

    invoke-virtual {p2, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z
'''
        with tempfile.TemporaryDirectory() as directory:
            smali = Path(directory) / 'smali' / 'pmsj' / 'work' / 'e' / 'cv.smali'
            smali.parent.mkdir(parents=True)
            smali.write_text(source, encoding='utf-8')
            self.assertTrue(patch_role_delete_confirmation(Path(directory)))
            patched = smali.read_text(encoding='utf-8')
        self.assertIn('Local role delete: ignore surrounding input whitespace.', patched)
        self.assertIn('invoke-virtual {p2}, Ljava/lang/String;->trim()Ljava/lang/String;', patched)
        self.assertIn('move-result-object p2', patched)


if __name__ == '__main__':
    unittest.main()
