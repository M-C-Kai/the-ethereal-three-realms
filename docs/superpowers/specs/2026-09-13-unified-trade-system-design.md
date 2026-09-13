# 统一交易系统设计

日期：2026-09-13  
目标分支：`master`

## 1. 背景

当前服务器已经按玩法域拆分为 `systems/<name>/`。交易相关能力仍分散在三个不同领域：

- `systems/consignment/`：协议 1138，负责物品寄售、购买、下架、托管与寄售交易记录；
- `systems/exchange/`：协议 1083，负责仙晶求购/出售订单、撮合、手续费与仙晶/银两结算；
- `systems/social/`：协议 1056，除社交功能外还直接承载玩家面对面交易请求、接受、开窗、锁定、结算。

这导致“交易”作为业务域没有统一边界：相同的资产交换、事务回滚、成交记录和审计能力分散在多个系统中；同时 `social` 承担了不属于社交领域的资产交易职责。

本次重构将所有交易能力统一收敛到 `systems/trade/`，并在其下继续按交易类型拆分子模块。客户端协议、页面与已有业务行为保持兼容。

## 2. 目标

### 2.1 领域边界

建立唯一交易域：

```text
systems/trade/
├── __init__.py
├── handler.py
├── events.py
├── common/
│   ├── __init__.py
│   ├── ledger.py
│   ├── models.py
│   └── transaction.py
├── item/
│   ├── __init__.py
│   ├── handler.py
│   ├── service.py
│   ├── protocol.py
│   └── registry.py
├── crystal/
│   ├── __init__.py
│   ├── handler.py
│   ├── service.py
│   └── protocol.py
└── player/
    ├── __init__.py
    ├── handler.py
    ├── service.py
    ├── protocol.py
    └── registry.py
```

映射关系：

```text
systems/consignment/*        -> systems/trade/item/*
systems/exchange/*           -> systems/trade/crystal/*
systems/social/ 的 1056 交易 -> systems/trade/player/*
```

`systems/social/` 重构后只保留社交行为，例如查看资料、好友、私聊、赠送、切磋和 PK；不再保存玩家交易请求、交易会话或交易结算逻辑。

### 2.2 统一成交事实

三类交易都通过公共账本生成全局唯一、单调递增的 `transaction_id`，并写入统一成交文件：

```text
data/trade_transactions.json
```

物品寄售与仙晶交易的业务挂单状态仍分别保存在原业务文件中：

```text
data/consignment_listings.json
data/exchange_orders.json
```

玩家面对面交易的未完成会话仍为进程内状态，不做持久化；只有成功结算后的成交事实写入统一账本。

## 3. 非目标

本次重构不修改以下外部行为：

- 不修改 APK 消息号、字段顺序、字段类型或页面跳转；
- 不改变 1138 物品寄售的上架、浏览、购买、下架语义；
- 不改变 1083 仙晶求购/出售订单的现有语义；
- 不改变 1056 玩家交易的客户端交互流程；
- 不在本次重构中开放宠物寄售；
- 不增加新的交易 UI；
- 不改变好友、私聊、赠送、切磋、PK 等社交行为。

## 4. 顶层 TradeSystem

`server.py` 最终只感知一个交易系统：

```python
self.trade_system = TradeSystem(...)
register_trade_routes(self.system_router, self.trade_system)
```

`TradeSystem` 负责装配三个交易子模块和公共账本，但不承载具体业务规则。

路由分发关系：

```text
1138 -> trade.item
1083 -> trade.crystal
1056 -> trade.player
```

此外，寄售商人 NPC 相关对话 hook 统一从 `TradeSystem` 暴露给地图系统，再由 TradeSystem 内部分派给物品寄售或仙晶交易子模块。

这样 `server.py` 不再分别 import 或实例化 `ConsignmentSystem`、`ExchangeSystem`，也不再让 `SocialSystem` 处理 1056。

## 5. 子模块职责

### 5.1 trade/item

负责现有物品寄售业务：

