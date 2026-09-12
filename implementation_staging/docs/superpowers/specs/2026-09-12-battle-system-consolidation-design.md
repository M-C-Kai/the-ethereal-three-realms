# 战斗系统整合设计

## 目标

把当前分散在 `server.py`、`server_pets.py`、`battle_escape_guard.py` 和协议测试中的战斗逻辑整理成一个边界清晰、可独立测试的 `battle` 子系统。

本次工作首先是**结构重构**：保持当前已经真机验证或 APK 静态确认的协议、表现和战斗行为不变，不趁重构修改伤害公式、怪物 AI、技能系统、掉落概率或客户端协议。

## 当前问题

当前战斗职责分散在多个位置：

- `server.py`
  - `LocalBattleState`
  - 1040 / 1041 / 1042 / 1048 等战斗协议编码
  - 战斗资源分发
  - 战斗开始、回合、攻击、逃跑、结束
  - 胜利奖励、经验、掉落、升级
  - 地图对象触发战斗和逃跑后的重复触发保护
- `battle_escape_guard.py`
  - 逃跑后 1 格 / 2 秒重触发策略
- `server_pets.py`
  - 为移动 Boss 做 2029 -> 2031 战斗入口桥接
  - 将 1005 接近 Boss 改写为战斗交互
  - monkey-patch `LocalBattleState.set_escape_guard`
  - monkey-patch `should_suppress_escape_retrigger`
  - monkey-patch `update_escape_guard_for_movement`
- `tests/test_protocol.py`
  - 大量战斗协议、状态和行为测试与其他系统测试混在一起
- `tests/test_battle_escape_guard.py`
  - 单独验证逃跑保护
- `tests/test_roaming_boss_interaction.py`
  - 地图 Boss 交互测试中同时覆盖战斗入口

这导致战斗状态机存在多个入口和替换层，后续扩展技能、宠物参战、多怪、AI 时容易再次出现锁状态和生命周期不同步的问题。

## 总体边界

新增包：

```text
implementation_staging/battle/
├── __init__.py
├── state.py
├── protocol.py
├── engine.py
├── encounter.py
├── rewards.py
└── resources.py
```

职责如下。

### `battle/state.py`

只保存和修改一次战斗会话的权威状态。

包含：

- `CombatStats`
- `LocalBattleState`
- 玩家与怪物 HP
- 当前回合
- 当前 phase
- fighter / monster id 集合
- `monster_defeated`
- `player_tile`
- `map_id`
- `contact_tile`
- `escape_guard`
- `begin()` / `finish()` / `reset_encounter()` / `escape()`
- 基础伤害状态变更函数

逃跑保护归属于状态对象本身，不再由 `server_pets.py` 替换方法。

`escape_guard` 的统一规则：

- 逃跑成功后记录 `map_id / monster_id / player_id / contact_tile / created_at`。
- 同图同怪在保护期内禁止立即重新开战。
- 满足以下任一条件后解除：
  1. 玩家离开 `contact_tile` 的 1 格范围；
  2. 保护建立满 2 秒。
- 计时使用 `time.monotonic()`。
- 普通胜利结束不建立逃跑保护。

### `battle/protocol.py`

只负责 APK 战斗协议的编解码和字段类型契约，不拥有业务状态。

迁入并保持现有行为的内容：

- 1040：reset / start / progress / end
- 1041：玩家命令解析、逃跑结果
- 1042：战斗动作及效果记录
- 1048：fighter 创建/更新
- 1049：奖励层
- 1010 中与战斗结束/地图怪物移除有关的编码助手
- 与战斗协议直接相关的字段类型验证

必须保留 APK 已确认类型：byte / short / int 不互换。

### `battle/engine.py`

只处理战斗中的回合和裁决，不处理地图、不处理网络 socket。

包含：

- `battle_command_target_id()`
- 普通攻击伤害计算
- 防御状态
- 玩家命令合法性检查
- 怪物基础 AI 决策
- 回合推进
- 怪物 HP / 玩家 HP 更新
- 生成“本回合发生了什么”的领域结果

现阶段只迁移现有能力，不新增完整技能公式。

引擎结果由 `server.py` 或 encounter 层转换成协议帧；引擎本身不直接写 socket。

### `battle/encounter.py`

负责战斗生命周期和“地图事件如何进入/离开战斗”。这是本次整合的核心。

统一管理：

- 地图对象手动触发战斗
- q 明雷怪 `2029 [BYTE 1, INT actorId]` 触发战斗
- 玩家移动 `1005` 靠近怪物自动触发战斗
- 重复触发抑制
- 逃跑后保护
- 玩家离开接触半径解除保护
- 2 秒超时解除保护
- 开战时把地图、怪物、接触格写入 `LocalBattleState`
- 战斗胜利 / 失败 / 逃跑后的会话终止

