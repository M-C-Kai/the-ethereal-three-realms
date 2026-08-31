# 昆仑门派地图与导师学习闭环 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 建立“长安传送阵 → 独立昆仑地图 → 昆仑导师 → 门派技能学习模式 → 返回长安”的服务端闭环。

**Architecture:** 在现有地图注册表中增加本地地图 `60001`，用配置驱动的 NPC 服务元数据识别昆仑导师。连接内保存最近一次原生 NPC 对话上下文；导师选项通过已确认的 `1010/action=69` 打开门派技能界面 mode 1，实际升级仍复用现有 `1103/action=3` 状态转换。

**Tech Stack:** Python 3 标准库、现有二进制协议编码器、JSON 地图规格、`map_o.py`/`tools/map_o_generator.py`、`unittest`。

**Spec:** `docs/superpowers/specs/2026-08-31-kunlun-sect-loop-design.md`

## Global Constraints

- 新地图 ID 固定为本地 `60001`，不得宣称是原服昆仑编号。
- 保留地图 `50000`“传送测试区”及 `data/roles.json`。
- 核心服务只使用 Python 标准库，不重新打包 APK。
- 协议字段类型必须精确保持 byte/short/int/string 的 APK 读取顺序。
- 昆仑不生成怪物；技能升级只允许走现有 `1103/action=3`。
- 手机端验收由用户执行；仓库要求的最小自动检查仍需运行。

---

### Task 1: 扩展 NPC 服务元数据

**Files:**
- Modify: `map_registry.py:21-30, 55-67, 247-274`
- Test: `tests/test_map_registry.py`

**Interfaces:**
- Produces: `MapActorDefinition.service: str` 与 `MapActorDefinition.sect_id: int | None`。
- Consumes: 现有 `_actor(payload)` 和 `_validate_registry(...)`。

- [ ] **Step 1: 写入失败测试**

在 `tests/test_map_registry.py` 增加用例，向昆仑 NPC 配置写入：

```python
{
    'id': 1900101,
    'name': '昆仑导师',
    'x': 12,
    'y': 8,
    'service': 'sect_skill_mentor',
    'sect_id': 1,
}
```

断言加载后 `service == 'sect_skill_mentor'`、`sect_id == 1`；另断言未知 service 以及导师缺少/使用非法 `sect_id` 时抛出 `ValueError`。

- [ ] **Step 2: 运行定向测试并确认失败**

Run: `D:\python\python.exe -m unittest tests.test_map_registry.MapRegistryTests -v`

Expected: FAIL，提示 `MapActorDefinition` 没有 `service`/`sect_id` 或缺少配置校验。

- [ ] **Step 3: 实现最小元数据与校验**

将数据类与解析器扩展为：

```python
@dataclass(frozen=True)
class MapActorDefinition:
    # existing fields...
    service: str = ''
    sect_id: int | None = None


def _actor(payload: dict[str, Any]) -> MapActorDefinition:
    raw_sect_id = payload.get('sect_id')
    return MapActorDefinition(
        # existing assignments...
        service=str(payload.get('service', '')),
        sect_id=None if raw_sect_id is None else int(raw_sect_id),
    )
```

在 `_validate_registry` 中只接受空 service 或 `sect_skill_mentor`；后者必须有 `sect_id` 且范围为 `1..13`。普通旧 NPC 不带字段时保持现状。

- [ ] **Step 4: 运行定向测试**

Run: `D:\python\python.exe -m unittest tests.test_map_registry.MapRegistryTests -v`

Expected: PASS。

### Task 2: 注册独立昆仑地图、导师与双向传送

**Files:**
- Create: `maps/60001.map.json`
- Create: `maps/60001.map.o`
- Modify: `config.json`
- Modify: `data/npcs.json`
- Modify: `map_registry.py:293-398`（默认注册表与运行配置保持一致）
- Test: `tests/test_map_registry.py`
- Test: `tests/test_npc_spawn.py`

**Interfaces:**
- Produces: 地图 `60001`、长安 portal `580005`、昆仑 return portal `6000101`、导师 NPC `1900101`。
- Consumes: Task 1 的 `service`、`sect_id` 字段。

- [ ] **Step 1: 写入地图与实体失败测试**

断言项目配置和默认注册表都满足：

```python
kunlun = registry.require(60001)
self.assertEqual(kunlun.name, '昆仑')
self.assertIsNone(kunlun.monster)
self.assertEqual([npc.id for npc in kunlun.npcs], [1900101])
self.assertEqual(kunlun.npcs[0].service, 'sect_skill_mentor')
self.assertEqual(kunlun.npcs[0].sect_id, 1)
self.assertEqual(kunlun.portals[0].target_map_id, 58)
self.assertEqual(registry.require(58).portals[-1].target_map_id, 60001)
```

