# Unified Trade System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将 `systems/consignment/`、`systems/exchange/` 和 `systems/social/` 中的交易能力统一到 `systems/trade/`，拆成 `item / crystal / player` 三个子模块，并让三类成功成交共享一个持久化 `TradeLedger` 与全局 `transaction_id`。

**Architecture:** `TradeSystem` 是唯一注册到 `SystemRouter` 的交易域入口，内部按消息号把 1138、1083、1056 委托给三个子模块。物品挂单与仙晶订单继续使用各自业务文件；只有成功成交进入 `data/trade_transactions.json`。`social` 重构后只保留查看、好友、私聊、赠送、切磋和 PK。

**Tech Stack:** Python 3、标准库 `json/pathlib/dataclasses/typing/asyncio`、现有 `app.router.SystemRouter`、`app.context.SystemContext`、`protocol.py`、`RoleStore`、inventory helpers、`GameCipher`、`unittest`。

**Spec:** `docs/superpowers/specs/2026-09-13-unified-trade-system-design.md`

## Global Constraints

- 基于实施时最新 `master` 工作，不覆盖 task/pet/map/team 等其他系统的新改动。
- 严格 TDD：先 RED，再最小 GREEN，再 REFACTOR；每个 Task 完成后独立提交。
- 不改变 APK 的 1138 / 1083 / 1056 消息号、字段顺序、字段类型、页面跳转和现有业务语义。
- 物品寄售、仙晶订单、玩家面对面交易的业务模型保持独立，只统一交易域、公共事务和最终成交流水。
- 宠物寄售继续返回“宠物寄售暂未开放”，不得猜测宠物交易协议。
- `server.py` 只负责装配、路由和网络生命周期，不新增交易业务分支。
- 新成交历史唯一权威来源是 `trade_transactions.json`；旧业务文件中的 `transactions` 只做兼容读取与幂等迁移，不再写新记录。
- 角色资产、业务订单状态、统一 ledger 作为一个逻辑事务提交；任一持久化失败时全部恢复。文件系统层面不宣称数据库级 ACID。
- 物品失败回滚必须保留原 Python item 对象 identity。
- 挂单、撤单、取消、仅锁定、校验失败、保存失败、自交易、重复购买/应单均不得留下成交记录。
- 自动化通过不代表真机通过；最后由用户进行一次真机验收。

---

### Task 1: 建立统一 TradeLedger 与公共事务核心

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
class TradeLedgerError(RuntimeError):
    pass

