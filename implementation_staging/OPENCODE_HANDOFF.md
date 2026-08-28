# OpenCode 项目交接说明

更新时间：2026-08-25

## 1. 项目目标

这是《飘渺三界2》Android 客户端的纯本地登录/游戏服兼容原型。目标是逐步补齐客户端已经存在的玩法协议，让手机只连接局域网内的本地服务。不要访问、扫描、修改或尝试登录任何官方/第三方服务器。

当前可用链路：

`登录 -> 本地一区 -> 角色列表 -> 创建/删除角色 -> 进入地图 -> 1126 试炼妖兽实体 -> 背包 -> 人物四页面板 -> 装备/卸下/使用物品`

## 2. 规范工作目录

```text
C:\Users\Kail\Documents\Codex\2026-08-24\new-chat\outputs\piaomiao_local_login
```

这里是继续开发的唯一主目录。不要直接在反编译目录里实现服务端功能。

重要外部参考：

```text
原始 APK：C:\Users\Kail\Downloads\base.apk.1
另一份 APK：C:\Users\Kail\Downloads\base.apk
原始 JAR：C:\Users\Kail\Downloads\飘渺三界.jar
完整反编译：C:\Users\Kail\Documents\Codex\2026-08-24\new-chat\work\apk-initial-role-reference
当前 APK 反编译/补丁目录：C:\Users\Kail\Documents\Codex\2026-08-24\new-chat\work\apk-person-panel
解出的图片：C:\Users\Kail\Documents\Codex\2026-08-24\new-chat\work\initial-apk-images\rebuilt
```

## 3. 源码结构

| 文件 | 作用 |
|---|---|
| `server.py` | asyncio TCP 登录服和游戏服，协议路由、角色、物品、心跳、地图流程 |
| `protocol.py` | 字段编码/解码、帧格式、客户端游戏阶段加密 |
| `map_o.py` | `.map.o` 解析、序列化和 RLE |
| `config.json` | 监听地址、手机跳转地址、地图和角色数据路径 |
| `test_client.py` | 两次真实 TCP 连接的端到端客户端 |
| `tests/` | 无网络单元测试，当前应为 16 项 |
| `tools/` | APK 端点补丁、人物快捷键补丁、地图生成与渲染工具 |
| `maps/` | 当前可运行的 58 号地图及实验地图 |
| `EQUIPMENT_RESOURCE_CATALOG.md` | 装备槽位、图标与角色外观资源结论 |
| `MAP_O_GENERATOR.md` | 地图逻辑文件格式与生成方法 |

## 4. 已实现协议

- `1077` 登录与服务器列表。
- `1051 -> 1052` 选服跳转和游戏阶段加密。
- `1080` 角色列表、推荐名、创建、删除、选择角色。
- `1006` 完整人物属性表（0～84）。
- `1089` 人物基础页扩展资料空集合初始化。
- `1132` 人物技能容器初始化。
- `1039` 人物属性页和神通页基础数据。
- `1008/1009/1032` 物品下发、说明、详情、装备、卸下、使用和丢弃。
- `1123/1110/1010/1407` 地图初始化、地图逻辑数据和进入流程。
- `1126` subtype 0 的地图通用实体列表；当前本地服进入地图时放置一个可由 APK 原始资源渲染的怪物实体。
- `2031` 当前 APK 的通用地图对象交互；服务端已记录妖兽对象请求并保留 `1010/7` 旧客户端兼容分支。妖兽触碰现在进入连接内的最小本地战斗探针：先发 `1040/action=0` 创建战斗界面，再发 `1040/action=1` 首回合；客户端 `1041` 命令触发 `1042` 普攻记录和 `1040/action=2` 回合推进，十次攻击后 `1040/action=4` 结束；正式参与者属性/技能伤害/掉落仍未实现，静态证据见 `APK_BATTLE_CATALOG.md`。
- `1012` 心跳，防止客户端约 90 秒后退回首页。
- 主菜单预取 `1403/1090/1153/1061` 的安全空应答。

