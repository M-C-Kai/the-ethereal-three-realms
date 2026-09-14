from __future__ import annotations

import argparse
import io
import json
import re
import struct
import sys
import zipfile
import zlib
from pathlib import Path
from typing import Iterable

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
PNG_IEND = b"\x00\x00\x00\x00IEND\xaeB`\x82"
PNG_CONTAINER_RE = re.compile(r"^assets/res/images/png(\d+)\.p$")
MAP_ID = 60011
MAP_DIR = ROOT / "maps" / str(MAP_ID)
ASSET_BUNDLE = MAP_DIR / "60011_apk_assets.zip"


class ImagePackError(ValueError):
    pass


def _read_png_chunks(data: bytes) -> list[tuple[bytes, bytes]]:
    if not data.startswith(PNG_SIGNATURE):
        raise ImagePackError("source is not a PNG")
    chunks: list[tuple[bytes, bytes]] = []
    offset = len(PNG_SIGNATURE)
    while offset + 12 <= len(data):
        length = struct.unpack_from(">I", data, offset)[0]
        kind = data[offset + 4:offset + 8]
        payload_start = offset + 8
        payload_end = payload_start + length
        crc_end = payload_end + 4
        if crc_end > len(data):
            raise ImagePackError("PNG chunk is truncated")
        chunks.append((kind, data[payload_start:payload_end]))
        offset = crc_end
        if kind == b"IEND":
            break
    return chunks


