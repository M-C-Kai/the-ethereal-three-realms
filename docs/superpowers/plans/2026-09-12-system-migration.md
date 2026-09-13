# 系统化迁移实施计划

> **状态（2026-09-13）：已全部完成。** 六大核心系统（商店、技能、地图、角色、背包、战斗）及任务、帮派、宠物、寄售、福缘均已迁入 `systems/<name>/` 五层目录；`server.py` 只保留依赖装配、系统总线路由和网络收发；宠物/动态地图 monkey-patch 兼容层已拆除；根级旧模块已删除。现状以 `systems/README.md` 为准。

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**目标：** 按商店、技能、地图、角色、背包、战斗的顺序，把 `implementation_staging/server.py` 中的协议入口逐步迁移到 `implementation_staging/systems/<name>/`，由 `app.router.SystemRouter` 统一分发。

**架构：** 系统目录先建立窄入口 `handler.py`，统一提供系统类和 `register_*_routes()`。已有 registry/service/protocol 的系统先迁入口，深耦合系统先建立边界和测试，再分批抽离业务逻辑。

**技术栈：** Python 标准库、`unittest`、现有协议编码模块、`app.router.SystemRouter`、`app.context.SystemContext`。

**Spec：** 用户要求“按顺序开始迁移，区分商店系统、技能系统、地图系统、角色系统、背包系统、战斗系统”。

## 全局约束

- 文档输出使用中文。
- 不改变协议字段顺序和字段类型。
- 不删除 `server.py` 的兼容入口，直到对应系统路由测试覆盖完整入口。
- 每个系统迁移先写失败测试，再实现最小代码。
- 运行验证必须至少覆盖本轮新增测试、已迁移系统的既有测试和 Python 编译检查。

---

### Task 1: 建立六个系统边界

**Files:**
- Create: `implementation_staging/systems/shop/__init__.py`
- Create: `implementation_staging/systems/shop/handler.py`
- Create: `implementation_staging/systems/skill/__init__.py`
- Create: `implementation_staging/systems/skill/handler.py`
- Create: `implementation_staging/systems/map/__init__.py`
- Create: `implementation_staging/systems/map/handler.py`
- Create: `implementation_staging/systems/role/__init__.py`
- Create: `implementation_staging/systems/role/handler.py`
- Create: `implementation_staging/systems/inventory/__init__.py`
- Create: `implementation_staging/systems/inventory/handler.py`
- Create: `implementation_staging/systems/battle/__init__.py`
- Create: `implementation_staging/systems/battle/handler.py`
- Test: `implementation_staging/tests/test_system_boundaries.py`
- Modify: `implementation_staging/systems/README.md`

**Interfaces:**
- Consumes: `app.router.SystemRouter.register(name, predicate, handler)`。
- Produces: 每个系统导出系统类和 `register_*_routes(router, system)`。

- [ ] **Step 1: 写失败测试**

```python
from systems.shop import ShopSystem, register_shop_routes
from systems.skill import SkillSystem, register_skill_routes
from systems.map import MapSystem, register_map_routes
from systems.role import RoleSystem, register_role_routes
from systems.inventory import InventorySystem, register_inventory_routes
from systems.battle import BattleSystem, register_battle_routes
```

- [ ] **Step 2: 运行测试确认失败**

Run: `D:\python\python.exe -m unittest tests.test_system_boundaries -v`
Expected: FAIL，提示缺少对应系统包或导出对象。

- [ ] **Step 3: 实现最小系统边界**

每个 `handler.py` 提供系统类、`system_name` 和注册函数。暂未迁移完整业务的系统注册函数可以只声明入口名，不处理消息。

- [ ] **Step 4: 运行测试确认通过**

Run: `D:\python\python.exe -m unittest tests.test_system_boundaries -v`
Expected: PASS。

### Task 2: 商店系统入口迁移

**Files:**
- Modify: `implementation_staging/systems/shop/handler.py`
- Modify: `implementation_staging/server.py`
- Test: `implementation_staging/tests/test_shop.py`

**Interfaces:**
- Consumes: `shop_registry.ShopRegistry` 和当前 `server.py` 中的商店协议辅助函数。
- Produces: 商店打开、商品列表、购买入口逐步走 `ShopSystem`。

- [ ] **Step 1: 写失败测试**

覆盖 `ShopSystem` 能识别商品列表请求和购买请求，并且非商店 1033 不被处理。

- [ ] **Step 2: 运行测试确认失败**

Run: `D:\python\python.exe -m unittest tests.test_shop -v`
Expected: FAIL，提示系统入口未实现。

- [ ] **Step 3: 最小迁移**

把 1033 商店列表和购买相关判断收敛到 `ShopSystem`，`server.py` 保留发送和日志。

- [ ] **Step 4: 运行测试确认通过**

Run: `D:\python\python.exe -m unittest tests.test_shop -v`
Expected: PASS。

### Task 3: 技能系统入口迁移

**Files:**
- Modify: `implementation_staging/systems/skill/handler.py`
- Modify: `implementation_staging/server.py`
- Test: `implementation_staging/tests/test_life_skills.py`
- Test: `implementation_staging/tests/test_life_skill_direct_use.py`

**Interfaces:**
- Consumes: `life_skill_registry.py`、`life_skill_service.py`。
- Produces: 生活技能列表、打开、配方、制作、采集入口逐步走 `SkillSystem`。

- [ ] **Step 1: 写失败测试**
- [ ] **Step 2: 运行测试确认失败**
- [ ] **Step 3: 最小迁移技能入口**
- [ ] **Step 4: 运行技能相关测试确认通过**

### Task 4: 地图系统入口迁移

**Files:**
- Modify: `implementation_staging/systems/map/handler.py`
- Modify: `implementation_staging/server.py`
- Test: `implementation_staging/tests/test_map_registry.py`
- Test: `implementation_staging/tests/test_map_o.py`
- Test: `implementation_staging/tests/test_dynamic_map_builder.py`

**Interfaces:**
- Consumes: `map_registry.py`、`map_o.py`、`dynamic_map_builder.py`。
- Produces: 地图寻路、地图进入、NPC/对象流式刷新逐步走 `MapSystem`。

- [ ] **Step 1: 写失败测试**
- [ ] **Step 2: 运行测试确认失败**
- [ ] **Step 3: 最小迁移地图寻路入口**
- [ ] **Step 4: 运行地图相关测试确认通过**

### Task 5: 角色、背包、战斗深耦合系统拆分

**Files:**
- Modify: `implementation_staging/systems/role/handler.py`
- Modify: `implementation_staging/systems/inventory/handler.py`
- Modify: `implementation_staging/systems/battle/handler.py`
- Modify: `implementation_staging/server.py`
- Test: `implementation_staging/tests/test_role_dat.py`
- Test: `implementation_staging/tests/test_inventory.py`
- Test: `implementation_staging/tests/test_battle_escape_guard.py`

**Interfaces:**
- Produces: 角色登录/创建/删除、背包物品使用/装备、战斗开始/结算逐步从 `server.py` 拆出。

- [ ] **Step 1: 按入口写失败测试**
- [ ] **Step 2: 每次只迁一个协议分支**
- [ ] **Step 3: 保留兼容方法直到测试完整覆盖**
- [ ] **Step 4: 运行对应系统测试和编译检查**