## 5. 已确认的协议陷阱

1. 协议字段类型必须与客户端读取方法完全一致，`byte/short/int/string/binary` 不能只按数值大小替换。
2. `1008` 第 12 字段是图标编号；模板号末位是品质；装备位置由独立的位置字节决定。
3. 装备位置 `1..14` 依次为头盔、肩甲、铠甲、腰带、腿甲、项链、披风、护腕、鞋子、武器、戒指、外套、饰品、法宝。背包是 50，仓库是 51。
4. 人物属性 `14..20/22/26` 是独立的角色叠加资源，不是装备模板号。尤其属性 22 的 `40000/410xx` 是坐骑/变身，不能当武器外观。
5. 背包分组 100 只能放装备子类；普通道具放入该组会冻结 UI。当前普通道具使用分组 150。
6. 打开人物/主菜单时客户端会主动预取多个未实现系统。未知系统应先返回已验证的安全空应答，不要猜复杂字段。
7. `58.map.o` 是目前唯一确认可运行的地图逻辑资源；配置名称虽然是仙石村，但它不是原服完整的 50000 号仙石村。

## 6. 推荐的后续顺序

一次只实现一个可从手机验证的闭环：

1. 完善装备属性计算：装备/卸下后重算人物面板数值，并补充对应的属性更新帧。
2. 背包扩展：堆叠、拆分、合并、整理、仓库。
3. NPC 与对话：在已验证的 1126 实体基础上实现点击、对话和商店的最小闭环。
4. 任务系统：接取、状态保存、完成、奖励。
5. 战斗最小闭环：目标、普通攻击、伤害、死亡与复活。
6. 技能、队伍、宠物、聊天等独立系统。
7. 只有取得真实 `50000.map.ref/.map.o` 或可靠协议样本后，再继续完整仙石村复原。

每个阶段都应：先从 smali/JAR 确认请求字段和响应字段，再添加编码函数和测试，最后让手机验证。不要根据消息号名称猜字段。

## 7. 开发与验证命令

核心服务只使用 Python 标准库。当前机器可用：

```powershell
cd C:\Users\Kail\Documents\Codex\2026-08-24\new-chat\outputs\piaomiao_local_login
D:\python\python.exe -m unittest discover -s tests -v
D:\python\python.exe server.py
```

服务运行后执行真实协议测试：

```powershell
D:\python\python.exe test_client.py --host 127.0.0.1 --port 6805 --exercise-role-crud
D:\python\python.exe test_client.py --host 127.0.0.1 --port 6805 --hold-seconds 120
```

地图图片工具额外需要 Pillow：

```powershell
D:\python\python.exe -m pip install -r requirements-tools.txt
```

不要同时启动两个 6805 服务。修改服务端后，应停止旧 PID、隐藏窗口启动新进程，并确认日志第一行显示：

```text
listening on ('0.0.0.0', 6805); advertising 192.168.0.104:6805
```

## 8. 数据与 APK 注意事项

- `data/roles.json` 是手机测试存档；改数据结构时必须向后迁移，不能直接覆盖或删除。
- 手机测试只使用临时账号密码，协议会明文传输凭据。
- 当前手机使用的 APK 是 `piaomiao_local_login.apk`。普通服务端改动不需要重新安装 APK。
- 只有修改客户端 smali 或电脑 IP 时才重建 APK。
- 覆盖安装必须继续使用原目录的 `local-test-keystore.p12`，否则 Android 会拒绝覆盖。
- 不要把 6805 暴露到公网。

## 9. 交给 OpenCode 的建议首条指令

```text
请先完整阅读 AGENTS.md、OPENCODE_HANDOFF.md、README.md、EQUIPMENT_RESOURCE_CATALOG.md，运行 14 项单元测试和 test_client.py，确认现状后再修改。一次只实现一个手机可验证的协议闭环。所有字段必须从 references/smali、完整反编译目录或 JAR 中取得证据，不要猜协议；保留 data/roles.json，完成后重启最新服务并告诉我手机端怎么测试。
```
