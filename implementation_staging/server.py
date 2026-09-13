"""《飘渺三界2》本地兼容服务器：依赖装配、系统总线路由与网络收发。

所有玩法协议入口位于 ``systems/<name>/{handler,service,protocol,registry,events}.py``。
本模块只保留三类职责：

1. 依赖装配：``Settings`` 读取 config.json 与 data/ 目录，``LocalGameServer``
   实例化全部系统并把依赖（存储、事件总线、跨系统回调）注入它们；
2. 总线路由：每条客户端消息经 ``app.router.SystemRouter`` 分发到唯一系统；
3. 网络收发：asyncio TCP 帧收发、游戏阶段加密、心跳、在线连接登记与断线清理。
"""
from __future__ import annotations

import argparse
import asyncio
import contextlib
import json
import logging
import struct
import time
from dataclasses import dataclass, field, fields
from pathlib import Path

from app.context import SystemContext
from app.router import SystemRouter
from protocol import GameCipher, ProtocolError, decode_payload, encode_frame, field_values, integer
from systems.battle.handler import BattleSystem, register_battle_routes
from systems.consignment.handler import ConsignmentSystem, register_consignment_routes
from systems.exchange.handler import ExchangeSystem, register_exchange_routes
from systems.fuyuan.handler import FuyuanSystem, register_fuyuan_routes
from systems.gang.handler import GangSystem, register_gang_routes
from systems.inventory.handler import InventorySystem, register_inventory_routes
from systems.inventory.registry import default_item_registry
from systems.inventory.service import bag_capacity, item_frame
from systems.map.handler import MapSystem, register_map_routes
from systems.map.registry import (
    MapRegistry, default_map_registry, load_map_registry,
)
from systems.map.service import (
    materialize_all_dynamic_maps, merge_dynamic_maps_into_registry_payload,
)
from systems.pet.handler import PetSystem, register_pet_routes
from systems.role.handler import RoleSystem, register_role_routes
from systems.role.registry import default_sect_registry
from systems.role.protocol import role_creation_frames, role_list
from systems.role.service import AccountStore, RoleStore, role_entry_frames
from systems.shop.handler import ShopSystem, register_shop_routes
from systems.shop.registry import default_shop_registry
from systems.skill.handler import SkillSystem, register_skill_routes
from systems.skill.registry import default_life_skill_registry
from systems.social.handler import SocialSystem, register_social_routes
from systems.task.handler import TaskSystem, register_task_routes
from systems.team.handler import TeamSystem, register_team_routes


LOG = logging.getLogger('piaomiao-local')


