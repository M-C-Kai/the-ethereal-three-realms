from __future__ import annotations

from protocol import TYPE_BYTE, TYPE_INT, TYPE_SHORT, byte, encode_frame, integer, short, string
from systems.shop.registry import MAX_SHOP_PURCHASE_QUANTITY, ShopCategoryDefinition, ShopDefinition, shop_currency_type

MALL_SCREEN_ID = 611
MALL_CATEGORY_SCREEN_ID = 612
SHOP_SCREEN_ID = 7
SHOP_OPEN_SCREEN_ACTION = 0x45
MALL_TAB_TO_DP_MODE = {2000: 1000, 2100: 2100}
SHOP_GOODS_HEADER_FIELDS = 7


def mall_category_list_frame(categories):
    fields = [byte(0), integer(MALL_SCREEN_ID), byte(0), byte(len(categories))]
    for category in categories:
        fields.extend((integer(category.category_id), string(category.name)))
    return encode_frame(1067, fields)


def mall_title_frame(title: str) -> bytes:
    return encode_frame(1067, [byte(2), integer(MALL_SCREEN_ID), string(title)])


def shop_screen_bridge_frame(dp_mode: int) -> bytes:
    return encode_frame(1010, [integer(0), short(0), short(0), integer(dp_mode), integer(SHOP_SCREEN_ID), short(SHOP_OPEN_SCREEN_ACTION)])


def shop_purchase_ack_frame() -> bytes:
    return encode_frame(1033, [byte(1)])


def shop_goods_list_frame(shop: ShopDefinition, category: ShopCategoryDefinition, item_registry) -> bytes:
    fields = [byte(7), integer(shop.shop_id), integer(len(category.goods)), integer(0), integer(len(category.goods)), byte(0), byte(shop_currency_type(shop.mode))]
    for goods in category.goods:
        definition = item_registry.require(goods.template_id)
        fields.extend((integer(goods.template_id), integer(goods.price), string(definition.name)))
        fields.extend(integer(0) for _ in range(4))
        if int(definition.equipment_slot) > 0:
            fields.extend(short(int(value)) for value in definition.equipment_attributes[:4])
    fields.append(string(shop.name))
    return encode_frame(1033, fields)


class ShopProtocol:
    """识别商店相关客户端请求的字段布局。"""

    @staticmethod
    def is_mall_category_request(fields: list[object]) -> bool:
        return bool(len(fields) >= 3 and fields[0].type_id == TYPE_BYTE and fields[0].value == 0 and fields[1].type_id == TYPE_INT and fields[1].value == MALL_SCREEN_ID and fields[2].type_id == TYPE_INT)

    @staticmethod
    def is_mall_title_request(fields: list[object]) -> bool:
        return bool(len(fields) >= 3 and fields[0].type_id == TYPE_BYTE and fields[0].value == 2 and fields[1].type_id == TYPE_INT and fields[1].value == MALL_SCREEN_ID and fields[2].type_id == TYPE_INT)

    @staticmethod
    def is_mall_open_category_request(fields: list[object]) -> bool:
        return bool(len(fields) >= 3 and fields[0].type_id == TYPE_BYTE and fields[0].value == 1 and fields[1].type_id == TYPE_INT and fields[1].value == MALL_CATEGORY_SCREEN_ID and fields[2].type_id == TYPE_INT)

    @staticmethod
    def is_shop_list_request(fields: list[object]) -> bool:
        return bool(len(fields) >= 5 and fields[0].type_id == TYPE_INT and fields[1].type_id == TYPE_BYTE and fields[1].value == 7 and fields[2].type_id == TYPE_SHORT and fields[3].type_id == TYPE_SHORT and fields[4].type_id == TYPE_BYTE)

    @staticmethod
    def is_shop_purchase_request(fields: list[object]) -> bool:
        return bool(len(fields) == 4 and fields[0].type_id == TYPE_INT and fields[1].type_id == TYPE_BYTE and fields[1].value == 1 and fields[2].type_id == TYPE_INT and fields[3].type_id == TYPE_SHORT and type(fields[3].value) is int and 0 < fields[3].value <= MAX_SHOP_PURCHASE_QUANTITY)


is_mall_category_request = ShopProtocol.is_mall_category_request
is_mall_title_request = ShopProtocol.is_mall_title_request
is_mall_open_category_request = ShopProtocol.is_mall_open_category_request
is_shop_list_request = ShopProtocol.is_shop_list_request
is_shop_purchase_request = ShopProtocol.is_shop_purchase_request
