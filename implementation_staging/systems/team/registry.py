"""Single in-memory authority for teams and pending invitations."""
from __future__ import annotations

from dataclasses import dataclass, field

TEAM_MAX_MEMBERS = 3
INVITE_TTL_SECONDS = 60.0


@dataclass
class TeamState:
    leader_id: int
    members: list[int] = field(default_factory=list)
    away: set[int] = field(default_factory=set)

    @property
    def full(self) -> bool:
        return len(self.members) >= TEAM_MAX_MEMBERS


class TeamRegistry:
    def __init__(self) -> None:
        self.teams: dict[int, TeamState] = {}
        self.member_to_leader: dict[int, int] = {}
        self.invites: dict[int, tuple[int, float]] = {}
        self.join_requests: dict[int, tuple[int, float]] = {}

    def team_of(self, role_id: int) -> TeamState | None:
        leader_id = self.member_to_leader.get(int(role_id))
        return self.teams.get(leader_id) if leader_id is not None else None

    def create(self, leader_id: int) -> TeamState:
        leader_id = int(leader_id)
        existing = self.team_of(leader_id)
        if existing is not None:
            return existing
        team = TeamState(leader_id, [leader_id])
        self.teams[leader_id] = team
        self.member_to_leader[leader_id] = leader_id
        return team

    def join(self, leader_id: int, member_id: int) -> TeamState | None:
        team = self.teams.get(int(leader_id))
        member_id = int(member_id)
        if team is None or team.full or self.team_of(member_id) is not None:
            return None
        team.members.append(member_id)
        self.member_to_leader[member_id] = team.leader_id
        return team

    def promote(self, new_leader_id: int) -> TeamState | None:
        """提升新队长：aa.a 语义要求队长行在所有客户端都排首位。"""
        new_leader_id = int(new_leader_id)
        team = self.team_of(new_leader_id)
        if team is None or team.leader_id == new_leader_id:
            return team
        old_leader_id = team.leader_id
        team.members.remove(new_leader_id)
        team.members.insert(0, new_leader_id)
        team.leader_id = new_leader_id
        self.teams.pop(old_leader_id, None)
        self.teams[new_leader_id] = team
        for member_id in team.members:
            self.member_to_leader[member_id] = new_leader_id
        return team

    def leave(self, role_id: int) -> tuple[TeamState | None, list[int]]:
        role_id = int(role_id)
        team = self.team_of(role_id)
        if team is None:
            return None, []
        if role_id == team.leader_id:
            members = list(team.members)
            self.teams.pop(team.leader_id, None)
            for member_id in members:
                self.member_to_leader.pop(member_id, None)
            return team, members
        team.members.remove(role_id)
        team.away.discard(role_id)
        self.member_to_leader.pop(role_id, None)
        return team, list(team.members)

    @staticmethod
    def _pop_pending(table: dict[int, tuple[int, float]], key: int, at: float) -> int | None:
        row = table.pop(int(key), None)
        if row is None or at - row[1] > INVITE_TTL_SECONDS:
            return None
        return row[0]

    def pop_invite(self, member_id: int, at: float) -> int | None:
        return self._pop_pending(self.invites, member_id, at)

    def pop_join_request(self, leader_id: int, at: float) -> int | None:
        return self._pop_pending(self.join_requests, leader_id, at)

    def clear_pending_for(self, role_id: int) -> None:
        role_id = int(role_id)
        for table in (self.invites, self.join_requests):
            table.pop(role_id, None)
            for target, (source, _) in list(table.items()):
                if source == role_id:
                    table.pop(target, None)
