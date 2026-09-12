# 任务系统设计

日期：2026-09-12

## 目标

在本地兼容服中建立服务端权威任务系统，并复用 APK 已存在的任务界面与 1403/1145 协议，不新增客户端 UI、不访问任何官方/第三方服务器。

## APK 证据

上传 APK 的 `pmsj/work/e/ca`、`em`、`en` 已确认任务页包含主线、支线、循环、每日和神炼任务，以及领取、提交、放弃、任务说明、目标与奖励选择。客户端 `main/e` 将消息 1403 路由到任务处理器 `ad(w)`；该处理器已确认响应 action 2/3/6/7/9/12/13/14/15/20/22/23/40/50/51/52/53。客户端请求端已确认：

- `1403 [BYTE 6, BYTE, BYTE, BYTE]`：已接任务列表/分类刷新。
- `1403 [BYTE 50, BYTE, BYTE]`：可领取任务列表刷新。
- `1403 [BYTE 15|22|52, INT task_id]`：任务说明/详情。
- `1403 [BYTE 7, INT, INT, BYTE, BYTE]`：任务操作。
- `1145 [BYTE 0, INT, BYTE, BYTE]`：从可领取列表执行任务动作。
- `1145 [BYTE 0, INT, BYTE, BYTE, INT]`：已接任务提交路径。

1403 action 6 写入客户端 `b/f.v`（按类别分组的已接任务），action 50/52 写入 `b/f.w`（可领取/任务候选列表）。当前服务端把 1403 放在 `MENU_PREFETCH_EMPTY_SUBTYPES` 中，仅返回安全空应答，因此任务系统尚未实现。

## 架构

新增三个独立模块：

1. `task_registry.py`：从 JSON 加载任务定义，启动时做完整校验。任务定义只保存静态资料：类别、前置、等级要求、目标、奖励、重复策略和客户端路由元数据。
2. `task_service.py`：纯业务状态机。玩家存档仅保存任务状态、目标进度、接取/完成时间、循环次数和每日计数。服务通过统一事件 API 更新进度，首批支持 `monster_killed`、`item_gained`、`npc_talked`、`map_entered`、`battle_won`、`item_submitted`。
3. `task_protocol.py`：只负责 1403/1145 的严格 TLV 请求识别与 S->C 帧构造，不承担业务判断。

`server.py` 只做编排：加载 registry、迁移角色任务状态、把 1403/1145 请求交给 task service、保存角色、发送协议帧，并在已经存在的战斗胜利/地图进入/物品获得路径发布任务事件。

## 数据模型

任务定义的稳定字段：`task_id/category/name/description/level_requirement/prerequisites/objectives/rewards/repeat_policy/daily_limit/client_route`。目标为 `{kind,target_id,required}`；奖励首批支持经验、银两和已有 item template。

角色新增 `tasks`：

```json
{
  "version": 1,
  "active": {
    "10001": {
      "status": "active",
      "progress": [0],
      "accepted_at": 0,
      "completed_at": 0,
      "cycle_count": 0
    }
  },
  "completed": {"10000": 1},
  "daily": {"date": "YYYY-MM-DD", "counts": {}}
}
```

旧 `roles.json` 角色无 `tasks` 时按空状态迁移，不覆盖已有角色/物品字段。

## 状态机

`available -> active -> ready -> claimed`。可重复任务在 `claimed` 后依据 repeat policy 回到 available；一次性任务记录进 completed。`abandon` 仅允许 active/ready，删除活动状态但不破坏历史完成计数。所有状态转换先校验后变更，失败不部分写入。

## 协议兼容策略

协议编码只使用 APK 已证明的消息号、action 和请求字段类型。对于服务端响应中尚未能从客户端静态代码唯一证明的记录字段，集中封装在 `task_protocol.py` 并以客户端读取索引为依据，禁止散落到 server.py。未知 action 保留安全日志与无副作用处理，不猜测字段。

首个闭环目标：打开任务页可见本地任务；领取后进入已接列表；目标事件推进进度；完成后可提交领奖；重新登录保持状态。任务文本和奖励明确标注为本地兼容服数据，不冒充原服任务资料。

## 初始本地任务

先提供五类各一条最小任务，用于验证客户端五个分类与状态机；内容只引用本地服已经存在的地图、试炼妖兽和物品资源。后续从 APK/JAR 或其他可靠样本恢复原任务时，只替换 catalog，不改变引擎。

## 错误与一致性

- catalog 启动校验失败时拒绝启动任务模块并给出明确错误。
- 重复领取、未完成提交、重复领奖、未知 task id 均不改存档。
- 奖励发放需先检查背包容量；奖励失败时任务不进入 claimed。
- 每次成功状态转换立即调用现有 RoleStore.save()。
- 每日任务按本地日期懒重置，仅清每日计数，不删一次性完成记录。

## 测试

按 TDD 增加 registry、service、protocol 与 server integration 单元测试。必须验证旧角色迁移、前置条件、接取/放弃、目标增量、完成/领奖、每日限制、重登恢复，以及 1403/1145 的精确字段类型和关键响应 record 布局。最终运行项目标准命令：`python -m unittest discover -s tests -v`。网络与真机验收仍由用户在本地 6805 环境执行。