- 原生寄售商场和“我的寄售”入口；
- 28 个物品分类；
- 上架、托管、部分堆叠拆分；
- 市场浏览；
- 下架取回；
- 买家购买；
- 买卖双方银两和物品转移；
- listing 生命周期：`active / sold / cancelled / expired`；
- 原有 1138 协议兼容。

原 `ConsignmentService` 的 listing 业务继续存在，但成功购买后不再由其私有 transaction 序列作为最终成交事实；成交记录交给统一 `TradeLedger`。

### 5.2 trade/crystal

负责现有仙晶交易所：

- 求购单；
- 出售单；
- 发布订单；
- 委托费用；
- 撤单；
- 应单撮合；
- 银两和仙晶托管、返还及结算；
- 原有 1083 协议兼容。

订单生命周期仍保存在 `exchange_orders.json`；成功撮合后通过统一账本记录成交。

### 5.3 trade/player

从 `systems/social/` 中完整剥离玩家面对面交易：

- 交易请求；
- 接受/拒绝；
- 打开交易窗口；
- 双方物品和银两展示；
- 锁定/确认；
- 取消；
- 最终结算；
- 断线或失效会话清理。

`trade/player/registry.py` 保存未完成交易请求和交易会话。会话保持进程内状态，不进入统一成交账本；只有最终完成资产交换后才生成成交记录。

## 6. 公共交易账本

### 6.1 文件格式

`data/trade_transactions.json`：

```json
{
  "next_transaction_id": 1,
  "transactions": []
}
```

每一条成功成交记录至少包含：

```json
{
  "transaction_id": 10001,
  "trade_type": "item",
  "status": "completed",
  "participants": [
    {"role_id": 1001, "side": "seller"},
    {"role_id": 1002, "side": "buyer"}
  ],
  "assets": [
    {
      "type": "item",
      "template_id": 20001,
      "instance_id": 98765,
      "quantity": 1
    },
    {"type": "silver", "amount": 5000}
  ],
  "source": {
    "type": "listing",
    "id": 321
  },
  "created_at": 1789270000,
  "completed_at": 1789270002
}
```

### 6.2 trade_type

第一阶段固定支持：

```text
item     物品寄售
crystal  仙晶交易所
player   玩家面对面交易
```

### 6.3 source

`source` 只保存业务来源引用，不复制整个业务订单：

- 物品寄售：`{"type": "listing", "id": listing_id}`；
- 仙晶交易：`{"type": "order", "id": order_id}`；
- 玩家交易：`{"type": "player_session", "id": <settlement/session id>}`。

### 6.4 assets

账本以“实际发生的资产交换”为准，而不是客户端请求参数。允许记录：

- `item`：物品模板、实例、数量；
- `silver`：银两；
- `crystal`：仙晶。

玩家交易可能包含双方多个物品与银两，因此 `assets` 可以包含多条记录，并应带 `from_role_id` / `to_role_id` 以明确方向。

### 6.5 查询

`TradeLedger` 至少提供：

- `record_completed(...)`；
- `get(transaction_id)`；
- `history_for_role(role_id, trade_type=None)`；
- `all_transactions()`。

统一账本是跨交易类型查询成交历史的唯一入口。

## 7. 全局 transaction_id

全局成交编号只由 `TradeLedger` 分配。

规则：

1. `next_transaction_id >= 1`；
2. 每次成功写入后递增；
3. 重启后从文件恢复；
4. 若文件中的 `next_transaction_id` 小于历史最大编号 + 1，则自动修正；
5. 三种交易不得各自再生成独立的最终 transaction_id。

业务模块可继续拥有自己的 `listing_id`、`order_id` 或会话编号，但它们都不是最终成交编号。

## 8. 事务与回滚

三类交易必须满足统一原则：

> 业务状态变更、角色资产变更和统一成交账本写入要么全部成功，要么全部恢复到操作前状态。

### 8.1 transaction.py

`trade/common/transaction.py` 提供公共事务辅助，职责包括：

- 对参与角色做深拷贝快照；
- 对业务数据做快照；
- 对统一账本做快照；
- 执行业务变更；
- 保存角色数据；
- 保存业务文件；
- 保存统一账本；
- 任一步骤失败时恢复角色、业务状态和账本状态；
- 对物品类交易保留原物品对象 identity，避免失败回滚后生成新的 Python item 对象。

