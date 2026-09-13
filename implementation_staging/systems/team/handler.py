"""One owner for 1023 team requests and cross-player roster synchronization."""
from __future__ import annotations

import logging
from typing import Callable

from app.context import SystemContext
from app.notify import top_message_frame
from app.router import RouteResult, SystemRouter
from systems.role.protocol import role_property_fields
from systems.role.service import normalized_sect_id
from systems.team import service
from systems.team.protocol import (
    disband_frame, follow_chain_frame, invite_frame, leader_flag_frame, member_frame,
    member_removed_frame, member_state_frame,
)
from systems.team.registry import TeamRegistry

LOG = logging.getLogger('piaomiao-local')


class TeamSystem:
    system_name = 'team'

    def __init__(self, settings=None,
                 find_role: Callable[[int], dict | None] | None = None,
                 online_role_ids: Callable[[], set[int]] | None = None,
                 push_to_role: Callable[[int, tuple[bytes, ...]], None] | None = None,
                 can_follow: Callable[[int, int], bool] | None = None) -> None:
        self.settings = settings
        self.find_role = find_role or (lambda role_id: None)
        self.online_role_ids = online_role_ids or (lambda: set())
        self.push_to_role = push_to_role or (lambda role_id, frames: None)
        self.can_follow = can_follow or (lambda leader_id, member_id: False)
        self.registry = TeamRegistry()

    def can_handle(self, context: SystemContext, message_id: int, fields: list[object]) -> bool:
        return message_id == 1023 and context.active_role is not None and bool(fields)

    def handle(self, context: SystemContext, message_id: int, fields: list[object]) -> RouteResult:
        values = [field.value for field in fields]
        action = int(values[0])
        role = context.active_role
        role_id = int(role['id'])
        online = self.online_role_ids()
        if action == 0:
            if len(values) < 2 or int(values[1]) != role_id:
                return RouteResult.handled()
            if self.registry.team_of(role_id) is not None:
                return RouteResult.handled()
            self.registry.create(role_id)
            return RouteResult.handled((leader_flag_frame(role_id, True), self._record(role)))

        if action == 11:
            team = self.registry.team_of(role_id)
            if team is None or team.leader_id != role_id:
                return RouteResult.handled((leader_flag_frame(role_id, False), disband_frame()))
            _, members = self.registry.leave(role_id)
            for member_id in members:
                self.registry.clear_pending_for(member_id)
                if member_id != role_id and member_id in online:
                    self.push_to_role(member_id, (disband_frame(),))
            return RouteResult.handled((leader_flag_frame(role_id, False), disband_frame()))

        if action == 1:
            target_id = int(values[1]) if len(values) > 1 else role_id
            team = self.registry.team_of(role_id)
            if team is None or target_id not in team.members:
                return RouteResult.handled()
            if target_id != role_id and team.leader_id != role_id:
                return RouteResult.handled()
            if target_id == team.leader_id:
                _, members = self.registry.leave(target_id)
                for member_id in members:
                    self.registry.clear_pending_for(member_id)
                    if member_id != role_id and member_id in online:
                        self.push_to_role(member_id, (disband_frame(),))
                return RouteResult.handled((leader_flag_frame(role_id, False), disband_frame()))
            _, remaining = self.registry.leave(target_id)
            self.registry.clear_pending_for(target_id)
            for member_id in remaining:
                if member_id != role_id and member_id in online:
                    self.push_to_role(member_id, (member_removed_frame(target_id),))
            if target_id != role_id and target_id in online:
                self.push_to_role(target_id, (disband_frame(),))
            if target_id == role_id:
                return RouteResult.handled((disband_frame(),))
            return RouteResult.handled((
                member_removed_frame(target_id), top_message_frame('队员已离队'),
            ))

        if action == 2:
            target_id = service.role_id_from_actor(int(values[1])) if len(values) > 1 else 0
            target = self.find_role(target_id)
            if target is None or target_id not in online:
                return self._notice('对方不在线')
            if target_id == role_id:
                return self._notice('不能邀请自己')
            if self.registry.team_of(target_id) is not None:
                return self._notice('对方已在其他队伍中')
            team = self.registry.team_of(role_id)
            own_frames: tuple[bytes, ...] = ()
            if team is None:
                team = self.registry.create(role_id)
                own_frames = (leader_flag_frame(role_id, True), self._record(role))
            if team.leader_id != role_id or team.full:
                return self._notice('队伍已满')
            self.registry.invites[target_id] = (role_id, service.now())
            self.push_to_role(target_id, (self._invite(role),))
            return RouteResult.handled((*own_frames, top_message_frame('组队邀请已发送')))

        if action == 3:
            peer_id = int(values[1]) if len(values) > 1 else 0
            at = service.now()
            leader_id = self.registry.pop_invite(role_id, at)
            if leader_id == peer_id and leader_id in online:
                return self._join(leader_id, role_id)
            requester_id = self.registry.pop_join_request(role_id, at)
            if requester_id == peer_id and requester_id in online:
                return self._join(role_id, requester_id)
            return self._notice('组队邀请已过期')

        if action == 4:
            peer_id = int(values[1]) if len(values) > 1 else 0
            self.registry.clear_pending_for(role_id)
            if peer_id in online:
                self.push_to_role(peer_id, (top_message_frame('对方拒绝了组队邀请'),))
            return RouteResult.handled()

        if action == 6:
            leader_id = int(values[1]) if len(values) > 1 else 0
            leader = self.find_role(leader_id)
            if leader is None or leader_id not in online:
                return self._notice('对方不在线')
            team = self.registry.team_of(leader_id)
            if team is None:
                return self._notice('对方尚未建立队伍')
            if team.leader_id != leader_id or team.full or self.registry.team_of(role_id):
                return self._notice('无法申请加入队伍')
            self.registry.join_requests[leader_id] = (role_id, service.now())
            self.push_to_role(leader_id, (self._invite(role),))
            return self._notice('入队申请已发送')

        if action in (17, 18):
            team = self.registry.team_of(role_id)
            if team is None:
                return self._notice('当前没有加入队伍')
            if action == 18:
                team.away.add(role_id)
            else:
                team.away.discard(role_id)
            frame = member_state_frame(action, role_id)
            for member_id in team.members:
                if member_id in online:
                    self.push_to_role(member_id, (frame,))
            return self._notice('已暂离' if action == 18 else '已归队')

        return RouteResult.handled()

    def _join(self, leader_id: int, member_id: int) -> RouteResult:
        leader = self.find_role(leader_id)
        member = self.find_role(member_id)
        if leader is None or member is None:
            return self._notice('对方不在线')
        team = self.registry.join(leader_id, member_id)
        if team is None:
            return self._notice('队伍已满或对方已入队')
        # 1026 appends to APK aa.a. The APK patch keeps roster updates on
        # the current game screen instead of navigating to team page 0x5c.
        member_frames = [self._record(leader), self._record(member)]
        if self.can_follow(leader_id, member_id) and leader_id != member_id:
            member_frames.append(follow_chain_frame(
                leader_id, member_id,
                int(leader.get('map_x', self.settings.spawn_x)),
                int(leader.get('map_y', self.settings.spawn_y)),
            ))
        member_frames.append(top_message_frame(f"已加入 {leader.get('name', '')} 的队伍"))
        self.push_to_role(member_id, tuple(member_frames))
        self.push_to_role(leader_id, (self._record(member),
                          top_message_frame(f"{member.get('name', '')} 加入了队伍")))
        LOG.info('TEAM_1023 join role_id=%d leader=%d members=%s', member_id, leader_id, team.members)
        return self._notice('已加入队伍')

    def _record(self, role: dict) -> bytes:
        properties = role_property_fields(self.settings, role)
        return member_frame(
            str(role.get('name', '')), int(role['id']),
            int(properties[40].value), int(properties[11].value),
            int(properties[42].value), int(properties[12].value),
        )

    def _invite(self, role: dict) -> bytes:
        return invite_frame(
            int(role['id']), str(role.get('name', '')),
            int(role.get('level', 1)),
            normalized_sect_id(role, self.settings.sect_registry),
        )

    @staticmethod
    def _notice(message: str) -> RouteResult:
        return RouteResult.handled((top_message_frame(message),))

    def on_disconnect(self, role_id: int) -> None:
        self.registry.clear_pending_for(role_id)
        team, remaining = self.registry.leave(role_id)
        if team is None:
            return
        frame = disband_frame() if team.leader_id == role_id else member_removed_frame(role_id)
        for member_id in remaining:
            if member_id != role_id and member_id in self.online_role_ids():
                self.push_to_role(member_id, (frame,))

    def follow_movement_frame(self, leader_id: int, member_id: int, x: int, y: int) -> bytes | None:
        """Replace the member's 1005 leader update with a native 1028 chain.

        APK 1005 calls v.ad(), which clears the follow child. 1028/e.ai
        reattaches the local member and moves the leader actor in one frame.
        """
        team = self.registry.team_of(member_id)
        if (team is None or team.leader_id != int(leader_id)
                or int(member_id) == int(leader_id) or member_id in team.away):
            return None
        return follow_chain_frame(leader_id, member_id, x, y)


def register_team_routes(router: SystemRouter, system: TeamSystem) -> None:
    router.register(system.system_name, system.can_handle, system.handle)
