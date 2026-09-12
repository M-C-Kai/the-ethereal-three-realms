"""Persistent, server-authoritative item consignment service.

The APK provides the UI and protocol; this module owns the economic state.
Items are escrowed by concrete instance ``id``. Pet consignment is deliberately
outside this module until the pet data model is implemented.
"""

from __future__ import annotations

import copy
import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any


CONSIGNMENT_OBJECT_ITEM = 1
MAX_CURRENCY_BALANCE = 2_147_483_647
DEFAULT_BAG_CAPACITY = 1000

# Native 28-category indices after the 13 weapon-family rows.
_SLOT_TO_CATEGORY = {
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
    12: 25,  # 外套
}


@dataclass(frozen=True)
class ConsignmentResult:
    changed: bool
    reason: str = ''
    listing: dict[str, Any] | None = None
    item: dict[str, Any] | None = None
    source_item: dict[str, Any] | None = None


def _role_items(role: dict[str, Any]) -> list[dict[str, Any]]:
    items = role.get('items')
    if not isinstance(items, list):
        items = []
        role['items'] = items
    return [item for item in items if isinstance(item, dict)]


def _bag_capacity(role: dict[str, Any]) -> int:
    try:
        return max(0, int(role.get('bag_capacity', DEFAULT_BAG_CAPACITY)))
    except (TypeError, ValueError):
        return DEFAULT_BAG_CAPACITY


def _bag_count(role: dict[str, Any]) -> int:
    return sum(str(item.get('location', 'bag')) == 'bag' for item in _role_items(role))


def _quality(item: dict[str, Any], registry: Any) -> int:
    resolved = registry.resolve(item)
    # APK equipment quality selector is a five-row 0..4 choice. Catalog
    # quality is authoritative where present; template low digit is the
    # original equipment fallback.
    raw = resolved.get('quality')
    try:
        value = int(raw)
    except (TypeError, ValueError):
        value = int(item.get('template_id', 0)) % 10
    if not 0 <= value <= 4:
        value = int(item.get('template_id', 0)) % 10
    return value if 0 <= value <= 4 else 0


