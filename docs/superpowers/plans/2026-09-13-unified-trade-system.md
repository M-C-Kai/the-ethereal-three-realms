# Unified Trade System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Track every checkbox and keep each task independently testable.

**Goal:** 将当前分散在 `systems/consignment/`、`systems/exchange/` 和 `systems/social/` 中的交易能力统一到 `systems/trade/`，在其下拆分 `item / crystal / player` 三个子模块，并让三类成功成交共享同一个持久化 `TradeLedger` 与全局 `transaction_id`。

**Architecture:** 顶层 `TradeSystem` 是唯一向 `SystemRouter` 注册的交易域入口，内部按消息号委托给物品寄售（1138）、仙晶交易所（1083）和玩家面对面交易（1056）。挂单业务数据继续分别存放在 `consignment_listings.json` 与 `exchange_orders.json`，成功成交统一写入 `trade_transactions.json`。`social` 只保留社交职责，不再持有 1056 协议、交易会话或结算逻辑。

**Tech Stack:** Python 3、标准库 `json/pathlib/dataclasses/typing/asyncio`、现有 `app.router.SystemRouter`、`app.context.SystemContext`、二进制协议模块 `protocol.py`、`unittest`、现有 `RoleStore` / inventory helpers / `GameCipher`。

**Spec:** `docs/superpowers/specs/2026-09-13-unified-trade-system-design.md`

## Global Constraints

- 目标分支是 `master`；实施时基于当时最新 `master`，不要覆盖其他系统的新改动。
- 严格 TDD：每个行为变化先写 RED 测试，再实现最小代码，最后 REFACTOR。
- 不改变 APK 的 1138 / 1083 / 1056 消息号、字段顺序、字段类型、页面跳转和现有中文提示语义。
- 物品寄售、仙晶订单和玩家交易的业务模型保持独立；只统一交易域、事务辅助与最终成交流水。
- 宠物寄售仍然返回“宠物寄售暂未开放”，不得猜测宠物交易协议。
- `server.py` 只负责依赖装配、路由注册和网络生命周期，不新增交易业务分支。
- `trade_transactions.json` 是新成交历史的唯一权威来源；旧业务文件中的 `transactions` 只做兼容读取和幂等迁移，不再写新记录。
- 成交的逻辑事务要求：角色资产、业务订单状态、统一账本三者要么一起成功，要么恢复到操作前状态；文件系统层面不宣称数据库级 ACID。
- 回滚物品交易时必须保留原 Python 物品对象 identity，沿用现有寄售的跨角色 item-pool 恢复语义。
- 保存失败、余额不足、背包满、自交易、重复购买/应单、撤单、取消、仅锁定未确认，都不得留下统一成交流水。
- 不宣称真机通过；最终只报告自动化验证，真机验收由用户完成。

---

### Task 1: 建立统一 TradeLedger 与公共事务基础

**Files:**
- Create: `implementation_staging/systems/trade/__init__.py`
- Create: `implementation_staging/systems/trade/common/__init__.py`
- Create: `implementation_staging/systems/trade/common/models.py`
- Create: `implementation_staging/systems/trade/common/ledger.py`
- Create: `implementation_staging/systems/trade/common/transaction.py`
- Create: `implementation_staging/data/trade_transactions.json`
- Create: `implementation_staging/tests/test_trade_ledger.py`

**Interfaces:**

```python
# systems/trade/common/ledger.py
class TradeLedgerError(RuntimeError): ...

class TradeLedger:
    def __init__(self, path: str | Path): ...
    def record_completed(
        self,
        *,
        trade_type: str,
        participants: list[dict[str, object]],
        assets: list[dict[str, object]],
        source: dict[str, object],
        created_at: int,
        completed_at: int,
        legacy_source: dict[str, object] | None = None,
        persist: bool = True,
    ) -> dict[str, object]: ...
    def get(self, transaction_id: int) -> dict[str, object] | None: ...
    def history_for_role(self, role_id: int, trade_type: str | None = None) -> list[dict[str, object]]: ...
    def all_transactions(self) -> list[dict[str, object]]: ...
    def save(self) -> None: ...
    def snapshot(self) -> dict[str, object]: ...
    def restore(self, snapshot: dict[str, object]) -> None: ...
    def has_legacy_source(self, system: str, transaction_id: int) -> bool: ...
```