`encounter.py` 提供明确入口，建议接口：

```python
@dataclass(frozen=True)
class EncounterRequest:
    map_id: int
    monster_id: int
    player_id: int
    player_tile: tuple[int, int] | None
    monster_tile: tuple[int, int] | None
    source: str

@dataclass(frozen=True)
class EncounterDecision:
    start: bool
    suppressed: bool
    reason: str


def request_encounter(state: LocalBattleState, request: EncounterRequest) -> EncounterDecision:
    ...


def update_player_tile(state: LocalBattleState, x: int, y: int) -> bool:
    ...
```

`source` 只用于日志和诊断，允许值固定为：

- `map_interaction`
- `q_action`
- `proximity`

手动点击、q 菜单和靠近触发最终必须走同一个 `request_encounter()`，不能各自维护锁。

### `battle/rewards.py`

只处理胜利后的服务端结算。

迁入：

- `BATTLE_EXP_REWARD`
- `BATTLE_DROP_TEMPLATE_ID`
- `level_experience_required()` 中仅与战斗结算直接相关的使用逻辑
- `apply_one_level()` 的战斗调用封装
- `apply_battle_rewards()`
- 战斗奖励结果结构

角色基础等级公式如果同时被其他系统使用，则保留在公共角色模块；`rewards.py` 只调用它，不复制实现。

奖励层仍保持现有协议行为：胜利后更新人物数据、掉落和顶部奖励层；逃跑不发奖励。

### `battle/resources.py`

集中所有战斗场景资源解析和响应。

迁入：

- `BATTLE_RESOURCE_MODEL_OFFSET`
- `BATTLE_RESOURCE_ALIASES`
- `BATTLE_EMPTY_RESOURCE_IDS`
- `battle_resource_path()`
- `battle_resource_resolution()`
- `battle_resource_frames()`
- `battle_image_resource()`
- `battle_image_frames()`
- 相关 debug snapshot / resolve helper

这里只负责资源，不处理回合状态。

## `server.py` 的最终职责

`server.py` 保留网络主循环和非战斗系统。

战斗相关代码只保留薄适配层：

```text
收到客户端包
    ↓
解析 message_id / fields
    ↓
调用 battle 子系统
    ↓
拿到 frames / state transition
    ↓
发送 frames
```

`server.py` 不再自行实现：

- 战斗 HP 变更
- 战斗回合推进
- 逃跑 guard 规则
- 战斗奖励规则
- 1040/1041/1042/1048 编码细节

为了降低一次性迁移风险，`server.py` 可以在迁移期间暂时 re-export 已被其他测试/模块引用的旧函数名：

```python
from battle.protocol import battle_start_frame
```

调用方稳定后再删除兼容 re-export。本次整理不要求同步修改所有外部调用方名称。

## `server_pets.py` 的最终职责

`server_pets.py` 只维护宠物系统和移动 Boss 的地图层适配，不再修改战斗内部状态机。

允许保留：

- q 明雷怪协议识别
- Boss 当前地图坐标跟踪，直到地图系统拥有统一移动实体状态

必须移除：

- `_ORIGINAL_SET_ESCAPE_GUARD`
- 对 `LocalBattleState.set_escape_guard` 的 monkey-patch
- 对 `should_suppress_escape_retrigger` 的 monkey-patch
- 对 `update_escape_guard_for_movement` 的 monkey-patch

`server_pets.py` 识别到 q 战斗操作或接近事件后，只构造 `EncounterRequest` 并交给 battle encounter 层。

Boss 自身游荡仍属于地图系统，不放进 battle：

```text
地图系统：Boss 在哪里、怎么走
战斗系统：玩家与 Boss 是否进入战斗、战斗何时结束
```

## 战斗生命周期

统一生命周期如下：

```text
地图事件
  ├─ 手动交互
  ├─ q 菜单“战斗”
  └─ 靠近 1 格
        ↓
EncounterRequest
        ↓
encounter.request_encounter()
        ↓
检查 active / monster_defeated / escape_guard
        ↓
LocalBattleState.begin()
        ↓
protocol: 1040/action=0
        ↓
protocol: 双方 1048
        ↓
protocol: 1040/action=1
        ↓
等待 1041 玩家命令
        ↓
engine 裁决
        ↓
1042 动作 + 1040/action=2
        ↓
等待客户端 action=2 ACK
        ↓
下一回合 / 胜利 / 逃跑
```

胜利：

```text
最后动作完成
→ 1040/action=4
→ 地图怪物移除
→ rewards 结算
→ LocalBattleState.finish()
```

逃跑：

```text
1041 command=6
→ 离场动作
→ 客户端 action=2 ACK
→ 1.25 秒离场宽限
→ 1041 [10, player_id]
→ state.escape()
→ 建立 escape_guard
```

