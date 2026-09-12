# 寄售完整流程实施计划

## 目标

在当前 `master` 已能打开 APK 原生 screen 613 并显示 28 个物品分类的基础上，一次性完成真实物品寄售闭环：

`赵公明 -> 购买物品 -> 分类 -> 市场列表 -> 购买 -> 我的寄售 -> 上架 -> 下架`

仅实现物品寄售；宠物寄售继续明确返回未开放。

## 已确认 APK 协议事实

- `1138` 为寄售双向协议。
- `main/e.al(w)` 按 action 路由原生页面：
  - action 1 / 12 / 16 -> screen 73
  - action 3 / 22 -> screen 613
  - action 7 / 9 / 14 / 15 -> screen 70
  - action 13 -> screen 44
- 当前 `master` 已使用 screen 613 item mode `2809`，并在打开时下发 action 3 的 28 个原生分类。
- 当前 `master` 对 action 13 仍返回空结果，且未实现 2/4/7/9 等业务动作，因此分类之后无法形成完整页面链。

## 实施步骤

### 1. 协议层先行（TDD）

在 `tests/test_consignment_protocol.py` 先写失败测试，锁定：

- C->S action 3 分类刷新
- C->S action 13 分类选择
- C->S action 7 我的寄售
- C->S action 9 上架
- C->S action 2 下架
- C->S action 4 购买
- screen 44 需要的 action 13 分类统计帧
- screen 73 使用的 action 1 市场记录帧
- screen 70 使用的 action 7/9 我的寄售记录帧
- action 15/16 删除页面记录帧

字段类型必须保持 BYTE / INT / STRING 的精确类型，不做宽松数字兼容。

### 2. 真实物品寄售服务（TDD）

新增 `consignment_service.py` 与 `tests/test_consignment_service.py`：

- 整件上架：同一物品实例进入 `consignment` 托管，不复制。
- 堆叠部分上架：原堆叠扣减，并分配全局唯一实例给托管部分。
- 持久化至 `data/consignment_listings.json`。
- 重启后 active listing 可恢复。
- 分类查询只返回 active listing。
- 我的寄售仅返回本人 active listing。
- 下架恢复同一实例 ID；背包满时拒绝且 listing 保持 active。
- 购买把同一实例从卖家托管转给买家。
- 买家扣银两、卖家加银两；不足、背包满、自购、重复购买全部拒绝且不改变状态。
- 任意保存异常回滚内存状态。
- 宠物不进入业务模型。

### 3. 服务端协议编排（TDD）

新增 `tests/test_consignment_server_flow.py`，覆盖完整状态机：

1. action 13 -> 下发 screen 44 所需统计
2. 客户端随后 action 0/23 -> 下发 action 1 市场记录
3. action 7 -> 本人寄售列表
4. action 9 -> 上架并同步背包 + 原生寄售页面
5. action 2 -> 下架并同步背包 + 删除寄售行
6. action 4 -> 购买并同步市场行、背包、银两

所有请求中的 role id 均与当前登录角色再次校验。

### 4. 数据与 UI 同步

- 沿用现有角色 `currencies.silver` 与 property 50 刷新，不新增第二套余额。
- 沿用现有 `1009`/物品帧同步背包增删改。
- 上架、下架、购买后同时更新寄售页和背包，避免客户端页面显示旧行。

### 5. 验证

先在功能分支跑：

```bash
python -m py_compile consignment_protocol.py consignment_service.py server.py server_dynamic_maps.py
python -m unittest tests.test_consignment_protocol tests.test_consignment_service tests.test_consignment_server_flow tests.test_consignment_entry tests.test_consignment_categories -v
python -m unittest discover -s tests -v
```

网络协议有变化后再启动测试服并运行 `test_client.py` 的寄售链路回归。所有验证通过后删除临时 CI，再合并到 `master`。

## 真机验收

代码与自动化验证全部完成后，只进行一次完整真机验收：

`赵公明 -> 分类可点击 -> 市场列表 -> 上架 -> 我的寄售 -> 下架 -> 再上架 -> 另一角色购买 -> 双方银两/背包正确 -> 重启服务后持久化正确`。
