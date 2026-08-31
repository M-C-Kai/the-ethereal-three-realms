# 独立地图注册表与多传送点 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 把 58 的全局默认地图字段迁移为类型化地图注册表，令 58 以“长安”独立配置，并支持 58 的两个前向传送点与 50000 的返回传送点。

**Architecture:** 新建 `map_registry.py`，负责地图/实体/传送点数据模型、配置解析、旧格式兼容和启动校验。`server.py` 的网络协议函数改为消费 `MapDefinition`，角色只持久化当前地图 ID 与进入坐标；地图名称、资源和实体始终从注册表派生。

**Tech Stack:** Python 3.10+、`dataclasses`、JSON、现有 `unittest`/TCP 协议测试。

**Spec:** `docs/superpowers/specs/2026-08-31-map-registry-design.md`

## Global Constraints

- 58 地图名称固定为“长安”；50000 继续名为“传送测试区”。
- 不修改 `.map.o`、`.map.ref`、APK 图集或协议字段布局。
- 58 生成传送点 `580001`、`580003`；50000 生成返回点 `580002`。
- 未知地图不得继承 58 的名称、文件、出生点或实体。
- 旧扁平配置和旧角色存档必须无损加载；不删除旧 `map_name` 或道具字段。
- `data/npcs.json` 只能补充注册表中已有 NPC 的资源字段，不能追加缺坐标 NPC。
- 每项生产代码变更前必须先写并运行失败测试。
- 不访问官方或第三方服务器，只在本机隔离端口验证。

---

### Task 1: 类型化地图注册表与配置校验

**Files:**
- Create: `map_registry.py`
- Create: `tests/test_map_registry.py`

**Interfaces:**
- Produces: `MapActorDefinition`, `PortalDefinition`, `MapDefinition`, `MapRegistry`。
- Produces: `load_map_registry(payload: dict[str, object], npc_catalog: list[dict[str, object]] | None = None) -> MapRegistry`。
- Produces: `default_map_registry() -> MapRegistry`，供 `Settings()` 与测试使用。

- [ ] **Step 1: 写新格式解析失败测试**

```python
def test_registry_loads_changan_and_all_portals():
    registry = load_map_registry(NEW_CONFIG)
    changan = registry.require(58)
    target = registry.require(50000)
    self.assertEqual(changan.name, '长安')
    self.assertEqual(changan.map_o_file, 'maps/58.map.o')
    self.assertEqual([portal.id for portal in changan.portals], [580001, 580003])
    self.assertEqual(changan.portals[1].target_map_id, 50000)
    self.assertEqual((changan.portals[1].target_x, changan.portals[1].target_y), (8, 6))
    self.assertEqual([portal.id for portal in target.portals], [580002])
```

- [ ] **Step 2: 运行测试并确认因模块不存在而失败**

Run: `D:\python\python.exe -m unittest tests.test_map_registry.MapRegistryTests.test_registry_loads_changan_and_all_portals -v`

Expected: `ModuleNotFoundError: No module named 'map_registry'`。

- [ ] **Step 3: 实现最小数据模型与解析器**

```python
@dataclass(frozen=True)
class PortalDefinition:
    id: int
    name: str
    model: int
    x: int
    y: int
    direction: int
    target_map_id: int
    target_x: int
    target_y: int

@dataclass(frozen=True)
class MapActorDefinition:
    id: int
    name: str
    model: int
    x: int
    y: int
    direction: int = 0
    label: str = ''
    dat_id: int = 0

@dataclass(frozen=True)
class MapDefinition:
    id: int
    name: str
    map_o_file: str
    map_ref_available: bool
    fallback_width: int
    fallback_height: int
    spawn_x: int
    spawn_y: int
    monster: MapActorDefinition | None
    npcs: tuple[MapActorDefinition, ...]
    portals: tuple[PortalDefinition, ...]

    def with_spawn(self, x: int, y: int) -> 'MapDefinition':
        return replace(self, spawn_x=int(x), spawn_y=int(y))

@dataclass(frozen=True)
class MapRegistry:
    default_map_id: int
    maps: dict[int, MapDefinition]

    def require(self, map_id: int) -> MapDefinition:
        try:
            return self.maps[int(map_id)]
        except KeyError as exc:
            raise ValueError(f'unknown map id {map_id}') from exc

    def portal(self, map_id: int, object_id: int) -> PortalDefinition | None:
        return next((item for item in self.require(map_id).portals if item.id == int(object_id)), None)
```

