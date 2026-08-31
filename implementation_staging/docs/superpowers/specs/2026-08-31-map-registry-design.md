# 独立地图注册表与多传送点设计

状态：用户已于 2026-08-31 确认实施；58 地图名称定为“长安”。

## 目标

把当前“58 地图占用全局 `Settings`、50000 地图由条件分支临时替换”的结构迁移为独立地图注册表。每张地图独立拥有名称、地图文件、出生点、地图引用策略、妖兽、NPC 和任意数量传送点；传送点自身声明目标地图及落点。运行时不得让未知地图继承 58 的配置。

本次同时补齐当前测试已经期待、服务端尚未实现的多传送点能力：58 地图生成 `580001`、`580003` 两个前往 50000 的传送点，50000 地图生成 `580002` 返回 58。

## 非目标

- 不修改 `.map.o`、`.map.ref`、APK 图集或地图素材。
- 不增加多妖兽战斗；每张地图本轮仍最多配置一个本地试炼妖兽。
- 不实现地图分线、动态副本、跨服或热重载。
- 不改变已经确认的 `1010`、`1110`、`1126`、`2030` 字段布局。

## 现状与问题

当前 `Settings` 顶层字段 `map_id/map_name/spawn_x/spawn_y/map_o_file` 实际代表 58；NPC 函数直接判断 `map_id == 58`。`settings_for_map()` 只特殊处理 `portal_target_map_id`，其他 ID 只替换 `map_id`，因此会错误继承 58 的地图文件、名称、实体和坐标。

`config.json` 已写入 `portals` 数组，但 `Settings` 没有该字段，加载时会静默丢弃。服务端仍只生成单个 `portal_id`，而 `tests/test_protocol.py` 已按多传送点接口导入 `map_portal_frames`，造成完整测试无法收集。

## 方案比较与选择

### 方案 A：继续扩充顶层字段

为每张地图增加 `map_50000_*`、`map_XXXXX_*` 字段。改动最小，但每增加地图都要改数据类、分支和传送逻辑，无法解决继承错误，不采用。

### 方案 B：保留字典，业务代码直接读取原始 JSON

配置迁移简单，但字段类型、默认值和目标地图校验散落在协议代码中，错误只能在玩家进入地图时暴露，不采用。

### 方案 C：类型化地图注册表（采用）

新增独立 `map_registry.py`，集中解析、验证和查询地图。`server.py` 只消费 `MapDefinition`、`PortalDefinition` 等稳定接口。配置在启动时完成校验，协议函数不再猜测或回退到 58。

## 配置模型

服务器级配置保留监听地址、账号策略、角色默认值、心跳和存档路径；地图级字段移动到 `maps`。`default_map_id` 决定新角色初始地图。

```json
{
  "host": "0.0.0.0",
  "port": 6805,
  "advertise_host": "192.168.0.104",
  "default_map_id": 58,
  "maps": {
    "58": {
      "name": "长安",
      "map_o_file": "maps/58.map.o",
      "map_ref_available": true,
      "fallback_width": 96,
      "fallback_height": 96,
      "spawn": {"x": 60, "y": 67},
      "monster": {
        "id": 1900001,
        "name": "试炼妖兽",
        "model": -2004250,
        "x": 9,
        "y": 28,
        "direction": 0
      },
      "npcs": [
        {"id": 1900002, "name": "孙思邈", "label": "药王", "x": 50, "y": 64},
        {"id": 1900003, "name": "接引真人", "label": "接引", "x": 34, "y": 50},
        {"id": 1900004, "name": "赵公明", "label": "赵公明", "x": 11, "y": 21}
      ],
      "portals": [
        {
          "id": 580001,
          "name": "跨地图传送点",
          "model": -2004250,
          "x": 55,
          "y": 55,
          "direction": 0,
          "target_map_id": 50000,
          "target_x": 8,
          "target_y": 6
        },
        {
          "id": 580003,
          "name": "跨地图传送点",
          "model": -2004250,
          "x": 34,
          "y": 7,
          "direction": 0,
          "target_map_id": 50000,
          "target_x": 8,
          "target_y": 6
        }
      ]
    },
    "50000": {
      "name": "传送测试区",
      "map_o_file": "maps/50000.map.o",
      "map_ref_available": true,
      "fallback_width": 90,
      "fallback_height": 90,
      "spawn": {"x": 8, "y": 6},
      "monster": {
        "id": 1900001,
        "name": "试炼妖兽",
        "model": -2004250,
        "x": 12,
        "y": 8,
        "direction": 0
      },
      "npcs": [],
      "portals": [
        {
          "id": 580002,
          "name": "返回长安",
          "model": -2004250,
          "x": 9,
          "y": 6,
          "direction": 0,
          "target_map_id": 58,
          "target_x": 60,
          "target_y": 67
        }
      ]
    }
  }
}
```

加载器在一个兼容周期内接受现有扁平配置，并把它转换为等价的 58/50000 注册表；项目内 `config.json` 迁移为上述新格式，成为唯一文档化格式。

## 组件与接口

`map_registry.py` 提供：

