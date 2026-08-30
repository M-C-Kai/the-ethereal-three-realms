# 角色外观诊断资料

本目录集中保存角色模型、叠加层和装备映射的历史诊断产物。它们用于人工审计和视觉对照，不参与服务端运行，也不参与 APK 构建。

## 文件关联

| 产物 | 生成来源或用途 |
| --- | --- |
| `player_overlay_variants.png` | 由仓库根目录 `render_player_overlay_variants.py` 生成，对比角色属性槽位替换后的外观。 |
| `role_50k_diagnostic.json` / `.png` | 50xxx 角色资源的历史结构清单与预览图；原始生成器不在当前仓库。 |
| `role_models_diagnostic.json` / `.png` | 基础角色模型的历史结构清单与预览图；原始生成器不在当前仓库。 |
| `role_overlay_diagnostic.json` / `.png` | 角色叠加资源的历史结构清单与预览图；原始生成器不在当前仓库。 |
| `appearance-layer-audit/` | 由根目录 `audit_all_character_layers.py` 生成的逐图层审计结果。 |
| `appearance-layer-audit/selected-equipment-mapping.png` | 由根目录 `render_selected_equipment_mapping.py` 生成的已选装备映射预览。 |

三个生成脚本仍保留在仓库根目录。它们依赖历史提取目录中的资源，可能需要调整脚本顶部的绝对路径后才能在其他机器上重新运行；输出路径已经统一指向本目录。

## NPC 镜像预览

`npc-facing/96030-vs-96031.png` 由 `implementation_staging/tools/mirror_role_dat.py` 生成，用于确认 `96031.dat` 的首帧与 `96030.dat` 首帧构成逐像素水平镜像。
