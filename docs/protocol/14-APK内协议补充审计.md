# APK 内协议补充审计

> 审计对象：`implementation_staging/piaomiao_local_login.apk` 对应的完整反编译目录 `implementation_staging/build/dex-smali/`。本文件补充 Python 本地服协议文档，重点回答 APK 内还保留了哪些协议以及调用位置。没有访问任何外部服务器。

## 结论

- APK 主接收器从 TCP 读取 `short messageId` 后解析字段并进入 sparse-switch；主入口：`pmsj/work/main/e.smali:4620-9170`。
- 主接收分发表包含 **110 个 S→C ID**：`pmsj/work/main/e.smali:8876-8988`。
- 对 `main/w` 发送帮助函数及直接 `a/c/r` Packet 构造的静态回溯找到 **91 个 C→S ID、528 个发送调用点**。发送帮助函数本体：`pmsj/work/main/w.smali:47-938`。
- 两侧合并为 **120 个唯一协议 ID**：81 个双向、29 个仅有 APK 接收分支、10 个仅有 APK 发送构造。
- 当前 Python 本地服覆盖范围持续扩展，具体以消息号总表和各功能审计为准。
- 下表中标为“未使用/无发送调用证据”的额外 ID 只有 APK 接收分支，当前仓库也没有本地服发送实现。这不代表旧官方服务端一定从未发送。
- 另有 10 个仅 C→S ID：1031、1051、1074、1085、1095、1159、1534、1999、2031、6000。这是正常的 request-only 形态，不因 APK 没有同 ID 接收器就判定废弃。

## 功能位置摘要

| 协议/范围 | APK 中的使用位置 | 判断 |
|---|---|---|
| 1009、1008、1032 | 人物装备页、背包和物品基类；如 `pmsj/work/e/af.smali:1389-1690`、`pmsj/work/e/bt.smali:869-1591` | 物品查看、装备、卸下和详情；已确认 |
| 1019 | 仇人、好友与社交界面；`pmsj/work/e/ae.smali:253-431`、`pmsj/work/e/an.smali:582` | 社交关系操作；功能名称由界面字符串确认 |
| 1033 | 物品属性/购买数量界面；`pmsj/work/e/ar.smali:310-1323`、`pmsj/work/e/dp.smali:181` | 商店或购买操作；待确认具体 action |
| 1050 | 星官/关卡挑战界面；`pmsj/work/e/aw.smali:1100-1460` | 副本/挑战；待确认字段 |
| 1054 | 福缘界面；`pmsj/work/e/ak.smali:265-702` | 福缘系统；已确认模块，字段待确认 |
| 1056 | 交易请求；`pmsj/work/e/er.smali:1441`、`pmsj/work/e/et.smali:935` | “请求交易”发送 `1056/action=2`；旧版误标为队伍 |
| 1023/1026 | 队伍；`pmsj/work/b/aa.smali`、`pmsj/work/main/e.smali:12187`、`pmsj/work/main/e.smali:13100` | 创建、解散及成员记录；已确认最小闭环 |
| 1061 | 活动详情界面；`pmsj/work/e/g.smali:450-1020` | 活动系统；已确认模块 |
| 1065 | 人物状态页；`pmsj/work/e/dk.smali:392` | 取消/查看状态；已确认模块 |
| 1068 | 公告/版本预告；`pmsj/work/e/ex.smali:145-733` | 公告系统；已确认模块 |
| 1069 | 可领取/已领取奖励界面；`pmsj/work/e/bc.smali:209-910` | 奖励领取；已确认模块 |
| 1071 | 修真、五行、灵力界面；`pmsj/work/e/dl.smali:610-745` | 修真系统；已确认模块 |
| 1072 | 封魔榜/BOSS 目标；`pmsj/work/e/v.smali:117-511` | BOSS 榜单或挑战；已确认模块 |
| 1075、1153 | 关卡/副本界面；`pmsj/work/e/bg.smali:945-1458`、`pmsj/work/e/ek.smali:393-1251` | 副本、进度与挑战；已确认模块 |
| 1082 | 好友在线/离线列表；`pmsj/work/e/bo.smali:764-1632` | 好友/联系人；已确认模块 |
| 1083 | 仙晶、银两显示；`pmsj/work/e/ac.smali:598-1490` | 货币/兑换相关；具体 action 待确认 |
| 1084 | 背包、银两和物品详情界面；`pmsj/work/e/al.smali:741-2255`、`pmsj/work/e/am.smali:334` | 背包/交易相关；具体 action 待确认 |
| 1092 | 累计金额与领取界面；`pmsj/work/e/ab.smali:215-948` | 累计充值/奖励类；待确认 |
| 1094 | 斗胜值、排名、挑战次数；`pmsj/work/e/be.smali:654-1081` | 竞技/挑战；已确认模块线索 |
| 1103 | 宠物资质、存放宠物；`pmsj/work/e/cg.smali:387-467` 等 | 宠物系统；已确认模块 |
| 1107 | 帮主、成员、资金、活跃度；`pmsj/work/e/cx.smali:213-792` | 帮派系统；已确认模块 |
| 1127 | 容量、领出等仓储界面；`pmsj/work/e/ai.smali:121-713` | 仓库/领取；待确认 |
| 1128、1132 | 技能学习/升级界面；`pmsj/work/e/ax.smali:909-1036`、`pmsj/work/e/az.smali:763` | 技能系统；已确认模块 |
| 1135 | 初/中级训练等界面；`pmsj/work/e/ce.smali:2633-2799` | 宠物或角色训练；对象待确认 |
| 1137、1138、1158、1731 | 加友、聊天、邀请、玩家详情；`pmsj/work/e/ef.smali:331-696`、`pmsj/work/e/au.smali:968-986`、`pmsj/work/e/cy.smali:869-921` | 社交/聊天/邀请；已确认模块 |
| 1403 | 活动/奖励页面多处调用；如 `pmsj/work/e/ca.smali:1035-1566` | 活动任务预取与领奖；本地服当前仅空应答 |
| 1500-1534 | 图片、角色 DAT、PNG 缓存、界面资源请求；主分发 `main/e.smali:8292-8583` | 动态资源传输；部分已接入，部分未接入 |
| 2031 | 地图通用实体交互；`main/e.smali:4537-4600` | 地图对象接近/交互；已确认 |
| 6000 | 切石/秘石界面；`pmsj/work/e/dn.smali:433-615` | 小玩法；仅 C→S 构造，服务端未接入 |

