from pathlib import Path

path = Path('server.py')
text = path.read_text(encoding='utf-8')
old = """    # 1110 field 1/2 are the logical map id used by the client. The patched\n    # APK carries the matching 50000.map.ref alias for the target map.\n    client_map_id = current_map.id\n    world = encode_frame(1110, [\n        integer(0),\n        integer(client_map_id),\n        integer(client_map_id),\n        string(current_map.name),\n    ])\n"""
new = """    # APK main/e stores 1110 fields as: [logical map id, resource map id,\n    # map flags, map name]. Task screens compare m.q() (field 0) with their\n    # route map id before choosing same-map local auto-pathfinding.\n    client_map_id = current_map.id\n    world = encode_frame(1110, [\n        integer(client_map_id),\n        integer(client_map_id),\n        integer(0),\n        string(current_map.name),\n    ])\n"""
if old not in text:
    raise SystemExit('expected notice_and_world 1110 block not found')
path.write_text(text.replace(old, new, 1), encoding='utf-8')
print('patched notice_and_world 1110 field order')
