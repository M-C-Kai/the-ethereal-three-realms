"""APK-confirmed mall (仙晶/仙石商城) protocol and purchase business tests.

Reverse-engineered from the original APK:
- C->S 1067 [BYTE 0|2, INT 611, INT tab_mode] opens/switches mall tabs
  (2000=仙晶商城, 2100=仙石商城); S->C 1067 action 0 = category list,
  action 2 = title. 1067 action 1 responses are dropped by the client.
- C->S 1067 [BYTE 1, INT 612, INT category_id] clicks a category; the ONLY
  reply that opens the screen-7 shop page (pmsj/work/e/dp) is the generic
  1010/open-screen frame: [f3=INT mode, f4=INT 7, f5=SHORT 0x45].
- C->S 1033 [INT shop_id, BYTE 7, SHORT page1, SHORT page2, BYTE mode%100]
  requests the goods list; shop_id = (dp_mode/1000)*1000.
- S->C 1033 action 7 header is index-addressed: [0]=BYTE 7, [1]=INT shop_id,
  [2]=INT batch count, [3]=INT page, [4]=INT total, [5]=unread placeholder,
  [6]=BYTE currency type; goods records start at [7]; one trailing STRING.
- Purchase C->S 1033 = [INT shop_id, BYTE 1, INT item_id, SHORT quantity]
  (main/e.a(BIIS)); S->C 1033 actions 1/2 read NO further fields.
- Currency: property 50 = 银两, 52 = 仙晶, 49 = 仙石; client type 0/1/2.
"""
import copy
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from protocol import (  # noqa: E402
    TYPE_BYTE,
    TYPE_INT,
    TYPE_SHORT,
    TYPE_STRING,
    byte,
    decode_frame,
    encode_frame,
    field_values,
    integer,
    short,
    string,
)
from server import (  # noqa: E402
    MAX_SHOP_PURCHASE_QUANTITY,
    MALL_TAB_TO_DP_MODE,
    LocalGameServer,
    RoleStore,
    Settings,
    default_role,
    is_mall_category_request,
    is_mall_open_category_request,
    is_mall_title_request,
    is_shop_list_request,
    is_shop_purchase_request,
    mall_category_list_frame,
    mall_title_frame,
    role_items,
    shop_currency_type,
    shop_goods_list_frame,
    shop_purchase_ack_frame,
    shop_purchase_result,
    shop_screen_bridge_frame,
)
from shop_registry import ShopCatalogError, ShopRegistry, default_shop_registry  # noqa: E402

SHOP_XIANJING_ID = 1000
SHOP_XIANSHI_ID = 2000
DP_MODE_XIANJING = 1000
DP_MODE_XIANSHI = 2100
WEAPON_TEMPLATE_ID = 10_000_1001
ARMOUR_TEMPLATE_ID = 30_001_001
POTION_TEMPLATE_ID = 260_000_001
MOUNT_TEMPLATE_ID = 170_410_004
INITIAL_STONE_TEMPLATE_ID = 322_260_000


def _ids(fields):
    return [field.type_id for field in fields]


