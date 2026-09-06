# 动态 map.ref 下发协议锁定

更新时间：2026-09-06

本记录修正旧结论“1407 不能替代 APK-local `.map.ref`”。该结论已经被当前 APK 的 DEX 调用链推翻。

## 结论

客户端原生支持两条等价的 `.map.ref` 来源：

1. 本地 `assets/res/map/{mapId}.map.ref`；
2. 服务端通过 `1407` subtype `11/12` 分块下发到内存。

两条路径最终都写入 `pmsj.work.b.m.z`，并由 `pmsj.work.b.m.C()` 解析。因此新地图不需要重新打包 APK，只要客户端已有其引用的全局 Image ID 美术资源，服务端即可动态提供新的 `.map.ref`。

## 进入地图协商

服务端先发送 `1110`，客户端从其中取得当前逻辑 `mapId`。随后客户端检查当前地图本地资源并发送：

- `1010 [short(12), int(local_map_o_size)]`：查询/协商逻辑地图数据；
- `1010 [short(13), int(local_map_ref_size)]`：查询/协商地图复合图块引用数据。

不存在本地文件时长度为 `0`。

当前兼容服原有 `1010/12 -> 1407 subtype 0/1/3/5/7 -> 1010/action=12 status=1` 路径继续负责逻辑地图、tile、collision 和 mirror。

## map.ref 网络帧

APK 的 `1407 subtype 11/12` 最终调用：

```text
pmsj.work.b.m.a(short totalLength, short offset, byte[] chunk)
```

客户端行为：

```text
if m.z == null:
    m.z = new byte[totalLength]

arraycopy(chunk, 0, m.z, offset, chunk.length)

if offset + chunk.length >= totalLength:
    m.C()
```

对应 S->C TLV 字段顺序固定为：

```text
1407 [
  byte(subtype),       # 首块 11，后续块 12
  short(total_size),
  binary(chunk),
  short(offset)
]
```

当前兼容实现使用 12000 字节一块。由于 APK 使用 Java `short` 保存总长度与 offset，兼容实现明确限制单个 `.map.ref` 不超过 `32767` 字节，超限时拒绝发送而不是截断或回绕。

## 完成后的 1010/13

当服务端已经通过 1407/11+12 填充并触发 `m.C()` 后，服务端发送：

```text
1010/action=13 status=1
```

表示不要再执行 APK-local `{mapId}.map.ref` 打开路径。随后沿原进入链继续：

```text
1010/action=14
1010/action=105
```

NPC、怪物、传送点和其他地图实体沿现有协议继续下发。

如果服务器端不存在 `maps/{mapId}.map.ref`，兼容层保持旧行为，完全回退到原 `server.py` 的 APK-local `.map.ref` 路径，因此 58 等已预置地图不受影响。

## mapworld.o

`1407 subtype=15` 使用同类的 `total/chunk/offset` 分块机制写入 `pmsj.work.b.p.d`。`pmsj.work.e.bn.ag()` 优先解析该内存数据，本地 `mapworld.o` 仅为备用来源。这进一步确认地图世界资源原生支持运行时下发。

## 兼容服实现

入口：

```text
server_dynamic_maps.py
```

资源约定：

```text
implementation_staging/maps/{mapId}.map.ref
```

`restart_server.ps1` 已切换为启动该入口。该入口只 monkey-patch `server.map_enter_frames`，其余 `server.py` 的登录、战斗、NPC、背包、持久化和其他协议实现保持不变。

测试：

```text
tests/test_dynamic_map_ref_transfer.py
```

覆盖：

- 首块 subtype=11、续块 subtype=12；
- `total_size`、`offset` 和完整 payload 重组；
- 无服务端 `.map.ref` 时回退旧 APK-local 路径；
- 有服务端 `.map.ref` 时将 `1010/action=13` 切换为 `status=1`。

## 对旧 PROTOCOL_LOCK 的修正

旧文档中如下表述不再成立：

> `1407` 负责逻辑地图、阻挡和镜像数据，但不能替代客户端渲染器所需的 `.map.ref`。

应以本记录为准：

> `1407 subtype 11/12` 可以直接下发完整 `.map.ref` 二进制，并进入与本地 `.map.ref` 相同的 `m.z -> m.C()` 解析路径。
