"""Keep 1026/0 roster writes from replacing the active map screen."""
from __future__ import annotations

import sys
from pathlib import Path


def patch_team_roster_ui(source: str) -> str:
    method_start = source.index('.method private static aj(Lpmsj/work/main/w;)V')
    method_end = source.index('.end method', method_start)
    method = source[method_start:method_end]
    branch_start = method.index('    :pswitch_1\n')
    branch_end = method.index('    :pswitch_2\n', branch_start)
    branch = method[branch_start:branch_end]
    navigation = (
        '    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;\n\n'
        '    const/16 v0, 0x5c\n\n'
        '    invoke-static {v0}, Lpmsj/work/d/n;->h(I)V\n\n'
    )
    if navigation not in branch:
        compact = navigation.replace('\n\n', '\n')
        if compact in branch:
            navigation = compact
        elif 'const/16 v0, 0x5c' not in branch:
            return source
        else:
            raise ValueError('1026/0 navigation layout changed')
    patched_branch = branch.replace(navigation, '', 1)
    return source[:method_start] + method[:branch_start] + patched_branch + method[branch_end:] + source[method_end:]


def main() -> None:
    decoded = Path(sys.argv[1])
    target = decoded / 'smali/pmsj/work/main/e.smali'
    source = target.read_text(encoding='utf-8')
    patched = patch_team_roster_ui(source)
    if patched == source and 'const/16 v0, 0x5c' in source[source.index('.method private static aj'):source.index('.end method', source.index('.method private static aj'))]:
        raise SystemExit('team roster UI patch not applied')
    target.write_text(patched, encoding='utf-8')


if __name__ == '__main__':
    main()
