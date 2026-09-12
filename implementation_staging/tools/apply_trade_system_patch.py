from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SERVICE = ROOT / 'consignment_service.py'
SERVER = ROOT / 'server.py'
SEED = ROOT / 'data' / 'consignment_listings.json'
DOC = ROOT / 'TRADE_SYSTEM.md'
TRADE_TEST = ROOT / 'tests' / 'test_trade_system.py'


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{label}: expected exactly one marker, got {count}')
    return text.replace(old, new, 1)


def patch_service() -> None:
    text = SERVICE.read_text(encoding='utf-8')

    text = replace_once(
        text,
        """    listing: dict[str, object] | None = None\n    item: dict[str, object] | None = None\n""",
        """    listing: dict[str, object] | None = None\n    transaction: dict[str, object] | None = None\n    item: dict[str, object] | None = None\n""",
        'result transaction field',
    )

    old_restore = """def _restore_role_in_place(role: dict[str, object], snapshot: dict[str, object]) -> None:\n    \"\"\"Restore a role while retaining existing item object identities when possible.\"\"\"\n    current_items = _role_items(role)\n    current_by_id = {\n        int(item.get('id', 0)): item\n        for item in current_items\n        if int(item.get('id', 0)) > 0\n    }\n    restored_items: list[dict[str, object]] = []\n"""
    new_restore = """def _restore_role_in_place(\n    role: dict[str, object],\n    snapshot: dict[str, object],\n    item_pool: Mapping[int, dict[str, object]] | None = None,\n) -> None:\n    \"\"\"Restore a role and preserve item identity even after cross-role moves.\"\"\"\n    # A failed purchase may already have moved the original escrow object from\n    # seller -> buyer.  A role-local lookup cannot find it when restoring the\n    # seller, so _persist supplies one cross-role object pool captured before\n    # either role is restored.\n    current_by_id: dict[int, dict[str, object]] = dict(item_pool or {})\n    current_by_id.update({\n        int(item.get('id', 0)): item\n        for item in _role_items(role)\n        if int(item.get('id', 0)) > 0\n    })\n    restored_items: list[dict[str, object]] = []\n"""
    text = replace_once(text, old_restore, new_restore, 'cross-role rollback restore helper')

    text = replace_once(
        text,
        """        self.data: dict[str, object] = {\n            'next_listing_id': 1,\n            'next_item_instance_id': 1,\n            'listings': [],\n        }\n""",
        """        self.data: dict[str, object] = {\n            'next_listing_id': 1,\n            'next_item_instance_id': 1,\n            'next_transaction_id': 1,\n            'listings': [],\n            'transactions': [],\n        }\n""",
        'initial trade store schema',
    )

    text = replace_once(
        text,
        """        if not isinstance(loaded, dict) or not isinstance(loaded.get('listings'), list):\n            return\n        loaded.setdefault('next_listing_id', 1)\n        loaded.setdefault('next_item_instance_id', 1)\n        self.data = loaded\n""",
        """        if not isinstance(loaded, dict) or not isinstance(loaded.get('listings'), list):\n            return\n        if 'transactions' in loaded and not isinstance(loaded.get('transactions'), list):\n            return\n        loaded.setdefault('next_listing_id', 1)\n        loaded.setdefault('next_item_instance_id', 1)\n        transactions = loaded.setdefault('transactions', [])\n        max_transaction_id = max(\n            (int(row.get('transaction_id', 0)) for row in transactions if isinstance(row, dict)),\n            default=0,\n        )\n        loaded['next_transaction_id'] = max(\n            int(loaded.get('next_transaction_id', 1)),\n            max_transaction_id + 1,\n            1,\n        )\n        self.data = loaded\n""",
        'trade store migration',
    )

    text = replace_once(
        text,
        """        except Exception:\n            for role, snapshot in role_snapshots:\n                _restore_role_in_place(role, snapshot)\n            self.data = copy.deepcopy(data_snapshot)\n""",
        """        except Exception:\n            # Capture original objects across every participating role before\n            # restoring either side. A buy may have already moved the exact\n            # escrow object from seller to buyer.\n            item_pool: dict[int, dict[str, object]] = {}\n            for role, _snapshot in role_snapshots:\n                for current_item in _role_items(role):\n                    current_id = int(current_item.get('id', 0))\n                    if current_id > 0:\n                        item_pool[current_id] = current_item\n            for role, snapshot in role_snapshots:\n                _restore_role_in_place(role, snapshot, item_pool)\n            self.data = copy.deepcopy(data_snapshot)\n""",
        'cross-role persistence rollback pool',
    )

    text = replace_once(
        text,
        """    def _listings(self) -> list[dict[str, object]]:\n        rows = self.data.setdefault('listings', [])\n        if not isinstance(rows, list):\n            rows = []\n            self.data['listings'] = rows\n        return rows  # type: ignore[return-value]\n\n    def _all_roles(self):\n""",
        """    def _listings(self) -> list[dict[str, object]]:\n        rows = self.data.setdefault('listings', [])\n        if not isinstance(rows, list):\n            rows = []\n            self.data['listings'] = rows\n        return rows  # type: ignore[return-value]\n\n    def _transactions(self) -> list[dict[str, object]]:\n        rows = self.data.setdefault('transactions', [])\n        if not isinstance(rows, list):\n            rows = []\n            self.data['transactions'] = rows\n        return rows  # type: ignore[return-value]\n\n    def _all_roles(self):\n""",
        'transactions collection',
    )

    text = replace_once(
        text,
        """    def _next_listing_id(self) -> int:\n        existing = [int(row.get('listing_id', 0)) for row in self._listings()]\n        value = max(max(existing, default=0) + 1, int(self.data.get('next_listing_id', 1)), 1)\n        self.data['next_listing_id'] = value + 1\n        return value\n\n    def _tradable(self, item: Mapping[str, object]) -> bool:\n""",
        """    def _next_listing_id(self) -> int:\n        existing = [int(row.get('listing_id', 0)) for row in self._listings()]\n        value = max(max(existing, default=0) + 1, int(self.data.get('next_listing_id', 1)), 1)\n        self.data['next_listing_id'] = value + 1\n        return value\n\n    def _next_transaction_id(self) -> int:\n        existing = [int(row.get('transaction_id', 0)) for row in self._transactions()]\n        value = max(\n            max(existing, default=0) + 1,\n            int(self.data.get('next_transaction_id', 1)),\n            1,\n        )\n        self.data['next_transaction_id'] = value + 1\n        return value\n\n    def _tradable(self, item: Mapping[str, object]) -> bool:\n""",
        'transaction id allocator',
    )

    text = replace_once(
        text,
        """    def category_count(self, category_id: int) -> int:\n        return len(self.search(category_id))\n\n    def unlist(self, seller: dict[str, object], item_instance_id: int) -> ConsignmentResult:\n""",
        """    def category_count(self, category_id: int) -> int:\n        return len(self.search(category_id))\n\n    def order_history(\n        self,\n        role_id: int,\n        *,\n        status: str | None = None,\n    ) -> list[dict[str, object]]:\n        \"\"\"Return one seller's complete listing lifecycle.\"\"\"\n        self._reload()\n        if status is not None and status not in VALID_STATUSES:\n            raise ValueError(f'unknown listing status: {status}')\n        target = int(role_id)\n        rows = [\n            row\n            for row in self._listings()\n            if int(row.get('seller_role_id', 0)) == target\n            and (status is None or row.get('status') == status)\n        ]\n        return sorted(rows, key=lambda row: int(row.get('listing_id', 0)))\n\n    def trade_history(\n        self,\n        role_id: int,\n        *,\n        side: str = 'all',\n    ) -> list[dict[str, object]]:\n        \"\"\"Return durable successful-trade receipts for a buyer or seller.\"\"\"\n        self._reload()\n        if side not in {'all', 'seller', 'buyer'}:\n            raise ValueError(f'unknown trade history side: {side}')\n        target = int(role_id)\n        rows: list[dict[str, object]] = []\n        for row in self._transactions():\n            seller_match = int(row.get('seller_role_id', 0)) == target\n            buyer_match = int(row.get('buyer_role_id', 0)) == target\n            if side == 'seller' and not seller_match:\n                continue\n            if side == 'buyer' and not buyer_match:\n                continue\n            if side == 'all' and not (seller_match or buyer_match):\n                continue\n            rows.append(row)\n        return sorted(rows, key=lambda row: int(row.get('transaction_id', 0)))\n\n    def unlist(self, seller: dict[str, object], item_instance_id: int) -> ConsignmentResult:\n""",
        'history query methods',
    )

    text = replace_once(
        text,
        """        listing['status'] = 'sold'\n        listing['buyer_role_id'] = int(buyer.get('id', 0))\n        listing['sold_at'] = int(time.time())\n\n        self._persist(\n            [(buyer, buyer_snapshot), (seller, seller_snapshot)],\n            data_snapshot,\n        )\n        return ConsignmentResult(True, listing=listing, item=item, total_price=total)\n""",
        """        completed_at = int(time.time())\n        listing['status'] = 'sold'\n        listing['buyer_role_id'] = int(buyer.get('id', 0))\n        listing['sold_at'] = completed_at\n\n        transaction = {\n            'transaction_id': self._next_transaction_id(),\n            'listing_id': int(listing.get('listing_id', 0)),\n            'status': 'completed',\n            'seller_role_id': int(seller.get('id', 0)),\n            'seller_name': str(seller.get('name', listing.get('seller_name', ''))),\n            'buyer_role_id': int(buyer.get('id', 0)),\n            'buyer_name': str(buyer.get('name', '')),\n            'item_instance_id': int(listing.get('item_instance_id', 0)),\n            'template_id': int(listing.get('template_id', 0)),\n            'display_name': str(listing.get('display_name', item.get('name', ''))),\n            'quantity': int(listing.get('quantity', 1)),\n            'unit_price': int(listing.get('unit_price', 0)),\n            'total_price': total,\n            'completed_at': completed_at,\n        }\n        self._transactions().append(transaction)\n\n        self._persist(\n            [(buyer, buyer_snapshot), (seller, seller_snapshot)],\n            data_snapshot,\n        )\n        return ConsignmentResult(\n            True,\n            listing=listing,\n            transaction=transaction,\n            item=item,\n            total_price=total,\n        )\n""",
        'completed transaction creation',
    )

    SERVICE.write_text(text, encoding='utf-8')


