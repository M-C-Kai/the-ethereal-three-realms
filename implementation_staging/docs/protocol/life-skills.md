# 生活技能协议（1132 / 1143 / 1141 / 2027 / 1145 / 1084，APK 逆向确认）

> smali 证据基目录：
> `C:\Users\Kail\Documents\Codex\2026-08-24\new-chat\work\apk-initial-role-reference\smali`
>
> TLV 类型：BYTE=2 (`w.a(I)B`/`r.b(I)`)，SHORT=3 (`w.b(I)S`/`r.c(I)`)，
> INT=4 (`w.c(I)I`/`w.d(I)I`/`r.d(I)`)，STRING=6 (`w.e(I)`)。
>
> 标注约定：`[APK]` = 静态证据确认；`[compat]` = 本地兼容值（原服数值不可恢复）；
> `unknown` = 客户端不读/语义未确认的占位字段。

## 0. 重大勘误（相对任务书假设）

| 任务书假设 | APK 实际 | 证据 |
|---|---|---|
| 1145 = 采集协议 | **1145(0x479) 是跨图自动寻路**（findRoadOtherMap）。真正采集 = **2027(0x7EB)**，目标目录 = **1141(0x475)**，目标状态 = **1142(0x476)** | `main/e` 路由：0x479→`e.av`（只处理 action 0，写 `ab.i` 寻路点）；0x7eb→`e.az`；0x475→`e.S`；0x476→`e.R` |
| 1132 action0 仅生活技能 | 1132 是**通用技能容器**（门派+生活共用 `b/f.n`），action0 按 `(size-2)/count` 切记录合并入库 | `main/e.E` pswitch_0 |
| 任务书 record 访问号 | 已全部按 accessor 核实（见下文各表） | 各 parser |

## 一、1132（0x46C）技能容器

### 路由（`main/e.E(w)`，action 为 field[0] BYTE）

| action | 行为 |
|---|---|
| 0 | 解析技能记录入 `b/f.n`，刷新 screen 203(du) |
| 1 | 投递 screen 325 (`e/ay` 层级页) |
| 2 | 投递 screen 326 (`e/db` 配方列表) |
| 3 | `y.c(id, level, string)` 更新 `x.A` 信息文本；刷新 203 / 603 |
| 4 | 熟练度记录更新 `b/f.n`；刷新 203、329(az)、328(dc)、603(ax) |
| 5 | 配方桩（fields[1..2]）入 `b/f.p`；刷新 326/328 |
| 6 | 投递 screen 329 (`e/az` 升级页，flag=false 只复用已开页) |

### C→S 请求（均已核实 builder）

| 请求 | wire | builder 证据 |
|---|---|---|
| 初始化 | `[BYTE 0]` | `du.d`/`dj`/`ei.d`：`w.a(0x46c, 0)` |
| 进入技能(层级页) | `[BYTE 1, INT skill_id]` | `ax.b`/`dv.b`：`w.a(IBI)(0x46c,1,id)` |
| 配方列表 | `[BYTE 2, INT skill_id, BYTE tier, BYTE pa, BYTE pb]` | `db.i()` 手工 r.b/r.d 序列 |
| 技能信息 | `[BYTE 3, INT skill_id, BYTE level]` | `ax.k()`/`dv.e()`：`w.a(IBIB)` |
| 升级确认 | `[BYTE 6, INT skill_id]` | `az.c_(I)`：`w.a(0x46c, 6, az.e)` |

### S→C action 0 技能列表

`[BYTE 0, BYTE count, records...]`，`width=(size-2)/count`，记录按下标懒读取：

| idx | 类型 | 含义 | 证据 |
|---|---|---|---|
| 0 | STRING | 名称 | `x.e()`、`ax.j()` |
| 1 | INT | skill id | 构造键/容器匹配 |
| 2 | INT | 等级 | `x.f()` |
| 3 | INT | 等级上限 | `az`: `rec[3]>rec[2]` 可升级 |
| 4 | INT | 熟练度当前 | `ax` O[i*2]、`dc` |
| 5 | INT | 熟练度上限 | `ax` O[i*2+1]、`dc`（az 上下文中被读作经验成本，见 action 4 说明） |
| 6 | INT | 位标志（bit0=显示熟练度） | `x.a(I)Z`、`dc` `rec[6]&1` |
| 7 | INT | 图标 id | `ax.j()` `b(7)` |
| 8..13 | INT | unknown（客户端不读） | 兼容占位 0 |

