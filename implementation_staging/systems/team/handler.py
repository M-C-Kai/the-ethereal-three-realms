"""One owner for 1023 team requests and cross-player roster synchronization."""
from __future__ import annotations

import logging
from typing import Callable

from app.context import SystemContext
from app.notify import top_message_frame
from app.router import RouteResult, SystemRouter
from systems.map.protocol import player_actor_object_id
from systems.role.protocol import role_property_fields
from systems.role.service import normalized_sect_id
from systems.team import service
from systems.team.protocol import (
    disband_frame, follow_chain_frame, invite_frame, leader_flag_frame, member_frame,
    member_removed_frame, member_state_frame, team_role_flag_frame,
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
                    self.push_to_role(member_id, (
                        leader_flag_frame(member_id, False), disband_frame(),
                    ))
            return RouteResult.handled((leader_flag_frame(role_id, False), disband_frame()))

        if action in (1, 12):
            # 离队/踢出：et 踢出确认发 12 [目标条目 id=actor]，离队发 1 [自己]。
            # S→C 1023/1 [id] 一帧两用：id=自己 → aa.i() 清空自己的队伍
            # 状态；id=他人 → aa.a(id)Z 移除该行并停掉其跟随。
            team = self.registry.team_of(role_id)
            if team is None:
                return RouteResult.handled()
            if len(values) > 1:
                target_id = self._normalize_member_id(team, int(values[1]))
                if target_id is None:
                    return RouteResult.handled()
            else:
                target_id = role_id
            if target_id != role_id and team.leader_id != role_id:
                return RouteResult.handled()
            if target_id == team.leader_id:
                # 队长离队 = 解散
                _, members = self.registry.leave(target_id)
                for member_id in members:
                    self.registry.clear_pending_for(member_id)
                    if member_id != role_id and member_id in online:
                        self.push_to_role(member_id, (disband_frame(),))
                return RouteResult.handled((leader_flag_frame(role_id, False), disband_frame()))
            _, remaining = self.registry.leave(target_id)
            self.registry.clear_pending_for(target_id)
            for member_id in remaining:
                if member_id in online:
                    self.push_to_role(member_id, (member_removed_frame(
                        self._entry_id(member_id, target_id)),))
            if target_id != role_id and target_id in online:
                self.push_to_role(target_id, (
                    leader_flag_frame(target_id, False), disband_frame(),
                ))
            self._push_follow_chains(team, online)
            if target_id == role_id:
                # 主动离队：1023/11 清花名册，同时清自己的 prop0 队员位
                return RouteResult.handled((
                    leader_flag_frame(role_id, False), disband_frame(),
                ))
            return RouteResult.handled((
                member_removed_frame(target_id), top_message_frame('队员已离队'),
            ))

        if action == 20:
            # 升为队长：et 确认框(id=2)发 20 [目标条目 id=actor]；
            # 地图菜单"交队"确认(44)同样发 20 [目标 actor id]。
            # S→C 1023/20 [新队长] → 每个客户端 aa.d(id) 把该行移到 aa.a
            # 首位（成员页第 0 行标"队长"）；随后双向 1017 队长旗刷新
            # （新队长的 Z() 立起来才能重建跟随链），最后全队重发 1038 链。
            team = self.registry.team_of(role_id)
            if team is None or len(values) < 2:
                return RouteResult.handled()
            target_id = self._normalize_member_id(team, int(values[1]))
            if team.leader_id != role_id:
                return self._notice('只有队长可以移交队长')
            if target_id is None or target_id == role_id:
                return RouteResult.handled()
            old_leader_id = team.leader_id
            self.registry.promote(target_id)
            team = self.registry.team_of(role_id)
            for member_id in team.members:
                if member_id in online:
                    # 每个客户端 aa.d(id) 把新队长行移到 aa.a 首位；
                    # id 必须是该客户端行内的条目 id（自己 raw / 他人 actor）
                    self.push_to_role(member_id, (member_state_frame(
                        20, self._entry_id(member_id, target_id)),))
            for viewer_id in team.members:
                if viewer_id not in online:
                    continue
                self.push_to_role(viewer_id, (
                    team_role_flag_frame(
                        self._entry_id(viewer_id, target_id), True),
                    team_role_flag_frame(
                        self._entry_id(viewer_id, old_leader_id), False),
                ))
            self._push_follow_chains(team, online)
            if target_id in online:
                self.push_to_role(target_id, (top_message_frame('你已成为新队长'),))
            LOG.info('TEAM_1023 promote leader=%s new_leader=%d', old_leader_id, target_id)
            if role_id == old_leader_id:
                return RouteResult.handled((top_message_frame(f"{self._name_of(target_id)} 已成为新队长"),))
            return RouteResult.handled((top_message_frame('你已成为新队长'),))

        if action == 19:
            # 召集队员：et 菜单发 19 [目标条目 id=actor]，仅对暂离队员有效
            # （客户端对未暂离目标直接提示，不发帧）。
            team = self.registry.team_of(role_id)
            if team is None or len(values) < 2:
                return RouteResult.handled()
            target_id = self._normalize_member_id(team, int(values[1]))
            if team.leader_id != role_id:
                return self._notice('只有队长可以召集队员')
            if target_id is None or target_id == role_id:
                return RouteResult.handled()
            if target_id not in team.away:
                return self._notice('当前队员并未暂离队伍！')
            team.away.discard(target_id)
            for member_id in team.members:
                if member_id in online:
                    self.push_to_role(member_id, (member_state_frame(
                        17, self._entry_id(member_id, target_id)),))
            self._push_follow_chains(team, online)
            if target_id in online:
                self.push_to_role(target_id, (
                    top_message_frame(f"队长 {self._name_of(role_id)} 召集你归队"),
                ))
            LOG.info('TEAM_1023 summon leader=%d target=%d', role_id, target_id)
            return RouteResult.handled((top_message_frame('已召集队员归队'),))


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

        if action in (7, 8):
            # 0x51 申请列表页（e/eo）按钮：允许加入→7、拒绝加入→8，
            # C→S [short 7|8, int 申请人 role id]。
            applicant_id = int(values[1]) if len(values) > 1 else 0
            applicant = self.find_role(applicant_id)
            at = service.now()
            requester_id = self.registry.pop_join_request(role_id, at)
            if action == 8:
                self.registry.clear_pending_for(role_id)
                if applicant_id in online:
                    self.push_to_role(applicant_id, (top_message_frame('对方拒绝了你的入队申请'),))
                return self._notice('已拒绝该入队申请')
            if requester_id is None or int(requester_id) != applicant_id:
                return self._notice('入队申请已过期')
            if applicant is None or applicant_id not in online:
                return self._notice('对方不在线')
            return self._join(role_id, applicant_id)

        if action in (17, 18):
            team = self.registry.team_of(role_id)
            if team is None:
                return self._notice('当前没有加入队伍')
            if action == 18:
                team.away.add(role_id)
            else:
                team.away.discard(role_id)
            for member_id in team.members:
                if member_id in online:
                    self.push_to_role(member_id, (member_state_frame(
                        action, self._entry_id(member_id, role_id)),))
            if action == 17:
                # 归队客户端侧只清空本地队列，不重建链（e.ag sswitch_c6）；
                # 链必须由服务端的 1038 重发。
                self._push_follow_chains(team, online)
            return self._notice('已暂离' if action == 18 else '已归队')

        return RouteResult.handled()

    def _push_follow_chains(self, team, online: set[int]) -> None:
        """向全队每个在线成员发送按其定制的 1038 跟随链帧。

        链头是队长；链员为全部未暂离队员。队员客户端只有在双方
        1014 已互见（can_follow=True，m.o 能命中队长 actor）时才挂链，
        否则等队长下一次移动由 follow_movement_frame 补挂；队长客户端
        的链头是自己（m.o 按 raw id 必中），始终可挂。
        """
        leader_id = team.leader_id
        followers = [m for m in team.members if m != leader_id and m not in team.away]
        if not followers:
            return
        leader = self.find_role(leader_id)
        if leader is None:
            return
        x = int(leader.get('map_x', getattr(self.settings, 'spawn_x', 0)) or 0)
        y = int(leader.get('map_y', getattr(self.settings, 'spawn_y', 0)) or 0)
        for viewer_id in (leader_id, *followers):
            if viewer_id not in online:
                continue
            if viewer_id != leader_id and not self.can_follow(leader_id, viewer_id):
                continue
            self.push_to_role(viewer_id, (
                follow_chain_frame(leader_id, viewer_id, followers, x, y),
            ))

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
        member_frames = [
            self._record(leader, viewer_id=member_id),
            self._record(member, viewer_id=member_id),
        ]
        # prop0 队员位（0x200000）：主菜单"队伍"项按 b/v.aa() 判断已入队，
        # 缺位时"队伍"页永远显示"你目前尚未组队"帮助页。
        member_frames.append(team_role_flag_frame(member_id, False))
        member_frames.append(top_message_frame(f"已加入 {leader.get('name', '')} 的队伍"))
        self.push_to_role(member_id, tuple(member_frames))
        self.push_to_role(leader_id, (self._record(member, viewer_id=leader_id),
                          top_message_frame(f"{member.get('name', '')} 加入了队伍")))
        # 双端跟随链：队员客户端挂链后由队长 1038 走位同步；队长客户端
        # 挂链用于本地拖拽队员形象。id 按 m.o 语义对每个接收方定制。
        self._push_follow_chains(team, self.online_role_ids())
        LOG.info('TEAM_1023 join role_id=%d leader=%d members=%s', member_id, leader_id, team.members)
        return self._notice('已加入队伍')

    def _normalize_member_id(self, team, sent_id: int) -> int | None:
        """C→S 菜单帧可能携带 raw role id 或 actor id（行内条目 id），归一化。"""
        sent = int(sent_id)
        if sent in team.members:
            return sent
        from systems.map.protocol import PLAYER_ACTOR_ID_BASE
        role_id = sent - PLAYER_ACTOR_ID_BASE
        if role_id in team.members:
            return role_id
        return None

    def _entry_id(self, viewer_id: int, member_id: int) -> int:
        """b/m.o 语义的接收方定制 id：本机自己 = raw role id，他人 = actor id。"""
        member_id = int(member_id)
        return member_id if member_id == int(viewer_id) else player_actor_object_id(member_id)

    def _record(self, role: dict, viewer_id: int | None = None) -> bytes:
        properties = role_property_fields(self.settings, role)
        role_id = int(role['id'])
        entry_id = role_id if viewer_id is None else self._entry_id(viewer_id, role_id)
        return member_frame(
            str(role.get('name', '')), entry_id,
            int(properties[40].value), int(properties[42].value),
            int(properties[11].value), int(properties[12].value),
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

    def _name_of(self, role_id: int) -> str:
        role = self.find_role(int(role_id))
        return str(role.get('name', '')) if role else str(role_id)

    def resync_role(self, role_id: int) -> None:
        """重连/重登后重建该客户端的队伍状态（aa.a 行、prop0 位、跟随链）。

        队伍注册表在进程内存活而客户端状态随连接丢失；角色再次入场后
        调用本方法把花名册、prop0 位与 1038 链补发一次。行 id 仍按
        b/m.o 语义定制：自己 = raw role id，他人 = actor id。
        """
        team = self.registry.team_of(int(role_id))
        if team is None:
            return
        online = self.online_role_ids()
        if int(role_id) not in online:
            return
        viewer = self.find_role(int(role_id))
        if viewer is None:
            return
            team.away.discard(target_id)
            for member_id in team.members:
                if member_id in online:
                    self.push_to_role(member_id, (member_state_frame(
                        17, self._entry_id(member_id, target_id)),))
        is_leader = team.leader_id == int(role_id)
        frames.append(team_role_flag_frame(int(role_id), is_leader))
        frames.append(top_message_frame('已恢复队伍状态'))
        self.push_to_role(int(role_id), tuple(frames))
        self._push_follow_chains(team, online)
        LOG.info('TEAM_1023 resync role_id=%d leader=%d members=%s',
                 role_id, team.leader_id, team.members)

    def on_disconnect(self, role_id: int) -> None:
        """断线清理：注册表移除 + 留存客户端的花名册/prop0/跟随链同步。

        队员掉线：其余成员按各自视角收 1023/1（他人 = actor id，
        aa.a(id) 才能在本机行内命中并移除该行），随后重建 1038 链。
        队长掉线 = 解散：1023/11 清花名册，并清每个留存者的 prop0 位
        （aa.i() 不清 prop0，缺位会让"队伍"菜单仍判已组队）。
        """
        role_id = int(role_id)
        self.registry.clear_pending_for(role_id)
        team, remaining = self.registry.leave(role_id)
        if team is None:
            return
        online = self.online_role_ids()
        if team.leader_id == role_id:
            for member_id in remaining:
                if member_id != role_id and member_id in online:
                    self.push_to_role(member_id, (
                        leader_flag_frame(member_id, False), disband_frame(),
                    ))
            return
        for member_id in remaining:
            if member_id != role_id and member_id in online:
                self.push_to_role(member_id, (member_removed_frame(
                    self._entry_id(member_id, role_id)),))
        self._push_follow_chains(team, online)

    def follow_movement_frame(self, leader_id: int, member_id: int, x: int, y: int) -> bytes | None:
        """Replace the member's 1005 leader update with a native 1038 chain.

        APK 1005 对被移动 actor 调用 v.ad()，把 J 重置为宠物链接，拆掉
        跟随链；1038/e.ai 在一帧内重挂全链并把链头走到 (x,y)。帧中的 id
        按 member_id（接收方）定制：队长用 actor id，member 自己放链表
        首位用 raw id，其余队员用 actor id（b/m.o 的查找语义）。
        """
        team = self.registry.team_of(member_id)
        if (team is None or team.leader_id != int(leader_id)
                or int(member_id) == int(leader_id) or member_id in team.away):
            return None
        followers = [m for m in team.members if m != team.leader_id and m not in team.away]
        return follow_chain_frame(int(leader_id), int(member_id), followers, x, y)


def register_team_routes(router: SystemRouter, system: TeamSystem) -> None:
    router.register(system.system_name, system.can_handle, system.handle)
