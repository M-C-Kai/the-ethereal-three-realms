from __future__ import annotations

import inspect
import unittest

import server


class ConsignmentServerContractTests(unittest.TestCase):
    def test_server_dispatch_contains_complete_consignment_actions(self):
        source = inspect.getsource(server.LocalGameServer.handle)
        required = (
            'is_consignment_market_list_request',
            'is_consignment_my_listings_request',
            'is_consignment_list_item_request',
            'is_consignment_unlist_request',
            'is_consignment_buy_request',
            'consignment_category_counts_frame',
            'consignment_market_list_frame',
            'consignment_my_listings_frame',
            'consignment_remove_owned_frame',
            'consignment_remove_market_frame',
        )
        for name in required:
            self.assertIn(name, source, name)

    def test_connection_state_constructs_persistent_consignment_service(self):
        source = inspect.getsource(server.LocalGameServer.handle)
        self.assertIn('ConsignmentService(', source)
        self.assertIn('self.roles', source)
        self.assertIn('self.settings.item_registry', source)
        self.assertIn('self.consignment_data_file', source)
        self.assertIn('current_consignment_category', source)


if __name__ == '__main__':
    unittest.main()
