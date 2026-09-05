# 装备模板证据（最终调查报告）

本文只整理当前仓库里**已保存、可复核**的 APK 客户端证据。  
252 个图标资源候选是 **APK 装备图标资源**，不是官方装备模板。  
当前可靠的「真实官方装备 ID + 官方名称」配对数量为 **0**。

证据路径：

- `implementation_staging/references/smali/pmsj/work/b/j.smali`
- `implementation_staging/references/smali/pmsj/work/b/g.smali`
- `implementation_staging/references/smali/pmsj/work/b/a.smali`
- `implementation_staging/references/smali/pmsj/work/b/v.smali`
- `implementation_staging/references/smali/pmsj/work/e/af.smali`
- `implementation_staging/references/smali/pmsj/work/d/a.smali`
- `implementation_staging/references/smali/pmsj/work/main/e.smali`
- `implementation_staging/references/smali/a/c/x.smali`
- `implementation_staging/references/CLIENT_EVIDENCE.md`
- `implementation_staging/EQUIPMENT_RESOURCE_CATALOG.md`
- `implementation_staging/data/catalog/apk_equipment_resources.json`
- `implementation_staging/materials/appearance-layer-audit/manifest.json`

---

## CONFIRMED

1. 物品 `template_id` 字段为：`pmsj/work/b/j.f`。

2. 装备 category：

   ```text
   category = (template_id // 10_000_000) % 100
   ```

   `category` 为 `1..21` 时，客户端将其识别为装备。

3. quality：

   ```text
   quality = template_id % 10
   ```

   客户端明确存在至少 `0..4` 的品质处理。`5..9` 是否正式使用未知。

4. `category 10` 是武器。

5. 武器：

   ```text
   weapon_type = (template_id // 100_000) % 100
   ```

   `weapon_type` 用于：

   - 武器类型文字数组 `ai[]`
   - 角色武器适配 bitmask：`1 << weapon_type`

   因此定义为：**「武器类型 / 武器适配类型索引」**。  
   它**不是**已证明的 appearance ID。

6. 人物装备面板：`implementation_staging/references/smali/pmsj/work/e/af.smali`  
   每件装备按 6 字段解析：

   | 字段 | 含义 | 写入 |
   |---:|---|---|
   | field0 | `template_id` | |
   | field1 | equipped slot/state | `g.k` |
   | field2 | name | |
   | field3 | `required_level` | |
   | field4 | `instance_id` | |
   | field5 | icon resource index | `j.q` |

7. `required_level` 是独立服务端字段。  
   目前没有 `required_level = formula(template_id)` 证据。

8. 装备名称由服务端直接下发。

9. `icon_code` 独立下发。UI 中：

   ```text
   j.q → a/c/x.f(icon_code) → 24×24 物品图标资源
   ```

   目前没有 `icon_code = formula(template_id)` 证据。

10. 人物装备面板标准槽位数为 **14**。

11. equipped slot 使用独立 `g.k` 字段。  
    **template category、equipment slot、icon resource group 必须视为三个不同概念。**

12. 人物 appearance 是独立资源系统。`pmsj/work/b/v.smali`：

    | 方法 | 图层 | 资源 |
    |---|---|---|
    | `A(I)` | layer5 | `16000 + value` |
    | `B(I)` | layer6 | `17000 + value` |
    | `C(I)` | layer7 | `18000 + value` |
    | `D(I)` | layer8 | `19000 + value` |
    | `E(I)` | layer9 | `20000 + value` |
    | `F(I)` | layer10 | `21000 + value` |
    | `G(I)` | `layer = ((value % 1000) // 100) + 32` | `resource = 40000 + (value % 10000)` |

    当前没有 `template_id → appearance` 或 `icon_code → appearance` 公式证据。

---

## STRONG EVIDENCE

客户端整体结构强烈表明：

服务器维护：

- `template_id`
- `instance_id`
- `name`
- `required_level`
- `icon_code`
- equipped slot

客户端负责：

- `category`
- `quality`
- `weapon_type`
- 装备资格
- 强化逻辑
- UI
- 图片资源
- 人物复合资源

因此官方装备主体模板很可能在原服务端数据库。

当前仓库 `references` 只是完整 APK 反编译目录中抽取的关键文件，**不能**写成「已经证明 APK 绝对不存在装备静态表」。

只能写：

> 当前已保存并可复核的 APK 客户端证据中，没有恢复出完整官方装备模板库。

---

## UNKNOWN

- `template_id` 中间位结构
- quality `5..9` 是否正式使用
- category `1..21` 完整中文名称
- `weapon_type` 具体武器名称
- `template_id →` 官方 name
- `template_id →` `required_level`
- `template_id →` `icon_code`
- `template_id →` appearance
- 官方属性
- 官方价格

当前可靠的「真实官方装备 ID + 官方名称」配对数量：**0**。

---

## REJECTED ASSUMPTIONS

1. 青纹套装不是 APK 官方装备。它是兼容服构造数据，保留在 `items.json` / `starter_inventory.json` 中，不得称为官方模板。
2. `10001001` 中的 `001` 不能解释为 1 级。
3. 图标存在 ≠ 官方装备模板存在。`apk_equipment_resources.json` 的 252 条只是 APK 图标资源候选。
4. `resource_group` ≠ template category。
5. template category ≠ equipment panel slot。
6. `322xxxxxx` 不是普通装备模板。它们 `category=32`，是装备相关材料/特殊物品逻辑。
7. `weapon_type` ≠ 已证明的 weapon appearance。
8. `icon_code` ≠ appearance。

---

## 兼容服资源预览装备（非官方）

为了让客户端背包能显示全部 252 个 APK 装备图标，兼容服另外构造了独立 catalog：

`data/catalog/equipment_resource_preview_items.json`

这些条目的 `kind/status` 为 `compatibility_preview`。  
其中 `icon_code` / 资源分组来自 APK；`template_id`、名称、等级、属性均为本地预览构造，**不代表官方装备**。

人物外观：slot 1/2/3/5/7/8/9 的 preview `appearance_properties` 现在引用 `materials/appearance-layer-audit/manifest.json` 中 **APK-confirmed character-layer candidates**（`candidate_image_ids - group_base`，按 `sort_order` 配对，超出则循环）。

这是 **APK资源预览配对 / compatibility preview pairing**，**不是**官方 `icon_code → appearance` 或 `template_id → appearance` 映射。

以下槽位仍保持 `appearance_properties: {}`：腰带(4)、项链(6)、武器(10)、戒指(11)、外套(12)、饰品(13)、法宝(14)。武器虽已知 property 7，但尚未恢复 icon group 21..33 → weapon appearance code 的完整映射，本轮不猜测。

预览项只进入背包。登录补齐 **不修改** 人物 appearance；只有玩家手动装备后，才通过现有 `character_appearance()` / `character_appearance_change_frame()` 生效。
