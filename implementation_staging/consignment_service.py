"""Persistent real-item escrow and transactions for protocol 1138."""
from __future__ import annotations
import copy
import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

CONSIGNMENT_LOCATION = 'consignment'
ACTIVE = 'active'
VALID_STATUSES = {'active', 'sold', 'cancelled', 'expired'}
DEFAULT_BAG_CAPACITY = 1000
MAX_SILVER = 2_147_483_647

EQUIPMENT_SLOT_TO_CATEGORY = {
    1: 14, 2: 15, 3: 16, 4: 17, 5: 18, 6: 19, 7: 20,
    8: 21, 9: 22, 11: 23, 17: 24,
}

@dataclass
class ConsignmentResult:
    ok: bool
    reason: str = ''
    listing: dict[str, object] | None = None
    item: dict[str, object] | None = None
    source_item: dict[str, object] | None = None
    removed_from_bag: bool = False
    total_price: int = 0

def _role_items(role: Mapping[str, object]) -> list[dict[str, object]]:
    items = role.get('items', [])
    return items if isinstance(items, list) else []  # type: ignore[return-value]

def _bag_count(role: Mapping[str, object]) -> int:
    return sum(str(item.get('location', 'bag')) == 'bag' for item in _role_items(role))

def _bag_capacity(role: Mapping[str, object]) -> int:
    try:
        return max(0, int(role.get('bag_capacity', DEFAULT_BAG_CAPACITY)))
    except (TypeError, ValueError):
        return DEFAULT_BAG_CAPACITY

def _silver(role: Mapping[str, object]) -> int:
    currencies = role.get('currencies', {})
    if not isinstance(currencies, dict):
        return 0
    try:
        return max(0, int(currencies.get('silver', 0)))
    except (TypeError, ValueError):
        return 0

def _set_silver(role: dict[str, object], value: int) -> None:
    currencies = role.get('currencies')
    if not isinstance(currencies, dict):
        currencies = {}
        role['currencies'] = currencies
    currencies['silver'] = max(0, min(MAX_SILVER, int(value)))