def patch_server() -> None:
    text = SERVER.read_text(encoding='utf-8')
    text = replace_once(
        text,
        """                                LOG.info(\n                                    'CONSIGNMENT_BUY_SUCCESS user=%r buyer_role_id=%d item_id=%d total=%d silver=%d',\n                                    username, role_id, item_id, result.total_price, silver,\n                                )\n""",
        """                                transaction_id = int(\n                                    (result.transaction or {}).get('transaction_id', 0)\n                                )\n                                LOG.info(\n                                    'TRADE_COMPLETED transaction_id=%d user=%r buyer_role_id=%d '\n                                    'item_id=%d total=%d silver=%d',\n                                    transaction_id, username, role_id, item_id,\n                                    result.total_price, silver,\n                                )\n""",
        'trade completion log',
    )
    SERVER.write_text(text, encoding='utf-8')


def strengthen_atomicity_test() -> None:
    text = TRADE_TEST.read_text(encoding='utf-8')
    text = replace_once(
        text,
        """        self.assertIn(item, self.seller['items'])\n        self.assertNotIn(item, self.buyer['items'])\n        self.assertEqual(item['location'], 'consignment')\n""",
        """        self.assertIn(item, self.seller['items'])\n        restored = next(row for row in self.seller['items'] if int(row['id']) == item_id)\n        self.assertIs(restored, item)\n        self.assertNotIn(item, self.buyer['items'])\n        self.assertEqual(item['location'], 'consignment')\n""",
        'atomic rollback same-object assertion',
    )
    TRADE_TEST.write_text(text, encoding='utf-8')


