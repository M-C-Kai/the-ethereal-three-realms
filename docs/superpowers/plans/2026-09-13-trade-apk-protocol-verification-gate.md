# Trade APK Protocol Verification Gate Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:systematic-debugging for any mismatch discovered, then superpowers:test-driven-development for every protocol correction. This gate MUST finish before `docs/superpowers/plans/2026-09-13-unified-trade-system.md` Task 1 begins.

**Goal:** 直接从原始 APK / 完整 smali 证据重新锁定 1138、1083、1056 三套交易协议的双向字段与页面路由，形成可执行协议矩阵与契约测试，避免把旧服务端中的错误假设原样迁入新 `systems/trade/` 架构。

**Architecture:** 本计划不做交易域重构。先建立“APK 事实 → 协议矩阵 → 自动化契约测试 → 必要的协议修正”闭环；Gate 通过后才允许执行统一交易系统主计划。

**Tech Stack:** apktool/smali、现有 APK 反编译资料、Python `unittest`、现有 `protocol.py`、`systems/consignment`、`systems/exchange`、`systems/social`。

**Spec:** `docs/superpowers/specs/2026-09-13-unified-trade-system-apk-protocol-gate.md`

## Global Constraints

- 原始 APK 是最高协议事实来源；当前 Python 实现和旧测试都只能作为待核对对象。
- 必须区分 C→S 与 S→C；同一个 action 在不同方向的含义不能合并描述。
- 不使用 OCR 解析 smali；直接读取反编译文本与调用链。
- 每个字段都记录类型、下标、含义和证据位置。
- 只要发现当前实现与 APK 不一致，先写 RED 测试再修复。
- 在 Gate 通过前禁止移动 `consignment` / `exchange` 目录，也禁止从 `social` 抽离 1056。
- 不开放宠物寄售，不猜测 APK 未锁定字段。

---

### Task 0: 固定输入与证据目录

**Files:**
- Inspect: `piaomiao_local_login.apk`
- Inspect: `implementation_staging/references/smali/`
- Create: `docs/protocol/trade-apk-protocol-matrix.md`

- [ ] **Step 1: 确认 APK 与反编译目录同源**

记录 APK 文件名、大小、SHA-256；如果仓库中的 `references/smali` 不是由当前 APK 产生，则重新 apktool 解包到临时工作目录，不覆盖仓库已有证据。

- [ ] **Step 2: 建立矩阵骨架**

矩阵固定列：

```text
message_id | direction | action | field_types | field_meanings | sender_evidence | receiver_evidence | screen | confidence | python_status
```

其中 `python_status` 只允许 `match / mismatch / not-implemented / unresolved`。

- [ ] **Step 3: Commit checkpoint**

```bash
git add docs/protocol/trade-apk-protocol-matrix.md
git commit -m "docs: start APK trade protocol evidence matrix"
```

---

### Task 1: 重新锁定 1138 物品寄售

**Files:**
- Inspect: APK/smali 中所有 `0x472` / `1138` 构造与接收分支
- Inspect: `implementation_staging/systems/consignment/protocol.py`
- Inspect: `implementation_staging/systems/consignment/handler.py`
- Modify: `docs/protocol/trade-apk-protocol-matrix.md`
- Create: `implementation_staging/tests/test_trade_apk_contract_1138.py`

- [ ] **Step 1: 搜索所有 1138 发送点**

必须逐个确认 action `3, 13, 0, 23, 7, 9, 2, 4` 的 C→S 构造方法。对每个字段记录写入 API（byte/short/int/string 对应的 smali 调用）和参数来源。

- [ ] **Step 2: 搜索所有 1138 接收点**

锁定 action `1, 3, 7, 9, 13, 15, 16` 以及当前服务端实际返回的其他 action，记录客户端读取 API、下标和路由到 screen 44/70/73/613 的证据。

- [ ] **Step 3: 特别验证行结构**

分别验证：

```text
market row: object_type / item_instance_id / template_id / quantity / price / display_name / seller_role_id / seller_name
own row:    object_type / item_instance_id / template_id / quantity / price / display_name / seller_role_id
```