class TradeLedger:
    def __init__(self, path: str | Path): ...
    def record_completed(
        self, *, trade_type: str,
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
T = TypeVar('T')

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

- [ ] **Step 1: 写 Ledger RED 测试**

```python
def test_global_ids_cross_trade_types(self):
    first = self.ledger.record_completed(
        trade_type='item',
        participants=[{'role_id': 1, 'side': 'seller'}, {'role_id': 2, 'side': 'buyer'}],
        assets=[], source={'type': 'listing', 'id': 10}, created_at=1, completed_at=2,
    )
    second = self.ledger.record_completed(
        trade_type='crystal',
        participants=[{'role_id': 3, 'side': 'seller'}, {'role_id': 1, 'side': 'buyer'}],
        assets=[], source={'type': 'order', 'id': 11}, created_at=3, completed_at=4,
    )
    self.assertEqual((first['transaction_id'], second['transaction_id']), (1, 2))
    self.assertEqual(len(self.ledger.history_for_role(1)), 2)
```

同一测试文件再明确覆盖：重启恢复、陈旧 `next_transaction_id` 自动修正、`trade_type` 过滤、损坏已有 ledger 抛 `TradeLedgerError`。

- [ ] **Step 2: 运行 RED**

```bash
cd implementation_staging
python -m unittest tests.test_trade_ledger -v
```

Expected: FAIL / ImportError，因为 `systems.trade.common` 尚不存在。

- [ ] **Step 3: 实现 models.py 与 ledger.py**

`models.py` 固定：

```python
TRADE_TYPES = {'item', 'crystal', 'player'}
COMPLETED = 'completed'
```

`ledger.py` 初始化数据固定为：

```json
{"next_transaction_id": 1, "transactions": []}
```

`save()` 写 `<ledger>.tmp` 后 `replace()`；若 ledger 文件已存在但 JSON/结构非法，抛 `TradeLedgerError`，禁止重置为空。

- [ ] **Step 4: 运行 Ledger 测试到 GREEN**

```bash
python -m unittest tests.test_trade_ledger -v
```

Expected: PASS。

- [ ] **Step 5: 写公共事务 RED 测试**

加入两个测试：第三个保存动作（ledger.save）抛错后角色/业务/ledger 全恢复；物品已从 seller list 移到 buyer list 后失败，恢复时 `seller['items'][0] is original_item`。

- [ ] **Step 6: 实现 commit_trade()**

实现顺序固定：快照角色、业务数据、ledger → `apply()` 修改内存并用 `record_completed(..., persist=False)` 生成待提交记录 → `role_save()` → `business_save()`（非 None）→ `ledger.save()`。异常时先抓取参与角色当前 item 对象池，再原位恢复角色与对象 identity、恢复业务 dict、恢复 ledger snapshot，并 best-effort 重写已经成功保存过的文件，最后重新抛原异常。

- [ ] **Step 7: 运行公共事务测试到 GREEN**

```bash
python -m unittest tests.test_trade_ledger -v
```

Expected: PASS。

- [ ] **Step 8: Commit**

```bash
git add implementation_staging/systems/trade implementation_staging/data/trade_transactions.json implementation_staging/tests/test_trade_ledger.py
git commit -m "feat: add unified trade ledger and transaction core"
```

---

### Task 2: 迁移 1138 物品寄售到 trade/item

**Files:**
- Move: `implementation_staging/systems/consignment/` → `implementation_staging/systems/trade/item/`
- Create: `implementation_staging/tests/test_trade_item.py`
- Modify: `implementation_staging/tests/test_aux_systems.py`

**Interfaces:**

```python
class ItemTradeService:
    def __init__(self, role_store, item_registry, data_file, ledger: TradeLedger): ...
    def list_item(self, seller, instance_id: int, quantity: int, unit_price: int): ...
    def search(self, category_id: int): ...
    def my_listings(self, role_id: int): ...
    def unlist(self, seller, item_instance_id: int): ...
    def buy(self, buyer, item_instance_id: int): ...
    def order_history(self, role_id: int, *, status: str | None = None): ...
    def trade_history(self, role_id: int, side: str = 'all'): ...
    def migrate_legacy_transactions(self) -> int: ...
```

- [ ] **Step 1: 写新路径 RED 测试**

把 `test_aux_systems.py` 的 `ConsignmentSystemTests` 迁到 `test_trade_item.py`，import 改成 `systems.trade.item.*`；新增成功购买断言：ledger 只有一条 `trade_type='item'`，`source={'type':'listing', ...}`，assets 同时有 item 与 silver 且方向正确。再新增撤单不写流水、double-buy 不写第二条、ledger 保存失败完整回滚且 item identity 不变。

- [ ] **Step 2: 运行 RED**

```bash
python -m unittest tests.test_trade_item -v
```

Expected: FAIL / ImportError。

- [ ] **Step 3: 执行目录迁移并修正内部 imports**

```bash
git mv implementation_staging/systems/consignment implementation_staging/systems/trade/item
```

运行时代码 imports 全部从 `systems.consignment.*` 改为 `systems.trade.item.*`；类改名为 `ItemTradeSystem` / `ItemTradeService`。wire-level 的 `CONSIGNMENT_*` 常量名称保持不变。

- [ ] **Step 4: 将 buy() 接入 commit_trade() 与 TradeLedger**

成功购买的 `apply()` 必须同时：移动同一 item 对象、买家扣银、卖家加银、listing 置 `sold`，并调用：

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
    created_at=int(listing['created_at']), completed_at=completed_at,
    persist=False,
)
```

新成交不得 append 旧 `transactions`，不得递增旧 `next_transaction_id`。`trade_history()` 改为查询 `ledger.history_for_role(role_id, 'item')` 并按 side 过滤 participants。

- [ ] **Step 5: 运行 item + aux 回归**

```bash
python -m unittest tests.test_trade_item tests.test_aux_systems -v
```

Expected: PASS。

- [ ] **Step 6: Commit**

```bash
git add -A implementation_staging/systems/trade/item implementation_staging/tests/test_trade_item.py implementation_staging/tests/test_aux_systems.py
git commit -m "refactor: move item consignment under trade domain"
```

---

### Task 3: 迁移 1083 仙晶交易所到 trade/crystal

**Files:**
- Move: `implementation_staging/systems/exchange/` → `implementation_staging/systems/trade/crystal/`
- Move: `implementation_staging/tests/test_exchange_system.py` → `implementation_staging/tests/test_trade_crystal.py`

**Interfaces:**

```python
class CrystalTradeService:
    def __init__(self, role_store, data_file, ledger: TradeLedger, fee_rate: float = 0.02): ...
    def fee_quote(self, crystals: int, unit_price: int): ...
    def post_order(self, poster, kind: str, crystals: int, unit_price: int): ...
    def cancel_order(self, poster, order_id: int): ...
    def accept_order(self, acceptor, order_id: int): ...
    def market_orders(self, tab: int): ...
    def my_orders(self, role_id: int, mode: int | None = None): ...
    def my_order_ids(self, role_id: int, tab: int): ...
    def migrate_legacy_transactions(self) -> int: ...
