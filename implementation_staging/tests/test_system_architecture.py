"""统一测试：系统架构边界与装配。

验证 systems/<name>/ 五层结构、路由注册顺序与 server.py 装配。
"""
from __future__ import annotations

import importlib
import unittest
from pathlib import Path

from app.context import SystemContext
from app.router import SystemRouter

ROOT = Path(__file__).resolve().parent.parent

SYSTEMS = (
    'team', 'social', 'shop', 'skill', 'map', 'role', 'inventory', 'battle',
    'task', 'gang', 'pet', 'consignment', 'fuyuan',
)

LAYERS = ('handler', 'service', 'protocol', 'registry', 'events')


class FiveLayerLayoutTests(unittest.TestCase):
    def test_every_system_has_five_layers(self):
        for name in SYSTEMS:
            for layer in LAYERS:
                path = ROOT / 'systems' / name / f'{layer}.py'
                self.assertTrue(path.is_file(), f'missing {path}')

    def test_every_system_imports_and_registers(self):
        router = SystemRouter()
        registered = []
        for name in SYSTEMS:
            module = importlib.import_module(f'systems.{name}.handler')
            system_cls = getattr(module, f'{name.capitalize()}System', None)
            register_fn = getattr(module, f'register_{name}_routes', None)
            self.assertIsNotNone(system_cls, name)
            self.assertIsNotNone(register_fn, name)
            minimal_args = {
                'task': (None, lambda: None),
                'gang': (Path('data/gangs.json'), lambda: None, lambda role_id: None),
            }
            system = system_cls(*minimal_args.get(name, ()))
            register_fn(router, system)
            registered.append(system.system_name)
        # task 注册两条路由（1403 与任务型 1145）
        self.assertEqual(len(router.routes), len(SYSTEMS) + 1)
        self.assertEqual(set(registered), set(SYSTEMS))


class RouterPriorityTests(unittest.TestCase):
    def test_route_registration_order(self):
        """装配后的路由顺序必须保证：宠物先于角色认领 1103，
        角色先于地图认领 1010/36 与登出页 1054，任务先于地图认领任务型 1145。"""
        import server

        settings = server.Settings.load(server.Path(ROOT) / 'config.json')
        game = server.LocalGameServer(settings)
        names = [route.name for route in game.system_router.routes]
        for first, second in (
            ('team', 'social'),
            ('team', 'role'),
            ('social', 'role'),
            ('social', 'inventory'),
            ('pet', 'role'),
            ('role', 'map'),
            ('task.1403', 'map'),
            ('task.1145', 'map'),
            ('role', 'fuyuan'),
        ):
            self.assertLess(names.index(first), names.index(second), f'{first} must precede {second}')

    def test_duplicate_route_name_rejected(self):
        router = SystemRouter()
        router.register('x', lambda *a: False, lambda *a: None)
        with self.assertRaises(ValueError):
            router.register('x', lambda *a: False, lambda *a: None)


class ServerSurfaceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import server

        cls.server_module = server
        cls.settings = server.Settings.load(server.Path(ROOT) / 'config.json')
        cls.game = server.LocalGameServer(cls.settings)

    def test_server_exposes_all_systems(self):
        for attr in (
            'team_system', 'shop_system', 'skill_system', 'map_system', 'role_system',
            'inventory_system', 'battle_system', 'task_system', 'gang_system',
            'pet_system', 'consignment_system', 'fuyuan_system',
        ):
            self.assertTrue(hasattr(self.game, attr), attr)

    def test_server_keeps_only_assembly_routing_and_network(self):
        """server.py 不得重新出现协议分支（elif message_id == ...）。"""
        source = (ROOT / 'server.py').read_text(encoding='utf-8')
        self.assertNotIn('elif message_id', source)
        self.assertNotIn('if message_id ==', source)

    def test_context_dispatch_roundtrip(self):
        """总线路由对未知消息返回 not_handled，不抛异常。"""
        context = SystemContext(username='t', active_role=None, session={})
        result = self.game.system_router.dispatch(context, 9999, [])
        self.assertFalse(result.handled)


if __name__ == '__main__':
    unittest.main()
