# 同图在线玩家互见协议（APK 逆向确认 + 本地服实现）

> 本文记录多账号同图互见（其他玩家出现/移动/移除）的协议链路。
> 接收端均为原 APK 主分发器 `pmsj/work/main/e.smali`（`.method public static
> a(Ljava/io/DataInputStream;)V`，字段偏移寄存器 v6=3、v7=0、v8=1、v13=2、v14=4）。
> 本地服实现位于 `systems/map/handler.py`、`systems/role/protocol.py`。

## 容器与类层次（pmsj/work/b/m.smali、b/n、b/q、b/v）

| 类/容器 | 语义 |
|---|---|
| `b/n` (extends b/e) | 通用地图对象；1126 subtype=0 批量生成后加入 `m.u`（小写 u） |
| `b/q` (extends b/n) | 会走路的怪/AI 对象；2028 生成后加入 `m.X`，`m.j(id)` 只查 X |
| `b/v` (extends b/n) | **玩家角色**（带装备叠加层）；经 `m.a(III)` 加入 `m.U`，`m.n(id)`/`m.z()` 查 U |
| 1010/action=18 | id ≤ 299,999 → `m.m(id)`（V/W 容器）；id ∈ [1_000_000, 499_999_999] → `m.p(id)` 删 **U** |