```

- [ ] **Step 1: 先移动测试并制造 RED**

```bash
git mv implementation_staging/tests/test_exchange_system.py implementation_staging/tests/test_trade_crystal.py
```

把 imports 改成 `systems.trade.crystal.*`，新增四类断言：post/cancel 不写 ledger；accept 成功只写一条 `crystal`；double fill 不增加流水；ledger/save 失败恢复订单状态与双方银两/仙晶。

- [ ] **Step 2: 运行 RED**

```bash
python -m unittest tests.test_trade_crystal -v
```

Expected: FAIL / ImportError。

- [ ] **Step 3: 执行目录迁移并修正 imports/classes**

```bash
git mv implementation_staging/systems/exchange implementation_staging/systems/trade/crystal
```

内部 imports 改为 `systems.trade.crystal.*`，类改名 `CrystalTradeSystem` / `CrystalTradeService`。1083 action 0/3/4/5/6/10/11/12/13/15/16 及 screen 350/351 frame 构造原样保留。

- [ ] **Step 4: accept_order() 接入统一事务与 ledger**

`kind='buy'` 时 poster 是 buyer、acceptor 是 seller；`kind='sell'` 时 poster 是 seller、acceptor 是 buyer。流水 participants 必须按真实 buyer/seller 方向填写；assets 记录 crystal 与 silver 两条真实方向。发布时已扣的 fee 保持当前业务语义，不伪装成成交时玩家间资产。

- [ ] **Step 5: 保持通知只发生在提交成功后**

`_notify_counterparty()` 只在 `accept_order()` 成功提交以后调用；推送异常继续只记 debug，不回滚已经成功持久化的成交。

- [ ] **Step 6: 运行 crystal 回归**

```bash
python -m unittest tests.test_trade_crystal -v
```

Expected: PASS。

- [ ] **Step 7: Commit**

```bash
git add -A implementation_staging/systems/trade/crystal implementation_staging/tests/test_trade_crystal.py
git commit -m "refactor: move crystal exchange under trade domain"
```

---

### Task 4: 从 social 剥离 1056 玩家面对面交易

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
    def open_trade(self, left_role_id: int, right_role_id: int) -> PlayerTradeSession: ...
    def session_for(self, role_id: int) -> PlayerTradeSession | None: ...
    def trade_peer(self, role_id: int) -> int | None: ...
    def close_trade(self, role_id: int) -> int | None: ...
```

- [ ] **Step 1: 建立 player RED 测试**

从 `test_social_system.py` 复制 1056 测试到 `test_trade_player.py`：请求/接受开窗、锁定后启用确认、双方确认交换物品和银两、单方确认不结算、物品消失失败、关闭通知 peer。新增：成功结算写一条 `player` ledger；取消/失败不写；保存失败恢复双方资产且不写；`disconnect_role()` 关闭 session。

- [ ] **Step 2: 运行 RED**

```bash
python -m unittest tests.test_trade_player -v
```

Expected: FAIL / ImportError。

- [ ] **Step 3: 移动 wire helpers**

把以下函数从 `social/protocol.py` 原样移动到 `trade/player/protocol.py`：`trade_request_frame`、`trade_open_frame`、`trade_peer_money_frame`、`trade_peer_items_frame`、`trade_enable_confirm_frame`、`trade_complete_frame`、`trade_close_frames`。

- [ ] **Step 4: 实现 PlayerTradeRegistry**

