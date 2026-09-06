# 人物装备刷新链设计

## 目标

统一角色登录预览、游戏内人物外观、人物属性面板与战斗属性对当前 `equipped` 装备状态的读取，避免装备后各界面依赖不同缓存或等待重登。

## 已确认协议证据

- APK `pmsj/work/main/e.K` 对 `1080/action=0` 的单角色 15 字段记录读取为：`role_id, level, property7, model, race*10+gender, name, slot, property2, property14..20`。
- APK `pmsj/work/main/e.O` 接收 `1017`，按 `role_id + property/value` 增量更新当前人物对象及依赖界面。
- APK `pmsj/work/main/e.ae` 的 `1039/action=1` 将后续属性数据交给人物属性页并调用 `ag()` 重绘。
- 现有 `1008 operation=3 + 1009 action=5/6` 仍是装备/卸下确认链，不改变字段类型和动作号。
- 当前强化逻辑会修改实例 `equipment_attributes`；实例字段会覆盖模板默认值。

## 设计

1. `role_list()` 直接从 `character_appearance(role, item_registry)` 生成 1080 登录人物预览，禁止再用 `role.stats` 填充外观字段。
2. 增加装备属性汇总函数，只统计 `location == "equipped"` 的装备实例。已确认字段语义仅使用：`equipment_attributes[0]` 作为攻击加成、`equipment_attributes[1]` 作为防御加成；第 2/3 项不赋予新语义。
3. 人物面板与战斗计算共享同一装备属性汇总。全量登录 `1006` 和实时 `1017/1039` 使用同一当前装备快照。
4. 新增统一 `character_equipment_refresh_frames()`：返回一帧完整当前人物 `1017`（外观 + 当前人物面板属性）和一帧 `1039/action=1` 属性面板刷新。
5. 装备、卸下、丢弃已装备物品、强化成功/失败导致装备属性改变后统一调用该刷新函数。
6. 不在游戏中重发 `1006`，避免重新初始化地图人物。
7. 不修改 APK、不修改存档结构、不删除 `data/roles.json`。

## 验收

- 1080 单角色 15 字段与 APK `e.K` 顺序一致。
- 装备/卸下后 1017 包含当前完整外观以及实时人物属性；1039/action=1 同步当前属性页。
- 已装备武器强化后，人物属性页和战斗攻击使用强化后的实例属性。
- 现有武器/铠甲/头盔/腿甲/鞋子外观映射与强化测试不回归。
- 真机验收由用户重启本地服务后执行；自动化验证不冒充真机结果。
