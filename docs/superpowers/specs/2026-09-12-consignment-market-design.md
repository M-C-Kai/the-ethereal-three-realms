# 物品寄售市场设计

## 目标

在现有 APK 原生 `1138` 寄售协议与赵公明 `screen 613` 入口基础上，实现可持久化、可真实交易的物品寄售市场。仅实现物品寄售；宠物寄售暂不实现，也不伪造数据。

## 范围

实现以下原生寄售动作：

- `1138/action=9`：上架物品
- `1138/action=13`：按分类浏览真实寄售记录
- `1138/action=7`：查看自己的寄售记录
- `1138/action=2`：下架自己的寄售记录
- `1138/action=4`：购买寄售记录

现有 `1138/action=3` 28 个原生物品分类继续保留。

不实现：宠物寄售、摆摊 `1731`、拍卖、竞价、跨服市场、邮件取回。

## 核心原则

1. **真实物品实例交易**：寄售对象必须是角色背包中的真实 `ItemInstance`，按 `instance_id` 操作，不按模板复制物品。
2. **实例唯一性**：整件上架后，该实例从角色背包移出；购买时同一实例转移到买家，不创建替代副本。
3. **部分堆叠拆分**：可堆叠物品部分上架时，原堆叠扣减数量，并创建一个新的独立实例作为寄售实例；该新实例只存在于寄售托管中。
4. **服务端权威**：价格、数量、所有权、银两、背包容量、交易状态均由服务端再次校验，不信任客户端。
5. **事务一致性优先**：任何一步失败都不得出现重复物品、丢物、负银两或 listing 已售但物品未转移的状态。
6. **宠物明确排除**：`object_type=3` 请求暂时返回不支持，不进入宠物数据模型。

## 数据模型

新增 `implementation_staging/data/consignment_listings.json`。

每条记录包含：

```json
{
  "listing_id": 1,
  "seller_role_id": 10001,
  "item_instance_id": 1000117,
  "template_id": 170901002,
  "quantity": 1,
  "unit_price": 5000,
  "category_id": 24,
  "status": "active",
  "created_at": 0,
  "expires_at": 0,
  "buyer_role_id": null,
  "sold_at": null
}
```

状态只使用：

- `active`
- `sold`
- `cancelled`
- `expired`

第一版先记录 `expires_at`，但不过期自动处理；在协议字段完全确认后再启用过期机制。

## 模块边界

新增 `implementation_staging/consignment_service.py`，职责仅限寄售业务与持久化。

主要接口：

```python
class ConsignmentService:
    def list_item(self, seller, instance_id: int, quantity: int, unit_price: int) -> ConsignmentResult: ...
    def search(self, category_id: int) -> list[ConsignmentListing]: ...
    def my_listings(self, role_id: int) -> list[ConsignmentListing]: ...
    def unlist(self, seller, listing_id: int) -> ConsignmentResult: ...
    def buy(self, buyer, listing_id: int, role_store) -> ConsignmentResult: ...
```

`consignment_protocol.py` 只负责 APK `1138` 的字段解析和编码，不负责修改业务状态。

`server.py` 只负责分发：解析请求 → 调用 `ConsignmentService` → 下发对应 APK 帧。

## 上架流程

客户端 `1138/action=9` 请求到达后：

1. 必须是 `object_type=1`。
2. 找到当前角色背包中的 `instance_id`。
3. 拒绝已装备、非背包、绑定、任务物品、禁止交易物品。
4. 校验 `1 <= quantity <= item.quantity`。
5. 校验 `unit_price > 0`。
6. 根据物品模板计算原生寄售分类 `category_id`。
7. 若整件上架：从角色 `items` 移除该实例，并由 listing 托管原实例。
8. 若部分上架：原实例扣减数量，分配新的全局唯一 `instance_id` 给寄售拆分实例。
9. 创建 `active` listing。
10. 同步保存角色数据和寄售数据。

