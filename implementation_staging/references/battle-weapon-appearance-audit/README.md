# 战斗武器资源视觉审计

本目录只归档 APK 里**实际存在**的两类资源：装备武器图标组、战斗人物武器 image family。  
不是官方装备映射表，也**不要**把左右两列当成配对。

来源：

- `implementation_staging/build/weapon-apk-extracted/assets/res/images/images.o`
- 同目录 `png*.p`

使用项目已有脚本：

- `references/scripts/extract_game_images.py`（`rebuild_png`）
- `references/scripts/build_equipment_icon_sheet.py`（图标组 `3002424 + group * 10000`、帧号 `icon_code`）
- `references/scripts/render_role_resources.py`（本轮未改角色 DAT；战斗图从 `images.o` 直接重建）

没有提交整个 `build/`、全量 PNG、dex-smali 或 APK。

---

## CONFIRMED

客户端：`implementation_staging/references/smali/pmsj/work/b/h.smali` → `h.e(I)V` → `v.e(I)V`

战斗协议 field2（`v.e` 的参数）：

```text
field2 / 10  = battle weapon image
field2 % 10  = quality overlay selector
```

`quality != 0` 时：

```text
weapon_code = field2 / 1000
```

`weapon_code` **只**在以下固定数组中生成品质覆盖：

```text
[241, 220, 290, 231, 280, 250, 270, 271, 242, 240, 260, 221, 230]
```

overlay slot / image：

```text
index = 上述数组索引
slot  = 19 + index
image = 30000 + index * 100 + quality
```

这些是 **battle `v.e(field2)`** 使用的 weapon image family（本目录 `22000..29099` 段）。  
不要和地图人物 `property7` 使用的 `40000..49999` 图片混在一起。

---

## 历史验证样本

```text
270001
→ weapon image 27000
→ slot16
→ quality1
→ overlay slot25
→ image 30601
```

按上式核对：`270001 / 10 = 27000`，`270001 % 10 = 1`，`weapon_code = 270`，数组下标 6，`slot = 25`，`image = 30000 + 600 + 1 = 30601`。

---

## UNKNOWN

icon group `21..33` 到 battle `weapon_code` 的**完整映射仍未恢复**。

本目录两张 contact sheet 只是各自按组/族罗列实际图片，**禁止**按行号或视觉相似做左右配对。

---

## 文件

| 文件 | 内容 |
|---|---|
| `icon_groups.png` | 图标组 21..33 分行；每张标 `icon_code`（如 2100） |
| `battle_weapon_families.png` | 战斗 family 220..290 分行；每张标 `image_id` |
| `manifest.json` | 实际提取到的 `icon_groups` / `battle_weapon_families` ID 列表 |
| `build_audit.py` | 从已提取 `images.o` 重建并拼 sheet |
