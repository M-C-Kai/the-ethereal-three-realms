"""Shop catalog data layer for the mall (仙晶商城 / 仙石商城).

Mirrors the existing registry style (item_registry / map_registry):
- data lives in ``data/catalog/shops.json``
- stdlib only, frozen dataclasses, validation at load time
- server.py only performs protocol/business calls

Shops are keyed by the APK ``shop_id`` derived from the screen-7 page mode:
``shop_id = (mode // 1000) * 1000`` (dp.ap()). The 仙晶 mall uses dp mode 1000
(APK dp.E(): (1000/1000)%2==1 -> currency type 1 -> property 52) and the
仙石 mall uses dp mode 2100 (type 2 -> property 49).
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from item_registry import ItemRegistry, default_item_registry


class ShopCatalogError(Exception):
    """Raised when the shop catalog is invalid."""


# bk (screen 611) tab modes -> screen-7 dp mode params.
# dp.E(mode): (mode/1000)%2 == 1 -> 仙晶(type 1), == 0 -> 仙石(type 2).
TAB_MODE_XIANJING = 2000
TAB_MODE_XIANSHI = 2100
DP_MODE_XIANJING = 1000
DP_MODE_XIANSHI = 2100

CURRENCY_PROPERTIES = {
    'immortal_stones': 49,
    'silver': 50,
    'immortal_crystals': 52,
}

MAX_SHOP_PURCHASE_QUANTITY = 99


def shop_currency_type(dp_mode: int) -> int:
    """Mirror the APK's ``dp.E(I)`` currency-type derivation."""
    mode = int(dp_mode)
    if mode == 0:
        return 0
    return 1 if (mode // 1000) % 2 == 1 else 2


@dataclass(frozen=True)
class ShopGoodsDefinition:
    template_id: int
    price: int


@dataclass(frozen=True)
class ShopCategoryDefinition:
    category_id: int
    name: str
    goods: tuple[ShopGoodsDefinition, ...]


@dataclass(frozen=True)
class ShopDefinition:
    shop_id: int
    mode: int
    name: str
    currency_property: int
    currency_name: str
    categories: tuple[ShopCategoryDefinition, ...]

    def category(self, category_id: int) -> ShopCategoryDefinition | None:
        for candidate in self.categories:
            if candidate.category_id == category_id:
                return candidate
        return None

    def find_goods(self, category_id: int, template_id: int) -> ShopGoodsDefinition | None:
        category = self.category(category_id)
        if category is None:
            return None
        for goods in category.goods:
            if goods.template_id == template_id:
                return goods
        return None


class ShopRegistry:
    """Load and validate shop definitions from ``shops.json``."""

    def __init__(self, shops_file: Path, item_registry: ItemRegistry) -> None:
        self.item_registry = item_registry
        self._shops: dict[int, ShopDefinition] = {}
        self._load(shops_file)

    def _load(self, path: Path) -> None:
        data = json.loads(path.read_text(encoding='utf-8'))
        if not isinstance(data, dict) or 'shops' not in data:
            raise ShopCatalogError(f'shops.json missing "shops" key: {path}')
        raw_shops = data['shops']
        if not isinstance(raw_shops, list):
            raise ShopCatalogError(f'shops.json "shops" must be a list: {path}')
        shops: dict[int, ShopDefinition] = {}
        seen_shop_ids: set[int] = set()
        seen_modes: set[int] = set()
        for raw in raw_shops:
            if not isinstance(raw, dict):
                raise ShopCatalogError(f'each shop must be a dict: {path}')
            mode = int(raw['mode'])
            shop_id = int(raw['shop_id'])
            expected_shop_id = (mode // 1000) * 1000
            if shop_id != expected_shop_id:
                raise ShopCatalogError(
                    f'shop_id {shop_id} inconsistent with mode {mode}: {path}'
                )
            if shop_id in seen_shop_ids or mode in seen_modes:
                raise ShopCatalogError(f'duplicate shop_id/mode: {shop_id}/{mode}')
            currency_name = str(raw['currency_name'])
            if currency_name not in CURRENCY_PROPERTIES:
                raise ShopCatalogError(f'unknown currency_name {currency_name!r}: {path}')
            currency_property = int(raw['currency_property'])
            if currency_property != CURRENCY_PROPERTIES[currency_name]:
                raise ShopCatalogError(
                    f'currency_property {currency_property} does not match'
                    f' {currency_name}: {path}'
                )
            currency_type = shop_currency_type(mode)
            expected_type = 1 if currency_property == 52 else 2
            if currency_type != expected_type:
                raise ShopCatalogError(
                    f'shop mode {mode} currency type {currency_type} does not match'
                    f' property {currency_property}: {path}'
                )
            raw_categories = raw.get('categories', [])
            if not isinstance(raw_categories, list) or not raw_categories:
                raise ShopCatalogError(f'shop {shop_id} needs categories: {path}')
            categories: list[ShopCategoryDefinition] = []
            seen_category_ids: set[int] = set()
            for raw_category in raw_categories:
                if not isinstance(raw_category, dict):
                    raise ShopCatalogError(f'each category must be a dict: {path}')
                category_id = int(raw_category['id'])
                if category_id in seen_category_ids:
                    raise ShopCatalogError(
                        f'duplicate category id {category_id} in shop {shop_id}'
                    )
                seen_category_ids.add(category_id)
                name = str(raw_category.get('name', ''))
                if not name:
                    raise ShopCatalogError(
                        f'category {category_id} in shop {shop_id} needs a name'
                    )
                raw_goods = raw_category.get('items', [])
                if not isinstance(raw_goods, list) or not raw_goods:
                    raise ShopCatalogError(
                        f'category {category_id} in shop {shop_id} needs items: {path}'
                    )
                goods: list[ShopGoodsDefinition] = []
                for raw_item in raw_goods:
                    template_id = int(raw_item['template_id'])
                    price = int(raw_item['price'])
                    if price < 0:
                        raise ShopCatalogError(
                            f'negative price for template {template_id}: {path}'
                        )
                    try:
                        self.item_registry.require(template_id)
                    except KeyError as exc:
                        raise ShopCatalogError(
                            f'shop {shop_id} sells unknown template_id {template_id}'
                        ) from exc
                    goods.append(ShopGoodsDefinition(template_id=template_id, price=price))
                categories.append(ShopCategoryDefinition(
                    category_id=category_id,
                    name=name,
                    goods=tuple(goods),
                ))
            definition = ShopDefinition(
                shop_id=shop_id,
                mode=mode,
                name=str(raw['name']),
                currency_property=currency_property,
                currency_name=currency_name,
                categories=tuple(categories),
            )
            shops[shop_id] = definition
            seen_shop_ids.add(shop_id)
            seen_modes.add(mode)
        self._shops = shops

    @property
    def shops(self) -> dict[int, ShopDefinition]:
        return self._shops

    def require(self, shop_id: int) -> ShopDefinition:
        try:
            return self._shops[int(shop_id)]
        except KeyError:
            raise KeyError(f'unknown shop_id: {shop_id}')

    def by_mode(self, dp_mode: int) -> ShopDefinition | None:
        """Find the shop whose screen-7 page mode matches ``dp_mode``."""
        if int(dp_mode) == 0:
            return None
        return self._shops.get((int(dp_mode) // 1000) * 1000)

    def find_bk_mode(self, tab_mode: int) -> ShopDefinition | None:
        """Find the shop for a screen-611 mall tab mode (2000/2100)."""
        mapping = {
            TAB_MODE_XIANJING: DP_MODE_XIANJING,
            TAB_MODE_XIANSHI: DP_MODE_XIANSHI,
        }
        dp_mode = mapping.get(int(tab_mode))
        if dp_mode is None:
            return None
        return self._shops.get((dp_mode // 1000) * 1000)


_DEFAULT_SHOPS_FILE = Path(__file__).resolve().parent / 'data' / 'catalog' / 'shops.json'


def default_shop_registry(item_registry: ItemRegistry | None = None) -> ShopRegistry:
    if item_registry is None:
        item_registry = default_item_registry()
    return ShopRegistry(_DEFAULT_SHOPS_FILE, item_registry)
