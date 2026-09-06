# Character Update Bus Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 建立同步、进程内的人物状态更新总线，使装备切换、卸下、强化、升级等人物状态变化统一触发人物外观和属性刷新，并保证同槽位装备替换不会残留旧装备属性。

**Architecture:** 新增独立 `character_update_bus.py`，只负责事件路由，不反向依赖 `server.py`。`server.py` 将现有已验证的 `character_equipment_refresh_frames()`、外观刷新构建器和“装备是否正在穿戴”判断作为回调注入总线；业务分支完成最终角色状态修改后发布一次事件，再下发总线返回的 frames。

**Tech Stack:** Python 3、`unittest`、现有 TLV 协议编码器、现有 `server.py` 人物状态计算函数。

**Spec:** `docs/superpowers/specs/2026-09-06-character-update-bus-design.md`

## Global Constraints

- 总线必须是同步、进程内实现；不引入后台线程、异步队列或跨进程消息系统。
- 依赖方向固定为 `server.py -> character_update_bus.py`；`character_update_bus.py` 不得 import `server.py`。
- 总线不持有 `StreamWriter`、`GameCipher`、连接锁或用户会话。
- 总线只读取最终角色状态并构建刷新结果，不修改角色存档。
- `equipment_attributes[0]` 继续作为攻击加成，`[1]` 继续作为防御加成；`[2]`、`[3]` 不赋予新语义。
- 完整人物刷新继续使用现有 `1017 + 1039/action=1` 协议链。
- 登录选角 `1080` 保持直接读取当前角色装备状态，不接入运行期总线。
- 直接修改 `master`，不创建功能分支或 PR。

---

### Task 1: 新增独立人物状态更新总线

**Files:**
- Create: `implementation_staging/character_update_bus.py`
- Create: `implementation_staging/tests/test_character_update_bus.py`

**Interfaces:**
- Produces: `CharacterUpdateEvent`
- Produces: `CharacterUpdateResult`
- Produces: `CharacterUpdateBus.__init__(build_full_refresh, build_appearance_refresh, is_item_equipped)`
- Produces: `CharacterUpdateBus.publish(event, *, role, registry, item_id=None) -> CharacterUpdateResult`
- Constraint: 模块不得 import `server`

- [ ] **Step 1: 写总线 RED 测试**

在 `tests/test_character_update_bus.py` 先只依赖新模块，使用假的刷新构建器验证事件路由：

```python
import importlib
import sys
import unittest

from character_update_bus import (
    CharacterUpdateBus,
    CharacterUpdateEvent,
)


class CharacterUpdateBusTests(unittest.TestCase):
    def setUp(self):
        self.calls = []

        def full(role, registry):
            self.calls.append(('full', role['id']))
            return (b'full-1017', b'full-1039')

        def appearance(role, registry):
            self.calls.append(('appearance', role['id']))
            return (b'appearance-1017',)

        def equipped(role, item_id):
            return any(
                int(item.get('id', 0)) == int(item_id)
                and item.get('location') == 'equipped'
                for item in role.get('items', [])
            )

        self.bus = CharacterUpdateBus(full, appearance, equipped)
        self.role = {'id': 10001, 'items': []}
        self.registry = object()

    def test_equipment_changed_builds_full_refresh(self):
        result = self.bus.publish(
            CharacterUpdateEvent.EQUIPMENT_CHANGED,
            role=self.role,
            registry=self.registry,
        )
        self.assertEqual(result.frames, (b'full-1017', b'full-1039'))
        self.assertEqual(result.refresh_scope, ('appearance', 'attributes'))

    def test_strengthened_bag_item_returns_empty_frames(self):
        self.role['items'] = [{'id': 7, 'location': 'bag'}]
        result = self.bus.publish(
            CharacterUpdateEvent.EQUIPMENT_STRENGTHENED,
            role=self.role,
            registry=self.registry,
            item_id=7,
        )
        self.assertEqual(result.frames, ())
        self.assertEqual(self.calls, [])

    def test_strengthened_equipped_item_builds_full_refresh(self):
        self.role['items'] = [{'id': 7, 'location': 'equipped'}]
        result = self.bus.publish(
            CharacterUpdateEvent.EQUIPMENT_STRENGTHENED,
            role=self.role,
            registry=self.registry,
            item_id=7,
        )
        self.assertEqual(result.frames, (b'full-1017', b'full-1039'))

    def test_level_and_stats_changes_build_full_refresh(self):
        for event in (
            CharacterUpdateEvent.CHARACTER_LEVEL_CHANGED,
            CharacterUpdateEvent.CHARACTER_STATS_CHANGED,
        ):
            result = self.bus.publish(event, role=self.role, registry=self.registry)
            self.assertEqual(result.frames, (b'full-1017', b'full-1039'))

    def test_appearance_changed_builds_only_appearance_refresh(self):
        result = self.bus.publish(
            CharacterUpdateEvent.CHARACTER_APPEARANCE_CHANGED,
            role=self.role,
            registry=self.registry,
        )
        self.assertEqual(result.frames, (b'appearance-1017',))

    def test_unknown_event_raises(self):
        with self.assertRaises(ValueError):
            self.bus.publish('unknown.event', role=self.role, registry=self.registry)

    def test_strengthened_requires_item_id(self):
        with self.assertRaises(ValueError):
            self.bus.publish(
                CharacterUpdateEvent.EQUIPMENT_STRENGTHENED,
                role=self.role,
                registry=self.registry,
            )

    def test_module_does_not_import_server(self):
        sys.modules.pop('character_update_bus', None)
        module = importlib.import_module('character_update_bus')
        self.assertNotIn('server', module.__dict__)
```

