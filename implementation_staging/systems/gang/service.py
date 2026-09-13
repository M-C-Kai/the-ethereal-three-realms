"""Gang system business rules and state.

Membership truth lives on the role dict (``gang_id`` / ``gang_position`` /
``gang_contribution`` / ``gang_joined_at``) so it persists through the normal
``RoleStore`` save.  The gang catalog itself (names, mottos, rosters,
applications, pending invites) persists in its own JSON file.

Local-server bootstrap: the APK has no "create gang" protocol, so the catalog
ships with seed gangs.  A seed gang starts without a leader; the first player
who applies to a leaderless gang is admitted immediately as 帮主 so the
verified leader flows (invite/kick/abdicate/motto/applications) become
reachable.  Leader-led gangs follow the audited APK flow exactly.
"""

from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Dict, Optional, Tuple

from systems.gang.protocol import (
    GangApplicationEntry,
    GangListEntry,
    GangMemberDetail,
    GangMemberEntry,
    GangProtocol,
    application_list_frame,
    gang_close_frame,
    gang_info_frame,
    gang_invite_frame,
    gang_list_frame,
    gang_position_update_frame,
    gang_properties_update_frame,
    member_detail_frame,
    member_list_frame,
    position_name,
)
from systems.gang.registry import (
    APPLICATION_LIST_COMMAND,
    DEFAULT_GANG_SEEDS,
    FIRST_GANG_ID,
    GANG_COMMAND,
    GANG_CREATION_COST_SILVER,
    GANG_LIST_COMMAND,
    GANG_POSITION_LEADER,
    GANG_POSITION_MEMBER,
    GANG_POSITION_NONE,
    GANG_POSITION_PROPERTY,
    MAX_GANG_MEMBERS,
    MAX_GANG_NAME_LENGTH,
    MAX_MOTTO_LENGTH,
    MAX_PENDING_APPLICATIONS,
    MEMBER_LIST_COMMAND,
    SILVER_CURRENCY_PROPERTY,
    SUB_ACCEPT_APPLICATION,
    SUB_ACCEPT_INVITE,
    SUB_ABDICATE,
    SUB_APPLY,
    SUB_GANG_INFO,
    SUB_INVITE,
    SUB_KICK,
    SUB_LEAVE,
    SUB_MODIFY_MOTTO,
    SUB_REJECT_APPLICATION,
    SUB_REJECT_INVITE,
)

LOG = logging.getLogger('piaomiao-local')

RoleLookup = Callable[[int], Optional[Dict[str, object]]]
OnlineCheck = Callable[[int], bool]
Notifier = Callable[[int, Tuple[bytes, ...]], None]


@dataclass
class GangMemberRecord:
    role_id: int
    name: str
    position: int
    contribution: int = 0
    joined_at: int = 0


@dataclass
class GangApplicationRecord:
    role_id: int
    applied_at: int = 0


@dataclass
class PendingInvite:
    gang_id: int
    inviter_id: int
    invited_at: int = 0


@dataclass
class GangState:
    gang_id: int
    name: str
    motto: str = ''
    funds: int = 10000
    activity: int = 0
    members: dict[int, GangMemberRecord] = field(default_factory=dict)
    applications: dict[int, GangApplicationRecord] = field(default_factory=dict)

    def leader(self) -> GangMemberRecord | None:
        for member in self.members.values():
            if member.position == GANG_POSITION_LEADER:
                return member
        return None


@dataclass(frozen=True)
class OperationResult:
    """Reply frames for the requester plus push frames for other roles."""

    replies: tuple[bytes, ...] = ()
    notifications: tuple[tuple[int, tuple[bytes, ...]], ...] = ()
    reason: str = ''


def _today_int() -> int:
    return int(time.strftime('%Y%m%d'))


