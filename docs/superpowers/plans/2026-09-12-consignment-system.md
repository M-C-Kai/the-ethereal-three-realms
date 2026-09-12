# 寄售系统 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将赵公明原生寄售入口、1138 分类页、真实物品上架/查询/我的寄售/下架/购买整合成一个持久化的物品寄售系统。

**Architecture:** `consignment_service.py` 负责寄售状态、物品托管、银两与角色持久化；`consignment_protocol.py` 仅负责 APK 1138 请求解析与响应编码；`server.py` 仅负责协议分发和客户端刷新。寄售记录持久化到独立 JSON 文件，并始终以真实 `ItemInstance.id` 为交易对象。

**Tech Stack:** Python 3.12、现有自定义 TLV 协议、JSON 持久化、`unittest`。

**Spec:** `docs/superpowers/specs/2026-09-12-consignment-market-design.md`

## Global Constraints

- 只实现物品寄售；宠物 `object_type=3` 不实现。
- 交易必须使用真实物品实例，不按模板复制整件物品。
- 整件上架后实例必须离开角色背包；下架/购买继续使用同一实例 ID。
- 部分堆叠上架必须拆出新的全局唯一实例 ID。
- 购买必须同时更新买家银两、卖家银两、物品所有权和 listing 状态。
- 任何失败不得产生重复物品、负银两或丢物。
- 1138 S→C 记录字段必须按 APK 读取顺序编码，不使用猜测字段。
- 宠物寄售、摆摊 1731、竞价、跨服、邮件取回均不在本轮范围。

---

### Task 1: 锁定 APK 1138 请求/响应字段

**Files:**
- Modify: `implementation_staging/consignment_protocol.py`
- Test: `implementation_staging/tests/test_consignment_protocol.py`

**Interfaces:**
- Produces: `parse_consignment_request(fields) -> ConsignmentRequest`
- Produces: `consignment_browse_frame(listings, registry) -> bytes`
- Produces: `consignment_my_listings_frame(listings, registry) -> bytes`
- Produces: 成功/失败 ACK 编码函数供 `server.py` 使用。

- [ ] **Step 1:** 从 APK 静态证据核对 `main/e.al(...)` 对 action 2/4/7/9/13 的字段读取顺序，以及 `e/au`、`e/p`、`e/t` 的发送字段。
- [ ] **Step 2:** 在 `tests/test_consignment_protocol.py` 写失败测试，固定 C→S 请求解析：action 9 上架、action 13 分类查询、action 7 我的寄售、action 2 下架、action 4 购买、object_type=3 拒绝。
- [ ] **Step 3:** 运行 `python -m unittest tests.test_consignment_protocol`，确认因缺少解析/编码函数失败。
- [ ] **Step 4:** 在 `consignment_protocol.py` 实现最小解析和 S→C 编码，只使用 APK 已确认字段。
- [ ] **Step 5:** 再运行协议测试并提交 `feat: encode native consignment records`。

### Task 2: 建立 ConsignmentService 持久化和真实托管

**Files:**
- Create: `implementation_staging/consignment_service.py`
- Test: `implementation_staging/tests/test_consignment_service.py`

**Interfaces:**
- Consumes: `ItemRegistry.resolve(item)`、角色 `items`、`currencies['silver']`。
- Produces: `ConsignmentService.list_item(...)`
- Produces: `ConsignmentService.search(...)`
- Produces: `ConsignmentService.my_listings(...)`
- Produces: `ConsignmentService.unlist(...)`
- Produces: `ConsignmentService.buy(...)`
- Produces: `ConsignmentResult(changed, reason, listing, item)`。

