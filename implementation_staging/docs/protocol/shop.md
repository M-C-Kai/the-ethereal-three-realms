# 商城协议（仙晶商城 / 仙石商城，APK 逆向确认）

> 本文记录从原 APK 静态逆向确认的商城完整链路。所有字段类型均已通过 smali
> 读取函数（`pmsj/work/main/w`）核实；TLV 类型不可替换。
>
> smali 证据基目录：
> `C:\Users\Kail\Documents\Codex\2026-08-24\new-chat\work\apk-initial-role-reference\smali`

## TLV 读写基元（`pmsj/work/main/w` / `a/c/r`）

| 方法 | TLV 类型 | type_id |
|---|---|---|
| `w.a(I)B` / `r.b(I)` | BYTE | 2 |
| `w.b(I)S` / `r.c(I)` | SHORT | 3 |
| `w.c(I)I`、`w.d(I)I` / `r.d(I)` | INT | 4 |
| `w.e(I)Ljava/lang/String;` | STRING | 6 |

发送入口：`w.a(IBII)V` 等重载按变参写字段；`t.a(ZZ)V` 刷send队列。

## 一、商城入口（screen 611，`pmsj/work/e/bk`）

- 页面标题 `商城`（bk.c()V 本地设置）；两个 Tab：`仙晶商城`/`仙石商城`
  （`bk.smali` `:array_0`：`R = [0x7d0, 0x834]` = [2000, 2100]）。

### C→S 1067 首次进 Tab（`cd.y(I)V`，cache miss）

```text
1067 [BYTE 0, INT 611, INT mode]      # w.a(IBII)V，mode=2000 仙晶 / 2100 仙石
1067 [BYTE 2, INT 611, INT mode]      # 同一时刻还会发送标题请求
```

cache 命中（切换 Tab）时只发送第二条 `[BYTE 2, ...]`。

### S→C 1067 action=0 分类列表（`pmsj/work/e/cd.a(w)` `:pswitch_1`）

| index | 类型 | 说明 | 证据 |
|---|---|---|---|
| 0 | BYTE | action=0 | `w.a(0)B`，`packed-switch` |
| 1 | INT | screen id（必须 611） | 路由 `main/e.u`：`v1 = w.c(1)` → `n.a(611, w, false)`；cd 另用 `field[1]*10000+mode` 作分类缓存键 |
| 2 | (未读) | 占位字段，客户端不读 | cd.a(w) 全分支无 index 2 读取 |
| 3 | BYTE | 分类数量 | `w.a(3)B` |
| 4.. | 记录 × count | 每条记录 = [INT category_id, STRING name] | `recordLen = (w.b.size()-4)/count` 动态切分；`record[0].b()I` 取 id，`record[1].toString()` 取名 |

recordLen 由字段总数反推：本服每条记录恰好 2 个字段（INT+STRING）。

### S→C 1067 action=2 标题（`cd.a(w)` `:pswitch_2`）

```text
1067 [BYTE 2, INT 611, STRING title]
```

客户端只读 field[2] STRING 并调用 `d(String)`（`d/c.W` 标题）。field[1] 不读。

### S→C 1067 action=1

客户端在 `cd.a(w)` 和路由 `main/e.u` 两处都**直接丢弃**（`:pswitch_0` = return）。
服务端无需也不应回复 1067 action=1。

### 分类按钮

按钮 id = `612001(0x956a1) + index`（bk 构造器/`bk.b(Vector)`）。点击时
`C(index)` 取回服务端下发 record[index][0] 的原始 category_id，再发送：

```text
C->S 1067 [BYTE 1, INT 612, INT category_id]     # bk.b(widget) : 0x42b, 0x264
```

## 二、screen 7 跳转桥（本次逆向确认的关键点）

`1067/BYTE 1/INT 612/category_id` 之后，客户端自己**不会**打开 dp；
1067 action=1 的响应也被丢弃。唯一打开 `pmsj/work/e/dp`（screen 7）的机制是
服务端下发通用 1010 open-screen 指令：

