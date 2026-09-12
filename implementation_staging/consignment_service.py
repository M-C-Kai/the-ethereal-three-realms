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


@dataclass
class ConsignmentResult:
    ok: bool
    reason: str = ''
    listing: dict[str, object] | None = None
    transaction: dict[str, object] | None = None
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


def _restore_role_in_place(
    role: dict[str, object],
    snapshot: dict[str, object],
    item_pool: Mapping[int, dict[str, object]] | None = None,
) -> None:
    """Restore a role and preserve item identity even after cross-role moves."""
    # A failed purchase may already have moved the original escrow object from
    # seller -> buyer.  A role-local lookup cannot find it when restoring the
    # seller, so _persist supplies one cross-role object pool captured before
    # either role is restored.
    current_by_id: dict[int, dict[str, object]] = dict(item_pool or {})
    current_by_id.update({
        int(item.get('id', 0)): item
        for item in _role_items(role)
        if int(item.get('id', 0)) > 0
    })
    restored_items: list[dict[str, object]] = []
    snapshot_items = snapshot.get('items', [])
    if isinstance(snapshot_items, list):
        for raw in snapshot_items:
            if not isinstance(raw, dict):
                continue
            item_id = int(raw.get('id', 0))
            item = current_by_id.get(item_id)
            if item is None:
                item = copy.deepcopy(raw)
            else:
                item.clear()
                item.update(copy.deepcopy(raw))
            restored_items.append(item)

    for key in list(role):
        if key != 'items' and key not in snapshot:
            del role[key]
    for key, value in snapshot.items():
        if key == 'items':
            continue
        role[key] = copy.deepcopy(value)
    role['items'] = restored_items


