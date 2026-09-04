# 游戏内退出协议（APK 逆向确认）

> 本文档记录从原始 APK 静态逆向确认的游戏内退出完整流程。
> 协议字段类型为协议锁内容，禁止用数值相等的其他类型替代。

## 完整流程

### 第一步：打开退出页面

客户端请求：

```text
C -> S
messageId = 1054
field[0] = BYTE 8
```

服务端回复：

```text
S -> C
messageId = 1054
field[0] = BYTE 8      (固定回显 action)
field[1] = BYTE flag   (0 = 普通确认页)
field[2] = STRING text (确认文案)
```

本地服当前下发：

```text
flag = 0
text = "是否确认退出游戏？"
```

字段类型严格为 `BYTE, BYTE, STRING`（type_id `2, 2, 6`），不得用 short/int 替代。

### 第二步：真正注销

用户在退出页面确认后，客户端发送：

```text
C -> S
messageId = 1003
field[0] = INT 0
```

注意：字段类型是 `INT`（type_id `4`），**不是** `BYTE`。

服务端处理顺序：

1. 若当前连接有尚未 checkpoint 的位置变化（`position_dirty`），立即调用
   `RoleStore.save()` 保存当前位置，并记录日志
   `ROLE_POSITION_LOGOUT_SAVE`（含 `user`、`role_id`、`map_id`、`map_x`、`map_y`），
   同时将 `position_dirty` 复位为 `False`（避免 `finally` 断线兜底重复保存）。
2. 回复：

```text
S -> C
messageId = 1003
field[0] = BYTE 0
```

3. 记录日志 `ROLE_LOGOUT_ACK`。
4. 服务端**不要**主动断开 socket：不 `break`、不 `return`、不 `writer.close()`、
   不提前结束 `handle()`。

### 客户端行为（APK 已确认）

原 APK 收到 `1003 / BYTE 0` 后：

- 等待约 1 秒；
- 自行关闭游戏连接；
- 清理角色 / UI 状态；
- 返回登录界面。

客户端断开 TCP 后，服务端进入现有 `finally` 断线清理流程。

## 1074 不是退出协议

APK 已确认：`1074` 是 `pmsj/work/main/i.e()` 周期发送的连接/状态类协议，
游戏循环大约每秒调用一次。

- 不修改 1074；
- 不新增 1074 logout handler；
- 不把 1074 与退出流程关联。

## 服务端实现位置

| 内容 | 位置 |
| --- | --- |
| `logout_page_frame()` / `logout_ack_frame()` | `server.py`（协议构造函数） |
| `is_logout_page_request()` / `is_logout_confirm_request()` | `server.py`（TLV 类型+值校验的纯函数） |
| 1054 / 1003 handler | `server.py` `LocalGameServer.handle()` 消息分发链 |

## 请求校验规则（防类型混淆）

只判断 `values[0]` 会把错误类型当成退出请求，必须同时校验 TLV 类型：

| 请求 | 合法 | 非法（必须拒绝） |
| --- | --- | --- |
| 1054 退出页面 | `BYTE 8`（type_id 2） | `INT 8`、`STRING '8'`、`BYTE 7` 等 |
| 1003 注销确认 | `INT 0`（type_id 4） | `BYTE 0`、`INT 1` 等 |

## 与断线保存的关系

```text
正常退出：
1003/INT 0 -> ROLE_POSITION_LOGOUT_SAVE（如 dirty） -> 1003/BYTE 0 ACK
           -> APK 主动断线 -> finally（无 dirty，不重复保存）

异常掉线：
TCP disconnect -> finally -> ROLE_POSITION_DISCONNECT_SAVE（兜底）
```

`finally` 中现有的 `ROLE_POSITION_DISCONNECT_SAVE` 兜底逻辑保持不变，
用于掉线 / 强制关闭 / 非正常退出场景。

## 自动化验证

```text
tests/test_logout.py        13 项协议/校验单元测试
test_client.py --exercise-logout-only   登录后完整走一遍 1054 -> 1003 退出闭环
```
