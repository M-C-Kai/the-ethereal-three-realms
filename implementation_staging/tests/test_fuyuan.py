import copy
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from protocol import byte, integer, string, decode_frame, encode_frame, TYPE_BYTE, TYPE_INT, TYPE_STRING
import fuyuan as fy


def request(*fields):
    return decode_frame(encode_frame(1054, list(fields)))[1]


class FuyuanTests(unittest.TestCase):
    def role(self, points=1000):
        role = {'id': 101, 'bag_capacity': 40, 'currencies': {'silver': 50000}}
        fy.ensure_state(role, now=1000)
        role['fuyuan']['points'] = points
        return role

    def test_migrate_once_preserves_inventory_and_zero(self):
        role = {'items': [{'id': 8}], 'currencies': {'silver': 9}}
        self.assertTrue(fy.ensure_state(role, now=1000))
        self.assertEqual(role['fuyuan']['points'], 1000)
        self.assertFalse(fy.ensure_state(role, now=1001))
        role['fuyuan']['points'] = 0
        fy.ensure_state(role, now=1002)
        self.assertEqual(role['fuyuan']['points'], 0)
        self.assertEqual(role['items'], [{'id': 8}])
        self.assertEqual(role['currencies']['silver'], 9)

    def test_settlement_keeps_partial_minutes_and_never_credits_rollback(self):
        role = self.role(3)
        self.assertFalse(fy.settle(role, now=1059))
        self.assertTrue(fy.settle(role, now=1061))
        self.assertEqual(role['fuyuan']['points'], 2)
        self.assertEqual(role['fuyuan']['settled_at'], 1060)
        self.assertFalse(fy.settle(role, now=1050))
        fy.settle(role, now=1180)
        self.assertEqual(role['fuyuan']['points'], 0)
        self.assertEqual(fy.remaining_points(role, now=5000), 0)

    def test_exact_tier_boundaries_and_offline_expiry(self):
        for points, tier in [(0,0),(1,1),(5000,1),(5001,2),(15000,2),(15001,3)]:
            role = self.role(points)
            self.assertEqual(fy.tier(role, now=1000), tier)
            self.assertEqual(fy.tier(role, now=1000+points*60), 0)

    def test_list_wire_types_pagination_and_detail(self):
        role = self.role()
        session = fy.FuyuanSession()
        replies = session.handle(role, request(byte(0), byte(0), byte(5)), now=1000)
        fields = next(decode_frame(frame)[1] for frame in replies if decode_frame(frame)[1][0].value == 0)
        self.assertEqual([f.type_id for f in fields[:4]], [TYPE_BYTE,TYPE_STRING,TYPE_BYTE,TYPE_BYTE])
        self.assertEqual([f.value for f in fields[2:4]], [17,5])
        self.assertEqual([f.type_id for f in fields[4:9]], [TYPE_INT,TYPE_STRING,TYPE_INT,TYPE_STRING,TYPE_STRING])
        detail = session.handle(role, request(byte(3),integer(fields[4].value)), now=1000)
        self.assertEqual([f.type_id for f in decode_frame(detail[0])[1]], [TYPE_BYTE,TYPE_INT,TYPE_STRING])
        page2 = session.handle(role, request(byte(0), byte(1), byte(5)), now=1000)
        ids1 = [f.value for f in fields[4::5]]
        ids2 = [f.value for f in decode_frame(page2[-1])[1][4::5]]
        self.assertFalse(set(ids1) & set(ids2))

    def test_purchase_requires_quote_confirmation_and_is_not_replayed(self):
        role = self.role()
        session = fy.FuyuanSession()
        replies = session.handle(role, request(byte(4)), now=1000)
        self.assertEqual(role['currencies']['silver'], 50000)
        row_id = decode_frame(replies[-1])[1][4].value
        confirm = request(byte(2), integer(338), byte(0), integer(row_id), byte(0))
        session.handle(role, confirm, now=1001)
        self.assertEqual(role['fuyuan']['points'], 2000)
        self.assertEqual(role['currencies']['silver'], 49000)
        session.handle(role, confirm, now=1002)
        self.assertEqual(role['currencies']['silver'], 49000)

    def test_insufficient_balance_cancel_and_expired_quote_do_not_charge(self):
        for kind in ['balance','cancel','expired','forged']:
            role = self.role()
            session = fy.FuyuanSession()
            frames = session.handle(role, request(byte(4)), now=1000)
            row_id = decode_frame(frames[-1])[1][4].value
            if kind == 'balance': role['currencies']['silver'] = 0
            original_balance = role['currencies']['silver']
            session.handle(role, request(byte(2), integer(338), byte(0), integer(row_id + (999 if kind == 'forged' else 0)), byte(1 if kind == 'cancel' else 0)), now=1201 if kind == 'expired' else 1001)
            self.assertEqual(role['currencies']['silver'], original_balance)
            self.assertEqual(role['fuyuan'].get('purchased_points',0), 0)

    def test_upgrade_has_real_tier_and_quoted_price(self):
        role = self.role(1000)
        session = fy.FuyuanSession()
        frames = session.handle(role, request(byte(5)), now=1000)
        fields = decode_frame(frames[-1])[1]
        session.handle(role, request(byte(2),integer(338),byte(0),integer(fields[4].value),byte(0)), now=1001)
        self.assertEqual(fy.tier(role, now=1001), 2)
        self.assertEqual(role['currencies']['silver'], 45999)

    def test_wrong_types_unknown_actions_and_logout_cannot_purchase(self):
        role = self.role()
        session = fy.FuyuanSession()
        before = copy.deepcopy(role)
        for fields in [request(integer(4)),request(byte(4),integer(1)),request(byte(8)),request(byte(2),integer(338),integer(0),integer(9001),byte(0))]:
            self.assertEqual(session.handle(role, fields, now=1000), [])
        self.assertEqual(role, before)

    def test_server_stats_and_capacity_expire_without_item_deletion(self):
        import server
        role = server.default_role(server.Settings())
        role['fuyuan'].update(points=15001, settled_at=int(time.time()))
        base_capacity = role['bag_capacity']
        self.assertEqual(server.bag_capacity(role), base_capacity+20)
        values = [f.value for f in decode_frame(server.player_info(server.Settings(),role))[1]]
        self.assertEqual(values[25],3)
        self.assertEqual(values[41],server.combat_stats(role).max_hp)
        items = copy.deepcopy(role['items'])
        role['fuyuan']['points'] = 0
        self.assertEqual(server.bag_capacity(role),base_capacity)
        self.assertEqual(items,role['items'])

    def test_battle_experience_bonus_is_once_and_uses_floor(self):
        import server
        role = server.default_role(server.Settings())
        role['auto_level'] = False
        server.apply_battle_rewards(role, experience=50)
        self.assertEqual(role['experience'],52)
        role['fuyuan']['points'] = 0
        server.apply_battle_rewards(role, experience=50)
        self.assertEqual(role['experience'],102)


if __name__ == '__main__':
    unittest.main()