- [ ] **Step 2: 运行 RED 测试**

Run:

```bash
cd implementation_staging
python -m unittest discover -s tests -p 'test_character_update_bus.py' -v
```

Expected: FAIL/ERROR，因为 `character_update_bus.py` 尚不存在。

- [ ] **Step 3: 写最小总线实现**

`character_update_bus.py` 使用标准库即可：

```python
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Callable


class CharacterUpdateEvent(str, Enum):
    EQUIPMENT_CHANGED = 'equipment.changed'
    EQUIPMENT_STRENGTHENED = 'equipment.strengthened'
    CHARACTER_LEVEL_CHANGED = 'character.level_changed'
    CHARACTER_STATS_CHANGED = 'character.stats_changed'
    CHARACTER_APPEARANCE_CHANGED = 'character.appearance_changed'


@dataclass(frozen=True)
class CharacterUpdateResult:
    event: CharacterUpdateEvent
    frames: tuple[bytes, ...]
    refresh_scope: tuple[str, ...]


class CharacterUpdateBus:
    def __init__(
        self,
        build_full_refresh: Callable[[dict[str, object], object], tuple[bytes, ...]],
        build_appearance_refresh: Callable[[dict[str, object], object], tuple[bytes, ...]],
        is_item_equipped: Callable[[dict[str, object], int], bool],
    ) -> None:
        self._build_full_refresh = build_full_refresh
        self._build_appearance_refresh = build_appearance_refresh
        self._is_item_equipped = is_item_equipped

    def publish(
        self,
        event: CharacterUpdateEvent | str,
        *,
        role: dict[str, object],
        registry: object,
        item_id: int | None = None,
    ) -> CharacterUpdateResult:
        try:
            normalized = event if isinstance(event, CharacterUpdateEvent) else CharacterUpdateEvent(event)
        except ValueError as exc:
            raise ValueError(f'unsupported character update event: {event!r}') from exc

        if normalized is CharacterUpdateEvent.EQUIPMENT_STRENGTHENED:
            if item_id is None:
                raise ValueError('equipment.strengthened requires item_id')
            if not self._is_item_equipped(role, int(item_id)):
                return CharacterUpdateResult(normalized, (), ())
            return CharacterUpdateResult(
                normalized,
                tuple(self._build_full_refresh(role, registry)),
                ('appearance', 'attributes'),
            )

        if normalized in {
            CharacterUpdateEvent.EQUIPMENT_CHANGED,
            CharacterUpdateEvent.CHARACTER_LEVEL_CHANGED,
            CharacterUpdateEvent.CHARACTER_STATS_CHANGED,
        }:
            return CharacterUpdateResult(
                normalized,
                tuple(self._build_full_refresh(role, registry)),
                ('appearance', 'attributes'),
            )

        if normalized is CharacterUpdateEvent.CHARACTER_APPEARANCE_CHANGED:
            return CharacterUpdateResult(
                normalized,
                tuple(self._build_appearance_refresh(role, registry)),
                ('appearance',),
            )

        raise ValueError(f'unsupported character update event: {normalized!r}')
```

