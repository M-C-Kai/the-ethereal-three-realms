# APK 协议核查结论：1303 查看玩家的请求形态（byte 1 地图菜单）

版本：1.0  
日期：2026-09-17  
核查范围：MessageID 1303（查看玩家）C→S 请求形态与 S→C 打开面板路径  
证据等级：**B 级（发送端字段构造 + 接收端分发表 + 界面解析字段全部闭环）**  
真机状态：`pending real-device verification`

---

## 1. 问题（复现）

玩家在地图上点击其他玩家 → 菜单"查看" → 客户端没有弹出"查看他人信息"
面板，服务端日志只有：

```
INFO received message=1303 field_types=[2, 4]
INFO ignored unimplemented message=1303 values=[1, 1010077]
```

`field_types=[2, 4]` 即 `[byte 1, int 1000000+10077]`：客户端发的是
**action=1 + actor id**，而 `systems/social/handler.py::can_handle` 当时只认
`byte 2`，请求被静默丢弃，客户端收不到 S→C 1303，因此面板根本不打开。

## 2. 发送端证据（B 级）

`pmsj/work/main/k.smali::b(String)`（本文档行号取自
`implementation_staging/build_artifacts/build/dex-smali/`）：

| 行号 | 内容 |
|---|---|
| 4035 | `const/4 v4, 0x2`（1089 用） |
| 4039 | `const/4 v2, 0x1`（1303 用） |
| 4214-4220 | `const-string "查看"` → `equals` 分支 |
| 4222-4230 | `const/16 v0, 0x517` + `w.a(0x517, v2=1, b/v.u()=actor id)` |
| 4232-4240 | `const/16 v0, 0x441` + `w.a(0x441, v4=2, 同 actor id)` |

即点击"查看"一次发两帧：`1303/action=1 [byte 1, int actor id]` 与
`1089/action=2 [byte 2, int actor id]`。

其它入口形态（同一消息号）：

| 发送位置 | 形态 | 语义 |
|---|---|---|
| `main/d.smali:698` | `[byte 2, int 0, string 名字]` | 好友/聊天页菜单"查看" |
| `e/m.smali:180` | `[byte 2, int 0, string 名字]` | 列表页菜单"查看" |
| `e/cx.smali:778`、`e/es.smali:311` | `[byte 2, int 0, string 名字]` | "查看对方" |
| `e/p.smali:839` | `[byte 2, int 0, string 名字]` | "查看对方" |
| `e/be.smali:803` | `[byte 3, int 行首列]` | 排行榜"查看" |
| `main/e.smali:16129 d(I)` | `byte 1`（`m.n(id)` 命中）否则 `byte 2` | 程序化查看入口 |

## 3. 接收端证据（B 级）

`pmsj/work/main/e.smali`：

- 分发表 `0x517 -> :sswitch_eb5`（行 9011）；
- `:sswitch_eb5`（行 8530）读 field0 byte 后 `packed-switch :pswitch_data_1396`
  （行 9212），覆盖 **0x1、0x2、0x3** 三个 action，全部走 `:pswitch_ec4`；
- `:pswitch_ec4` 执行 `d/n.a(0x60, w, false)`，即打开界面 id `0x60`（= `pmsj/work/e/ey`）。

**结论**：面板由 S→C 1303 打开，客户端自身不发包打开面板；S→C 用
action=1（`ey.a(w)` 的 `pswitch_11`，行 1066 起）即可对所有三种 C→S
形态生效。

`pmsj/work/e/ey.smali::a(w)`（行 1041 起）字段读取：

| 字段 | 读取 | 落点 |
|---:|---|---|
| 0 | `w.a(0)B` → `packed-switch` | action |
| 1 | `w.d(1)I` → `m.n(id)` | 目标活对象 `b/v`；为 null 时 `ae()` 关面板 |
| 2 | `w.g(2)` | 属性 0x36（54，配偶） |
| 3 | `w.g(3)` | 属性 0x4b（75，人气） |
| 4 | `a(w, 4)` 辅助 → 装备数量 N | 每件 6 字段 |
| 尾-1 | `w.g(...)` | 属性 0x4f（79，师傅） |
| 尾 | `w.g(...)` | 属性 0x54（84，斗法排名） |
| 末尾 | `ag()` | 刷新面板 |

与本地服 `systems/social/protocol.py::player_view_frame` 的字段布局逐项一致。

## 4. 装备行图标（B 级，2026-09-17 增补）

真机打开面板后装备格空白。根因不在"没读物品数据库"，而是**装备行第 6 个字段
下发了数量而不是图标编号**。

`e/ey.a(w,I)`（装备行解析，`ey.smali:230-318`）的 6 字段落点：

