"""Patch the compatibility APK to use the native full equipment tooltip."""
from __future__ import annotations

import argparse
from pathlib import Path


VIEW_MARKER = "# Local equipment detail: use native b/g tooltip for self equipment."
CATEGORY_MARKER = "# Local equipment detail: categories 1..14 carry full attribute blocks."

VIEW_NEEDLE = """    invoke-direct {p0}, Lpmsj/work/e/af;->i()Z

    move-result v1

    if-eqz v1, :cond_1

    iget v0, v0, Lpmsj/work/b/g;->e:I

    invoke-static {v0}, Lpmsj/work/main/e;->c(I)V"""

VIEW_REPLACEMENT = f"""    invoke-direct {{p0}}, Lpmsj/work/e/af;->i()Z

    move-result v1

    if-eqz v1, :cond_1

    {VIEW_MARKER}
    iget-object v1, p0, Lpmsj/work/e/af;->ad:Lpmsj/work/d/l;

    iget v2, p0, Lpmsj/work/e/af;->ao:I

    iget v3, p0, Lpmsj/work/e/af;->ap:I

    invoke-static {{v1, v0, p0, v2, v3}}, Lpmsj/work/e/b;->a(Lpmsj/work/d/l;Lpmsj/work/b/j;Lpmsj/work/d/c;II)V"""


def patch_self_equipment_view(source: str) -> str:
    if VIEW_MARKER in source:
        return source
    if VIEW_NEEDLE not in source:
        raise ValueError("self-equipment 1032 view branch was not found")
    return source.replace(VIEW_NEEDLE, VIEW_REPLACEMENT, 1)


def patch_full_equipment_categories(source: str) -> str:
    method_start = source.find(".method public final c()Z")
    if method_start < 0:
        raise ValueError("b/g.c() equipment predicate was not found")
    method_end = source.find(".end method", method_start)
    if method_end < 0:
        raise ValueError("b/g.c() method end was not found")

    method = source[method_start:method_end]
    if CATEGORY_MARKER in method:
        return source

    needle = """    const/16 v1, 0xb

    if-ge v0, v1, :cond_0"""
    replacement = f"""    {CATEGORY_MARKER}
    const/16 v1, 0xf

    if-ge v0, v1, :cond_0"""
    if needle not in method:
        raise ValueError("b/g.c() category upper bound was not found")

    patched_method = method.replace(needle, replacement, 1)
    return source[:method_start] + patched_method + source[method_end:]


def patch_equipment_details(decode_dir: Path) -> bool:
    af_path = decode_dir / "smali" / "pmsj" / "work" / "e" / "af.smali"
    g_path = decode_dir / "smali" / "pmsj" / "work" / "b" / "g.smali"

    af_source = af_path.read_text(encoding="utf-8")
    g_source = g_path.read_text(encoding="utf-8")
    af_patched = patch_self_equipment_view(af_source)
    g_patched = patch_full_equipment_categories(g_source)

    changed = False
    if af_patched != af_source:
        af_path.write_text(af_patched, encoding="utf-8")
        changed = True
    if g_patched != g_source:
        g_path.write_text(g_patched, encoding="utf-8")
        changed = True
    return changed


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Enable native full equipment details for local compatibility gear",
    )
    parser.add_argument("decode_dir", type=Path)
    args = parser.parse_args()
    changed = patch_equipment_details(args.decode_dir)
    print(f"{'Patched' if changed else 'Already patched'}: {args.decode_dir}")


if __name__ == "__main__":
    main()