结论：1126/b/n 路线**不能**用于玩家——其容器 u 无消息级移动入口（1005 的
`m.j` 只查 X），且 1126 的 raw-model 需 +0x200b20 后的 role/*.dat 直接存在。
玩家必须走原生 **1014（出现，b/v）→ 1005（走路）→ 1010/action=18（移除）**。

## 出现：S→C 1014（`0x3f6 → :sswitch_24` → `e.T`）

`T` 的处理（行 3117 起）：

1. `m.z()`（= U 容器）size ≥ 20 直接丢弃（同屏其他玩家上限 20）；
2. `id = w.c(1)`，等于接收者自身 role_id（`ab.u()`）则丢弃；
3. 精灵族 = `v.H(w.d(22))`：`H(x)=100000+((x%10000)/1000+1)*1000`，
   字段 22 即 1006 的坐骑骑乘码（未骑乘为 0 → H=100000 基础角色族）；
4. `m.a(id, H(22), w.d(6))` get-or-create **b/v**：构造器
   `b/v(id, dir=0, sprite=H(22), model=field6, true)`，`y(model)` 按模型
   叠加身体/装备图层（与选人界面 main/e.K 同一构造链）；
5. **整帧字段按索引拷进属性包** `v.a(i, field[i])` —— 字段 i 即属性 i；
6. `v.c(w.d(4), w.d(5))` 落格，`I()` 刷新。

因此 **1014 帧字段布局 = 1006 的 85 属性表去掉数量前缀、按下标直排**：
field1=actor id、field3=名字、field4/5=x/y、field6=model、field7/14..20=外观、
field22=坐骑码。本地服实现：`systems/role/protocol.py::role_property_fields`
（从 `player_info` 抽出的同一张表）+ `player_appear_frame`，仅替换
field1=1_000_000+role_id、field4/5=当前坐标。

## 走路：S→C 1005（`0x3ed → :sswitch_25`，分发器内联）

读取 `id=w.c(0)`、`x=w.b(3)`、`y=w.b(4)`（均为 short 3/4 —— 与巡逻 Boss
`roaming_boss_move_frame` 的 [int id, short src_x, short src_y, short dst_x,
short dst_y] 一致，客户端只读 0/3/4）。随后按 id 分流：

- id ∈ [699,233, 798,975] → q 分支：`m.j(id)` 查 X，`q.b(x,y,0)` 走路（明雷怪）；
- **其余 id → b/v 分支（cond_15）**：`m.n(id)` 查 U，
  - 找到且逐轴 |Δ| ≤ 20（相对接收者自身坐标 `ab.e/f`）→ `ad()` 取消当前
    行走 + `b(x,y,0)` 走路（cond_17）；
  - 找到但超出 20 格 → `m.p(id)` **就地移除**（cond_16，原生视野剔除）；
  - 未找到且 20 格内且 U<20 → `w.b(0x3f6, id)` **把当前帧按 1014 重新分发**
    （cond_18，懒重建——要求 1005 帧携带完整属性表；本地服不做懒重建，
    而是服务端镜像邻近状态，见下）。

## 移除：S→C 1010/action=18

id ∈ [1_000_000, 499_999_999] → `m.p(id)` 从 U 删除（见上表）。玩家对象
id 约定 `1_000_000 + role_id`（role_id 自 10001 递增，< 900,000），同时
满足：b/v 分支（避开 699,233..798,975 的 q 区间）、m.p 区间、不与怪物
1_900_001+/传送点 580_001 冲突。

## 本地服实现（systems/map/handler.py）

`MapSystem` 维护 `self._visible_roles: dict[role_id, set[actor_id]]`——
APK U 容器的服务端镜像；role_id 不在表中 = 该客户端尚未进图或已离场，
不向其发送任何可见性帧。推送通道与在线快照由 `LocalGameServer` 注入
（`push_to_role` / `online_roles_hook`）。

| 场景 | 行为 |
|---|---|
| 进图（1010/action=13） | `_announce_player_entry`：清空自身视野集合；对 20 格内已进图的其他在线玩家**双向**发 1014（对方看到我、我看到对方）；换图时先向旧图在线玩家广播 1010/action=18 并清理其集合 |
| 移动（1005） | `_update_player_visibility`：对每个同图在线者按新格逐轴判定 20 格——进入范围→1014（首次）；格内移动→1005 走路帧（复用 `map_actor_move_frame`）；离开范围→1010/action=18。双向成对处理，静止一方随移动者跨界增减 |
| 断线/切换角色 | `depart_map`（server.py finally / 角色切换簿记）：向最后公告地图广播 1010/action=18，弹出自身视野集合并从所有集合中剔除该 actor |

20 格逐轴判定与 APK cond_15/17 的 `|ab.e-x|≤20 && |ab.f-y|≤20` 完全一致，
因此服务端永不发出会触发 cond_16 自动剔除或 cond_18 懒重建的 1005 帧。

## 外观同步：换装后定向 1017（`0x3f9 → :sswitch_20` → `e.O`）

`O` 读取 `target = w.c(1)`，经 `m.o(target)` 定位角色——target 等于自身
role_id 时命中自身访问器 `ab`，否则按 id 查 **U 容器里的 b/v**；随后逐对
`(byte 属性, typed 值)` 写入属性包，sparse-switch 对外观属性触发对应图层
重载（`v.d(II)Z`/`v.b(IZ)`，image family 0x2143a0/0x208050/0x21b8d0 等），
循环后统一刷新。因此 **1017 天然支持定向刷新其他玩家的装备外观**。

本地服实现：`CharacterUpdateBus` 增加 `on_publish` 回调（产出刷新帧的
事件统一触发），server.py 接到 `MapSystem.broadcast_player_appearance(role)`
——对视野集合里持有 `1_000_000+role_id` 的其他在线客户端发送
`character_appearance_frame(actor_id, properties)`，其中 `properties` 为
`character_appearance(role, registry)` 全表 + 属性 22（`mount_ride_code_for_role`，
走 O 的 0x16 分支 `v.I(I)` 重载精灵族）。换装、强化、卸下等一切走总线的
`EQUIPMENT_CHANGED` / `EQUIPMENT_STRENGTHENED` / `CHARACTER_APPEARANCE_CHANGED`
事件自动覆盖。

### 外观属性 → 装备槽位覆盖表（`character_appearance`）

| 属性 | 图层 | 数据来源 |
|---|---|---|
| 2 | 铠甲主体（image 14000..14030） | slot 3，`armor_property2_from_equipment`（资料库优先） |
| 7 | 武器 + 强化炫光 | slot 10，icon 映射 + 实例强化档位 |
| 14 | 腿甲 | slot 5，模板 `appearance_properties` |
| 15 | 旧铠甲层 | 仅模板（slot 3 不覆盖 2/15） |
| 16 | 肩甲 | slot 2，模板 `appearance_properties` |
| 17 | 护腕 | slot 8，模板 `appearance_properties` |
| 18 | 长靴 | slot 9，模板 `appearance_properties` |
| 19 | 披风 | slot 7，模板 `appearance_properties` |
| 20 | 头盔（image 21000+） | slot 1，`helmet_property20_from_icon`（资料库优先，模板硬编码不覆盖） |
| 22 | 坐骑/精灵族 | `mount_ride_code_for_role`；坐骑穿/卸分支经 `appearance_broadcast_hook` 广播 |

腰带(4)/项链(6)/戒指(11) 无外观层（`PREVIEW_SLOTS_WITHOUT_APPEARANCE`）。
头盔映射目录 `helmet_appearance_mapping.json` 目前仅收录 icon 102；
新装备外观需按团队审计流程扩充目录，服务端不猜映射。

## 与 1126 方案的关系

1126 subtype=0（`e.Q`）仍用于怪物、传送点与 NPC 朝向补丁；玩家可见性
不再使用 1126（b/n 在 u 容器无移动入口，且模型字段语义不匹配属性表）。
