# 翠溪村 60011 本地地图包

`source_scene.png` 是用户在“生成地图素材调用”对话中选定的图二场景图。
`build_map_60011_apk.ps1` 保持原比例缩放为 675×900，切成 5×8 共 40 块，
注册 Image ID `60011000..60011039`，生成 `map.ref.json`、`map.json`，
再把二进制地图和 `images.o/png*.p` 注入本地测试 APK 并使用原本地测试密钥签名。
仓库以 JSON 和源图为构建源；`maps/60011.map.ref/.map.o` 是脚本生成物。

地图逻辑大小 90×90，入口保留长安 `(50,70)`，本图出生点 `(50,33)`，
返回点 `(52,35)`。水、瀑布、房屋、中央悬崖以及画面外区域设为不可走，
右侧草地和道路保持可走。`preview.png` 是资源回读的离线渲染预览，
不能替代客户端渲染和碰撞验收。

## APK Verification

- 客户端可观察影响：60011 的画面、地形尺寸、碰撞与入口/返回位置。
- MessageID：沿用 `1010/13` 地图进入、`1407/11|12` 资源下发及已有地图逻辑数据流；
  未新增消息号、Action、Property 或改变字段类型与顺序。
- 资源：`60011.map.ref/.map.o`、`images.o`、`png201.p..png240.p` 和上述 40 个 Image ID。
  具体 `png*.p` 编号由源 APK 索引末位决定，脚本会检查空余与 ID 冲突。
- APK 依据：原 APK 的 `assets/res/map/58.map.ref`、`images.o/png*.p`；
  `tools/map_ref_generator.py` 的结构往返验证；`tools/map_ref_renderer.py`
  按原图像容器结构重建 PNG 并离线渲染；地图协议见 `systems/map/protocol.py`。
- 证据等级：**B**（客户端资源格式与地图流有静态直接证据；新场景与碰撞是本地兼容值）。
- 测试：`test_map_60011_package`、`test_map_system`；打包后回读 40 张图片、
  检查地图大小、出生/返回点通行、签名验证与预览检查。
- 真机状态：`pending real-device verification`。重点检查画面切片是否随移动突然消失、
  角色与场景前景的遮挡关系，以及水边、房屋、悬崖和传送点的实际碰撞。
