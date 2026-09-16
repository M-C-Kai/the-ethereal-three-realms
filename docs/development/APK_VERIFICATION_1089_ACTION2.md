# APK 协议核查结论：1089/action=2（查看他人属性面板）

版本：1.1  
日期：2026-09-15  
核查范围：MessageID 1089/action=2（玩家交互 - 查看他人信息）  
证据等级：**B级（协议帧格式完整闭环）**；属性项图标→属性语义仍为 C 级（需真机标定）

---

## 1. 功能概述

**功能**：玩家点击其他玩家后，弹出的"查看他人信息"面板右侧的属性/按钮列。该列目前显示空白，根因是服务端下发 0 行数据。

**影响模块**：社交系统 - 玩家交互协议  
**方向**：S→C（服务端发送给客户端）  
**MessageID**：1089  
**Action/Subtype**：2（属性列数据）

---

## 2. 协议帧格式（B级已闭环）

### 2.1 最终帧布局

```
1089/action=2:
  field 0:  byte      action = 2
  field 1:  int       占位，客户端不读取（但计入字段总数）
  field 2:  byte      columns = 列数 N
  field 3..: int      按列交错排列的值，共 N*rows 个
```

客户端解析：
- `rows = (字段总数 - 3) / columns`（当每列恰为 [图标, 数值] 时，rows=2）
- 每列取 `rows` 个连续字段，构成 `[La/c/i;` 数组（`a/c/x.a(rows, offset, w)`）

### 2.2 推荐下发形态（rows=2）

```
[byte 2, int 0, byte N,  int 图标0, int 数值0, int 图标1, int 数值1, ...]
```

字段总数 = 3 + 2N → 客户端算出 rows=2，列 c 使用字段 `3+2c`（图标）与 `3+2c+1`（数值）。

---

## 3. 逆向证据链

### 3.1 接收解析：`ey.b(w)`（ey.smali:1758-1833）

已确认逻辑（见 v1.0 记录）：
- `w.a(2)` 读 byte 列数；
- `rows = (w.b.size() - 3) / columns`；
- 逐列 `a/c/x.a(rows, 3+col*rows, w)` 取出 `La/c/i[]`，存入 `ey.an` Vector。

### 3.2 列取值：`a/c/x.a(IIw)`（x.smali:2138-2170）

```smali
.method public static a(IILpmsj/work/main/w;)[La/c/i;
    new-array v1, p0, [La/c/i;            # 行数个
    move v2, 0
:goto_4
    if-ge v2, p0, :cond_16
    iget-object v0, p2, Lpmsj/work/main/w;->b:Ljava/util/Vector;
    add-int v3, v2, p1                     # 偏移 p1 = 3 + col*rows
    invoke-virtual {v0, v3}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;
    move-result-object v0
    check-cast v0, La/c/i;
    aput-object v0, v1, v2
    ...
```

**结论**：`w.b`（字段容器）中 `3..` 的直接就是 `La/c/i` 值对象；列按「列优先」交错存放。

### 3.3 值类型：`La/c/i` 及其实现类

`La/c/i` 抽象类（i.smali）方法：`a()` 类型码、`b()` 取值、`a(I)` 设值、`c()` 取 long。

| 实现类 | `a()` 类型码 | 存储 | 语义 |
|--------|------------|------|------|
| `La/c/h` | 2 | byte `a:B` | byte 值 |
| `La/c/o` | 3 | short `a:S` | short 值 |
| `La/c/m` | 4 | int `a:I` | **int 值**（属性列主要用） |
| `La/c/p` | 6 | StringBuffer | string 值 |
| `La/c/n` | 9 | long `a:J` | long 值 |

属性列使用 **int 值**（`La/c/m`）。

### 3.4 渲染：`ey.k()`（ey.smali:674-836）

对 `ey.an` 中每个列数组（`[La/c/i;`）：

```smali
# 每个列对应面板槽位（slot id）：0x17728 + 列索引
const v1, 0x17728
add-int/2addr v1, v3
invoke-virtual {p0, v1}, Lpmsj/work/e/ey;->w(I)Lpmsj/work/d/b;   # 取槽位

# 1) 显示 v0[1].b() 的字符串（数值文本，位置参数 c=0x0c）
aget-object v4, v0, v7                    # v7=1
invoke-virtual {v4}, La/c/i;->b()I
…
a(Ljava/lang/String;II)V                  # 写入文本

# 2) 图标/颜色：v0[1]>0 → 绿 0x38a806；≤0 → 黄 0x38cf16
if-lez v4, :cond_6d
const v4, 0x38a806                        # 绿
:else
const v4, 0x38cf16                        # 黄

# 3) 数字样式下标 = v0[0].b()，构造 Lpmsj/work/a/i(color, index)
aget-object v0, v0, v6                    # v6=0
invoke-virtual {v0}, La/c/i;->b()I
new-instance v5, Lpmsj/work/a/i;
invoke-direct {v5, v4, v0}, Lpmsj/work/a/i;-><init>(II)V
invoke-virtual {v1, v5}, Lpmsj/work/d/a;->c(Lpmsj/work/a/i;)V

# 4) 特例：列索引 3 的槽位被跳过（v3==3 → continue）；列 4 放置到槽位 index-1
if-eq v3, 0x3 → 跳过
if-ne v3, 0x4 → a(g, v1, v3)
```