现有物品寄售已经具备成熟的快照与跨角色物品 identity 恢复逻辑，迁移时以其行为为基线抽取公共能力。

### 8.2 成交写入时机

只有在资产交换已经通过全部校验、且即将作为一个事务提交时才创建成交记录。

以下情况不得产生成交流水：

- 挂单；
- 撤单/下架；
- 玩家交易请求或接受；
- 锁定但未最终完成；
- 余额不足；
- 背包空间不足；
- 自买/自交易；
- 保存失败并回滚；
- 重复购买或重复应单。

## 9. 业务数据迁移

### 9.1 物品寄售

现有 `consignment_listings.json` 可能包含：

```text
next_listing_id
next_item_instance_id
next_transaction_id
listings
transactions
```

迁移后业务文件只需要：

```text
next_listing_id
next_item_instance_id
listings
```

兼容策略：

1. 读取旧文件时允许存在 `transactions` 和 `next_transaction_id`；
2. 首次启动迁移代码把旧的已完成交易转换为统一 ledger 记录；
3. 迁移使用稳定的 legacy source 标记，避免重复导入；
4. 迁移成功后业务服务不再向旧 `transactions` 写入新数据；
5. 可以暂时保留旧字段以便向后读取，但它不再是权威数据源；后续清理版本再物理删除。

### 9.2 仙晶交易

对 `exchange_orders.json` 采用相同策略：旧 `transactions` 可读取并迁移，但新成交统一写入 `trade_transactions.json`。

### 9.3 防重复迁移

统一账本记录 legacy 导入来源，例如：

```json
"legacy_source": {
  "system": "consignment",
  "transaction_id": 7
}
```

导入前按 `(system, transaction_id)` 查重，保证重复启动不会重复生成成交记录。

## 10. 玩家交易从 social 剥离

### 10.1 SocialSystem

重构后 `SocialSystem`：

- `HANDLED_MESSAGE_IDS` 不再包含 1056；
- 删除 `_handle_trade`；
- 删除对 trade protocol frame 的 imports；
- 不再持有 `trade_requests` / trade session registry；
- 社交 Registry 只保留好友/社交相关临时状态。

### 10.2 PlayerTradeSystem

`trade/player` 接管 1056，保持原有消息 action 行为与客户端 frame 完全一致。

其依赖通过 `TradeSystem` 构造期注入：

- `find_role`；
- `online_role_ids`；
- `push_to_role`；
- `save roles`；
- item registry / inventory helpers；
- `TradeLedger`。

不允许 `trade/player` 反向 import `SocialSystem` handler。

## 11. NPC 对话归属

寄售商人当前同时提供：

- 寄售商场；
- 我的寄售；
- 仙晶交易所；
- 寄售仙晶；
- 求购仙晶。

重构后由 `TradeSystem` 对地图系统暴露统一 hook：

```text
trade_system.npc_dialogue_frames
trade_system.npc_dialogue_option
```

TradeSystem 内部根据 NPC service 和 option id 分发给 item/crystal 子模块。

地图系统只依赖“交易系统 NPC hook”，不需要知道 item/crystal 的具体实现。

## 12. server.py 装配

重构后的装配目标：

```text
server.py
  -> TradeLedger
  -> TradeSystem
       -> ItemTradeSystem
       -> CrystalTradeSystem
       -> PlayerTradeSystem
  -> SocialSystem（不含交易）
```

`Settings` 新增：

```python
trade_transactions_file: str = 'data/trade_transactions.json'
```

原有：

```python
consignment_data_file
exchange_data_file
```

继续保留，分别供 item/crystal 子模块使用。

## 13. 错误处理

错误处理原则不改变客户端兼容性：

- 协议字段不合法：由对应子模块返回现有错误提示或忽略帧；
- 业务校验失败：不改变资产、不写成交账本；
- 持久化失败：完整回滚并记录服务端错误日志；
- 玩家交易任一参与方失效/离线：关闭会话，不结算；
- 统一账本损坏或无法解析：启动时拒绝静默覆盖，记录明确错误；新交易不得在账本不可持久化时被报告为成功。