若 APK 实际读取顺序或类型不同，矩阵标 `mismatch`，不得继续沿用旧结构。

- [ ] **Step 4: 验证角色 id=0 与 object type**

找到客户端角色 id 来源与物品/宠物 object type 写入点；把“0 是否正常”的结论写入证据，而不是只沿用现有兼容注释。

- [ ] **Step 5: 写 1138 契约测试**

测试至少锁定每个 confirmed-bidirectional 请求 detector 的精确 field types，以及每个服务端 frame 的 action、字段数量和逐字段 type_id。

- [ ] **Step 6: 运行契约测试**

```bash
cd implementation_staging
python -m unittest tests.test_trade_apk_contract_1138 -v
```

Expected: 当前实现正确则 PASS；若 FAIL，进入 systematic-debugging，先修协议再继续 Gate。

- [ ] **Step 7: Commit**

```bash
git add docs/protocol/trade-apk-protocol-matrix.md implementation_staging/tests/test_trade_apk_contract_1138.py implementation_staging/systems/consignment
git commit -m "test: lock 1138 protocol against APK evidence"
```

---

### Task 2: 重新锁定 1083 仙晶交易所

**Files:**
- Inspect: APK/smali 中所有 `0x43b` / `1083` 构造与接收分支
- Inspect: `implementation_staging/systems/exchange/protocol.py`
- Inspect: `implementation_staging/systems/exchange/handler.py`
- Modify: `docs/protocol/trade-apk-protocol-matrix.md`
- Create: `implementation_staging/tests/test_trade_apk_contract_1083.py`

- [ ] **Step 1: 锁定 screen 350 的全部交互**

逐项确认：

```text
[4, tab]
[5, tab]
[0, page, size, tab]
[3, order_id]
```

同时确认服务端 action `0/3/4/5/6` 的客户端读取字段与 screen 350 路由。

- [ ] **Step 2: 锁定 screen 351 的全部交互**

逐项确认：

```text
[10, mode]
[11, page, size, mode]
[12, mode, num, price]
[13, order_id]
[15, num, price]
[16, num, price]
```

确认 mode 0/1、求购/出售语义及字段类型。

- [ ] **Step 3: 验证应单资产方向**

从客户端文案与发送逻辑共同确认：求购单应单者交仙晶收银两；出售单应单者交银两收仙晶。矩阵中必须分别写 buyer/seller 身份，不能只写 poster/acceptor。

- [ ] **Step 4: 写 1083 契约测试并运行**

```bash
python -m unittest tests.test_trade_apk_contract_1083 -v
```

要求锁定所有已确认 action 的逐字段 type_id、screen open frame 和列表行布局。

- [ ] **Step 5: Commit**

```bash
git add docs/protocol/trade-apk-protocol-matrix.md implementation_staging/tests/test_trade_apk_contract_1083.py implementation_staging/systems/exchange
git commit -m "test: lock 1083 protocol against APK evidence"
```

---

### Task 3: 重新锁定 1056 玩家面对面交易

**Files:**
- Inspect: APK/smali 中所有 `0x420` / `1056` 构造与接收分支
- Inspect: `implementation_staging/systems/social/handler.py`
- Inspect: `implementation_staging/systems/social/protocol.py`
- Inspect: `implementation_staging/systems/social/registry.py`
- Inspect: `implementation_staging/systems/social/service.py`
- Modify: `docs/protocol/trade-apk-protocol-matrix.md`
- Create: `implementation_staging/tests/test_trade_apk_contract_1056.py`

- [ ] **Step 1: 建立双向 action 表**

C→S 与 S→C 分开记录 action `1,2,3,4,5,6,8,10,11,12,20`；不存在于某方向的 action 明确写 `N/A`。

- [ ] **Step 2: 锁定握手与窗口字段**

确认请求、接受、拒绝、开窗、关闭使用的是 actor id 还是 role id，并找到 `player_actor_object_id` 对应换算的客户端证据。

- [ ] **Step 3: 锁定锁定报价 payload**

确认 C→S action 20 的完整结构：银两、物品数量、逐项实例 id 以及任何保留字段；确认客户端锁定后是否允许重新发送 action 20。