```python
# systems/trade/common/transaction.py
def restore_roles_in_place(
    snapshots: list[tuple[dict[str, object], dict[str, object]]],
) -> None: ...

def commit_trade(
    *,
    roles: list[dict[str, object]],
    role_save: Callable[[], None],
    business_data: dict[str, object] | None,
    business_save: Callable[[], None] | None,
    ledger: TradeLedger,
    apply: Callable[[], T],
) -> T: ...
```

`commit_trade()` 在调用 `apply()` 前快照角色、业务数据和 ledger；`apply()` 只修改内存，并通过 `ledger.record_completed(..., persist=False)` 暂存流水；随后按 `role_save -> business_save -> ledger.save` 提交。任一步骤抛错时恢复全部内存状态并 best-effort 重写已成功保存的文件，然后重新抛出原异常。

- [ ] **Step 1: 写 Ledger RED 测试**

在 `test_trade_ledger.py` 覆盖：三个 `trade_type` 共用同一 ID 序列；重启恢复；文件里 `next_transaction_id` 落后于历史最大 ID 时自动修正；`history_for_role()` 可跨类型查询并按类型过滤；畸形已存在 ledger 文件必须抛 `TradeLedgerError`，不能静默清空。

核心断言示例：

```python
item = ledger.record_completed(
    trade_type='item', participants=[{'role_id': 1, 'side': 'seller'}, {'role_id': 2, 'side': 'buyer'}],
    assets=[], source={'type': 'listing', 'id': 10}, created_at=1, completed_at=2,
)
crystal = ledger.record_completed(
    trade_type='crystal', participants=[{'role_id': 3, 'side': 'seller'}, {'role_id': 1, 'side': 'buyer'}],
    assets=[], source={'type': 'order', 'id': 11}, created_at=3, completed_at=4,
)
self.assertEqual((item['transaction_id'], crystal['transaction_id']), (1, 2))
self.assertEqual(len(ledger.history_for_role(1)), 2)
```

- [ ] **Step 2: 运行并确认 RED**

Run from `implementation_staging`:

```bash
python -m unittest tests.test_trade_ledger -v
```

Expected: FAIL / ImportError，因为 `systems.trade.common` 尚不存在。

- [ ] **Step 3: 实现最小 Ledger**

`models.py` 定义 `TRADE_TYPES = {'item', 'crystal', 'player'}` 和交易记录规范化/校验帮助函数；`ledger.py` 使用 `.tmp + replace()` 原子替换自身 JSON 文件。初始化文件内容固定为：

```json
{
  "next_transaction_id": 1,
  "transactions": []
}
```

- [ ] **Step 4: 写事务回滚 RED 测试**

覆盖 `commit_trade()`：模拟第二/第三个保存动作失败后，角色银两、业务状态、ledger ID/rows 全部恢复；再构造“物品已从卖家移动到买家后保存失败”的场景，断言恢复到卖家时仍是原始 `item is original_item`。

- [ ] **Step 5: 实现公共事务辅助并跑 GREEN**

Run:

```bash
python -m unittest tests.test_trade_ledger -v
```

Expected: PASS。

- [ ] **Step 6: Commit checkpoint**

```bash
git add implementation_staging/systems/trade/common implementation_staging/data/trade_transactions.json implementation_staging/tests/test_trade_ledger.py
git commit -m "feat: add unified trade ledger and transaction core"
```

---

### Task 2: 将 1138 物品寄售迁入 trade/item 并接入统一流水

**Files:**
- Create: `implementation_staging/systems/trade/item/__init__.py`
- Create: `implementation_staging/systems/trade/item/handler.py`
- Create: `implementation_staging/systems/trade/item/service.py`
- Create: `implementation_staging/systems/trade/item/protocol.py`
- Create: `implementation_staging/systems/trade/item/registry.py`
- Create: `implementation_staging/tests/test_trade_item.py`
- Modify: `implementation_staging/tests/test_aux_systems.py`
- Reference during migration: `implementation_staging/systems/consignment/*`

**Interfaces:**

```python
class ItemTradeService:
    def __init__(self, role_store, item_registry, data_file, ledger: TradeLedger): ...
    def list_item(...): ...
    def search(category_id: int): ...
    def my_listings(role_id: int): ...
    def unlist(...): ...
    def buy(...): ...
    def order_history(...): ...
    def trade_history(role_id: int, side: str = 'all'): ...  # 从统一 ledger 查询 item 类型
    def migrate_legacy_transactions(self) -> int: ...
```