沿用 pending request TTL=60 秒；`open_trade()` 分配进程内递增 `session_id` 并双向索引同一个 session。session id 只作为 ledger `source={'type':'player_session','id':...}`，不承担跨重启唯一性。

- [ ] **Step 5: 移动 settle_trade 业务到 PlayerTradeService**

完整保留余额、item 在 bag、重复 item、双方背包容量检查；通过 `commit_trade()` 执行资产交换和 `TradeLedger.record_completed(trade_type='player', ...)`。assets 对每件 item 记录方向；双方实际给出的 silver 分别记录方向，金额为 0 时不写该 asset。

- [ ] **Step 6: 实现 PlayerTradeSystem 1056 actions**

保持 action 1/2/3/4/20/10 的既有客户端行为；最终第二方确认成功后发送当前已有的 1056/20、1056/11/12、1008、1009、1017、1049 帧，然后关闭 session。

- [ ] **Step 7: 清理 social 并写边界断言**

`HANDLED_MESSAGE_IDS` 删除 1056；`handle()` 删除 1056 分支；删除 `_handle_trade`；`social.protocol` 删除 trade frame；`social.service` 删除交易结算类/函数；`SocialRegistry` 删除 `trade_requests/active_trades/trade_locks/trade_confirms`。

在 `test_social_system.py` 增加：

```python
self.assertFalse(self.system.can_handle(
    self._context(self.alice), 1056, [byte(1), integer(1)]
))
self.assertFalse(hasattr(self.system.registry, 'active_trades'))
```

- [ ] **Step 8: 运行 player + social 回归**

```bash
python -m unittest tests.test_trade_player tests.test_social_system -v
```

Expected: PASS。

- [ ] **Step 9: Commit**

```bash
git add implementation_staging/systems/trade/player implementation_staging/systems/social implementation_staging/tests/test_trade_player.py implementation_staging/tests/test_social_system.py
git commit -m "refactor: move player trading out of social"
```

---

### Task 5: 建立顶层 TradeSystem 并让 server.py 只装配它

**Files:**
- Create: `implementation_staging/systems/trade/handler.py`
- Create: `implementation_staging/systems/trade/events.py`
- Modify: `implementation_staging/systems/trade/__init__.py`
- Modify: `implementation_staging/server.py`
- Modify: `implementation_staging/config.json`
- Modify: `implementation_staging/tests/test_system_architecture.py`
- Create: `implementation_staging/tests/test_trade_system.py`

**Interfaces:**

```python
class TradeSystem:
    system_name = 'trade'
    def can_handle(self, context, message_id: int, fields: list[object]) -> bool: ...
    def handle(self, context, message_id: int, fields: list[object]) -> RouteResult: ...
    def npc_dialogue_frames(self, npc, role, settings): ...
    def npc_dialogue_option(self, settings, role, state, option_id: int, input_text: str = ''): ...
    def disconnect_role(self, role_id: int) -> None: ...

def register_trade_routes(router: SystemRouter, system: TradeSystem) -> None:
    router.register(system.system_name, system.can_handle, system.handle)
```

- [ ] **Step 1: 写顶层路由与 NPC RED 测试**

`test_trade_system.py` 断言：1138→item、1083→crystal、1056→player、未知消息 not handled；`register_trade_routes()` 只添加一个 route `trade`；赵公明对话仍包含“寄售商场 / 我的寄售 / 仙晶交易所 / 寄售仙晶 / 求购仙晶”，options 1/2 委托 item，3/4/5 委托 crystal。

- [ ] **Step 2: 修改架构测试为目标结构并运行 RED**

`test_system_architecture.py` 的顶层 systems 去掉 `consignment`，加入 `trade`；不要要求 composite trade 顶层伪造 `service.py/protocol.py/registry.py`，改为专门断言 `trade/common`、`trade/item`、`trade/crystal`、`trade/player` 的必需文件。`ServerSurfaceTests` 要求 `trade_system`，并断言没有 `consignment_system` / `exchange_system`。

```bash
python -m unittest tests.test_trade_system tests.test_system_architecture -v
```

Expected: FAIL，因为 server 仍装配旧入口。

- [ ] **Step 3: 实现 TradeSystem**

构造时创建唯一 `TradeLedger` 并注入三个子模块；`can_handle` 只认 1138/1083/1056，`handle` 按 message id 委托。`events.py` 定义：

```python
TRADE_COMPLETED = 'trade.completed'
TRADE_CANCELLED = 'trade.cancelled'
```