```text
S->C 1010

field[0] = INT   0        （未读占位）
field[1] = SHORT 0        （未读占位）
field[2] = SHORT 0        （未读占位）
field[3] = INT   mode     → dp.y(mode)，决定货币与标题
field[4] = INT   7        → screen id，n.f(7) 创建/复用 dp
field[5] = SHORT 0x45(69) → main/e 1010 子命令（open screen）
```

证据（`pmsj/work/main/e.smali` 流式分发 0x3f2 分支，`:sswitch_d`）：

```smali
invoke-virtual {v0, v1}, Lpmsj/work/main/w;->b(I)S   # field[5] SHORT 子命令 → sparse-switch 0x45
invoke-virtual {v0, v1}, Lpmsj/work/main/w;->c(I)I   # field[4] INT screen id
invoke-virtual {v0, v1}, Lpmsj/work/main/w;->c(I)I   # field[3] INT mode
invoke-virtual {v5, v4}, Lpmsj/work/d/n;->f(I)       # n.f(7) get-or-create dp
invoke-virtual {v11, v12}, Lpmsj/work/d/c;->y(I)     # dp.y(mode)
# field[6] STRING 为可选标题（vector.size()>6 且 length>0 才读取），本服不下发
```

全树唯一 `n.f(7)` 创建点；`n.a(7, w, false)`（1067/1033 路由）的 `Z=false`
变体只投递已打开页面，从不创建。screen 7 不在 `:pswitch_data_5` 特例表内。
本服昆仑导师（screen 179）已使用同一 0x45 桥。

dp 收到 `y(mode)` 后自己发送 1033 商品列表请求（见下）。

## 三、dp 模式与货币（`pmsj/work/e/dp`）

`dp.E(I)`（货币类型推导，直接决定 1033 响应 field[6] 校验）：

```text
mode == 0            -> 类型 0（银两）
(mode/1000) % 2 == 1 -> 类型 1（仙晶，property 52）
(mode/1000) % 2 == 0 -> 类型 2（仙石，property 49）
```

`dp.s()`：类型 0 → `ab.f(50)`、类型 1 → `ab.f(52)`、类型 2 → `ab.f(49)`。
`dp.y(mode)`：类型 2 → 标题 `仙石商店`；类型 1 → 标题 `仙晶商店`。

注意 bk 的 Tab mode（2000/2100）与 dp 的 mode 是两个空间：E(2000)=E(2100)=2。
服务端桥接时自行选择 dp mode：仙晶 → 1000（shop_id 1000），仙石 → 2100
（shop_id 2000）。1033 请求到达时 `shop_id = (dp_mode/1000)*1000` 即可区分两个商城。

## 四、1033 商品列表

### C→S（`dp.ap()`）

```text
field[0] = INT   shop_id       # mode==0 时取 b/m.h()；否则 (mode/1000)*1000
field[1] = BYTE  7             # 商品列表 action
field[2] = SHORT page1         # K.c()
field[3] = SHORT page2         # K.d()
field[4] = BYTE  mode % 100    # 2000/2100 均为 0
```

### S→C action=7（`dp.a(w)` `:sswitch_0`，按固定下标读取）

| index | 类型 | 说明 | 证据 |
|---|---|---|---|
| 0 | BYTE | action=7 | `w.a(0)B` sparse-switch |
| 1 | INT | shop_id | `w.d(1)I`，与 `b/m.h()` 不一致时 `m.e()` 覆盖 |
| 2 | INT | 本批商品数 | `w.d(2)I` |
| 3 | INT | 页码（0 起） | `w.d(3)I` |
| 4 | INT | 商品总数 | `w.d(4)I`（在 field[6] 之后读，但下标固定） |
| 5 | (未读) | 占位字段，客户端不读 | 解析器从 index 3 直接跳到 6 |
| 6 | BYTE | 货币类型 | `w.a(6)B`；必须等于本地 `E(mode)`，否则 `ae()` 关页 |

商品记录自 field[7] 起按顺序读取，每条普通商品 7 项：