`ItemTradeSystem` 保持 1138 原有检测器和回包；内部 import 全部改为 `systems.trade.item.*`。协议常量可以继续使用 `CONSIGNMENT_*` 名字，因为这是 APK 协议语义，不要求重命名 wire-level 标识。

- [ ] **Step 1: 从现有 Consignment 测试建立 RED 基线**

把 `test_aux_systems.py` 的 `ConsignmentSystemTests` 移到新 `test_trade_item.py`，改为 import `ItemTradeSystem`，并新增：成功购买后 `ledger.all_transactions()` 只有一条 `trade_type='item'`；撤单没有流水；重复购买没有第二条流水；交易记录里的 `source` 是 listing ID、assets 包含 item 和 silver 的方向。

- [ ] **Step 2: 运行 RED**

```bash
python -m unittest tests.test_trade_item -v
```

Expected: FAIL / ImportError。

- [ ] **Step 3: 复制并重命名现有寄售实现到 trade/item**

保留以下行为不变：28 分类、action 3/13/0/23/7/9/2/4、角色 ID 为 0 时按 session 角色绑定、整件保留实例 ID、拆栈分配新实例 ID、宠物寄售拒绝、原客户端帧布局。

- [ ] **Step 4: 把 buy() 改为统一逻辑事务**

`buy()` 完成全部校验后，在一个 `commit_trade()` 内：移动同一物品对象、买家扣银、卖家加银、listing 标记 `sold`、调用：

```python
transaction = self.ledger.record_completed(
    trade_type='item',
    participants=[
        {'role_id': seller_id, 'side': 'seller'},
        {'role_id': buyer_id, 'side': 'buyer'},
    ],
    assets=[
        {'type': 'item', 'instance_id': item_id, 'template_id': template_id,
         'quantity': quantity, 'from_role_id': seller_id, 'to_role_id': buyer_id},
        {'type': 'silver', 'amount': total_price,
         'from_role_id': buyer_id, 'to_role_id': seller_id},
    ],
    source={'type': 'listing', 'id': listing_id},
    created_at=int(listing['created_at']),
    completed_at=completed_at,
    persist=False,
)
```

新成交不再 append 到 `consignment_listings.json['transactions']`，也不再递增它的 `next_transaction_id`。

- [ ] **Step 5: 回滚与对象 identity 测试**

模拟 ledger 保存失败，断言：listing 仍 active、买卖双方银两恢复、物品回到卖家 `location='consignment'`，并且是同一个 Python 对象；统一 ledger 无 ghost row。

- [ ] **Step 6: 跑 GREEN + 原协议回归**

```bash
python -m unittest tests.test_trade_item tests.test_aux_systems -v
```

Expected: PASS。

- [ ] **Step 7: Commit checkpoint**

```bash
git add implementation_staging/systems/trade/item implementation_staging/tests/test_trade_item.py implementation_staging/tests/test_aux_systems.py
git commit -m "refactor: move item consignment under trade domain"
```

---

### Task 3: 将 1083 仙晶交易所迁入 trade/crystal 并接入统一流水

**Files:**
- Create: `implementation_staging/systems/trade/crystal/__init__.py`
- Create: `implementation_staging/systems/trade/crystal/handler.py`
- Create: `implementation_staging/systems/trade/crystal/service.py`
- Create: `implementation_staging/systems/trade/crystal/protocol.py`
- Create: `implementation_staging/tests/test_trade_crystal.py`
- Reference: `implementation_staging/systems/exchange/*`
- Later delete: `implementation_staging/tests/test_exchange_system.py`

**Interfaces:**

```python
class CrystalTradeService:
    def __init__(self, role_store, data_file, ledger: TradeLedger, fee_rate: float = 0.02): ...
    def fee_quote(...): ...
    def post_order(...): ...
    def cancel_order(...): ...
    def accept_order(...): ...
    def market_orders(...): ...
    def my_orders(...): ...
    def my_order_ids(...): ...
    def migrate_legacy_transactions(self) -> int: ...
```

- [ ] **Step 1: 建立新路径 RED 测试**