以上模块名只有在类内中文 UI 字符串、调用入口或现有协议证据能够支撑时才写入；其余 ID 不根据编号猜功能。

## APK 补充协议全表

| ID | APK 方向 | 静态调用/处理位置 | 当前状态 |
|---:|---|---|---|
| 1003 | S→C | 接收 main/e.f，分发:8731 | 未使用/无发送调用证据 |
| 1004 | 双向 | 接收内联 main/e:5786<br>发送 pmsj/work/main/e.smali:9401 | APK静态使用；本地服未接入 |
| 1005 | 双向 | 接收内联 main/e:6685<br>发送 pmsj/work/b/ab.smali:699 | APK静态使用；本地服未接入 |
| 1014 | S→C | 接收 main/e.T，分发:6680 | 未使用/无发送调用证据 |
| 1015 | S→C | 接收 main/e.am，分发:8436 | 未使用/无发送调用证据 |
| 1019 | 双向 | 接收 main/e.ah，分发:7444<br>发送 pmsj/work/e/ae.smali:253（7处） | APK静态使用；本地服未接入 |
| 1023 | 双向 | 接收 main/e.ag，分发:8421<br>发送 pmsj/work/b/aa.smali:429（42处） | 本地服已接入创建与解散最小闭环 |
| 1024 | 双向 | 接收 main/e.t，分发:8776<br>发送 pmsj/work/e/bt.smali:869（16处） | APK静态使用；本地服未接入 |
| 1025 | 双向 | 接收 main/e.A，分发:8736<br>发送 pmsj/work/e/dv.smali:570（2处） | APK静态使用；本地服未接入 |
| 1026 | S→C | 接收 main/e.aj，分发:8426 | 本地服已用于创建队伍后的队长成员记录推送 |
| 1030 | 双向 | 接收 main/e.ak，分发:8431<br>发送 pmsj/work/main/k.smali:7248（4处） | APK静态使用；本地服未接入 |
| 1031 | C→S | 发送 pmsj/work/main/c.smali:1509 | APK静态使用；本地服未接入 |
| 1033 | 双向 | 接收 main/e.g，分发:8627<br>发送 pmsj/work/e/ar.smali:310（5处） | APK静态使用；本地服未接入 |
| 1038 | S→C | 接收 main/e.ai，分发:6925 | 未使用/无发送调用证据 |
| 1050 | 双向 | 接收 main/e.n，分发:8791<br>发送 pmsj/work/e/aw.smali:1100（5处） | APK静态使用；本地服未接入 |
| 1054 | 双向 | 接收 main/e.v，分发:8766<br>发送 pmsj/work/e/ak.smali:265（8处） | APK静态使用；本地服未接入 |
| 1056 | 双向 | 接收内联 main/e:7449<br>发送 pmsj/work/e/er.smali:1441（7处） | APK静态使用；本地服未接入 |
| 1059 | 双向 | 接收 main/e.m，分发:8796<br>发送 pmsj/work/e/by.smali:304（6处） | APK静态使用；本地服未接入 |
| 1065 | 双向 | 接收 main/e.I，分发:8691<br>发送 pmsj/work/e/dk.smali:392 | APK静态使用；本地服未接入 |
| 1066 | S→C | 接收 main/e.J，分发:8671 | 未使用/无发送调用证据 |
| 1067 | 双向 | 接收 main/e.u，分发:8771<br>发送 pmsj/work/e/ao.smali:171（6处） | APK静态使用；本地服未接入 |
| 1068 | 双向 | 接收 main/e.j，分发:8811<br>发送 pmsj/work/e/ex.smali:145（3处） | APK静态使用；本地服未接入 |
| 1069 | 双向 | 接收 main/e.k，分发:8806<br>发送 pmsj/work/e/bc.smali:209（3处） | APK静态使用；本地服未接入 |
| 1071 | 双向 | 接收 main/e.B，分发:8726<br>发送 pmsj/work/e/dl.smali:610（8处） | APK静态使用；本地服未接入 |
| 1072 | 双向 | 接收 main/e.z，分发:8746<br>发送 pmsj/work/e/v.smali:117（2处） | APK静态使用；本地服未接入 |
| 1073 | 双向 | 接收 main/e.y，分发:8751<br>发送 pmsj/work/e/f.smali:657（6处） | APK静态使用；本地服未接入 |
| 1074 | C→S | 发送 pmsj/work/main/i.smali:1630 | APK静态使用；本地服未接入 |
| 1075 | 双向 | 接收 main/e.x，分发:8756<br>发送 pmsj/work/e/bg.smali:945（8处） | APK静态使用；本地服未接入 |
| 1078 | S→C | 接收 main/e.s，分发:8617 | 未使用/无发送调用证据 |
| 1079 | 双向 | 接收 main/e.j，分发:8811<br>发送 pmsj/work/e/ex.smali:126（3处） | APK静态使用；本地服未接入 |
| 1081 | 双向 | 接收 main/e.F，分发:8711<br>发送 pmsj/work/e/av.smali:893（3处） | APK静态使用；本地服未接入 |
| 1082 | 双向 | 接收 main/e.w，分发:8761<br>发送 pmsj/work/e/bo.smali:764（11处） | APK静态使用；本地服未接入 |
| 1083 | 双向 | 接收 main/e.p，分发:8781<br>发送 pmsj/work/e/ac.smali:598（10处） | APK静态使用；本地服未接入 |
| 1084 | 双向 | 接收 main/e.o，分发:8632<br>发送 pmsj/work/e/al.smali:741（7处） | APK静态使用；本地服未接入 |
| 1085 | C→S | 发送 pmsj/work/e/eg.smali:348（3处） | APK静态使用；本地服未接入 |
| 1087 | 双向 | 接收 main/e.i，分发:8816<br>发送 pmsj/work/e/ey.smali:1985 | APK静态使用；本地服未接入 |
| 1091 | 双向 | 接收 main/e.aE，分发:8836<br>发送 pmsj/work/e/dm.smali:279 | APK静态使用；本地服未接入 |
| 1092 | 双向 | 接收 main/e.c，分发:8851<br>发送 pmsj/work/e/ab.smali:215（4处） | APK静态使用；本地服未接入 |
| 1094 | 双向 | 接收 main/e.a，分发:8476<br>发送 pmsj/work/e/be.smali:654（8处） | APK静态使用；本地服未接入 |
| 1095 | C→S | 发送 pmsj/work/main/k.smali:4583 | APK静态使用；本地服未接入 |
| 1096 | S→C | 接收 main/e.M，分发:6559 | 未使用/无发送调用证据 |
| 1103 | 双向 | 接收 main/e.an，分发:8446<br>发送 pmsj/work/e/cg.smali:387（11处） | APK静态使用；本地服未接入 |
| 1107 | 双向 | 接收内联 main/e:7645<br>发送 pmsj/work/e/cx.smali:213（12处） | APK静态使用；本地服未接入 |
| 1115 | S→C | 接收 main/e.aA，分发:8696 | 未使用/无发送调用证据 |
| 1127 | 双向 | 接收 main/e.aa，分发:8451<br>发送 pmsj/work/e/ai.smali:713（9处） | APK静态使用；本地服未接入 |
| 1128 | 双向 | 接收 main/e.e，分发:8841<br>发送 pmsj/work/e/ci.smali:1103（4处） | APK静态使用；本地服未接入 |
| 1130 | 双向 | 接收 main/e.ac，分发:8461<br>发送 pmsj/work/e/ai.smali:121（18处） | APK静态使用；本地服未接入 |
| 1134 | 双向 | 接收 main/e.ab，分发:8456<br>发送 pmsj/work/e/ck.smali:2896 | APK静态使用；本地服未接入 |
| 1135 | 双向 | 接收 main/e.aB，分发:8701<br>发送 pmsj/work/e/ce.smali:2633（6处） | APK静态使用；本地服未接入 |
| 1136 | 双向 | 接收内联 main/e:7613<br>发送 pmsj/work/e/cx.smali:241 | APK静态使用；本地服未接入 |
| 1137 | 双向 | 接收内联 main/e:7818<br>发送 pmsj/work/e/ef.smali:331（2处） | APK静态使用；本地服未接入 |
| 1138 | 双向 | 接收 main/e.al，分发:8441<br>发送 pmsj/work/e/au.smali:968（12处） | APK静态使用；本地服未接入 |
| 1140 | 双向 | 接收内联 main/e:8564<br>发送 pmsj/work/e/ec.smali:336 | APK静态使用；本地服未接入 |
| 1141 | S→C | 接收 main/e.S，分发:8602 | 未使用/无发送调用证据 |
| 1142 | S→C | 接收 main/e.R，分发:8607 | 未使用/无发送调用证据 |
| 1143 | 双向 | 接收 main/e.D，分发:8721<br>发送 pmsj/work/e/db.smali:697（7处） | APK静态使用；本地服未接入 |
| 1144 | S→C | 接收 main/e.at，分发:8647 | 未使用/无发送调用证据 |
| 1145 | 双向 | 接收 main/e.av，分发:8666<br>发送 pmsj/work/e/ca.smali:1856（6处） | APK静态使用；本地服未接入 |
| 1157 | 双向 | 接收内联 main/e:5478<br>发送 pmsj/work/e/cu.smali:93（5处） | APK静态使用；本地服未接入 |
| 1158 | 双向 | 接收内联 main/e:8385<br>发送 pmsj/work/e/cy.smali:921（3处） | APK静态使用；本地服未接入 |
| 1159 | C→S | 发送 pmsj/work/e/dw.smali:603（2处） | APK静态使用；本地服未接入 |
| 1167 | 双向 | 接收内联 main/e:4973<br>发送 pmsj/work/e/aq.smali:83（3处） | APK静态使用；本地服未接入 |
| 1170 | S→C | 接收 main/e.G，分发:8706 | 未使用/无发送调用证据 |
| 1303 | 双向 | 接收内联 main/e:8481<br>发送 pmsj/work/e/be.smali:813（8处） | APK静态使用；本地服未接入 |
| 1500 | 双向 | 接收 main/e.au，分发:8652<br>发送 pmsj/work/e/bh.smali:761（8处） | APK静态使用；本地服未接入 |
| 1504 | 双向 | 接收 main/e.aq，分发:8554<br>发送 pmsj/work/e/bd.smali:787 | APK静态使用；本地服未接入 |
| 1505 | S→C | 接收 main/e.Y，分发:8559 | 未使用/无发送调用证据 |
| 1506 | 双向 | 接收内联 main/e:8583<br>发送 pmsj/work/e/ck.smali:1432（6处） | APK静态使用；本地服未接入 |
| 1509 | 双向 | 接收内联 main/e:8292<br>发送 pmsj/work/main/k.smali:2212（2处） | APK静态使用；本地服未接入 |
| 1511 | 双向 | 接收 main/e.aw，分发:8676<br>发送 pmsj/work/e/d.smali:1963 | APK静态使用；本地服未接入 |
| 1512 | S→C | 接收 main/e.ax，分发:8681 | 未使用/无发送调用证据 |
| 1518 | 双向 | 接收 main/e.av，分发:8657<br>发送 pmsj/work/main/k.smali:4377 | APK静态使用；本地服未接入 |
| 1519 | 双向 | 接收 main/e.H，分发:8637<br>发送 pmsj/work/e/z.smali:1030（2处） | APK静态使用；本地服未接入 |
| 1520 | 双向 | 接收 main/e.q，分发:8786<br>发送 pmsj/work/e/aj.smali:194 | APK静态使用；本地服未接入 |
| 1523 | 双向 | 接收 main/e.P，分发:5510<br>发送 pmsj/work/e/dr.smali:101（7处） | APK静态使用；本地服未接入 |
| 1533 | 双向 | 接收内联 main/e:5386<br>发送 pmsj/work/e/dt.smali:358（3处） | NPC 对话面板：本地服下发正文/选项，客户端回传选项 id |
| 1534 | C→S | 发送 pmsj/work/e/bk.smali:271（6处） | APK静态使用；本地服未接入 |
| 1731 | 双向 | 接收 main/e.ay，分发:8686<br>发送 pmsj/work/e/au.smali:986（9处） | APK静态使用；本地服未接入 |
| 1999 | C→S | 发送 pmsj/work/main/w.smali:834 | APK静态使用；本地服未接入 |
| 2027 | 双向 | 接收 main/e.az，分发:6930<br>发送 pmsj/work/main/k.smali:5177 | APK静态使用；本地服未接入 |
| 2028 | S→C | 接收 main/e.W，分发:6935 | 未使用/无发送调用证据 |
| 2029 | 双向 | 接收内联 main/e:6940<br>发送 pmsj/work/main/k.smali:5132 | APK静态使用；本地服未接入 |
| 2030 | S→C | 接收 main/e.X，分发:7033 | 未使用/无发送调用证据 |
| 2032 | 双向 | 接收内联 main/e:7108<br>发送 pmsj/work/e/cb.smali:974 | APK静态使用；本地服未接入 |
| 2100 | S→C | 接收 main/e.d，分发:8846 | 未使用/无发送调用证据 |
| 5020 | S→C | 接收 main/e.b，分发:8856 | 未使用/无发送调用证据 |
| 6000 | C→S | 发送 pmsj/work/e/dn.smali:433（6处） | APK静态使用；本地服未接入 |