## 14. 事件

`systems/trade/events.py` 定义交易域事件名，第一阶段至少包含：

```text
trade.completed
trade.cancelled
```

`trade.completed` 的载荷包含统一 transaction 记录。业务系统可以在事务成功提交后发布事件。

本次不要求其他系统消费这些事件，但事件接口为后续成就、统计、邮件、风控预留稳定边界。

## 15. 测试策略

### 15.1 common

新增账本测试：

- 三类交易共享同一 transaction_id 序列；
- 重启恢复；
- 最大历史编号修正；
- legacy 导入幂等；
- role history 跨交易类型查询；
- 保存失败不留下幽灵流水。

### 15.2 item

迁移现有寄售测试并保证：

- 1138 协议不变；
- 上架/浏览/下架/购买不变；
- 部分堆叠托管不变；
- 双买保护不变；
- 银两/背包/绑定/任务物品校验不变；
- 成功购买写统一账本；
- 保存失败时物品 identity 和资产完整回滚。

### 15.3 crystal

保证：

- 1083 协议不变；
- 求购/出售/撤单/应单行为不变；
- 手续费不变；
- 成功撮合写统一账本；
- 重复应单不产生第二条流水。

### 15.4 player

把原 social 玩家交易测试迁入 trade/player，并增加：

- 请求/接受/拒绝；
- 开窗；
- 双方物品和银两同步；
- 锁定/确认；
- 取消；
- 断线清理；
- 最终资产交换；
- 成功结算写统一账本；
- 失败/取消不写流水。

### 15.5 路由回归

重点验证：

- `1056` 只能由 TradeSystem 处理；
- social 不再认领 1056；
- `1138`、`1083` 仍由正确交易子模块处理；
- role/inventory/map 等存在重叠 message id 的现有优先级不受影响。

### 15.6 系统回归

至少运行：

- trade 全量单测；
- 现有 social 测试；
- task 测试；
- pet 核心测试；
- 真实加密 TCP 的物品寄售完整生命周期；
- 玩家交易的双连接 TCP 流程（若现有测试基础允许直接构造）。

## 16. 实施顺序

为降低一次性重构风险，代码实现按以下顺序进行：

1. 建立 `trade/common` 与统一 Ledger，先写 RED 测试；
2. 迁移物品寄售到 `trade/item`，接入 Ledger；
3. 迁移仙晶交易到 `trade/crystal`，接入 Ledger；
4. 从 social 剥离 1056 到 `trade/player`，接入 Ledger；
5. 建立顶层 `TradeSystem` 并修改 server 装配；
6. 更新地图 NPC hook；
7. 增加 legacy transaction 迁移；
8. 删除旧 `systems/consignment/`、`systems/exchange/`；
9. 清理 social 中所有交易残留；
10. 更新 `systems/README.md` 与交易文档；
11. 跑全量目标回归和真实 TCP 验证。

每一步必须保持可测试，并使用 TDD 的 RED -> GREEN -> REFACTOR 节奏。

## 17. 完成标准

重构完成需要同时满足：

1. 代码结构只存在一个顶层交易域 `systems/trade/`；
2. 物品、仙晶、玩家交易作为明确子模块存在；
3. `social` 不含 1056 玩家交易实现或交易会话状态；
4. `server.py` 只装配一个 `TradeSystem`；
5. 1138 / 1083 / 1056 的客户端兼容行为保持；
6. 三类成功成交都写入同一 `trade_transactions.json`；
7. 全局 `transaction_id` 跨交易类型唯一且重启后连续；
8. 失败、取消和回滚不产生成交记录；
9. 旧寄售/仙晶成交记录可幂等迁入统一账本；
10. 现有交易、social、task、pet 相关回归不新增失败；
11. 物品寄售真实 TCP 生命周期继续通过；
12. 不宣称手机真机行为通过，直到用户完成真实设备验收。
