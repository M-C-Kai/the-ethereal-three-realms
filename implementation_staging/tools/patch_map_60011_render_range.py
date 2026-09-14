"""Widen the APK map renderer's tile scan for the local 90x90 scene.

The client scans tile anchors inside a viewport-derived rectangle. The local
60011 tiles use images up to 135x113 with signed-byte layer offsets, so an
anchor just outside that rectangle can still paint well inside the screen.
The Graphics clip remains the original viewport; only tile discovery widens.
"""
from __future__ import annotations

import argparse
from pathlib import Path


NEEDLE = (
    '    iput-short v4, v3, La/b/e;->d:S\n\n'
    '    move-object/from16 v0, p0\n\n'
    '    iget v0, v0, Lpmsj/work/b/m;->p:I'
)
INSERT = '''    iput-short v4, v3, La/b/e;->d:S

    # Only the local 60011 map uses this 90x90 scene layout. The renderer
    # still clips to the original screen rectangle; enlarge tile discovery.
    move-object/from16 v0, p0
    iget-byte v3, v0, Lpmsj/work/b/m;->g:B
    const/16 v4, 0x5a
    if-ne v3, v4, :map60011_range_done
    iget-byte v3, v0, Lpmsj/work/b/m;->h:B
    if-ne v3, v4, :map60011_range_done

    sget-object v3, Lpmsj/work/b/m;->ai:La/b/e;
    iget-short v4, v3, La/b/e;->a:S
    add-int/lit16 v4, v4, -0x100
    int-to-short v4, v4
    iput-short v4, v3, La/b/e;->a:S
    iget-short v4, v3, La/b/e;->b:S
    add-int/lit16 v4, v4, -0x100
    int-to-short v4, v4
    iput-short v4, v3, La/b/e;->b:S
    iget-short v4, v3, La/b/e;->c:S
    add-int/lit16 v4, v4, 0x200
    int-to-short v4, v4
    iput-short v4, v3, La/b/e;->c:S
    iget-short v4, v3, La/b/e;->d:S
    add-int/lit16 v4, v4, 0x200
    int-to-short v4, v4
    iput-short v4, v3, La/b/e;->d:S

    :map60011_range_done
    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/b/m;->p:I'''


def patch_smali(source: str) -> str:
    normalized = source.replace('\r\n', '\n')
    if ':map60011_range_done' in normalized:
        return normalized
    if normalized.count(NEEDLE) != 1:
        raise ValueError('expected map draw-range insertion point exactly once')
    return normalized.replace(NEEDLE, INSERT, 1)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('smali', type=Path)
    args = parser.parse_args()
    original = args.smali.read_text(encoding='utf-8')
    with args.smali.open('w', encoding='utf-8', newline='\n') as output:
        output.write(patch_smali(original))


if __name__ == '__main__':
    main()