- [ ] **Step 4: 运行 GREEN 测试与导入检查**

```bash
cd implementation_staging
python -m py_compile character_update_bus.py
python -m unittest discover -s tests -p 'test_character_update_bus.py' -v
```

Expected: 全部 PASS。

- [ ] **Step 5: Commit**

```bash
git add implementation_staging/character_update_bus.py implementation_staging/tests/test_character_update_bus.py
git commit -m 'feat: add character update bus'
```

---

### Task 2: 将装备切换、卸下和丢弃接入总线

**Files:**
- Modify: `implementation_staging/server.py`
- Modify: `implementation_staging/tests/test_character_update_bus.py`
- Modify: `implementation_staging/tests/test_character_equipment_refresh.py`

**Interfaces:**
- Consumes: `CharacterUpdateBus`, `CharacterUpdateEvent`
- Produces: `is_role_item_equipped(role, item_id) -> bool`
- Produces: `build_character_update_bus() -> CharacterUpdateBus`
- Runtime owner: `LocalGameServer.character_update_bus`

- [ ] **Step 1: 写同槽位替换 RED 测试**

新增真实 `server.py` 计算链测试。测试必须明确模拟“先卸 A、再装 B、最后发布一次”的最终状态：

```python
from protocol import decode_frame, field_values
from server import (
    Settings,
    build_character_update_bus,
    combat_stats,
    default_role,
    effective_character_stats,
    item_slot,
    role_items,
)
from character_update_bus import CharacterUpdateEvent


def _slot_items(role, settings, slot):
    return [
        item for item in role_items(role)
        if item_slot(item, settings.item_registry) == slot
    ]


class CharacterEquipmentSwitchBusTests(unittest.TestCase):
    def test_weapon_a_to_b_uses_only_new_attack(self):
        settings = Settings()
        role = default_role(settings)
        weapons = _slot_items(role, settings, 10)
        first = weapons[0]
        second = dict(first)
        second['id'] = max(int(item['id']) for item in role_items(role)) + 1
        second['equipment_attributes'] = [25, 0, 0, 0]
        role_items(role).append(second)
        first['equipment_attributes'] = [10, 0, 0, 0]
        first['location'] = 'equipped'

        base_attack = max(0, int(role['stats'][0]))
        first['location'] = 'bag'
        second['location'] = 'equipped'
        result = build_character_update_bus().publish(
            CharacterUpdateEvent.EQUIPMENT_CHANGED,
            role=role,
            registry=settings.item_registry,
        )

        self.assertEqual(effective_character_stats(role, settings.item_registry)[0], base_attack + 25)
        self.assertNotEqual(effective_character_stats(role, settings.item_registry)[0], base_attack + 35)
        self.assertEqual(combat_stats(role, settings.item_registry).physical_attack, 10 + base_attack + 25)
        self.assertEqual([decode_frame(frame)[0] for frame in result.frames], [1017, 1039])

    def test_armor_a_to_b_uses_only_new_defence(self):
        settings = Settings()
        role = default_role(settings)
        armors = _slot_items(role, settings, 3)
        first = armors[0]
        second = dict(first)
        second['id'] = max(int(item['id']) for item in role_items(role)) + 1
        first['equipment_attributes'] = [0, 7, 0, 0]
        second['equipment_attributes'] = [0, 12, 0, 0]
        role_items(role).append(second)
        first['location'] = 'bag'
        second['location'] = 'equipped'
        base_defence = max(0, int(role['stats'][1]))

        build_character_update_bus().publish(
            CharacterUpdateEvent.EQUIPMENT_CHANGED,
            role=role,
            registry=settings.item_registry,
        )

        self.assertEqual(effective_character_stats(role, settings.item_registry)[1], base_defence + 12)
        self.assertEqual(combat_stats(role, settings.item_registry).physical_defence, base_defence + 12)
```