以当前 `test_exchange_system.py` 为行为基线，复制到 `test_trade_crystal.py` 并改为 `systems.trade.crystal.*` imports。新增断言：post/cancel 不写 ledger；accept 成功只写一条 `crystal` 流水；double fill 不新增；保存失败回滚订单/两边货币/ledger。

- [ ] **Step 2: 运行 RED**

```bash
python -m unittest tests.test_trade_crystal -v
```

Expected: FAIL / ImportError。

- [ ] **Step 3: 迁移 protocol/handler/service，保持 1083 wire contract**

所有 action 0/3/4/5/6/10/11/12/13/15/16 的类型检测与 screen 350/351 帧原样保留。

- [ ] **Step 4: accept_order() 使用统一事务与 Ledger**

求购单 `kind='buy'`：poster 是 buyer、acceptor 是 seller；出售单 `kind='sell'`：poster 是 seller、acceptor 是 buyer。流水的 participants 必须按真实角色方向填写，assets 至少包含 crystal 和 silver 两条有 `from_role_id/to_role_id` 的记录。手续费仍按现有逻辑在发布时扣除，不伪装成成交时的玩家间资产转移。

- [ ] **Step 5: 通知发生在事务成功之后**

`CrystalTradeSystem._notify_counterparty()` 只在 `accept_order()` 已提交成功后调用；通知失败只记 debug，不回滚已成功交易，保持当前语义。

- [ ] **Step 6: GREEN**

```bash
python -m unittest tests.test_trade_crystal -v
```

Expected: PASS。

- [ ] **Step 7: Commit checkpoint**

```bash
git add implementation_staging/systems/trade/crystal implementation_staging/tests/test_trade_crystal.py
git commit -m "refactor: move crystal exchange under trade domain"
```

---

### Task 4: 从 social 完整剥离 1056 玩家面对面交易

**Files:**
- Create: `implementation_staging/systems/trade/player/__init__.py`
- Create: `implementation_staging/systems/trade/player/handler.py`
- Create: `implementation_staging/systems/trade/player/service.py`
- Create: `implementation_staging/systems/trade/player/protocol.py`
- Create: `implementation_staging/systems/trade/player/registry.py`
- Create: `implementation_staging/tests/test_trade_player.py`
- Modify: `implementation_staging/systems/social/handler.py`
- Modify: `implementation_staging/systems/social/service.py`
- Modify: `implementation_staging/systems/social/protocol.py`
- Modify: `implementation_staging/systems/social/registry.py`
- Modify: `implementation_staging/tests/test_social_system.py`

**Interfaces:**

```python
@dataclass
class PlayerTradeSession:
    session_id: int
    left_role_id: int
    right_role_id: int
    locks: dict[int, dict[str, object]]
    confirms: set[int]

class PlayerTradeRegistry:
    trade_requests: dict[int, tuple[int, float]]
    def pop_trade_request(...): ...
    def open_trade(left_role_id: int, right_role_id: int) -> PlayerTradeSession: ...
    def session_for(role_id: int) -> PlayerTradeSession | None: ...
    def trade_peer(role_id: int) -> int | None: ...
    def close_trade(role_id: int) -> int | None: ...
```

```python
class PlayerTradeService:
    def settle(
        self,
        session: PlayerTradeSession,
        left: dict[str, object],
        right: dict[str, object],
    ) -> PlayerTradeResult: ...
```

- [ ] **Step 1: 先把现有 1056 测试复制成新 RED 测试**

从 `test_social_system.py` 移出：请求/接受开窗、锁定后启用确认、双方确认交换物品和银两、单方确认不结算、物品消失失败、关闭通知 peer。再新增：完成后统一 ledger 有一条 `player` 流水；取消/失败不写；断线清理 session；保存失败恢复双方物品/银两并无流水。

- [ ] **Step 2: 运行 RED**

```bash
python -m unittest tests.test_trade_player -v
```

Expected: FAIL / ImportError。

- [ ] **Step 3: 移动 1056 wire helpers 到 trade/player/protocol.py**

迁移 `trade_request_frame / trade_open_frame / trade_peer_money_frame / trade_peer_items_frame / trade_enable_confirm_frame / trade_complete_frame / trade_close_frames`，字节布局不改。

- [ ] **Step 4: 移动交易状态到 PlayerTradeRegistry**