- [ ] **Step 4: 运行新格式测试并确认通过**

Run: `D:\python\python.exe -m unittest tests.test_map_registry.MapRegistryTests.test_registry_loads_changan_and_all_portals -v`

Expected: `OK`。

- [ ] **Step 5: 写旧扁平配置兼容失败测试**

```python
def test_legacy_flat_config_migrates_to_two_maps():
    registry = load_map_registry(LEGACY_CONFIG)
    self.assertEqual(registry.default_map_id, 58)
    self.assertEqual(registry.require(58).map_o_file, 'maps/58.map.o')
    self.assertEqual(registry.require(50000).map_o_file, 'maps/50000.map.o')
    self.assertEqual(registry.require(50000).portals[0].target_map_id, 58)
```

- [ ] **Step 6: 实现旧字段到注册表的纯函数迁移并转绿**

旧配置的 `map_id/map_name/spawn_*` 构造默认地图；`portal_target_*` 构造目标地图；`portals` 数组存在时全部转换，缺少时从单数 `portal_*` 构造一项；目标地图从 `return_portal_*` 构造返回点。旧 58 名称仍按旧文件读取，新仓库配置由 Task 5 固定为“长安”。

Run: `D:\python\python.exe -m unittest tests.test_map_registry -v`

Expected: 解析测试全部 `OK`。

- [ ] **Step 7: 写并实现校验测试**

```python
def test_registry_rejects_unknown_portal_target():
    payload = deepcopy(NEW_CONFIG)
    payload['maps']['58']['portals'][0]['target_map_id'] = 99999
    with self.assertRaisesRegex(ValueError, 'unknown target map 99999'):
        load_map_registry(payload)

def test_registry_rejects_duplicate_portal_ids():
    payload = deepcopy(NEW_CONFIG)
    payload['maps']['50000']['portals'][0]['id'] = 580001
    with self.assertRaisesRegex(ValueError, 'duplicate portal id 580001'):
        load_map_registry(payload)

def test_registry_rejects_out_of_bounds_target():
    payload = deepcopy(NEW_CONFIG)
    payload['maps']['58']['portals'][0]['target_x'] = 127
    with self.assertRaisesRegex(ValueError, 'target coordinate'):
        load_map_registry(payload)
```

校验 `default_map_id`、地图键、尺寸 `2..127`、出生点、实体坐标、传送目标和全局传送点 ID。

Run: `D:\python\python.exe -m unittest tests.test_map_registry -v`

Expected: 全部 `OK`。

- [ ] **Step 8: 提交注册表模型**

```powershell
git add map_registry.py tests/test_map_registry.py
git commit -m "feat: add validated map registry"
```

---

### Task 2: Settings、角色地图状态与世界名称迁移

**Files:**
- Modify: `server.py:58-141`
- Modify: `server.py:416-434`
- Modify: `server.py:563-715`
- Modify: `server.py:1394-1421`
- Test: `tests/test_map_registry.py`
- Test: `tests/test_protocol.py:156-232`

**Interfaces:**
- Consumes: `MapRegistry`, `MapDefinition`, `default_map_registry()`, `load_map_registry()`。
- Produces: `Settings.map_registry: MapRegistry`, `Settings.default_map_id: int`。
- Produces: `settings_for_map(settings: Settings, map_id: int) -> MapDefinition`。
- Produces: `settings_for_role(settings: Settings, role: dict[str, object] | None) -> MapDefinition`。

- [ ] **Step 1: 写 Settings 加载与长安名称失败测试**

```python
def test_settings_loads_nested_registry_and_ignores_no_map_keys():
    settings = Settings.load(config_path)
    self.assertEqual(settings.default_map_id, 58)
    self.assertEqual(settings.map_registry.require(58).name, '长安')
    self.assertEqual(len(settings.map_registry.require(58).portals), 2)

def test_world_name_is_derived_from_registry_not_stale_role_name():
    settings = Settings(map_registry=default_map_registry())
    role = default_role(settings)
    role['map_name'] = '旧名称'
    _, fields = decode_frame(notice_and_world(settings, role)[1])
    self.assertEqual(field_values(fields)[3], '长安')
```

- [ ] **Step 2: 运行测试并确认当前 Settings 无 `map_registry` 而失败**

Run: `D:\python\python.exe -m unittest tests.test_map_registry.SettingsRegistryTests -v`