逃跑后重新允许战斗：

```text
离开 Boss 1 格范围
OR
escape_guard >= 2 秒
→ guard 解除
→ 下一次 encounter request 可开战
```

## 协议兼容约束

本次重构必须保持以下已确认行为：

- 1040 action 0/1/2/4 语义不变。
- 1041 C->S：1=攻击、2=防御、6=逃跑、8=召回、10=退出观战、12=待机。
- 玩家逃跑成功 S->C 仍为 `1041 [INT 10, INT player_id]`。
- 1042 普通攻击继续使用 actionType=1，扣血继续用 effect 22。
- 1048 fighter 字段布局和类型不变。
- 客户端短格式 1040/action=2 继续作为动作播放完成屏障。
- 逃跑不发送胜利奖励、不移除怪物。
- 胜利才执行奖励和地图怪物移除。
- 不为本次重构发明新协议字段。
- 不修改 APK。

## 测试结构

新增/拆分为：

```text
implementation_staging/tests/battle/
├── test_state.py
├── test_protocol.py
├── test_engine.py
├── test_encounter.py
├── test_rewards.py
└── test_resources.py
```

其中：

- `test_state.py`
  - begin / finish / reset
  - HP 状态
  - escape / guard 建立
  - 1 格解除
  - 2 秒解除
- `test_protocol.py`
  - 每个战斗 frame 的 message id、字段值、字段 type id
- `test_engine.py`
  - 普通攻击
  - 防御
  - 非法目标
  - 玩家死亡 / 怪物死亡
  - 回合推进
- `test_encounter.py`
  - 手动交互开战
  - q 菜单开战
  - 靠近开战
  - active 时不重开
  - 逃跑 2 秒内抑制
  - 离开 1 格后允许
  - 等 2 秒后允许
- `test_rewards.py`
  - 经验
  - 升级
  - 掉落
  - 逃跑无奖励
- `test_resources.py`
  - role/image 资源别名和响应协议

原 `tests/test_protocol.py` 中已有的战斗测试在迁移后删除重复项，非战斗协议测试保留。

`tests/test_battle_escape_guard.py` 在逻辑迁入 `battle/state.py` / `battle/encounter.py` 后删除。

`tests/test_roaming_boss_interaction.py` 只保留地图/q 协议桥接和 Boss 坐标相关测试；战斗 suppress/escape 行为迁到 `tests/battle/test_encounter.py`。

## 迁移顺序

为了保持每一步都能运行，迁移按以下顺序执行：

1. 建立 `battle` 包并迁移纯协议 encoder/helper；`server.py` re-export 旧接口。
2. 迁移 `LocalBattleState`、CombatStats 和 escape guard 到 `battle/state.py`。
3. 建立 `battle/encounter.py`，把所有开战入口和逃跑重触发规则统一到一个状态机。
4. 删除 `server_pets.py` 对战斗方法的 monkey-patch，改为调用 encounter API。
5. 迁移回合/伤害/命令裁决到 `battle/engine.py`。
6. 迁移奖励到 `battle/rewards.py`。
7. 迁移战斗资源到 `battle/resources.py`。
8. 拆分战斗测试并删除旧重复测试。
9. 仅在所有调用方稳定后清理 `server.py` 中不再需要的兼容 re-export。

每一步必须先补/迁测试，再移动实现，避免一次性大爆炸式重写。

## 验收标准

重构完成后必须满足：

1. `server_pets.py` 不再 monkey-patch 任何战斗状态方法。
2. `server.py` 不再包含 `LocalBattleState` 的实现体。
3. `server.py` 不再包含逃跑 guard 算法实现。
4. 1040 / 1041 / 1042 / 1048 编码实现集中在 `battle/protocol.py`。
5. 所有地图开战入口最终通过 `battle/encounter.py`。
6. 战斗状态只有一个权威 `LocalBattleState`。
7. Boss 游荡仍属于地图系统；战斗只消费 Boss 当前坐标。
8. 逃跑后“离开 1 格或满 2 秒”规则保持不变。
9. 现有手动战斗、靠近自动战斗、逃跑、再次触发、胜利奖励行为不变。
10. 不需要重建 APK。
11. 完整验证使用：

```powershell
D:\python\python.exe -m unittest discover -s tests -v
D:\python\python.exe test_client.py --host 127.0.0.1 --port 6805 --exercise-role-crud
```

真机仍由用户执行最终战斗回归：进入战斗、普通攻击、逃跑、2 秒重触发、离开 1 格重触发、击杀奖励。

## 非目标

本次明确不做：

- 新技能系统
- 新怪物 AI
- PVP
- 宠物正式参战逻辑
- 新掉落表
- 新伤害公式
- 新协议
- APK 修改
- Boss 随机巡逻算法升级

这些应在战斗子系统边界稳定后单独实现。
