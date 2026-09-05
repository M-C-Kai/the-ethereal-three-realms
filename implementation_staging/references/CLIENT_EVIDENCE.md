# 客户端证据索引

这些文件从 `base.apk.1` 的反编译结果中复制，用于让后续开发快速核对协议与资源读取逻辑。它们是只读参考，不应直接作为服务端源码修改。

| 文件 | 已知用途 |
|---|---|
| `smali/pmsj/work/main/e.smali` | 主要网络消息分发；包含 `1008` 等协议的字段读取顺序 |
| `smali/pmsj/work/main/w.smali` | 协议字段容器及 byte/short/int/string/binary 读取方法 |
| `smali/pmsj/work/main/k.smali` | 主菜单文字入口与人物页面跳转 |
| `smali/pmsj/work/b/j.smali` | 物品基类；模板大类、品质和通用动作 |
| `smali/pmsj/work/b/g.smali` | 装备物品子类及装备附加字段 |
| `smali/pmsj/work/b/a.smali` | 客户端背包/装备物品集合 |
| `build/apk_decoded/smali/pmsj/work/b/ab.smali` | 人物属性访问器；`g()` 读取属性 62（背包容量），`n()` 读取属性 59（仓库容量） |
| `build/apk_decoded/smali/pmsj/work/e/au.smali` | 仓库存放菜单；确认 `1009` 动作 47（NPC 兼容动作 29），本轮仅记录不实现 |
| `build/apk_decoded/smali/pmsj/work/e/ea.smali` | 仓库界面和取出菜单；确认属性 59、位置 51、`1009` 动作 48（NPC 兼容动作 30），本轮仅记录不实现 |
| `smali/pmsj/work/b/v.smali` | 人物属性到角色叠加资源的转换 |
| `smali/pmsj/work/b/n.smali` | 战斗人物基础渲染；h.r() 调用的 e(field2) 武器主图/品质覆盖层解析证据。 |
| `smali/pmsj/work/b/h.smali` | 战斗人物 work/b/h；1048 kind=1 field[2] 的人物底板、武器图层和品质覆盖层解析证据。 |
| `smali/pmsj/work/e/af.smali` | 人物装备面板；14 个装备槽位及其名称 |
| `smali/pmsj/work/d/a.smali` | UI 物品控件；图标字段到图片资源的调用 |
| `smali/a/c/x.smali` | 图片图集编号算法；`f(int)` 是 24×24 物品图标转换 |
| `smali/a/a/a.smali` | `role/*.dat` 角色动画资源解析和绘制 |

辅助脚本：

- `scripts/extract_game_images.py`：从 `images.o + png*.p` 提取图片。
- `scripts/build_equipment_icon_sheet.py`：生成带图标编号的装备资源总览。
- `scripts/render_role_resources.py`：解析并预览 `role/*.dat`。
- `battle-weapon-appearance-audit/`：战斗武器图标组 21..33 与 battle image family 220..290 的视觉审计（不推断映射）。

完整反编译目录仍位于：

```text
C:\Users\Kail\Documents\Codex\2026-08-24\new-chat\work\apk-initial-role-reference
```