- [ ] **Step 2: 运行测试确认缺少 server 适配器**

```bash
cd implementation_staging
python -m unittest discover -s tests -p 'test_character_update_bus.py' -v
```

Expected: FAIL，因为 `build_character_update_bus` 尚不存在。

- [ ] **Step 3: 在 server.py 添加单向适配器**

在 import 区新增：

```python
from character_update_bus import CharacterUpdateBus, CharacterUpdateEvent
```

在 `character_equipment_refresh_frames()` 和 `equipment_panel_refresh_frame()` 定义之后、`LocalGameServer` 使用之前新增：

```python
def is_role_item_equipped(role: dict[str, object], item_id: int) -> bool:
    return any(
        int(item.get('id', 0)) == int(item_id)
        and item.get('location') == 'equipped'
        for item in role_items(role)
    )


def build_character_update_bus() -> CharacterUpdateBus:
    return CharacterUpdateBus(
        build_full_refresh=character_equipment_refresh_frames,
        build_appearance_refresh=lambda role, registry: (
            equipment_panel_refresh_frame(role, registry),
        ),
        is_item_equipped=is_role_item_equipped,
    )
```

`LocalGameServer.__init__` 增加：

```python
self.character_update_bus = build_character_update_bus()
```

- [ ] **Step 4: 把装备 action=5 改为发布一次最终状态事件**

保留现有同槽旧装备先移回 bag、再将新装备置为 `equipped` 的状态修改顺序；删除该分支对 `character_equipment_refresh_frames()` 的直接调用，替换成：

```python
refresh = self.character_update_bus.publish(
    CharacterUpdateEvent.EQUIPMENT_CHANGED,
    role=active_role,
    registry=self.settings.item_registry,
)
updates.extend(refresh.frames)
```

关键检查：调用必须位于“所有同槽旧装备已经 `location='bag'`、新装备已经 `location='equipped'`”之后，并且一个 action=5 只 publish 一次。

- [ ] **Step 5: 把卸下 action=6 和丢弃已装备物品改为总线事件**

卸下成功后：

```python
refresh = self.character_update_bus.publish(
    CharacterUpdateEvent.EQUIPMENT_CHANGED,
    role=active_role,
    registry=self.settings.item_registry,
)
replies.extend(refresh.frames)
```

丢弃分支仅当被丢物品在操作前属于装备时发布 `EQUIPMENT_CHANGED`。先保存布尔值：

```python
was_equipped = item.get('location') == 'equipped'
```

状态删除完成后再 publish，避免总线读取到旧状态。

- [ ] **Step 6: GREEN 验证**

```bash
cd implementation_staging
python -m py_compile server.py character_update_bus.py
python -m unittest discover -s tests -p 'test_character_update_bus.py' -v
python -m unittest discover -s tests -p 'test_character_equipment_refresh.py' -v
```

Expected: 全部 PASS；同槽 A→B 攻击/防御只保留 B。

- [ ] **Step 7: Commit**

```bash
git add implementation_staging/server.py implementation_staging/tests/test_character_update_bus.py implementation_staging/tests/test_character_equipment_refresh.py
git commit -m 'refactor: route equipment changes through update bus'
```

---

### Task 3: 强化和升级接入总线

**Files:**
- Modify: `implementation_staging/server.py`
- Modify: `implementation_staging/tests/test_character_update_bus.py`
- Modify: `implementation_staging/tests/test_character_equipment_refresh.py`
- Test existing: `implementation_staging/tests/test_strengthening.py`

**Interfaces:**
- Consumes: `CharacterUpdateEvent.EQUIPMENT_STRENGTHENED`
- Consumes: `CharacterUpdateEvent.CHARACTER_LEVEL_CHANGED`

- [ ] **Step 1: 写强化背包/已装备 RED 集成测试**

在现有强化刷新测试旁补充两种状态：

