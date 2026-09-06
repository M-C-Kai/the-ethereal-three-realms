# 动态地图标准

后续新增地图默认使用服务器动态地图包，不再把 `<mapId>.map.ref/.map.o` 注入 APK，也不再为每张地图编写 `generate_map_<id>.py`。

## 目录

```text
implementation_staging/maps/
  60010/
    map.json
    map.ref.json
  60011/
    map.json
    map.ref.json
```

目录名必须是十进制 `mapId`。只有同时存在 `map.json` 与 `map.ref.json` 的数字目录才会被扫描为动态地图包。

服务器启动 `server_dynamic_maps.py` 时会：

1. 扫描全部数字地图包。
2. 将 `map.ref.json` 编译并往返校验为 `maps/<id>.map.ref`。
3. 将 `map.json` 编译并按对应 map.ref 校验为 `maps/<id>.map.o`。
4. 把 `map.json.registry` 自动合并进运行时地图注册表。
5. 把 `registry.inbound_portals` 自动挂到来源地图，因此不需要再修改 `config.json`。
6. 客户端请求目标地图时按已经真机验证的顺序下发：

```text
1010/action13 status=1
→ 1407/11+12 map.ref
→ 1010/action14
→ 1010/action105
```

`action13` 必须在 1407 map.ref 之前。反过来会让客户端在旧 renderer 上直接解析新 ref，表现为地图画面从屏幕上方向下铺，而不是原生切图动画。

## map.ref.json

格式固定为 `piaomiao-map-ref-v1`：

```json
{
  "format": "piaomiao-map-ref-v1",
  "map_id": 60011,
  "image_records": [],
  "composite_tiles": []
}
```

`image_records` 与 `composite_tiles` 使用 `tools/map_ref_generator.py` 已锁定的 APK 原生结构。动态 map.ref 仍只能引用 APK `images.o` 已存在的 Image ID；服务器下发的是组合/裁剪/图层定义，不会凭空增加新的底层图片资源。

## map.json

格式固定为 `piaomiao-dynamic-map-v1`。地图布局字段直接对应 `MapO`：

```json
{
  "format": "piaomiao-dynamic-map-v1",
  "map_id": 60011,
  "width": 24,
  "height": 24,
  "map_type": 0,
  "tile_pixel_width": 20,
  "tile_pixel_height": 10,
  "tile_definitions": [0],
  "tiles": [
    "0 0 0 0",
    "0 0 0 0"
  ],
  "collision": ["....", "...."],
  "mirror": ["....", "...."],
  "registry": {
    "name": "新地图",
    "spawn": {"x": 1, "y": 1},
    "npcs": [],
    "portals": [],
    "inbound_portals": []
  }
}
```

`tiles` 可以继续使用二维整数数组，也可以使用空格或逗号分隔的字符串行。`.` / `null` / `none` 表示空地块。

### registry

`registry` 至少需要：

- `name`
- `spawn.x/y`

可选使用现有地图注册表支持的 `monster`、`npcs`、`portals`。

动态地图的以下字段由构建器强制生成，不应手填：

- `id`：来自目录名/map_id
- `map_o_file`：固定 `maps/<id>.map.o`
- `map_ref_available`：固定 `false`，确保走服务器 1407 下发而不是 APK-local lookup
- `fallback_width/height`：来自 map.json 的 width/height

### inbound_portals

用于把进入当前动态地图的传送点挂到别的地图：

```json
{
  "source_map_id": 58,
  "id": 580011,
  "name": "前往新地图",
  "model": -2043000,
  "x": 64,
  "y": 67,
  "direction": 0
}
```

`target_map_id` 默认就是当前包的 mapId，`target_x/target_y` 默认就是当前地图 spawn。需要时可以显式写 target_x/target_y；target_map_id 若填写则必须等于当前包 mapId。

## 60010 基准

60010 已迁移为第一份标准动态地图包：

```text
maps/60010/map.json
maps/60010/map.ref.json
```

它不再出现在 `config.json`，长安的 580006 入口也不再出现在 `config.json`；两者都由地图包在启动时自动注册。

迁移前后资源必须保持：

```text
60010.map.ref  122 bytes
SHA256 7eb419659ca28a006bc0c1a0980e863472fcdd45149c5e90076e1f991c7afceb

60010.map.o    738 bytes
SHA256 f92cb8de6d5816e3311c2ad73f2ebfcbd069526da4349aa81855fda8ed8b3a4a
```

因此 60010 同时是以后动态地图构建管线的回归基准。