## 明确标记为未使用/无调用证据

以下 18 个 ID 只有 `main/e` 的服务端消息接收分支，未找到 APK 发送构造，当前 Python 本地服也没有对应发送函数：

`1003, 1014, 1015, 1038, 1066, 1078, 1096, 1115, 1141, 1142, 1144, 1170, 1505, 1512, 2028, 2030, 2100, 5020`

它们应理解为“客户端保留了解码/处理能力，但在当前仓库可运行链路中没有生产者证据”。每个 ID 的具体处理入口已列在上表，不应删除，也不应当作已投入使用。

## 仅发送、无同 ID 接收器

`1031, 1051, 1074, 1085, 1095, 1159, 1534, 1999, 2031, 6000`

其中 1051 是选服请求、2031 是地图对象交互，已经由本地服处理；其余是 APK 内请求能力，本地服尚未接入。1999 由固定发送帮助函数 `main/w.a(La/c/i;)` 构造，6000 来自切石/秘石界面。缺少同 ID 接收器通常意味着应由另一响应 ID 或推送结束流程，不能强行配对。

## 裸数字/常量候选（按要求保留，但标明未使用）

下列数字位于网络或主菜单相邻代码，外观上可能被误认为 CMD，但没有作为 Packet 的 messageId 进入网络层。为避免遗漏，仍记录在这里；它们**不计入 120 个正式协议 ID**。