class ShopRegistryTests(unittest.TestCase):
    def test_default_registry_loads_both_mall_shops(self):
        registry = default_shop_registry()
        xianjing = registry.require(SHOP_XIANJING_ID)
        self.assertEqual(xianjing.name, '仙晶商城')
        self.assertEqual(xianjing.currency_property, 52)
        self.assertEqual(xianjing.currency_name, 'immortal_crystals')
        self.assertEqual(xianjing.mode, DP_MODE_XIANJING)
        xianshi = registry.require(SHOP_XIANSHI_ID)
        self.assertEqual(xianshi.name, '仙石商城')
        self.assertEqual(xianshi.currency_property, 49)
        self.assertEqual(xianshi.currency_name, 'immortal_stones')
        self.assertEqual(xianshi.mode, DP_MODE_XIANSHI)

    def test_every_goods_template_exists_in_item_registry(self):
        registry = default_shop_registry()
        items = registry.item_registry
        for shop in registry.shops.values():
            for category in shop.categories:
                for goods in category.goods:
                    definition = items.require(goods.template_id)
                    self.assertTrue(len(definition.name) > 0)

    def test_find_bk_tab_mode_maps_to_shop(self):
        registry = default_shop_registry()
        self.assertEqual(registry.find_bk_mode(2000).shop_id, SHOP_XIANJING_ID)
        self.assertEqual(registry.find_bk_mode(2100).shop_id, SHOP_XIANSHI_ID)
        self.assertIsNone(registry.find_bk_mode(1234))

    def test_mall_tab_mapping_uses_apk_modes(self):
        self.assertEqual(MALL_TAB_TO_DP_MODE, {2000: DP_MODE_XIANJING, 2100: DP_MODE_XIANSHI})

    def test_currency_type_mirrors_apk_E_derivation(self):
        self.assertEqual(shop_currency_type(0), 0)
        self.assertEqual(shop_currency_type(DP_MODE_XIANJING), 1)
        self.assertEqual(shop_currency_type(DP_MODE_XIANSHI), 2)
        self.assertEqual(shop_currency_type(3000), 1)

    def test_registry_rejects_unknown_template(self):
        with tempfile.TemporaryDirectory() as directory:
            shops_file = Path(directory) / 'shops.json'
            shops_file.write_text(
                '{"version": 1, "shops": [{"shop_id": 1000, "mode": 1000,'
                ' "name": "测试", "currency_property": 52,'
                ' "currency_name": "immortal_crystals", "categories":'
                ' [{"id": 1, "name": "分类", "items": [{"template_id": 999999999, "price": 1}]}]}]}',
                encoding='utf-8',
            )
            with self.assertRaises(ShopCatalogError):
                ShopRegistry(shops_file, default_shop_registry().item_registry)

    def test_shop_category_and_goods_lookup(self):
        registry = default_shop_registry()
        shop = registry.require(SHOP_XIANJING_ID)
        self.assertIsNone(shop.category(999))
        category = shop.category(1)
        self.assertIsNotNone(category)
        self.assertIsNone(shop.find_goods(1, INITIAL_STONE_TEMPLATE_ID))
        self.assertIsNotNone(shop.find_goods(1, WEAPON_TEMPLATE_ID))


class ShopRequestGuardTests(unittest.TestCase):
    """TLV types must be verified, not just values."""

    def test_mall_category_request_valid(self):
        fields = decode_frame(encode_frame(1067, [byte(0), integer(611), integer(2000)]))[1]
        self.assertTrue(is_mall_category_request(fields))

    def test_mall_category_request_rejects_wrong_types(self):
        fields = decode_frame(encode_frame(1067, [integer(0), integer(611), integer(2000)]))[1]
        self.assertFalse(is_mall_category_request(fields))

    def test_mall_category_request_rejects_wrong_screen_or_action(self):
        fields = decode_frame(encode_frame(1067, [byte(0), integer(612), integer(2000)]))[1]
        self.assertFalse(is_mall_category_request(fields))
        fields = decode_frame(encode_frame(1067, [byte(1), integer(611), integer(2000)]))[1]
        self.assertFalse(is_mall_category_request(fields))

    def test_mall_title_request_valid(self):
        fields = decode_frame(encode_frame(1067, [byte(2), integer(611), integer(2100)]))[1]
        self.assertTrue(is_mall_title_request(fields))

    def test_mall_title_request_rejects_wrong_types(self):
        fields = decode_frame(encode_frame(1067, [short(2), integer(611), integer(2100)]))[1]
        self.assertFalse(is_mall_title_request(fields))

    def test_mall_open_category_request_valid(self):
        fields = decode_frame(encode_frame(1067, [byte(1), integer(612), integer(1)]))[1]
        self.assertTrue(is_mall_open_category_request(fields))

    def test_mall_open_category_request_rejects_screen_611_or_wrong_types(self):
        fields = decode_frame(encode_frame(1067, [byte(1), integer(611), integer(1)]))[1]
        self.assertFalse(is_mall_open_category_request(fields))
        fields = decode_frame(encode_frame(1067, [integer(1), integer(612), integer(1)]))[1]
        self.assertFalse(is_mall_open_category_request(fields))

    def test_shop_list_request_valid(self):
        fields = decode_frame(encode_frame(1033, [
            integer(1000), byte(7), short(0), short(0), byte(0),
        ]))[1]
        self.assertTrue(is_shop_list_request(fields))

    def test_shop_list_request_rejects_wrong_types(self):
        fields = decode_frame(encode_frame(1033, [
            byte(1000), byte(7), short(0), short(0), byte(0),
        ]))[1]
        self.assertFalse(is_shop_list_request(fields))

    def test_shop_list_request_rejects_wrong_action(self):
        fields = decode_frame(encode_frame(1033, [
            integer(1000), byte(1), short(0), short(0), byte(0),
        ]))[1]
        self.assertFalse(is_shop_list_request(fields))

    def test_shop_purchase_request_valid(self):
        fields = decode_frame(encode_frame(1033, [
            integer(1000), byte(1), integer(POTION_TEMPLATE_ID), short(2),
        ]))[1]
        self.assertEqual(_ids(fields), [TYPE_INT, TYPE_BYTE, TYPE_INT, TYPE_SHORT])
        self.assertTrue(is_shop_purchase_request(fields))

    def test_shop_purchase_request_rejects_byte_quantity(self):
        fields = decode_frame(encode_frame(1033, [
            integer(1000), byte(1), integer(POTION_TEMPLATE_ID), byte(2),
        ]))[1]
        self.assertFalse(is_shop_purchase_request(fields))

    def test_shop_purchase_request_rejects_zero_or_negative_quantity(self):
        for quantity in (0, -1):
            fields = decode_frame(encode_frame(1033, [
                integer(1000), byte(1), integer(POTION_TEMPLATE_ID), short(quantity),
            ]))[1]
            self.assertFalse(is_shop_purchase_request(fields))

    def test_shop_purchase_request_rejects_wrong_action_or_length(self):
        fields = decode_frame(encode_frame(1033, [
            integer(1000), byte(2), integer(POTION_TEMPLATE_ID), short(1),
        ]))[1]
        self.assertFalse(is_shop_purchase_request(fields))
        fields = decode_frame(encode_frame(1033, [
            integer(1000), byte(1), integer(POTION_TEMPLATE_ID),
        ]))[1]
        self.assertFalse(is_shop_purchase_request(fields))


