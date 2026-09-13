"""Authoritative 仙晶 order-book service for protocol 1083.

订单模型（与 APK 原生帮助文本一致）：

- 求购单 ``kind='buy'``：发布者想用银两买入仙晶。发布时托管
  ``crystals * unit_price`` 银两和委托费用；应单者交付仙晶并获得银两。
- 出售单 ``kind='sell'``：发布者想卖出仙晶换取银两。发布时托管
  ``crystals`` 仙晶和委托费用；应单者支付银两并获得仙晶。

委托费用按成交额比例在发布时以银两收取，撤单不退还（与寄售佣金语义一致）。
所有余额与订单状态由服务端校验；每次变更先深拷贝快照，任一保存异常时整体回滚。
"""

from __future__ import annotations

import copy
import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

MAX_CURRENCY = 2_147_483_647
ORDER_ACTIVE = 'active'
ORDER_FILLED = 'filled'
ORDER_CANCELLED = 'cancelled'
DEFAULT_FEE_RATE = 0.02
MIN_FEE = 1


@dataclass
class ExchangeResult:
    ok: bool
    reason: str = ''
    order: dict[str, object] | None = None
    fee: int = 0
    total: int = 0


def _currencies(role: Mapping[str, object]) -> dict[str, int]:
    currencies = role.get('currencies', {})
    if not isinstance(currencies, dict):
        currencies = {}
    return currencies  # type: ignore[return-value]


def _balance(role: Mapping[str, object], name: str) -> int:
    try:
        return max(0, int(_currencies(role).get(name, 0)))
    except (TypeError, ValueError):
        return 0


def _set_balance(role: Mapping[str, object], name: str, value: int) -> None:
    currencies = role.get('currencies')
    if not isinstance(currencies, dict):
        currencies = {}
        role['currencies'] = currencies
    currencies[name] = max(0, min(MAX_CURRENCY, int(value)))


def crystal_balance(role: Mapping[str, object]) -> int:
    return _balance(role, 'immortal_crystals')


def silver_balance(role: Mapping[str, object]) -> int:
    return _balance(role, 'silver')


def crystal_sync_properties(role: Mapping[str, object]) -> dict[int, int]:
    """1017 property pair refreshed after any exchange mutation."""
    return {
        50: silver_balance(role),
        52: crystal_balance(role),
    }


def commission_fee(crystals: int, unit_price: int, fee_rate: float) -> int:
    total = int(crystals) * int(unit_price)
    if total <= 0:
        return 0
    fee = int(round(total * float(fee_rate)))
    return max(MIN_FEE, min(fee, MAX_CURRENCY))