沿用 60 秒 pending request TTL。每次 `open_trade()` 分配进程内 `session_id`，只用于 ledger `source={'type':'player_session','id':...}`；它不需要跨重启连续，因为全局唯一性由 ledger transaction_id 保证。

- [ ] **Step 5: 移动结算逻辑到 PlayerTradeService 并接入 commit_trade()**

先完整校验两边余额、物品仍在 bag、重复 item id、双方背包容量，再执行资产交换。统一流水逐件记录 item 方向，并分别记录双方实际给出的 silver；零金额不需要生成空资产行。

- [ ] **Step 6: 实现 PlayerTradeSystem 的 1056 actions**

保持当前 action 1/2/3/4/20/10 的客户端行为。最终第二方确认成功后才关闭 session 并发送 1056/20 + 11/12、1008、1009、1017、1049 等现有帧。

- [ ] **Step 7: 清理 social**

`SocialSystem.HANDLED_MESSAGE_IDS` 删除 1056；`handle()` 删除 1056 分支；删 `_handle_trade`；`social.protocol` 删除 trade frame；`social.service` 删除 `TradeSettlement/settle_trade` 及仅交易使用的货币辅助；`SocialRegistry` 只保留 `friend_requests` 和好友 pending helper。`test_social_system.py` 删除交易测试，并新增：

```python
self.assertFalse(self.system.can_handle(self._context(self.alice), 1056, [byte(1), integer(1)]))
self.assertFalse(hasattr(self.system.registry, 'active_trades'))
```

- [ ] **Step 8: GREEN**

```bash
python -m unittest tests.test_trade_player tests.test_social_system -v
```

Expected: PASS。

- [ ] **Step 9: Commit checkpoint**

```bash
git add implementation_staging/systems/trade/player implementation_staging/systems/social implementation_staging/tests/test_trade_player.py implementation_staging/tests/test_social_system.py
git commit -m "refactor: move player trading out of social"
```

---

### Task 5: 建立顶层 TradeSystem 与统一 NPC 对话入口

**Files:**
- Create: `implementation_staging/systems/trade/handler.py`
- Create: `implementation_staging/systems/trade/events.py`
- Modify: `implementation_staging/systems/trade/__init__.py`
- Create: `implementation_staging/tests/test_trade_system.py`

**Interfaces:**

```python
class TradeSystem:
    system_name = 'trade'

    def __init__(
        self,
        role_store,
        item_registry,
        consignment_data_file,
        exchange_data_file,
        transaction_data_file,
        *,
        exchange_fee_rate: float,
        find_role,
        online_role_ids,
        push_to_role,
    ): ...

    def can_handle(self, context, message_id, fields) -> bool: ...
    def handle(self, context, message_id, fields) -> RouteResult: ...
    def npc_dialogue_frames(self, npc, role, settings): ...
    def npc_dialogue_option(self, settings, role, state, option_id, input_text=''): ...
    def disconnect_role(self, role_id: int) -> None: ...

def register_trade_routes(router: SystemRouter, system: TradeSystem) -> None: ...
```

- [ ] **Step 1: 写路由 RED 测试**

验证一个 `TradeSystem`：1138 委托 `item`，1083 委托 `crystal`，1056 委托 `player`，其他消息 not handled；`register_trade_routes()` 只增加一个顶层 route name `trade`。

- [ ] **Step 2: 写 NPC hook RED 测试**

赵公明 options 1/2 走 item，3/4/5 走 crystal；对话文本仍包含“寄售商场 / 我的寄售 / 仙晶交易所 / 寄售仙晶 / 求购仙晶”。地图只需要调用一个 trade hook。

- [ ] **Step 3: 实现顶层委托**

顶层不复制子模块业务。`events.py` 第一阶段只定义稳定事件名：

```python
TRADE_COMPLETED = 'trade.completed'
TRADE_CANCELLED = 'trade.cancelled'
```

- [ ] **Step 4: GREEN**

```bash
python -m unittest tests.test_trade_system -v
```

Expected: PASS。

- [ ] **Step 5: Commit checkpoint**

```bash
git add implementation_staging/systems/trade/handler.py implementation_staging/systems/trade/events.py implementation_staging/tests/test_trade_system.py
git commit -m "feat: add unified trade system router"
```

---