class ShopFrameTests(unittest.TestCase):
    def setUp(self):
        self.settings = Settings()
        self.registry = self.settings.shop_registry

    def test_mall_category_list_frame_layout(self):
        shop = self.registry.require(SHOP_XIANJING_ID)
        message_id, fields = decode_frame(mall_category_list_frame(shop.categories))
        self.assertEqual(message_id, 1067)
        self.assertEqual(_ids(fields[:4]), [TYPE_BYTE, TYPE_INT, TYPE_BYTE, TYPE_BYTE])
        expected_values = [0, 611, 0, len(shop.categories)]
        for category in shop.categories:
            expected_values.extend((category.category_id, category.name))
        self.assertEqual(field_values(fields), expected_values)
        self.assertEqual(_ids(fields[4:]), [TYPE_INT, TYPE_STRING] * len(shop.categories))

    def test_mall_title_frame_layout(self):
        message_id, fields = decode_frame(mall_title_frame('仙晶商城'))
        self.assertEqual(message_id, 1067)
        self.assertEqual(_ids(fields), [TYPE_BYTE, TYPE_INT, TYPE_STRING])
        self.assertEqual(field_values(fields), [2, 611, '仙晶商城'])

    def test_shop_screen_bridge_frame_layout(self):
        message_id, fields = decode_frame(shop_screen_bridge_frame(DP_MODE_XIANJING))
        self.assertEqual(message_id, 1010)
        self.assertEqual(_ids(fields), [TYPE_INT, TYPE_SHORT, TYPE_SHORT, TYPE_INT, TYPE_INT, TYPE_SHORT])
        self.assertEqual(field_values(fields), [0, 0, 0, DP_MODE_XIANJING, 7, 69])

    def test_shop_purchase_ack_frame_layout(self):
        message_id, fields = decode_frame(shop_purchase_ack_frame())
        self.assertEqual(message_id, 1033)
        self.assertEqual(_ids(fields), [TYPE_BYTE])
        self.assertEqual(field_values(fields), [1])

    def test_shop_goods_list_frame_layout(self):
        shop = self.registry.require(SHOP_XIANJING_ID)
        category = shop.category(1)
        message_id, fields = decode_frame(
            shop_goods_list_frame(shop, category, self.settings.item_registry)
        )
        self.assertEqual(message_id, 1033)
        values = field_values(fields)
        self.assertEqual(_ids(fields[:7]), [TYPE_BYTE, TYPE_INT, TYPE_INT, TYPE_INT, TYPE_INT, TYPE_BYTE, TYPE_BYTE])
        self.assertEqual(values[0], 7)
        self.assertEqual(values[1], SHOP_XIANJING_ID)
        self.assertEqual(values[2], len(category.goods))
        self.assertEqual(values[3], 0)
        self.assertEqual(values[4], len(category.goods))
        self.assertEqual(values[6], 1)
        # equipment records carry 4 extra SHORT attribute slots
        expected_tail = []
        for goods in category.goods:
            expected_tail.extend((
                TYPE_INT, TYPE_INT, TYPE_STRING,
                TYPE_INT, TYPE_INT, TYPE_INT, TYPE_INT,
            ))
            goods_definition = self.settings.item_registry.require(goods.template_id)
            if int(goods_definition.equipment_slot) > 0:
                expected_tail.extend([TYPE_SHORT] * 4)
        self.assertEqual(_ids(fields[7:-1]), expected_tail)
        self.assertEqual(_ids(fields[-1:]), [TYPE_STRING])
        self.assertEqual(values[-1], shop.name)
        # server price from the shop catalog, not item price
        first_values = values[7:7 + 7]
        self.assertEqual(first_values[0], category.goods[0].template_id)
        self.assertEqual(first_values[1], category.goods[0].price)
        self.assertEqual(
            first_values[2],
            self.settings.item_registry.require(category.goods[0].template_id).name,
        )

    def test_shop_goods_list_consumable_has_no_extra_shorts(self):
        shop = self.registry.require(SHOP_XIANJING_ID)
        category = shop.category(2)
        _, fields = decode_frame(
            shop_goods_list_frame(shop, category, self.settings.item_registry)
        )
        self.assertEqual(
            _ids(fields[7:-1]),
            [TYPE_INT, TYPE_INT, TYPE_STRING, TYPE_INT, TYPE_INT, TYPE_INT, TYPE_INT],
        )


