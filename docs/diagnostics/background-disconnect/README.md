# 后台掉线诊断：为什么“一离开游戏就掉线、没有后台存活”

本目录保存“客户端切到后台后账号立即离线”的静态 APK 证据、服务端证据和日志证据。它不修改任何协议、服务端行为或客户端资源，只用于定位原因。

- 结论针对 `piaomiao_local_60011_scenery_border.apk`（2026-09-16 构建）与其同源的本地 APK 构建链。
- 真机复核状态：**pending real-device verification**（需要用户在目标手机上确认冻结/查杀哪一条路径为主）。

## 1. 结论摘要

| 编号 | 结论 | 证据等级 |
| --- | --- | --- |
| C1 | 客户端没有任何后台保活能力：清单里只有 2 个 Activity、**0 个 Service**，权限只有 `INTERNET` 与 `ACCESS_NETWORK_STATE`，没有 `FOREGROUND_SERVICE` / `WAKE_LOCK` / 前台服务声明。 | A |
| C2 | 客户端**没有**在生命周期里主动断线：`pmsj.work.main.MyMidlet` 直接继承 `android.app.Activity`，未重写 `onPause` / `onStop` / `onDestroy`。`javax.microedition.midlet.MIDlet` 里的空实现与它**没有继承关系**（那两个空方法不是本客户端的生命周期钩子）。 | A |
| C3 | 客户端判定“与服务器断开连接。”只靠一个 **90 秒收包看门狗**：`pmsj/work/main/i;->h:La/c/q`，超时值来自 `i;->g:I = 0x15f90`（90000 ms），在 `1052` 握手成功分支写入；渲染循环每帧检查，一旦超时就显示断线。收到任何消息时刷新。 | B |
| C4 | 服务端**不会主动踢人**：心跳循环只发 `1012`、不校验 pong、不跟踪失活；读循环 `reader.readexactly` 无限阻塞，只有对端 FIN/RST 时才走 `client disconnected` 分支。 | A |
| C5 | 因此“离开就掉线”不是服务端超时，而是**客户端进程在离开前台后被系统冻结/回收/主动退出**导致 socket 被关闭。服务端只是被动记录 EOF。 | B（日志 + C1/C4 推理；具体杀进程路径待真机确认） |
| C6 | 客户端存在显式退出路径 `MyMidlet.a()`：`finish()` + `System.exit(0)`，由各退出确认对话框调用；走这条路会**立刻**断开并杀掉进程。 | B |

## 2. 客户端静态证据（APK/反编译）

反编译目录（构建产物，不入库）：`implementation_staging/build_artifacts/build/apk_decoded/`。

### 2.1 清单：没有 Service、没有前台服务、targetSdk=7

`aapt2 dump xmltree --file AndroidManifest.xml build_artifacts/apk/piaomiao_local_60011_scenery_border.apk` 输出（节选）：

```text
E: manifest
  A: package="com.PiaoMiaoSanJie.PiaoMiaoSanJiejb"
  E: uses-sdk
    A: minSdkVersion=7
    A: targetSdkVersion=7
  E: uses-permission  name="android.permission.INTERNET"
  E: uses-permission  name="android.permission.ACCESS_NETWORK_STATE"
  E: application  (screenOrientation=5)
    E: activity  name="pmsj.work.main.MyMidlet"  (MAIN/LAUNCHER)
    E: activity  name="EditActivity"
```

- **没有任何 `<service>`、`android:foregroundServiceType`、`WAKE_LOCK`、`POST_NOTIFICATIONS`**；也没有 `android:persistent`（该属性仅系统应用有效）。
- 结果：应用一旦不在前台，就是一个普通 cached 进程，没有任何机制阻止 Android 12+ 的 cached-app freezer 冻结它，也没有机制阻止厂商电池管理/低内存回收直接杀掉它。
- `targetSdkVersion=7` 说明这个客户端是老 MIUI/MIDlet 移植版；它不会受到 Android 8+ 后台服务限制，但**也不会**因此获得免冻结保护，唯一可靠的保护是前台服务。

### 2.2 生命周期：客户端不主动断线

- `pmsj/work/main/MyMidlet.smali`：`.super Landroid/app/Activity;`，全文没有 `onPause()` / `onStop()` / `onDestroy()` / `onResume()`。
- `javax/microedition/midlet/MIDlet.smali` 里确实有空的 `onPause()/onStop()/onDestroy()/onResume()`，但 `MyMidlet` 不继承该类；这些空方法只属于未被本客户端使用的基类，不参与运行。
- 结论：切后台时客户端既不暂停游戏线程，也不发送登出或关闭 socket。掉线不是这里的代码造成的。

### 2.3 断线判定 = 90 秒收包看门狗

