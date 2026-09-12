import tempfile
import unittest
from pathlib import Path

from tools.patch_login_failure_ui import patch_login_flow


class LoginFailureUiPatchTests(unittest.TestCase):
    def test_failure_restores_input_without_changing_success_transition(self):
        failure_smali = """    :pswitch_11
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v4

    const-string v5, "wrong password"
"""
        request_smali = """.method public static a(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)V
    .locals 5
    const/4 v4, 0x1
"""
        with tempfile.TemporaryDirectory() as directory:
            main_dir = Path(directory) / 'smali' / 'pmsj' / 'work' / 'main'
            main_dir.mkdir(parents=True)
            (main_dir / 'e.smali').write_text(failure_smali, encoding='utf-8')
            (main_dir / 'c.smali').write_text(request_smali, encoding='utf-8')
            self.assertTrue(patch_login_flow(Path(directory)))
            failure_patched = (main_dir / 'e.smali').read_text(encoding='utf-8')
            request_patched = (main_dir / 'c.smali').read_text(encoding='utf-8')
        self.assertIn('Local login: return an authentication failure', failure_patched)
        self.assertIn('const/16 v5, 0x136', failure_patched)
        self.assertEqual(request_patched, request_smali)


if __name__ == '__main__':
    unittest.main()
