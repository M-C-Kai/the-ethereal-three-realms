from __future__ import annotations

import json
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "data" / "catalog" / "mount_appearance_mapping.json"
OUTPUT_DIR = ROOT / "references" / "mount-atlas"
OUTPUT = OUTPUT_DIR / "mount_riding_atlas.svg"

COLS = 6
CARD_W = 190
CARD_H = 92
GAP = 14
LEFT = 36
TOP = 118


def build_svg(catalog: dict) -> str:
    families = catalog["families"]
    named = {
        int(image_id): str(meta["name"])
        for image_id, meta in catalog.get("named_templates", {}).items()
    }
    rows = sum((len(family["image_ids"]) + COLS - 1) // COLS for family in families)
    height = TOP + rows * (CARD_H + GAP) + len(families) * 50 + 80
    width = LEFT * 2 + COLS * CARD_W + (COLS - 1) * GAP

    parts = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<rect width="100%" height="100%" fill="#0f1115"/>
<style>
text{{font-family:Arial,"Microsoft YaHei",sans-serif;fill:#eef2f7}}
.title{{font-size:30px;font-weight:700}} .sub{{font-size:14px;fill:#9aa4b2}}
.family{{font-size:20px;font-weight:700;fill:#ffffff}}
.card{{fill:#171b22;stroke:#303844;stroke-width:1}}
.id{{font-size:20px;font-weight:700}} .meta{{font-size:13px;fill:#aab4c2}}
.name{{font-size:13px;fill:#ffd166;font-weight:700}}
.badge{{fill:#252c36}} .badgeText{{font-size:12px;fill:#d7dee8}}
</style>
<text x="{LEFT}" y="48" class="title">飘渺三界 · 骑乘图集</text>
<text x="{LEFT}" y="75" class="sub">{catalog['count']} 个 APK 验证骑乘资源 · character property {catalog['character_property']} = ride_code · image_id = 40000 + ride_code</text>
<text x="{LEFT}" y="96" class="sub">每组 role_model 为客户端骑乘人物骨架；411xx 为骑手/鞍具接口层，不计入独立坐骑。</text>
''']

    y = TOP
    for family in families:
        role_model = int(family["role_model"])
        image_ids = [int(value) for value in family["image_ids"]]
        parts.append(
            f'<text x="{LEFT}" y="{y}" class="family">role_model {role_model} · {len(image_ids)} 个</text>'
        )
        y += 18
        for index, image_id in enumerate(image_ids):
            row = index // COLS
            col = index % COLS
            x = LEFT + col * (CARD_W + GAP)
            yy = y + row * (CARD_H + GAP)
            ride_code = image_id - 40000
            name = named.get(image_id)

            parts.append(
                f'<rect x="{x}" y="{yy}" rx="10" ry="10" width="{CARD_W}" height="{CARD_H}" class="card"/>'
            )
            parts.append(f'<text x="{x + 14}" y="{yy + 28}" class="id">{image_id}</text>')
            parts.append(
                f'<rect x="{x + 112}" y="{yy + 12}" rx="9" ry="9" width="64" height="22" class="badge"/>'
            )
            parts.append(
                f'<text x="{x + 144}" y="{yy + 28}" text-anchor="middle" class="badgeText">#{ride_code}</text>'
            )
            parts.append(
                f'<text x="{x + 14}" y="{yy + 54}" class="meta">ride_code {ride_code}</text>'
            )
            parts.append(
                f'<text x="{x + 14}" y="{yy + 75}" class="meta">rider {role_model}</text>'
            )
            if name:
                parts.append(
                    f'<text x="{x + 174}" y="{yy + 75}" text-anchor="end" class="name">{escape(name)}</text>'
                )
        y += ((len(image_ids) + COLS - 1) // COLS) * (CARD_H + GAP) + 34

    parts.append(
        f'<text x="{LEFT}" y="{height - 30}" class="sub">source: {escape(str(catalog["source"]))} · catalog: implementation_staging/data/catalog/mount_appearance_mapping.json</text></svg>'
    )
    return "".join(parts)


def main() -> None:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    if int(catalog.get("count", 0)) != 54:
        raise SystemExit("mount catalog count must remain 54")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(build_svg(catalog), encoding="utf-8")
    print(OUTPUT)


if __name__ == "__main__":
    main()
