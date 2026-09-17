"""临时校验：1303 装备行字段 + 图标图集存在性。用完即删。"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import server as server_module  # noqa: E402
from protocol import decode_frame  # noqa: E402
from systems.social.protocol import player_view_frame  # noqa: E402

images = {
    int(row['image_id'])
    for row in json.loads(
        (ROOT / 'build_artifacts' / 'legacy' / 'work' / 'all-images.json').read_text(encoding='utf-8')
    )
}
items = json.loads((ROOT / 'data' / 'catalog' / 'items.json').read_text(encoding='utf-8'))['items']
codes = sorted({int(item.get('icon_code', 0)) for item in items})
missing = [
    code for code in codes
    if (3_002_424 + (code // 100 % 100) * 10_000) not in images
]
print('catalog icon codes:', codes)
print('icon codes whose atlas is absent in APK images:', missing)

settings = server_module.Settings.load(ROOT / 'config.json')
data = json.loads((ROOT / 'data' / 'roles.json').read_text(encoding='utf-8'))
role = [r for r in data['accounts']['5201314'] if int(r['id']) == 10085][0]
message_id, fields = decode_frame(player_view_frame(settings, role, 1010085))
print('message', message_id, 'equips', int(fields[4].value))
for index in range(int(fields[4].value)):
    base = 5 + index * 6
    row = [(fields[base + offset].type_id, fields[base + offset].value) for offset in range(6)]
    code = int(row[5][1])
    atlas = 3_002_424 + (code // 100 % 100) * 10_000
    print('  row', row, 'atlas', atlas, 'exists', atlas in images)