import unittest
from copy import deepcopy
import json
import tempfile
from pathlib import Path

from protocol import decode_frame, field_values
import server as server_module
from server import RoleStore, Settings, default_role, notice_and_world, settings_for_map, settings_for_role


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

    def test_sect_skill_mentor_metadata_is_loaded_and_validated(self):
        payload = deepcopy(NEW_CONFIG)
        payload['maps']['58']['npcs'] = [{
            'id': 1900101,
            'name': '昆仑导师',
            'x': 12,
            'y': 8,
            'service': 'sect_skill_mentor',
            'sect_id': 1,
        }]

        mentor = load_map_registry(payload).require(58).npcs[0]

        self.assertEqual(mentor.service, 'sect_skill_mentor')
        self.assertEqual(mentor.sect_id, 1)

        invalid_cases = [
            ({'service': 'unknown_service', 'sect_id': 1}, 'unknown NPC service'),
            ({'service': 'sect_skill_mentor'}, 'requires sect_id'),
            ({'service': 'sect_skill_mentor', 'sect_id': 0}, 'sect_id must be within 1..13'),
            ({'service': 'sect_skill_mentor', 'sect_id': 14}, 'sect_id must be within 1..13'),
        ]
        for replacement, message in invalid_cases:
            with self.subTest(replacement=replacement):
                invalid = deepcopy(payload)
                npc = invalid['maps']['58']['npcs'][0]
                npc.pop('sect_id', None)
                npc.update(replacement)
                with self.assertRaisesRegex(ValueError, message):
                    load_map_registry(invalid)

    def test_default_registry_uses_changan_and_rejects_unknown_maps(self):
        self.assertIsNotNone(default_map_registry, 'map registry module is missing')
        if default_map_registry is None:
            return

        registry = default_map_registry()
        changan = registry.require(58)

        self.assertEqual(registry.default_map_id, 58)
        self.assertEqual(changan.name, '长安')
        self.assertEqual([item.id for item in changan.portals], [580001, 580003, 580005])
        self.assertEqual(len(changan.npcs), 44)
        self.assertEqual(len({npc.dat_id for npc in changan.npcs}), 44)
        self.assertEqual([npc.id for npc in changan.npcs[:3]], [1900002, 1900003, 1900004])
        self.assertEqual([npc.dat_id for npc in changan.npcs[:3]], [95750, 96010, 95520])
        kunlun = registry.require(60001)
        self.assertEqual(kunlun.name, '昆仑')
        self.assertTrue(kunlun.map_ref_available)
        self.assertIsNone(kunlun.monster)
        self.assertEqual([npc.id for npc in kunlun.npcs], [1900101])
        self.assertEqual((kunlun.npcs[0].service, kunlun.npcs[0].sect_id), ('sect_skill_mentor', 1))
        self.assertEqual([portal.id for portal in kunlun.portals], [6000101])
        self.assertEqual(kunlun.portals[0].target_map_id, 58)
        with self.assertRaisesRegex(ValueError, 'unknown map id 99999'):
            registry.require(99999)


class SettingsRegistryTests(unittest.TestCase):
    def test_project_config_uses_nested_changan_registry(self):
        config_path = Path(__file__).resolve().parents[1] / 'config.json'
        payload = json.loads(config_path.read_text(encoding='utf-8'))

        self.assertEqual(payload['default_map_id'], 58)
        self.assertNotIn('map_name', payload)
        self.assertEqual(payload['maps']['58']['name'], '长安')
        self.assertTrue(payload['maps']['58']['npc_appearance_gallery'])
        self.assertTrue(all('appearance_key' in npc for npc in payload['maps']['58']['npcs']))
        self.assertTrue(all('dat_id' not in npc for npc in payload['maps']['58']['npcs']))
        self.assertEqual(
            [portal['id'] for portal in payload['maps']['58']['portals']],
            [580001, 580003, 580005],
        )
        self.assertEqual(payload['maps']['50000']['portals'][0]['id'], 580002)
        self.assertEqual(payload['maps']['60001']['name'], '昆仑')
        self.assertTrue(payload['maps']['60001']['map_ref_available'])
        self.assertNotIn('monster', payload['maps']['60001'])
        self.assertEqual(payload['maps']['60001']['npcs'][0]['service'], 'sect_skill_mentor')

    def test_settings_loads_nested_registry(self):
        with tempfile.TemporaryDirectory() as directory:
            config_path = Path(directory) / 'config.json'
            config_path.write_text(json.dumps(NEW_CONFIG, ensure_ascii=False), encoding='utf-8')

            settings = Settings.load(config_path)

        self.assertEqual(settings.default_map_id, 58)
        self.assertEqual(settings.map_registry.require(58).name, '长安')
        self.assertEqual(len(settings.map_registry.require(58).portals), 2)

    def test_world_name_is_derived_from_registry_not_stale_role_name(self):
        settings = Settings(map_registry=default_map_registry())
        role = default_role(settings)
        role['map_name'] = '旧名称'

        _, fields = decode_frame(notice_and_world(settings, role)[1])

        self.assertEqual(field_values(fields)[3], '长安')

    def test_map_queries_use_role_position_and_reject_unknown_map(self):
        settings = Settings(map_registry=default_map_registry())
        role = default_role(settings)
        role.update({'map_id': 50000, 'map_x': 14, 'map_y': 15})

        current = settings_for_role(settings, role)

        self.assertEqual((current.id, current.name), (50000, '传送测试区'))
        self.assertEqual((current.spawn_x, current.spawn_y), (14, 15))
        with self.assertRaisesRegex(ValueError, 'unknown map id 99999'):
            settings_for_map(settings, 99999)

    def test_role_store_migrates_unknown_map_to_default_and_adds_coordinates(self):
        with tempfile.TemporaryDirectory() as directory:
            role_path = Path(directory) / 'roles.json'
            legacy = default_role(Settings())
            legacy.update({'map_id': 99999, 'map_name': '错误地图'})
            legacy.pop('map_x', None)
            legacy.pop('map_y', None)
            role_path.write_text(json.dumps({
                'next_role_id': 10002,
                'accounts': {'legacy': [legacy]},
            }, ensure_ascii=False), encoding='utf-8')

            migrated = RoleStore(Settings(role_data_file=str(role_path))).roles_for('legacy')[0]

        self.assertEqual(migrated['map_id'], 58)
        self.assertEqual(migrated['map_name'], '长安')
        self.assertEqual((migrated['map_x'], migrated['map_y']), (60, 67))