NPC hooks 由顶层依次委托 item/crystal，不复制具体页面逻辑。

- [ ] **Step 4: 修改 Settings/config/server 装配**

`Settings` 与 `config.json` 增加：

```python
trade_transactions_file: str = 'data/trade_transactions.json'
```

删除 server 对 `ConsignmentSystem` / `ExchangeSystem` 的 imports、实例化和独立 route 注册；只实例化 `self.trade_system`。Map hooks 改成：

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

连接断开且已知 role_id 时调用 `self.trade_system.disconnect_role(role_id)` 清理玩家交易 session。

- [ ] **Step 5: 运行架构/路由/social 回归**

```bash
python -m unittest tests.test_trade_system tests.test_system_architecture tests.test_social_system -v
```

Expected: PASS。

- [ ] **Step 6: Commit**

```bash
git add implementation_staging/systems/trade/handler.py implementation_staging/systems/trade/events.py implementation_staging/server.py implementation_staging/config.json implementation_staging/tests/test_trade_system.py implementation_staging/tests/test_system_architecture.py
git commit -m "refactor: assemble one unified trade system"
```

---

### Task 6: 幂等迁移旧成交记录并清理旧路径/文档

**Files:**
- Modify: `implementation_staging/systems/trade/common/ledger.py`
- Modify: `implementation_staging/systems/trade/item/service.py`
- Modify: `implementation_staging/systems/trade/crystal/service.py`
- Modify: `implementation_staging/systems/trade/handler.py`
- Modify: `implementation_staging/tests/test_trade_ledger.py`
- Modify: `implementation_staging/tests/test_trade_item.py`
- Modify: `implementation_staging/tests/test_trade_crystal.py`
- Modify: `implementation_staging/systems/README.md`
- Modify: `implementation_staging/TRADE_SYSTEM.md`
- Modify: `docs/protocol/1083-crystal-exchange.md`
- Modify: `docs/protocol/1138-consignment-flow.md`
- Modify: `docs/protocol/15-玩家交互协议.md`

- [ ] **Step 1: 写 legacy migration RED 测试**

临时 consignment JSON 放一条旧 completed transaction，临时 exchange JSON 放一条旧 completed transaction；初始化 `TradeSystem` 两次，断言 ledger 只有两条，并分别带：

```json
{"legacy_source": {"system": "consignment", "transaction_id": 7}}
```

和 `system="exchange"`。然后新成交的 `transaction_id` 必须从已导入 ledger 的最大统一 ID + 1 继续。

- [ ] **Step 2: 实现幂等 importer**

`TradeLedger.has_legacy_source(system, transaction_id)` 做查重。item importer 用旧 seller/buyer/item/listing/quantity/price 映射统一结构；crystal importer 根据旧 `kind` 推导 poster/counterparty 的 buyer/seller 方向。缺 `created_at` 时优先从对应 listing/order 补，仍缺时使用 `completed_at`。

- [ ] **Step 3: 运行 migration GREEN**

```bash
python -m unittest tests.test_trade_ledger tests.test_trade_item tests.test_trade_crystal tests.test_trade_system -v
```

Expected: PASS。

- [ ] **Step 4: 运行引用扫描并清理残留**

```bash
rg "systems\.(consignment|exchange)|ConsignmentSystem|ExchangeSystem" implementation_staging
rg "_handle_trade|trade_requests|active_trades|trade_locks|trade_confirms" implementation_staging/systems/social
```

Expected: 运行时代码无旧 package/class 引用；social 无交易实现/状态引用。历史设计文档中的旧路径说明可以保留。

- [ ] **Step 5: 更新文档到最终领域边界**

`systems/README.md`：social 去掉 1056；新增唯一 `trade` 行，协议入口 `1138 / 1083 / 1056`，说明 item/crystal/player 与统一 ledger。`TRADE_SYSTEM.md` 改成三类交易、统一 ID、统一账本、三个业务数据边界、回滚与 legacy migration。三个 protocol 文档只更新服务端代码路径，不更改逆向确认的 wire 事实。

- [ ] **Step 6: 编译与目标回归**

```bash
python -m compileall systems server.py tests
python -m unittest tests.test_trade_ledger tests.test_trade_item tests.test_trade_crystal tests.test_trade_player tests.test_trade_system tests.test_social_system tests.test_system_architecture -v
```