### Task 6: server.py 只装配一个 TradeSystem

**Files:**
- Modify: `implementation_staging/server.py`
- Modify: `implementation_staging/config.json`
- Modify: `implementation_staging/tests/test_system_architecture.py`
- Modify: `implementation_staging/tests/test_trade_system.py`

**Required server changes:**

1. 删除 `ConsignmentSystem/register_consignment_routes` 与 `ExchangeSystem/register_exchange_routes` imports。
2. import `TradeSystem, register_trade_routes`。
3. `Settings` 新增：

```python
trade_transactions_file: str = 'data/trade_transactions.json'
```

4. `LocalGameServer` 只保留 `self.trade_system`，构造时注入三个业务数据路径、统一 ledger 路径、费率、角色/在线/推送依赖。
5. MapSystem hooks 改为：

```python
npc_dialogue_frames_hook=[
    self.trade_system.npc_dialogue_frames,
    self.gang_system.npc_dialogue_frames,
]
npc_dialogue_option_hook=[
    self.trade_system.npc_dialogue_option,
    self.gang_system.npc_dialogue_option,
]
```

6. router 只 `register_trade_routes(...)`，不再分别注册 consignment/exchange。
7. 连接断开且已解析出 role_id 时调用 `self.trade_system.disconnect_role(role_id)`，关闭面对面交易 session；peer 在线时由 player 子模块发送取消/关窗提示。

- [ ] **Step 1: 先改架构测试为 RED 目标**

`test_system_architecture.py` 的顶层 `SYSTEMS` 去掉 `consignment`，加入 `trade`。因为 trade 是复合域，不强迫顶层具备无意义的 `service.py/protocol.py/registry.py`；新增专门的 `TradeLayoutTests` 检查 `trade/common`、`trade/item`、`trade/crystal`、`trade/player` 的设计文件。

`ServerSurfaceTests` 改为要求 `trade_system`，并明确断言不存在 `consignment_system` / `exchange_system`。

- [ ] **Step 2: 运行 RED**

```bash
python -m unittest tests.test_system_architecture tests.test_trade_system -v
```

Expected: FAIL，因为 server 仍装配旧系统。

- [ ] **Step 3: 改 server.py/config.json**

`config.json` 加：

```json
"trade_transactions_file": "data/trade_transactions.json"
```

保持现有 `consignment_data_file`、`exchange_data_file` 与 `exchange_fee_rate`。

- [ ] **Step 4: 路由优先级回归**

保持 `social` 仍早于 role/inventory 处理 1089/1009 的社交特例；`trade` 的 1056 已独占，不依赖 social。架构测试至少断言 `trade` route 存在一次、`social` 仍早于 `role` 和 `inventory`、现有 pet/task/map 优先级不变。

- [ ] **Step 5: GREEN**

```bash
python -m unittest tests.test_system_architecture tests.test_trade_system tests.test_social_system -v
```

Expected: PASS。

- [ ] **Step 6: Commit checkpoint**

```bash
git add implementation_staging/server.py implementation_staging/config.json implementation_staging/tests/test_system_architecture.py implementation_staging/tests/test_trade_system.py
git commit -m "refactor: assemble one unified trade system"
```

---

### Task 7: 幂等迁移旧 consignment/exchange 成交记录

**Files:**
- Modify: `implementation_staging/systems/trade/common/ledger.py`
- Modify: `implementation_staging/systems/trade/item/service.py`
- Modify: `implementation_staging/systems/trade/crystal/service.py`
- Modify: `implementation_staging/systems/trade/handler.py`
- Modify: `implementation_staging/tests/test_trade_ledger.py`
- Modify: `implementation_staging/tests/test_trade_item.py`
- Modify: `implementation_staging/tests/test_trade_crystal.py`

**Migration rule:** 旧业务 JSON 可继续含 `next_transaction_id` / `transactions`，但它们只读。`TradeSystem` 初始化后调用两个子服务的 `migrate_legacy_transactions()`。每条导入 ledger 时增加：

```json
"legacy_source": {"system": "consignment", "transaction_id": 7}
```

或 `system='exchange'`。

- [ ] **Step 1: 写幂等 RED 测试**

构造临时旧 consignment 文件含一条 completed transaction、旧 exchange 文件含一条 completed transaction；初始化 TradeSystem 两次，断言 ledger 只有两条，不重复导入，且新分配 transaction_id 继续从 3 开始。