def consignment_category_id(item: dict[str, Any], registry: Any) -> int:
    """Map one item to the APK's native item-consignment category index.

    No display-name matching is used. Equipment uses its concrete equipment
    slot and, for weapons, the template's equipment category. Non-equipment
    materials go to 27; all other ordinary items go to 26.
    """
    resolved = registry.resolve(item)
    try:
        slot = int(resolved.get('equipment_slot', 0))
    except (TypeError, ValueError):
        slot = 0
    template_id = int(item.get('template_id', resolved.get('template_id', 0)))

    if slot == 10:
        family = (template_id // 10_000_000) % 100
        return family if 1 <= family <= 13 else 1
    mapped = _SLOT_TO_CATEGORY.get(slot)
    if mapped is not None:
        return mapped

    kind = str(resolved.get('kind', '')).lower()
    if 'material' in kind or kind in {'material', 'craft_material'}:
        return 27
    return 26


class ConsignmentService:
    """Own persistent item listings and atomic in-memory transaction rules."""

    def __init__(self, path: Path | str, role_store: Any, registry: Any):
        self.path = Path(path)
        self.role_store = role_store
        self.registry = registry
        self.data: dict[str, Any] = {'next_listing_id': 1, 'listings': []}
        if self.path.exists():
            try:
                loaded = json.loads(self.path.read_text(encoding='utf-8'))
            except (OSError, ValueError) as exc:
                raise ValueError(f'寄售数据损坏: {self.path}: {exc}') from exc
            if not (
                isinstance(loaded, dict)
                and isinstance(loaded.get('listings'), list)
            ):
                raise ValueError(f'寄售数据结构非法: {self.path}')
            loaded.setdefault('next_listing_id', 1)
            self.data = loaded

    @property
    def listings(self) -> list[dict[str, Any]]:
        rows = self.data.setdefault('listings', [])
        if not isinstance(rows, list):
            raise ValueError('寄售 listings 数据结构非法')
        return rows

    def _save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_suffix(self.path.suffix + '.tmp')
        temporary.write_text(
            json.dumps(self.data, ensure_ascii=False, indent=2),
            encoding='utf-8',
        )
        temporary.replace(self.path)

    def _save_transaction(self) -> None:
        self.role_store.save()
        self._save()

    def _all_roles(self) -> list[dict[str, Any]]:
        root = getattr(self.role_store, 'data', {})
        accounts = root.get('accounts', {}) if isinstance(root, dict) else {}
        roles: list[dict[str, Any]] = []
        if not isinstance(accounts, dict):
            return roles
        for account_roles in accounts.values():
            if not isinstance(account_roles, list):
                continue
            roles.extend(role for role in account_roles if isinstance(role, dict))
        return roles

    def _find_role(self, role_id: int) -> dict[str, Any] | None:
        return next(
            (role for role in self._all_roles() if int(role.get('id', 0)) == int(role_id)),
            None,
        )

    def _find_active(self, item_instance_id: int) -> dict[str, Any] | None:
        return next(
            (
                listing for listing in self.listings
                if str(listing.get('status', '')) == 'active'
                and int(listing.get('item_instance_id', 0)) == int(item_instance_id)
            ),
            None,
        )

    def _next_instance_id(self) -> int:
        used: set[int] = set()
        for role in self._all_roles():
            for item in _role_items(role):
                try:
                    used.add(int(item.get('id', 0)))
                except (TypeError, ValueError):
                    continue
        for listing in self.listings:
            try:
                used.add(int(listing.get('item_instance_id', 0)))
            except (TypeError, ValueError):
                pass
            escrow = listing.get('item')
            if isinstance(escrow, dict):
                try:
                    used.add(int(escrow.get('id', 0)))
                except (TypeError, ValueError):
                    pass
        return max(used, default=0) + 1

    def _restore_role(self, role: dict[str, Any], snapshot: dict[str, Any]) -> None:
        role.clear()
        role.update(snapshot)

    def _rollback(
        self,
        role_snapshots: list[tuple[dict[str, Any], dict[str, Any]]],
        data_snapshot: dict[str, Any],
    ) -> None:
        for role, snapshot in role_snapshots:
            self._restore_role(role, snapshot)
        self.data = data_snapshot
        # Best effort: if one of the two prior writes succeeded, restore both
        # stores to the pre-transaction snapshot before surfacing the error.
        try:
            self.role_store.save()
            self._save()
        except Exception:
            pass

    def list_item(
        self,
        seller: dict[str, Any],
        item_instance_id: int,
        quantity: int,
        unit_price: int,
    ) -> ConsignmentResult:
        items = _role_items(seller)
        item = next(
            (candidate for candidate in items if int(candidate.get('id', 0)) == int(item_instance_id)),
            None,
        )
        if item is None or str(item.get('location', 'bag')) != 'bag':
            return ConsignmentResult(False, '物品不在背包中')
        if self._find_active(item_instance_id) is not None:
            return ConsignmentResult(False, '物品已经寄售')
        try:
            owned_quantity = int(item.get('quantity', 1))
            requested_quantity = int(quantity)
            price = int(unit_price)
        except (TypeError, ValueError):
            return ConsignmentResult(False, '数量或价格非法')
        if not 1 <= requested_quantity <= owned_quantity:
            return ConsignmentResult(False, '寄售数量非法')
        if price <= 0:
            return ConsignmentResult(False, '寄售价格必须大于零')
        # Respect explicit instance/catalog trade restrictions without
        # inventing bit meanings for the APK's opaque flag words.
        if bool(item.get('bound', False)) or item.get('tradeable') is False:
            return ConsignmentResult(False, '该物品不可交易')

        seller_snapshot = copy.deepcopy(seller)
        data_snapshot = copy.deepcopy(self.data)
        source_item: dict[str, Any] | None = None
        try:
            if requested_quantity == owned_quantity:
                items.remove(item)
                escrow = item
            else:
                source_item = item
                item['quantity'] = owned_quantity - requested_quantity
                escrow = copy.deepcopy(item)
                escrow['id'] = self._next_instance_id()
                escrow['quantity'] = requested_quantity
            escrow['location'] = 'consignment'
            listing_id = int(self.data.get('next_listing_id', 1))
            self.data['next_listing_id'] = listing_id + 1
            listing: dict[str, Any] = {
                'listing_id': listing_id,
                'seller_role_id': int(seller.get('id', 0)),
                'seller_name': str(seller.get('name', '')),
                'object_type': CONSIGNMENT_OBJECT_ITEM,
                'item_instance_id': int(escrow['id']),
                'template_id': int(escrow.get('template_id', 0)),
                'quantity': requested_quantity,
                'unit_price': price,
                'category_id': consignment_category_id(escrow, self.registry),
                'status': 'active',
                'created_at': int(time.time()),
                'expires_at': 0,
                'buyer_role_id': None,
                'sold_at': None,
                'item': escrow,
            }
            self.listings.append(listing)
            self._save_transaction()
            return ConsignmentResult(True, listing=listing, item=escrow, source_item=source_item)
        except Exception:
            self._rollback([(seller, seller_snapshot)], data_snapshot)
            raise

    def _matches_category(self, listing: dict[str, Any], category_id: int) -> bool:
        listing_category = int(listing.get('category_id', -1))
        if int(category_id) == 0:
            return 1 <= listing_category <= 13
        return listing_category == int(category_id)

    def _listing_quality(self, listing: dict[str, Any]) -> int:
        item = listing.get('item')
        if not isinstance(item, dict):
            item = {
                'id': int(listing.get('item_instance_id', 0)),
                'template_id': int(listing.get('template_id', 0)),
            }
        return _quality(item, self.registry)

    def search(
        self,
        category_id: int,
        quality: int | None = None,
        *,
        offset: int = 0,
        limit: int | None = None,
    ) -> list[dict[str, Any]]:
        rows = [
            listing for listing in self.listings
            if str(listing.get('status', '')) == 'active'
            and int(listing.get('object_type', 0)) == CONSIGNMENT_OBJECT_ITEM
            and self._matches_category(listing, int(category_id))
            and (quality is None or self._listing_quality(listing) == int(quality))
        ]
        rows.sort(key=lambda row: (int(row.get('unit_price', 0)), int(row.get('listing_id', 0))))
        start = max(0, int(offset))
        if limit is None:
            return rows[start:]
        return rows[start:start + max(0, int(limit))]

    def quality_counts(self, category_id: int) -> list[int]:
        rows = self.search(category_id)
        counts = [len(rows), 0, 0, 0, 0, 0]
        for listing in rows:
            quality = self._listing_quality(listing)
            if 0 <= quality <= 4:
                counts[quality + 1] += 1
        return counts

    def my_listings(self, role_id: int) -> list[dict[str, Any]]:
        return [
            listing for listing in self.listings
            if str(listing.get('status', '')) == 'active'
            and int(listing.get('object_type', 0)) == CONSIGNMENT_OBJECT_ITEM
            and int(listing.get('seller_role_id', 0)) == int(role_id)
        ]

    def unlist(self, seller: dict[str, Any], item_instance_id: int) -> ConsignmentResult:
        listing = self._find_active(item_instance_id)
        if listing is None:
            return ConsignmentResult(False, '寄售记录不存在或已失效')
        if int(listing.get('seller_role_id', 0)) != int(seller.get('id', 0)):
            return ConsignmentResult(False, '不能下架他人的寄售物')
        if _bag_count(seller) >= _bag_capacity(seller):
            return ConsignmentResult(False, '背包已满，无法下架')
        escrow = listing.get('item')
        if not isinstance(escrow, dict):
            return ConsignmentResult(False, '寄售物品托管状态异常')

        seller_snapshot = copy.deepcopy(seller)
        data_snapshot = copy.deepcopy(self.data)
        try:
            escrow['location'] = 'bag'
            seller.setdefault('items', []).append(escrow)
            listing['status'] = 'cancelled'
            listing['item'] = None
            self._save_transaction()
            return ConsignmentResult(True, listing=listing, item=escrow)
        except Exception:
            self._rollback([(seller, seller_snapshot)], data_snapshot)
            raise

    def buy(self, buyer: dict[str, Any], item_instance_id: int) -> ConsignmentResult:
        listing = self._find_active(item_instance_id)
        if listing is None:
            return ConsignmentResult(False, '寄售物已经售出或下架')
        seller = self._find_role(int(listing.get('seller_role_id', 0)))
        if seller is None:
            return ConsignmentResult(False, '卖家角色不存在')
        if int(seller.get('id', 0)) == int(buyer.get('id', 0)):
            return ConsignmentResult(False, '不能购买自己寄售的物品')
        if _bag_count(buyer) >= _bag_capacity(buyer):
            return ConsignmentResult(False, '背包已满，无法购买')
        escrow = listing.get('item')
        if not isinstance(escrow, dict):
            return ConsignmentResult(False, '寄售物品托管状态异常')

        quantity = max(1, int(listing.get('quantity', escrow.get('quantity', 1))))
        total_price = max(0, int(listing.get('unit_price', 0))) * quantity
        buyer_currencies = buyer.setdefault('currencies', {})
        seller_currencies = seller.setdefault('currencies', {})
        if not isinstance(buyer_currencies, dict) or not isinstance(seller_currencies, dict):
            return ConsignmentResult(False, '角色货币数据异常')
        buyer_silver = int(buyer_currencies.get('silver', 0))
        seller_silver = int(seller_currencies.get('silver', 0))
        if total_price <= 0:
            return ConsignmentResult(False, '寄售价格异常')
        if buyer_silver < total_price:
            return ConsignmentResult(False, '银两不足')
        if seller_silver + total_price > MAX_CURRENCY_BALANCE:
            return ConsignmentResult(False, '卖家银两已达上限')
        if any(
            int(item.get('id', 0)) == int(item_instance_id)
            for role in self._all_roles()
            for item in _role_items(role)
        ):
            return ConsignmentResult(False, '物品实例冲突，交易已取消')

        buyer_snapshot = copy.deepcopy(buyer)
        seller_snapshot = copy.deepcopy(seller)
        data_snapshot = copy.deepcopy(self.data)
        try:
            buyer_currencies['silver'] = buyer_silver - total_price
            seller_currencies['silver'] = seller_silver + total_price
            escrow['location'] = 'bag'
            buyer.setdefault('items', []).append(escrow)
            listing['status'] = 'sold'
            listing['buyer_role_id'] = int(buyer.get('id', 0))
            listing['sold_at'] = int(time.time())
            listing['item'] = None
            self._save_transaction()
            return ConsignmentResult(True, listing=listing, item=escrow)
        except Exception:
            snapshots = [(buyer, buyer_snapshot)]
            if seller is not buyer:
                snapshots.append((seller, seller_snapshot))
            self._rollback(snapshots, data_snapshot)
            raise
