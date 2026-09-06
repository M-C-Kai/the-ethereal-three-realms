import json
import unittest
from copy import deepcopy
from pathlib import Path

from map_registry import load_map_registry


ROOT = Path(__file__).resolve().parents[1]


class NpcAppearanceGalleryTests(unittest.TestCase):
    def test_map_58_materializes_every_confirmed_enabled_appearance_once(self):
        config = json.loads((ROOT / 'config.json').read_text(encoding='utf-8'))
        catalog = json.loads(
            (ROOT / 'data' / 'npc_appearance_catalog.json').read_text(encoding='utf-8')
        )

        registry = load_map_registry(config, appearance_catalog=catalog)
        changan = registry.require(58)
        expected = {
            int(entry['dat_id'])
            for entry in catalog['appearances']
            if entry.get('enabled') is True and entry.get('status') == 'confirmed'
        }
        actual = [npc.dat_id for npc in changan.npcs]

        self.assertEqual(len(expected), 44)
        self.assertEqual(len(actual), 44)
        self.assertEqual(set(actual), expected)
        self.assertEqual(len(actual), len(set(actual)))
        self.assertNotIn(0, actual)

        occupied = {(npc.x, npc.y) for npc in changan.npcs}
        self.assertEqual(len(occupied), len(changan.npcs))
        self.assertNotIn((changan.spawn_x, changan.spawn_y), occupied)
        if changan.monster is not None:
            self.assertNotIn((changan.monster.x, changan.monster.y), occupied)
        for portal in changan.portals:
            self.assertNotIn((portal.x, portal.y), occupied)

    def test_business_npc_resolves_appearance_key_from_catalog(self):
        config = json.loads((ROOT / 'config.json').read_text(encoding='utf-8'))
        catalog = json.loads(
            (ROOT / 'data' / 'npc_appearance_catalog.json').read_text(encoding='utf-8')
        )
        by_key = {entry['key']: int(entry['dat_id']) for entry in catalog['appearances']}
        configured = {
            int(entry['id']): entry['appearance_key']
            for entry in config['maps']['58']['npcs']
        }

        changan = load_map_registry(config, appearance_catalog=catalog).require(58)
        by_id = {npc.id: npc for npc in changan.npcs}

        for npc_id, key in configured.items():
            with self.subTest(npc_id=npc_id, key=key):
                self.assertEqual(by_id[npc_id].dat_id, by_key[key])
                self.assertEqual(by_id[npc_id].model, by_key[key] - 2_100_000)

    def test_gallery_ignores_disabled_and_unconfirmed_entries(self):
        config = {
            'default_map_id': 58,
            'maps': {
                '58': {
                    'name': '测试地图',
                    'map_o_file': 'maps/58.map.o',
                    'map_ref_available': True,
                    'fallback_width': 96,
                    'fallback_height': 96,
                    'spawn': {'x': 60, 'y': 67},
                    'monster': None,
                    'npcs': [
                        {'id': 1900002, 'name': '业务NPC', 'x': 50, 'y': 64, 'appearance_key': 'keep'}
                    ],
                    'portals': [],
                    'npc_appearance_gallery': True,
                }
            },
        }
        catalog = {
            'appearances': [
                {'key': 'keep', 'dat_id': 90000, 'status': 'confirmed', 'enabled': True},
                {'key': 'gallery', 'dat_id': 90030, 'status': 'confirmed', 'enabled': True},
                {'key': 'disabled', 'dat_id': 90120, 'status': 'confirmed', 'enabled': False},
                {'key': 'pending', 'dat_id': 90150, 'status': 'pending', 'enabled': True},
            ]
        }

        npcs = load_map_registry(config, appearance_catalog=catalog).require(58).npcs

        self.assertEqual([npc.dat_id for npc in npcs], [90000, 90030])
        self.assertEqual(npcs[0].name, '业务NPC')
        self.assertEqual(npcs[1].name, 'NPC外观 90030')

    def test_catalog_rejects_duplicate_keys_and_dat_ids(self):
        base_config = {
            'default_map_id': 58,
            'maps': {
                '58': {
                    'name': '测试地图',
                    'map_o_file': 'maps/58.map.o',
                    'map_ref_available': True,
                    'fallback_width': 96,
                    'fallback_height': 96,
                    'spawn': {'x': 60, 'y': 67},
                    'monster': None,
                    'npcs': [],
                    'portals': [],
                    'npc_appearance_gallery': True,
                }
            },
        }
        cases = [
            (
                [
                    {'key': 'same', 'dat_id': 90000, 'status': 'confirmed', 'enabled': True},
                    {'key': 'same', 'dat_id': 90030, 'status': 'confirmed', 'enabled': True},
                ],
                'duplicate NPC appearance key',
            ),
            (
                [
                    {'key': 'first', 'dat_id': 90000, 'status': 'confirmed', 'enabled': True},
                    {'key': 'second', 'dat_id': 90000, 'status': 'confirmed', 'enabled': True},
                ],
                'duplicate NPC appearance dat_id',
            ),
        ]
        for appearances, message in cases:
            with self.subTest(message=message):
                config = deepcopy(base_config)
                with self.assertRaisesRegex(ValueError, message):
                    load_map_registry(config, appearance_catalog={'appearances': appearances})


if __name__ == '__main__':
    unittest.main()
