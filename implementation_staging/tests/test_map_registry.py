import unittest
from copy import deepcopy


try:
    from map_registry import default_map_registry, load_map_registry
except ImportError:
    default_map_registry = None
    load_map_registry = None


NEW_CONFIG = {
    'default_map_id': 58,
    'maps': {
        '58': {
            'name': '长安',
            'map_o_file': 'maps/58.map.o',
            'map_ref_available': True,
            'fallback_width': 96,
            'fallback_height': 96,
            'spawn': {'x': 60, 'y': 67},
            'monster': {
                'id': 1900001,
                'name': '试炼妖兽',
                'model': -2004250,
                'x': 9,
                'y': 28,
                'direction': 0,
            },
            'npcs': [],
            'portals': [
                {
                    'id': 580001,
                    'name': '跨地图传送点',
                    'model': -2004250,
                    'x': 55,
                    'y': 55,
                    'direction': 0,
                    'target_map_id': 50000,
                    'target_x': 8,
                    'target_y': 6,
                },
                {
                    'id': 580003,
                    'name': '跨地图传送点',
                    'model': -2004250,
                    'x': 34,
                    'y': 7,
                    'direction': 0,
                    'target_map_id': 50000,
                    'target_x': 8,
                    'target_y': 6,
                },
            ],
        },
        '50000': {
            'name': '传送测试区',
            'map_o_file': 'maps/50000.map.o',
            'map_ref_available': True,
            'fallback_width': 90,
            'fallback_height': 90,
            'spawn': {'x': 8, 'y': 6},
            'monster': {
                'id': 1900001,
                'name': '试炼妖兽',
                'model': -2004250,
                'x': 12,
                'y': 8,
                'direction': 0,
            },
            'npcs': [],
            'portals': [
                {
                    'id': 580002,
                    'name': '返回长安',
                    'model': -2004250,
                    'x': 9,
                    'y': 6,
                    'direction': 0,
                    'target_map_id': 58,
                    'target_x': 60,
                    'target_y': 67,
                }
            ],
        },
    },
}

LEGACY_CONFIG = {
    'map_id': 58,
    'map_name': '仙石村',
    'map_width': 96,
    'map_height': 96,
    'spawn_x': 60,
    'spawn_y': 67,
    'map_o_file': 'maps/58.map.o',
    'monster_id': 1900001,
    'monster_name': '试炼妖兽',
    'monster_model': -2004250,
    'monster_x': 9,
    'monster_y': 28,
    'portal_enabled': True,
    'portals': [
        {'id': 580001, 'name': '跨地图传送点', 'x': 55, 'y': 55},
        {'id': 580003, 'name': '跨地图传送点', 'x': 34, 'y': 7},
    ],
    'portal_target_map_id': 50000,
    'portal_target_map_name': '传送测试区',
    'portal_target_spawn_x': 8,
    'portal_target_spawn_y': 6,
    'portal_target_map_o_file': 'maps/50000.map.o',
    'portal_target_map_ref_available': True,
    'return_portal_id': 580002,
    'return_portal_name': '返回仙石村',
    'return_portal_x': 9,
    'return_portal_y': 6,
    'npcs': [],
}


class MapRegistryTests(unittest.TestCase):
    def test_registry_loads_changan_and_all_portals(self):
        self.assertIsNotNone(load_map_registry, 'map registry module is missing')
        if load_map_registry is None:
            return

        registry = load_map_registry(NEW_CONFIG)
        changan = registry.require(58)
        target = registry.require(50000)

        self.assertEqual(changan.name, '长安')
        self.assertEqual(changan.map_o_file, 'maps/58.map.o')
        self.assertEqual([portal.id for portal in changan.portals], [580001, 580003])
        self.assertEqual(changan.portals[1].target_map_id, 50000)
        self.assertEqual((changan.portals[1].target_x, changan.portals[1].target_y), (8, 6))
        self.assertEqual([portal.id for portal in target.portals], [580002])

    def test_legacy_flat_config_migrates_to_two_maps(self):
        registry = load_map_registry(LEGACY_CONFIG)

        self.assertEqual(registry.default_map_id, 58)
        self.assertEqual(registry.require(58).map_o_file, 'maps/58.map.o')
        self.assertEqual([item.id for item in registry.require(58).portals], [580001, 580003])
        self.assertEqual(registry.require(50000).map_o_file, 'maps/50000.map.o')
        self.assertEqual(registry.require(50000).portals[0].target_map_id, 58)

    def test_registry_rejects_unknown_portal_target(self):
        payload = deepcopy(NEW_CONFIG)
        payload['maps']['58']['portals'][0]['target_map_id'] = 99999

        with self.assertRaisesRegex(ValueError, 'unknown target map 99999'):
            load_map_registry(payload)

    def test_registry_rejects_duplicate_portal_ids(self):
        payload = deepcopy(NEW_CONFIG)
        payload['maps']['50000']['portals'][0]['id'] = 580001

        with self.assertRaisesRegex(ValueError, 'duplicate portal id 580001'):
            load_map_registry(payload)

    def test_registry_rejects_out_of_bounds_target(self):
        payload = deepcopy(NEW_CONFIG)
        payload['maps']['58']['portals'][0]['target_x'] = 127

        with self.assertRaisesRegex(ValueError, 'target coordinate'):
            load_map_registry(payload)

    def test_registry_rejects_map_key_mismatch_and_unknown_default(self):
        mismatched = deepcopy(NEW_CONFIG)
        mismatched['maps']['58']['id'] = 59
        with self.assertRaisesRegex(ValueError, 'map key 58 does not match id 59'):
            load_map_registry(mismatched)

        unknown_default = deepcopy(NEW_CONFIG)
        unknown_default['default_map_id'] = 99999
        with self.assertRaisesRegex(ValueError, 'unknown default map 99999'):
            load_map_registry(unknown_default)

    def test_npc_catalog_only_supplements_registered_npcs(self):
        payload = deepcopy(NEW_CONFIG)
        payload['maps']['58']['npcs'] = [
            {'id': 1900002, 'name': '孙思邈', 'label': '药王', 'x': 50, 'y': 64}
        ]
        registry = load_map_registry(
            payload,
            npc_catalog=[
                {'id': 1900002, 'dat_id': 90000, 'model': -2010000},
                {'id': 1999999, 'dat_id': 99999, 'model': -2999999},
            ],
        )

        self.assertEqual([npc.id for npc in registry.require(58).npcs], [1900002])
        self.assertEqual(registry.require(58).npcs[0].dat_id, 90000)
        self.assertEqual(registry.require(58).npcs[0].model, -2010000)

    def test_default_registry_uses_changan_and_rejects_unknown_maps(self):
        self.assertIsNotNone(default_map_registry, 'default registry factory is missing')
        if default_map_registry is None:
            return

        registry = default_map_registry()

        self.assertEqual(registry.default_map_id, 58)
        self.assertEqual(registry.require(58).name, '长安')
        self.assertEqual([item.id for item in registry.require(58).portals], [580001, 580003])
        with self.assertRaisesRegex(ValueError, 'unknown map id 99999'):
            registry.require(99999)


if __name__ == '__main__':
    unittest.main()
