# 多怪回合与先手规则

APK evidence: B。完整解包 map-60011-render-fix-20260914-224828：
main/e.U（3456）读取 1042 的回合、sender/target INT、动作 BYTE 和效果；
main/b.a(b/b)（3969）向 m 动作向量追加记录。
main/b 的 r/s/m 队列屏障负责完成攻击、效果及归位。
既有 APK_BATTLE_CATALOG.md 锁定完整 1040/2 启动播放、短 1040/2 ACK 完成回合。

Protocol impact: 不变更 1042 字段或 1040/2 布局；一次下发全体存活单位动作。
死亡单位不再行动；胜利只在全体怪物死亡时结算，移除全部遭遇怪物。

排序业务规则由用户确认：速度降序、同速神通等级降序；全同 PvE 玩家先手、PK 被挑战者先手。
怪物之间全同采用原列表稳定顺序，这是本地兼容选择，不冒充原服。
状态 initiative 为 actor_id -> (速度, 神通等级)，不下发、不持久化。
角色速度已接入角色层 effective_character_stats 第五项，与人物 Property 48 共源，按需计算。
APK a/n.ay 标签第五项为速度；角色协议现有 44..48 属性映射不变。
未知项：怪物速度、总神通仍无完整权威数据映射；默认零表示未知，
不能用角色普通等级或猜测 stats 下标代替。排序算法已接入，真实属性接入仍待证据。
未扩展技能 AI；PK 仍沿用现有单方命令触发对方普攻的模型，非双指令收集重构。

Tests: 多怪行动、不同速度、同速神通等级、全同 PvE/PK、死亡跳过、全怪胜利。
Real-device: pending real-device verification。