更新 NPC 生成测试，断言地图 60001 只生成导师，地图 50000 仍无 NPC。

- [ ] **Step 2: 运行定向测试并确认失败**

Run: `D:\python\python.exe -m unittest tests.test_map_registry tests.test_npc_spawn -v`

Expected: FAIL，提示未知地图 `60001`。

- [ ] **Step 3: 创建功能地图规格并生成二进制**

以 `maps/50000.map.json` 为安全基线复制规格，唯一语义变化是 `map_id: 60001`；保持 32×32、`tile_definitions: [10]`、全地表索引 0、全可行走、无镜像。使用生成器产生二进制：

Run: `D:\python\python.exe tools\map_o_generator.py build maps\60001.map.json -o maps\60001.map.o`

Expected: `wrote maps\60001.map.o: 1288 bytes, 32x32, 1 definitions`。

- [ ] **Step 4: 配置地图与资源**

在长安增加：

```json
{
  "id": 580005,
  "name": "昆仑传送阵",
  "model": -2004250,
  "x": 62,
  "y": 67,
  "direction": 0,
  "target_map_id": 60001,
  "target_x": 8,
  "target_y": 6
}
```

注册昆仑：

```json
"60001": {
  "name": "昆仑",
  "map_o_file": "maps/60001.map.o",
  "map_ref_available": false,
  "fallback_width": 32,
  "fallback_height": 32,
  "spawn": {"x": 8, "y": 6},
  "npcs": [{
    "id": 1900101,
    "name": "昆仑导师",
    "label": "昆仑导师",
    "introduction": "昆仑道法，贵在潜心修行。",
    "x": 12,
    "y": 8,
    "service": "sect_skill_mentor",
    "sect_id": 1
  }],
  "portals": [{
    "id": 6000101,
    "name": "返回长安",
    "model": -2004250,
    "x": 9,
    "y": 6,
    "direction": 0,
    "target_map_id": 58,
    "target_x": 60,
    "target_y": 67
  }]
}
```

在 `data/npcs.json` 为 `1900101` 复用已验证真人资源 `dat_id: 90010, model: -2009990`。同步更新 `DEFAULT_MAP_PAYLOAD`，防止无配置构造的单元测试与实际运行配置分叉。

- [ ] **Step 5: 检查地图并运行定向测试**

Run: `D:\python\python.exe tools\map_o_generator.py inspect maps\60001.map.o`

Expected: 32×32、1 个 definition、0 blocked、0 mirrored。

Run: `D:\python\python.exe -m unittest tests.test_map_registry tests.test_npc_spawn -v`

Expected: PASS。

### Task 3: 编码导师对话和门派学习界面帧

**Files:**
- Modify: `server.py:1783-1848`
- Test: `tests/test_protocol.py`

**Interfaces:**
- Produces: `SECT_MENTOR_LEARN_OPTION = 1`、`sect_skill_screen_frame(mode: int = 1) -> bytes`、导师感知的 `map_npc_dialogue_frames(npc, role)`。
- Consumes: `MapActorDefinition.service`、`MapActorDefinition.sect_id`。

- [ ] **Step 1: 写入协议失败测试**

新增测试精确断言：

```python
message_id, fields = decode_frame(sect_skill_screen_frame())
self.assertEqual(message_id, 1010)
self.assertEqual([field.type_id for field in fields], [4, 3, 3, 4, 4, 3])
self.assertEqual(field_values(fields), [179, 0, 0, 0, 1, 69])
```

导师对话测试断言昆仑角色获得 option id 1、“学习门派技能”和结束项；非昆仑角色只获得拒绝正文与结束项；普通 NPC 对话仍只有原有正文和结束项。

- [ ] **Step 2: 运行定向测试并确认失败**

Run: `D:\python\python.exe -m unittest tests.test_protocol.ProtocolTests.test_sect_skill_screen_frame_opens_native_mentor_mode -v`

Expected: FAIL，提示 helper 不存在。

- [ ] **Step 3: 实现精确界面帧**

```python
def sect_skill_screen_frame(mode: int = 1) -> bytes:
    return encode_frame(1010, [
        integer(179),
        short(0),
        short(0),
        integer(0),
        integer(mode),
        short(69),
    ])
```

