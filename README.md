# 飘渺三界项目导航

目录核查日期：2026-09-12。本项目是《飘渺三界2》Android 客户端的本地 TCP 登录／游戏兼容服务，主体使用 Python；APK 补丁、地图资源和离线诊断工具与服务端共同维护。

> **开发前必读：**任何人工开发者或智能体在修改项目之前，必须先阅读根 `AGENTS.md` 和 `docs/development/APK_PROTOCOL_FIRST.md`，再读取目标目录的 `AGENTS.md`、相关协议证据与测试。所有修改都必须执行 APK Verification Gate；涉及客户端可观察行为的实现至少需要 B 级 APK 证据。

## 当前目录

```text
飘渺三界/
├─ implementation_staging/       实际开发与运行目录
│  ├─ server.py                  基础服务、角色存储、游戏逻辑与协议路由
│  ├─ server_dynamic_maps.py     动态地图及相关服务扩展
│  ├─ server_pets.py             基础宠物接入层
│  ├─ server_pet_system.py       当前启动脚本使用的集成入口
│  ├─ protocol.py               TCP 帧、字段类型、编码／解码
│  ├─ *_registry.py             各系统定义与资源注册表
│  ├─ *_service.py              各系统业务处理
│  ├─ *_protocol.py             各系统协议处理（另有 pet_protocol_core.py）
│  ├─ data/                     配置目录、资源目录、账号与角色运行数据
│  ├─ maps/                     地图源配置与地图二进制资源
│  ├─ materials/                地图和外观相关素材
│  ├─ tests/                    65 个 test_*.py 文件（不等于测试用例数）
│  ├─ test_client.py            TCP 集成测试客户端
│  ├─ tools/                    APK 补丁、地图生成、资源检查工具
│  ├─ references/               外观审计与资源证据
│  ├─ docs/                     模块说明与补充文档
│  ├─ build_artifacts/         APK、签名、构建中间产物和历史提取产物
│  ├─ logs/                    服务日志与 stdout/stderr 捕获文件
│  ├─ runtime/                 PID 与其他小型运行状态文件
│  ├─ 历史版本apk/              历史安装包
│  ├─ start_server.bat          Windows 启动入口
│  └─ restart_server.ps1        服务重启与进程管理
├─ resource_generator/          地图、角色和资源可视化／生成器项目
│  ├─ tools/characters/         角色外观诊断脚本
│  ├─ tools/maps/               后续地图可视化与编辑工具入口
│  └─ outputs/                  生成器默认输出目录
├─ docs/
│  ├─ development/             项目级开发规范与 APK-first 门禁
│  ├─ protocol/                协议结构、消息号、调用链与审计
│  ├─ diagnostics/             人物外观诊断图与结果
│  └─ superpowers/             功能设计 specs 与实施计划 plans
├─ .github/workflows/          任务系统相关自动化
└─ 项目级导航与自动化配置
```

## 入口与模块关系

启动链为 `start_server.bat → restart_server.ps1 → server_pet_system.py`。
集成入口先安装宠物支持与核心桥接，再调用 `server_dynamic_maps.main()`；扩展层依赖基础 `server.py`。
直接执行 `server.py` 与执行集成入口的功能范围不同。

| 领域 | 主要文件（位于 implementation_staging） |
| --- | --- |
| 网络、账号、角色、背包、战斗及综合路由 | `server.py`、`protocol.py` |
| 人物状态刷新 | `character_update_bus.py` |
| 物品、商店、强化、福缘 | `item_registry.py`、`systems/shop/`、`strengthening.py`、`fuyuan.py` |
| 地图 | `map_registry.py`、`map_o.py`、`dynamic_map_builder.py`、`server_dynamic_maps.py` |
| 门派与生活技能 | `sect_registry.py`、`life_skill_registry.py`、`life_skill_service.py` |
| 坐骑 | `mount_constructor.py`、`mount_protocol.py` |
| 宠物 | `pet_*.py`、`server_pets.py`、`server_pet_system.py` |
| 寄售 | `consignment_protocol.py`、`consignment_service.py` |
| 任务 | `task_registry.py`、`task_protocol.py`、`task_runtime.py`、`task_service.py`、`task_server_support.py` |

## 阅读顺序

1. `AGENTS.md`：全仓最高级智能体开发规则，任何修改前必读。
2. `docs/development/APK_PROTOCOL_FIRST.md`：APK 协议优先规范、A/B/C/D 证据等级和 Protocol Review 门禁。
3. `implementation_staging/AGENTS.md`：实现目录的开发约束与验证要求。
4. `implementation_staging/README.md`：功能说明、配置与手机测试。
5. `implementation_staging/PROTOCOL_LOCK.md` 和 `EQUIPMENT_RESOURCE_CATALOG.md`：协议与资源约束。
6. `docs/protocol/README.md`：协议文档索引。
7. 对应模块源码和 `implementation_staging/tests/` 中的测试。

`implementation_staging/OPENCODE_HANDOFF.md` 是历史交接资料，其中主目录路径和测试数量已过时；当前工作区及实际代码应作为目录与入口的依据。旧 README 中直接启动 `server.py` 的命令也不等同于当前集成启动流程。历史交接内容不得覆盖根 `AGENTS.md` 与 APK-first 开发规范。

## 当前整理事项

- 第一轮规范化已将日志、APK、签名和构建产物目标目录固定到 `logs/`、`runtime/` 与 `build_artifacts/`；历史根目录产物可按该规则归档。
- 资源可视化和生成器项目已独立为 `resource_generator/`，后续地图、角色等资源编辑能力优先在其中扩展。
- `server.py` 仍集中承载大量逻辑，功能模块已开始拆分，尚未形成统一 Python 包结构。
- 文档分布在根目录 `docs/`、主体 `docs/` 和主体顶层；本文件作为统一导航。
- 日志、APK、签名文件、缓存和多数构建产物已有 `.gitignore` 规则；忽略规则不会清理磁盘文件或取消已有跟踪。
- `data/` 混合静态定义与运行存档。整理时必须保留角色、账号及其他业务状态；不要整目录删除或覆盖。

本次仅核查布局并添加导航，未迁移源码、清理文件、重启服务或执行测试。功能是否通过测试及手机验收，不由本目录核查推断。
