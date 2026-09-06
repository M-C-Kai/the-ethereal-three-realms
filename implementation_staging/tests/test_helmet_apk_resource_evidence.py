import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAPPING = ROOT / 'data/catalog/helmet_appearance_mapping.json'
AUDIT = ROOT / 'references/helmet-appearance-audit/manifest.json'

class HelmetApkResourceEvidenceTests(unittest.TestCase):
    def test_real_apk_icon_strip_is_recorded(self):
        data = json.loads(MAPPING.read_text(encoding='utf-8'))
        self.assertEqual(data['apk_sha256'], '34348c4ac16108222871203c46faabc1e6e5383c455e39b871c7666505da60b5')
        self.assertEqual(data['icon_resource']['image_id'], 3012424)
        self.assertEqual(data['icon_resource']['icon_to_frame'], {str(code): code - 100 for code in range(100, 110)})

    def test_only_packaged_property20_candidate_is_21003(self):
        data = json.loads(AUDIT.read_text(encoding='utf-8'))
        self.assertEqual(data['property20_images_in_apk'], [{'property20': 3, 'image_id': 21003, 'dimensions': [166, 101]}])
        self.assertEqual(data['confirmed_icon_to_property20'], {})

if __name__ == '__main__':
    unittest.main()
