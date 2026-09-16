# 1138 寄售原生页面链

以下路由自 APK（`piaomiao_local_login.apk`）`pmsj/work/main/e.smali` 的 `al(w)` 接收器逐行确认（2026-09-13 apktool 全量反编译复核）：

- action 1 / 12 / 16 -> screen 73 (`0x49`)，市场列表
- action 3 / 22 -> screen 613 (`0x265`)，分类选择
- action 7 / 9 / 14 / 15 -> screen 70 (`0x46`)，"已寄售物品"（我的寄售）
- action 13 -> screen 44 (`0x2c`) 后紧接 screen 70，分类计数

action 3 的 S→C 分类帧布局为
`[BYTE 3, BYTE count, (INT category_id, STRING label, INT branch_flag) * count]`。
`ev.a(w)` 按固定宽度切分记录，`cd.C()/cd.a()` 分别读取第 0/1 字段；
`ev.b(...)` 读取第 2 字段为 `INT`，值 `1` 时打开 screen 44 并发送 action 13。
装备分类使用该分支；“道具”和“材料”的分支值为 `0`，由 `ev.b(...)` 直接打开
screen 73，避免进入只适用于装备的品阶筛选页。screen 73 的原生列表请求为
`[BYTE action, INT client_hint, INT filter, SHORT page, BYTE page_size]`；`filter`
以 `category_id * 10 + subfilter` 编码，服务端以整除 `10` 还原分类。

因此 action 13 不能只返回 `[13, 0]` 这种通用空计数；screen 44 使用 count/filter vector，随后客户端再通过 action 0/23 请求市场行，服务端以 action 1 返回市场记录。

市场行固定 8 字段、我的寄售行固定 7 字段。APK `pmsj/work/e/p.smali` 与
`pmsj/work/e/t.smali` 都以第 2 字段的模板 ID 调用客户端物品资料库，并把第 5/6
字段分别作为显示名称与图标编号 `icon_code`；第 7 字段才是市场行卖家名。
第 6 字段不是品质：完整反编译 `pmsj/work/a/k.a(IIII)` 将该参数乘 10，
再与 `b/j.j(template_id)` 得到的模板末位品质组合成 `#(0,icon_code*10+quality)`。
背包 `b/j.q()` 使用完全相同的调用，其 `q:S` 来自 1008 第 12 字段（图标编号）。
证据等级 B；服务端必须通过统一 `ItemRegistry` 解析名称和图标编号，不能填入
卖家角色 ID 或品质。2026-09-15 修正先前“视觉品质参数”的错误结论。
回归覆盖 1138/action 1、action 9 图标字段；真机状态：pending real-device verification。

## 寄售途径（screen 70 的原生上架入口）

screen 70 是原生的寄售操作中枢，界面自带两个按钮（smali 证据 `pmsj/work/e/t.smali`，控件 id `0x11171`/`0x11176`）：

- **添加物品**：打开背包选择界面（`pmsj.work.e.au`，per-item 菜单 `[寄售, 查看, 丢弃]`），
  选择"寄售"后输入售价（可堆叠物品先输数量再输售价），客户端发送
  `1138 [9, INT instance_id, BYTE object_type, INT role_id, BYTE quantity, INT unit_price]`。
- **添加宠物**：打开宠物选择界面（`pmsj.work.e.cn`，菜单 `[寄售, 查看]`），同样提交 action 9
  （object_type=3；服务端仍明确返回未开放）。

screen 70 创建时（`c()`）自动发送 `1138 [7, role_id]` 请求自己的挂单，因此服务端只需用
`1010` 开屏帧（`consignment_my_screen_frame()`，mode 0）打开 screen 70，随后正常应答
action 7 即可；上架成功的 action 9 应答会再次路由回 screen 70 刷新列表。

## 寄售商人对话（赵公明，service=consignment_merchant）

2032 对话现有五个功能选项（`systems/consignment/handler.py`）：

| 选项 | 文本 | 行为 |
| ---- | ---- | ---- |
| 1 | 寄售商场 | `1010` 开屏 613（mode 2809）+ 1138 action 3 分类帧 |
| 2 | 我的寄售 | `1010` 开屏 70（mode 0），原生寄售途径 |
| 3 | 仙晶交易所 | exchange 系统认领，`1010` 开屏 350（见 1083 文档） |
| 4 | 寄售仙晶 | exchange 系统认领，`1010` 开屏 351（mode 1 卖出仙晶下单页） |
| 5 | 求购仙晶 | exchange 系统认领，`1010` 开屏 351（mode 0 买入仙晶下单页） |

## 请求身份绑定（真机兼容）

寄售请求（action 7/9/2/4）的该 `INT` 字段来自客户端 `pmsj/work/b/m.h()`。
2026-09-15 真机日志确认：角色 `10084` 点击寄售商人 `1900004` 后，screen 70 发送
`1138 [7, INT 1900004]`，因此该值不能视为可靠的当前角色 ID，也不得用于查找或切换角色。
服务端将所有寄售请求只绑定到已认证连接的**会话当前角色**，并忽略该客户端提示值。
这不会放宽跨角色权限：资产操作仍始终针对 `context.active_role`。

## C->S 发送点（已逐行确认）

| 请求 | 触发界面 | 说明 |
| ---- | -------- | ---- |
| `[3]` (BYTE) | screen 613 | 事件 0xaf9 分类刷新 |
| `[13, BYTE category]` | screen 613/44 | 分类浏览 |
| `[0/23]` (BYTE) | screen 44 | 市场行请求 |
| `[7, INT role_id]` | screen 70 创建 | 我的寄售 |
| `[9, INT id, BYTE type, INT role_id, BYTE qty, INT price]` | screen 70 背包/宠物选择 | 上架 |
| `[2, INT id, BYTE type, INT role_id]` | screen 70 行菜单"下架" | 下架 |
| `[4, INT id, INT role_id]` | screen 73 | 购买 |

后续若需要，可继续从全量反编译目录补齐 action 14/22 的字段级证据。
