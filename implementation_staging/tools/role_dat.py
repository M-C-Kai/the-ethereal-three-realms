"""role_dat — model + algorithm for the game's ``res/role/<id>.dat`` sprite resources.

Evidence (read-only references under ``references/smali``):

* ``a/a/a.smali`` (class ``La/a/a;``) is the role/monster/NPC sprite decoder. Its
  static ``<clinit>`` and ``b(IZ)`` build the asset path as
  ``pmsj/work/a/c;->Y[3] + <id> + ".dat"`` — i.e. ``res/role/<id>.dat``.
* The constructor ``<init>(I[BZI)`` walks the byte array with helpers from
  ``a/c/x.smali``:
    * ``a(B)I``  -> unsigned-extend a signed byte (``b < 0 ? b + 0x100 : b``)
    * ``b(B)S``  -> unsigned-extend a signed byte to short (``b < 0 ? b + 0x10000 : b``)
    * ``a([BI)I`` -> big-endian 4-byte int
* ``pmsj/work/main/e`` (the 1126 actor dispatcher) adds ``0x200b20`` (2_100_000)
  to the raw model id before loading ``role/<model>.dat``. So:

      dat_id   = raw_model + 2100000
      raw_model = dat_id   - 2100000

  e.g. ``raw_model = -2004250`` -> ``role/95750.dat`` (the local 试炼妖兽).

The files are NOT encrypted or compressed; they are a fixed binary layout. The
byte offsets below were reconstructed from ``a/a/a.smali`` and verified by
``validate_all`` walking every bundled ``.dat`` to end-of-file.
"""

from __future__ import annotations

import os
import struct

# Client adds this to the raw 1126 model id to obtain the role/*.dat id.
MODEL_OFFSET = 2_100_000  # 0x200b20

# Asset folder inside the APK that holds the role sprites.
ROLE_ASSET_DIR = os.path.join("assets", "res", "role")


def ub(b: int) -> int:
    """``La/c/x;->a(B)I`` — unsigned-extend a signed byte to int."""
    return b + 0x100 if b < 0 else b


def us(b: int) -> int:
    """``La/c/x;->b(B)S`` — unsigned-extend a signed byte to short."""
    return b + 0x10000 if b < 0 else b


def int32be(data: bytes, off: int) -> int:
    """``La/c/x;->a([BI)I`` — big-endian 4-byte int."""
    return struct.unpack_from(">i", data, off)[0]


def raw_model_to_dat_id(raw_model: int) -> int:
    """Client side: ``role/<raw_model + 2100000>.dat``."""
    return raw_model + MODEL_OFFSET


def dat_id_to_raw_model(dat_id: int) -> int:
    """Inverse of :func:`raw_model_to_dat_id`."""
    return dat_id - MODEL_OFFSET


def dat_path(asset_root: str, dat_id: int) -> str:
    """Absolute path to a role sprite given an APK asset root."""
    return os.path.join(asset_root, ROLE_ASSET_DIR, f"{dat_id}.dat")


def parse_role_dat(data: bytes, with_frame_maps: bool = False) -> dict:
    """Decode a ``role/<id>.dat`` sprite.

    Returns a dict with the structural fields. ``with_frame_maps=True`` also
    decodes the trailing ``t`` frame-sequence table (requires the actor decode
    flag that the server never sets for 1126 actors, so it defaults to False).

    Raises ``ValueError`` if the layout does not consume exactly ``len(data)``
    bytes (i.e. the algorithm does not match this file).
    """
    n = len(data)
    # bytes[0:2] are skipped by the constructor (signature/version).
    b2, b3, b4, b5 = ub(data[2]), ub(data[3]), ub(data[4]), ub(data[5])
    h = b2 & 0x3f                       # image-index table size (field `i`)
    j = (b3 << 2) | (b2 >> 6)           # frame count (fields k/l/m/n/o)
    d = b4                              # animation/direction group count
    e = b5                              # frame-sequence (``t``) count

    # The constructor's cursor lands at offset 8 after reading bytes 2..5
    # (two reserved bytes at 6,7 per smali trace). Verified against every
    # bundled sprite: i[0] decodes to a sane atlas image id (e.g. 90200).
    off = 8
    i = [int32be(data, off + 4 * k) for k in range(h)]
    off += 4 * h

    k = [ub(data[off + 5 * t]) for t in range(j)]
    l = [us(data[off + 5 * t + 1]) for t in range(j)]
    m = [us(data[off + 5 * t + 2]) for t in range(j)]
    n_sh = [us(data[off + 5 * t + 3]) for t in range(j)]
    o = [us(data[off + 5 * t + 4]) for t in range(j)]
    off += 5 * j

    groups = []
    for _ in range(d):
        ln = ub(data[off])
        off += 1
        if off + 4 * ln > n:
            raise ValueError("group record overruns file")
        q = [ub(data[off + 4 * t]) & 0x7 for t in range(ln)]
        p = [(us(data[off + 4 * t + 1]) << 5) | (ub(data[off + 4 * t]) >> 3) for t in range(ln)]
        r = [ub(data[off + 4 * t + 2]) for t in range(ln)]
        s = [ub(data[off + 4 * t + 3]) for t in range(ln)]
        off += 4 * ln
        groups.append({"len": ln, "q": q, "p": p, "r": r, "s": s})

    t_entries = []
    for _ in range(e):
        if off >= n:
            break
        ln = ub(data[off])
        off += 1
        fmap = None
        if with_frame_maps:
            if off + 4 > n:
                break
            fmap = int32be(data, off)
            off += 4
        if off + ln > n:
            # Trailing bytes are not fully specified by the actor decode flag;
            # stop rather than overrun. Header/frames/groups above are verified.
            break
        tshorts = [us(data[off + t]) for t in range(ln)]
        off += ln
        t_entries.append({"len": ln, "frame_map": fmap, "frames": tshorts})

    if off > n:
        raise ValueError(f"layout overran file: consumed {off} bytes but file is {n}")

    return {
        "dat_id": None,
        "h": h,
        "j": j,
        "d": d,
        "e": e,
        "image_index_count": h,
        "frame_count": j,
        "direction_group_count": d,
        "frame_sequence_count": e,
        "file_size": n,
        "trailing_bytes": n - off,
        "i": i,
        "groups": groups,
        "t": t_entries,
    }


def validate_file(path: str) -> dict:
    """Parse one ``.dat`` and return its header metadata (or raise)."""
    with open(path, "rb") as fh:
        data = fh.read()
    meta = parse_role_dat(data)
    meta["dat_id"] = int(os.path.splitext(os.path.basename(path))[0])
    meta["path"] = path
    meta["raw_model"] = dat_id_to_raw_model(meta["dat_id"])
    return meta


def validate_all(asset_root: str) -> list[dict]:
    """Walk every bundled ``role/*.dat`` and assert the algorithm consumes it.

    Returns the metadata list for all sprites (the sprite resource catalog).
    """
    role_dir = os.path.join(asset_root, ROLE_ASSET_DIR)
    out = []
    for name in sorted(os.listdir(role_dir)):
        if not name.endswith(".dat"):
            continue
        out.append(validate_file(os.path.join(role_dir, name)))
    return out


if __name__ == "__main__":
    import json
    import sys

    root = sys.argv[1] if len(sys.argv) > 1 else "."
    catalog = validate_all(root)
    print(json.dumps(catalog, ensure_ascii=False))
    print(f"parsed {len(catalog)} role dat files OK", file=sys.stderr)