def consignment_category_for_item(item: Mapping[str, object], registry: Any) -> int:
    """Map one server item to the APK's 28 native item-consignment categories."""
    resolved = registry.resolve(dict(item))
    slot = int(resolved.get('equipment_slot', item.get('equipment_slot', 0)) or 0)

    # Weapon slot: icon-code hundreds group 21..33 maps to categories 1..13.
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
    """Authoritative item-consignment service backed by role data + JSON listings."""

    def __init__(self, role_store: Any, item_registry: Any, data_file: str | Path | None = None):
        self.role_store = role_store
        self.item_registry = item_registry
        if data_file is None:
            data_file = Path(__file__).resolve().parent / 'data' / 'consignment_listings.json'
        self.path = Path(data_file)
        self.data: dict[str, object] = {
            'next_listing_id': 1,
            'next_item_instance_id': 1,
            'next_transaction_id': 1,
            'listings': [],
            'transactions': [],
        }
        self._reload()

    def _reload(self) -> None:
        if not self.path.exists():
            return
        try:
            loaded = json.loads(self.path.read_text(encoding='utf-8'))
        except (OSError, ValueError):
            return
        if not isinstance(loaded, dict) or not isinstance(loaded.get('listings'), list):
            return
        if 'transactions' in loaded and not isinstance(loaded.get('transactions'), list):
            return
        loaded.setdefault('next_listing_id', 1)
        loaded.setdefault('next_item_instance_id', 1)
        transactions = loaded.setdefault('transactions', [])
        max_transaction_id = max(
            (int(row.get('transaction_id', 0)) for row in transactions if isinstance(row, dict)),
            default=0,
        )
        loaded['next_transaction_id'] = max(
            int(loaded.get('next_transaction_id', 1)),
            max_transaction_id + 1,
            1,
        )
        self.data = loaded

    def _save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(self.path.suffix + '.tmp')
        tmp.write_text(json.dumps(self.data, ensure_ascii=False, indent=2), encoding='utf-8')
        tmp.replace(self.path)

    def _persist(
        self,
        role_snapshots: list[tuple[dict[str, object], dict[str, object]]],
        data_snapshot: dict[str, object],
    ) -> None:
        try:
            self.role_store.save()
            self._save()
        except Exception:
            # Capture original objects across every participating role before
            # restoring either side. A buy may have already moved the exact
            # escrow object from seller to buyer.
            item_pool: dict[int, dict[str, object]] = {}
            for role, _snapshot in role_snapshots:
                for current_item in _role_items(role):
                    current_id = int(current_item.get('id', 0))
                    if current_id > 0:
                        item_pool[current_id] = current_item
            for role, snapshot in role_snapshots:
                _restore_role_in_place(role, snapshot, item_pool)
            self.data = copy.deepcopy(data_snapshot)
            # Best-effort repair of persistent state. Never mask the original failure.
            try:
                self.role_store.save()
                self._save()
            except Exception:
                pass
            raise

    def _listings(self) -> list[dict[str, object]]:
        rows = self.data.setdefault('listings', [])
        if not isinstance(rows, list):
            rows = []
            self.data['listings'] = rows
        return rows  # type: ignore[return-value]

    def _transactions(self) -> list[dict[str, object]]:
        rows = self.data.setdefault('transactions', [])
        if not isinstance(rows, list):
            rows = []
            self.data['transactions'] = rows
        return rows  # type: ignore[return-value]

    def _all_roles(self):
        accounts = self.role_store.data.get('accounts', {})
        if not isinstance(accounts, dict):
            return
        for roles in accounts.values():
            if not isinstance(roles, list):
                continue
            for role in roles:
                if isinstance(role, dict):
                    yield role

    def find_role(self, role_id: int) -> dict[str, object] | None:
        target = int(role_id)
        return next((role for role in self._all_roles() if int(role.get('id', 0)) == target), None)

    def _find_item(self, role: Mapping[str, object], item_id: int) -> dict[str, object] | None:
        target = int(item_id)
        return next((item for item in _role_items(role) if int(item.get('id', 0)) == target), None)

    def _listing(self, item_instance_id: int) -> dict[str, object] | None:
        target = int(item_instance_id)
        return next(
            (
                row
                for row in self._listings()
                if int(row.get('item_instance_id', 0)) == target and row.get('status') == ACTIVE
            ),
            None,
        )

    def _next_item_id(self) -> int:
        used = {
            int(item.get('id', 0))
            for role in self._all_roles()
            for item in _role_items(role)
            if int(item.get('id', 0)) > 0
        }
        used.update(
            int(row.get('item_instance_id', 0))
            for row in self._listings()
            if int(row.get('item_instance_id', 0)) > 0
        )
        floor = max(used, default=0) + 1
        candidate = max(floor, int(self.data.get('next_item_instance_id', 1)))
        while candidate in used:
            candidate += 1
        self.data['next_item_instance_id'] = candidate + 1
        return candidate

    def _next_listing_id(self) -> int:
        existing = [int(row.get('listing_id', 0)) for row in self._listings()]
        value = max(max(existing, default=0) + 1, int(self.data.get('next_listing_id', 1)), 1)
        self.data['next_listing_id'] = value + 1
        return value

    def _next_transaction_id(self) -> int:
        existing = [int(row.get('transaction_id', 0)) for row in self._transactions()]
        value = max(
            max(existing, default=0) + 1,
            int(self.data.get('next_transaction_id', 1)),
            1,
        )
        self.data['next_transaction_id'] = value + 1
        return value

    def _tradable(self, item: Mapping[str, object]) -> bool:
        if str(item.get('location', 'bag')) != 'bag':
            return False
        if any(bool(item.get(key, False)) for key in ('bound', 'is_bound', 'binding')):
            return False
        resolved = self.item_registry.resolve(dict(item))
        if resolved.get('tradable') is False or resolved.get('can_trade') is False:
            return False
        text = f"{resolved.get('kind', item.get('kind', ''))} {resolved.get('name', item.get('name', ''))}".lower()
        if '任务' in text or 'task' in text:
            return False
        return True

    def list_item(
        self,
        seller: dict[str, object],
        instance_id: int,
        quantity: int,
        unit_price: int,
    ) -> ConsignmentResult:
        self._reload()
        item = self._find_item(seller, instance_id)
        if item is None or not self._tradable(item):
            return ConsignmentResult(False, 'item_not_tradable')

        owned = int(item.get('quantity', 1))
        quantity = int(quantity)
        unit_price = int(unit_price)
        if quantity <= 0 or quantity > owned:
            return ConsignmentResult(False, 'invalid_quantity')
        if unit_price <= 0 or unit_price > MAX_SILVER:
            return ConsignmentResult(False, 'invalid_price')
        if unit_price * quantity > MAX_SILVER:
            return ConsignmentResult(False, 'price_overflow')

        category = consignment_category_for_item(item, self.item_registry)
        resolved = self.item_registry.resolve(item)
        seller_snapshot = copy.deepcopy(seller)
        data_snapshot = copy.deepcopy(self.data)

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
        return ConsignmentResult(
            True,
            listing=listing,
            item=escrow_item,
            source_item=None if removed else item,
            removed_from_bag=removed,
            total_price=unit_price * quantity,
        )

    def search(self, category_id: int) -> list[dict[str, object]]:
        self._reload()
        category_id = int(category_id)
        rows = [row for row in self._listings() if row.get('status') == ACTIVE]
        if category_id == 0:
            rows = [row for row in rows if 0 <= int(row.get('category_id', -1)) <= 13]
        else:
            rows = [row for row in rows if int(row.get('category_id', -1)) == category_id]
        return sorted(rows, key=lambda row: int(row.get('listing_id', 0)))

    def my_listings(self, role_id: int) -> list[dict[str, object]]:
        self._reload()
        target = int(role_id)
        return sorted(
            [
                row
                for row in self._listings()
                if row.get('status') == ACTIVE and int(row.get('seller_role_id', 0)) == target
            ],
            key=lambda row: int(row.get('listing_id', 0)),
        )

    def category_count(self, category_id: int) -> int:
        return len(self.search(category_id))

    def order_history(
        self,
        role_id: int,
        *,
        status: str | None = None,
    ) -> list[dict[str, object]]:
        """Return one seller's complete listing lifecycle."""
        self._reload()
        if status is not None and status not in VALID_STATUSES:
            raise ValueError(f'unknown listing status: {status}')
        target = int(role_id)
        rows = [
            row
            for row in self._listings()
            if int(row.get('seller_role_id', 0)) == target
            and (status is None or row.get('status') == status)
        ]
        return sorted(rows, key=lambda row: int(row.get('listing_id', 0)))

    def trade_history(
        self,
        role_id: int,
        *,
        side: str = 'all',
    ) -> list[dict[str, object]]:
        """Return durable successful-trade receipts for a buyer or seller."""
        self._reload()
        if side not in {'all', 'seller', 'buyer'}:
            raise ValueError(f'unknown trade history side: {side}')
        target = int(role_id)
        rows: list[dict[str, object]] = []
        for row in self._transactions():
            seller_match = int(row.get('seller_role_id', 0)) == target
            buyer_match = int(row.get('buyer_role_id', 0)) == target
            if side == 'seller' and not seller_match:
                continue
            if side == 'buyer' and not buyer_match:
                continue
            if side == 'all' and not (seller_match or buyer_match):
                continue
            rows.append(row)
        return sorted(rows, key=lambda row: int(row.get('transaction_id', 0)))

    def unlist(self, seller: dict[str, object], item_instance_id: int) -> ConsignmentResult:
        self._reload()
        listing = self._listing(item_instance_id)
        if listing is None or int(listing.get('seller_role_id', 0)) != int(seller.get('id', 0)):
            return ConsignmentResult(False, 'listing_not_found')
        item = self._find_item(seller, item_instance_id)
        if item is None or item.get('location') != CONSIGNMENT_LOCATION:
            return ConsignmentResult(False, 'escrow_item_missing')
        if _bag_count(seller) >= _bag_capacity(seller):
            return ConsignmentResult(False, 'bag_full')

        seller_snapshot = copy.deepcopy(seller)
        data_snapshot = copy.deepcopy(self.data)
        item['location'] = 'bag'
        listing['status'] = 'cancelled'
        self._persist([(seller, seller_snapshot)], data_snapshot)
        return ConsignmentResult(True, listing=listing, item=item)

    def buy(self, buyer: dict[str, object], item_instance_id: int) -> ConsignmentResult:
        self._reload()
        listing = self._listing(item_instance_id)
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

        buyer_snapshot = copy.deepcopy(buyer)
        seller_snapshot = copy.deepcopy(seller)
        data_snapshot = copy.deepcopy(self.data)

        _set_silver(buyer, _silver(buyer) - total)
        _set_silver(seller, _silver(seller) + total)
        _role_items(seller).remove(item)
        item['location'] = 'bag'
        _role_items(buyer).append(item)
        completed_at = int(time.time())
        listing['status'] = 'sold'
        listing['buyer_role_id'] = int(buyer.get('id', 0))
        listing['sold_at'] = completed_at

        transaction = {
            'transaction_id': self._next_transaction_id(),
            'listing_id': int(listing.get('listing_id', 0)),
            'status': 'completed',
            'seller_role_id': int(seller.get('id', 0)),
            'seller_name': str(seller.get('name', listing.get('seller_name', ''))),
            'buyer_role_id': int(buyer.get('id', 0)),
            'buyer_name': str(buyer.get('name', '')),
            'item_instance_id': int(listing.get('item_instance_id', 0)),
            'template_id': int(listing.get('template_id', 0)),
            'display_name': str(listing.get('display_name', item.get('name', ''))),
            'quantity': int(listing.get('quantity', 1)),
            'unit_price': int(listing.get('unit_price', 0)),
            'total_price': total,
            'completed_at': completed_at,
        }
        self._transactions().append(transaction)

        self._persist(
            [(buyer, buyer_snapshot), (seller, seller_snapshot)],
            data_snapshot,
        )
        return ConsignmentResult(
            True,
            listing=listing,
            transaction=transaction,
            item=item,
            total_price=total,
        )
