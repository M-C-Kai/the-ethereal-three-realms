"""统一测试：技能/任务/宠物/寄售/福缘/帮派系统入口。"""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from app.context import SystemContext
from protocol import Field, TYPE_BYTE, TYPE_INT, byte, decode_frame, integer, short
from systems.consignment.handler import ConsignmentSystem
from systems.fuyuan.handler import FuyuanSystem
from systems.pet.handler import PetSystem
from systems.skill.handler import ConnectionGathering, SkillSystem
from systems.task.handler import TaskSystem


ROOT = Path(__file__).resolve().parent.parent


def make_settings():
    import server

    return server.Settings.load(server.Path(ROOT) / 'config.json')


def fields(values, type_ids):
    return [Field(type_id, value) for value, type_id in zip(values, type_ids)]


def decode(frame):
    return decode_frame(frame)


class SkillSystemTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.settings = make_settings()

    def test_life_skill_list(self):
        system = SkillSystem(self.settings)
        role = {'life_skills': {}}
        from systems.skill.service import ensure_life_skills
        ensure_life_skills(role, self.settings.life_registry)
        result = system.handle_message(1132, fields([0], [TYPE_BYTE]), role)
        self.assertTrue(result.handled)
        message_id, _ = decode(result.frames[0])
        self.assertEqual(message_id, 1132)

    def test_gather_start_rejects_wrong_map(self):
        system = SkillSystem(self.settings)
        role = {'map_id': 50000, 'life_skills': {}}
        from systems.skill.service import ensure_life_skills
        ensure_life_skills(role, self.settings.life_registry)
        gathering = ConnectionGathering()
        result = system.start_gathering(role, fields([1, 6001], [TYPE_BYTE, TYPE_INT]), gathering)
        # 50000 号地图没有 6001 目标 -> 拒绝并回中断帧
        self.assertTrue(result.handled)
        self.assertTrue(result.frames)
        message_id, _ = decode(result.frames[0])
        self.assertEqual(message_id, 2027)

    def test_forge_request_detectors(self):
        from systems.skill.protocol import is_forge_list_request
        self.assertTrue(is_forge_list_request(fields([0, 1, 2, 3, 4], [TYPE_BYTE, TYPE_INT, 3, 3, TYPE_BYTE])))
        self.assertFalse(is_forge_list_request(fields([1], [TYPE_BYTE])))


class TaskSystemTests(unittest.TestCase):
    def setUp(self):
        self.settings = make_settings()
        self.saved = []
        self.system = TaskSystem(self.settings.item_registry, lambda: self.saved.append(1))

    def test_handle_1403_active_list(self):
        role = {}
        result = self.system.handle_1403(role, fields([0], [TYPE_BYTE]))
        self.assertTrue(result)
        message_id, fields_ = decode(result[0])
        self.assertEqual(message_id, 1403)

    def test_record_map_entered_event(self):
        role = {}
        self.system.handle_1403(role, fields([0], [TYPE_BYTE]))
        frames = self.system.record_event(role, 'map_entered', target_id=50000)
        self.assertIsInstance(frames, tuple)


class PetSystemTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.settings = make_settings()

    def test_ensure_role_pets_and_entry_frames(self):
        system = PetSystem(self.settings, save=lambda: None)
        role = {}
        self.assertTrue(system.ensure_role_pets(role))
        self.assertFalse(system.ensure_role_pets(role))  # 幂等
        frames = system.role_entry_frames(role)
        self.assertTrue(frames)
        message_id, _ = decode(frames[0])
        self.assertEqual(message_id, 1127)

    def test_pet_detail_route(self):
        system = PetSystem(self.settings, save=lambda: None)
        role = {}
        system.ensure_role_pets(role)
        pet_id = int(role['pets'][0]['id'])
        context = SystemContext(username='t', active_role=role, session={})
        self.assertTrue(system.can_handle(context, 1127, fields([9, pet_id], [TYPE_BYTE, TYPE_INT])))
        result = system.handle(context, 1127, fields([9, pet_id], [TYPE_BYTE, TYPE_INT]))
        message_id, _ = decode(result.frames[0])
        self.assertEqual(message_id, 1127)


class ConsignmentSystemTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.settings = make_settings()
        self.data_file = Path(self.tmp.name) / 'consignment_listings.json'
        class _Store:
            def __init__(self, accounts):
                self.data = {'accounts': accounts}

            def save(self):
                pass

        self.store = _Store({})
        self.system = ConsignmentSystem(self.store, self.settings.item_registry, self.data_file)

    def tearDown(self):
        self.tmp.cleanup()

    def test_category_frame(self):
        context = SystemContext(username='t', active_role=None, session={})
        result = self.system.handle(context, 1138, fields([3], [TYPE_BYTE]))
        message_id, payload = decode(result.frames[0])
        self.assertEqual(message_id, 1138)
        self.assertEqual(int(payload[1].value), 28)  # 原生 28 个分类

    def test_list_search_buy_roundtrip(self):
        role = {
            'id': 424242,
            'name': '寄售测试',
            'bag_capacity': 1000,
            'currencies': {'silver': 10_000_000, 'immortal_stones': 0, 'immortal_crystals': 0},
            'items': [
                {'id': 101, 'template_id': 260000001, 'quantity': 5, 'location': 'bag'},
            ],
        }
        # 上架 5 个
        request = fields(
            [9, 101, 1, 424242, 5, 100],
            [TYPE_BYTE, TYPE_INT, TYPE_BYTE, TYPE_INT, TYPE_BYTE, TYPE_INT],
        )
        self.store.data['accounts'] = {'seller': [role]}
        context = SystemContext(username='t', active_role=role, session={})
        result = self.system.handle(context, 1138, request)
        self.assertTrue(result.handled)
        # 自己的寄售列表应有 1 行
        self.assertEqual(len(self.system.service.my_listings(424242)), 1)
        # 由另一名买家购买（不允许购买自己的寄售）；卖家需在角色存储中以便打款
        buyer = {
            'id': 999999,
            'name': '买家',
            'bag_capacity': 1000,
            'currencies': {'silver': 10_000_000, 'immortal_stones': 0, 'immortal_crystals': 0},
            'items': [],
        }
        self.store.data['accounts']['buyer'] = [buyer]
        buyer_context = SystemContext(username='buyer', active_role=buyer, session={})
        result = self.system.handle(buyer_context, 1138, fields([4, 101, 999999], [TYPE_BYTE, TYPE_INT, TYPE_INT]))
        self.assertTrue(result.handled)
        self.assertEqual(buyer['currencies']['silver'], 10_000_000 - 500)


class FuyuanSystemTests(unittest.TestCase):
    def setUp(self):
        self.saved = []
        self.system = FuyuanSystem(save=lambda: self.saved.append(1))

    def test_settle_and_frames(self):
        role = {'id': 1, 'currencies': {'silver': 100}, 'fuyuan': {
            'version': 1, 'points': 1000, 'settled_at': 0,
            'purchased_points': 0, 'claims': {},
        }}
        frames = self.system.settle_and_frames(role)
        self.assertEqual(len(frames), 2)  # 1017 属性刷新 + 1054 状态
        message_ids = [decode(frame)[0] for frame in frames]
        self.assertIn(1054, message_ids)

    def test_1054_overview_flow(self):
        role = {'id': 1, 'fuyuan': {
            'version': 1, 'points': 1000, 'settled_at': 0,
            'purchased_points': 0, 'claims': {},
        }, 'currencies': {'silver': 100}}
        context = SystemContext(username='t', active_role=role, session={})
        request = fields([0, 0, 20], [TYPE_BYTE, TYPE_BYTE, TYPE_BYTE])
        self.assertTrue(self.system.can_handle(context, 1054, request))
        result = self.system.handle(context, 1054, request)
        self.assertTrue(result.handled)
        message_ids = [decode(frame)[0] for frame in result.frames]
        self.assertIn(1054, message_ids)


class GangSystemSmokeTests(unittest.TestCase):
    def test_gang_system_imports_and_registers(self):
        from systems.gang.handler import GangSystem, register_gang_routes
        from app.router import SystemRouter
        system = GangSystem(Path('data/gangs.json'), lambda: None, lambda role_id: None)
        router = SystemRouter()
        register_gang_routes(router, system)
        self.assertEqual(len(router.routes), 1)


if __name__ == '__main__':
    unittest.main()
