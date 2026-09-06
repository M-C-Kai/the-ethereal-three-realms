# 人物状态更新总线设计

## 背景

当前兼容服已经有 `character_appearance()`、`effective_character_stats()`、`combat_stats()`、`character_equipment_refresh_frames()` 等人物状态计算与刷新逻辑，但触发点仍由装备、强化等业务代码直接调用。这样继续扩展等级、技能、BUFF、坐骑等系统时，容易出现“状态已变但人物面板/战斗属性/外观没有同步”的问题。

本设计引入一个轻量、同步、进程内的人物状态更新总线。业务代码只负责完成状态变更并发布人物状态事件；总线负责基于角色最终状态重新计算需要刷新的数据，并返回协议帧。网络层仍负责 `_send()`，总线不持有 socket、writer 或 cipher。

## 目标

1. 同槽位装备 A→B 时，先完成最终装备状态，再只重算一次人物状态；旧装备属性不残留，新装备属性立即生效。
2. 装备、卸下、替换、强化、升级、基础属性变化、外观变化统一通过一个人物状态刷新入口。
3. 人物面板属性、地图人物外观和战斗属性使用同一份角色当前状态计算源。
4. 总线本身保持同步、无后台线程、无异步队列，符合当前单进程兼容服结构。
5. 不改变 APK 已确认的协议字段含义，不为未知装备属性字段发明语义。

## 非目标

- 不实现跨进程消息队列。
- 不实现持久化事件日志或事件回放。
- 不把网络发送职责放进总线。
- 不改变 `equipment_attributes[2]`、`equipment_attributes[3]` 的含义；它们继续保持未定义。
- 不在本次改动中重构所有业务系统，只接入已经明确会改变人物状态的现有链路。

## 架构

新增模块：

`implementation_staging/character_update_bus.py`

核心对象：

- `CharacterUpdateEvent`：事件名枚举/常量。
- `CharacterUpdateResult`：总线返回结果，包含待下发 `frames` 和本次刷新范围元数据。
- `CharacterUpdateBus`：同步发布入口，根据事件类型决定是否重算外观、人物属性和面板刷新。

`server.py` 继续保留协议编码和角色业务处理，但不再让装备、强化等分支自行拼人物刷新帧；它们改为调用总线。

## 事件模型

首批事件：

- `equipment.changed`
  - 装备、卸下、同槽替换、丢弃已装备物品后发布。
  - 重算人物外观、人物有效属性、战斗属性依赖。
  - 返回完整 `1017` 人物状态刷新 + `1039/action=1` 人物属性面板刷新。

- `equipment.strengthened`
  - 强化成功/失败后，只要装备实例属性发生变化就发布。
  - 如果强化目标当前已装备，属性立即刷新；如果目标在背包，人物有效属性不变，但允许返回空刷新结果，避免无意义下发。

- `character.level_changed`
  - 等级变化后发布。
  - 重算等级相关 HP/MP、人物属性和战斗属性。
  - 返回 `1017` + `1039/action=1`。

- `character.stats_changed`
  - `role.stats` 等基础属性发生变化后发布。
  - 返回 `1017` + `1039/action=1`。

- `character.appearance_changed`
  - 仅外观属性变化时发布，例如明确的外观/坐骑变化。
  - 默认只返回 `1017`；如果调用方同时声明属性变化，则升级为完整刷新。

## 数据流

### 装备同槽替换

```text
收到装备 B 请求
  ↓
查找 slot 相同的已装备 A
  ↓
A.location = bag
  ↓
B.location = equipped
  ↓
角色最终状态已确定
  ↓
publish(equipment.changed)
  ↓
character_appearance(role)
effective_character_stats(role)
combat_stats(role)
  ↓
1017 完整人物状态
1039/action=1 人物属性面板
```

关键规则：总线只读取“最终角色状态”，不接受“旧装备加成”“新装备加成”这类增量差值，因此不会出现 A+B 叠加残留。

### 强化