class GangStore:
    """JSON-backed gang catalog."""

    def __init__(self, path: Path):
        self.path = path
        self.next_gang_id = FIRST_GANG_ID
        self.gangs: dict[int, GangState] = {}
        self.pending_invites: dict[int, PendingInvite] = {}
        self._load()

    def _load(self) -> None:
        if not self.path.exists():
            self._seed()
            self.save()
            return
        try:
            loaded = json.loads(self.path.read_text(encoding='utf-8'))
        except (OSError, ValueError) as exc:
            LOG.warning('failed to load gang data %s: %s', self.path, exc)
            self._seed()
            return
        if not isinstance(loaded, dict):
            self._seed()
            return
        self.next_gang_id = int(loaded.get('next_gang_id', FIRST_GANG_ID))
        for raw in loaded.get('gangs', []):
            if not isinstance(raw, dict):
                continue
            gang = GangState(
                gang_id=int(raw.get('gang_id', 0)),
                name=str(raw.get('name', '')),
                motto=str(raw.get('motto', '')),
                funds=int(raw.get('funds', 10000)),
                activity=int(raw.get('activity', 0)),
            )
            for raw_member in raw.get('members', []):
                member = GangMemberRecord(
                    role_id=int(raw_member.get('role_id', 0)),
                    name=str(raw_member.get('name', '')),
                    position=int(raw_member.get('position', GANG_POSITION_MEMBER)),
                    contribution=int(raw_member.get('contribution', 0)),
                    joined_at=int(raw_member.get('joined_at', 0)),
                )
                if member.role_id > 0:
                    gang.members[member.role_id] = member
            for raw_application in raw.get('applications', []):
                application = GangApplicationRecord(
                    role_id=int(raw_application.get('role_id', 0)),
                    applied_at=int(raw_application.get('applied_at', 0)),
                )
                if application.role_id > 0:
                    gang.applications[application.role_id] = application
            if gang.gang_id > 0:
                self.gangs[gang.gang_id] = gang
        for target_id, raw_invite in loaded.get('pending_invites', {}).items():
            invite = PendingInvite(
                gang_id=int(raw_invite.get('gang_id', 0)),
                inviter_id=int(raw_invite.get('inviter_id', 0)),
                invited_at=int(raw_invite.get('invited_at', 0)),
            )
            if invite.gang_id > 0:
                self.pending_invites[int(target_id)] = invite

    def _seed(self) -> None:
        gang_id = FIRST_GANG_ID
        for seed in DEFAULT_GANG_SEEDS:
            self.gangs[gang_id] = GangState(gang_id=gang_id, name=seed.name, motto=seed.motto)
            gang_id += 1
        self.next_gang_id = gang_id

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            'next_gang_id': self.next_gang_id,
            'gangs': [
                {
                    'gang_id': gang.gang_id,
                    'name': gang.name,
                    'motto': gang.motto,
                    'funds': gang.funds,
                    'activity': gang.activity,
                    'members': [
                        {
                            'role_id': member.role_id,
                            'name': member.name,
                            'position': member.position,
                            'contribution': member.contribution,
                            'joined_at': member.joined_at,
                        }
                        for member in gang.members.values()
                    ],
                    'applications': [
                        {'role_id': application.role_id, 'applied_at': application.applied_at}
                        for application in gang.applications.values()
                    ],
                }
                for gang in self.gangs.values()
            ],
            'pending_invites': {
                str(target_id): {
                    'gang_id': invite.gang_id,
                    'inviter_id': invite.inviter_id,
                    'invited_at': invite.invited_at,
                }
                for target_id, invite in self.pending_invites.items()
            },
        }
        temporary = self.path.with_suffix(self.path.suffix + '.tmp')
        temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
        temporary.replace(self.path)


