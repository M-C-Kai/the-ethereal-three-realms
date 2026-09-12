from __future__ import annotations

import asyncio
import tempfile
import unittest
from pathlib import Path

from consignment_protocol import CONSIGNMENT_ITEM_CATEGORIES
from consignment_service import ConsignmentService, consignment_category_for_item
from protocol import GameCipher, byte, decode_frame, encode_frame, field_values, integer, short, string
from server import LocalGameServer, Settings


async def read_frame(
    reader: asyncio.StreamReader,
    cipher: GameCipher | None = None,
) -> tuple[int, list[object]]:
    header = await reader.readexactly(2)
    if cipher is not None:
        header = cipher.decrypt(header)
    length = int.from_bytes(header, 'big')
    body = await reader.readexactly(length - 2)
    if cipher is not None:
        body = cipher.decrypt(body)
    message_id, fields = decode_frame(header + body)
    return message_id, field_values(fields)


async def drain_until_idle(
    reader: asyncio.StreamReader,
    cipher: GameCipher,
    *,
    idle_seconds: float = 0.15,
) -> list[tuple[int, list[object]]]:
    drained: list[tuple[int, list[object]]] = []
    while True:
        try:
            drained.append(
                await asyncio.wait_for(read_frame(reader, cipher), timeout=idle_seconds)
            )
        except asyncio.TimeoutError:
            return drained


async def close_writer(writer: asyncio.StreamWriter) -> None:
    writer.close()
    try:
        await writer.wait_closed()
    except (ConnectionResetError, BrokenPipeError):
        pass


class TradeTcpEndToEndTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.role_file = root / 'roles.json'
        self.account_file = root / 'accounts.json'
        self.trade_file = root / 'trades.json'
        self.settings = Settings(
            host='127.0.0.1',
            port=0,
            advertise_host='127.0.0.1',
            accept_any_credentials=True,
            account_data_file=str(self.account_file),
            role_data_file=str(self.role_file),
            consignment_data_file=str(self.trade_file),
            heartbeat_interval_seconds=3600,
        )
        self.handler = LocalGameServer(self.settings)
        # Seed exactly one role per account; avoid the default-role convenience
        # path because a marketplace requires globally distinct role ids.
        self.handler.roles.data['accounts'] = {'seller': [], 'buyer': []}
        self.handler.roles.data['next_role_id'] = 21001
        self.seller = self.handler.roles.create('seller', '卖家', 6, 0)
        self.buyer = self.handler.roles.create('buyer', '买家', 7, 0)

        self.item = next(
            item
            for item in self.seller['items']
            if item.get('location') == 'bag'
            and self.settings.item_registry.resolve(item).get('name') == '小还丹'
        )
        self.item_id = int(self.item['id'])
        self.quantity = int(self.item.get('quantity', 1))
        self.assertLessEqual(self.quantity, 255)
        self.unit_price = 37
        self.total_price = self.quantity * self.unit_price
        self.category_id = consignment_category_for_item(
            self.item, self.settings.item_registry
        )
        self.seller_silver_before = int(self.seller['currencies']['silver'])
        self.buyer_silver_before = int(self.buyer['currencies']['silver'])

        await self._start_server(self.handler)

    async def asyncTearDown(self):
        await self._stop_server()
        self.tmp.cleanup()

    async def _start_server(self, handler: LocalGameServer) -> None:
        self.tcp_server = await asyncio.start_server(
            handler.handle, '127.0.0.1', 0
        )
        self.port = int(self.tcp_server.sockets[0].getsockname()[1])
        handler.settings.port = self.port

    async def _stop_server(self) -> None:
        if getattr(self, 'tcp_server', None) is None:
            return
        self.tcp_server.close()
        await self.tcp_server.wait_closed()
        self.tcp_server = None
        await asyncio.sleep(0)

    async def _open_role(
        self,
        username: str,
    ) -> tuple[asyncio.StreamReader, asyncio.StreamWriter, GameCipher, int, list[object]]:
        account_reader, account_writer = await asyncio.open_connection(
            '127.0.0.1', self.port
        )
        account_writer.write(encode_frame(1077, [
            short(2000), byte(53), byte(0), string(username), string('pw1234'),
            short(15), byte(0),
        ]))
        await account_writer.drain()
        message_id, servers = await read_frame(account_reader)
        self.assertEqual(message_id, 1077)
        self.assertEqual(int(servers[2]), 1)

        account_writer.write(encode_frame(1051, [
            string(username), string('pw1234'), string(str(servers[4])),
            integer(1), byte(0),
        ]))
        await account_writer.drain()
        message_id, redirect = await read_frame(account_reader)
        self.assertEqual(message_id, 1052)
        await close_writer(account_writer)

        session_id, account_id = int(redirect[0]), int(redirect[1])
        game_reader, game_writer = await asyncio.open_connection('127.0.0.1', self.port)
        cipher = GameCipher()
        game_writer.write(cipher.encrypt_frame(encode_frame(
            1052, [integer(session_id), integer(account_id)]
        )))
        await game_writer.drain()
        message_id, roles = await read_frame(game_reader, cipher)
        self.assertEqual(message_id, 1080)
        self.assertEqual(int(roles[1]), 1)
        role_id = int(roles[2])

        game_writer.write(cipher.encrypt_frame(encode_frame(
            1080, [short(0), integer(role_id)]
        )))
        await game_writer.drain()
        message_id, player = await read_frame(game_reader, cipher)
        self.assertEqual(message_id, 1006)
        self.assertEqual(int(player[2]), role_id)
        await drain_until_idle(game_reader, cipher)
        return game_reader, game_writer, cipher, role_id, player

    @staticmethod
    def _property(player: list[object], property_id: int) -> int:
        return int(player[1 + property_id])

    async def _send(
        self,
        writer: asyncio.StreamWriter,
        cipher: GameCipher,
        frame: bytes,
    ) -> None:
        writer.write(cipher.encrypt_frame(frame))
        await writer.drain()

    async def test_real_tcp_sale_purchase_settlement_and_restart_persistence(self):
        # Seller: open the native category list and list one real bag stack.
        seller_reader, seller_writer, seller_cipher, seller_role_id, seller_player = (
            await self._open_role('seller')
        )
        self.assertEqual(self._property(seller_player, 50), self.seller_silver_before)

        await self._send(
            seller_writer, seller_cipher, encode_frame(1138, [byte(3)])
        )
        message_id, categories = await read_frame(seller_reader, seller_cipher)
        self.assertEqual(message_id, 1138)
        self.assertEqual(categories[0:2], [3, len(CONSIGNMENT_ITEM_CATEGORIES)])

        await self._send(seller_writer, seller_cipher, encode_frame(1138, [
            byte(9), integer(self.item_id), byte(1), integer(seller_role_id),
            byte(self.quantity), integer(self.unit_price),
        ]))
        seller_listing_frames: list[tuple[int, list[object]]] = []
        while True:
            frame = await read_frame(seller_reader, seller_cipher)
            seller_listing_frames.append(frame)
            if frame[0] == 1138 and frame[1] and int(frame[1][0]) == 9:
                break
        own_list = seller_listing_frames[-1][1]
        self.assertEqual(own_list[0:2], [9, 1])
        self.assertEqual(int(own_list[3]), self.item_id)

        await self._send(
            seller_writer, seller_cipher,
            encode_frame(1138, [byte(7), integer(seller_role_id)]),
        )
        message_id, mine = await read_frame(seller_reader, seller_cipher)
        self.assertEqual(message_id, 1138)
        self.assertEqual(mine[0:2], [7, 1])
        self.assertEqual(int(mine[3]), self.item_id)
        await close_writer(seller_writer)

        # Buyer: click the matching category, fetch market rows, then purchase.
        buyer_reader, buyer_writer, buyer_cipher, buyer_role_id, buyer_player = (
            await self._open_role('buyer')
        )
        self.assertEqual(self._property(buyer_player, 50), self.buyer_silver_before)

        await self._send(
            buyer_writer, buyer_cipher,
            encode_frame(1138, [byte(13), byte(self.category_id)]),
        )
        message_id, counts = await read_frame(buyer_reader, buyer_cipher)
        self.assertEqual(message_id, 1138)
        self.assertEqual(counts, [13, 1, 1])

        await self._send(
            buyer_writer, buyer_cipher, encode_frame(1138, [byte(23)])
        )
        message_id, market = await read_frame(buyer_reader, buyer_cipher)
        self.assertEqual(message_id, 1138)
        self.assertEqual(market[0:4], [1, 1, 0, 1])
        self.assertEqual(int(market[5]), self.item_id)
        self.assertEqual(int(market[10]), seller_role_id)
        self.assertEqual(str(market[11]), '卖家')

        await self._send(buyer_writer, buyer_cipher, encode_frame(1138, [
            byte(4), integer(self.item_id), integer(buyer_role_id),
        ]))
        message_id, removed = await read_frame(buyer_reader, buyer_cipher)
        self.assertEqual((message_id, removed), (1138, [16, self.item_id]))
        message_id, received_item = await read_frame(buyer_reader, buyer_cipher)
        self.assertEqual(message_id, 1008)
        self.assertEqual(str(received_item[8]), '小还丹')
        message_id, buyer_currency = await read_frame(buyer_reader, buyer_cipher)
        self.assertEqual(message_id, 1017)
        currency_pairs = dict(zip(buyer_currency[3::2], buyer_currency[4::2]))
        self.assertEqual(
            int(currency_pairs[50]), self.buyer_silver_before - self.total_price
        )
        await close_writer(buyer_writer)

        # Seller reconnects: listing is gone and proceeds are already durable.
        seller_reader, seller_writer, seller_cipher, seller_role_id_2, seller_player = (
            await self._open_role('seller')
        )
        self.assertEqual(seller_role_id_2, seller_role_id)
        self.assertEqual(
            self._property(seller_player, 50),
            self.seller_silver_before + self.total_price,
        )
        await self._send(
            seller_writer, seller_cipher,
            encode_frame(1138, [byte(7), integer(seller_role_id)]),
        )
        message_id, mine_after_sale = await read_frame(seller_reader, seller_cipher)
        self.assertEqual(message_id, 1138)
        self.assertEqual(mine_after_sale, [7, 0])
        await close_writer(seller_writer)

        # Simulate process restart: a brand-new server reloads role + trade JSON.
        await self._stop_server()
        fresh_handler = LocalGameServer(self.settings)
        self.handler = fresh_handler
        await self._start_server(fresh_handler)

        persisted = ConsignmentService(
            fresh_handler.roles,
            self.settings.item_registry,
            self.trade_file,
        )
        trades = persisted.trade_history(seller_role_id, side='seller')
        self.assertEqual(len(trades), 1)
        self.assertEqual(trades[0]['status'], 'completed')
        self.assertEqual(int(trades[0]['buyer_role_id']), buyer_role_id)
        self.assertEqual(int(trades[0]['item_instance_id']), self.item_id)
        self.assertEqual(int(trades[0]['total_price']), self.total_price)
        self.assertEqual(
            [row['status'] for row in persisted.order_history(seller_role_id)],
            ['sold'],
        )

        # And the restarted TCP server still reports no active seller listing.
        seller_reader, seller_writer, seller_cipher, restarted_role_id, _player = (
            await self._open_role('seller')
        )
        self.assertEqual(restarted_role_id, seller_role_id)
        await self._send(
            seller_writer, seller_cipher,
            encode_frame(1138, [byte(7), integer(seller_role_id)]),
        )
        message_id, restarted_mine = await read_frame(seller_reader, seller_cipher)
        self.assertEqual(message_id, 1138)
        self.assertEqual(restarted_mine, [7, 0])
        await close_writer(seller_writer)


if __name__ == '__main__':
    unittest.main()
