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

### Phase 1 — State ✅ 已实现，待真机/本地回归
已新增 `socket.py`、`socket_types`、`socket_state_version=1` 与迁移测试。
本阶段不改变 action 90 的开孔行为；现有真机表现应保持不变。

实现提交：
- `fa6c668e02cbcfa22e95168f279250dc5be7bdd1`：socket domain
- `26ffc69d2bc55285f8d479a720875a9c0b9aa4c0`：protocol 统一 helper
- `af352842484ea5fc3f81c39ee0216478c43d521b`：RoleStore migration V1
- `8fa1fdef6335394e33fe879ff63d73f87fbca521`：migration tests
- `b5378284b553bec1e06d812e51219f18f0e6d856`：新发放装备补齐 socket state

注意：当前执行环境无法直接 clone GitHub 仓库运行 unittest，因此不能声称自动化测试已通过；
代码已做静态复核，进入 Phase 2 前需要按计划完成回归。

### Phase 2 — Opening ✅ 已实现，待真机颜色回归
开孔成功后不再统一写 `1`，而是生成真实孔型：

- 普通原生装备（slot 1..10，除腰带/护腕）：候选 `1..6`。
- 腰带（slot 4）与护腕/手镯（slot 8）：候选 `1..7`，允许紫孔。
- 官方颜色权重未知，当前本地兼容策略在合法候选集中等概率。
- `socket_types[index]` 与 `extra_attributes[index]` 同步写入同一真实孔型。
- 继续沿用已真机验证的 action 90 事务、1008(operation=3) 与 action 95 实时刷新。

实现提交：
- `34a88fcefe59b82183517f07ecb4c14c805f2879`：合法孔色集合与随机策略
- `88328c556cd0a17b1cbb5ed89924cdca3245a2f4`：action 90 写入真实孔色
- `ff91d2c8c1ffd4849f0af7ded44efbb274b729e6`：普通装备/腰带/护腕孔色测试

Phase 3 前真机重点验证：同一装备连续开孔出现不同颜色时，关闭/重开页面仍保持原色；
腰带/护腕出现紫孔时客户端能正常绘制。

### Phase 3 — Gems ✅ 已实现，待真机验证
已完成 9 族 × 12 阶曜灵石模板目录，以及 `action 98/93` 原生镶嵌事务。

当前实现：
- `98`：打开/重绑“宝石镶嵌”页。
- `93`：确认镶嵌，字段为装备实例 ID + 宝石实例 ID。
- 服务端严格按 0→4 找第一个“已开且为空”的孔，不允许跳孔。
- 孔色不匹配时拒绝，且不消耗宝石。
- 匹配成功后仅把 `extra_attributes[index]` 替换为宝石模板 ID；
  `socket_types[index]` 保留原始孔色，供后续拆除恢复。
- 成功后发送装备 1008、宝石数量更新、action 93 repaint、action 98 rebind。
- 新旧角色仅一次性发放每族 1 阶测试宝石各 100 个；消耗后不会登录重发。
- 2～12 阶模板已入目录，但不自动发放。

实现提交：
- `46bd416af4a7f4769b32d886c5e2b51c7972cd42`：9 族 1 阶测试目录
- `029678ceec0ba45743b74f6282a2bfd6358f0172`：测试宝石 starter grant
- `a1d4ae7df9e1a5749809bc32a089f9f931035ce7`：registry 保留 socket_types
- `9cc37f4daf363f8b1c35c3554d04489f601f77a3`：98/93 协议帧
- `2363c53d977dcb942469351b4ec8cdcc65813b35`：镶嵌事务
- `554bf1b35127d1ded55e360264f0aa3c275b4682`：handler 路由
- `b2e731cb25caebcca5d7a2499b92e1d2d9bf7432`：镶嵌测试矩阵
- `e6dcd509a068036855f57f2800ad1c9feee5ef5d`：测试宝石一次性初始化
- `cfa44ccc881bbd617184854ca7aba4043328876e`：消耗后不重发测试
- `5a8099a3222446e71949921edef8cb7395981ef4`：补全 9 族 × 12 阶目录

真机重点验证：
1. 镶嵌页能列出 9 类 1 阶测试宝石。
2. 与第一个空孔颜色不匹配的宝石被拒绝且不扣数量。
3. 匹配宝石成功后，孔位立即显示已镶嵌宝石。
4. 退出/重进、重新登录后镶嵌状态保持。
5. 连续镶嵌时严格进入第 1→5 个已开孔，不跳孔。


### Phase 4 — Removal ✅ 已实现，待真机验证
已实现 `73 / 108 / 72` 拆除链路。

当前实现：
- `73`：打开/重绑“宝石拆除”页。
- `108`：读取指定装备与孔位中的已镶嵌宝石；当前保留安全兼容查看响应，
  因为保存下来的 smali 子集中缺少原生 S→C action 109 的完整字段解析，未伪造未知 payload。
- `72`：确认拆除。
- 仅允许拆除真实已镶嵌的曜灵石模板。
- 拆除费用固定按 APK 帮助文本扣除 1000 银两。
- 宝石优先回到背包内同模板堆叠；无同模板堆叠时创建新物品实例。
- 背包无空位时拒绝拆除，不扣钱、不修改装备。
- 拆除后 `extra_attributes[index]` 从宝石模板 ID 恢复为
  `socket_types[index]`，原始孔色不丢。
- 通过 1017 property 50 增量同步银两。
- 成功后重新发送 action 73 刷新拆除页。

实现提交：
- `b48e21b5099659eed75c07709a62d46fc62cd2bf`：拆除协议与银两增量帧
- `a4fa10ce37f66c6cdb0e76f590b7f0f78341202d`：拆除事务
- `3b21bc449b29707be536ad360968fcc98d93048c`：新返还宝石使用 1008 add operation
- `edf8b134ba216f7db3fa622d7e17f24eb573f495`：handler 路由
- `fc3d8b54bf530cd48686e93e2707583c842681fa`：Phase 4 测试矩阵

真机重点验证：
1. 已镶嵌装备能进入拆除页并选择孔位。
2. action 108 查看孔内宝石不会卡“请稍后”。
3. 确认拆除后宝石回到背包。
4. 孔位立即恢复原来的颜色，而不是统一青孔。
5. 银两准确减少 1000。
6. 退出重进与重新登录后状态保持。

### Phase 5 — Washing ⏸ 延后，作为后续玩法拓展
当前真机客户端入口中没有可用的“装备洗孔”页面，因此本阶段不继续开发，避免为当前不可达 UI 提前实现未验证玩法。

已保留并锁定的协议研究结果：
- `96`：洗孔页初始化。
- `91`：确认洗孔。
- `322251001..322251004`：分别对应第 2～5 孔。
- 普通装备候选孔色 1..6；腰带/手镯允许 1..7。
- 已镶嵌孔默认应先拒绝直接洗孔，避免吞掉宝石。

后续若恢复/开放洗孔入口，再从本阶段继续，不影响当前已完成的开孔、镶嵌、拆除系统。

### 当前后续优先项
1. 追查曜灵石原生物品资源（icon_code / 图集 / 12 阶对应关系）。
2. 替换 Phase 3 当前占位 icon_code。
3. 将曜灵石正式纳入原生物品资源库。
4. 再继续宝石实际属性加成与装备战斗数值联动。

