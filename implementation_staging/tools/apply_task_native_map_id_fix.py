from pathlib import Path
import re

path = Path('server.py')
text = path.read_text(encoding='utf-8')
pattern = re.compile(
    r"(?P<head>    client_map_id = current_map\.id\n"
    r"    world = encode_frame\(1110, \[\n)"
    r"        integer\(0\),\n"
    r"        integer\(client_map_id\),\n"
    r"        integer\(client_map_id\),\n"
    r"(?P<tail>        string\(current_map\.name\),\n"
    r"    \]\)\n)"
)
replacement = (
    r"\g<head>"
    "        integer(client_map_id),\n"
    "        integer(client_map_id),\n"
    "        integer(0),\n"
    r"\g<tail>"
)
new_text, count = pattern.subn(replacement, text, count=1)
if count != 1:
    raise SystemExit(f'expected exactly one notice_and_world 1110 block, found {count}')
path.write_text(new_text, encoding='utf-8')
print('patched notice_and_world 1110 fields to [logical_id, resource_id, flags, name]')