- [ ] **Step 4: 锁定 S→C 物品行**

对 action 8 每一件物品的 6 个字段逐个确认读取类型和用途，特别核对 slot/template/quantity/icon 的位置。

- [ ] **Step 5: 锁定 action 10 与 action 20 的方向语义**

明确区分“服务端启用确认按钮”“客户端最终确认”“服务端完成标志”，防止重构时把相同 action 常量误认为同一业务事件。

- [ ] **Step 6: 写 1056 契约测试并运行**

```bash
python -m unittest tests.test_trade_apk_contract_1056 -v
```

同时保留现有玩家交易成功/失败行为测试，不允许为了契约测试通过而削弱原结算测试。

- [ ] **Step 7: Commit**

```bash
git add docs/protocol/trade-apk-protocol-matrix.md implementation_staging/tests/test_trade_apk_contract_1056.py implementation_staging/systems/social
git commit -m "test: lock 1056 protocol against APK evidence"
```

---

### Task 4: APK 证据与 Python 实现差异清零

**Files:**
- Modify only when evidence requires: `implementation_staging/systems/consignment/*`
- Modify only when evidence requires: `implementation_staging/systems/exchange/*`
- Modify only when evidence requires: `implementation_staging/systems/social/*`
- Modify: `docs/protocol/trade-apk-protocol-matrix.md`

- [ ] **Step 1: 汇总所有 mismatch**

矩阵过滤 `python_status=mismatch`。每个 mismatch 单独执行 systematic-debugging：先定位旧实现为什么偏离，再写最小 RED 测试。

- [ ] **Step 2: 逐项最小修复**

只修 APK 证据能证明的协议问题，不在此阶段做目录迁移、统一 Ledger 或业务重构。

- [ ] **Step 3: 跑三套协议契约测试**

```bash
python -m unittest \
  tests.test_trade_apk_contract_1138 \
  tests.test_trade_apk_contract_1083 \
  tests.test_trade_apk_contract_1056 -v
```

Expected: PASS。

- [ ] **Step 4: 跑现有交易行为回归**

```bash
python -m unittest tests.test_aux_systems tests.test_exchange_system tests.test_social_system -v
```

Expected: PASS；若当前 master 的文件名已变化，以同等最新测试模块替换，但不得减少 1138/1083/1056 覆盖。

- [ ] **Step 5: Commit**

```bash
git add implementation_staging/systems docs/protocol/trade-apk-protocol-matrix.md implementation_staging/tests
git commit -m "fix: align trade protocols with APK evidence"
```

如果没有 mismatch，本 Task 不需要业务代码提交，只提交最终矩阵状态即可。

---

### Task 5: Gate 最终判定

- [ ] **Step 1: 检查矩阵完整性**

1138、1083、1056 当前服务器使用的每个 action 都必须有一行；每个资产结算相关字段不得为 `unresolved`。

- [ ] **Step 2: 检查证据等级**

资产结算与客户端固定下标读取字段必须达到 `confirmed-bidirectional`；无法达到时停止主重构计划并继续逆向，不得用旧实现猜测补齐。

- [ ] **Step 3: 最终测试**

```bash
python -m unittest \
  tests.test_trade_apk_contract_1138 \
  tests.test_trade_apk_contract_1083 \
  tests.test_trade_apk_contract_1056 \
  tests.test_aux_systems \
  tests.test_exchange_system \
  tests.test_social_system -v
```

- [ ] **Step 4: 写 Gate 结论到矩阵顶部**

只有所有强制条件满足时写：

```text
APK_PROTOCOL_GATE=PASSED
verified_apk=<sha256>
verified_at=<UTC timestamp>
```

否则写 `APK_PROTOCOL_GATE=BLOCKED` 并列出剩余证据缺口。

- [ ] **Step 5: Commit**

```bash
git add docs/protocol/trade-apk-protocol-matrix.md implementation_staging/tests
git commit -m "docs: pass APK trade protocol verification gate"
```

Gate 显示 `PASSED` 后，才开始执行 `2026-09-13-unified-trade-system.md` 的统一 Ledger 和目录重构。
