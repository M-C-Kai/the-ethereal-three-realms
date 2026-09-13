"""寄售系统静态目录：APK 原生 28 个物品分类与装备槽位映射。"""
from __future__ import annotations

CONSIGNMENT_ITEM_CATEGORIES = (
    '所有武器', '长枪', '折扇', '环器', '棍杖', '双刃', '爪刺', '剑', '刀', '笔',
    '长斧', '灯枪', '半月', '双斧', '头盔', '肩甲', '铠甲', '腰带', '腿甲', '项链',
    '披风', '护腕', '鞋子', '戒指', '坐骑', '外套', '道具', '材料',
)

# Existing equipment slots -> APK native consignment category indexes.
EQUIPMENT_SLOT_TO_CATEGORY = {
    1: 14,   # 头盔
    2: 15,   # 肩甲
    3: 16,   # 铠甲
    4: 17,   # 腰带
    5: 18,   # 腿甲
    6: 19,   # 项链
    7: 20,   # 披风
    8: 21,   # 护腕
    9: 22,   # 鞋子
    11: 23,  # 戒指
    17: 24,  # 坐骑
}