def consignment_category_for_item(item: Mapping[str, object], registry: Any) -> int:
    resolved = registry.resolve(dict(item))
    slot = int(resolved.get('equipment_slot', item.get('equipment_slot', 0)) or 0)
    if slot == 10:
        icon = int(resolved.get('icon_code', item.get('icon_code', 0)) or 0)
        group = (icon // 100) % 100
        if 21 <= group <= 33:
            return group - 20
        return 0
    if slot in EQUIPMENT_SLOT_TO_CATEGORY:
        return EQUIPMENT_SLOT_TO_CATEGORY[slot]
    text = f"{resolved.get('kind', item.get('kind', ''))} {resolved.get('name', item.get('name', ''))}".lower()
    if '外套' in text or 'outerwear' in text:
        return 25
    if any(token in text for token in ('材料', 'material', '矿石', '碎片', '药材')):
        return 27
    return 26

class ConsignmentService:
    def __init__(self, role_store: Any, item_registry: Any, data_file: str | Path | None = None):
        self.role_store = role_store
        self.item_registry = item_registry
        if data_file is None:
            data_file = Path(__file__).resolve().parent / 'data' / 'consignment_listings.json'
        self.path = Path(data_file)
        self.data: dict[str, object] = {'next_listing_id': 1, 'next_item_instance_id': 1, 'listings': []}
        self._reload()

    def _reload(self) -> None:
        if not self.path.exists():
            return
        try:
            loaded = json.loads(self.path.read_text(encoding='utf-8'))
        except (OSError, ValueError):
            return
        if isinstance(loaded, dict) and isinstance(loaded.get('listings'), list):
            self.data = loaded

    def _save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(self.path.suffix + '.tmp')
        tmp.write_text(json.dumps(self.data, ensure_ascii=False, indent=2), encoding='utf-8')
        tmp.replace(self.path)

    def _persist(self, role_snapshots: list[tuple[dict[str, object], dict[str, object]]], data_snapshot: dict[str, object]) -> None:
        try:
            self.role_store.save()
            self._save()
        except Exception:
            for role, snapshot in role_snapshots:
                role.clear(); role.update(copy.deepcopy(snapshot))
            self.data = copy.deepcopy(data_snapshot)
            try:
                self.role_store.save(); self._save()
            except Exception:
                pass
            raise

    def _listings(self) -> list[dict[str, object]]:
        rows = self.data.setdefault('listings', [])
        if not isinstance(rows, list):
            rows = []; self.data['listings'] = rows
        return rows  # type: ignore[return-value]

    def _all_roles(self):
        accounts = self.role_store.data.get('accounts', {})
        if not isinstance(accounts, dict):
            return
        for roles in accounts.values():
            if isinstance(roles, list):
                for role in roles:
                    if isinstance(role, dict):
                        yield role

    def find_role(self, role_id: int) -> dict[str, object] | None:
        return next((r for r in self._all_roles() if int(r.get('id', 0)) == int(role_id)), None)

    def _find_item(self, role: Mapping[str, object], item_id: int) -> dict[str, object] | None:
        return next((i for i in _role_items(role) if int(i.get('id', 0)) == int(item_id)), None)

    def _listing(self, item_instance_id: int) -> dict[str, object] | None:
        return next((row for row in self._listings()
                     if int(row.get('item_instance_id', 0)) == int(item_instance_id)
                     and row.get('status') == ACTIVE), None)

    def _next_item_id(self) -> int:
        used = {int(i.get('id', 0)) for role in self._all_roles() for i in _role_items(role) if int(i.get('id', 0)) > 0}
        floor = max(used, default=0) + 1
        candidate = max(floor, int(self.data.get('next_item_instance_id', 1)))
        while candidate in used:
            candidate += 1
        self.data['next_item_instance_id'] = candidate + 1
        return candidate

    def _next_listing_id(self) -> int:
        value = max(1, int(self.data.get('next_listing_id', 1)))
        self.data['next_listing_id'] = value + 1
        return value

    def _tradable(self, item: Mapping[str, object]) -> bool:
        if str(item.get('location', 'bag')) != 'bag':
            return False
        if any(bool(item.get(key, False)) for key in ('bound', 'is_bound', 'binding')):
            return False
        resolved = self.item_registry.resolve(dict(item))
        if resolved.get('tradable') is False or resolved.get('can_trade') is False:
            return False
        kind = str(resolved.get('kind', '')).lower()
        if '任务' in kind or kind == 'task':
            return False
        return True

    def list_item(self, seller: dict[str, object], instance_id: int, quantity: int, unit_price: int) -> ConsignmentResult:
        self._reload()
        item = self._find_item(seller, instance_id)
        if item is None or not self._tradable(item):
            return ConsignmentResult(False, 'item_not_tradable')
        owned = int(item.get('quantity', 1))
        quantity = int(quantity); unit_price = int(unit_price)
        if quantity <= 0 or quantity > owned:
            return ConsignmentResult(False, 'invalid_quantity')
        if unit_price <= 0 or unit_price > MAX_SILVER:
            return ConsignmentResult(False, 'invalid_price')
        category = consignment_category_for_item(item, self.item_registry)
        resolved = self.item_registry.resolve(item)
        seller_snapshot = copy.deepcopy(seller); data_snapshot = copy.deepcopy(self.data)
        removed = quantity == owned
        if removed:
            escrow_item = item
            escrow_item['location'] = CONSIGNMENT_LOCATION
        else:
            item['quantity'] = owned - quantity
            escrow_item = copy.deepcopy(item)
            escrow_item['id'] = self._next_item_id()
            escrow_item['quantity'] = quantity
            escrow_item['location'] = CONSIGNMENT_LOCATION
            _role_items(seller).append(escrow_item)
        listing = {
            'listing_id': self._next_listing_id(),
            'seller_role_id': int(seller.get('id', 0)),
            'seller_name': str(seller.get('name', '')),
            'item_instance_id': int(escrow_item['id']),
            'template_id': int(escrow_item.get('template_id', 0)),
            'quantity': int(escrow_item.get('quantity', 1)),
            'unit_price': unit_price,
            'category_id': category,
            'display_name': str(resolved.get('name', escrow_item.get('name', ''))),
            'status': ACTIVE,
            'created_at': int(time.time()),
            'expires_at': 0,
            'buyer_role_id': None,
            'sold_at': None,
        }
        self._listings().append(listing)
        self._persist([(seller, seller_snapshot)], data_snapshot)
        return ConsignmentResult(True, listing=listing, item=escrow_item,
                                 source_item=None if removed else item,
                                 removed_from_bag=removed,
                                 total_price=unit_price * quantity)

    def search(self, category_id: int) -> list[dict[str, object]]:
        self._reload(); category_id = int(category_id)
        rows = [row for row in self._listings() if row.get('status') == ACTIVE]
        if category_id == 0:
            rows = [row for row in rows if 0 <= int(row.get('category_id', -1)) <= 13]
        else:
            rows = [row for row in rows if int(row.get('category_id', -1)) == category_id]
        return sorted(rows, key=lambda row: int(row.get('listing_id', 0)))

    def my_listings(self, role_id: int) -> list[dict[str, object]]:
        self._reload()
        return [row for row in self._listings()
                if row.get('status') == ACTIVE and int(row.get('seller_role_id', 0)) == int(role_id)]

    def category_count(self, category_id: int) -> int:
        return len(self.search(category_id))

    def unlist(self, seller: dict[str, object], item_instance_id: int) -> ConsignmentResult:
        self._reload(); listing = self._listing(item_instance_id)
        if listing is None or int(listing.get('seller_role_id', 0)) != int(seller.get('id', 0)):
            return ConsignmentResult(False, 'listing_not_found')
        item = self._find_item(seller, item_instance_id)
        if item is None or item.get('location') != CONSIGNMENT_LOCATION:
            return ConsignmentResult(False, 'escrow_item_missing')
        if _bag_count(seller) >= _bag_capacity(seller):
            return ConsignmentResult(False, 'bag_full')
        seller_snapshot = copy.deepcopy(seller); data_snapshot = copy.deepcopy(self.data)
        item['location'] = 'bag'; listing['status'] = 'cancelled'
        self._persist([(seller, seller_snapshot)], data_snapshot)
        return ConsignmentResult(True, listing=listing, item=item)

    def buy(self, buyer: dict[str, object], item_instance_id: int) -> ConsignmentResult:
        self._reload(); listing = self._listing(item_instance_id)
        if listing is None:
            return ConsignmentResult(False, 'listing_not_found')
        seller = self.find_role(int(listing.get('seller_role_id', 0)))
        if seller is None:
            return ConsignmentResult(False, 'seller_not_found')
        if int(seller.get('id', 0)) == int(buyer.get('id', 0)):
            return ConsignmentResult(False, 'self_purchase')
        item = self._find_item(seller, item_instance_id)
        if item is None or item.get('location') != CONSIGNMENT_LOCATION:
            return ConsignmentResult(False, 'escrow_item_missing')
        total = int(listing.get('unit_price', 0)) * int(listing.get('quantity', 1))
        if total <= 0 or _silver(buyer) < total:
            return ConsignmentResult(False, 'insufficient_silver')
        if _bag_count(buyer) >= _bag_capacity(buyer):
            return ConsignmentResult(False, 'bag_full')
        if _silver(seller) + total > MAX_SILVER:
            return ConsignmentResult(False, 'seller_silver_overflow')
        buyer_snapshot = copy.deepcopy(buyer); seller_snapshot = copy.deepcopy(seller); data_snapshot = copy.deepcopy(self.data)
        _set_silver(buyer, _silver(buyer) - total); _set_silver(seller, _silver(seller) + total)
        _role_items(seller).remove(item); item['location'] = 'bag'; _role_items(buyer).append(item)
        listing['status'] = 'sold'; listing['buyer_role_id'] = int(buyer.get('id', 0)); listing['sold_at'] = int(time.time())
        self._persist([(buyer, buyer_snapshot), (seller, seller_snapshot)], data_snapshot)
        return ConsignmentResult(True, listing=listing, item=item, total_price=total)