## 分类查询

客户端发送 `1138 [13, category_id]`。

服务端只返回 `active` listing。

分类 `0=所有武器` 以及其它 APK 原生分类的匹配规则必须由当前物品模板分类推导，不能靠 listing 名称字符串匹配。

响应记录必须严格按 APK `main/e.al(...)` 对 action 13 的读取顺序编码；实现前先反编译确认字段类型和索引。

## 我的寄售

客户端发送 `1138/action=7`。

仅返回当前角色的 `active` listing；必要时根据 APK 原生行为可同时显示历史状态，但第一版保持 active-only，避免客户端允许对已完成记录执行下架。

## 下架流程

客户端发送 `1138/action=2`。

1. listing 必须存在且为 `active`。
2. `seller_role_id` 必须等于当前角色。
3. 检查背包容量。
4. 将寄售托管实例放回卖家背包，保留同一 `item_instance_id`。
5. listing 标记 `cancelled`。
6. 同步保存角色数据和寄售数据。

背包满时拒绝下架，不丢物，不改变 listing 状态。

## 购买流程

客户端发送 `1138/action=4`。

1. listing 必须仍为 `active`。
2. 买家不能是卖家。
3. 校验买家银两 >= `unit_price * quantity`。
4. 校验买家背包容量。
5. 从卖家/寄售托管中确认实例仍唯一存在。
6. 扣除买家银两。
7. 增加卖家银两。
8. 将同一个寄售实例转移至买家背包。
9. listing 标记 `sold`，记录 `buyer_role_id` 与 `sold_at`。
10. 一次事务性保存角色与寄售数据。

任一步失败时恢复事务前快照。

## 银两

沿用现有角色数据中的银两字段与现有货币刷新协议，不引入第二套余额字段。

购买成功后买卖双方都必须持久化；在线买家立即刷新银两。卖家若不在线，仅持久化余额，下一次上线读取最新值。

## 实例 ID

寄售市场不得通过 `role_id * 100 + 常量` 这种局部规则生成拆分实例 ID。

新增统一实例 ID 分配逻辑，保证：

- 所有角色背包实例不冲突
- 装备实例不冲突
- 寄售托管实例不冲突
- 服务重启后继续单调分配或通过全量扫描得到安全下一个值

## 事务与崩溃一致性

第一版使用内存快照 + 双文件顺序保存：

- 操作前深拷贝受影响角色和 listing 状态
- 业务校验全部通过后再变更
- 任意保存异常时恢复内存快照并抛出错误

不承诺跨两个 JSON 文件的真正 ACID；但代码结构必须集中在 `ConsignmentService`，为后续迁移 SQLite 保留边界。

## 协议要求

实现前必须继续反编译确认以下 S→C 结构：

- action 13：分类查询结果记录
- action 7：我的寄售记录
- action 4：购买成功/失败回包
- action 2：下架成功/失败回包
- action 9：上架成功/失败回包

禁止用猜测字段填充让页面“看起来能显示”。

## 测试要求

至少覆盖：

- 上架整件后背包不存在该实例
- 部分堆叠上架后数量正确，寄售实例 ID 唯一
- 分类查询能看到真实 listing
- 我的寄售只能看到自己的 active listing
- 下架恢复同一实例 ID
- 背包满时下架失败且 listing 仍 active
- 购买转移同一实例 ID
- 买家银两减少、卖家银两增加
- 买家银两不足时无状态变化
- 买家背包满时无状态变化
- 自己购买自己的 listing 被拒绝
- 重复购买同一 listing 只有第一次成功
- 服务重启后 active listing 仍可读取
- 宠物 `object_type=3` 明确返回不支持

## 验收标准

真机上：赵公明 → 寄售 → 分类 → 真实寄售列表 → 购买/我的寄售/下架均使用 APK 原生页面完成，并且服务重启后寄售记录不消失。整个流程中不存在复制物品、丢失物品或银两不同步。