本服现有门派记录即 14 字段宽（`character_skill_list`）；生活技能记录同宽 14，
action-0 响应内所有记录必须等宽。

`e/ax`（screen 603）内部固定分配 7 个 `x` 记录槽，并在 `j()` 中无空值检查地
读取全部 7 槽；少于 7 条会在客户端本地构建页面时空指针退出，多于 7 条则会
写越界。因此本服的合并 action-0 列表严格发送 7 条：真实门派/生活技能不足时，
用唯一 skill id、等级 0、标志 0 的“未开放”记录补齐。锁定记录不可点击，也不
参与熟练度、升级或配方业务。

### S→C action 1 层级页（`e/ay`）

`[BYTE 1, INT skill_id, BYTE count, records...]`，`width=(size-3)/count`。
层级栅格标签由 `w.e(i+3)`/`w.a(i+3)` 交错填充；记录 `rec.a(1)I` = 该层配方数。
完整记录 schema 未全部锁定 → 本服发送最小等宽记录并标注 `[compat]`。

### S→C action 2 配方列表（`e/db`）

| idx | 类型 | 含义 |
|---|---|---|
| 0 | BYTE | action=2 |
| 1 | INT | skill_id（页面标题“名称 X级”取自容器记录） |
| 2 | STRING | 列表首行文本（`l.i()`） |
| 3 | STRING | 列表次行文本（`l.g()`） |
| 4 | BYTE | 翻页器状态（`d/i.a`） |
| 5 | BYTE | 记录数 |
| 6.. | 记录 × count，`width=(size-6)/count` | `rec[0]`=INT 配方 id；**rec[1] 不读**（占位）；`rec[2]`=STRING 名称；`rec[3]`=STRING 次行 |

### S→C action 3 信息文本

`y.c(w.d(1), w.d(2), w.e(3))` → `[BYTE 3, INT skill_id, INT level, STRING text]`，
写入 `x.A`（603 信息列表）。本服用于生活技能详情文本。

### S→C action 4 熟练度同步

`[BYTE 4, BYTE count, records...]`，`width=(size-2)/count`，按 field[1] 匹配更新容器：

| idx | 含义 | 消费者 |
|---|---|---|
| 0 | STRING 名称 | az |
| 1 | INT skill id | 匹配键 |
| 2 | INT 等级 | az/dc/ax |
| 3 | INT 等级上限 | az（>level 保持升级页打开） |
| 4 | INT 熟练度当前 | dc/ax |
| 5 | INT 熟练度上限（az 上下文读作经验成本 N —— APK 双重语义） | dc/ax vs az |
| 6 | INT 位标志（bit0=熟练度显示） | dc |
| 7 | INT 图标 | az/ax |
| 8 | INT （az 读作银两成本 M） | az |
| 9 | INT （az 读作需求等级 L） | az |

本服统一发 10 字段（8/9 填 0，升级页成本由 action 6 下发）。

### S→C action 6 升级页（`e/az`，仅 push）

```text
[0] BYTE  6
[1] INT   skill_id        （确认时原样回传）
[2] STRING 技能名
[3] BYTE  当前等级
[4] BYTE  等级上限（f<K 时弹“升级条件”）
[5] BYTE  需求角色等级（L<=property11 才允许升级）
[6] INT   银两成本          → 与 property 50 (ab.j()) 对比
[7] INT   经验成本          → 与 property 31 (ab.l(), Long) 对比
[8] STRING 当前效果
[9] STRING 下一级效果
[10] INT  图标
```

**经验 = property 31（角色当前经验）**，银两 = property 50，角色等级 = property 11。
客户端失败提示（银两不足/经验不足）均在 `az.b(String)`，发送前无等待态解锁问题
（确认后等待由 1132 路由 `e.E`… 任意 1132 响应刷新；本服确认成功回
action 0 列表 + action 4 熟练度；失败回 action 3 信息文本，均为已确认 wire）。