```text
INT    item_definition_id     → b/a.a(0, id) 客户端本地建物品
INT    price                  → j.i
STRING name                   → j.o
INT    (收窄为 BYTE  j.n)
INT    (收窄为 SHORT j.h)
INT    (收窄为 SHORT j.l)
INT    (收窄为 SHORT j.q)
```

装备商品（客户端 `j.c()==true`）追加 4 个：

```text
SHORT × 4 → b/g.a(BS)V 写入 g.d:[S]（长度 8，下标 0..3）
```

TLV 本身是 INT（`w.d`）+ 4×SHORT（`w.b`）；Java 端的 int-to-byte/short 只是收窄。

所有商品之后读取一个 STRING（`w.e` → `dp.d(String)`，`*` 为颜色标记分隔符，
本服不下发 `*`）作为商店标题。本服一次整页下发：`page=0`、
`count == total == 分类商品数`；客户端本地分页。

## 五、1033 购买

### C→S（`main/e.a(BIIS)`，已完整确认）

```smali
const/16 v1, 0x409
invoke-virtual {v0, v1}, La/c/r;->a(I)V   # messageId 1033
invoke-virtual {v0, p1}, La/c/r;->d(I)V   # INT   shop_id
invoke-virtual {v0, p0}, La/c/r;->b(I)V   # BYTE  1（action）
invoke-virtual {v0, p2}, La/c/r;->d(I)V   # INT   item_id
invoke-virtual {v0, p3}, La/c/r;->c(I)V   # SHORT quantity
```

即 `type_ids == [4, 2, 4, 3]`，服务端纯函数
`is_shop_purchase_request(fields)` 同时校验类型、action=1 和 quantity>0。

### S→C action=1 / action=2（`dp.a(w)` `:sswitch_1/:sswitch_2`）

两个分支都**不再读取任何字段**：

- action 1 → 仅 `ag()`：按 `s()` 重读货币属性并刷新商店货币标签；
- action 2 → `ag()` + 本地重建卖出页（`au.at.ap()`，无网络请求）。

购买成功本服发送顺序：

```text
1017 增量帧（property 49/52 新余额）   → 客户端人物模型货币更新
1008 operation=3（物品实例）           → 新增/堆叠同步
1033 [BYTE 1]                          → 商店货币标签刷新
```

1033 ACK 不是发放物品协议；发放完全复用 1008/1017。

## 六、货币属性对照

| property | 货币 | 客户端商店类型 |
|---:|---|---:|
| 50 | 银两 | 0 |
| 52 | 仙晶 | 1 |
| 49 | 仙石 | 2 |

服务端复用 `role['currencies']['immortal_crystals'|'immortal_stones'|'silver']`
与 `CURRENCY_PROPERTIES`，不新增角色字段。

## 七、服务端实现

| 内容 | 位置 |
|---|---|
| 商城资料层 | `shop_registry.py` + `data/catalog/shops.json` |
| 1067/1033 协议构造与纯函数校验 | `server.py`（`mall_*_frame` / `shop_*_frame` / `is_*_request`） |
| 1067/1033 handler | `server.py` `LocalGameServer.handle()` 分发链 |
| 购买原子业务 | `shop_purchase_result()`（服务端价格/库存/货币/背包全部重验） |
| 连接级商城状态 | `current_shop_mode` / `current_shop_category`（不入角色 JSON） |
| 日志 | `SHOP_OPEN` / `SHOP_CATEGORY` / `SHOP_LIST` / `SHOP_PURCHASE_REQUEST` / `SHOP_PURCHASE_SUCCESS` / `SHOP_PURCHASE_REJECT` |

资料层约束：商城只能出售 `item_registry` 中真实存在的 template_id
（加载期校验），购买创建的是最小背包实例 `{id, template_id, quantity,
location}`，走现有实例 id 分配、堆叠与背包容量规则。

## 八、验证

```powershell
D:\python\python.exe -m unittest discover -s tests -v     # 258 项（含 41 项商城）
D:\python\python.exe test_client.py --host 127.0.0.1 --port 6805 --exercise-shop-only
D:\python\python.exe test_client.py --host 127.0.0.1 --port 6805 --exercise-role-crud
```