- [ ] **Step 1:** 写失败测试：整件上架从背包移出；listing 保存真实 item 快照；重载 service 后记录仍存在。
- [ ] **Step 2:** 运行 `python -m unittest tests.test_consignment_service`，确认缺少模块失败。
- [ ] **Step 3:** 实现 `ConsignmentListing`、`ConsignmentResult`、JSON 原子写入和 active 查询。
- [ ] **Step 4:** 写失败测试：部分堆叠拆实例且 ID 不与所有角色/寄售实例冲突。
- [ ] **Step 5:** 实现全量扫描式 `next_instance_id()` 与部分堆叠托管。
- [ ] **Step 6:** 写失败测试：下架保留同一实例 ID；背包满失败且 listing 保持 active。
- [ ] **Step 7:** 实现 `unlist()`。
- [ ] **Step 8:** 写失败测试：购买扣买家银两、加卖家银两、转移同一实例、重复购买和自己买自己被拒绝。
- [ ] **Step 9:** 实现 `buy()`，对角色数据和 listing 使用内存快照，保存异常时恢复。
- [ ] **Step 10:** 运行全部 service 测试并提交 `feat: add transactional consignment service`。

### Task 3: 将物品模板映射到 APK 28 类寄售分类

**Files:**
- Modify: `implementation_staging/consignment_service.py`
- Modify: `implementation_staging/consignment_protocol.py`
- Test: `implementation_staging/tests/test_consignment_categories.py`

**Interfaces:**
- Produces: `consignment_category_id(item, registry) -> int`
- `category_id=0` 表示所有武器聚合；其它分类按装备槽/物品种类和已确认模板元数据映射。

- [ ] **Step 1:** 写失败测试覆盖武器、头盔、肩甲、铠甲、腰带、腿甲、项链、披风、护腕、鞋子、戒指、坐骑、外套、道具、材料。
- [ ] **Step 2:** 实现基于 registry 元数据的分类，不按名称字符串匹配。
- [ ] **Step 3:** 验证 `search(category_id)` 只返回 active 且分类匹配的真实 listing。
- [ ] **Step 4:** 运行分类和 service 测试并提交 `feat: classify consignment items`。

### Task 4: 接入 server.py 的 1138 完整分发

**Files:**
- Modify: `implementation_staging/server.py`
- Modify: `implementation_staging/settings.json` 或 `Settings` 默认值（仅增加寄售数据路径）
- Test: `implementation_staging/tests/test_consignment_server.py`

**Interfaces:**
- Consumes: Task 1 的请求解析/响应编码。
- Consumes: Task 2 的 `ConsignmentService`。
- Produces: 赵公明页面内可完成 action 9/13/7/2/4 的真实服务器行为。

- [ ] **Step 1:** 写失败测试，构造 1138 action 9 请求，断言真实背包实例变为寄售托管并返回原生 ACK。
- [ ] **Step 2:** 在服务器初始化时创建一个共享 `ConsignmentService`，数据文件默认为 `data/consignment_listings.json`。
- [ ] **Step 3:** 将现有只处理 action 3/13 空结果的 1138 分支替换为完整分发。
- [ ] **Step 4:** action 13 返回真实分类 listing；action 7 返回当前角色 active listing；action 2 下架；action 4 购买；action 9 上架。
- [ ] **Step 5:** 成功交易后按现有协议刷新 1008 物品和 1006/1017 银两；失败则发送客户端可安全结束等待状态的原生 1138 回包/顶部提示。
- [ ] **Step 6:** 运行 `python -m unittest tests.test_consignment_entry tests.test_consignment_categories tests.test_consignment_protocol tests.test_consignment_service tests.test_consignment_server`。
- [ ] **Step 7:** 提交 `feat: integrate native consignment market`。

### Task 5: 完整验证与兼容性检查

**Files:**
- Test only; production file only when verification exposes a defect.

**Interfaces:**
- Verifies: 赵公明 → screen 613 → 分类 → listing → 我的寄售/下架/购买全链路。

- [ ] **Step 1:** `python -m py_compile consignment_protocol.py consignment_service.py server.py server_dynamic_maps.py`。
- [ ] **Step 2:** 运行寄售专项测试与物品/商店/坐骑相关回归测试，确认新托管逻辑没有破坏背包、装备和坐骑实例。
- [ ] **Step 3:** 检查 `data/consignment_listings.json` 为空文件/不存在时均可启动，损坏 JSON 只记录错误而不静默覆盖有效角色数据。
- [ ] **Step 4:** 检查宠物 object_type=3 明确拒绝且不修改任何 pet/role 数据。
- [ ] **Step 5:** 记录最终 feature branch commit，并等待真机验证原生页面交互。