**渲染结论**：
- 每列 = 2 个 int：`v0[0]` = 数字图标图集下标（`Lpmsj/work/a/i(color,index)` 的 index），`v0[1]` = 显示数值（>0 绿色 / ≤0 黄色）。
- 因此**每列固定 2 个值 → rows 恒为 2**，服务端应发 `3 + 2N` 个字段。
- 图标样式由 `La/c/i` 的 int 值经 `a/i` 数字图集绘制，属性语义由客户端本地决定。

### 3.5 发送端类型确认：`ey.a(w)`（ey.smali:1041-1138, action=1）

- `w.a(0)B`：field 0 为 byte action；
- `w.d(1)I`：field 1 为 int（角色 id）；
- `w.g(i)`：后续字段为 `La/c/i` 值。

与现有服务端 `encode_frame` 的 `byte` / `integer` 字段能力一致。

---

## 4. 证据等级

### 4.1 已确认（B级）

- ✅ 1089/action=2 协议格式：`[byte 2, int 0, byte N, int...]`（N 列 × [图标下标, 数值]）
- ✅ `rows=(size-3)/columns` 解析逻辑；每列 rows 个连续字段（列优先交错）
- ✅ `La/c/i` 值对象体系（类型码 2/3/4/6/9），属性列用 int（`La/c/m`）
- ✅ 渲染：数值文本 + 颜色（>0 绿 / ≤0 黄）+ 数字图集下标
- ✅ 每列固定 2 值 → 服务端发 3+2N 字段即可闭环

### 4.2 未知项（C级，待确认）

- ❓ **列数 N 的原服典型值**：APK 支持任意 N，但原服通常下发多少列未确认
- ❓ **图标下标取值/映射**：`v0[0]` 应取何值对应具体属性（无资源图集对照，需真机标定）
- ❓ **数值来源**：属性列的数值来自哪些 Character Property（0x54 等），待真机对拍

### 4.3 证据来源

| 证据类型 | 来源 | 等级 |
|---------|------|------|
| 接收解析 | `ey.smali:1758-1833` `b(w)` | B |
| 列取值 | `a/c/x.smali:2138-2170` `a(IIw)` | B |
| 值对象体系 | `a/c/i|h|o|m|n|p.smali` | B |
| 渲染逻辑 | `ey.smali:674-836` `k()` | B |
| 发送/字段类型 | `ey.smali:1041-1138` `a(w)` | B |
| 图标→属性映射 | 无 / 待真机 | C |

---

## 5. 实现建议（遵守证据门槛）

### 5.1 可实现的 B 级部分

1. 新增 `character_view_rows_frame(columns: list[tuple[int,int]])` 编码器：
   `encode_frame(1089, [byte(2), integer(0), byte(len(columns))] + flatten((icon, value) for ...))`
2. 必须处理 `len(columns)==0` → 保持 `[byte(2), integer(0), byte(0)]`（现状安全默认）。
3. 补协议字节级单元测试（golden frame：列数、字段顺序、TLV 类型、总长 3+2N）。

### 5.2 禁止（C级门槛）

- 不得猜测并硬编码具体「属性图标下标」与属性对应关系；
- 若实现，属性列内容必须由**本地配置/显式参数**驱动，默认 0 列；
- 真机验收前一律标注 `pending real-device verification`。

---

## 6. 下一步行动

1. 实现 B 级编码器 + 字节级测试（不改变 wire contract）。
2. 建议用户真机抓包/截图标定：面板出现属性列时的 1089/2 帧、列数 N、各列 [图标, 数值] 与屏幕显示的对应关系。
3. 根据真机结果把图标映射升级到 B 级后再落内容默认值。

---

## 7. 结论

**1089/action=2 协议帧格式已 B 级完整闭环**：`[byte 2, int 0, byte N, int 图标, int 数值 × N]`，每列渲染为「数字图标 + 正绿/负黄数值」。属性项具体内容（图标下标↔属性语义）保持 C 级，不影响帧编码器实现，但不得猜测默认内容。

---

## 8. 参考文件

- `implementation_staging/systems/social/protocol.py:71-75` - 当前实现
- `implementation_staging/build_artifacts/build/dex-smali/pmsj/work/e/ey.smali` - `b(w)` 1758、`a(w)` 1041、`k()` 674
- `implementation_staging/build_artifacts/build/dex-smali/a/c/x.smali:2138` - 列取值 `a(IIw)`
- `implementation_staging/build_artifacts/build/dex-smali/a/c/i{s,m,h,o,n,p}.smali` - 值对象体系
- `implementation_staging/build_artifacts/build/dex-smali/pmsj/work/main/w.smali:965-1114` - 字段读取 `a(I)B/d(I)I/g(I)La/c/i`
- `implementation_staging/build_artifacts/build/dex-smali/pmsj/work/a/i.smali:62-107` - 数字图标绘制 `a/i(color,index)`
- `docs/protocol/15-玩家交互协议.md:48-53` - 协议文档