| 偏移 | 读取 | 落点 |
|---:|---|---|
| base+0 | `w.d` int | `new b/g(w.d(base+4), w.d(base))` → `b/j.e`=实例 ID、`b/j.f`=模板 ID |
| base+1 | `w.a` byte | `b/g.k`（槽位） |
| base+2 | `w.e` string | `b/j.o`（名字） |
| base+3 | `w.d` int → `int-to-byte` | `b/j.n` |
| base+4 | `w.d` int | 见 base+0 |
| base+5 | `w.b` **short** | `b/j.q` |

两个字段语义由 1008 解析 `main/e.smali::Z`（行 4108-4200）交叉确认为同一布局：

- field 11（`w.a` byte）→ `b/j.n`；`e/ey.smali:1430` 用 `p1.n` 与 `b/v.c()`
  （角色等级）比较，超出即提示"等级不足，无法装备。" → **n = 等级需求**；
  服务端 `systems/inventory/protocol.py::item_frame` 第 11 字段同样是
  `byte(level_required)`。
- field 12（`w.b` short）→ `b/j.q`；`d/a.a(b/j)`（`d/a.smali:859-895`）
  执行 `La/c/x.f(p1.q)` 得到 `a/i` 并 `a(icon, 0)` 写入槽位图标 →
  **q = 图标编号**；`a/c/x.f(I)`（`x.smali:2976`）为
  `image = 3_002_424 + (icon_code//100%100)*10_000`、`frame = icon_code%100`，
  与 `docs/protocol/1138-consignment-flow.md` 记录的 1008 第 12 字段一致。

因为 `a/c/x.f(1)` 会去查图集 `3_002_424`——该 image id 在 APK
`images` 索引（`build_artifacts/legacy/work/all-images.json`）中**不存在**，
客户端拿不到位图，装备格保持空白；而 `icon_code=6109`（坐骑）对应
`3_612_424`、`icon_code=109`（青纹盔）对应 `3_012_424` 都存在。

**修复**：`systems/social/protocol.py::player_view_frame` 装备行改为

```
[int 模板, byte 槽位, string 名字, int 等级需求, int 实例 id, short 图标编号]
```

即 base+3 用 `resolved['level_required']`、base+5 用
`resolved['icon_code']`（与 1008 同一取值口径）。已核对
`data/catalog/items.json` 全部 15 个 `icon_code` 的图集在 APK 内均存在。

## 5. 本次实现（不改 wire contract）

1. `systems/social/handler.py`：新增 `VIEW_REQUEST_ACTIONS = (1, 2)`，
   `can_handle` 对 1303 接受 byte 1（地图菜单）与 byte 2（名字表单）；
   byte 3（排行榜）保持不认领（目标语义未确认）。
2. `_handle_view`：两种形态共用同一应答（S→C `1303/1` + `1089/2`）；
   目标 `map_id` 与查看者不同时回 1049"对方不在当前地图"——因为
   `ey.pswitch_11` 的 `m.n(actor_id)` 只查本地地图对象，跨图必然 `ae()`
   关面板（实测运营存档中 `role['map_id']` 为权威来源，切图时由
   `systems/map/service.py::apply_portal` 更新）。
3. 未改动任何 S→C 帧布局、消息号或字段类型。

## 5. 测试

`implementation_staging/tests/test_social_system.py`：

- `test_view_map_menu_action1_is_answered`：byte 1 请求被认领并回 2 帧；
- `test_view_rank_list_action3_stays_unclaimed`：byte 3 仍不认领；
- `test_view_target_on_another_map_reports`：跨图回 1049 提示；
- 原有 `test_view_updates_live_actor_with_panel_fields`、`test_view_by_name_variant`
  继续锁定 byte 2 形态与面板字段布局。

## 6. 仍为 C 级的未知项（不得实现）

- 排行榜"查看"（1303/byte 3）目标字段语义（`La/c/a` 行首列是 role id 还是
  名次）未确认；
- 面板右侧属性列（1089/action=2）的"图标下标 ↔ 属性语义"映射未标定，
  本地服继续下发 0 列，见 `APK_VERIFICATION_1089_ACTION2.md`；
- 配偶 / 人气 / 师傅 / 斗法排名尚无本地真值来源，继续回占位值
  （`无` / `0` / `无` / `0`）。

## 7. 参考文件

- `implementation_staging/systems/social/handler.py`（can_handle 1303、_handle_view）
- `implementation_staging/systems/social/protocol.py::player_view_frame`
- `implementation_staging/tests/test_social_system.py`
- `docs/protocol/15-玩家交互协议.md`（查看章节）
- `implementation_staging/build_artifacts/build/dex-smali/pmsj/work/main/k.smali:4214-4244`
- `implementation_staging/build_artifacts/build/dex-smali/pmsj/work/main/e.smali:8530-8543, 9011, 9212-9217, 16129-16161`
- `implementation_staging/build_artifacts/build/dex-smali/pmsj/work/e/ey.smali:1041-1140`
- `implementation_staging/build_artifacts/build/dex-smali/pmsj/work/e/be.smali:803`