Expected: `TypeError` 或 `AttributeError` 指向缺失的注册表接口。

- [ ] **Step 3: 修改 Settings 与 Settings.load**

保留服务器级字段；移除协议代码对顶层地图字段的依赖。`Settings.load()` 把完整 JSON 交给 `load_map_registry()`，并只把服务器字段传给数据类。`Settings()` 使用 `default_map_registry()`，确保现有纯单元测试不依赖磁盘配置。

- [ ] **Step 4: 修改角色初始化和旧存档迁移**

```python
initial_map = settings.map_registry.require(settings.default_map_id)
role.update({
    'map_id': initial_map.id,
    'map_x': initial_map.spawn_x,
    'map_y': initial_map.spawn_y,
    'map_name': initial_map.name,
})
```

`RoleStore.roles_for()` 对已知地图补齐缺失坐标；未知地图记录警告并迁回默认地图。旧 `map_name` 字段保留但每次保存时同步注册表名称。

- [ ] **Step 5: 实现地图查询与世界帧派生**

```python
def settings_for_map(settings: Settings, map_id: int) -> MapDefinition:
    return settings.map_registry.require(map_id)

def settings_for_role(settings: Settings, role: dict[str, object] | None) -> MapDefinition:
    map_id = int(role.get('map_id', settings.default_map_id)) if role else settings.default_map_id
    definition = settings.map_registry.require(map_id)
    if role is None:
        return definition
    return definition.with_spawn(
        int(role.get('map_x', definition.spawn_x)),
        int(role.get('map_y', definition.spawn_y)),
    )
```

`notice_and_world()` 使用查询结果的 `id/name`，不读取角色中的旧名称。

- [ ] **Step 6: 运行角色/世界测试并确认通过**

Run: `D:\python\python.exe -m unittest tests.test_map_registry tests.test_inventory -v`

Expected: 全部 `OK`，背包迁移测试保持通过。

- [ ] **Step 7: 提交 Settings 与存档迁移**

```powershell
git add server.py tests/test_map_registry.py tests/test_protocol.py
git commit -m "refactor: load maps from registry"
```

---

### Task 3: 地图数据、NPC、妖兽和多传送点协议帧

**Files:**
- Modify: `server.py:1450-1595`
- Modify: `server.py:2432-2496`
- Modify: `tests/test_protocol.py:940-990`
- Modify: `tests/test_npc_spawn.py`

**Interfaces:**
- Consumes: `MapDefinition`, `MapActorDefinition`, `PortalDefinition`。
- Produces: `map_portal_frame(portal: PortalDefinition) -> bytes`。
- Produces: `map_portal_frames(map_definition: MapDefinition) -> list[bytes]`。
- Produces: `map_return_portal_frame(map_definition: MapDefinition) -> bytes` 兼容现有导入，返回当前地图第一项传送帧；空列表抛出 `ValueError`。
- Produces: `map_enter_frames(map_definition: MapDefinition, role_id: int) -> list[bytes]`。

- [ ] **Step 1: 写两个前向传送点失败测试**

```python
def test_forward_portals_spawn_all_entries_on_changan():
    map_definition = default_map_registry().require(58)
    frames = map_portal_frames(map_definition)
    self.assertEqual(len(frames), 2)
    values = [field_values(decode_frame(frame)[1]) for frame in frames]
    self.assertEqual([item[2] for item in values], [580001, 580003])
    self.assertEqual(values[1][3:5], [34, 7])
```

- [ ] **Step 2: 运行测试并确认当前缺少复数函数而失败**

Run: `D:\python\python.exe -m unittest tests.test_protocol.ProtocolTests.test_forward_portals_spawn_all_entries_on_origin_map -v`

Expected: 当前导入错误或缺少 `map_portal_frames`。

- [ ] **Step 3: 实现复数传送帧和方向帧**

每个 `1126/subtype=0` 传送帧从 `PortalDefinition` 读取自身 `id/x/y/model/name`。`map_enter_frames()` 依次追加所有传送帧，并为每个传送点追加 `map_actor_direction_frame(portal.id, portal.direction)`。

- [ ] **Step 4: 写地图实体隔离失败测试**