class ExchangeService:
    """JSON-backed 仙晶 order book shared by every connection."""

    def __init__(
        self,
        role_store: Any,
        data_file: str | Path | None = None,
        fee_rate: float = DEFAULT_FEE_RATE,
    ) -> None:
        self.role_store = role_store
        self.fee_rate = float(fee_rate)
        if data_file is None:
            data_file = Path(__file__).resolve().parents[2] / 'data' / 'exchange_orders.json'
        self.path = Path(data_file)
        self.data: dict[str, object] = {
            'next_order_id': 1,
            'next_transaction_id': 1,
            'orders': [],
            'transactions': [],
        }
        self._reload()

    # ------------------------------------------------------------------
    # 持久化
    # ------------------------------------------------------------------
    def _reload(self) -> None:
        if not self.path.exists():
            return
        try:
            loaded = json.loads(self.path.read_text(encoding='utf-8'))
        except (OSError, ValueError):
            return
        if not isinstance(loaded, dict) or not isinstance(loaded.get('orders'), list):
            return
        loaded.setdefault('next_order_id', 1)
        transactions = loaded.setdefault('transactions', [])
        if not isinstance(transactions, list):
            loaded['transactions'] = transactions = []
        loaded['next_transaction_id'] = max(
            int(loaded.get('next_transaction_id', 1)),
            max(
                (int(row.get('transaction_id', 0)) for row in transactions if isinstance(row, dict)),
                default=0,
            ) + 1,
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
            for role, snapshot in role_snapshots:
                _restore_role_in_place(role, snapshot)
            self.data = copy.deepcopy(data_snapshot)
            try:
                self.role_store.save()
                self._save()
            except Exception:
                pass
            raise

    def _orders(self) -> list[dict[str, object]]:
        rows = self.data.setdefault('orders', [])
        if not isinstance(rows, list):
            rows = []
            self.data['orders'] = rows
        return rows  # type: ignore[return-value]

    def _transactions(self) -> list[dict[str, object]]:
        rows = self.data.setdefault('transactions', [])
        if not isinstance(rows, list):
            rows = []
            self.data['transactions'] = rows
        return rows  # type: ignore[return-value]

    def _next_order_id(self) -> int:
        existing = [int(row.get('order_id', 0)) for row in self._orders()]
        value = max(max(existing, default=0) + 1, int(self.data.get('next_order_id', 1)), 1)
        self.data['next_order_id'] = value + 1
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

    # ------------------------------------------------------------------
    # 角色访问
    # ------------------------------------------------------------------
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

    # ------------------------------------------------------------------
    # 查询
    # ------------------------------------------------------------------
    def market_orders(self, tab: int) -> list[dict[str, object]]:
        """Active orders of one market tab (求购单 tab 0 / 出售单 tab 1)."""
        self._reload()
        kind = 'buy' if int(tab) == 0 else 'sell'
        return sorted(
            (row for row in self._orders() if row.get('status') == ORDER_ACTIVE and row.get('kind') == kind),
            key=lambda row: int(row.get('order_id', 0)),
        )

    def my_orders(self, role_id: int, mode: int | None = None) -> list[dict[str, object]]:
        """One role's active orders; ``mode`` filters 买入(0)/卖出(1) entry page."""
        self._reload()
        target = int(role_id)
        rows = [
            row
            for row in self._orders()
            if row.get('status') == ORDER_ACTIVE and int(row.get('poster_role_id', 0)) == target
        ]
        if mode is not None:
            kind = 'buy' if int(mode) == 0 else 'sell'
            rows = [row for row in rows if row.get('kind') == kind]
        return sorted(rows, key=lambda row: int(row.get('order_id', 0)))

    def my_order_ids(self, role_id: int, tab: int) -> list[int]:
        kind = 'buy' if int(tab) == 0 else 'sell'
        return [
            int(row.get('order_id', 0))
            for row in self.my_orders(role_id)
            if row.get('kind') == kind
        ]

    # ------------------------------------------------------------------
    # 下单 / 撤单 / 应单
    # ------------------------------------------------------------------
    def fee_quote(self, crystals: int, unit_price: int) -> ExchangeResult:
        crystals = int(crystals)
        unit_price = int(unit_price)
        if crystals <= 0 or unit_price <= 0:
            return ExchangeResult(False, 'invalid_input')
        if crystals * unit_price > MAX_CURRENCY:
            return ExchangeResult(False, 'total_overflow')
        return ExchangeResult(True, fee=commission_fee(crystals, unit_price, self.fee_rate))

    def post_order(
        self,
        poster: dict[str, object],
        kind: str,
        crystals: int,
        unit_price: int,
    ) -> ExchangeResult:
        """Post one 求购单(buy)/出售单(sell) and escrow the backing funds."""
        crystals = int(crystals)
        unit_price = int(unit_price)
        if kind not in ('buy', 'sell'):
            return ExchangeResult(False, 'invalid_kind')
        if crystals <= 0 or unit_price <= 0:
            return ExchangeResult(False, 'invalid_input')
        total = crystals * unit_price
        if total > MAX_CURRENCY:
            return ExchangeResult(False, 'total_overflow')
        fee = commission_fee(crystals, unit_price, self.fee_rate)

        if kind == 'buy':
            if silver_balance(poster) < total + fee:
                return ExchangeResult(False, 'insufficient_silver')
        else:
            if crystal_balance(poster) < crystals:
                return ExchangeResult(False, 'insufficient_crystals')
            if silver_balance(poster) < fee:
                return ExchangeResult(False, 'insufficient_silver')

        poster_snapshot = copy.deepcopy(poster)
        data_snapshot = copy.deepcopy(self.data)

        if kind == 'buy':
            _set_balance(poster, 'silver', silver_balance(poster) - total - fee)
        else:
            _set_balance(poster, 'immortal_crystals', crystal_balance(poster) - crystals)
            _set_balance(poster, 'silver', silver_balance(poster) - fee)

        order = {
            'order_id': self._next_order_id(),
            'kind': kind,
            'poster_role_id': int(poster.get('id', 0)),
            'poster_name': str(poster.get('name', '')),
            'crystals': crystals,
            'unit_price': unit_price,
            'fee': fee,
            'status': ORDER_ACTIVE,
            'created_at': int(time.time()),
            'counterparty_role_id': None,
            'finished_at': None,
        }
        self._orders().append(order)
        self._persist([(poster, poster_snapshot)], data_snapshot)
        return ExchangeResult(True, order=order, fee=fee, total=total)

    def cancel_order(self, poster: dict[str, object], order_id: int) -> ExchangeResult:
        """撤单：退还托管，委托费用不退。"""
        self._reload()
        order = self._active_order(order_id)
        if order is None or int(order.get('poster_role_id', 0)) != int(poster.get('id', 0)):
            return ExchangeResult(False, 'order_not_found')

        poster_snapshot = copy.deepcopy(poster)
        data_snapshot = copy.deepcopy(self.data)

        if order.get('kind') == 'buy':
            refund = int(order['crystals']) * int(order['unit_price'])
            if silver_balance(poster) + refund > MAX_CURRENCY:
                return ExchangeResult(False, 'silver_overflow')
            _set_balance(poster, 'silver', silver_balance(poster) + refund)
        else:
            refunded = int(order['crystals'])
            if crystal_balance(poster) + refunded > MAX_CURRENCY:
                return ExchangeResult(False, 'crystal_overflow')
            _set_balance(poster, 'immortal_crystals', crystal_balance(poster) + refunded)

        order['status'] = ORDER_CANCELLED
        order['finished_at'] = int(time.time())
        self._persist([(poster, poster_snapshot)], data_snapshot)
        return ExchangeResult(True, order=order, total=int(order['crystals']) * int(order['unit_price']))

    def accept_order(self, acceptor: dict[str, object], order_id: int) -> ExchangeResult:
        """应单：撮合一张求购单（应单者卖仙晶）或出售单（应单者买仙晶）。"""
        self._reload()
        order = self._active_order(order_id)
        if order is None:
            return ExchangeResult(False, 'order_not_found')
        poster = self.find_role(int(order.get('poster_role_id', 0)))
        if poster is None:
            return ExchangeResult(False, 'poster_not_found')
        if int(poster.get('id', 0)) == int(acceptor.get('id', 0)):
            return ExchangeResult(False, 'self_trade')

        crystals = int(order['crystals'])
        total = crystals * int(order['unit_price'])

        acceptor_snapshot = copy.deepcopy(acceptor)
        poster_snapshot = copy.deepcopy(poster)
        data_snapshot = copy.deepcopy(self.data)

        if order.get('kind') == 'buy':
            # 应单者出售仙晶：扣仙晶、得托管银两；发布者得仙晶。
            if crystal_balance(acceptor) < crystals:
                return ExchangeResult(False, 'insufficient_crystals')
            if silver_balance(acceptor) + total > MAX_CURRENCY:
                return ExchangeResult(False, 'silver_overflow')
            if crystal_balance(poster) + crystals > MAX_CURRENCY:
                return ExchangeResult(False, 'crystal_overflow')
            _set_balance(acceptor, 'immortal_crystals', crystal_balance(acceptor) - crystals)
            _set_balance(acceptor, 'silver', silver_balance(acceptor) + total)
            _set_balance(poster, 'immortal_crystals', crystal_balance(poster) + crystals)
        else:
            # 应单者购买仙晶：支付银两、得托管仙晶；发布者得银两。
            if silver_balance(acceptor) < total:
                return ExchangeResult(False, 'insufficient_silver')
            if crystal_balance(acceptor) + crystals > MAX_CURRENCY:
                return ExchangeResult(False, 'crystal_overflow')
            if silver_balance(poster) + total > MAX_CURRENCY:
                return ExchangeResult(False, 'silver_overflow')
            _set_balance(acceptor, 'silver', silver_balance(acceptor) - total)
            _set_balance(acceptor, 'immortal_crystals', crystal_balance(acceptor) + crystals)
            _set_balance(poster, 'silver', silver_balance(poster) + total)

        order['status'] = ORDER_FILLED
        order['finished_at'] = int(time.time())
        order['counterparty_role_id'] = int(acceptor.get('id', 0))

        transaction = {
            'transaction_id': self._next_transaction_id(),
            'order_id': int(order['order_id']),
            'kind': str(order.get('kind', 'buy')),
            'poster_role_id': int(order.get('poster_role_id', 0)),
            'poster_name': str(order.get('poster_name', '')),
            'acceptor_role_id': int(acceptor.get('id', 0)),
            'acceptor_name': str(acceptor.get('name', '')),
            'crystals': crystals,
            'unit_price': int(order['unit_price']),
            'total_silver': total,
            'completed_at': int(time.time()),
        }
        self._transactions().append(transaction)

        self._persist(
            [(acceptor, acceptor_snapshot), (poster, poster_snapshot)],
            data_snapshot,
        )
        return ExchangeResult(True, order=order, total=total)

    # ------------------------------------------------------------------
    def _active_order(self, order_id: int) -> dict[str, object] | None:
        target = int(order_id)
        return next(
            (
                row
                for row in self._orders()
                if int(row.get('order_id', 0)) == target and row.get('status') == ORDER_ACTIVE
            ),
            None,
        )


def _restore_role_in_place(role: dict[str, object], snapshot: dict[str, object]) -> None:
    for key in list(role):
        if key not in snapshot:
            del role[key]
    for key, value in snapshot.items():
        role[key] = copy.deepcopy(value)