| 环节 | 位置 | 行为 |
| --- | --- | --- |
| 看门狗对象 | `pmsj/work/main/i;->h:La/c/q`（`La/c/q`：`d`=超时毫秒，`e`=最后活动时间戳） | `q.i()` 返回 `now >= e + d` |
| 超时常量 | `pmsj/work/main/i.smali` `<clinit>`：`const v0, 0x15f90` → `sput Lpmsj/work/main/i;->g:I` | `0x15f90 = 90000` ms |
| 启动看门狗 | `pmsj/work/main/e.smali` `private static K(Lpmsj/work/main/w;)`（`1052` 握手成功分支） | 若 `i.h.h()` 为假则 `i.h.e(i.g)` → 90 秒计时开始 |
| 刷新看门狗 | `pmsj/work/main/i.smali` `public final a(Ljava/io/DataInputStream;)V`（收包入队入口） | 若看门狗已启动则 `i.h.e()` 刷新“最后活动时间” |
| 判定断线 | `pmsj/work/main/t.smali` 渲染循环 | `if (i.h.i()) → i.b("与服务器断开连接。")`，随后该连接被判为断开 |

→ 只要客户端进程被冻结或长时间收不到数据，**帧循环一旦重新运行就会立刻判定断线**，即使服务端 socket 仍然存在。

### 2.4 心跳收发链（与协议文档一致）

- 服务端 `1012` ping → 客户端 `pmsj/work/main/e.smali` `private static as(Lpmsj/work/main/w;)`：
  `mid=0x3f4`、`field0 = w.c(0)`（原样回非收）、`field1 = (int) currentTimeMillis() ^ field0`、`field2 = 0`。
- 服务端日志中该帧为 `values=[nonce, <负数>, 0]`，与 `field1` 的异或结果一致。
- 客户端只在**收到** ping 时回应，没有独立的客户端侧心跳线程；`a/c/u.smali` 的 socket 读线程也没有 `setSoTimeout`，属于永久阻塞读。

### 2.5 显式退出路径（会被误认为“掉线”）

`pmsj/work/main/MyMidlet.smali` `public final a()V`：

```smali
invoke-virtual {p0}, Lpmsj/work/main/MyMidlet;->finish()V
const/4 v0, 0x0
invoke-static {v0}, Ljava/lang/System;->exit(I)V
```

调用点（静态扫描 `MyMidlet;->a()V` / `MyMidlet;->b()V`）：`pmsj/work/main/u.smali:30`、`pmsj/work/e/bd.smali:1178/1208`、`pmsj/work/e/e.smali:993`、`pmsj/work/main/e.smali:5924` 直接调用 `a()`；`pmsj/work/e/do.smali:637` 经 `MyMidlet.b()`（内部再调 `a()`）。走到这里进程立即结束，socket 随之关闭，服务端看到 EOF。

## 3. 服务端证据

| 环节 | 位置 | 行为 |
| --- | --- | --- |
| 心跳间隔 | `implementation_staging/config.json:141`（`heartbeat_interval_seconds: 25`）、`server.py:126` | 每 25 秒发一次 |
| 心跳循环 | `server.py:474-503` `_heartbeat_loop` | 只 `_send(heartbeat_challenge(nonce))`；异常只 `return`；**不记录最后 pong、不超时断开** |
| 心跳启动 | `server.py:580-583` | 仅当 `session['game_ready']` 时创建任务 |
| 断线判定 | `server.py:584-626` | 只在 `asyncio.IncompleteReadError` / `ConnectionResetError`（对端 FIN/RST）时记 `client disconnected`，并执行位置落盘、`depart_map`、队伍/对决清理 |
| 对 pong 的处理 | 路由层 | 客户端 `1012` 只被记为 `ignored unimplemented message=1012`，不参与任何超时判定 |

结论：服务端在本现象里是“被动受害者”，不是掉线发起方。`docs/protocol/13-协议审计问题.md` 中的行号（`server.py:1726-1746` 等）来自重构前的单文件版本，当前网络层已收敛到 `server.py:454-626`。

## 4. 日志证据（`implementation_staging/logs/server.20260916-002046.stderr.log`）

两次手机端掉线都发生在**最后一次成功 pong 之后约 2 秒**，而不是 25 秒心跳周期或 90 秒看门狗超时：

```text
2026-09-16 00:27:41,523 INFO heartbeat sent to ('192.168.0.102', 36668) nonce=10
2026-09-16 00:27:41,617 INFO received message=1012 field_types=[4, 4, 4]
2026-09-16 00:27:43,660 INFO client disconnected: ('192.168.0.102', 36668)
2026-09-16 00:27:43,677 INFO ROLE_POSITION_DISCONNECT_SAVE user='5201314' role_id=10085 map=58 tile=40,44
```

```text
2026-09-16 07:50:14,625 INFO heartbeat sent to ('192.168.0.102', 49672) nonce=4
2026-09-16 07:50:14,663 INFO received message=1012 field_types=[4, 4, 4]
2026-09-16 07:50:16,798 INFO client disconnected: ('192.168.0.102', 49672)
2026-09-16 07:50:16,798 INFO PLAYER_MAP_DEPART role_id=10085 announced_map=58
```

判读：

