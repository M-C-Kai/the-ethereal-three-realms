import argparse
from pathlib import Path


PATCH_MARKER = '# Local login: return an authentication failure to the input form.'
REQUEST_MARKER = '# Local login: keep the login form visible while authenticating.'
REQUEST_NAVIGATION = f'''\n\n    {REQUEST_MARKER}\n    invoke-static {{}}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;\n\n    move-result-object v1\n\n    const/16 v0, 0xa\n\n    invoke-virtual {{v1, v0}}, Lpmsj/work/d/n;->a(I)Z\n'''


def patch_login_failure_ui(smali_file: Path) -> bool:
    source = smali_file.read_text(encoding='utf-8')
    if PATCH_MARKER in source:
        return False
    switch_at = source.find('    :pswitch_11')
    if switch_at < 0:
        raise ValueError('wrong-password branch (:pswitch_11) was not found')
    result_at = source.find('    move-result-object v4', switch_at)
    if result_at < 0:
        raise ValueError('UI manager result in wrong-password branch was not found')
    insert_at = result_at + len('    move-result-object v4')
    navigation = f'''\n\n    {PATCH_MARKER}\n    const/16 v5, 0xa\n\n    invoke-virtual {{v4, v5}}, Lpmsj/work/d/n;->a(I)Z\n\n    invoke-static {{}}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;\n\n    move-result-object v4\n\n    const/16 v5, 0x136\n\n    invoke-virtual {{v4, v5}}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;\n'''
    smali_file.write_text(source[:insert_at] + navigation + source[insert_at:], encoding='utf-8')
    return True


def patch_login_flow(decode_dir: Path) -> bool:
    main_dir = decode_dir / 'smali' / 'pmsj' / 'work' / 'main'
    failure_file = main_dir / 'e.smali'
    request_file = main_dir / 'c.smali'
    failure_source = failure_file.read_text(encoding='utf-8')
    request_source = request_file.read_text(encoding='utf-8')
    changed = False
    if REQUEST_NAVIGATION in request_source:
        request_file.write_text(request_source.replace(REQUEST_NAVIGATION, '', 1), encoding='utf-8')
        changed = True
    if PATCH_MARKER not in failure_source:
        changed = patch_login_failure_ui(failure_file) or changed
    return changed


def main() -> None:
    parser = argparse.ArgumentParser(description='Return failed authentication to the login form')
    parser.add_argument('decode_dir', type=Path)
    args = parser.parse_args()
    changed = patch_login_flow(args.decode_dir)
    print(f"{'Patched' if changed else 'Already patched'}: {args.decode_dir}")


if __name__ == '__main__':
    main()
