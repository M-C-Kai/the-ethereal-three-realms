# 骑乘图集

本目录的骑乘图集以 `data/catalog/mount_appearance_mapping.json` 为唯一坐骑资料来源，并直接读取原 APK 资源生成外观，不再在图集脚本中硬编码坐骑编号、人物模型、图片槽或代表动画帧。

## 资源链路

生成器 `../scripts/build_mount_atlas.py` 读取：

- `mount_appearance_mapping.json`：54 个已确认主骑乘资源、分组、已知名称和 `image_base`。
- APK `assets/res/images/images.o`：`image_id -> png*.p / offset` 真实资源索引。
- APK `assets/res/images/png*.p`：原始打包精灵图。
- APK `assets/res/role/{role_model}.dat`：骑乘人物复合模型、图片槽、frame/group/sequence。

主坐骑图片槽不会写死。程序会根据当前 family 的 `image_id // 100` 在对应 role DAT 的 `image_ids` 中定位唯一主坐骑槽，因此能自动区分 `410xx` 主体与 `411xx` 鞍具/骑手接口层，以及 `400xx` 与 `401xx/402xx` 的辅助飞行层。

代表预览帧也不会写死。程序遍历 role DAT 的 sequence，选择第一个实际引用主坐骑槽的 group。当前 APK 资源自动推导出的结果为：101000→slot32/group0、102000→slot33/group5、103000→slot33/group5、104000→slot33/group0、105000→slot33/group0、106000→slot33/group6；这些值是生成结果，不是配置常量。

## 生成

在 `implementation_staging` 目录执行：

```powershell
D:\python\python.exe references\scripts\build_mount_atlas.py --apk <原APK路径>
```

默认输出：

- `mount_riding_atlas.png`：54 个真实 APK 骑乘人物+坐骑组合总览。
- `model_101000_resources.png` ... `model_106000_resources.png`：6 个骑乘人物模型分组图。
- `manifest.json`：逐项记录 `image_id / ride_code / role_model / primary_slot / representative_group / images.o container+offset / name`。

`mount_riding_atlas.svg` 是前一版仅展示索引关系的静态资料图；新的 PNG 资源图集才是外观验证基准。

## 数据原则

`property 22` 下发的是 `ride_code`，其值由 `ride_code = image_id - image_base` 得到。`image_base`、资源路径和 54 个主骑乘资源全部在 `mount_appearance_mapping.json` 中维护。生成器不维护第二套坐骑清单。

`411xx` 继续按 APK 行为视为骑手/鞍具接口层，不计为独立坐骑。没有从 APK 或其他已确认资料中得到的坐骑名称不会猜测；当前已确认 `41004 -> ride_code 1004 -> role_model 102000 -> 辟邪`。