- [ ] **Step 2: Item legacy converter**

旧寄售 row 的 `seller_role_id / buyer_role_id / item_instance_id / template_id / quantity / unit_price / total_price / listing_id / completed_at` 映射成统一 participants/assets/source。缺失 `created_at` 时可从对应 listing 的 `created_at` 补，仍缺失则使用 `completed_at`，不得凭空丢弃一条历史成交。

- [ ] **Step 3: Crystal legacy converter**

根据旧 row 的 `kind` 判断 poster 与 counterparty 的 buyer/seller 方向，使用 `order_id / crystals / unit_price / completed_at` 构造统一记录；优先从 orders 中补 `created_at`。

- [ ] **Step 4: GREEN**

```bash
python -m unittest tests.test_trade_ledger tests.test_trade_item tests.test_trade_crystal tests.test_trade_system -v
```

Expected: PASS。

- [ ] **Step 5: Commit checkpoint**

```bash
git add implementation_staging/systems/trade implementation_staging/tests/test_trade_*.py
git commit -m "feat: migrate legacy trade receipts into unified ledger"
```

---

### Task 8: 删除旧交易包与残留，并更新文档

**Files:**
- Delete: `implementation_staging/systems/consignment/__init__.py`
- Delete: `implementation_staging/systems/consignment/events.py`
- Delete: `implementation_staging/systems/consignment/handler.py`
- Delete: `implementation_staging/systems/consignment/protocol.py`
- Delete: `implementation_staging/systems/consignment/registry.py`
- Delete: `implementation_staging/systems/consignment/service.py`
- Delete: `implementation_staging/systems/exchange/__init__.py`
- Delete: `implementation_staging/systems/exchange/handler.py`
- Delete: `implementation_staging/systems/exchange/protocol.py`
- Delete: `implementation_staging/systems/exchange/service.py`
- Delete: `implementation_staging/tests/test_exchange_system.py`
- Modify: `implementation_staging/systems/README.md`
- Modify: `implementation_staging/TRADE_SYSTEM.md`
- Modify: `docs/protocol/1083-crystal-exchange.md`
- Modify: `docs/protocol/1138-consignment-flow.md`
- Modify: `docs/protocol/15-玩家交互协议.md`

- [ ] **Step 1: 在删除前做引用扫描**

```bash
rg "systems\.(consignment|exchange)|ConsignmentSystem|ExchangeSystem" implementation_staging docs
rg "_handle_trade|trade_requests|active_trades|trade_locks|trade_confirms" implementation_staging/systems/social
```

第一条只允许出现在明确说明“旧路径”的历史/迁移文档；运行时代码和 tests 必须已经是 `systems.trade.*`。第二条应无结果。

- [ ] **Step 2: 删除旧 packages 与旧 test_exchange_system.py**

删除后再运行相同 `rg`，确保没有运行时 import 残留。

- [ ] **Step 3: 更新 systems/README.md**

系统表改为：`social` 不含 1056；增加唯一 `trade` 行，协议入口 `1138 / 1083 / 1056`，说明 item/crystal/player 子模块与统一流水。说明 `systems/trade/` 是复合域，顶层只暴露 handler/events，具体五层职责下沉到子模块/common。

- [ ] **Step 4: 更新 TRADE_SYSTEM.md 与协议文档**

`TRADE_SYSTEM.md` 明确三种交易、统一 ledger、全局 ID、三个业务数据边界、旧记录迁移、事务失败回滚。协议文档只更新服务端模块路径，不改变已逆向确认的 wire 事实。

- [ ] **Step 5: 编译与 import 回归**

```bash
python -m compileall systems server.py tests
python -m unittest tests.test_system_architecture tests.test_trade_system tests.test_trade_item tests.test_trade_crystal tests.test_trade_player tests.test_social_system -v
```

Expected: PASS。

- [ ] **Step 6: Commit checkpoint**

```bash
git add -A implementation_staging/systems implementation_staging/tests implementation_staging/TRADE_SYSTEM.md docs/protocol
git commit -m "refactor: retire legacy consignment and exchange packages"
```

---

### Task 9: 恢复真实加密 TCP 交易回归并做完整验证

