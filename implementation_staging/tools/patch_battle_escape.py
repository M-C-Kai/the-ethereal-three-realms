from __future__ import annotations

import sys
from pathlib import Path


ESCAPE_DURATION_MS = 500


def _method_bounds(lines: list[str], signature: str) -> tuple[int, int]:
    start = next(
        (index for index, line in enumerate(lines) if line.strip() == signature),
        None,
    )
    if start is None:
        raise SystemExit(f"method not found: {signature}")
    end = next(
        (
            index
            for index in range(start + 1, len(lines))
            if lines[index].strip() == ".end method"
        ),
        None,
    )
    if end is None:
        raise SystemExit(f"unterminated method: {signature}")
    return start, end


def patch_battle_screen_smali(text: str) -> str:
    """Speed up native escape and retire the completed command indicator.

    The battle screen's command timer ``W`` gates both the hourglass and the
    ready marker. Normal action playback clears it in ``i()``; the custom
    ``escapeStart()`` transition must do the same because it bypasses i().
    """
    lines = text.split("\n")
    start, end = _method_bounds(
        lines,
        ".method public final escapeStart()V",
    )

    duration_indices = [
        index
        for index in range(start, end)
        if lines[index].strip().startswith("const/16 v5,")
    ]
    if len(duration_indices) != 1:
        raise SystemExit(
            f"unexpected escape duration constant count: {len(duration_indices)}"
        )
    lines[duration_indices[0]] = f"    const/16 v5, 0x{ESCAPE_DURATION_MS:x}"

    start, end = _method_bounds(
        lines,
        ".method public final escapeStart()V",
    )
    method_text = "\n".join(lines[start:end])
    timer_clear = """\
    iget-object v0, p0, Lpmsj/work/e/j;->W:La/c/q;
    invoke-virtual {v0}, La/c/q;->g()V
""".rstrip("\n")
    if "Lpmsj/work/e/j;->W:La/c/q;" not in method_text:
        duration_index = next(
            index
            for index in range(start, end)
            if lines[index].strip().startswith("const/16 v5,")
        )
        lines[duration_index + 1:duration_index + 1] = ["", *timer_clear.split("\n")]

    start, end = _method_bounds(
        lines,
        ".method public final escapeStart()V",
    )
    method_text = "\n".join(lines[start:end])
    ready_clear = """\
    const/4 v0, 0x0
    invoke-virtual {v2, v0}, Lpmsj/work/b/h;->a(Z)V
""".rstrip("\n")
    if "invoke-virtual {v2, v0}, Lpmsj/work/b/h;->a(Z)V" not in method_text:
        move_anchor = next(
            (
                index
                for index in range(start, end)
                if lines[index].strip()
                == "invoke-virtual {v2}, Lpmsj/work/b/h;->l()La/b/c;"
            ),
            None,
        )
        if move_anchor is None:
            raise SystemExit("escape fighter movement anchor not found")
        lines[move_anchor:move_anchor] = [*ready_clear.split("\n"), ""]

    return "\n".join(lines)


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("usage: patch_battle_escape.py <smali_root>")
    root = Path(sys.argv[1])
    target = next(
        (
            candidate
            for candidate in (
                root / "smali" / "pmsj" / "work" / "e" / "j.smali",
                root / "pmsj" / "work" / "e" / "j.smali",
            )
            if candidate.exists()
        ),
        None,
    )
    if target is None:
        raise SystemExit(f"battle screen j.smali not found under {root}")

    text = target.read_text(encoding="utf-8")
    patched = patch_battle_screen_smali(text)
    if patched == text:
        print(f"already patched: {target}")
    else:
        target.write_text(patched, encoding="utf-8")
        print(
            f"patched native escape to {ESCAPE_DURATION_MS} ms and cleared ready state: {target}"
        )


if __name__ == "__main__":
    main()