- 若只是“进程被冻结”，socket 不会关闭，服务端**不会**看到 EOF（冻结只影响应用层读写，内核仍持有连接）。
- 日志显示的是干净的连接终止 + 位置落盘，说明是**对端 socket 被关闭**：进程退出（用户退出流程/`System.exit(0)`）或被系统杀掉（低内存回收、厂商后台清理、强行停止）。
- 同一日志里 `('192.168.0.104', 62124)` 从 00:22 一直心跳到 19:34（约 19 小时、1686 次心跳）都没断，说明“只要进程活着，服务端连接可以长期保持”；掉线问题完全在客户端进程存活侧。

## 5. 未知项（不得当作已实现）

1. 具体是哪一条杀进程路径（cached-app freezer 冻结后被回收 / 厂商电池管家即时查杀 / 用户手势退出 / 走到 `System.exit(0)`）取决于机型与系统设置，**需要真机 logcat 确认**。
2. 冻结期间服务端仍认为角色在线（socket 未关）；回到前台时是客户端先判超时，还是读线程先处理攒下的 ping，取决于帧循环与读线程竞态，属客户端时序，未做真机验证。
3. 服务端当前**没有**断线恢复协议（无 lastSeq/snapshot/session resume 语义），所以即使客户端被保活，也只能依赖客户端自身的 90 秒看门狗判定；原服在这一点上的行为未确认，禁止据此发明恢复语义。

## 6. 处理选项（未实现，仅候选）

### 选项 A：APK 侧加前台服务保活（推荐，改动最大但最有效）

- 新增一个 `android.app.Service` 子类（smali 手写，例如 `pmsj/work/local/KeepAliveService.smali`）：
  - `onCreate` 里 `startForeground(id, notification)`；
  - `onStartCommand` 返回 `START_STICKY`；
  - 清单声明 `<service android:name="pmsj.work.local.KeepAliveService" android:exported="false"/>`；
  - 因为 `targetSdkVersion=7`，不需要 `FOREGROUND_SERVICE` 权限，也不受 Android 8+ 后台服务限制；前台服务进程不会进入 cached 状态，可避开 Android 12+ cached-app freezer。
  - 可选：`WAKE_LOCK` 权限 + `PARTIAL_WAKE_LOCK`，避免熄屏后读写线程被长期挂起。
- 实现方式：沿用现有构建链（`build_local_apk.ps1` + `tools/patch_*.py`），新增一个 patch 脚本注入 smali 类与清单节点，再重签名。
- 风险：常驻通知（Android 8+ 需要 channel，Android 13+ 需要 `POST_NOTIFICATIONS` 才显示通知，但不影响服务运行）；厂商 ROM 仍需用户在设置里允许后台运行；必须先真机验证。

### 选项 B：手机侧临时规避（零改动，可立即验证）

- 关闭该应用的电池优化（“不受限制/允许后台活动”）；
- 在最近任务里给应用加锁（部分 ROM 提供“锁定后台”）；
- 在厂商自启动/后台管理白名单中加入该应用；
- 开发者选项里关闭“不保留活动”。
- 这些措施能否完全避免查杀取决于 ROM，但可以用来区分“冻结”与“查杀”。

### 选项 C：服务端 pong 超时（与当前现象无关，属于健壮性）

- 目前没有任何超时清理，僵尸连接会一直占着 `online_connections`（直到 TCP 层报错，默认可能很久）。
- 若要补，只能作为本地兼容的内部清理，并明确它不是客户端契约；不得据此发明重连/恢复协议（当前证据为 C 级）。

## 7. 真机验证步骤（交给用户执行）

1. 进入游戏并确认服务端日志出现该连接的 `heartbeat sent ... nonce=...` 与对应 `received message=1012`。
2. 按 Home/切换应用离开游戏，保持 30 秒以上。
3. 观察服务端日志是否出现 `client disconnected`：
   - 若**立即出现**（秒级）→ 进程被杀或主动退出（对应选项 A/B）。
   - 若**不出现**且回到前台立刻提示“与服务器断开连接。”→ 进程被冻结 + 90 秒看门狗（对应选项 A）。
4. 回到游戏后确认是否需要重新登录、角色是否保留原地图坐标（`ROLE_POSITION_DISCONNECT_SAVE`）。
5. 如需定位杀进程来源，用 `adb logcat` 抓 `ActivityManager`、`LowMemoryKiller`、`am_kill`、`cached app freezer` 等关键字。

## 8. 边界声明

- 本次只做静态证据收集与日志判读，未修改 `server.py`、协议字段、资源映射或客户端行为。
- 未访问任何官方/第三方服务器；日志与反编译产物均来自本仓库与用户提供的 APK。
- 结论等级：清单/生命周期/服务端行为为 A 级；90 秒看门狗为 B 级（常量、设置点、检查点、刷新点均已定位，但冻结期间竞态未真机确认）；杀进程路径为 B 级推理，真机状态 `pending real-device verification`。
- 反编译目录 `implementation_staging/build_artifacts/build/apk_decoded/` 属于构建产物，不入库；本文引用的 smali 行号取自该目录 2026-09-16 的构建快照，重新构建后可能变化。