class GangService:
    """Gang business rules over the catalog and role membership state."""

    def __init__(
        self,
        store: GangStore,
        save_roles: Callable[[], None],
        role_lookup: RoleLookup,
        online_check: OnlineCheck | None = None,
        notifier: Notifier | None = None,
    ) -> None:
        self.store = store
        self._save_roles = save_roles
        self._role_lookup = role_lookup
        self._online_check = online_check or (lambda role_id: False)
        self._notifier = notifier

    # ------------------------------------------------------------------
    # role membership helpers

    @staticmethod
    def role_gang_id(role: dict[str, object]) -> int:
        try:
            return int(role.get('gang_id', 0) or 0)
        except (TypeError, ValueError):
            return 0

    @staticmethod
    def role_position(role: dict[str, object]) -> int:
        try:
            return int(role.get('gang_position', 0) or 0)
        except (TypeError, ValueError):
            return 0

    @staticmethod
    def _clear_role_membership(role: dict[str, object]) -> None:
        role.pop('gang_id', None)
        role.pop('gang_position', None)
        role.pop('gang_contribution', None)
        role.pop('gang_joined_at', None)

    def _apply_role_membership(self, role: dict[str, object], gang: GangState, position: int) -> None:
        role['gang_id'] = gang.gang_id
        role['gang_position'] = position
        role['gang_joined_at'] = _today_int()
        role.setdefault('gang_contribution', 0)

    def _member_name(self, member: GangMemberRecord) -> str:
        role = self._role_lookup(member.role_id)
        if role is not None and str(role.get('name', '') or ''):
            return str(role['name'])
        return member.name

    def _member_level(self, member: GangMemberRecord) -> int:
        role = self._role_lookup(member.role_id)
        if role is None:
            return 1
        try:
            return max(1, int(role.get('level', 1) or 1))
        except (TypeError, ValueError):
            return 1

    def _strength(self, gang: GangState) -> int:
        return sum(self._member_level(member) for member in gang.members.values())

    def _sorted_members(self, gang: GangState) -> list[GangMemberRecord]:
        return sorted(
            gang.members.values(),
            key=lambda member: (-member.position, member.joined_at, member.role_id),
        )

    def _role_name(self, role: dict[str, object]) -> str:
        return str(role.get('name', '') or '')

    # ------------------------------------------------------------------
    # dispatch

    def handle_message(
        self,
        message_id: int,
        fields: list[object],
        role: dict[str, object],
    ) -> OperationResult:
        if message_id == GANG_COMMAND:
            return self._handle_command(fields, role)
        if message_id == GANG_LIST_COMMAND:
            return self._handle_gang_list()
        if message_id == MEMBER_LIST_COMMAND:
            return self._handle_member_list(fields, role)
        if message_id == APPLICATION_LIST_COMMAND:
            return self._handle_application_list(fields, role)
        return OperationResult(reason='unknown_message')

    def _handle_command(self, fields: list[object], role: dict[str, object]) -> OperationResult:
        subcommand = GangProtocol.gang_subcommand(fields)
        if subcommand is None:
            return OperationResult(reason='malformed_command')
        if subcommand == SUB_GANG_INFO:
            return self._handle_gang_info(fields, role)
        if subcommand == SUB_LEAVE:
            return self.leave_gang(role)
        if subcommand == SUB_KICK:
            return self.kick_member(role, GangProtocol.gang_kick_member_id(fields))
        if subcommand == SUB_ABDICATE:
            return self.abdicate(role, GangProtocol.gang_int_param(fields))
        if subcommand == SUB_APPLY:
            return self.apply_to_gang(role, GangProtocol.gang_int_param(fields))
        if subcommand == SUB_ACCEPT_APPLICATION:
            return self.accept_application(role, GangProtocol.gang_int_param(fields))
        if subcommand == SUB_REJECT_APPLICATION:
            return self.reject_application(role, GangProtocol.gang_int_param(fields))
        if subcommand == SUB_INVITE:
            return self.invite_player(role, GangProtocol.gang_int_param(fields))
        if subcommand == SUB_ACCEPT_INVITE:
            return self.accept_invite(role, GangProtocol.gang_int_param(fields))
        if subcommand == SUB_REJECT_INVITE:
            return self.reject_invite(role, GangProtocol.gang_int_param(fields))
        if subcommand == SUB_MODIFY_MOTTO:
            return self.modify_motto(role, GangProtocol.gang_motto_param(fields))
        return OperationResult(reason='unknown_subcommand')

    # ------------------------------------------------------------------
    # read-only views

    def _handle_gang_info(self, fields: list[object], role: dict[str, object]) -> OperationResult:
        gang_id = GangProtocol.gang_int_param(fields)
        target_id = gang_id if gang_id else self.role_gang_id(role)
        gang = self.store.gangs.get(target_id) if target_id else None
        if gang is None:
            return OperationResult(reason='unknown_gang')
        return OperationResult(replies=(self.gang_info_reply(gang),))

    def gang_info_reply(self, gang: GangState) -> bytes:
        leader = gang.leader()
        return gang_info_frame(
            gang.gang_id,
            gang.name,
            leader.role_id if leader else 0,
            self._member_name(leader) if leader else '',
            len(gang.members),
            gang.funds,
            gang.activity,
            gang.motto,
            self._strength(gang),
        )

    def _handle_gang_list(self) -> OperationResult:
        entries = [
            GangListEntry(
                gang_id=gang.gang_id,
                name=gang.name,
                leader_name=self._member_name(leader) if (leader := gang.leader()) else '',
                member_count=len(gang.members),
            )
            for gang in sorted(self.store.gangs.values(), key=lambda item: item.gang_id)
        ]
        return OperationResult(replies=(gang_list_frame(entries),))

    def _handle_member_list(self, fields: list[object], role: dict[str, object]) -> OperationResult:
        if GangProtocol.is_detail_request(fields):
            return self._handle_member_detail(fields, role)
        gang = self.store.gangs.get(self.role_gang_id(role))
        if gang is None:
            return OperationResult(reason='no_gang')
        members = [
            GangMemberEntry(
                role_id=member.role_id,
                name=self._member_name(member),
                position=member.position,
                level=self._member_level(member),
                online=self._online_check(member.role_id),
            )
            for member in self._sorted_members(gang)
        ]
        return OperationResult(replies=(member_list_frame(members),))

    def _handle_member_detail(self, fields: list[object], role: dict[str, object]) -> OperationResult:
        gang = self.store.gangs.get(self.role_gang_id(role))
        if gang is None:
            return OperationResult(reason='no_gang')
        member_id = GangProtocol.detail_role_id(fields)
        member = gang.members.get(member_id) if member_id else None
        if member is None:
            return OperationResult(reason='unknown_member')
        target = self._role_lookup(member.role_id)
        detail = GangMemberDetail(
            name=self._member_name(member),
            sex=int(target.get('sex', 0) or 0) if target else 0,
            level=self._member_level(member),
            race=int(target.get('race', 0) or 0) if target else 0,
            sect_id=int(target.get('sect_id', 0) or 0) if target else 0,
            joined_at=member.joined_at,
            position=member.position,
            contribution=member.contribution,
            online=self._online_check(member.role_id),
        )
        return OperationResult(replies=(member_detail_frame(detail),))

    def _handle_application_list(self, fields: list[object], role: dict[str, object]) -> OperationResult:
        gang = self.store.gangs.get(self.role_gang_id(role))
        if gang is None:
            return OperationResult(reason='no_gang')
        if not GangProtocol.is_list_request(fields):
            return OperationResult(reason='malformed_command')
        if self.role_position(role) != GANG_POSITION_LEADER:
            return OperationResult(replies=(application_list_frame([]),), reason='not_leader')
        applications = [
            GangApplicationEntry(
                role_id=application.role_id,
                name=self._application_name(application),
                race=self._application_race(application),
                level=self._application_level(application),
                online=self._online_check(application.role_id),
            )
            for application in sorted(gang.applications.values(), key=lambda item: (item.applied_at, item.role_id))
        ]
        return OperationResult(replies=(application_list_frame(applications),))

    def _application_role(self, application: GangApplicationRecord) -> dict[str, object] | None:
        return self._role_lookup(application.role_id)

    def _application_name(self, application: GangApplicationRecord) -> str:
        role = self._application_role(application)
        if role is not None and str(role.get('name', '') or ''):
            return str(role['name'])
        return f'侠客{application.role_id}'

    def _application_race(self, application: GangApplicationRecord) -> int:
        role = self._application_role(application)
        return int(role.get('race', 0) or 0) if role else 0

    def _application_level(self, application: GangApplicationRecord) -> int:
        role = self._application_role(application)
        if role is None:
            return 1
        try:
            return max(1, int(role.get('level', 1) or 1))
        except (TypeError, ValueError):
            return 1

    # ------------------------------------------------------------------
    # mutations

    def leave_gang(self, role: dict[str, object]) -> OperationResult:
        gang = self.store.gangs.get(self.role_gang_id(role))
        if gang is None:
            return OperationResult(reason='no_gang')
        role_id = int(role.get('id', 0))
        gang.members.pop(role_id, None)
        self._clear_role_membership(role)
        self._persist()
        return OperationResult(
            replies=(gang_position_update_frame(role_id, GANG_POSITION_NONE), gang_close_frame(SUB_LEAVE)),
            reason='left',
        )

    def kick_member(self, role: dict[str, object], member_id: int | None) -> OperationResult:
        gang = self.store.gangs.get(self.role_gang_id(role))
        if gang is None:
            return OperationResult(reason='no_gang')
        if self.role_position(role) != GANG_POSITION_LEADER:
            return OperationResult(reason='not_leader')
        if not member_id or member_id == int(role.get('id', 0)):
            return OperationResult(reason='invalid_member')
        member = gang.members.get(member_id)
        if member is None:
            return OperationResult(reason='unknown_member')
        gang.members.pop(member_id, None)
        target = self._role_lookup(member_id)
        if target is not None:
            self._clear_role_membership(target)
        notifications: list[tuple[int, tuple[bytes, ...]]] = []
        if member_id and self._online_check(member_id):
            notifications.append((
                member_id,
                (gang_position_update_frame(member_id, GANG_POSITION_NONE), gang_close_frame(SUB_KICK)),
            ))
        self._persist()
        return OperationResult(
            replies=(self.gang_info_reply(gang),),
            notifications=tuple(notifications),
            reason='kicked',
        )

    def abdicate(self, role: dict[str, object], member_id: int | None) -> OperationResult:
        gang = self.store.gangs.get(self.role_gang_id(role))
        if gang is None:
            return OperationResult(reason='no_gang')
        if self.role_position(role) != GANG_POSITION_LEADER:
            return OperationResult(reason='not_leader')
        if not member_id or member_id == int(role.get('id', 0)):
            return OperationResult(reason='invalid_member')
        successor = gang.members.get(member_id)
        if successor is None:
            return OperationResult(reason='unknown_member')
        leader = gang.leader()
        successor.position = GANG_POSITION_LEADER
        if leader is not None and leader.role_id != successor.role_id:
            leader.position = GANG_POSITION_MEMBER
        if leader is not None:
            leader_role = self._role_lookup(leader.role_id)
            if leader_role is not None:
                self._apply_role_membership(leader_role, gang, GANG_POSITION_MEMBER)
        successor_role = self._role_lookup(successor.role_id)
        if successor_role is not None:
            self._apply_role_membership(successor_role, gang, GANG_POSITION_LEADER)
        notifications: list[tuple[int, tuple[bytes, ...]]] = []
        if self._online_check(successor.role_id):
            notifications.append((successor.role_id, (gang_position_update_frame(successor.role_id, GANG_POSITION_LEADER),)))
        self._persist()
        return OperationResult(
            replies=(
                gang_position_update_frame(int(role.get('id', 0)), GANG_POSITION_MEMBER),
                self.gang_info_reply(gang),
            ),
            notifications=tuple(notifications),
            reason='abdicated',
        )

    def create_gang(self, role: dict[str, object], name: str | None = None) -> OperationResult:
        """帮派管理员 NPC 的创建入口：扣银两、开新帮、任职帮主。

        APK 没有"创建帮派"的客户端协议（0x453 子命令表中不存在），命名走
        服务端确定性规则：显式传入优先，否则用 ``{玩家名}帮``。
        """
        if self.role_gang_id(role):
            return OperationResult(reason='already_in_gang')
        role_id = int(role.get('id', 0))
        cleaned = (name or '').strip() or f'{self._role_name(role)}帮'
        if not cleaned or len(cleaned) > MAX_GANG_NAME_LENGTH:
            return OperationResult(reason='invalid_name')
        if any(gang.name == cleaned for gang in self.store.gangs.values()):
            return OperationResult(reason='name_taken')
        currencies = role.get('currencies')
        if not isinstance(currencies, dict):
            return OperationResult(reason='missing_currency_state')
        try:
            balance = int(currencies.get('silver', 0) or 0)
        except (TypeError, ValueError):
            balance = 0
        if balance < GANG_CREATION_COST_SILVER:
            return OperationResult(reason='insufficient_silver')
        currencies['silver'] = balance - GANG_CREATION_COST_SILVER
        gang = GangState(
            gang_id=self.store.next_gang_id,
            name=cleaned,
            motto='',
            funds=GANG_CREATION_COST_SILVER,
        )
        self.store.next_gang_id += 1
        self.store.gangs[gang.gang_id] = gang
        self._apply_role_membership(role, gang, GANG_POSITION_LEADER)
        gang.members[role_id] = GangMemberRecord(
            role_id=role_id,
            name=self._role_name(role) or f'侠客{role_id}',
            position=GANG_POSITION_LEADER,
            contribution=0,
            joined_at=_today_int(),
        )
        self._persist()
        return OperationResult(
            replies=(gang_properties_update_frame(role_id, {
                GANG_POSITION_PROPERTY: GANG_POSITION_LEADER,
                SILVER_CURRENCY_PROPERTY: balance - GANG_CREATION_COST_SILVER,
            }),),
            reason='gang_created',
        )

    def apply_to_gang(self, role: dict[str, object], gang_id: int | None) -> OperationResult:
        if self.role_gang_id(role):
            return OperationResult(reason='already_in_gang')
        gang = self.store.gangs.get(gang_id) if gang_id else None
        if gang is None:
            return OperationResult(reason='unknown_gang')
        role_id = int(role.get('id', 0))
        gang.applications.pop(role_id, None)
        # Bootstrap: a leaderless seed gang admits the first applicant as 帮主
        # so the audited leader flows stay reachable without a create protocol.
        if gang.leader() is None:
            return self._join(role, gang, GANG_POSITION_LEADER, 'joined_as_leader', actor_role_id=int(role.get('id', 0)))
        if len(gang.members) >= MAX_GANG_MEMBERS:
            return OperationResult(reason='gang_full')
        if len(gang.applications) >= MAX_PENDING_APPLICATIONS:
            return OperationResult(reason='applications_full')
        gang.applications[role_id] = GangApplicationRecord(role_id=role_id, applied_at=_today_int())
        self._persist()
        return OperationResult(reason='applied')

    def accept_application(self, role: dict[str, object], applicant_id: int | None) -> OperationResult:
        gang = self.store.gangs.get(self.role_gang_id(role))
        if gang is None:
            return OperationResult(reason='no_gang')
        if self.role_position(role) != GANG_POSITION_LEADER:
            return OperationResult(reason='not_leader')
        application = gang.applications.get(applicant_id) if applicant_id else None
        if application is None:
            return OperationResult(reason='unknown_application')
        applicant = self._role_lookup(applicant_id)
        if applicant is None:
            gang.applications.pop(applicant_id, None)
            self._persist()
            return OperationResult(reason='unknown_role')
        if self.role_gang_id(applicant):
            gang.applications.pop(applicant_id, None)
            self._persist()
            return OperationResult(reason='already_in_gang')
        if len(gang.members) >= MAX_GANG_MEMBERS:
            return OperationResult(reason='gang_full')
        gang.applications.pop(applicant_id, None)
        result = self._join(
            applicant,
            gang,
            GANG_POSITION_MEMBER,
            'application_accepted',
            actor_role_id=int(role.get('id', 0)),
        )
        self.store.pending_invites.pop(applicant_id, None)
        return result

    def reject_application(self, role: dict[str, object], applicant_id: int | None) -> OperationResult:
        gang = self.store.gangs.get(self.role_gang_id(role))
        if gang is None:
            return OperationResult(reason='no_gang')
        if self.role_position(role) != GANG_POSITION_LEADER:
            return OperationResult(reason='not_leader')
        if not applicant_id or applicant_id not in gang.applications:
            return OperationResult(reason='unknown_application')
        gang.applications.pop(applicant_id, None)
        self._persist()
        return OperationResult(replies=(application_list_frame(self._application_entries(gang)),), reason='rejected')

    def _application_entries(self, gang: GangState) -> list[GangApplicationEntry]:
        return [
            GangApplicationEntry(
                role_id=application.role_id,
                name=self._application_name(application),
                race=self._application_race(application),
                level=self._application_level(application),
                online=self._online_check(application.role_id),
            )
            for application in sorted(gang.applications.values(), key=lambda item: (item.applied_at, item.role_id))
        ]

    def invite_player(self, role: dict[str, object], target_id: int | None) -> OperationResult:
        gang = self.store.gangs.get(self.role_gang_id(role))
        if gang is None:
            return OperationResult(reason='no_gang')
        if self.role_position(role) != GANG_POSITION_LEADER:
            return OperationResult(reason='not_leader')
        if not target_id or target_id == int(role.get('id', 0)):
            return OperationResult(reason='invalid_target')
        target = self._role_lookup(target_id)
        if target is None:
            return OperationResult(reason='unknown_role')
        if self.role_gang_id(target):
            return OperationResult(reason='already_in_gang')
        if len(gang.members) >= MAX_GANG_MEMBERS:
            return OperationResult(reason='gang_full')
        if not self._online_check(target_id):
            return OperationResult(reason='target_offline')
        self.store.pending_invites[target_id] = PendingInvite(
            gang_id=gang.gang_id,
            inviter_id=int(role.get('id', 0)),
            invited_at=_today_int(),
        )
        self._persist()
        inviter_id = int(role.get('id', 0))
        notification = ((target_id, (gang_invite_frame(inviter_id, self._role_name(role), gang.name),)),)
        return OperationResult(notifications=notification, reason='invited')

    def accept_invite(self, role: dict[str, object], inviter_id: int | None) -> OperationResult:
        if self.role_gang_id(role):
            return OperationResult(reason='already_in_gang')
        role_id = int(role.get('id', 0))
        invite = self.store.pending_invites.get(role_id)
        if invite is None:
            return OperationResult(reason='no_pending_invite')
        if inviter_id and invite.inviter_id and inviter_id != invite.inviter_id:
            return OperationResult(reason='invite_mismatch')
        gang = self.store.gangs.get(invite.gang_id)
        self.store.pending_invites.pop(role_id, None)
        if gang is None:
            return OperationResult(reason='unknown_gang')
        if len(gang.members) >= MAX_GANG_MEMBERS:
            return OperationResult(reason='gang_full')
        gang.applications.pop(role_id, None)
        return self._join(
            role,
            gang,
            GANG_POSITION_MEMBER,
            'invite_accepted',
            actor_role_id=role_id,
        )

    def reject_invite(self, role: dict[str, object], inviter_id: int | None) -> OperationResult:
        role_id = int(role.get('id', 0))
        invite = self.store.pending_invites.get(role_id)
        if invite is None:
            return OperationResult(reason='no_pending_invite')
        if inviter_id and invite.inviter_id and inviter_id != invite.inviter_id:
            return OperationResult(reason='invite_mismatch')
        self.store.pending_invites.pop(role_id, None)
        self._persist()
        return OperationResult(reason='invite_rejected')

    def modify_motto(self, role: dict[str, object], motto: str | None) -> OperationResult:
        gang = self.store.gangs.get(self.role_gang_id(role))
        if gang is None:
            return OperationResult(reason='no_gang')
        if self.role_position(role) != GANG_POSITION_LEADER:
            return OperationResult(reason='not_leader')
        if motto is None:
            return OperationResult(reason='malformed_command')
        text = motto.strip()
        if not text or len(text) > MAX_MOTTO_LENGTH:
            return OperationResult(reason='invalid_motto')
        gang.motto = text
        self._persist()
        return OperationResult(replies=(self.gang_info_reply(gang),), reason='motto_changed')

    def disband_gang(self, role: dict[str, object]) -> OperationResult:
        """帮主通过帮派管理员 NPC 解散帮派：移除目录、清理全员、推送重置。"""
        gang = self.store.gangs.get(self.role_gang_id(role))
        if gang is None:
            return OperationResult(reason='no_gang')
        if self.role_position(role) != GANG_POSITION_LEADER:
            return OperationResult(reason='not_leader')
        role_id = int(role.get('id', 0))
        notifications: list[tuple[int, tuple[bytes, ...]]] = []
        for member in gang.members.values():
            member_role = self._role_lookup(member.role_id)
            if member_role is not None:
                self._clear_role_membership(member_role)
            if member.role_id != role_id and self._online_check(member.role_id):
                notifications.append((
                    member.role_id,
                    (
                        gang_position_update_frame(member.role_id, GANG_POSITION_NONE),
                        gang_close_frame(SUB_LEAVE),
                    ),
                ))
        self.store.gangs.pop(gang.gang_id, None)
        self.store.pending_invites = {
            target_id: invite
            for target_id, invite in self.store.pending_invites.items()
            if invite.gang_id != gang.gang_id
        }
        self._clear_role_membership(role)
        self._persist()
        return OperationResult(
            replies=(gang_position_update_frame(role_id, GANG_POSITION_NONE),),
            notifications=tuple(notifications),
            reason='disbanded',
        )

    # ------------------------------------------------------------------

    def _join(
        self,
        role: dict[str, object],
        gang: GangState,
        position: int,
        reason: str,
        actor_role_id: int | None = None,
    ) -> OperationResult:
        role_id = int(role.get('id', 0))
        name = self._role_name(role) or f'侠客{role_id}'
        gang.members[role_id] = GangMemberRecord(
            role_id=role_id,
            name=name,
            position=position,
            contribution=0,
            joined_at=_today_int(),
        )
        self._apply_role_membership(role, gang, position)
        self._persist()
        position_push = gang_position_update_frame(role_id, position)
        if actor_role_id is not None and role_id == actor_role_id:
            # The joiner's own connection consumes the reply frames directly.
            replies: tuple[bytes, ...] = (position_push,)
            if position == GANG_POSITION_LEADER:
                replies += (self.gang_info_reply(gang),)
            return OperationResult(replies=replies, reason=reason)
        notifications: list[tuple[int, tuple[bytes, ...]]] = []
        if self._online_check(role_id):
            notifications.append((role_id, (position_push,)))
        return OperationResult(notifications=tuple(notifications), reason=reason)

    def _persist(self) -> None:
        self.store.save()
        self._save_roles()

    # ------------------------------------------------------------------
    # helpers shared with the handler layer

    @staticmethod
    def position_label(position: int) -> str:
        return position_name(position)


def default_gang_service(
    store_path: Path,
    save_roles: Callable[[], None],
    role_lookup: RoleLookup,
    online_check: OnlineCheck | None = None,
    notifier: Notifier | None = None,
) -> GangService:
    return GangService(
        GangStore(store_path),
        save_roles,
        role_lookup,
        online_check=online_check,
        notifier=notifier,
    )
