# 1083 仙晶交易所（玩家求购单 / 出售单）

协议 1083 是 APK 原生的仙晶↔银两玩家交易系统。2026-09-13 通过 apktool 全量反编译
`piaomiao_local_login.apk` 逐行确认：发送点在 `pmsj/work/e/ac.smali`（下单界面）与
`pmsj/work/e/ad.smali`（行情界面），接收分发在 `pmsj/work/main/e.smali` 的 `p(w)`。

## 界面路由（S->C action -> 屏幕）

| action | 屏幕 | 类 | 说明 |
| ------ | ---- | -- | ---- |
| 0 / 3 / 4 / 5 / 6 | 350 (`0x15e`) | `pmsj.work.e.ad` | 仙晶订单行情 |
| 10 .. 17 | 351 (`0x15f`) | `pmsj.work.e.ac` | 下单界面（买入/卖出仙晶） |

`1010` 开屏帧 `1010 [INT 0, SHORT 0, SHORT 0, INT mode, INT screen, SHORT 69]` 可直接打开
350/351；`mode` 会传给 `y(I)`，screen 350 用它作为初始页签（0=求购单，1=出售单）。

## 页签语义

- **玩家求购单**（tab 0）：发布者想用银两买入仙晶。应单者出售自己的仙晶换取发布者托管的银两。
- **玩家出售单**（tab 1）：发布者想卖出仙晶换取银两。应单者用银两买入发布者托管的仙晶。

原生帮助文本（`e/ad.smali`）：买入需支付的仙晶/银两直接从购买者资产扣除；卖出所得通过邮件
发放。本地实现改为直接入账（角色库即时加款，在线玩家推 1017 货币同步，离线玩家下次上线
读取最新值），不引入邮件系统。

## C->S 请求（字段 0 均为 BYTE action）

| 请求 | 触发点 | 说明 |
| ---- | ------ | ---- |
| `[4, B tab]` | screen 350 `y(I)` | 页签标题 + 帮助文本 |
| `[5, B tab]` | screen 350 `y(I)` | 当前页签的列标题向量 |
| `[0, B page, B size, B tab]` | screen 350 `y(I)` / 翻页 | 行情行 |
| `[3, I order_id]` | screen 350 行菜单 出售/购买 确认 | 应单 |
| `[10, B mode]` | screen 351 `y(I)` | mode 0=买入仙晶页 / 1=卖出仙晶页 |
| `[11, B page, B size, B mode]` | screen 351 翻页 | 自己的分页订单 |
| `[12, B mode, I num, I price]` | screen 351 费用按钮 | 委托费用查询 |
| `[15, I num, I price]` | screen 351 "确认提交出售订单？"，确认事件 4 | 挂出售单 |
| `[16, I num, I price]` | screen 351 "确认提交购买订单？"，确认事件 3 | 挂求购单 |
| `[13, I order_id]` | screen 351 行菜单"撤单" | 撤单 |

## S->C 应答格式（客户端按固定下标读取具体类型）

| 应答 | 消费界面 | 字段 |
| ---- | -------- | ---- |
| `[0, S total, B n, B tab, row×n]` | 350 行情 | row = `[I order_id, S 仙晶数量, S 发布者名, S 银两总额]`；确认弹窗按 `出售{f1}个仙晶换取{f3}银两` 拼接 |
| `[4, B n, S×n, S footer]` | 350 页签 | `["玩家求购单","玩家出售单"]` + 帮助文本 |
| `[5, B 4, I tab, S left, S middle, S right]` | 350 | 列标题：页签、仙晶数量、发布者、银两总额 |
| `[6, B tab, I order_id, S total]` | 350 | 应单成功，删除该行 |
| `[10, B n, S×n, S footer]` | 351 | 固定两个页签（下单 / 我的订单）+ 帮助文本，不是订单摘要 |
| `[11, S total, B n, row×n]` | 351 分页 | row = `[I order_id, S 单价, S 数量, S 上单时间]`（渲染顺序 f2=左列, f1=中列, f3=右列） |
| `[12, S fee_text]` | 351 | 委托费用显示 |
| `[13, S total, I order_id]` | 351 | 撤单成功（注意 total 在 id 前） |
| `[15]` / `[16]` | 351 | 下单成功，清空数量/单价输入 |
| `[17, S total, row]` | 351 | 下单成功后单行订单刷新，更新已经缓存的我的订单列表 |

## 服务端实现

- 模块：`systems/exchange/`（`protocol.py` 编解码、`service.py` 订单簿、`handler.py` 编排）。
- 托管：
  - 求购单：发布时扣 `num*price + fee` 银两；撤单退回 `num*price`（费用不退）。
  - 出售单：发布时扣 `num` 仙晶 + `fee` 银两；撤单退回 `num` 仙晶。