修改 `map_npc_dialogue_frames`：导师且角色门派匹配时在结束项前插入 `dialogue_record(2, option_id=1, text='学习门派技能')`；不匹配时正文替换为“仅限昆仑弟子学习。”；普通 NPC 保持原输出。

- [ ] **Step 4: 运行协议定向测试**

Run: `D:\python\python.exe -m unittest tests.test_protocol -v`

Expected: PASS。

### Task 4: 连接内导师上下文和选项路由

**Files:**
- Modify: `server.py:2772-2850, 2951-3250`
- Test: `tests/test_protocol.py`

**Interfaces:**
- Produces: `LocalNpcDialogueState`、`npc_dialogue_option_frames(settings, role, state, option_id)`。
- Consumes: Task 3 的 `sect_skill_screen_frame()` 与现有 `map_object_interaction_ack_frame()`。

- [ ] **Step 1: 写入状态转换失败测试**

覆盖四种纯函数路径：

1. 当前地图昆仑导师 + 昆仑角色 + option 1 → `[1010/action=7, 1010/action=69]`。
2. 非昆仑角色 → 仅 ACK。
3. state map ID 与角色当前地图不同 → 仅 ACK。
4. option 0 或未知 option → 仅 ACK。

并断言调用后 state 被清空，不能重复使用旧对话。

- [ ] **Step 2: 运行定向测试并确认失败**

Run: `D:\python\python.exe -m unittest tests.test_protocol -v`

Expected: FAIL，提示连接状态或选项 helper 不存在。

- [ ] **Step 3: 实现连接内状态与验证**

```python
@dataclass
class LocalNpcDialogueState:
    map_id: int | None = None
    npc_id: int | None = None

    def select(self, map_id: int, npc_id: int) -> None:
        self.map_id = int(map_id)
        self.npc_id = int(npc_id)

    def clear(self) -> None:
        self.map_id = None
        self.npc_id = None
```

`npc_dialogue_option_frames(...)` 始终先构造 ACK，然后读取当前角色地图并核对 state、NPC、service、导师门派和角色门派；全部匹配且 option 为 1 时追加 `sect_skill_screen_frame(1)`，最后无条件清空 state。

- [ ] **Step 4: 接入网络循环**

- 每个游戏连接创建一个 `LocalNpcDialogueState`。
- `_handle_map_object_interaction` 接收该 state；传送成功时清空，点击 NPC 时记录 map/NPC，并把 role 传给 `map_npc_dialogue_frames`。
- `message_id == 2032` 分支从 `values[0]` 读取 option id，调用 `npc_dialogue_option_frames` 并发送返回帧。
- 旧的只回 ACK 逻辑由新 helper 取代；日志记录 NPC、option、是否打开导师模式。

- [ ] **Step 5: 运行协议与状态测试**

Run: `D:\python\python.exe -m unittest tests.test_protocol -v`

Expected: PASS。

### Task 5: 最小验证、文档同步和服务重启

**Files:**
- Modify: `README.md`
- Modify: `PROTOCOL_LOCK.md`
- Modify: `OPENCODE_HANDOFF.md`
- Modify: `test_client.py`（仅在现有客户端探针需要识别地图 60001 时）

**Interfaces:**
- Consumes: Tasks 1-4 的完整闭环。
- Produces: 可供手机直接验证的最新 6805 服务进程。

- [ ] **Step 1: 同步事实文档**

记录本地昆仑地图 ID、双向传送、导师 option 1、`1010/action=69` 精确字段和“非原服地图还原”的边界。手机端验收步骤不扩展为自动验收规范。

- [ ] **Step 2: 运行完整单元测试**

Run: `D:\python\python.exe -m unittest discover -s tests -v`

Expected: 全部 PASS。

- [ ] **Step 3: 运行静态与地图检查**

Run: `D:\python\python.exe -m py_compile server.py map_registry.py`

Expected: 无输出、exit 0。

Run: `D:\python\python.exe tools\map_o_generator.py inspect maps\60001.map.o`

Expected: 32×32、0 blocked、0 mirrored。

- [ ] **Step 4: 重启唯一服务进程**

只在全部检查通过后停止当前占用 6805 的旧服务，使用项目现有启动方式启动最新 `server.py`。确认新 PID、`0.0.0.0:6805` 监听和最新日志首行时间戳。

- [ ] **Step 5: 运行真实 TCP 探针**

Run: `D:\python\python.exe test_client.py --host 127.0.0.1 --port 6805 --exercise-skill-only`

Expected: `OK`；不得改写或删除现有手机角色存档。
