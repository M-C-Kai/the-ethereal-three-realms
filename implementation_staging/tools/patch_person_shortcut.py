from __future__ import annotations

import argparse
from pathlib import Path


RELATIVE_SMALI = Path('smali/pmsj/work/main/k.smali')
OLD_HANDLER = r'''    :cond_3b
    const-string v0, "\u4eba\u7269\u88c5\u5907"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_3c

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x12

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    move-result-object p0

    check-cast p0, Lpmsj/work/e/af;

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v0

    invoke-static {}, Lpmsj/work/b/a;->g()Ljava/util/Vector;

    move-result-object v1

    invoke-virtual {p0, v0, v1}, Lpmsj/work/e/af;->a(Lpmsj/work/b/v;Ljava/util/Vector;)V

    goto/16 :goto_5
'''
NEW_HANDLER = r'''    :cond_3b
    const-string v0, "\u4eba\u7269\u88c5\u5907"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_3c

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    invoke-static {}, Lpmsj/work/d/n;->j()Lpmsj/work/e/ei;

    goto/16 :goto_5
'''

ROLE_INFO_OLD_HANDLER = r'''    :cond_1e
    const-string v0, "\u89d2\u8272\u4fe1\u606f"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_1f

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    invoke-static {}, Lpmsj/work/d/n;->j()Lpmsj/work/e/ei;

    goto/16 :goto_4
'''

ROLE_INFO_NEW_HANDLER = r'''    :cond_1e
    const-string v0, "\u89d2\u8272\u4fe1\u606f"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_1f

    # Open the concrete base-character screen directly.  The aggregate
    # tab-panel constructor can leave no foreground page on this client.
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x8

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    goto/16 :goto_4
'''


def replace_handler(source: str, old: str, new: str, name: str) -> str:
    occurrences = source.count(old)
    if occurrences == 0:
        if source.count(new) == 1:
            return source
        raise RuntimeError(f'expected one {name} handler, found {occurrences}')
    if occurrences != 1:
        raise RuntimeError(f'expected one {name} handler, found {occurrences}')
    return source.replace(old, new)


def patch(decoded_apk: Path) -> Path:
    smali_path = decoded_apk / RELATIVE_SMALI
    source = smali_path.read_text(encoding='utf-8')
    source = replace_handler(source, OLD_HANDLER, NEW_HANDLER, 'character-equipment shortcut')
    source = replace_handler(source, ROLE_INFO_OLD_HANDLER, ROLE_INFO_NEW_HANDLER, 'main menu character-info')
    smali_path.write_text(source, encoding='utf-8')
    return smali_path


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Route the bottom red-shirt shortcut to the four-page character panel.'
    )
    parser.add_argument('decoded_apk', type=Path)
    args = parser.parse_args()
    print(f'patched character shortcut: {patch(args.decoded_apk)}')


if __name__ == '__main__':
    main()