- 应单（`[3, id]`）：服务端校验订单 active、非自购、应单者资产充足，一次事务完成双方
  余额/托管转移并落盘；失败整体回滚（快照恢复）。
- 委托费用：`fee = max(1, round(num*price*exchange_fee_rate))`（`config.json` 的
  `exchange_fee_rate`，默认 0.02），发布时以银两收取。
- 持久化：`exchange_data_file`（默认 `data/exchange_orders.json`），记录 `orders`
  （active/filled/cancelled）与 `transactions`（成交流水）。
- 货币同步：资产变动后向操作者发 `1017` property 50（银两）/52（仙晶）；对手方在线时经
  `_push_to_role` 推送同样帧。

## 寄售商人入口

赵公明（`consignment_merchant`）对话的三个仙晶选项由 `ExchangeSystem.npc_dialogue_option`
认领，均返回 `1010` 交互 ack + 对应开屏帧：

| 选项 | 文本 | 开屏帧 |
| ---- | ---- | ------ |
| 3 | 仙晶交易所 | `1010 [0,0,0,0,350,69]` 行情页（客户端随后自动发 `[4]/[5]/[0]` 三连请求） |
| 4 | 寄售仙晶 | `1010 [0,0,0,1,351,69]` 卖出仙晶下单页（mode 1） |
| 5 | 求购仙晶 | `1010 [0,0,0,0,351,69]` 买入仙晶下单页（mode 0） |

screen 351 的 mode 决定提交按钮的语义：mode 0 提交 `[16, num, price]` 求购单，
mode 1 提交 `[15, num, price]` 出售单；打开后客户端自动发送 `[10, mode]` 请求
两个页签。原生界面没有从 350 跳转 351 的按钮，因此下单页必须由服务端对话
选项直接开屏。

## 回归

2026-09-15 应单拒绝结束等待（B 级）：`main/e.p(w)` 将 action 3 分发到
screen 350；`ad.a(w)` packed-switch 的 action 3 指向 `pswitch_0`，执行
`main/t.a(false,false)`，不读取额外字段、不删除订单。失败时先返回
`1083 [BYTE 3]`，再发 1049 中文提示，避免提示消失后仍停留“请稍后”。
测试覆盖自己买/卖订单均拒绝、资产不变、订单仍 active 与应答顺序。
真机状态：pending real-device verification。

2026-09-15 列布局复核（B 级，用户截图一致）：`ac.a(row)` 左/中/右列读取
索引 2/1/3，`ac.i()` 标题为数量/单价/上单时间，故不能写订单类型文字。
`ad.a(w)` action 0 以 BYTE 读取索引 2 为行数、索引 3 为页签；先前两者反置。
action 5 将长度为 n 的整段 TLV 存入 `P`，`C(tab)` 以第 0 个元素匹配页签；
`o()` 把后续元素绘制为列标题。错误“订单 ID”应答导致 `o()->p()` 持续重试。
修正不变更存档、托管或成交语义。时间文本及列标题为本地兼容显示值。
真机状态：pending real-device verification。

2026-09-15 下单动作更正（B 级）：`ac.b(b)` mode 1 的出售确认事件为 4，
`ac.c_(4)` 实际发送 action 15；mode 0 的购买确认事件为 3，`ac.c_(3)` 发送
action 16。先前动作说明反置。真机订单 4（11 仙晶、单价 1）因此被旧实现存为
buy，保留现有托管数据，不自动转换。`ac.d(b)` 在 `ai=true` 后不重复拉取订单；
action 15/16 只清空输入，故成功应答后补发原生 action 17（BYTE/SHORT/四字段行）。
该接收分支按实例 ID 去重并写入 `ag` 缓存，切换页签后即可显示。
真机状态：pending real-device verification。

2026-09-15 action 10 复核（B 级）：`ac.a(w)` 将 STRING 列表写入页签控件
`S:d/k`，随后以 `控件宽度 / 页签数量` 计算宽度，数量为 0 会除零并跳过
`main/t.a(false,false)`，造成“请稍后”不消失。`ac.d(b)` 明确以页签索引 0
显示下单表单、非 0 显示我的订单并触发 action 11。服务端固定返回两个页签；
名称为本地兼容标签，挂单行不能放入 action 10。字段类型仍为 BYTE/BYTE/STRING×3。
自动回归覆盖无挂单两种模式与有挂单初始化；真机状态 pending real-device verification。

- `tests/test_exchange_system.py`：协议字段类型锁定、订单簿托管/撤单/应单/自购拒绝、
  持久化恢复、保存失败回滚、路由注册、对话选项分派。
- `python test_client.py --exercise-consignment-only`：真机协议级端到端（对话 → 我的寄售
  上架/下架 → 仙晶交易所挂单/费用/撤单）。
