# 统一交易系统 APK 协议复核门

日期：2026-09-13  
适用主 Spec：`docs/superpowers/specs/2026-09-13-unified-trade-system-design.md`

## 1. 地位

本文件是统一交易系统设计的强制补充规范。任何 `systems/trade/` 业务代码迁移、重命名、路由接管、统一账本接入之前，必须先完成本协议复核门。

如果本文件与已有服务端实现、旧文档或旧测试存在冲突，以本次直接从原始 APK 复核得到的证据为协议事实来源；先修正协议认知和测试，再进行架构重构。

## 2. 复核对象

必须直接针对原始 `piaomiao_local_login.apk` 或由该 APK 生成的完整 apktool/smali 反编译目录复核以下三套交易协议：

- `1138`：物品寄售；
- `1083`：仙晶交易所；
- `1056`：玩家面对面交易。

不得只依据当前 Python 实现反推协议，也不得因为现有测试通过就视为协议已确认。

## 3. 每套协议必须同时查 C→S 与 S→C

每一个已使用 action 都必须锁定以下信息：

1. 消息号；
2. action 值；
3. 发送方向（C→S / S→C）；
4. 发送端 smali 类、方法和关键调用位置；
5. 接收端 smali 类、方法和 switch 分支；
6. 精确字段数量；
7. 每个字段的类型（BYTE / SHORT / INT / STRING 等）；
8. 每个字段的下标与业务含义；
9. 对应 screen/page 路由；
10. 客户端是否把某字段再次原样回发；
11. 空列表、0 值、分页、关闭窗口等边界帧；
12. 当前 Python detector/builder 是否与 APK 完全一致。

只找到接收端而没找到发送端时，必须标记为“单向证据”，不能写成“双向已确认”。

## 4. 1138 必查范围

至少复核当前使用的：

- action 3：分类请求/返回；
- action 13：分类筛选/数量向量；
- action 0、23：市场列表请求；
- action 1：市场列表返回；
- action 7：我的寄售；
- action 9：物品上架；
- action 2：下架请求；
- action 15：我的寄售行移除；
- action 4：购买请求；
- action 16：市场行移除；
- screen 613、70、44、73 之间的真实路由关系；
- object type 中物品/宠物值的来源；
- 客户端角色 id 为 0 的真实来源与使用方式。

特别检查旧实现中“8 字段市场行”“7 字段我的寄售行”的每个字段读取方法，不能只验证字段数量。

## 5. 1083 必查范围

至少复核：

- screen 350、351；
- action 0、3、4、5、6；
- action 10、11、12、13、15、16；
- tab/mode 的 0/1 语义；
- order_id、数量、单价、成交总额的真实字段位置和类型；
- 求购单与出售单的应单方向；
- 撤单/应单后客户端怎样移除或刷新列表；
- 委托费用只是显示字段还是参与客户端计算。

## 6. 1056 必查范围

至少复核：

- action 1：发起交易；
- action 2：接受；
- action 3：拒绝；
- action 4：关闭/取消；
- action 5：打开窗口；
- action 6：对方银两；
- action 8：对方物品；
- action 10：启用确认/最终确认的双向语义；
- action 11、12：关闭相关页面；
- action 20：锁定/完成在 C→S 与 S→C 两个方向上的实际语义；
- 物品行六个字段的精确读取类型；
- actor id 与 role id 的换算来源；
- 锁定后能否改变报价、重复确认、断线后的客户端行为。

1056 当前代码存在同一个 action 在两个方向承担不同含义的情况，因此必须按方向分开建表，禁止用一个笼统 action 描述覆盖两边。

## 7. 强制产物

复核必须新增并提交：

`docs/protocol/trade-apk-protocol-matrix.md`

矩阵每行至少包含：

```text
message_id | direction | action | exact field types | field meanings | sender evidence | receiver evidence | screen | confidence
```

`confidence` 只能是：

- `confirmed-bidirectional`：发送端和接收端都已找到；
- `confirmed-receiver`：只锁定接收端；
- `confirmed-sender`：只锁定发送端；
- `unresolved`：仍缺关键证据。

同时新增自动化协议契约测试，把矩阵中 `confirmed-bidirectional` 的字段类型与当前 Python builder/detector 固化下来。

## 8. Gate 通过条件

只有同时满足以下条件，才能开始统一交易代码重构：

1. 1138、1083、1056 当前服务端实际使用的全部 action 均进入矩阵；
2. 每个 action 的方向被明确区分；
3. 所有客户端固定下标读取字段都有精确类型证据；
4. 页面/screen 路由有接收分发证据；
5. 当前 Python 实现与 APK 不一致的地方已经列出；
6. 不一致项先通过 RED 测试暴露并修正；
7. 协议契约测试全部通过；
8. 仍为 `unresolved` 且会影响资产结算的字段为 0 个。

若只剩不影响本次交易重构的展示性字段无法完全锁定，可以继续，但必须在矩阵中保留 `unresolved`，不得伪装成已确认。

## 9. 重构期间的协议保护

协议门通过后，`systems/consignment` → `systems/trade/item`、`systems/exchange` → `systems/trade/crystal`、`social` 1056 → `systems/trade/player` 的迁移必须满足：

- wire builder 输出字节级行为不变；
- detector 的字段类型条件不放宽；
- screen/open frame 不变；
- 协议契约测试在每个迁移 Task 后都运行；
- 架构命名可以改变，APK 协议常量和值不能为了“统一风格”而重编号。

本协议门的目的不是重新设计交易协议，而是在重构前确保“我们正在保持兼容的协议”确实来自 APK，而不是来自旧服务端自己的假设。
