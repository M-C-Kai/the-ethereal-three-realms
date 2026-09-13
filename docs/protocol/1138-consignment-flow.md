# 1138 寄售原生页面链

以下路由自 APK（`piaomiao_local_login.apk`）`pmsj/work/main/e.smali` 的 `al(w)` 接收器逐行确认（2026-09-13 apktool 全量反编译复核）：

- action 1 / 12 / 16 -> screen 73 (`0x49`)，市场列表
- action 3 / 22 -> screen 613 (`0x265`)，分类选择
- action 7 / 9 / 14 / 15 -> screen 70 (`0x46`)，"已寄售物品"（我的寄售）
- action 13 -> screen 44 (`0x2c`) 后紧接 screen 70，分类计数

因此 action 13 不能只返回 `[13, 0]` 这种通用空计数；screen 44 使用 count/filter vector，随后客户端再通过 action 0/23 请求市场行，服务端以 action 1 返回市场记录。

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

## 角色 id 校验（真机兼容）

寄售请求（action 7/9/2/4）携带的角色 id 来自客户端 `pmsj/work/b/m.h()`（字段
`b/m.ad`，默认 0）。本客户端构建中该值**恒为 0**：1014 出现流明确跳过自己的
actor，地图入场帧（1010 action 13/14/105）也不回填此字段，唯一写入点是
`1010` 开屏 action 63（服务端未使用）。因此服务端把每个请求绑定到**会话当前
角色**，客户端携带的 id 只作提示性校验：`> 0 且不匹配会话角色` 时才拒绝
（例如切换角色后残留的旧页面）。切勿恢复"必须精确匹配"的旧校验，否则真机
全部寄售/购买操作都会报"寄售角色信息已失效"。

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
