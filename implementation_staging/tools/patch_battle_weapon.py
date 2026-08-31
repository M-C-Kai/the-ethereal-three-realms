from __future__ import annotations

import hashlib
import sys
from pathlib import Path


BASELINE_SHA256 = "BD51B92AA44D33823CAC6CCA71057D742F3988EE2284097B86E6D4EBC724E2A7"
PATCHED_SHA256 = "DEAE5D713731CBE054936876F41B30CB05CB8584BC766107F3E477D0CDE26281"

# The original character definition already contains the weapon frame records,
# but its six idle-direction groups do not reference them. These pieces were
# recovered from the previously verified weapon-visible build. They are placed
# immediately before each group's three existing foreground pieces so the
# original body-layer ordering remains unchanged.
IDLE_WEAPON_PIECES = (
    ((0, 233, -46, -40), (0, 353, -19, -4), (0, 348, -22, -11), (0, 345, -21, -16)),
    ((0, 233, -46, -39), (0, 351, -17, -21), (0, 347, -22, -15), (0, 347, -33, -22), (0, 346, -22, -21)),
    ((0, 233, -46, -39), (0, 349, -24, -32), (0, 346, -21, -19), (0, 348, -32, -27)),
    ((0, 233, -46, -39), (0, 352, -29, -38), (0, 345, -22, -24), (0, 345, -31, -32)),
    ((0, 233, -46, -39), (0, 350, -44, -34), (0, 346, -32, -40), (0, 347, -22, -3)),
    ((0, 233, -46, -40), (0, 349, -44, -28), (0, 348, -22, -9)),
)


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def _encode_piece(piece: tuple[int, int, int, int]) -> bytes:
    transform, record_index, x, y = piece
    if not 0 <= transform <= 7:
        raise ValueError(f"invalid transform: {transform}")
    if not 0 <= record_index <= 0x1FFF:
        raise ValueError(f"invalid record index: {record_index}")
    if not -128 <= x <= 127 or not -128 <= y <= 127:
        raise ValueError(f"piece offset does not fit signed bytes: {(x, y)}")
    packed = ((record_index & 0x1F) << 3) | transform
    return bytes((packed, record_index >> 5, x & 0xFF, y & 0xFF))


def patch_role_dat(data: bytes) -> bytes:
    digest = _sha256(data)
    if digest == PATCHED_SHA256:
        return data
    if digest != BASELINE_SHA256:
        raise SystemExit(
            "unsupported assets/res/role/100000.dat: "
            f"SHA-256 {digest}; expected {BASELINE_SHA256} or {PATCHED_SHA256}"
        )
    if len(data) < 8:
        raise SystemExit("role/100000.dat header is truncated")

    image_count = data[2] & 0x3F
    record_count = (data[3] << 2) | (data[2] >> 6)
    group_count = data[4]
    if group_count < len(IDLE_WEAPON_PIECES):
        raise SystemExit(f"role/100000.dat has only {group_count} groups")

    group_start = 8 + image_count * 4 + record_count * 5
    position = group_start
    encoded_groups: list[bytes] = []
    for group_index in range(group_count):
        if position >= len(data):
            raise SystemExit(f"role/100000.dat group {group_index} is truncated")
        piece_count = data[position]
        pieces_start = position + 1
        pieces_end = pieces_start + piece_count * 4
        if pieces_end > len(data):
            raise SystemExit(f"role/100000.dat group {group_index} pieces are truncated")

        raw_pieces = data[pieces_start:pieces_end]
        if group_index < len(IDLE_WEAPON_PIECES):
            additions = b"".join(_encode_piece(piece) for piece in IDLE_WEAPON_PIECES[group_index])
            if piece_count < 3:
                raise SystemExit(f"role/100000.dat idle group {group_index} lacks layer anchors")
            insert_at = len(raw_pieces) - 3 * 4
            raw_pieces = raw_pieces[:insert_at] + additions + raw_pieces[insert_at:]
            piece_count += len(IDLE_WEAPON_PIECES[group_index])
        encoded_groups.append(bytes((piece_count,)) + raw_pieces)
        position = pieces_end

    patched = data[:group_start] + b"".join(encoded_groups) + data[position:]
    patched_digest = _sha256(patched)
    if patched_digest != PATCHED_SHA256:
        raise SystemExit(
            "weapon patch produced an unexpected role asset: "
            f"SHA-256 {patched_digest}; expected {PATCHED_SHA256}"
        )
    return patched


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: patch_battle_weapon.py <decoded_apk_root>")
    root = Path(sys.argv[1])
    target = root / "assets" / "res" / "role" / "100000.dat"
    if not target.exists():
        raise SystemExit(f"player role asset not found: {target}")

    source = target.read_bytes()
    patched = patch_role_dat(source)
    if patched == source:
        print(f"battle idle weapon asset already patched: {target}")
    else:
        target.write_bytes(patched)
        print(f"patched battle idle weapon asset: {target}")


if __name__ == "__main__":
    main()