```python
def test_each_map_uses_only_its_registered_entities():
    registry = default_map_registry()
    changan_ids = [decode_frame(frame)[0] for frame in map_enter_frames(registry.require(58), 10001)]
    target_ids = [decode_frame(frame)[0] for frame in map_enter_frames(registry.require(50000), 10001)]
    self.assertEqual(changan_ids.count(2030), 3)
    self.assertEqual(target_ids.count(2030), 0)
    self.assertEqual(len(map_portal_frames(registry.require(58))), 2)
    self.assertEqual(len(map_portal_frames(registry.require(50000))), 1)
```

- [ ] **Step 5: 去除 NPC 的 58 硬编码并适配可选妖兽**

`map_npc_frames/map_npcs_near/map_npc_for_object_id` 只读取当前 `MapDefinition.npcs`。`map_enter_frames()` 在 `monster is not None` 时生成妖兽及方向帧；传送点不再复用全局妖兽字段。

- [ ] **Step 6: 改造 map_data_frames/map_action**

`map_data_frames()` 读取当前 `MapDefinition.map_o_file` 和自身 fallback 尺寸。`map_action()` 接收 `MapDefinition` 与明确 `role_id`，使用该地图有效 `spawn_x/spawn_y`。

- [ ] **Step 7: 运行协议和 NPC 测试**

Run: `D:\python\python.exe -m unittest tests.test_protocol tests.test_npc_spawn tests.test_map_registry -v`

Expected: `map_portal_frames` 可导入，传送点与 NPC 测试全部通过。

- [ ] **Step 8: 提交地图协议迁移**

```powershell
git add server.py tests/test_protocol.py tests/test_npc_spawn.py
git commit -m "feat: emit per-map entities and portals"
```

---

### Task 4: 多传送点路由与角色落点持久化

**Files:**
- Modify: `server.py:2504-2726`
- Modify: `server.py:2874-2989`
- Test: `tests/test_map_registry.py`
- Test: `test_client.py`

**Interfaces:**
- Consumes: `MapRegistry.portal(map_id, object_id)`。
- Produces: `apply_portal_transition(settings: Settings, role: dict[str, object], object_id: int) -> MapDefinition | None`。

- [ ] **Step 1: 写两个前向点和返回点状态转换失败测试**

```python
def test_every_registered_portal_persists_target_map_and_coordinates():
    settings = Settings(map_registry=default_map_registry())
    for portal_id in (580001, 580003):
        role = default_role(settings)
        target = apply_portal_transition(settings, role, portal_id)
        self.assertIsNotNone(target)
        self.assertEqual((role['map_id'], role['map_x'], role['map_y']), (50000, 8, 6))

    role = default_role(settings)
    role.update({'map_id': 50000, 'map_x': 8, 'map_y': 6})
    target = apply_portal_transition(settings, role, 580002)
    self.assertEqual(target.id, 58)
    self.assertEqual(target.name, '长安')
    self.assertEqual((role['map_x'], role['map_y']), (60, 67))
```

- [ ] **Step 2: 运行测试并确认 helper 不存在而失败**

Run: `D:\python\python.exe -m unittest tests.test_map_registry.PortalTransitionTests -v`

Expected: `ImportError` 或缺少 `apply_portal_transition`。

- [ ] **Step 3: 实现纯状态转换 helper**

```python
def apply_portal_transition(settings: Settings, role: dict[str, object], object_id: int) -> MapDefinition | None:
    current_id = int(role.get('map_id', settings.default_map_id))
    portal = settings.map_registry.portal(current_id, object_id)
    if portal is None:
        return None
    target = settings.map_registry.require(portal.target_map_id)
    role.update({
        'map_id': target.id,
        'map_x': portal.target_x,
        'map_y': portal.target_y,
        'map_name': target.name,
    })
    return target.with_spawn(portal.target_x, portal.target_y)
```

- [ ] **Step 4: 改造网络交互路由**

`_handle_map_object_interaction()` 先调用 helper；命中后保存角色并发送目标 `1110`。未命中传送点时，只在当前 `MapDefinition` 查 NPC 和妖兽。战斗日志和 escape guard 使用当前地图 ID。

- [ ] **Step 5: 修改移动和进图状态**

`1005` 更新角色 `map_x/map_y` 并持久化，使重连使用最后位置；`1010/action=12/13` 均从 `settings_for_role()` 获取独立地图。进图后 `streamed_npc_ids` 从当前地图 NPC 初始化，不判断 58。

- [ ] **Step 6: 扩展 test_client 的多传送点断言**

`--exercise-portal` 先验证 58 的两个 `1126` 传送实体都已下发，再选择 `580003` 进入 50000，并用 `580002` 返回 58；断言两次 `1110` 名称分别为“传送测试区”和“长安”。