class PortalTransitionTests(unittest.TestCase):
    def test_both_changan_portals_route_to_their_registered_landing_point(self):
        transition = getattr(server_module, 'apply_portal_transition', None)
        self.assertIsNotNone(transition, 'portal transition helper is missing')
        if transition is None:
            return
        settings = Settings()

        for portal_id in (580001, 580003):
            role = default_role(settings)
            target = transition(settings, role, portal_id)

            self.assertIsNotNone(target)
            self.assertEqual((role['map_id'], role['map_name']), (50000, '传送测试区'))
            self.assertEqual((role['map_x'], role['map_y']), (8, 6))
            self.assertEqual((target.id, target.spawn_x, target.spawn_y), (50000, 8, 6))

    def test_return_portal_routes_back_to_changan_and_persists_coordinates(self):
        transition = getattr(server_module, 'apply_portal_transition', None)
        self.assertIsNotNone(transition, 'portal transition helper is missing')
        if transition is None:
            return
        settings = Settings()
        role = default_role(settings)
        role.update({'map_id': 50000, 'map_name': '传送测试区', 'map_x': 8, 'map_y': 6})

        target = transition(settings, role, 580002)

        self.assertEqual((role['map_id'], role['map_name']), (58, '长安'))
        self.assertEqual((role['map_x'], role['map_y']), (60, 67))
        self.assertEqual((target.id, target.name), (58, '长安'))

    def test_kunlun_portals_route_both_directions(self):
        settings = Settings(map_registry=default_map_registry())
        role = default_role(settings)

        target = server_module.apply_portal_transition(settings, role, 580005)

        self.assertEqual((role['map_id'], role['map_name']), (60001, '昆仑'))
        self.assertEqual((role['map_x'], role['map_y']), (8, 6))
        self.assertEqual((target.id, target.name), (60001, '昆仑'))

        returned = server_module.apply_portal_transition(settings, role, 6000101)

        self.assertEqual((role['map_id'], role['map_name']), (58, '长安'))
        self.assertEqual((role['map_x'], role['map_y']), (60, 67))
        self.assertEqual((returned.id, returned.name), (58, '长安'))

    def test_portal_id_from_another_map_is_ignored_without_mutating_role(self):
        transition = getattr(server_module, 'apply_portal_transition', None)
        self.assertIsNotNone(transition, 'portal transition helper is missing')
        if transition is None:
            return
        settings = Settings()
        role = default_role(settings)
        before = dict(role)

        target = transition(settings, role, 580002)

        self.assertIsNone(target)
        self.assertEqual(role, before)

    def test_portal_landing_survives_role_store_reload(self):
        transition = server_module.apply_portal_transition
        with tempfile.TemporaryDirectory() as directory:
            role_path = Path(directory) / 'roles.json'
            settings = Settings(role_data_file=str(role_path))
            store = RoleStore(settings)
            role = store.roles_for('traveller')[0]

            transition(settings, role, 580003)
            store.save()
            reloaded = RoleStore(settings).roles_for('traveller')[0]

        self.assertEqual(
            (reloaded['map_id'], reloaded['map_name'], reloaded['map_x'], reloaded['map_y']),
            (50000, '传送测试区', 8, 6),
        )


if __name__ == '__main__':
    unittest.main()
