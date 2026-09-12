# 1138 寄售原生页面链

当前静态确认自 `implementation_staging/references/smali/pmsj/work/main/e.smali` 的 `al(w)` 接收器：

- action 1 / 12 / 16 -> screen 73 (`0x49`)
- action 3 / 22 -> screen 613 (`0x265`)
- action 7 / 9 / 14 / 15 -> screen 70 (`0x46`)
- action 13 -> screen 44 (`0x2c`)

因此 action 13 不能只返回 `[13, 0]` 这种通用空计数；screen 44 使用 count/filter vector，随后客户端再通过 action 0/23 请求市场行，服务端以 action 1 返回市场记录。

本文件只记录已用于本地兼容实现的页面路由与测试契约；后续若拿到完整 `e/au.smali`/`e/ev.smali`，继续补充 C->S 发送点逐行证据。