### 生活技能主页面流程（`e/dj` → `e/ax`(603) → `e/ay`(325) → `e/db`(326) → `e/dc`(328)）

1. 角色技能菜单 `dj` 在 `b/f.n==null` 时发 `1132 [BYTE 0]` 并开 603(ax)。
2. ax 点技能 → `1132 [BYTE 1, INT skill_id]` → S→C action1 开 325。
3. 325 选层 → 开 326(db) 并发 `1132 [BYTE 2,...]` → S→C action2 配方列表。
4. db 选配方“使用…” → 开 328(dc) + `1143 [BYTE 4, INT recipe_id]` +
   `1143 [BYTE 6, INT recipe_id]` → S→C action4 详情 + action6 动态文本。
5. dc 制造 → `1143 [BYTE 5, ...]` → S→C `1143 [BYTE 5]`（仅触发背包重扫 `dc.i()`）。

## 二、1143（0x477）导师学习 + 普通制造

### 路由（`main/e.D(w)`）

**第一语句无条件 `t.a(false,false)` 清除“请稍后”**（任意 1143 响应解锁等待）。
action 0–3 → screen 327 (`e/de`)；action 4–6 → screen 328 (`e/dc`)。

### C→S 请求（builder 均已核实）

| 请求 | wire | builder |
|---|---|---|
| 可学列表 | `[BYTE 1, INT trainer_id, BYTE pa, BYTE pb]` | `de.i()`，发送前置等待态 |
| 查看 | `[BYTE 2, INT id]` | `de.b(String)`“查看” |
| 学习确认 | `[BYTE 3, INT id]` | `de.c_(I)`，发送前置等待态 |
| 制造详情 | `[BYTE 4, INT recipe_id]` | `db.b(String)`“使用…” |
| 普通制造 | `[BYTE 5, INT recipe_id, INT slot1..4, BYTE qty]` | `dc.a(I,String)`（qty 1..99 客户端校验，99 上限硬编码） |
| 直接使用 | `[BYTE 5, INT recipe_id, INT 0, INT 0, INT 0, INT 0]` | `db.c_(I)`（无 qty BYTE） |
| 动态文本 | `[BYTE 6, INT recipe_id]` | `dc.C(I)` |

普通制造与直接使用以**字段长度**区分（7 vs 6），四个 slot INT 是
**物品实例 id**（`b/j.e`，槽控件 `d/a.d()I`）。

### S→C action 0 导师页（`e/de`，仅 push）

`[BYTE 0, INT trainer_id, STRING title, BYTE level, STRING text1, STRING text2]`
（全部核实；title 同时用作技能名 O）。收到后 de 立即发 action-1 列表请求。

### S→C action 1 可学列表（`e/de`）

`[BYTE 1, BYTE page, BYTE count, records...]`，`width=(size-3)/count`，
**记录宽 7**（de.X=7）：

| idx | 类型 | 含义 |
|---|---|---|
| 0 | INT | 条目 id |
| 1 | INT | 不读（占位） |
| 2 | INT | 需求角色等级（property 11） |
| 3 | INT | 银两（property 50，客户端“银两不足”） |
| 4 | INT | 经验（property 31，客户端“经验不足”） |
| 5 | STRING | 列表显示文本 |
| 6 | STRING | 详情文本 |
| 7/8 | — | 不读 |

客户端学习预检顺序：银两 → 经验 → 等级（`de.b(String)`），确认框后发 action 3。

### S→C action 2 查看详情（`e/de`）

`[BYTE 2, STRING text]`（text 按 `_` 分页显示）。

### S→C action 3 学习结果（`e/de`）

```text
[0] BYTE  3
[1] BYTE  page
[2] INT   条目 id
[3] INT   result：0 = 行从列表移除（已学完）；非 0 = 行被 fields[3..9] 重建的
          7 字段记录原位替换（例如同技能下一级条目）
```

等待态由路由清除。**本服失败路径**：重发同条目（result=1 + 原 7 字段记录）
—— 仅使用已确认 wire 形状，等待态被路由清除，视觉为无变化。`[compat]` 标注。

