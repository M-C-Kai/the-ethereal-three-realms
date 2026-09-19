# 装备孔位系统正式重构设计

> 日期：2026-09-19
> 目标：把当前“开孔显示兼容”升级为可持久化、可洗孔、可镶嵌、可拆除的完整原生孔位模型。
> 本文是实现设计，暂不修改业务代码。

## 一、总体原则

客户端只认识一个当前孔位数组：

`1008 fields[34..38] -> g.x[0..4]`

但服务端必须额外保存“原始孔型”，否则宝石镶嵌后 `g.x[i]` 被宝石模板 ID 覆盖，
拆除时无法知道应恢复成什么颜色。

正式模型：

```text
socket_types[0..4]      # 服务端持久化：0=未开，1..7=原始孔色
extra_attributes[0..4]  # 对客户端输出的当前状态
                        # 0 = 未开孔
                        # 1..7 = 已开空孔
                        # gemTemplateId = 已镶嵌
```

不再把 `extra_attributes` 当作足够描述全部孔语义的数据源。
它仍是 **1008 的唯一线协议状态**，但不是服务端唯一持久化状态。

## 二、统一孔位领域 API

建议新增模块：

`implementation_staging/systems/inventory/socket.py`

避免继续把孔逻辑散落在 `protocol.py / service.py / role/service.py`。

### 常量

```python
SOCKET_COUNT = 5

SOCKET_NONE = 0
SOCKET_CYAN = 1
SOCKET_GOLD = 2
SOCKET_RED = 3
SOCKET_YELLOW = 4
SOCKET_BLUE = 5
SOCKET_DARK = 6
SOCKET_PURPLE = 7

VALID_SOCKET_TYPES = {1, 2, 3, 4, 5, 6, 7}
COMMON_SOCKET_TYPES = {1, 2, 3, 4, 5, 6}
```

颜色命名只描述客户端孔框，不直接绑定宝石中文名。
类别 6/7 对应“黑/紫”最终名称若仍有歧义，不影响协议结构。

### 核心 helper

```python
def native_socket_slots(item) -> list[int]
def socket_types(item) -> list[int]
def ensure_socket_state(item) -> bool
def opened_socket_count(item) -> int
def first_empty_open_socket(item) -> int | None
def socket_is_open(item, index) -> bool
def socket_has_gem(item, index) -> bool
def socket_gem_template(item, index) -> int | None
def restore_empty_socket(item, index) -> None
```

判定规则：

- `socket_types[i] == 0`：未开孔。
- `socket_types[i] in 1..7`：已开孔。
- `extra_attributes[i] == socket_types[i]`：已开但为空。
- `extra_attributes[i] > 10` 且属于曜灵石模板族：已镶嵌。
- 不依赖“非零就一定是打开”这种模糊规则做业务判断。

## 三、旧数据迁移

### Migration V1：建立 socket_types

角色加载 `RoleStore._ensure_items()` 增加版本：

`socket_state_version = 1`

对每件允许孔位的装备执行：

#### A. 已有 extra_attributes，全部为 0

```text
extra_attributes = [0,0,0,0,0]
socket_types      = [0,0,0,0,0]
```

#### B. 旧兼容空孔值 1..10

当前历史版本可能留下：

```text
[1,1,0,0,0]
[10,1,0,0,0]
```

迁移规则：

- `1..7`：暂按该值作为 socket_type。
- `8..10`：旧错误/保留帧，迁移为 `1`。
- 同步把 `extra_attributes[i]` 归一成迁移后的孔型。

#### C. 已经包含真实宝石模板 ID

若 `extra_attributes[i]` 是已知宝石模板 ID，但角色没有 `socket_types`：

- 无法从宝石 ID 100% 反推出原孔色时：
  - 优先使用 gem family 的允许孔色；
  - 若该宝石只允许一种颜色，可直接恢复对应 socket_type；
  - 若允许多色（如青色系多个宝石），本质仍只有青色，因此可恢复为 1。
- 若未来出现一个宝石允许多个不同孔色，则记录迁移警告并使用兼容默认，不静默猜测。

#### D. socket_count 老字段