- `MapActorDefinition`：妖兽/NPC 绘制所需的稳定标识、模型、坐标和方向。
- `PortalDefinition`：传送点实体及 `target_map_id/target_x/target_y`。
- `MapDefinition`：一张地图的文件、引用策略、默认出生点、妖兽、NPC、传送点。
- `MapRegistry.require(map_id)`：返回已验证地图；未知 ID 抛出明确异常，不回退。
- `MapRegistry.portal(map_id, object_id)`：只在当前地图查找传送点。
- `load_map_registry(payload, npc_catalog)`：解析新格式或兼容旧扁平格式，合并 NPC 资源目录并执行启动校验。

`Settings` 保存 `default_map_id` 与 `map_registry`。现有 `settings_for_map()` 保留为兼容入口，但返回 `MapDefinition`；`settings_for_role()` 根据角色 `map_id/map_x/map_y` 返回带有效进入坐标的地图副本。

## 数据流

### 登录与恢复

新角色写入 `map_id=default_map_id` 以及该地图默认 `map_x/map_y`。旧角色缺少坐标时按其当前地图默认出生点补齐；旧角色地图不存在时记录警告并安全迁回默认地图。地图名称不再以角色存档为权威，`1110` 始终从注册表派生，旧 `map_name` 字段保留但忽略，避免破坏现有 JSON。

### 地图数据与实体生成

`1010/action=12` 通过当前 `MapDefinition.map_o_file` 发送 `1407` 数据；文件读取失败时只使用该地图自己的 fallback 尺寸。`1010/action=13` 使用当前地图的引用策略和角色落点，按配置依次生成可选妖兽、全部传送点、当前地图 NPC 及对应方向帧。NPC 不再写死 58。

### 多传送点

收到 `1010/action=7` 或 `2031` 后，服务端先在当前地图注册表中按对象 ID 查找传送点。命中后将角色 `map_id/map_x/map_y` 更新为该传送点目标并保存，再发送目标地图的 `1110`；客户端继续正常请求 `1010/12`、`1010/13`。同一个对象 ID 在当前地图只允许出现一次，跨地图也保持全局唯一以便日志与排错。

妖兽和 NPC 交互只使用当前地图的实体集合，不能命中其他地图同 ID 对象。

## 校验与错误处理

启动时拒绝以下配置：

- `default_map_id` 不存在；
- 地图键与内部 ID 不一致；
- 地图、妖兽、NPC 或传送点缺少必填字段；
- 地图 ID、地图内对象 ID 或全局传送点 ID 重复；
- 传送点目标地图不存在；
- 出生点、实体坐标或传送落点为负数，或超出该地图 fallback 尺寸；
- fallback 尺寸不在协议可编码范围 `2..127`。

运行时角色引用未知地图时迁回默认地图；网络请求携带未知对象 ID 时维持现有“记录并忽略”行为，不产生猜测性传送。

## 兼容与迁移

- 保留现有协议消息及字段类型。
- 保留 `settings_for_map()` 函数名，降低现有测试和调用方迁移成本。
- 提供旧扁平 `config.json` 到注册表的加载兼容测试，但仓库内配置立即切换为新格式。
- `data/npcs.json` 继续作为资源补充目录：只覆盖注册表中已有同 ID NPC 的 `dat_id/model` 等资源字段；不再把缺少坐标的孤立条目追加为可生成 NPC。
- 角色存档仅增补 `map_x/map_y`；不删除旧 `map_name`，不重建账号或道具。

## 测试策略

1. `tests/test_map_registry.py` 覆盖新配置解析、旧配置兼容、未知地图、重复 ID、坏坐标和无效目标。
2. `tests/test_protocol.py` 覆盖 58/50000 独立属性、两个前向传送点、一个返回传送点、方向帧及 NPC 地图隔离。
3. 对传送状态转换增加角色 `map_id/map_x/map_y` 持久化测试，验证两个 58 传送点都能到达 50000，返回点能回到 58。
4. 运行 `python -m unittest discover -s tests -v`，消除当前 `map_portal_frames` 导入错误。
5. 在隔离端口运行 `test_client.py --exercise-role-crud --exercise-portal`，确认登录、背包、地图数据和往返传送闭环。

## 涉及文件

- 新建 `map_registry.py`：地图配置模型、解析、兼容迁移和校验。
- 修改 `server.py`：Settings、角色地图迁移、地图协议、实体生成和传送路由。
- 修改 `config.json`：迁移到 `default_map_id + maps`。
- 新建 `tests/test_map_registry.py`，修改 `tests/test_protocol.py`、`test_client.py`。
- 更新 `README.md`、`PROTOCOL_LOCK.md` 与交接文档中的地图配置说明。

## 完成标准

- 58 和 50000 均从注册表取得完整且互不继承的配置。
- 58 同时生成 `580001`、`580003`，两者均可进入 50000；50000 生成 `580002` 并可返回 58。
- `config.json` 的 `portals` 不再被静默忽略。
- 未知地图不能复用 58 的名称、地图文件、出生点或实体。
- 旧角色与旧扁平配置可无损加载。
- 完整单元测试和隔离 TCP 传送测试通过。
