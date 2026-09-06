# 武器外观资源审计（property7 误判修正）

本目录保留 APK 中 `100000..110000` role DAT、`40000..49999` 图片 ID 与候选表作为历史审计资料，但这些候选**不再用于人物 property7 武器映射**。

## 已确认

`pmsj/work/b/v.r()` 的真实调用关系：

```text
property 7  -> v.e(I)
property 22 -> v.G(I)
```

`v.e(I)` 将 property7 解释为完整武器编码：`value//10` 为武器 image，`value%10` 为品质；使用的 family 数组为 `[241,220,290,231,280,250,270,271,242,240,260,221,230]`。因此地图 property7 与战斗 `1048 field[2]` 应使用同一个武器编码。

旧版 `property7_candidates.json` 的 69 个候选来自 `H/I/G`/40000 系列资源反向审计，但把这条路径标成 property7 是错误解释。文件继续保留用于复核 APK 资源存在性，生产代码不得再将其循环分配给 slot10 武器。