### S→C action 4 制造详情（`e/dc`）

| idx | 类型 | 含义（全部核实） |
|---|---|---|
| 0 | BYTE | 4 |
| 1 | INT | 产物 template id（`dc.ad`，拥有数角标 + “查看”回传） |
| 2 | STRING | 制造名称 |
| 3 | INT | 图标 id |
| 4 | STRING | 说明 |
| 5..8 | INT×4 | 材料 **template id**（`dd.c[i]`，<=0 禁用槽位） |
| 9..12 | STRING×4 | 槽位标题 |
| 13..16 | BYTE×4 | 每次制造所需数量（`dd.d[i]`） |

读完后 `dc.i()` 按模板自动从背包填槽。

### S→C action 5 制造回执（`e/dc`）

**`[BYTE 5]`，无任何字段** —— 唯一效果 `dc.i()` 背包重扫。
物品变化由独立 1008 帧送达。失败表现客户端无专属分支（unknown）；
本服失败时另发 `1143 [BYTE 6, STRING reason]` 用已确认的动态文本通道提示
（`[compat]`），并同样发 `[BYTE 5]` 触发重扫。

### S→C action 6 动态文本（`e/dc`）

`[BYTE 6, STRING text]` → 列表控件 0x5014d。

## 三、采集：1141 / 2027 / 1145

### 1141（0x475）采集目标目录（S→C push，`e.S` → `b/p.a`）

**无 action 字节**：`[INT count, records...]`，`width=(size-1)/count`：

| idx | 类型 | 含义 | 证据 |
|---|---|---|---|
| 0 | INT | 目标 id（`cc.c()`：state==0 时自动寻路目标） | cc.i 148 |
| 1 | STRING | 名称 | cc.i 172 |
| 2 | INT | 分类（cc 页签分组） | cc.ag 322 |
| 3 | INT | x | cc.i 190 |
| 4 | INT | y | cc.i 202 |
| 5 | INT | 状态（==0 → 可自动寻路） | cc.c 656 |
| 6 | — | 不读（占位） | — |
| 7 | INT | map_id（0=当前图） | cc.c 637 |
| 8 | INT | 状态字节（显示标记 1..4） | cc.i 225 |

### 2027（0x7EB）采集实体与流程

| 方向 | wire | 说明 |
|---|---|---|
| S→C action 0 | `[BYTE 0, INT id, INT x, INT y, INT model, STRING name, INT 0, INT 0, INT 0, STRING 菜单文本]` | 在 `b/m.t` 生成 `b/i` 实体（type 0x10）。字段按各自下标存入实体；**field 9 = 点击菜单文本**（`k` 采集发起时 `i.j(9)`）。6/7/8 客户端未读，占位 0 `[compat]` |
| C→S | `[BYTE 1, INT entity_id]` | 玩家点击实体菜单后 `main/k` 发起（`w.a(IBI)(0x7eb,1,m.h())`） |
| S→C action 1 | `[BYTE 1, INT duration_seconds, INT target_id]` | `k.a_(II)`：`duration*1000` 毫秒倒计时（`a/c/q`），字段单位为**秒** |
| S→C action 2 | `[BYTE 2]` | `k.s()` 停表清进程 + 提示“采集中断!”；无字段 |
| S→C action 3 | `[BYTE 3, INT target_id]` | 仅当 == 当前 `aL` 时停表并 `m.i(id)` 从地图删除实体；奖励**不**走此帧 |
| S→C action 4 | `[BYTE 4, BYTE count, records...]` | 小地图点（`b/p.b`：rec[1]=x, rec[2]=y, rec[3]=标签）；本服暂不下发 |

采集奖励 = `1008`（物品）+ `1017`（property 55 体力）+ `1132 action 4`（熟练度）
+ `2027 action 3`（目标移除）。发送顺序本服定为：1008 → 1017 → 1132/4 → 2027/3
（先同步背包与人物，再移除目标实体；客户端各 handler 相互独立）。

### 1145（0x479）跨图自动寻路