仅作为最老存档迁移来源：

```text
socket_count=N
=> socket_types[:N] = 1
=> extra_attributes[:N] = 1
=> 删除 socket_count
```

戒指和明确不可开孔装备仍不迁移。

### Migration V2：版本化

角色根节点保存：

`socket_state_version: 1`

迁移完成后不重复执行。
以后若修复孔色映射，新增 V2，而不是继续在 V1 中修改历史逻辑。

## 四、开孔重构

当前 `action=90` 成功后写死 `1`，改为：

```python
socket_type = roll_socket_type(equipment, rng, settings)
index = first_unopened_socket(equipment)

socket_types[index] = socket_type
extra_attributes[index] = socket_type
```

### 候选颜色

原版已确认边界：

- 普通可开孔装备：`{1,2,3,4,5,6}`
- 手镯/腰带：`{1,2,3,4,5,6,7}`

建议做：

```python
def allowed_socket_types(item, registry) -> tuple[int, ...]
def roll_socket_type(item, rng, registry, weights=None) -> int
```

默认兼容策略：

- 候选集内等概率。
- 权重配置独立放配置文件，明确标记为“local compatibility”。
- 不把等概率写死成“官方概率”。

### 开孔顺序

必须严格第 1→5 孔依次开启：

`first index where socket_types[i] == 0`

禁止出现：

`[1,0,3,0,0]`

## 五、曜灵石定义

建议在 `registry.py` 新增结构：

```python
@dataclass(frozen=True)
class GemFamily:
    base_template_id: int
    name: str
    socket_types: frozenset[int]
    effect: str
```

9 个族：

- 佛骨舍利
- 木曜
- 土曜
- 金曜
- 火曜
- 炎曜
- 水曜
- 玄曜
- 魔曜

每族模板：

`base .. base+11`

统一 helper：

```python
def gem_family_for_template(template_id) -> GemFamily | None
def gem_rank(template_id) -> int | None
def is_socket_gem(item) -> bool
def gem_fits_socket(template_id, socket_type) -> bool
```

不要把匹配规则散落到 handler 分支。

## 六、1009/action=93 宝石镶嵌

协议：

```text
C→S:
1009
SHORT 93
INT equipmentInstanceId
INT gemInstanceId
```

无孔号。

服务端事务：

1. 找装备。
2. 校验装备允许镶嵌。
3. 找宝石实例。
4. 校验模板属于 9 个合法族。
5. 从 0→4 顺序找第一个：
   `socket_types[i] != 0 && extra_attributes[i] == socket_types[i]`
6. 没有空孔 → 拒绝。
7. `gem_fits_socket(gem, socket_types[i])`。
8. 匹配失败 → 不扣宝石。
9. 匹配成功 → `extra_attributes[i] = gem.template_id`。
10. 宝石数量 -1；归零则移除实例。
11. 保存。
12. 回：
   - 装备 `1008(operation=3)`
   - 宝石数量更新或删除
   - 成功提示
   - 原生 action 98 页面刷新

### 镶嵌成功率

这一步必须和“孔色匹配”分开设计。

建议接口先预留：

```python
def gem_insert_rate(equipment, gem, socket_type, state) -> int
```

在没有官方完整成功率规则前：

- 同色首次镶嵌：按已确认资料可设 100%。
- 其他风险规则不要现在硬编码。
- 第一版正式闭环建议只允许匹配孔色镶嵌，因此天然 100%。

## 七、1009/action=72 宝石拆除

协议：

```text
C→S:
SHORT 72
INT equipmentInstanceId
INT socketIndex
```

事务：

1. 校验 index 0..4。
2. `socket_types[index] != 0`。
3. `extra_attributes[index]` 必须是已知宝石模板。
4. 校验银两 >= 1000。
5. 扣 1000 银两。
6. 将宝石返还背包：
   - 优先与同模板可堆叠实例合并；
   - 否则新建实例。
7. `extra_attributes[index] = socket_types[index]`。
8. 保存。
9. 发送：
   - 装备 1008 更新
   - 宝石背包更新
   - 货币更新
   - action 73 页面刷新

