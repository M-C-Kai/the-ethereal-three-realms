# 自动挂机启动（B 级 APK 证据）

## APK Verification Gate

影响客户端挂机启动；仅使用 1010/action 280，不新增 Property 或资源。
证据来自完整解包 `map-60011-render-fix-20260914-224828/decoded/smali`：

- `pmsj/work/main/k.smali:6537`：“自动挂机”菜单调用 `w.a(1010, SHORT 280)`。
- `main/w.smali:711` 写消息号及单个 SHORT；`a/c/r.smali:234` 写类型 3 和 writeShort。
- `main/e.smali:5985`：1010 分支先解除等待，然后读取 **field 5 SHORT**。
- `main/e.smali:6537`：action 280 清理移动状态，设置 T=0，将当前 e/f 坐标写入 L，关闭页面 5/382/381/380。无需读取其他字段。
- `work/b/ab.smali:596`：al() 围绕 L 随机偏移 -5..5，在非阻挡位置发起原生移动。

C→S 字段：`[SHORT 280]`。
S→C 字段：`[INT 0, SHORT 0, SHORT 0, INT 0, INT 0, SHORT 280]`。
前五个字段在此分支未使用，沿用地图应答安全零值，不赋予新语义。

服务端只补启动应答；不构造服务端挂机定时器，不修改角色存档。
权限、计费、持续遇怪及停止条件尚未完整确认，不推测实现。
自动测试锁定消息号、字段顺序/类型/数量及重复请求不改变角色数据。
真机状态：pending real-device verification。验收：在可移动地图点击自动挂机，确认菜单及等待关闭，角色移动；继续确认遇怪及战后恢复。
