import json
import shutil
import struct
import sys
import zipfile
import zlib
from pathlib import Path


PNG_SIG = b'\x89PNG\r\n\x1a\n'
IEND = b'\x00\x00\x00\x00IEND\xaeB\x60\x82'


def be16(data, off=0):
    return struct.unpack_from('>H', data, off)[0]


def be32(data, off=0):
    return struct.unpack_from('>I', data, off)[0]


def rebuild_png(blob, offset):
    pos = offset
    group_count, group_index = blob[pos], blob[pos + 1]
    pos += 2
    if group_count:
        pos += (group_count - group_index - 1) * 2
    header = blob[pos:pos + 22]
    if len(header) != 22:
        raise ValueError('truncated image header')
    pos += 22
    width, height = be16(header, 0), be16(header, 2)
    bit_depth, transparent_index = header[4], header[5]
    plte_crc, trns_crc, ihdr_crc = be32(header, 6), be32(header, 10), be32(header, 14)
    palette_len, idat_total_len = be16(header, 18), be16(header, 20)
    if group_count:
        pos += group_index * palette_len
        palette565 = blob[pos:pos + palette_len]
        pos += palette_len
        pos += (group_count - group_index - 1) * palette_len
        idat_and_crc = blob[pos:pos + idat_total_len]
    else:
        palette565 = blob[pos:pos + palette_len]
        pos += palette_len
        idat_and_crc = blob[pos:pos + idat_total_len]
    if len(palette565) != palette_len or len(idat_and_crc) != idat_total_len:
        raise ValueError('truncated palette or IDAT')
    palette = bytearray()
    for i in range(0, palette_len, 2):
        rgb565 = be16(palette565, i)
        signed565 = rgb565 if rgb565 < 0x8000 else rgb565 - 0x10000
        palette.extend((
            int(((signed565 >> 11) * 255) / 31) & 0xff,
            (((rgb565 >> 5) & 63) * 255) // 63,
            ((rgb565 & 31) * 255) // 31,
        ))
    chunks = [
        PNG_SIG,
        struct.pack('>I4sIIBBBBBI', 13, b'IHDR', width, height, bit_depth, 3, 0, 0, 0, ihdr_crc),
        struct.pack('>I4s', len(palette), b'PLTE') + palette + struct.pack('>I', plte_crc),
    ]
    if transparent_index != 0xFF:
        alpha = bytearray(b'\xff' * (palette_len // 2))
        if transparent_index < len(alpha):
            alpha[transparent_index] = 0
        trns_crc = zlib.crc32(b'tRNS' + alpha) & 0xffffffff
        chunks.append(struct.pack('>I4s', len(alpha), b'tRNS') + alpha + struct.pack('>I', trns_crc))
    chunks.append(struct.pack('>I4s', idat_total_len - 4, b'IDAT') + idat_and_crc)
    chunks.append(IEND)
    return b''.join(chunks), width, height


def main(apk_path, output_dir):
    out = Path(output_dir)
    rebuilt = out / 'rebuilt'
    regular = out / 'regular_png'
    rebuilt.mkdir(parents=True, exist_ok=True)
    regular.mkdir(parents=True, exist_ok=True)
    report = {'rebuilt': 0, 'regular_png': 0, 'errors': []}
    with zipfile.ZipFile(apk_path) as z:
        index = z.read('assets/res/images/images.o')
        index_len = be16(index, 0)
        records = index[2:2 + index_len]
        containers = {}
        for i in range(0, len(records), 7):
            rec = records[i:i + 7]
            if len(rec) != 7:
                continue
            image_id, container_no, offset = be32(rec, 0), rec[4], be16(rec, 5)
            try:
                if container_no not in containers:
                    containers[container_no] = z.read(f'assets/res/images/png{container_no}.p')
                png, width, height = rebuild_png(containers[container_no], offset)
                target = rebuilt / f'{image_id:07d}_{width}x{height}.png'
                target.write_bytes(png)
                report['rebuilt'] += 1
            except Exception as exc:
                report['errors'].append({'id': image_id, 'container': container_no, 'offset': offset, 'error': str(exc)})
        for info in z.infolist():
            if info.filename.startswith(('assets/', 'res/')) and info.filename.lower().endswith('.png'):
                safe_name = info.filename.replace('/', '__')
                (regular / safe_name).write_bytes(z.read(info.filename))
                report['regular_png'] += 1
    (out / 'extraction_report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