拆除绝不修改 `socket_types[index]`。

## 八、1009/action=91 洗孔

协议：

```text
SHORT 91
INT equipmentInstanceId
INT washStoneInstanceId
```

洗孔石：

- 322251001 → index 1 → 第2孔
- 322251002 → index 2 → 第3孔
- 322251003 → index 3 → 第4孔
- 322251004 → index 4 → 第5孔

事务：

1. 装备至少 2 孔。
2. 由洗孔石推目标 index。
3. 目标孔必须已经开启。
4. 第一版保守规则：目标孔有宝石则拒绝洗孔。
5. 消耗 1 个洗孔石。
6. 从该装备允许孔色集合重新 roll。
7. 是否允许 roll 出原颜色：
   - 原资料未锁定；
   - 第一版允许，避免伪造“必变色”规则。
8. 更新：
   `socket_types[index] = new_type`
   `extra_attributes[index] = new_type`
9. 保存。
10. 发送 1008 + 材料更新 + action 96 页面刷新。

## 九、协议层调整

`protocol.py`：

```python
SOCKET_ACTIONS = {
    72, 73,   # 拆除
    90, 95,   # 开孔
    91, 96,   # 洗孔
    93, 98,   # 镶嵌
    108,      # 查看孔内宝石
}
```

分别提供：

- `socket_opening_open_frame()`
- `socket_washing_open_frame()`
- `gem_embedding_open_frame()`
- `gem_removal_open_frame()`

页面刷新统一 helper：

```python
def socket_page_refresh_frame(mode) -> bytes
```

避免 service.py 自己拼 action 数字。

## 十、handler 结构调整

现在 `handler.py` 只有 opening 和 strengthening。

正式改成：

```text
_handle_socket_action()
    ├── opening
    ├── washing
    ├── embedding
    ├── removal
    └── gem-detail
```

但事务实现不放 handler。

handler 只负责：

- snapshot
- 调 service
- changed 时 save
- 异常 rollback
- 日志

## 十一、测试矩阵

### migration

- 0孔旧装备。
- [1,1,0,0,0]。
- [10,1,0,0,0] 归一。
- 已镶嵌宝石 ID 的旧存档。
- socket_count 老存档。
- 戒指不迁移。
- 二次登录幂等。

### opening

- 第一孔成功后 socket_types 和 extra 同步。
- 普通装备永不生成 7。
- 手镯/腰带可生成 7。
- 失败不改变两数组。
- 第 5 孔后拒绝。
- 重新登录状态一致。

### embedding

- 按顺序镶嵌。
- 不允许跳孔。
- 颜色不匹配拒绝且不扣宝石。
- 匹配成功扣 1。
- 客户端收到宝石模板 ID。
- 重登保持镶嵌状态。

### removal

- 指定 index。
- 拆除恢复原 socket_type。
- 返回相同模板宝石。
- 扣 1000 银两。
- 钱不足不改变装备。
- 空孔不能拆。

### washing

- 第2~5孔正确映射。
- 第1孔无法洗。
- 未开目标孔拒绝。
- 已镶嵌孔第一版拒绝。
- 洗孔后 socket_types/extra 同步。
- 普通装备不出紫。
- 手镯/腰带允许紫。

## 十二、实施顺序

严格分 5 个提交阶段，避免一次改动过大：

### Phase 1 — State
新增 `socket.py`、`socket_types`、migration version、测试。
**不改变现有真机行为。**

### Phase 2 — Opening
开孔开始生成真实 1..6/7 孔色。
保留 action 90 已验证事务和实时刷新方式。

### Phase 3 — Gems
补 9 族曜灵石目录及 `action 98/93` 镶嵌。
真机确认颜色过滤、宝石显示和实时刷新。

### Phase 4 — Removal
实现 `108/72/73`。
真机确认宝石返还、孔色恢复、银两扣除。

### Phase 5 — Washing
实现 `96/91` 与 4 种洗孔石。
最后再验证切玉/洗孔 UI。

每个 Phase 真机通过后再进入下一阶段；不要同时重写开孔、镶嵌、拆除和洗孔。
