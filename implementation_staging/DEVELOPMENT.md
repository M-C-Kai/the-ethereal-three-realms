# 开发规范

本目录是 Android 客户端当前使用的本地兼容服务器。改动应保持小步、可测试，并限定在本项目范围内。

## 事实来源

- 集成服务从 `server.py` 启动。启动时先物化动态地图（`materialize_all_dynamic_maps`），再装配全部系统并进入网络主循环。
- 本地运行使用 `start_server.bat` 或 `restart_server.ps1`。启动脚本会在 `logs/` 下写入一份带时间戳的标准输出日志和一份标准错误日志。
- `server.py` 只保留依赖装配、系统总线路由和网络收发；所有玩法协议入口位于 `systems/<name>/` 五层目录。
- 保持 `data/roles.json`、`data/accounts.json` 以及其他运行态数据文件完整。字段结构调整必须配迁移逻辑。
- 协议字段顺序和字段类型必须保持精确。即使数值能放下，byte、short、int 也不能随意互换。
- APK 包名和签名密钥必须稳定。本地重打包使用 `build_artifacts/signing/local-test-keystore.p12`。

## 目录职责

```text
implementation_staging/
├── app/                   应用层入口：系统路由、上下文、事件总线
├── systems/               按玩法/业务域拆分后的系统入口
├── protocol.py            字段编码/解码、帧格式、游戏阶段加密（共享基础层）
├── tests/                 单元测试、协议测试、迁移测试和契约测试
├── data/                  运行态数据和纳入版本管理的配置目录
├── maps/                  地图源 JSON 和生成后的地图资源
├── materials/             离线资源输入和渲染验证材料
├── tools/                 离线补丁、提取、审计工具
├── references/            客户端证据、资源审计和抓包参考
├── docs/                  本实现目录内的说明文档
├── logs/                  运行日志、stdout/stderr 捕获文件
├── build_artifacts/
│   ├── apk/               生成 APK、idsig、APK 校验和
│   ├── build/             APK 构建中间产物
│   ├── signing/           本地测试签名材料
│   └── legacy/            历史提取构建产物
└── runtime/               服务 PID 等小型运行态文件
```

不要把新的日志、APK、idsig 或提取构建产物放到项目根目录。新增生成文件应按用途放入 `logs/`、`runtime/` 或 `build_artifacts/`。

日志文件命名规范：

```text
logs/server.YYYYMMDD-HHMMSS.stdout.log
logs/server.YYYYMMDD-HHMMSS.stderr.log
```

## 功能模块布局（系统化拆分已完成）

全部玩法系统已迁入 `systems/<name>/` 五层目录，详见 `systems/README.md` 的系统清单：

```text
systems/<name>/
├── handler.py      系统协议入口，注册到 SystemRouter（can_handle / handle）
├── service.py      业务规则和状态流转
├── protocol.py     编码、解码和协议字段辅助函数
├── registry.py     静态目录加载与校验
└── events.py       需要发布或订阅的事件名
```

`server.py` 只保留三类职责：

1. **依赖装配** —— `Settings` 读取配置并加载目录；`LocalGameServer.__init__` 实例化全部系统并注入依赖（存储、刷新总线、任务事件回调、寄售对话钩子等）。
2. **系统总线路由** —— 每条消息构造 `app.context.SystemContext` 后交 `app.router.SystemRouter.dispatch`，由唯一系统处理。
3. **网络收发** —— asyncio TCP 帧收发、加密、1012 心跳、在线连接登记、会话令牌与断线清理。

跨系统协作一律通过装配期注入的依赖完成（例如地图系统持有战斗系统的遭遇战入口、任务事件回调、寄售对话钩子）；不要在系统之间直接 import 对方的 handler。跨系统的连接级状态存放在连接会话字典中，由所属系统读写。

原 `server_pet_system.py` / `server_pets.py` / `server_dynamic_maps.py` 的 monkey-patch 兼容层已拆除；新增功能不得再引入 monkey patch。

## 验证

在 `implementation_staging/` 目录运行统一测试套件（覆盖架构边界、各系统协议帧与业务流）：

```powershell
D:\python\python.exe -m unittest discover -s tests -v
```

如果改动影响网络流程，先确认单元测试通过，再重启本地服务并运行：

```powershell
D:\python\python.exe test_client.py --host 127.0.0.1 --port 6805 --exercise-role-crud
```

不要把 6805 端口暴露到本地网络以外。
