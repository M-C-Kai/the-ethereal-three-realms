# `.map.o` 生成器

`tools/map_o_generator.py` 用可编辑的 JSON 描述生成原客户端能够读取的 `.map.o`，并验证其中的图块引用是否超出对应 `.map.ref`。

## 已确认的客户端格式

客户端 `pmsj.work.b.m.o()` 按以下顺序读取：

| 顺序 | 长度 | 含义 |
|---|---:|---|
| 1 | 1 | 图块定义数量 N，兼容范围 1～128 |
| 2 | N × 2 | 大端 signed short；每项指向 `.map.ref` 的复合图块 |
| 3 | 5 | 原客户端直接跳过；原始 58 地图为 `map_type,width,height,20,10`，末两项对应客户端固定的等距图块像素宽高 |
| 4 | width × height | 行优先地表网格；`0..N-1` 是本地定义索引，`255` 表示无图块 |
| 5 | ceil(格数/8) | 阻挡位图，低位优先；1 表示不可行走 |
| 6 | ceil(格数/8) | 图块翻转位图，低位优先；1 使用客户端翻转绘制分支 |

宽高不是由原客户端从 `.map.o` 的五个跳过字节读取的。正常进入地图时，服务器先用 `1407/0` 告诉客户端地图类型和宽高。APK 地图类的静态初始化把等距图块宽高设为 20×10，和原始 `58.map.o` 的后两个头部字节完全一致。本工具完整保留这五项，项目服务端仍按原协议下发 `1407/0`。

传送点、NPC、任务触发和出生点不在这段本地读取格式中。出生点仍由 `config.json` 的 `spawn_x/spawn_y` 控制；其他对象需要以后实现对应游戏服协议。

## 58号引用数据（不是仙石村）

生成器已用客户端相同的记录边界完整解析 `58.map.ref`。`mapworld.o` 已确认仙石村真实地图 ID 为 50000、仙石村郊为 50001；地图 58 不在世界地图表中，因此下面这些数据不能再称为仙石村资源：

- 115 个复合图块；
- 135 个图片记录；
- 27 个唯一图片包编号；
- 4964 字节全部被记录解析器消费，没有尾部未知数据。

`tile_definitions` 保存的是 0～114 的复合图块编号，不是 `png<ID>.p` 的 ID。`tiles` 网格再通过 0～127 的局部索引选择 `tile_definitions`。缺失的原始网格排列无法从图片 ID 直接确定，需要人工编辑、画面匹配算法或原服数据。

## 使用方法

从 APK 读取 `58.map.ref` 并创建 16×12 模板：

```powershell
python tools\map_o_generator.py template `
  --apk C:\Users\Kail\Downloads\base.apk.1 `
  --map-id 58 --width 16 --height 12 --tile 0 `
  -o maps\58.map.json
```

编辑 `maps/58.map.json` 后生成并校验：

```powershell
python tools\map_o_generator.py build maps\58.map.json `
  --apk C:\Users\Kail\Downloads\base.apk.1 --map-id 58 `
  -o maps\58.map.o
```

检查生成文件，或反向导出 JSON：

```powershell
python tools\map_o_generator.py inspect maps\58.map.o `
  --apk C:\Users\Kail\Downloads\base.apk.1 --map-id 58

python tools\map_o_generator.py inspect maps\58.map.o `
  --dump-spec maps\58.roundtrip.json
```

服务端启动时读取 `config.json` 的 `map_o_file`，把定义表、RLE 地表网格、阻挡和翻转位图转换成 `1407/0,1,3,5,7`。传送目标 50000 使用 `maps/50000.map.o`（32×32 草地、全部可行走）；重新生成服务端地图后只需重启服务，只有修改 APK 内的 `50000.map.o` 才需要重新打包安装。

## JSON 字段

```json
{
  "width": 4,
  "height": 3,
  "map_type": 0,
  "tile_pixel_width": 20,
  "tile_pixel_height": 10,
  "tile_definitions": [0, 114],
  "tiles": [
    [0, 0, 1, null],
    [0, 1, 1, null],
    [0, 0, 0, 0]
  ],
  "collision": [
    ".#..",
    "....",
    "...."
  ],
  "mirror": [
    "....",
    "..#.",
    "...."
  ]
}
```

- `null` 会写为 `255`，客户端把它当作没有地表图块。
- `collision` 中 `#` 表示阻挡，`.` 表示可通行。
- `mirror` 中 `#` 表示启用该格图块的翻转绘制。
- 地图宽高上限按客户端 signed byte 限制为 127；局部图块定义最多 128 项。

`maps/58.reconstructed.map.json` 只是 APK 中58号逻辑地图的可编辑语义表示；用生成器回编译出的 `maps/58.reconstructed.map.o` 可与 APK 原始文件逐字节核对，但它不是仙石村。`maps/50000.map.json` 是当前传送闭环使用的空地逻辑地图；仙石村候选重建仍位于 `maps/xianshi-50000/`，不会自动替换这个安全的最小地图。