def write_seed_and_docs() -> None:
    SEED.write_text(
        '{\n'
        '  "next_listing_id": 1,\n'
        '  "next_item_instance_id": 1,\n'
        '  "next_transaction_id": 1,\n'
        '  "listings": [],\n'
        '  "transactions": []\n'
        '}\n',
        encoding='utf-8',
    )
    DOC.write_text(
        """# 交易系统（协议 1138）

当前交易系统以 APK 原生寄售界面为入口，但服务端按完整交易生命周期管理，而不是只做页面回包。

## 完整流程

1. **浏览**：寄售商人读取 28 个原生分类；分类点击通过 `1138/action=13` 进入筛选页，再由 `action=0/23` 请求市场列表，服务端用 `action=1` 返回有效挂单。
2. **挂售**：`action=9` 将真实背包物品转入 `consignment` 托管。整件保留原实例 ID；拆分堆叠只为拆出的托管份额分配全局唯一实例 ID。
3. **我的挂售**：`action=7` 返回当前角色仍为 `active` 的挂单。
4. **撤单**：`action=2` 将同一托管物品实例放回背包，订单变为 `cancelled`，不产生成功成交记录。
5. **购买 / 成功交易**：`action=4` 校验订单、买卖双方、银两、背包和溢出边界；成功后同时完成买家扣银、卖家加银、同一物品实例的所有权转移、订单 `sold`、唯一成交凭证 `completed`。

## 持久化模型

`data/consignment_listings.json` 同时保存：

- `listings`：挂单生命周期，状态为 `active / sold / cancelled / expired`。
- `transactions`：只记录真正完成的交易；购买失败和撤单都不会生成成交记录。
- `next_listing_id / next_item_instance_id / next_transaction_id`：独立单调 ID。

旧版本只有 `listings` 的数据文件会自动补齐交易字段，不需要清档。

## 原子性与幂等

成交把角色资产与市场流水视为一个逻辑事务。持久化失败时，买卖双方银两、物品归属与对象身份、挂单状态、成交凭证和流水 ID 全部恢复。跨角色回滚使用全局物品实例池，确保已经临时移动到买家背包的原始对象能够重新放回卖家的寄售托管，而不是复制一件等价物品。

已成交挂单不会再次出现在活动市场，因此重复购买不会二次扣款，也不会生成第二条成交记录。自购、银两不足、背包满、卖家银两溢出、托管物品缺失、非法数量或价格都会拒绝，而且不会写入 `transactions`。

宠物寄售仍保持未开放；在 APK 字段结构没有锁定前不伪造宠物交易协议。

## 服务端查询与审计

- `search(category_id)`：当前市场有效挂单。
- `my_listings(role_id)`：当前角色有效挂单。
- `order_history(role_id, status=None)`：卖家的完整挂单生命周期。
- `trade_history(role_id, side='all')`：买方 / 卖方成功成交历史。
- 成交日志统一使用 `TRADE_COMPLETED transaction_id=...`，便于真机日志和持久化成交凭证一一对应。
""",
        encoding='utf-8',
    )


def main() -> None:
    patch_service()
    patch_server()
    strengthen_atomicity_test()
    write_seed_and_docs()


if __name__ == '__main__':
    main()
