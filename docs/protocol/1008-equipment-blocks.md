# 1008 装备属性分支复核

APK evidence: B；完整解包 map-60011-render-fix-20260914-224828/decoded/smali。
main/e.Z（3984）处理 1008；b/g.c()（995）只对模板大类 1..10 返回 true。
Z 的 cond_7..cond_a（4460..4550）顺序读取：

| 零基字段 | 类型 | 对象 |
|---|---|---|
| 16..23 | SHORT | g.d[0..7]，a(BS) |
| 24..28 | BYTE | g.b[0..4]，a(BB) |
| 29..33 | BYTE | g.c[0..4]，b(BB) |
| 34..38 | 整数读取，服务端使用 INT | g.x[0..4]，a(BI) |

总计 39 字段，包含公共头 0..15。
main/w.b(I) 强转 a/c/o（SHORT）；d(I) 使用通用整数读取。
原编码 4 SHORT + 5 BYTE + 5 BYTE + 5 SHORT（35 字段）造成块错位。
本次补至 8 SHORT，后组保持位置并使用 INT；未知新增四项默认 0，不命名为耐久。
无存档迁移；原四项数据保持。其他模板大类编码暂不调整，其语义仍需独立复核。
Protocol impact: 仅修复 1008 模板大类 1..10 的附加块，不新增消息/Action/资源。
Tests: 字段数量、顺序、类型、非零哨兵值及非装备仍为 16 字段。
Real-device: pending real-device verification。