```python
def test_strengthening_bag_weapon_does_not_append_character_refresh(self):
    settings = server_module.Settings()
    role = server_module.default_role(settings)
    weapon = next(
        item for item in server_module.role_items(role)
        if server_module.item_slot(item, settings.item_registry) == 10
    )
    stone = next(
        item for item in server_module.role_items(role)
        if int(item.get('template_id', 0)) == INITIAL_STRENGTHEN_STONE_TEMPLATE_ID
    )
    weapon['location'] = 'bag'
    server_module.ensure_weapon_base_attributes(weapon, settings.item_registry)
    game_server = server_module.LocalGameServer(settings)
    game_server.roles.save = lambda: None

    frames = game_server.handle_strengthening_request(
        role,
        [92, int(weapon['id']), int(stone['id']), 5],
        rng=_AlwaysSuccessRng(),
    )

    self.assertNotEqual([decode_frame(frame)[0] for frame in frames][-2:], [1017, 1039])
```

保留已有“已装备武器强化最后追加 `[1017, 1039]`”测试。

- [ ] **Step 2: 修改 handle_strengthening_request**

强化前解析实际目标 `item_id`：

```python
item_id = int(values[1]) if len(values) > 1 else 0
```

`result.changed` 时保存成功后，不再直接调用 `character_equipment_refresh_frames()`，改为：

```python
refresh = self.character_update_bus.publish(
    CharacterUpdateEvent.EQUIPMENT_STRENGTHENED,
    role=role,
    registry=self.settings.item_registry,
    item_id=item_id,
)
return (*result.frames, *refresh.frames)
```

这样强化背包武器时 `frames=()`；强化当前装备时仍实时刷新属性。

- [ ] **Step 3: 将手动升级 1129/action=3 接入 level_changed**

`apply_one_level(active_role)` 返回 True 后，先构建：

```python
refresh = self.character_update_bus.publish(
    CharacterUpdateEvent.CHARACTER_LEVEL_CHANGED,
    role=active_role,
    registry=self.settings.item_registry,
)
```

保存成功后，在原有 `battle_progress_frame(active_role)` / `level_up_effect_frame(active_role)` 后追加 `*refresh.frames`，确保 HP/MP 和人物属性面板立即重绘。

- [ ] **Step 4: 将战斗奖励导致的自动升级接入 level_changed**

现有奖励链已有 `level_up` 布尔值。仅当 `level_up` 为 True 时发布一次：

```python
refresh = self.character_update_bus.publish(
    CharacterUpdateEvent.CHARACTER_LEVEL_CHANGED,
    role=active_role,
    registry=self.settings.item_registry,
)
result_frames.extend(refresh.frames)
```

不要在 `apply_one_level()` 内部直接 publish，因为该函数没有网络/registry 边界，而且自动升级循环可能一次连升多级；应在最终等级状态确定后只发布一次。

- [ ] **Step 5: 运行强化、升级和刷新测试**

```bash
cd implementation_staging
python -m unittest discover -s tests -p 'test_character_update_bus.py' -v
python -m unittest discover -s tests -p 'test_character_equipment_refresh.py' -v
python -m unittest discover -s tests -p 'test_strengthening.py' -v
python -m unittest discover -s tests -p 'test_level_progression.py' -v
```

如果仓库没有 `test_level_progression.py`，使用包含 `apply_one_level` / `battle_progress_frame` 的现有测试文件，而不是创建一个空壳测试文件。

Expected: 新增测试全部 PASS；原有强化规则继续 PASS。

- [ ] **Step 6: Commit**

```bash
git add implementation_staging/server.py implementation_staging/tests/test_character_update_bus.py implementation_staging/tests/test_character_equipment_refresh.py
git commit -m 'refactor: publish strengthening and level updates'
```

---

### Task 4: 收口业务直调并做完整回归

**Files:**
- Modify only if needed: `implementation_staging/server.py`
- Test: `implementation_staging/tests/test_character_update_bus.py`
- Test existing: appearance / strengthening suites

**Interfaces:**
- Requirement: 装备、卸下、替换、丢弃已装备物、强化、明确等级变化业务分支不再直接调用 `character_equipment_refresh_frames()`。
- Compatibility: `character_equipment_refresh_frames()` 本身保留，作为总线的 `build_full_refresh` 回调和现有测试入口。

- [ ] **Step 1: 搜索剩余直调**

```bash
cd implementation_staging
grep -n "character_equipment_refresh_frames(" server.py
```