**Files:**
- Create: `implementation_staging/tests/test_trade_tcp_e2e.py`
- Modify as needed: `implementation_staging/tests/test_trade_player.py`

**Reference:** 历史已通过的 TCP 用例可从提交 `e0b221e3c0c000d9a6e20eb58e846f1efe9edba0` 的 `implementation_staging/tests/test_trade_tcp_e2e.py` 取回并适配最新架构。不要复制旧根级 imports；改用 `systems.trade.item.*` / `game.trade_system.ledger`。

- [ ] **Step 1: 恢复物品寄售真实 TCP 用例为 RED**

用 `asyncio.start_server(LocalGameServer.handle, ...)`、两个真实账号、`GameCipher` 和实际二进制帧完成：seller 登录 -> 1138/3 -> 1138/9 上架 -> buyer 登录 -> 1138/13 + 23 浏览 -> 1138/4 购买 -> buyer 收 16/1008/1017 -> seller 重连看到银两到账/无活动挂单 -> 重启服务器 -> 统一 ledger 仍只有一条 item transaction。

临时 Settings 同时提供：

```python
consignment_data_file=str(root / 'consignment.json')
exchange_data_file=str(root / 'exchange.json')
trade_transactions_file=str(root / 'trade_transactions.json')
```

- [ ] **Step 2: 跑 RED 并修到 GREEN**

```bash
python -m unittest tests.test_trade_tcp_e2e -v
```

Expected after implementation: PASS。

- [ ] **Step 3: 增加玩家交易双连接验证**

复用同一 TCP 登录 helper，同时保持两个角色在线。通过 1056 action 1/2 建立 session，双方 action 20 锁定不同真实背包物品/银两，再双方 action 10 确认。验证双方客户端收到完成/物品/货币帧，服务端角色资产互换，`trade_system.ledger.history_for_role(..., 'player')` 两边指向同一 transaction_id。

- [ ] **Step 4: 跑全部当前 unittest**

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

Expected: 不新增失败。若发现此前已存在失败，必须先在当前 master 基线复跑同一测试并记录对比；不得把旧失败归咎于本次重构。

- [ ] **Step 5: 再跑交易 + social + task/pet 邻接回归**

当前 `test_aux_systems.py` 覆盖 task/pet 等邻接系统；同时执行：

```bash
python -m unittest \
  tests.test_trade_ledger \
  tests.test_trade_item \
  tests.test_trade_crystal \
  tests.test_trade_player \
  tests.test_trade_system \
  tests.test_trade_tcp_e2e \
  tests.test_social_system \
  tests.test_aux_systems \
  tests.test_system_architecture -v
```

Expected: PASS。

- [ ] **Step 6: 最终静态检查**

```bash
rg "systems\.(consignment|exchange)" implementation_staging
rg "1056" implementation_staging/systems/social
python -m compileall implementation_staging/systems implementation_staging/server.py
```

Expected: 第一条无运行时代码命中；第二条不再有玩家交易实现命中；compileall PASS。

- [ ] **Step 7: Final commit**

```bash
git add -A
git commit -m "test: verify unified trade system end to end"
```

---

## Completion Checklist

- [ ] `systems/trade/` 是唯一顶层交易域，包含 common/item/crystal/player。
- [ ] `server.py` 只装配并注册一个 `TradeSystem`。
- [ ] 1138、1083、1056 协议行为与客户端字段布局保持不变。
- [ ] `social` 不再处理 1056，也没有交易 session 状态/结算代码。
- [ ] item/crystal 的业务挂单文件继续独立。
- [ ] 三种成功交易统一写 `data/trade_transactions.json`。
- [ ] 全局 transaction_id 跨类型唯一、重启连续、陈旧 next id 可修正。
- [ ] 旧 consignment/exchange 成交记录幂等迁入 ledger。
- [ ] 失败/取消/撤单/重复提交不产生流水。
- [ ] 保存失败可回滚资产、业务状态和 ledger；物品 identity 保持。
- [ ] 旧 `systems/consignment/` 与 `systems/exchange/` 已删除且无 runtime import。
- [ ] 交易目标测试、social、架构及完整 unittest 不新增失败。
- [ ] 真实加密 TCP 物品寄售生命周期通过；玩家双连接 1056 结算通过。
- [ ] 最终报告明确：自动化通过不等于真机通过，等待用户一次真机验收。
