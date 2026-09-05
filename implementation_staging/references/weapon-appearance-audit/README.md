# 武器外观资源审计（property7）

本目录是从本机 `build/weapon-apk-extracted` 抽出的**最小可复核调查资料**。  
不是完整 APK，也不是官方装备映射表。

来源：

- `implementation_staging/build/weapon-apk-extracted/assets/res/role/`
- `implementation_staging/build/weapon-apk-extracted/assets/res/images/images.o`

没有提交整个 `build/`、全量 PNG、dex-smali 或 APK。

---

## CONFIRMED

客户端：`implementation_staging/references/smali/pmsj/work/b/v.smali`

- `I(I)`：`property7 == 0` 时把角色模板设回 `100000`（基础角色模板）。
- `H(I)`：由 `property7` 选择武器角色 DAT。
- `L(I)` / `G(I)`：选择武器图层并写入武器图。

公式（地图人物武器外观资源选择机制）：

```text
suffix = property7 % 10000

role_dat =
    100000 + ((suffix // 1000) + 1) * 1000

weapon_layer =
    ((property7 % 1000) // 100) + 32

当 role_dat >= 102000：
    weapon_layer += 1

weapon_image =
    40000 + suffix
```

`property7 == 0` 时回基础角色模板 `100000`。

这套公式只证明：**地图人物武器外观如何选 DAT / layer / 40000 段图片**。

---

## UNKNOWN

以下**尚未恢复**，不得写成已确认：

- `icon_code → property7`
- 背包图标组 `21..33` = 地图武器外观组
- 130 个 preview weapon 已有官方映射
- `property7` 高位的完整官方编码（当前只证明低 4 位资源语义）

---

## 历史样本（不是候选高位模板）

兼容服/历史验证曾使用 `property7 = 270001`。

按上式：

```text
suffix = 1
role_dat = 101000
weapon_layer = 32
weapon_image = 40001
```

`270001` 只能作为已知兼容服样本记录在此。  
**不能**把 `27xxxx` 当成所有候选的高位模板。候选表只写 `property7_low4_candidate`。

---

## 本目录文件

| 文件 | 说明 |
|---|---|
| `role/*.dat` | 实际存在的人物复合模板 DAT |
| `weapon_image_ids.json` | `images.o` 中实际存在的 `40000..49999` ID |
| `role_manifest.json` | 各 DAT 只读解析结果 |
| `property7_candidates.json` | 被实际 DAT + 实际图片反向支持的低 4 位候选 |
| `build_audit.py` | 生成上述资料的只读脚本 |

未生成 `weapon_candidates.png`：当前提取目录只有 `images.o` + `png*.p`，没有现成 rebuilt PNG，不额外展开数千张图。