Expected: 只允许看到函数定义、`build_character_update_bus()` 注入位置，以及确有兼容理由的非业务调用；装备/卸下/强化/升级业务分支不能直接调用。

- [ ] **Step 2: 记录完整测试基线**

```bash
cd implementation_staging
set +e
python -m unittest discover -s tests -v > /tmp/character-bus-before.log 2>&1
status=$?
set -e
grep -E ' \.\.\. (FAIL|ERROR)$' /tmp/character-bus-before.log | sort > /tmp/character-bus-before-failures.txt || true
cat /tmp/character-bus-before-failures.txt
```

这里的“before”应取实施前 master 基线；如果执行环境是在任务实施后才启动，必须先基于实施起点 commit 运行一次或使用已保存的实施前基线，不能把新的失败当历史失败。

- [ ] **Step 3: 跑专项回归**

```bash
cd implementation_staging
python -m py_compile server.py character_update_bus.py
python -m unittest discover -s tests -p 'test_character_update_bus.py' -v
python -m unittest discover -s tests -p 'test_character_equipment_refresh.py' -v
python -m unittest discover -s tests -p 'test_strengthening.py' -v
python -m unittest discover -s tests -p 'test_weapon_appearance_consistency.py' -v
python -m unittest discover -s tests -p 'test_armor_appearance_mapping.py' -v
python -m unittest discover -s tests -p 'test_armor_downlink.py' -v
python -m unittest discover -s tests -p 'test_helmet_appearance_mapping.py' -v
python -m unittest discover -s tests -p 'test_leg_armor_appearance_mapping.py' -v
python -m unittest discover -s tests -p 'test_shoe_appearance_mapping.py' -v
git diff --check
```

Expected: 所有专项 PASS。

- [ ] **Step 4: 完整测试前后失败差集**

```bash
cd implementation_staging
set +e
python -m unittest discover -s tests -v > /tmp/character-bus-after.log 2>&1
status=$?
set -e
grep -E ' \.\.\. (FAIL|ERROR)$' /tmp/character-bus-after.log | sort > /tmp/character-bus-after-failures.txt || true
comm -13 /tmp/character-bus-before-failures.txt /tmp/character-bus-after-failures.txt > /tmp/character-bus-new-failures.txt || true
cat /tmp/character-bus-new-failures.txt
test ! -s /tmp/character-bus-new-failures.txt
```

Expected: `/tmp/character-bus-new-failures.txt` 为空；历史失败可以继续存在，但本次不能新增失败。

- [ ] **Step 5: 最终代码检查**

确认：

```text
同槽装备 A -> B
A.location = bag
B.location = equipped
publish(equipment.changed) 只调用一次
  -> 1017 当前完整状态
  -> 1039/action=1 当前面板属性

强化装备中的物品
publish(equipment.strengthened, item_id)
  -> equipped: 1017 + 1039
  -> bag: frames=()

升级
最终 level 已更新
publish(character.level_changed) 一次
  -> 1017 + 1039
```

并确认 `combat_stats()` 仍按当前 `equipped` 集合即时计算，不缓存总线结果。

- [ ] **Step 6: Commit**

如果 Task 4 仅验证无代码变化，不创建空 commit；如有收口修改：

```bash
git add implementation_staging/server.py implementation_staging/tests/test_character_update_bus.py
git commit -m 'test: verify character update bus integration'
```

---

## Final Acceptance Checklist

- [ ] `character_update_bus.py` 可以独立 import，且没有 `import server`。
- [ ] 同槽武器 A(+10) -> B(+25) 后只保留 +25，不出现 +35。
- [ ] 同槽防具 A(+7) -> B(+12) 后只保留 +12。
- [ ] 装备、替换、卸下后立即返回 `1017 + 1039/action=1`。
- [ ] 强化当前装备立即更新人物属性；强化背包装备不刷新人物属性。
- [ ] 手动升级和战斗自动升级在最终等级确定后通过总线刷新一次。
- [ ] `character_panel_frames()`、`effective_character_stats()`、`combat_stats()` 均读取同一当前装备状态。
- [ ] `1080` 登录角色预览保持现有已修复结构，不经运行期总线。
- [ ] 专项测试全部通过。
- [ ] 完整测试相对实施前基线没有新增 FAIL/ERROR。