@dataclass
class Settings:
    host: str = '0.0.0.0'
    port: int = 6805
    advertise_host: str = '127.0.0.1'
    server_name: str = '本地一区'
    accept_any_credentials: bool = False
    account_data_file: str = 'data/accounts.json'
    password_hash_iterations: int = 200_000
    expected_client_version: int = 2000
    role_id: int = 10001
    role_name: str = '本地侠客'
    role_model: int = 2000
    default_map_id: int = 58
    map_registry: MapRegistry = field(default_factory=default_map_registry)
    item_registry: object = field(default_factory=default_item_registry)
    shop_registry: object = field(default_factory=default_shop_registry)
    life_registry: object = field(default_factory=default_life_skill_registry)
    sect_registry: SectRegistry = field(default_factory=default_sect_registry)
    # Deprecated aliases retained for protocol helpers and older local tests.
    # Map entry, entities and routing use ``map_registry`` below.
    map_id: int = 58
    map_name: str = '长安'
    map_width: int = 96
    map_height: int = 96
    spawn_x: int = 60
    spawn_y: int = 67
    # Protocol 1126 carries generic map actors.  The client adds 0x200b20 to
    # the raw model id before loading role/<model>.dat; 3760000 therefore maps
    # to the bundled role/5860000.dat sprite.  This model's image ids are
    # present in the local APK's images.o index.
    # Generic map actors can only be removed by the APK's protocol-18 handler
    # when their id is at least 1_000_000. Keep this encounter in that range
    # so victory despawns it before automatic battle mode can re-interact.
    monster_id: int = 1_900_001
    monster_name: str = '试炼妖兽'
    monster_model: int = 3_760_000
    monster_x: int = 10
    monster_y: int = 6
    # Initial facing for the 1126 subtype=0 monster actor, applied right after it
    # is spawned via a 1126 subtype=1 direction frame. 0=down, 1=right, 2=up, 3=left.
    monster_direction: int = 0
    # Minimal cross-map test portal.  The client treats 1126 actors as
    # interactable map objects and sends 1010/action=7 with this id when the
    # player reaches the actor's tile.
    portal_enabled: bool = False
    portal_id: int = 580001
    portal_name: str = '跨地图传送点'
    portal_x: int = 64
    portal_y: int = 67
    # Initial facing for the 1126 subtype=0 portal actor (it reuses the generic
    # b/n entity). Applied via a 1126 subtype=1 direction frame.
    portal_direction: int = 0
    portal_target_map_id: int = 50000
    portal_target_map_name: str = '传送测试区'
    portal_target_spawn_x: int = 8
    portal_target_spawn_y: int = 6
    portal_target_map_o_file: str = 'maps/50000.map.o'
    portal_target_map_ref_available: bool = True
    map_ref_available: bool = True
    return_portal_id: int = 580002
    return_portal_name: str = '返回长安'
    return_portal_x: int = 9
    return_portal_y: int = 6
    # Hand-placed map-58 NPCs. Each entry is a dict with id/name/label/x/y and
    # dat_id for the native 2030 b/t actor sprite. They only spawn on map 58.
    npc_enabled: bool = True
    npcs: list = field(default_factory=list)
    heartbeat_interval_seconds: float = 25.0
    map_o_file: str = 'maps/58.map.o'
    role_data_file: str = 'data/roles.json'
    consignment_data_file: str = 'data/consignment_listings.json'
    exchange_data_file: str = 'data/exchange_orders.json'
    # 仙晶交易所委托费用比例（按订单成交额，银两计）。
    exchange_fee_rate: float = 0.02
    gang_data_file: str = 'data/gangs.json'

    @classmethod
    def load(cls, path: Path) -> 'Settings':
        if not path.exists():
            return cls()
        payload = json.loads(path.read_text(encoding='utf-8'))
        npc_catalog = None
        catalog = Path(__file__).with_name('data') / 'npcs.json'
        if catalog.exists():
            try:
                loaded_catalog = json.loads(catalog.read_text(encoding='utf-8'))
                if isinstance(loaded_catalog, list):
                    npc_catalog = loaded_catalog
            except (OSError, ValueError) as exc:
                LOG.warning('failed to load NPC catalog %s: %s', catalog, exc)

        # maps/<id>/map.json 的动态地图元数据在类型校验前并入注册表载荷。
        registry = load_map_registry(
            merge_dynamic_maps_into_registry_payload(payload),
            npc_catalog=npc_catalog,
        )
        allowed = {
            item.name for item in fields(cls)
        } - {'map_registry', 'item_registry', 'shop_registry', 'life_registry'}
        values = {key: value for key, value in payload.items() if key in allowed}
        values['default_map_id'] = registry.default_map_id
        settings = cls(map_registry=registry, **values)

        # Keep the old public attributes coherent during the compatibility
        # cycle; new map code reads the typed definition instead.
        initial = registry.require(registry.default_map_id)
        settings.map_id = initial.id
        settings.map_name = initial.name
        settings.map_width = initial.fallback_width
        settings.map_height = initial.fallback_height
        settings.spawn_x = initial.spawn_x
        settings.spawn_y = initial.spawn_y
        settings.map_o_file = initial.map_o_file
        settings.map_ref_available = initial.map_ref_available
        settings.npcs = [dict(vars(npc)) for npc in initial.npcs]
        if initial.monster is not None:
            settings.monster_id = initial.monster.id
            settings.monster_name = initial.monster.name
            settings.monster_model = initial.monster.model
            settings.monster_x = initial.monster.x
            settings.monster_y = initial.monster.y
            settings.monster_direction = initial.monster.direction
        if initial.portals:
            portal = initial.portals[0]
            target = registry.require(portal.target_map_id)
            settings.portal_enabled = True
            settings.portal_id = portal.id
            settings.portal_name = portal.name
            settings.portal_x = portal.x
            settings.portal_y = portal.y
            settings.portal_direction = portal.direction
            settings.portal_target_map_id = target.id
            settings.portal_target_map_name = target.name
            settings.portal_target_spawn_x = portal.target_x
            settings.portal_target_spawn_y = portal.target_y
            settings.portal_target_map_o_file = target.map_o_file
            settings.portal_target_map_ref_available = target.map_ref_available
        return settings


