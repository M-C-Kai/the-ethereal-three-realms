import argparse
from pathlib import Path


MARKER = '# Local role delete: ignore surrounding input whitespace.'
NEEDLE = '''    const-string v0, "\\u786e\\u8ba4"

    invoke-virtual {p2, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z'''
REPLACEMENT = f'''    const-string v0, "\\u786e\\u8ba4"

    {MARKER}
    invoke-virtual {{p2}}, Ljava/lang/String;->trim()Ljava/lang/String;

    move-result-object p2

    invoke-virtual {{p2, v0}}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z'''


def patch_role_delete_confirmation(decode_dir: Path) -> bool:
    smali = decode_dir / 'smali' / 'pmsj' / 'work' / 'e' / 'cv.smali'
    source = smali.read_text(encoding='utf-8')
    if MARKER in source:
        return False
    if NEEDLE not in source:
        raise ValueError('role-delete confirmation comparison was not found')
    smali.write_text(source.replace(NEEDLE, REPLACEMENT, 1), encoding='utf-8')
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description='Allow whitespace around role-delete confirmation')
    parser.add_argument('decode_dir', type=Path)
    args = parser.parse_args()
    changed = patch_role_delete_confirmation(args.decode_dir)
    print(f"{'Patched' if changed else 'Already patched'}: {args.decode_dir}")


if __name__ == '__main__':
    main()