- [ ] **Step 7: 运行状态与协议回归测试**

Run: `D:\python\python.exe -m unittest tests.test_map_registry tests.test_protocol -v`

Expected: 全部 `OK`。

- [ ] **Step 8: 提交传送路由**

```powershell
git add server.py tests/test_map_registry.py test_client.py
git commit -m "feat: route multiple portals by map registry"
```

---

### Task 5: 迁移生产配置、长安文案和完整验证

**Files:**
- Modify: `config.json`
- Modify: `README.md`
- Modify: `PROTOCOL_LOCK.md`
- Modify: `OPENCODE_HANDOFF.md`
- Test: `tests/test_map_registry.py`

**Interfaces:**
- Consumes: Task 1-4 的注册表加载与协议接口。
- Produces: 仓库内唯一文档化的 `default_map_id + maps` 配置格式。

- [ ] **Step 1: 写真实 config.json 加载失败测试**

```python
def test_repository_config_uses_nested_registry_and_changan_name():
    settings = Settings.load(Path(__file__).resolve().parents[1] / 'config.json')
    self.assertEqual(settings.default_map_id, 58)
    self.assertEqual(settings.map_registry.require(58).name, '长安')
    self.assertEqual([item.id for item in settings.map_registry.require(58).portals], [580001, 580003])
    self.assertEqual([item.id for item in settings.map_registry.require(50000).portals], [580002])
```

- [ ] **Step 2: 运行测试并确认旧 config.json 不满足新格式**

Run: `D:\python\python.exe -m unittest tests.test_map_registry.RepositoryConfigTests -v`

Expected: 断言 `maps` 新格式或“长安”名称失败。

- [ ] **Step 3: 将 config.json 迁移为设计文档的嵌套格式**

保留服务器、账号、角色、心跳和存档字段；删除顶层 `map_*`、`monster_*`、`portal_*`、`npcs`，改写为 `default_map_id=58` 与 `maps.{58,50000}`。58 名称及返回点名称分别为“长安”“返回长安”。

- [ ] **Step 4: 更新文档中的地图语义**

README 手机测试应显示“长安”；协议文档的返回描述改为 `58/长安`；交接文档说明地图配置由注册表管理、如何新增地图和传送点，并注明 `maps/*.map.json` 不是运行配置。

- [ ] **Step 5: 运行完整静态与单元验证**

Run: `D:\python\python.exe -m py_compile map_registry.py server.py test_client.py tests\test_map_registry.py`

Run: `D:\python\python.exe -m unittest discover -s tests -v`

Run: `git diff --check`

Expected: Python 编译成功；完整测试零失败、零错误；差异检查退出码 0。

- [ ] **Step 6: 在隔离端口运行 TCP 往返传送测试**

使用临时配置把监听端口设为 `16805`、角色存档指向 `tests/map_registry_verification_roles.json`，启动后运行：

```powershell
D:\python\python.exe test_client.py --host 127.0.0.1 --port 16805 --username map_registry_verification --password local-only --exercise-role-crud --exercise-portal
```

Expected: 角色/背包流程通过，58 下发两个传送点，`580003` 进入 50000，`580002` 返回“长安”，进程退出码 0。随后停止隔离服务并删除临时配置与存档。

- [ ] **Step 7: 检查实际 6805 服务状态**

只读检查现有 PID、监听端口和日志。若 6805 正在运行且属于本项目，在全部测试通过后按项目脚本重启；若未运行，不主动启动面向局域网的服务，只在交付中说明。

- [ ] **Step 8: 提交配置与文档迁移**

```powershell
git add config.json README.md PROTOCOL_LOCK.md OPENCODE_HANDOFF.md tests/test_map_registry.py
git commit -m "feat: migrate maps to independent registry"
```

---

## Plan Self-Review

- Spec coverage: 注册表、旧配置兼容、角色迁移、多传送点、长安名称、错误校验、完整测试均有对应任务。
- Type consistency: 所有任务统一使用 `MapDefinition.with_spawn()`、`MapRegistry.require()`、`MapRegistry.portal()` 与 `apply_portal_transition()`。
- Scope: 保持单妖兽，不引入副本/热重载；没有扩大到地图素材或 APK 修改。
- Execution: 当前会话不允许在用户未请求时派发子代理，因此选择 Inline Execution，并使用 `superpowers:executing-plans` 按任务执行。