| 数值 | 出现位置 | 实际数据流 | 状态 |
|---:|---|---|---|
| 2000 | `pmsj/work/main/k.smali:6133-6137` | 传给界面对象 `d/c.y(2000)`；同一菜单文字为“商店仙晶” | 未使用/无协议调用证据，疑似界面 action |
| 2011 | `pmsj/work/main/k.smali:2115-2129` | 作为 short 子命令传给 `main/e.a(S,...)`；包装器实际发送的 messageId 是 1004 | 不是独立协议；1004 的 action |
| 2048 | `pmsj/work/main/c.smali:1344-1348` | 传给物品对象 `b/j.k(2048)` 做位标志判断 | 未使用/非协议，物品 flag |
| 2100 | `pmsj/work/main/k.smali:6106-6110` | 传给界面对象 `d/c.y(2100)`；但 2100 同时确实存在于主网络接收分发表 | 数值双重用途；网络协议仅 S→C，当前无生产者证据 |
| 2200 | `pmsj/work/main/k.smali:5534-5538` | “打造装备”界面调用 `d/c.y(2200)` | 未使用/无协议调用证据，界面 action |
| 2400 | `pmsj/work/main/k.smali:5578-5582,5630-5634` | “公告/宠物仓库”界面调用 `d/c.y(2400)` | 未使用/无协议调用证据，界面 action |
| 30000 | `pmsj/work/main/d.smali:2370` | 非 Packet 构造路径中的普通阈值/参数 | 未使用/无协议调用证据 |

