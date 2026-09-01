"""scale_role_dat.py — 放大 role/<id>.dat 帧数据（拉伸像素，无需重绘）。

用法:
    python tools/scale_role_dat.py data/role/41022.dat 1.5
    python tools/scale_role_dat.py data/role/41022.dat 2.0 --output data/role/41022_big.dat

帧字段（每帧5字节，存为 unsigned byte→short）:
    k[t]  1B  图集索引（不缩放）
    l[t]  1B  X 偏移（缩放）
    m[t]  1B  Y 偏移（缩放）
    n[t]  1B  绘制参数（缩放）
    o[t]  1B  绘制参数（缩放）
"""
from __future__ import annotations

import argparse
import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from role_dat import parse_role_dat, ub, us


def scale_dat(src: Path, scale: float, dst: Path) -> None:
    data = bytearray(src.read_bytes())
    meta = parse_role_dat(bytes(data))
    j = meta["frame_count"]
    h = meta["image_index_count"]

    # 帧数据起始位置: 8 (header) + 4*h (image indices)
    frame_start = 8 + 4 * h

    scaled = 0
    for t in range(j):
        off = frame_start + 5 * t
        # k[t]: 图集索引 — 不缩放
        # l[t]: X 偏移
        l_raw = data[off + 1]
        l_val = l_raw if l_raw < 128 else l_raw - 256  # signed
        l_new = int(round(l_val * scale))
        l_new = max(-128, min(127, l_new))
        data[off + 1] = l_new & 0xFF

        # m[t]: Y 偏移
        m_raw = data[off + 2]
        m_val = m_raw if m_raw < 128 else m_raw - 256
        m_new = int(round(m_val * scale))
        m_new = max(-128, min(127, m_new))
        data[off + 2] = m_new & 0xFF

        # n[t]: 绘制参数
        n_raw = data[off + 3]
        n_val = n_raw if n_raw < 128 else n_raw - 256
        n_new = int(round(n_val * scale))
        n_new = max(-128, min(127, n_new))
        data[off + 3] = n_new & 0xFF

        # o[t]: 绘制参数
        o_raw = data[off + 4]
        o_val = o_raw if o_raw < 128 else o_raw - 256
        o_new = int(round(o_val * scale))
        o_new = max(-128, min(127, o_new))
        data[off + 4] = o_new & 0xFF

        if (l_val, m_val, n_val, o_val) != (l_new, m_new, n_new, o_new):
            scaled += 1

    dst.write_bytes(bytes(data))
    print(f"done: {src.name} → {dst.name}  scale={scale}x  {j} frames, {scaled} modified")


def main() -> None:
    ap = argparse.ArgumentParser(description="放大 role dat 帧数据")
    ap.add_argument("src", help="源 dat 文件路径")
    ap.add_argument("scale", type=float, help="缩放倍数 (e.g. 1.5, 2.0)")
    ap.add_argument("-o", "--output", help="输出路径 (默认覆盖源文件)")
    args = ap.parse_args()

    src = Path(args.src)
    if not src.exists():
        print(f"error: {src} not found", file=sys.stderr)
        sys.exit(1)

    dst = Path(args.output) if args.output else src
    scale_dat(src, args.scale, dst)


if __name__ == "__main__":
    main()