Expected: PASS。

- [ ] **Step 7: Commit**

```bash
git add -A implementation_staging docs/protocol
git commit -m "feat: migrate trade history and retire legacy trade paths"
```

---

### Task 7: 恢复真实加密 TCP 回归并做最终验证

**Files:**
- Create: `implementation_staging/tests/test_trade_tcp_e2e.py`

**Reference:** 以提交 `e0b221e3c0c000d9a6e20eb58e846f1efe9edba0` 的 `implementation_staging/tests/test_trade_tcp_e2e.py` 为已验证 TCP harness 基线，适配到当前 `systems.trade.*` 和 `game.trade_system.ledger`；不复制旧根级 imports。

- [ ] **Step 1: 恢复物品寄售 TCP RED 测试**

测试使用 `asyncio.start_server(LocalGameServer.handle, ...)`、两个真实账号、`GameCipher`、实际 encode/decode frame：seller 登录→1138/3→1138/9 上架→buyer 登录→1138/13+23 浏览→1138/4 购买→buyer 收 16/1008/1017→seller 重连看到银两到账且无活动挂单→重启服务器→`trade_system.ledger` 仍只有一条 item transaction。

临时 Settings 明确配置：

```python
consignment_data_file=str(root / 'consignment.json')
exchange_data_file=str(root / 'exchange.json')
trade_transactions_file=str(root / 'trade_transactions.json')
```

- [ ] **Step 2: 运行 TCP RED**

```bash
python -m unittest tests.test_trade_tcp_e2e -v
```

Expected: 如果适配尚有遗漏则 FAIL，失败点必须对应当前架构路径/装配，不允许绕过真实 TCP。

- [ ] **Step 3: 修正 TCP harness/实现直到物品生命周期 GREEN**

只修复测试暴露的实际兼容问题；不得改 wire contract 来迎合测试。

- [ ] **Step 4: 在同一文件增加玩家双连接 TCP 用例**

保持两个角色在线，经 1056 action 1/2 建立 session；双方 action 20 锁定不同真实背包物品/银两；双方 action 10 最终确认。断言双方客户端收到完成/物品/货币帧、服务端资产互换，且 `trade_system.ledger.history_for_role(role_id, 'player')` 两边指向同一 `transaction_id`。

- [ ] **Step 5: 运行 TCP GREEN**

```bash
python -m unittest tests.test_trade_tcp_e2e -v
```

Expected: PASS。

- [ ] **Step 6: 跑完整 unittest**

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

Expected: 不新增失败。若出现失败，先在本次重构前的基线提交复跑同名测试，区分 pre-existing 与 regression 后再修复本次回归。

- [ ] **Step 7: 跑交易与邻接系统聚焦回归**

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

- [ ] **Step 8: 最终静态检查**

```bash
rg "systems\.(consignment|exchange)" implementation_staging
rg "1056" implementation_staging/systems/social
python -m compileall implementation_staging/systems implementation_staging/server.py
```

Expected: 第一条无运行时代码命中；第二条无玩家交易实现命中；compileall PASS。

- [ ] **Step 9: Commit**

```bash
git add -A
git commit -m "test: verify unified trade system end to end"
```

---

## Completion Checklist

- [ ] `systems/trade/` 是唯一顶层交易域，包含 common/item/crystal/player。
- [ ] `server.py` 只装配并注册一个 `TradeSystem`。
- [ ] 1138 / 1083 / 1056 wire contract 保持不变。
- [ ] `social` 不再处理 1056，也没有交易 session 状态或交易结算代码。
- [ ] item/crystal 业务挂单文件继续独立。
- [ ] 三类成功交易统一写 `data/trade_transactions.json`。
- [ ] 全局 transaction_id 跨类型唯一、重启连续、陈旧 next id 自动修正。
- [ ] 旧 consignment/exchange 成交历史幂等迁入 ledger。
- [ ] 失败/取消/撤单/重复提交不产生成交流水。
- [ ] 保存失败回滚资产、业务状态和 ledger，物品 identity 保持。
- [ ] 运行时代码无 `systems.consignment` / `systems.exchange` 旧路径。
- [ ] 交易、social、architecture、完整 unittest 不新增失败。
- [ ] 真实加密 TCP 物品寄售生命周期通过。
- [ ] 真实双连接 1056 玩家交易结算通过。
- [ ] 最终报告不把自动化测试等同于真机验收。
