from __future__ import annotations

import sys
from pathlib import Path

# smali inserted into pmsj/work/main/e.smali method Q as a new 1126 subtype=1
# branch.  It reads [byte(count), int(object_id), byte(direction)] records, finds
# the matching pmsj/work/b/n in the same generic container (b/m.u) that 1126
# subtype=0 used, then calls b/n.q(direction) + b/n.I() to rotate it in place.
# Direction is validated to 0..3; out-of-range records are skipped.  The original
# subtype=0 branch is untouched.
HANDLER = """\
    :pswitch_dir
    const/4 v0, 0x1
    invoke-virtual {p0, v0}, Lpmsj/work/main/w;->a(I)B
    move-result v0
    iget-object v1, p0, Lpmsj/work/main/w;->b:Ljava/util/Vector;
    invoke-virtual {v1}, Ljava/util/Vector;->size()I
    move-result v1
    const/4 v2, 0x2
    sub-int/2addr v1, v2
    div-int/2addr v1, v0
    const/4 v10, 0x0
    const/4 v11, 0x3
    move v2, v10
    :goto_dir
    if-ge v2, v0, :dir_done
    mul-int v3, v2, v1
    add-int/lit8 v4, v3, 0x2
    invoke-virtual {p0, v4}, Lpmsj/work/main/w;->d(I)I
    move-result v4
    add-int/lit8 v5, v3, 0x3
    invoke-virtual {p0, v5}, Lpmsj/work/main/w;->a(I)B
    move-result v5
    if-lt v5, v10, :next_dir
    if-gt v5, v11, :next_dir
    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;
    move-result-object v6
    iget-object v6, v6, Lpmsj/work/b/m;->u:Ljava/util/Vector;
    invoke-virtual {v6}, Ljava/util/Vector;->size()I
    move-result v7
    move v8, v10
    :goto_find
    if-ge v8, v7, :next_dir
    invoke-virtual {v6, v8}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;
    move-result-object v9
    check-cast v9, Lpmsj/work/b/n;
    iget v12, v9, Lpmsj/work/b/n;->j:I
    if-ne v12, v4, :find_cont
    invoke-virtual {v9, v5}, Lpmsj/work/b/n;->q(I)V
    invoke-virtual {v9}, Lpmsj/work/b/n;->I()V
    goto :next_dir
    :find_cont
    add-int/lit8 v8, v8, 0x1
    goto :goto_find
    :next_dir
    add-int/lit8 v2, v2, 0x1
    goto :goto_dir
    :dir_done
    return-void
"""


def patch_e_smali(text: str) -> str:
    lines = text.split("\n")
    q_start = next(
        (i for i, ln in enumerate(lines)
         if ln.strip() == ".method private static Q(Lpmsj/work/main/w;)V"),
        None,
    )
    if q_start is None:
        raise SystemExit("method Q not found in e.smali")
    # Bump available registers so the new branch has room (locals/params form too).
    for i in range(q_start, min(q_start + 6, len(lines))):
        stripped = lines[i].strip()
        if stripped.startswith(".registers"):
            cur = int(stripped.split()[1])
            lines[i] = f"    .registers {max(cur, 14)}"
            break
        if stripped.startswith(".locals"):
            cur = int(stripped.split()[1])
            # static method Q has 1 parameter register -> total = locals + 1.
            lines[i] = f"    .locals {max(cur, 13)}"
            break
    # Locate the 1126 packed-switch (0x0) inside method Q.
    ps_idx = None
    for i in range(q_start, len(lines)):
        if lines[i].strip().startswith(".method") and i > q_start:
            break
        if lines[i].strip() == ".packed-switch 0x0":
            ps_idx = i
            break
    if ps_idx is None:
        raise SystemExit("1126 packed-switch 0x0 not found in method Q")

    end_idx = next(
        i for i in range(ps_idx, len(lines)) if lines[i].strip() == ".end packed-switch"
    )
    cases = [
        (i, lines[i].strip())
        for i in range(ps_idx + 1, end_idx)
        if lines[i].strip().startswith(':pswitch')
    ]
    if len(cases) not in (1, 2):
        raise SystemExit(f"unexpected 1126 subtype count: {len(cases)}")

    data_label_idx = next(
        (
            i for i in range(ps_idx - 1, q_start, -1)
            if lines[i].strip().startswith(':pswitch_data')
        ),
        None,
    )
    if data_label_idx is None:
        raise SystemExit("1126 packed-switch data label not found in method Q")

    handler_lines = HANDLER.rstrip("\n").split("\n")
    if len(cases) == 1:
        # Clean APK: add subtype 1 immediately before the switch table.
        lines[data_label_idx:data_label_idx] = handler_lines
        ps_idx += len(handler_lines)
        end_idx += len(handler_lines)
        lines.insert(end_idx, "        :pswitch_dir")
    else:
        # Already patched APK/worktree: replace the complete subtype-1 branch.
        # This upgrades both the stale short-count handler and labels normalized
        # by a DEX disassembler, without appending an accidental subtype 2.
        subtype_one_label = cases[1][1]
        handler_idx = next(
            (
                i for i in range(q_start, data_label_idx)
                if lines[i].strip() == subtype_one_label
            ),
            None,
        )
        if handler_idx is None:
            raise SystemExit("1126 subtype=1 handler label not found in method Q")
        lines[handler_idx:data_label_idx] = handler_lines

        # Re-find the switch after replacing a differently sized old handler.
        ps_idx = next(
            i for i in range(q_start, len(lines))
            if lines[i].strip() == ".packed-switch 0x0"
        )
        end_idx = next(
            i for i in range(ps_idx, len(lines))
            if lines[i].strip() == ".end packed-switch"
        )
        case_indices = [
            i for i in range(ps_idx + 1, end_idx)
            if lines[i].strip().startswith(':pswitch')
        ]
        lines[case_indices[1]] = "        :pswitch_dir"
    return "\n".join(lines)


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("usage: patch_npc_direction.py <smali_root>")
    root = Path(sys.argv[1])
    target = next(
        (c for c in (
            root / "smali" / "pmsj" / "work" / "main" / "e.smali",
            root / "pmsj" / "work" / "main" / "e.smali",
        ) if c.exists()),
        None,
    )
    if target is None:
        raise SystemExit(f"e.smali not found under {root}")
    text = target.read_text(encoding="utf-8")
    patched = patch_e_smali(text)
    if patched == text:
        print(f"already patched: {target}")
    else:
        target.write_text(patched, encoding="utf-8")
        print(f"patched 1126 subtype=1 into: {target}")


if __name__ == "__main__":
    main()
