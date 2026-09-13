"""Cross-system event names published by the gang system."""

from __future__ import annotations

GANG_MEMBER_JOINED = 'gang.member_joined'
GANG_MEMBER_LEFT = 'gang.member_left'
GANG_MEMBER_KICKED = 'gang.member_kicked'
GANG_LEADER_CHANGED = 'gang.leader_changed'
GANG_MOTTO_CHANGED = 'gang.motto_changed'
GANG_APPLICATION_SUBMITTED = 'gang.application_submitted'


def gang_event_payload(gang_id: int, gang_name: str, role_id: int, **extra: object) -> dict[str, object]:
    return {
        'gang_id': int(gang_id),
        'gang_name': str(gang_name),
        'role_id': int(role_id),
        **extra,
    }