class SessionTokenStore:
    """选服会话令牌：1051 签发、1052 核销（网络层会话管理）。"""

    def __init__(self) -> None:
        self._next_session_id = 1000
        self._tokens: dict[tuple[int, int], str] = {}

    def create(self, username: str) -> tuple[int, int]:
        self._next_session_id += 1
        session_id = self._next_session_id
        account_id = session_id + 100000
        self._tokens[(session_id, account_id)] = username
        return session_id, account_id

    def pop(self, session_id: int, account_id: int) -> str:
        return self._tokens.pop((int(session_id), int(account_id)), '')


def heartbeat_challenge(nonce: int) -> bytes:
    """Ask the original client for its built-in 1012 heartbeat response."""
    return encode_frame(1012, [integer(nonce)])


class LocalGameServer:
    """依赖装配 + 系统总线路由 + 网络收发。"""

    def __init__(self, settings: Settings):
        self.settings = settings
        self.accounts = AccountStore(settings)
        self.roles = RoleStore(settings)
        self.character_update_bus = build_character_update_bus(
            # 外观类事件发布后，向视野内持有该角色的其他客户端定向重发 1017
            # （lambda 延迟绑定：构造时 map_system 尚未创建）。
            on_publish=lambda role: self.map_system.broadcast_player_appearance(role),
        )
        # role_id -> (writer, cipher, send_lock) for pushes to online players.
        self.online_connections: dict[int, tuple[asyncio.StreamWriter, GameCipher, asyncio.Lock]] = {}
        self.system_router = SystemRouter()
        self.session_tokens = SessionTokenStore()

        # --- 宠物系统：角色宠物 schema 迁移与 1127/1103/1130 协议入口 ---
        self.pet_system = PetSystem(settings, save=self.roles.save)
        self.roles.role_loaded_hooks.append(self.pet_system.ensure_role_pets)

        # --- 商店 / 技能 ---
        self.shop_system = ShopSystem(
            settings.shop_registry,
            settings.item_registry,
            lambda: self.roles.save(),
            bag_capacity,
            lambda item, registry: item_frame(item, registry=registry, operation=3),
        )
        self.skill_system = SkillSystem(
            settings,
            save=lambda: self.roles.save(),
        )

        # --- 任务（先于地图注册：任务型 1145 优先）---
        self.task_system = TaskSystem(settings.item_registry, self.roles.save)

        # --- 战斗 ---
        self.battle_system = BattleSystem(
            settings,
            save=self.roles.save,
            task_event_recorder=self._record_task_event,
            character_update_bus=self.character_update_bus,
            push_to_role=self._push_to_role,
            online_role_ids=lambda: set(self.online_connections.keys()),
            find_role=self._find_role_by_id,
        )

        # --- 寄售 ---
        self.consignment_system = ConsignmentSystem(
            self.roles,
            settings.item_registry,
            self._resolve_data_path(settings.consignment_data_file),
        )

        # --- 仙晶交易所（1083：应单撮合与委托费用；对话选项 3 由它认领）---
        self.exchange_system = ExchangeSystem(
            self.roles,
            self._resolve_data_path(settings.exchange_data_file),
            fee_rate=settings.exchange_fee_rate,
            notifier=self._push_to_role,
        )

        # --- 帮派（先于地图构造：帮派管理员 NPC 对话 hook 需要它）---
        self.gang_system = GangSystem(
            self._resolve_data_path(settings.gang_data_file),
            lambda: self.roles.save(),
            self._find_role_by_id,
            online_check=lambda role_id: role_id in self.online_connections,
            notifier=self._push_to_role,
        )

        # --- 地图（战斗、任务、寄售对话通过注入协作）---
        self.map_system = MapSystem(
            self._is_known_pathfind_target,
            settings=settings,
            save=lambda: self.roles.save(),
            battle=self.battle_system,
            task_event_recorder=self._record_task_event,
            npc_dialogue_frames_hook=[
                self.consignment_system.npc_dialogue_frames,
                self.gang_system.npc_dialogue_frames,
            ],
            npc_dialogue_option_hook=[
                self.consignment_system.npc_dialogue_option,
                self.exchange_system.npc_dialogue_option,
                self.gang_system.npc_dialogue_option,
            ],
            online_roles_hook=self._online_role_snapshots,
            push_to_role=self._push_to_role,
            team_movement_frame_hook=lambda leader, member, x, y: (
                self.team_system.follow_movement_frame(leader, member, x, y)
            ),
        )

        # --- 角色（含宠物入场帧扩展与登出位置落盘）---
        self.role_system = RoleSystem(
            settings,
            store=self.roles,
            accounts=self.accounts,
            session_tokens=self.session_tokens,
            role_entry_factory=self._role_entry_frames,
            role_list_factory=role_list,
            role_creation_factory=role_creation_frames,
            character_update_bus=self.character_update_bus,
            flush_position=self._flush_position,
        )

        # --- 背包 ---
        self.inventory_system = InventorySystem(
            settings,
            save=self.roles.save,
            character_update_bus=self.character_update_bus,
            appearance_broadcast_hook=lambda role: (
                self.map_system.broadcast_player_appearance(role)
            ),
        )

        # --- 福缘 ---
        self.fuyuan_system = FuyuanSystem(save=self.roles.save)

        # --- 玩家交互（必须先于 role/inventory 注册：1023 邀请动作、
        #     1089/byte-2 查看与 1009/81 赠送从全量认领中精确剥离）---
        self.social_system = SocialSystem(
            settings,
            save=self.roles.save,
            find_role=self._find_role_by_id,
            online_role_ids=lambda: set(self.online_connections.keys()),
            push_to_role=self._push_to_role,
            battle_system=self.battle_system,
        )
        self.team_system = TeamSystem(
            settings,
            find_role=self._find_role_by_id,
            online_role_ids=lambda: set(self.online_connections.keys()),
            push_to_role=self._push_to_role,
            can_follow=self.map_system.can_players_see_each_other,
        )

        # --- 总线注册（顺序即优先级：宠物先于角色认领 1103，
        #     角色先于地图认领 1010/36 与登出页，任务先于地图认领 1145）---
        register_team_routes(self.system_router, self.team_system)
        register_social_routes(self.system_router, self.social_system)
        register_pet_routes(self.system_router, self.pet_system)
        register_role_routes(self.system_router, self.role_system)
        register_shop_routes(self.system_router, self.shop_system)
        register_skill_routes(self.system_router, self.skill_system)
        register_inventory_routes(self.system_router, self.inventory_system)
        register_battle_routes(self.system_router, self.battle_system)
        register_task_routes(self.system_router, self.task_system)
        register_gang_routes(self.system_router, self.gang_system)
        register_consignment_routes(self.system_router, self.consignment_system)
        register_exchange_routes(self.system_router, self.exchange_system)
        register_fuyuan_routes(self.system_router, self.fuyuan_system)
        register_map_routes(self.system_router, self.map_system)

    # ------------------------------------------------------------------
    # 装配辅助
    # ------------------------------------------------------------------
    def _resolve_data_path(self, configured: str) -> Path:
        path = Path(configured)
        return path if path.is_absolute() else Path(__file__).resolve().parent / path

    def _find_role_by_id(self, role_id: int) -> dict[str, object] | None:
        for roles in self.roles.data['accounts'].values():
            if not isinstance(roles, list):
                continue
            for role in roles:
                if isinstance(role, dict) and int(role.get('id', 0) or 0) == int(role_id):
                    return role
        return None

    def _online_role_snapshots(self) -> list[dict[str, object]]:
        """Live role records for every online role (same-map visibility).

        Returns the store's own role dicts, so map/x/y/name/model reads stay
        current with movement checkpoints without copying.
        """
        snapshots: list[dict[str, object]] = []
        for role_id in list(self.online_connections):
            role = self._find_role_by_id(role_id)
            if role is not None:
                snapshots.append(role)
        return snapshots

    def _record_task_event(self, role, kind: str, **kwargs) -> tuple[bytes, ...]:
        kwargs.setdefault('now', time.time())
        return self.task_system.record_event(role, kind, **kwargs)

    def _role_entry_frames(self, settings: Settings, role: dict[str, object]) -> tuple[bytes, ...]:
        """角色入场帧 = 角色系统基础序列 + 宠物容器帧。"""
        return (
            *role_entry_frames(settings, role),
            *self.pet_system.role_entry_frames(role),
        )

    def _flush_position(self, context: SystemContext) -> None:
        self.map_system.flush_position(context.session)

    def _is_known_pathfind_target(self, map_id: int, x: int, y: int) -> bool:
        """Allow the shared 1145 pathfinder to target gathers or task NPCs."""
        if self.task_system.matches_path_target(map_id, x, y):
            return True
        return any(
            target.map_id == int(map_id)
            and target.x == int(x)
            and target.y == int(y)
            for target in self.settings.life_registry.gather_targets
        )

    def _push_to_role(self, role_id: int, frames: tuple[bytes, ...]) -> None:
        """Push frames to an online player outside the request/response cycle.

        Called from gang mutations while the requesting connection's event
        loop is running; failures (closed sockets) are logged and dropped.
        """
        connection = self.online_connections.get(int(role_id))
        if connection is None or not frames:
            return
        writer, cipher, lock = connection

        async def _push() -> None:
            try:
                await self._send(writer, *frames, cipher=cipher, lock=lock)
            except (ConnectionResetError, asyncio.IncompleteReadError, OSError) as exc:
                LOG.debug('push to role %d failed: %s', role_id, exc)

        asyncio.get_running_loop().create_task(_push())

    # ------------------------------------------------------------------
    # 网络收发
    # ------------------------------------------------------------------
    async def _send(
        self,
        writer: asyncio.StreamWriter,
        *frames: bytes,
        cipher: GameCipher | None = None,
        lock: asyncio.Lock | None = None,
    ) -> None:
        async def send_frames() -> None:
            for frame in frames:
                writer.write(cipher.encrypt_server_frame(frame) if cipher is not None else frame)
            await writer.drain()

        if lock is None:
            await send_frames()
        else:
            # GameCipher is stateful. Keep encryption and socket writes in one
            # critical section so heartbeat and request replies cannot interleave.
            async with lock:
                await send_frames()

    async def _heartbeat_loop(
        self,
        writer: asyncio.StreamWriter,
        cipher: GameCipher,
        send_lock: asyncio.Lock,
        peer: object,
        active_role_getter=None,
    ) -> None:
        nonce = 0
        try:
            while True:
                await asyncio.sleep(self.settings.heartbeat_interval_seconds)
                active_role = active_role_getter() if active_role_getter else None
                settle_frames = self.fuyuan_system.settle_and_frames(active_role)
                if settle_frames:
                    await self._send(writer, *settle_frames, cipher=cipher, lock=send_lock)
                nonce = 1 if nonce >= 0x7FFFFFFF else nonce + 1
                await self._send(
                    writer,
                    heartbeat_challenge(nonce),
                    cipher=cipher,
                    lock=send_lock,
                )
                LOG.info('heartbeat sent to %s nonce=%d', peer, nonce)
        except (ConnectionResetError, BrokenPipeError, OSError):
            return

    # ------------------------------------------------------------------
    # 连接主循环：解码 -> 总线分发 -> 应答
    # ------------------------------------------------------------------
    async def handle(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        peer = writer.get_extra_info('peername')
        LOG.info('client connected: %s', peer)
        # 连接级会话：各系统把自己的连接状态存放在这里（战斗状态、采集、
        # 商城页签、流式 NPC、位置检查点、福缘报价等），断线后整体丢弃。
        session: dict[str, object] = {}
        game_cipher: GameCipher | None = None
        send_lock = asyncio.Lock()
        heartbeat_task: asyncio.Task[None] | None = None
        online_registered_role_id: int | None = None

        async def push(*frames: bytes) -> None:
            await self._send(writer, *frames, cipher=game_cipher, lock=send_lock)

        session['push_frames'] = push

        try:
            while True:
                header = await reader.readexactly(2)
                frame_length = struct.unpack('>H', header)[0]
                if frame_length < 4:
                    raise ProtocolError(f'invalid frame length {frame_length}')
                payload = await reader.readexactly(frame_length - 2)
                if len(payload) < 2:
                    raise ProtocolError('payload is missing the message id')
                message_hint = struct.unpack_from('>H', payload, 0)[0]
                if game_cipher is None and message_hint == 1052:
                    game_cipher = GameCipher()
                    LOG.info('game cipher enabled for %s', peer)
                decoded_payload = payload
                if game_cipher is not None:
                    decoded_payload = payload[:2] + game_cipher.decrypt(payload[2:])
                try:
                    message_id, fields = decode_payload(decoded_payload)
                except ProtocolError:
                    LOG.warning('raw payload message_hint=%d hex=%s', message_hint, payload.hex())
                    raise
                values = field_values(fields)
                LOG.info('received message=%d field_types=%s', message_id, [x.type_id for x in fields])

                # 福缘周期结算：每条消息与心跳前结算一次到期点数。
                settle_frames = self.fuyuan_system.settle_and_frames(session.get('active_role'))
                if settle_frames:
                    await push(*settle_frames)

                context = SystemContext(
                    username=str(session.get('username', '')),
                    active_role=session.get('active_role'),
                    session=session,
                )
                route_result = self.system_router.dispatch(context, message_id, fields)
                if route_result.frames:
                    await push(*route_result.frames)
                elif not route_result.handled:
                    LOG.info(
                        'ignored unimplemented message=%d values=%r',
                        message_id, values,
                    )

                # 会话簿记：角色选择后的在线登记与跨系统连接状态复位。
                selected_role_id = session.pop('role.selected_role_id', None)
                if selected_role_id is not None and session.get('active_role') is not None:
                    role_id = int(selected_role_id)
                    if online_registered_role_id is not None and online_registered_role_id != role_id:
                        # 同连接切换角色：先向旧角色所在图的在线玩家广播移除，
                        # 再登记新角色（登记顺序保证 depart 的快照不含新角色）。
                        previous_role = self._find_role_by_id(online_registered_role_id)
                        self.map_system.depart_map(session, role=previous_role)
                        self.team_system.on_disconnect(online_registered_role_id)
                        self.online_connections.pop(online_registered_role_id, None)
                    session['map.world_sent'] = False
                    session.pop('map.streamed_npcs', None)
                    session['fuyuan'] = None
                    self.online_connections[role_id] = (writer, game_cipher, send_lock)
                    online_registered_role_id = role_id

                if heartbeat_task is None and game_cipher is not None and session.get('game_ready'):
                    heartbeat_task = asyncio.create_task(
                        self._heartbeat_loop(writer, game_cipher, send_lock, peer, lambda: session.get('active_role'))
                    )
        except (asyncio.IncompleteReadError, ConnectionResetError):
            LOG.info('client disconnected: %s', peer)
        except (ProtocolError, UnicodeDecodeError, ValueError) as exc:
            LOG.warning('protocol error from %s: %s', peer, exc)
        finally:
            if online_registered_role_id is not None:
                registered = self.online_connections.get(online_registered_role_id)
                if registered is not None and registered[0] is writer:
                    self.online_connections.pop(online_registered_role_id, None)
                    self.team_system.on_disconnect(online_registered_role_id)
            # Cancel any active gather; the socket is closing so the 2027
            # interrupt frame must NOT be sent.
            gathering = session.get('gathering')
            if gathering is not None:
                gathering.cancel()
            if self.map_system.flush_position(session):
                active_role = session.get('active_role')
                if active_role is not None:
                    LOG.info(
                        'ROLE_POSITION_DISCONNECT_SAVE '
                        'user=%r role_id=%d map=%d tile=%d,%d',
                        session.get('username', ''),
                        int(active_role.get('id', 0)),
                        int(active_role.get('map_id', self.settings.default_map_id)),
                        int(active_role.get('map_x', 0)),
                        int(active_role.get('map_y', 0)),
                    )
            # 断线离场：向最后公告地图的在线玩家广播 1010/action=18 移除。
            self.map_system.depart_map(session)
            # 断线退出对决：对手收到结束帧，避免对局悬挂。
            if online_registered_role_id is not None:
                abandoned = self.battle_system.abandon_duels(online_registered_role_id)
                if abandoned is not None:
                    peer_id, duel_frames = abandoned
                    self._push_to_role(peer_id, duel_frames)
            if heartbeat_task is not None:
                heartbeat_task.cancel()
                with contextlib.suppress(asyncio.CancelledError):
                    await heartbeat_task
            writer.close()
            try:
                await writer.wait_closed()
            except (ConnectionResetError, OSError):
                pass


def build_character_update_bus(on_publish=None):
    """角色刷新总线（装配期绑定角色系统的已验证刷新帧构造器）。"""
    from systems.inventory.service import is_role_item_equipped
    from systems.role.events import CharacterUpdateBus
    from systems.role.protocol import (
        character_equipment_refresh_frames, equipment_panel_refresh_frame,
    )
    return CharacterUpdateBus(
        build_full_refresh=character_equipment_refresh_frames,
        build_appearance_refresh=lambda role, registry: (
            equipment_panel_refresh_frame(role, registry),
        ),
        is_item_equipped=is_role_item_equipped,
        on_publish=on_publish,
    )


async def run(settings: Settings) -> None:
    handler = LocalGameServer(settings)
    server = await asyncio.start_server(handler.handle, settings.host, settings.port)
    addresses = ', '.join(str(sock.getsockname()) for sock in server.sockets or [])
    LOG.info('listening on %s; advertising %s:%d', addresses, settings.advertise_host, settings.port)
    async with server:
        await server.serve_forever()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Piao Miao San Jie 2 local login/game prototype')
    parser.add_argument('--config', type=Path, default=Path(__file__).with_name('config.json'))
    parser.add_argument('--host')
    parser.add_argument('--port', type=int)
    parser.add_argument('--advertise-host')
    parser.add_argument('--server-name')
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    settings = Settings.load(args.config)
    for name in ('host', 'port', 'advertise_host', 'server_name'):
        value = getattr(args, name)
        if value is not None:
            setattr(settings, name, value)
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    # 启动前物化动态地图（maps/<id>/map.json -> .map.ref/.map.o）。
    built_maps = materialize_all_dynamic_maps()
    for built in built_maps:
        LOG.info(
            'DYNAMIC_MAP_READY map=%d ref=%s ref_bytes=%d map_o=%s map_o_bytes=%d',
            built.map_id,
            built.map_ref_path,
            built.map_ref_bytes,
            built.map_o_path,
            built.map_o_bytes,
        )
    LOG.info('DYNAMIC_MAP_SCAN count=%d', len(built_maps))
    try:
        asyncio.run(run(settings))
    except KeyboardInterrupt:
        LOG.info('server stopped')


if __name__ == '__main__':
    main()