这里尤其说明了为什么不能把 APK 中所有四位数都直接登记成 CMD：同一个数值空间同时被协议号、界面 action、screen id、资源号和物品 bit flag 使用。

## “常量但无调用”的纳入口径

本次没有把 APK 中所有 900～10000 的整数都当协议号，因为大量数值是 UI screen id、资源号、坐标或计时参数。只有满足下列至少一项才进入协议候选：

1. 出现在主网络接收 sparse-switch；
2. 作为 `main/w.a(int,...)` 的第一个参数进入发送器；
3. 写入 `a/c/r` Packet 的消息号槽并最终交给网络层。

仅在菜单判断、资源计算或普通 switch 中出现且没有上述数据流的数字不进入正式表，避免制造假协议。对于已经进入表、但没有运行调用链的项目，则明确标为未使用。

## 与当前本地服的差距

优先级建议只基于 APK 已有 UI 与发送链，不代表要求立即实现：

1. 社交与组队：1019、1056、1082、1137、1138、1158、1731。
2. 活动/副本/挑战：1050、1061、1075、1094、1153、1403。
3. 宠物、技能、修真、帮派：1071、1103、1107、1128、1132、1135。
4. 经济和背包扩展：1033、1083、1084、1092、1127。
5. 动态资源补全：1500、1504、1505、1506、1509、1511、1512、1518、1519、1520、1523、1533、1534。

实现任何一项前仍需继续追踪相应发送 action、字段类型、主接收 handler 和具体 UI 类，不能只按本文模块名构造响应。
