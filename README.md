# 飘渺三界

《飘渺三界2》Android 客户端的本地 TCP 登录/游戏兼容服务。主体使用 Python；APK 补丁、地图资源和离线诊断工具与服务端共同维护。

> **开发前必读：** 任何人工开发者或智能体在修改项目之前，必须先阅读根 `AGENTS.md` 和 `docs/development/APK_PROTOCOL_FIRST.md`，再读取目标目录的 `AGENTS.md`、相关协议证据与测试。所有修改都必须执行 APK Verification Gate；涉及客户端可观察行为的实现至少需要 B 级 APK 证据。

## 项目结构

```text
飘渺三界/
├── AGENTS.md                       全仓智能体开发规范（最高优先级）
├── README.md                       本文件
├── docs/                           项目级文档
│   ├── FUNCTION_MANUAL.md          功能手册：各模块功能与联动总览
│   ├── development/                开发规范与 APK 验证
│   │   ├── APK_PROTOCOL_FIRST.md   APK 协议优先开发规范
│   │   └── APK_VERIFICATION_*.md   具体协议验证记录
│   ├── protocol/                   协议文档
│   │   ├── 01~15                   通信架构、包结构、消息号、登录、战斗等
│   │   └──专题文档                  1008 装备块、1010 挂机、1138 寄售等
│   ├── diagnostics/                诊断文档
│   └── superpowers/                设计规格与实施计划
│       ├── specs/                  功能设计文档
│       └── plans/                  实施计划文档
├── implementation_staging/         实际开发与运行目录
│   ├── AGENTS.md                   实现目录开发约束与验证要求
│   ├── server.py                   依赖装配、系统总线路由、网络收发
│   ├── protocol.py                 TCP 帧格式、字段编码/解码、游戏加密
│   ├── app/                        应用框架（路由、上下文、通知）
│   │   ├── router.py               SystemRouter 总线分发
│   │   ├── context.py              SystemContext 连接级状态
│   │   └── notify.py               通知帧工具
│   ├── systems/                    按玩法域拆分的系统层（五层结构）
│   │   ├── role/                   角色：账号、登录、CRUD、面板、门派、邮件
│   │   ├── map/                    地图：地图数据、进入、实体刷新、传送、对话
│   │   ├── inventory/              背包：物品下发、装备/卸下/使用、强化
│   │   ├── battle/                 战斗：回合制、逃跑保护、结算、PvP
│   │   ├── skill/                  技能：生活技能、门派技能、采集
│   │   ├── task/                   任务：目录、接取、进度、奖励
│   │   ├── pet/                    宠物：目录、详情、技能、状态切换
│   │   ├── shop/                   商店：页签、商品、购买
│   │   ├── social/                 玩家交互：查看、私聊、交易、好友、PK
│   │   ├── team/                   组队：建队、邀请、跟随
│   │   ├── gang/                   帮派：目录、成员、职位
│   │   ├── consignment/            寄售：上架、下架、购买
│   │   ├── exchange/               交易所：挂单、交易
│   │   └── fuyuan/                 福缘：目录、结算、充值
│   ├── data/                       配置与运行数据
│   │   ├── roles.json              角色存档（运行时生成）
│   │   ├── accounts.json           账号数据
│   │   └── *.json                  其他静态/运行时数据
│   ├── maps/                       地图资源（map.o / map.ref）
│   ├── tests/                      统一测试套件
│   ├── test_client.py              TCP 集成测试客户端
│   ├── tools/                      APK 补丁、地图生成工具
│   ├── references/                 外观审计与资源证据
│   ├── build_artifacts/            APK、签名、构建产物
│   ├── logs/                       服务日志
│   ├── start_server.bat            Windows 启动入口
│   └── restart_server.ps1          服务重启脚本
├── resource_generator/             地图与资源可视化/生成器
│   ├── tools/characters/           角色外观诊断脚本
│   ├── tools/maps/                 地图可视化与编辑工具
│   └── outputs/                    生成器输出目录
└── .github/workflows/              CI 自动化
```

## 系统架构

### 三层职责

| 层 | 文件 | 职责 |
|---|---|---|
| 网络与装配 | `server.py` | 依赖装配、SystemRouter 总线分发、asyncio TCP 收发、心跳、断线清理 |
| 路由 | `app/router.py` | 按 MessageID 分发到唯一系统 handler |
| 玩法系统 | `systems/<name>/` | handler → service → protocol → registry → events 五层 |

### 系统五层结构

每个 `systems/<name>/` 包含：

| 文件 | 职责 |
|---|---|
| `handler.py` | 系统协议入口，路由注册（can_handle / handle） |
| `service.py` | 业务规则和状态流转 |
| `protocol.py` | 协议字段编码、解码和适配 |
| `registry.py` | 静态目录加载和校验 |
| `events.py` | 跨系统事件名和事件载荷定义 |

### 核心流程

```
登录 → 选服 → 加密初始化 → 角色列表 → 创建/选择角色
→ 地图初始化(map.o + 1407 分块) → 实体列表(1126)
→ 背包/面板/技能初始化 → 游戏循环
```

### 模块联动

- 装备物品 → CharacterUpdateBus → 角色属性重算 + 广播
- 点击妖兽 → 地图系统 → 战斗系统
- NPC 对话 → 任务系统 / 寄售系统
- 坐骑穿卸 → 背包 → 地图外观广播

详细联动关系见 `docs/FUNCTION_MANUAL.md`。

## 阅读顺序

1. `AGENTS.md` — 全仓最高级智能体开发规则
2. `docs/development/APK_PROTOCOL_FIRST.md` — APK 协议优先规范
3. `implementation_staging/AGENTS.md` — 实现目录开发约束
4. `implementation_staging/README.md` — 功能说明与配置
5. `docs/FUNCTION_MANUAL.md` — 各模块功能与联动总览
6. `docs/protocol/` — 协议文档
7. 对应模块源码和 `implementation_staging/tests/` 中的测试

## 开发与验证

```powershell
# 单元测试
cd implementation_staging
D:\python\python.exe -m unittest discover -s tests -v

# 端到端测试
D:\python\python.exe test_client.py --host 127.0.0.1 --port 6805 --exercise-role-crud
```