```text
强化装备实例
  ↓
equipment_attributes 更新
  ↓
publish(equipment.strengthened, item_id)
  ↓
检查该实例当前是否 equipped
  ├─ 否 → 不刷新人物属性
  └─ 是 → 重算最终人物状态 → 1017 + 1039
```

### 升级/基础属性变化

```text
role.level / role.stats 改变
  ↓
publish(character.level_changed / character.stats_changed)
  ↓
重算 HP/MP、人物有效属性、战斗属性
  ↓
1017 + 1039
```

## 计算源

继续复用并保持单一来源：

- 外观：`character_appearance(role, registry)`
- 装备四属性汇总：`equipped_attribute_totals(role, registry)`
- 人物面板有效属性：`effective_character_stats(role, registry)`
- 战斗属性：`combat_stats(role, registry)`

总线不复制这些公式，只协调“何时重新计算、下发哪些帧”。

已确认的装备属性语义保持：

- `equipment_attributes[0]` → 攻击加成
- `equipment_attributes[1]` → 防御加成
- `[2]`、`[3]` → 未确认，不赋予新语义

## 协议刷新

完整人物刷新仍沿用已经验证的协议链：

- `1017`
  - 当前完整人物外观
  - HP/MP property 40..43
  - 当前人物有效属性 property 44..48
- `1039/action=1`
  - 当前人物属性面板数据
  - 用于已打开人物面板的即时重绘

登录选角 `1080` 仍直接从当前存档装备状态生成预览，不通过运行期事件总线。

## 网络边界

总线禁止持有：

- `asyncio.StreamWriter`
- `GameCipher`
- 连接锁
- 用户会话

调用方式：

```python
result = character_update_bus.publish(
    CharacterUpdateEvent.EQUIPMENT_CHANGED,
    role=active_role,
    registry=self.settings.item_registry,
)
await self._send(writer, *result.frames, cipher=game_cipher, lock=send_lock)
```

这样总线可以独立单元测试，协议发送仍由 `LocalGameServer` 管理。

## 失败与一致性

1. 业务状态修改失败时，不发布事件。
2. 持久化失败时沿用现有回滚策略；回滚后不得发布“已成功变化”事件。
3. 总线发布失败不得修改角色状态；它只读取当前状态并构造帧。
4. 同一业务事务内只发布一次最终状态事件，避免重复重算和重复下发。
5. 未识别事件直接报错，不静默忽略，防止业务以为已刷新。

## 首批接入点

本次实现接入：

1. 装备 `action=5`
2. 卸下 `action=6`
3. 同槽装备替换
4. 丢弃已装备物品
5. 强化装备属性变化
6. 已有等级变化链路中明确修改 `role.level` 的位置

现有 `character_equipment_refresh_frames()` 在迁移完成后作为总线内部兼容构建器保留，避免一次性扩大修改范围；业务处理分支不再直接调用它。

## 测试

新增 `tests/test_character_update_bus.py`，至少覆盖：

1. 同槽装备 A(+10攻击) → B(+25攻击)：最终人物属性只增加 25，不是 35。
2. 同槽防具 A(+7防御) → B(+12防御)：最终只增加 12。
3. 装备切换后总线返回 `1017` + `1039/action=1`。
4. `character_panel_frames()` 与 `combat_stats()` 对当前 equipped 集合一致。
5. 卸下装备后属性立即回退。
6. 强化当前已装备武器后触发属性刷新。
7. 强化背包中的武器不改变人物当前属性，并且不强制下发人物刷新。
8. `character.level_changed` 重新计算等级相关属性并刷新面板。
9. 未知事件抛出明确异常。

同时继续运行已有刷新链、强化、武器外观、铠甲/头盔/腿甲/鞋子专项回归，并用完整测试前后失败差集确保没有新增历史失败。

## 迁移原则

这次只把“人物状态变更后的刷新协调”抽到总线，不搬迁物品数据库、不改协议编码层、不改角色存档结构。这样可以先把更新一致性稳定下来，再让后续技能、BUFF、坐骑等系统逐步接入同一总线。