C→S：`[BYTE 0, INT map_id, BYTE x, BYTE y]`（screen 300 采集页点击目标）。
S→C action 0：`[BYTE 0, BYTE count? — 见下]`。核实布局：
`[0]=B action, [1]=I hop_count, records(width=(size-3)/count) 自 index 2, 末尾一个 INT(ab.T, 不读语义)`；
hop 记录 `[INT map_id, INT x, INT y]`（`ab.s()` 只读首记录 0/1/2 → 同图寻路 `ab.c(x,y,true)`）。
本服同图目标回单跳记录；跨图目标本服不支持（记 GATHER_REJECT 日志）。
记录宽 = 3，即整帧 `[BYTE 0, INT 1, INT map, INT x, INT y, INT 0]`。

## 四、1084（0x43C）装备打造

### 已确认 C→S（builder 全部核实，含等待态 `t.a(true,false)`）

| 请求 | wire |
|---|---|
| 列表 | `[BYTE 0, INT context(=screen_mode/1000), SHORT idx, SHORT page, BYTE page_size]` |
| 属性缓存 | `[BYTE 1, INT recipe_id]` |
| 选择打造 | `[BYTE 2, INT recipe_id]` |
| 查看材料 | `[BYTE 4, INT recipe_id]` |
| 领取（动画后） | `[BYTE 3, INT recipe_id, INT slot1..4(实例 id)]` |
| 确认打造 | `[BYTE 5, INT recipe_id, INT slot1..4(实例 id)]` |

### S→C（路由 `e.o`：第一语句无条件清等待；action 4 被忽略）

| action | wire | 状态 |
|---|---|---|
| 2（详情→al/355） | `[0]=B 2, [1]=B 布局(2|3), [2..9]=4×(I 材料template id, S 材料名), [10..15]=6×S 说明行` | **完整核实** |
| 3（领取结果） | `[0]=B 3, [1..6]=6×S 文本`；关 356 列表页、点亮打造按钮 | 完整核实 |
| 5（打造受理） | `[BYTE 5]` 无字段；触发 6 秒锻造动画，动画完发 action 3 领取 | 完整核实（无成功标志/无发放字段） |
| 0（配方列表→am/356） | `[1]=I npc_id, [2]=?(count), [3]=B flag, [4..]=records(width=(size-4)/count, rec[0] 去重, rec[2] 页列)`；al 侧映射 rec[0]/[1]→b/a.a(id,id)、rec[2]→j.i、rec[4]→j.o | **record 语义未完整锁定** |
| 1（属性缓存） | `[g(1), g(2)]` 原始对入 am.M | 部分核实 |

打造完成物品如何发放：客户端无字段（推测为通用背包帧），**unknown**。
按任务要求：本服实现 registry + 请求守卫 + 纯业务事务与测试；
**不下发任何 1084 S→C 帧**，UI 链未标记完成。

## 五、体力/活力（property 55–58）

| property | 含义 | 消耗 |
|---:|---|---|
| 55 | 体力（当前） | 采集草药/矿石 |
| 56 | 体力上限 | — |
| 57 | 活力（当前） | 炼药/酿酒/制造 |
| 58 | 活力上限 | — |

玩家真值持久化于 `role['life_skills']`（迁移见下），经 `player_info` 55–58
与 `1017` 增量帧同步；不新增平行真值字段。

## 六、玩家状态迁移（`role['life_skills']`）

```json
{
  "stamina": 100, "stamina_max": 100,
  "vitality": 100, "vitality_max": 100,
  "skills": {"2001": {"level": 1, "proficiency": 0}},
  "learned_recipes": []
}
```

旧角色无该字段时在 `RoleStore` 读取路径自动初始化（体力/活力满值，无技能，
无配方）并随下次保存持久化；不影响旧登录。上限 100/100 为 `[compat]`
（延续服务端现有 55–58 硬编码值）。

## 七、本地兼容数值清单（非 APK 数据）

- 技能/配方/条目/采集点 id 与名称、消耗、时长、产量、熟练度收益 → `[compat]`
- 体力/活力上限 100 → `[compat]`
- 采集实体点击菜单文本“采集” → `[compat]`（field 9 原文不可恢复）
- 协议字段/动作/类型 → 全部 `[APK]`
