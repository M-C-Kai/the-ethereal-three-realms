# 任务协议（APK 静态证据 + 本地兼容层）

## 范围

本文只记录当前 APK 可静态确认的任务协议。任务资料和奖励数值是本地兼容服数据，不代表原服资料。未能从客户端读取代码唯一确认的字段不在 `server.py` 中猜测。

## 1403 C->S

APK `pmsj/work/e/ca` 与 `pmsj/work/main/w` 已确认：

- 已接任务刷新：`1403 [BYTE 6, BYTE, BYTE, BYTE]`
- 可领取任务刷新：`1403 [BYTE 50, BYTE, BYTE]`
- 任务说明/详情：`1403 [BYTE 15|22|52, INT task_id]`
- 任务操作：`1403 [BYTE 7, INT, INT, BYTE, BYTE]`

服务端必须同时校验字段个数、类型与 action；数值相同但 TLV 类型不同不视为同一请求。

## 1145 C->S 任务形状

任务界面存在两种 `action=0` 形状：

- 可领取列表操作：`1145 [BYTE 0, INT route_id, BYTE category, BYTE route_kind]`
- 已接任务操作：`1145 [BYTE 0, INT route_id, BYTE operation, BYTE category, INT task_id]`

已接任务兼容记录中 `operation=2` 表示提交，`operation=4` 表示放弃。其他 1145 形状（尤其地图寻路）必须继续落到原有路由，不能被任务处理器吞掉。

## 1403 S->C action 6

`main/e.ad(w)` 对 action 6 的已确认布局：

```text
[0] BYTE  6
[1] SHORT record_count
[2] BYTE  record_width
[3] BYTE  category
[4..] records
```

类别 wire id：主线=1、支线=2、循环=3、每日=4、神炼=6。

本地兼容记录宽度固定为 9：

```text
INT task_id
STRING name
INT marker
INT level_requirement
INT detail_mode
INT route_id
BYTE operation
BYTE category
INT task_id
```

其中未完成任务 `operation=4`，已完成待提交任务 `operation=2`；`detail_mode=4` 仅用于待提交状态。

## 1403 S->C action 50

`main/e.ad(w)` 对 action 50/52 的已确认头：

```text
[0] BYTE  action
[1] SHORT record_count
[2] BYTE  record_width
[3..] records
```

本地兼容的可领取任务使用 action 50，记录宽度固定为 6：

```text
INT task_id
STRING name
INT status           # 0 = 未领取
INT route_id
BYTE category
BYTE route_kind
```

这些索引来自 `ca` 对 `b/f.w` 的读取：`[0]` 用作任务 id、`[1]` 显示名称、`[2]` 显示状态，`[3..5]` 用于 1145 操作路由。

## 详情页限制

1403 action 15/22/52 会进入 `pmsj/work/e/em`，其 `ag()` 会继续读取一组较长的详情/目标/奖励结构。该结构尚未完全锁定，因此当前实现对详情请求返回：

```text
1403 [BYTE 1]
```

action 1 在现有 `main/e.ad` 中未构造详情页，只释放等待状态。这样比猜测字段并导致旧客户端错位/闪退更安全。完整详情页作为后续 APK 追踪项，不影响列表、领取、进度、提交和持久化引擎本身。
