# 骑乘图集

本目录把 `data/catalog/mount_appearance_mapping.json` 中已经从 `piaomiao_local_login.apk` 验证出的骑乘关系整理成可视化索引。

## 当前覆盖

- 独立骑乘资源：54 个。
- 角色属性：`property 22`。
- 下发值：`ride_code = image_id - 40000`。
- 骑乘人物骨架：6 套，分别为 `101000.dat`、`102000.dat`、`103000.dat`、`104000.dat`、`105000.dat`、`106000.dat`。
- 已确认名称：`41004 -> ride_code 1004 -> role_model 102000 -> 辟邪`。
- `411xx` 属于骑手/鞍具接口层，不计入 54 个独立坐骑。

## 文件

- `mount_riding_atlas.svg`：54 个坐骑的总览图，按骑乘人物骨架分为 6 组。
- `manifest.json`：逐项列出 `image_id / ride_code / role_model / name / sprite_status`，供程序、测试和后续真实精灵图替换使用。
- `../scripts/build_mount_atlas.py`：从主坐骑资料库重新生成总览 SVG，避免手工维护两套映射。

## 图集状态说明

当前仓库没有保存 APK 中 `40001..45002` 对应的原始坐骑 PNG 切片，因此总览图只展示已经验证的资源索引和人物骨架关系，不使用 AI 或占位绘画冒充原始游戏资源。`manifest.json` 的 `sprite_status` 目前统一为 `indexed_no_png`。

后续把 APK 原始图像资源切片写入仓库后，可以按 `image_id` 直接挂接到同一 manifest，在不改变 `ride_code` 和 `role_model` 的前提下升级成真实精灵预览图集。
