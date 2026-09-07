import unittest

from item_registry import default_item_registry, deprecated_mount_template_ids
from mount_constructor import construct_mount_state, load_mount_catalog
from server import ensure_all_mount_series_items


class MountSeriesGrantTests(unittest.TestCase):
    def test_grants_one_item_for_every_series_and_is_idempotent(self):
        registry = default_item_registry()
        catalog = load_mount_catalog()
        role = {'id': 77, 'items': []}

        self.assertTrue(ensure_all_mount_series_items(role, registry))
        states = [construct_mount_state(item, registry, catalog) for item in role['items']]
        grantable = set()
        for series_id in catalog.series:
            template_id = catalog.template_id_for_image(
                catalog.resolve_appearance(series_id, 0)
            )
            try:
                registry.require(template_id)
            except KeyError:
                continue
            grantable.add(series_id)
        self.assertIn(41004, grantable)
        self.assertEqual(len(states), len(grantable))
        self.assertEqual({state.series_id for state in states}, grantable)
        self.assertTrue(all(state.stage == 0 for state in states))
        self.assertTrue(all(item['location'] == 'bag' for item in role['items']))
        self.assertEqual(len({item['id'] for item in role['items']}), len(role['items']))

        before = list(role['items'])
        self.assertFalse(ensure_all_mount_series_items(role, registry))
        self.assertEqual(role['items'], before)

    def test_existing_series_is_not_duplicated(self):
        registry = default_item_registry()
        catalog = load_mount_catalog()
        role = {
            'id': 78,
            'items': [{
                'id': 780000,
                'template_id': catalog.template_id_for_image(41002),
                'quantity': 1,
                'location': 'bag',
                'mount_state': {
                    'series_id': 41002,
                    'stage': 2,
                    'grade': 9,
                    'growth': 5,
                },
            }],
        }
        self.assertTrue(ensure_all_mount_series_items(role, registry))
        series_41002 = [
            item for item in role['items']
            if item.get('mount_state', {}).get('series_id') == 41002
        ]
        self.assertEqual(len(series_41002), 1)
        self.assertEqual(series_41002[0]['mount_state']['stage'], 2)

    def test_wrong_legacy_41004_template_is_deprecated_and_replaced(self):
        registry = default_item_registry()
        self.assertIn(170410004, deprecated_mount_template_ids())
        role = {
            'id': 79,
            'items': [{
                'id': 790000,
                'template_id': 170410004,
                'quantity': 1,
                'location': 'bag',
            }],
        }
        role['items'] = [
            item for item in role['items']
            if int(item.get('template_id', 0)) not in deprecated_mount_template_ids()
        ]
        self.assertTrue(ensure_all_mount_series_items(role, registry))
        series_41004 = [
            item for item in role['items']
            if item.get('mount_state', {}).get('series_id') == 41004
        ]
        self.assertEqual(len(series_41004), 1)
        self.assertEqual(int(series_41004[0]['template_id']), 170901004)
        self.assertEqual(series_41004[0]['mount_state']['stage'], 0)
        self.assertNotIn(170410004, {int(item['template_id']) for item in role['items']})


if __name__ == '__main__':
    unittest.main()