class ShopPurchaseBusinessTests(unittest.TestCase):
    def setUp(self):
        self.settings = Settings()
        self.registry = self.settings.shop_registry
        self.role = default_role(self.settings)

    def _balance(self, role, name):
        return int((role.get('currencies') or {}).get(name, 0))

    def test_purchase_deducts_xianjing_and_creates_instance(self):
        shop = self.registry.require(SHOP_XIANJING_ID)
        goods = shop.find_goods(2, POTION_TEMPLATE_ID)
        before = self._balance(self.role, 'immortal_crystals')
        result = shop_purchase_result(
            self.role, shop, 2, POTION_TEMPLATE_ID, 2,
            item_registry=self.settings.item_registry,
        )
        self.assertTrue(result.changed)
        self.assertEqual(result.reason, '')
        self.assertEqual(
            self._balance(self.role, 'immortal_crystals'),
            before - goods.price * 2,
        )
        # the starter potion stack is at bag: quantity must have grown by 2
        stack = next(
            item for item in role_items(self.role)
            if item.get('template_id') == POTION_TEMPLATE_ID
            and item.get('location') == 'bag'
        )
        self.assertEqual(stack['quantity'], 10 + 2)
        # frames: 1017 currency + 1008 item + 1033 ack
        self.assertEqual(len(result.frames), 3)
        self.assertEqual(decode_frame(result.frames[0])[0], 1017)
        self.assertEqual(decode_frame(result.frames[1])[0], 1008)
        ack_id, ack_fields = decode_frame(result.frames[2])
        self.assertEqual((ack_id, field_values(ack_fields)), (1033, [1]))

    def test_purchase_creates_new_instance_for_non_stacked_template(self):
        shop = self.registry.require(SHOP_XIANJING_ID)
        before_ids = {int(item['id']) for item in role_items(self.role)}
        result = shop_purchase_result(
            self.role, shop, 1, WEAPON_TEMPLATE_ID, 1,
            item_registry=self.settings.item_registry,
        )
        self.assertTrue(result.changed)
        items = role_items(self.role)
        purchased = [
            item for item in items
            if item.get('template_id') == WEAPON_TEMPLATE_ID
            and int(item['id']) not in before_ids
        ]
        self.assertEqual(len(purchased), 1)
        self.assertEqual(purchased[0]['quantity'], 1)
        self.assertEqual(purchased[0]['location'], 'bag')
        # minimal instance record: template fields must not leak
        for forbidden in ('name', 'icon_code', 'equipment_slot', 'max_quantity'):
            self.assertNotIn(forbidden, purchased[0])

    def test_purchase_price_comes_from_shop_catalog(self):
        shop = self.registry.require(SHOP_XIANJING_ID)
        goods = shop.find_goods(1, WEAPON_TEMPLATE_ID)
        before = self._balance(self.role, 'immortal_crystals')
        shop_purchase_result(
            self.role, shop, 1, WEAPON_TEMPLATE_ID, 1,
            item_registry=self.settings.item_registry,
        )
        self.assertEqual(
            self._balance(self.role, 'immortal_crystals'),
            before - goods.price,
        )

    def test_insufficient_xianjing_rejected_without_mutation(self):
        shop = self.registry.require(SHOP_XIANJING_ID)
        self.role['currencies']['immortal_crystals'] = 10
        before = copy.deepcopy(self.role)
        result = shop_purchase_result(
            self.role, shop, 2, POTION_TEMPLATE_ID, 1,
            item_registry=self.settings.item_registry,
        )
        self.assertFalse(result.changed)
        self.assertNotEqual(result.reason, '')
        self.assertEqual(self.role, before)

    def test_xianshi_purchase_deducts_property_49(self):
        shop = self.registry.require(SHOP_XIANSHI_ID)
        goods = shop.find_goods(1, INITIAL_STONE_TEMPLATE_ID)
        before = self._balance(self.role, 'immortal_stones')
        result = shop_purchase_result(
            self.role, shop, 1, INITIAL_STONE_TEMPLATE_ID, 3,
            item_registry=self.settings.item_registry,
        )
        self.assertTrue(result.changed)
        self.assertEqual(
            self._balance(self.role, 'immortal_stones'),
            before - goods.price * 3,
        )

    def test_insufficient_xianshi_rejected(self):
        shop = self.registry.require(SHOP_XIANSHI_ID)
        self.role['currencies']['immortal_stones'] = 5
        before = copy.deepcopy(self.role)
        result = shop_purchase_result(
            self.role, shop, 1, INITIAL_STONE_TEMPLATE_ID, 1,
            item_registry=self.settings.item_registry,
        )
        self.assertFalse(result.changed)
        self.assertEqual(self.role, before)

    def test_quantity_zero_or_negative_or_too_large_rejected(self):
        shop = self.registry.require(SHOP_XIANJING_ID)
        before = copy.deepcopy(self.role)
        for quantity in (0, -2, MAX_SHOP_PURCHASE_QUANTITY + 1):
            result = shop_purchase_result(
                self.role, shop, 2, POTION_TEMPLATE_ID, quantity,
                item_registry=self.settings.item_registry,
            )
            self.assertFalse(result.changed, f'quantity={quantity}')
            self.assertEqual(self.role, before)

    def test_unknown_item_and_category_rejected(self):
        shop = self.registry.require(SHOP_XIANJING_ID)
        before = copy.deepcopy(self.role)
        result = shop_purchase_result(
            self.role, shop, 2, INITIAL_STONE_TEMPLATE_ID, 1,
            item_registry=self.settings.item_registry,
        )
        self.assertFalse(result.changed)
        result = shop_purchase_result(
            self.role, shop, 99, POTION_TEMPLATE_ID, 1,
            item_registry=self.settings.item_registry,
        )
        self.assertFalse(result.changed)
        self.assertEqual(self.role, before)

    def test_unknown_shop_rejected_by_boundary(self):
        with tempfile.TemporaryDirectory() as directory:
            settings = Settings(role_data_file=str(Path(directory) / 'roles.json'))
            server = LocalGameServer(settings)
            role = default_role(settings)
            before = copy.deepcopy(role)
            fields = decode_frame(encode_frame(1033, [
                integer(9999), byte(1), integer(POTION_TEMPLATE_ID), short(1),
            ]))[1]
            result = server.handle_shop_purchase(role, fields, mode=0, category_id=0)
            self.assertFalse(result.changed)
            self.assertEqual(role, before)

    def test_bag_full_blocks_new_instance_purchase(self):
        shop = self.registry.require(SHOP_XIANJING_ID)
        capacity = int(self.role['bag_capacity'])
        distinct = [
            {'id': 900000 + index, 'template_id': 260_000_100 + index,
             'quantity': 1, 'location': 'bag'}
            for index in range(capacity)
        ]
        # keep the existing potion stack, fill the rest of the bag
        self.role['items'] = [
            item for item in self.role['items'] if item.get('location') != 'bag'
        ] + distinct
        before = copy.deepcopy(self.role)
        result = shop_purchase_result(
            self.role, shop, 1, WEAPON_TEMPLATE_ID, 1,
            item_registry=self.settings.item_registry,
        )
        self.assertFalse(result.changed)
        self.assertEqual(self.role, before)

    def test_stack_limit_blocks_overflow_purchase(self):
        shop = self.registry.require(SHOP_XIANJING_ID)
        max_quantity = int(
            self.settings.item_registry.require(POTION_TEMPLATE_ID).max_quantity
        )
        stack = next(
            item for item in role_items(self.role)
            if item.get('template_id') == POTION_TEMPLATE_ID
            and item.get('location') == 'bag'
        )
        stack['quantity'] = max_quantity
        before = copy.deepcopy(self.role)
        result = shop_purchase_result(
            self.role, shop, 2, POTION_TEMPLATE_ID, 1,
            item_registry=self.settings.item_registry,
        )
        self.assertFalse(result.changed)
        self.assertEqual(self.role, before)

    def test_boundary_saves_only_mutating_purchase(self):
        with tempfile.TemporaryDirectory() as directory:
            settings = Settings(role_data_file=str(Path(directory) / 'roles.json'))
            server = LocalGameServer(settings)
            role = server.roles.roles_for('shop-persistence')[0]
            fields = decode_frame(encode_frame(1033, [
                integer(SHOP_XIANJING_ID), byte(1), integer(POTION_TEMPLATE_ID), short(1),
            ]))[1]
            with mock.patch.object(server.roles, 'save', wraps=server.roles.save) as save:
                result = server.handle_shop_purchase(
                    role, fields, mode=DP_MODE_XIANJING, category_id=2,
                )
                self.assertTrue(result.changed)
                save.assert_called_once_with()
            reloaded = RoleStore(settings).find('shop-persistence', int(role['id']))
            self.assertEqual(
                self._balance(reloaded, 'immortal_crystals'),
                10_000_000 - 50,
            )

    def test_boundary_rolls_back_memory_when_save_fails(self):
        settings = Settings()
        server = LocalGameServer(settings)
        role = default_role(settings)
        before = copy.deepcopy(role)
        fields = decode_frame(encode_frame(1033, [
            integer(SHOP_XIANJING_ID), byte(1), integer(POTION_TEMPLATE_ID), short(1),
        ]))[1]
        with mock.patch.object(server.roles, 'save', side_effect=OSError('disk full')):
            with self.assertRaises(OSError):
                server.handle_shop_purchase(
                    role, fields, mode=DP_MODE_XIANJING, category_id=2,
                )
        self.assertEqual(role, before)

    def test_boundary_rejects_malformed_request_without_save(self):
        with tempfile.TemporaryDirectory() as directory:
            settings = Settings(role_data_file=str(Path(directory) / 'roles.json'))
            server = LocalGameServer(settings)
            role = server.roles.roles_for('shop-guard')[0]
            before = copy.deepcopy(role)
            bad_fields = decode_frame(encode_frame(1033, [
                byte(1), integer(SHOP_XIANJING_ID), integer(POTION_TEMPLATE_ID), short(1),
            ]))[1]
            with mock.patch.object(server.roles, 'save', wraps=server.roles.save) as save:
                result = server.handle_shop_purchase(
                    role, bad_fields, mode=DP_MODE_XIANJING, category_id=2,
                )
                self.assertFalse(result.changed)
                save.assert_not_called()
            self.assertEqual(role, before)


if __name__ == '__main__':
    unittest.main()