def _rgb888_to_565(r: int, g: int, b: int) -> int:
    return (
        ((r * 31 + 127) // 255) << 11
        | ((g * 63 + 127) // 255) << 5
        | ((b * 31 + 127) // 255)
    )


def _rgb565_to_bytes(value: int) -> bytes:
    signed565 = value if value < 0x8000 else value - 0x10000
    return bytes((
        int(((signed565 >> 11) * 255) / 31) & 0xFF,
        ((value >> 5) & 63) * 255 // 63,
        (value & 31) * 255 // 31,
    ))


def pack_png_for_client_bytes(png_data: bytes) -> bytes:
    source = Image.open(io.BytesIO(png_data)).convert("RGB")
    quantized = source.quantize(colors=256, method=Image.Quantize.MEDIANCUT)
    with io.BytesIO() as buffer:
        quantized.save(buffer, format="PNG", optimize=False, bits=8)
        indexed_png = buffer.getvalue()

    chunks = _read_png_chunks(indexed_png)
    ihdr = next((payload for kind, payload in chunks if kind == b"IHDR"), None)
    plte = next((payload for kind, payload in chunks if kind == b"PLTE"), None)
    idat_parts = [payload for kind, payload in chunks if kind == b"IDAT"]
    if ihdr is None or plte is None or not idat_parts:
        raise ImagePackError("quantized PNG is missing IHDR/PLTE/IDAT")
    if len(ihdr) != 13 or ihdr[9] != 3:
        raise ImagePackError("quantized PNG is not indexed-color")

    width, height = struct.unpack_from(">II", ihdr, 0)
    if not 1 <= width <= 0xFFFF or not 1 <= height <= 0xFFFF:
        raise ImagePackError("image dimensions exceed packed header")

    palette565 = bytearray()
    rebuilt_palette = bytearray()
    for offset in range(0, len(plte), 3):
        rgb = plte[offset:offset + 3]
        if len(rgb) != 3:
            break
        value = _rgb888_to_565(*rgb)
        palette565.extend(struct.pack(">H", value))
        rebuilt_palette.extend(_rgb565_to_bytes(value))

    idat = b"".join(idat_parts)
    idat_and_crc = idat + struct.pack(">I", zlib.crc32(b"IDAT" + idat) & 0xFFFFFFFF)
    if len(idat_and_crc) > 0xFFFF:
        raise ImagePackError(f"packed IDAT is too large: {len(idat_and_crc)} bytes")

    header = struct.pack(
        ">HHBBIIIHH",
        width,
        height,
        ihdr[8],
        255,
        zlib.crc32(b"PLTE" + rebuilt_palette) & 0xFFFFFFFF,
        0,
        zlib.crc32(b"IHDR" + ihdr) & 0xFFFFFFFF,
        len(palette565),
        len(idat_and_crc),
    )
    return b"\x00\x00" + header + bytes(palette565) + idat_and_crc


def rebuild_client_png(blob: bytes, offset: int = 0) -> bytes:
    position = offset
    if position + 24 > len(blob):
        raise ImagePackError("packed image is truncated")
    group_count, group_index = blob[position], blob[position + 1]
    position += 2
    if group_count:
        position += (group_count - group_index - 1) * 2

    header = blob[position:position + 22]
    position += 22
    width, height = struct.unpack_from(">HH", header, 0)
    bit_depth, transparent_index = header[4], header[5]
    palette_crc, _trns_crc, ihdr_crc = struct.unpack_from(">III", header, 6)
    palette_length, idat_total_length = struct.unpack_from(">HH", header, 18)

    if group_count:
        position += group_index * palette_length
        palette565 = blob[position:position + palette_length]
        position += palette_length
        position += (group_count - group_index - 1) * palette_length
    else:
        palette565 = blob[position:position + palette_length]
        position += palette_length
    idat_and_crc = blob[position:position + idat_total_length]
    if len(palette565) != palette_length or len(idat_and_crc) != idat_total_length:
        raise ImagePackError("packed palette or IDAT is truncated")

    palette = bytearray()
    for index in range(0, palette_length, 2):
        palette.extend(_rgb565_to_bytes(struct.unpack_from(">H", palette565, index)[0]))

    ihdr_payload = struct.pack(">IIBBBBB", width, height, bit_depth, 3, 0, 0, 0)
    chunks = [
        PNG_SIGNATURE,
        struct.pack(">I4s", 13, b"IHDR") + ihdr_payload + struct.pack(">I", ihdr_crc),
        struct.pack(">I4s", len(palette), b"PLTE") + palette + struct.pack(">I", palette_crc),
    ]
    if transparent_index != 255:
        alpha = bytearray(b"\xff" * (palette_length // 2))
        if transparent_index < len(alpha):
            alpha[transparent_index] = 0
        chunks.append(
            struct.pack(">I4s", len(alpha), b"tRNS")
            + alpha
            + struct.pack(">I", zlib.crc32(b"tRNS" + alpha) & 0xFFFFFFFF)
        )
    chunks.append(struct.pack(">I4s", idat_total_length - 4, b"IDAT") + idat_and_crc)
    chunks.append(PNG_IEND)
    return b"".join(chunks)


def parse_images_index(data: bytes) -> tuple[list[tuple[int, int, int]], bytes]:
    if len(data) < 2:
        raise ImagePackError("images.o is truncated")
    records_length = struct.unpack_from(">H", data, 0)[0]
    if records_length % 7:
        raise ImagePackError("images.o record byte length is not divisible by 7")
    end = 2 + records_length
    if end > len(data):
        raise ImagePackError("images.o records are truncated")
    records = [
        struct.unpack_from(">IBH", data, offset)
        for offset in range(2, end, 7)
    ]
    return records, data[end:]


def patch_images_index(data: bytes, additions: Iterable[tuple[int, int, int]]) -> bytes:
    records, suffix = parse_images_index(data)
    existing = {image_id for image_id, _container, _offset in records}
    additions = list(additions)
    duplicate = sorted(image_id for image_id, _container, _offset in additions if image_id in existing)
    if duplicate:
        raise ImagePackError(f"image ids already exist in images.o: {duplicate}")
    raw = b"".join(struct.pack(">IBH", *record) for record in records + additions)
    if len(raw) > 0xFFFF:
        raise ImagePackError("images.o records exceed uint16 byte-length field")
    return struct.pack(">H", len(raw)) + raw + suffix


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


def materialize_60011() -> tuple[Path, Path]:
    from systems.map.service import DynamicMapPackage, materialize_dynamic_map

    package = DynamicMapPackage(
        map_id=MAP_ID,
        directory=MAP_DIR,
        map_spec_path=MAP_DIR / "map.json",
        map_ref_spec_path=MAP_DIR / "map.ref.json",
        output_map_o_path=ROOT / "maps" / f"{MAP_ID}.map.o",
        output_map_ref_path=ROOT / "maps" / f"{MAP_ID}.map.ref",
    )
    built = materialize_dynamic_map(package)
    return built.map_ref_path, built.map_o_path


def build_unsigned_apk(
    source_apk: Path,
    destination_apk: Path,
    asset_bundle: Path = ASSET_BUNDLE,
) -> None:
    if not asset_bundle.is_file():
        raise ImagePackError(f"missing asset bundle: {asset_bundle}")
    map_ref, map_o = materialize_60011()

    with zipfile.ZipFile(asset_bundle, "r") as assets, zipfile.ZipFile(source_apk, "r") as src:
        manifest = json.loads(assets.read("resource_manifest.json").decode("utf-8"))
        resources = list(manifest["resources"])

        index_name = "assets/res/images/images.o"
        index_data = src.read(index_name)
        existing_containers = [
            int(match.group(1))
            for name in src.namelist()
            if (match := PNG_CONTAINER_RE.match(name))
        ]
        first_container = (max(existing_containers) + 1) if existing_containers else 0
        last_container = first_container + len(resources) - 1
        if last_container > 255:
            raise ImagePackError(
                f"need png{first_container}.p..png{last_container}.p, "
                "but images.o stores container id in one byte"
            )

        packed_members: dict[str, bytes] = {}
        additions: list[tuple[int, int, int]] = []
        for index, item in enumerate(resources):
            image_id = int(item["image_id"])
            container = first_container + index
            png_name = f"slices/{item['file']}"
            packed_members[f"assets/res/images/png{container}.p"] = pack_png_for_client_bytes(
                assets.read(png_name)
            )
            additions.append((image_id, container, 0))

        replacements = {
            index_name: patch_images_index(index_data, additions),
            f"assets/res/map/{MAP_ID}.map.ref": map_ref.read_bytes(),
            f"assets/res/map/{MAP_ID}.map.o": map_o.read_bytes(),
            **packed_members,
        }

        destination_apk.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(destination_apk, "w", allowZip64=True) as dst:
            for info in src.infolist():
                if info.filename.upper().startswith("META-INF/"):
                    continue
                if info.filename in replacements:
                    continue
                dst.writestr(clone_info(info), src.read(info.filename))
            for name, data in replacements.items():
                dst.writestr(name, data, compress_type=zipfile.ZIP_DEFLATED)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build an unsigned APK containing the image-backed map 60011 resources"
    )
    parser.add_argument("source_apk", type=Path)
    parser.add_argument("destination_apk", type=Path)
    parser.add_argument(
        "--asset-bundle",
        type=Path,
        default=ASSET_BUNDLE,
        help="60011_apk_assets.zip; defaults to maps/60011/60011_apk_assets.zip",
    )
    args = parser.parse_args()
    try:
        build_unsigned_apk(args.source_apk, args.destination_apk, args.asset_bundle)
    except (ImagePackError, OSError, ValueError, KeyError, zipfile.BadZipFile) as exc:
        parser.error(str(exc))
    print(f"wrote unsigned APK: {args.destination_apk}")


if __name__ == "__main__":
    main()
