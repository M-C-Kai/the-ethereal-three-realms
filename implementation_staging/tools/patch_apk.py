from __future__ import annotations

import argparse
import struct
import zipfile
from pathlib import Path


CHANNEL_ENTRY = 'assets/res/channel.o'


def packed_string(value: str) -> bytes:
    raw = value.encode('utf-8')
    if len(raw) > 0xFFFF:
        raise ValueError('configuration string is too long')
    return struct.pack('>H', len(raw)) + raw


def channel_blob(host: str, port: int, channel: int, base_url: str | None) -> bytes:
    if not 1 <= port <= 65535:
        raise ValueError('port must be between 1 and 65535')
    if not 0 <= channel <= 65535:
        raise ValueError('channel must be between 0 and 65535')
    url = base_url or f'http://{host}:{port}'
    return packed_string(url) + struct.pack('>H', channel) + packed_string(f'{host}:{port}')


def clone_info(info: zipfile.ZipInfo) -> zipfile.ZipInfo:
    cloned = zipfile.ZipInfo(info.filename, info.date_time)
    cloned.compress_type = info.compress_type
    cloned.comment = info.comment
    cloned.extra = info.extra
    cloned.internal_attr = info.internal_attr
    cloned.external_attr = info.external_attr
    cloned.create_system = info.create_system
    cloned.flag_bits = info.flag_bits
    return cloned


def patch_apk(source: Path, destination: Path, host: str, port: int, channel: int, base_url: str | None) -> None:
    replacement = channel_blob(host, port, channel, base_url)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(source, 'r') as src, zipfile.ZipFile(destination, 'w', allowZip64=True) as dst:
        names = set(src.namelist())
        if CHANNEL_ENTRY not in names:
            raise KeyError(f'{CHANNEL_ENTRY} is missing from the APK')
        for info in src.infolist():
            if info.filename.upper().startswith('META-INF/'):
                continue
            data = replacement if info.filename == CHANNEL_ENTRY else src.read(info.filename)
            dst.writestr(clone_info(info), data)
    print(f'patched {CHANNEL_ENTRY} -> {host}:{port}, channel={channel}')
    print(f'unsigned APK: {destination}')


def main() -> None:
    parser = argparse.ArgumentParser(description='Patch the local login endpoint in the APK')
    parser.add_argument('source', type=Path)
    parser.add_argument('destination', type=Path)
    parser.add_argument('--host', required=True)
    parser.add_argument('--port', type=int, default=6805)
    parser.add_argument('--channel', type=int, default=15)
    parser.add_argument('--base-url')
    args = parser.parse_args()
    patch_apk(args.source, args.destination, args.host, args.port, args.channel, args.base_url)


if __name__ == '__main__':
    main()
