"""APK-specific task protocol adapter for messages 1403 and 1145."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

from protocol import (
    Field,
    TYPE_BYTE,
    TYPE_INT,
    byte,
    encode_frame,
    integer,
    short,
    string,
)
from task_registry import TaskDefinition


TASK_MESSAGE_ID = 1403
TASK_ROUTE_MESSAGE_ID = 1145
ACTIVE_RECORD_WIDTH = 9
AVAILABLE_RECORD_WIDTH = 7
ACTIVE_STYLE_DEFAULT = 3
ACTIVE_STATE_ACTIVE = 1
ACTIVE_STATE_READY = 2


@dataclass(frozen=True)
class TaskOperationRequest:
    first_id: int
    second_id: int
    operation: int
    category: int


@dataclass(frozen=True)
class Task1145Request:
    variant: str
    route_id: int
    operation: int
    category: int
    task_id: int
    route_kind: int = 0


def _exact_types(fields: Sequence[Field], expected: tuple[int, ...]) -> bool:
    return len(fields) == len(expected) and tuple(field.type_id for field in fields) == expected


def is_active_list_request(fields: Sequence[Field]) -> bool:
    return bool(
        _exact_types(fields, (TYPE_BYTE, TYPE_BYTE, TYPE_BYTE, TYPE_BYTE))
        and int(fields[0].value) == 6
    )


def is_available_list_request(fields: Sequence[Field]) -> bool:
    return bool(
        _exact_types(fields, (TYPE_BYTE, TYPE_BYTE, TYPE_BYTE))
        and int(fields[0].value) == 50
    )


def detail_request_task_id(fields: Sequence[Field]) -> int | None:
    if not _exact_types(fields, (TYPE_BYTE, TYPE_INT)):
        return None
    if int(fields[0].value) not in {15, 22, 52}:
        return None
    return int(fields[1].value)


def parse_task_operation_request(fields: Sequence[Field]) -> TaskOperationRequest | None:
    if not _exact_types(fields, (TYPE_BYTE, TYPE_INT, TYPE_INT, TYPE_BYTE, TYPE_BYTE)):
        return None
    if int(fields[0].value) != 7:
        return None
    return TaskOperationRequest(
        first_id=int(fields[1].value),
        second_id=int(fields[2].value),
        operation=int(fields[3].value),
        category=int(fields[4].value),
    )


def parse_task_1145_request(fields: Sequence[Field]) -> Task1145Request | None:
    """Parse the historical compatibility 1145 task forms.

    The live APK also uses 1145/action-0 for cross-map pathfinding.  Runtime
    routing therefore validates the decoded route against the task catalog and
    falls through when it is not an exact task route.
    """
    if _exact_types(fields, (TYPE_BYTE, TYPE_INT, TYPE_BYTE, TYPE_BYTE)):
        if int(fields[0].value) != 0:
            return None
        return Task1145Request(
            variant='available',
            route_id=int(fields[1].value),
            operation=0,
            category=int(fields[2].value),
            task_id=0,
            route_kind=int(fields[3].value),
        )
    if _exact_types(fields, (TYPE_BYTE, TYPE_INT, TYPE_BYTE, TYPE_BYTE, TYPE_INT)):
        if int(fields[0].value) != 0:
            return None
        return Task1145Request(
            variant='active',
            route_id=int(fields[1].value),
            operation=int(fields[2].value),
            category=int(fields[3].value),
            task_id=int(fields[4].value),
            route_kind=0,
        )
    return None


def available_task_list_frame(
    entries: Iterable[tuple[TaskDefinition, int]],
) -> bytes:
    """Encode action 50 using the APK's seven-field task row.

    ``e/en`` and the available-task pane in ``e/ca`` read each row as
    ``task_id, name, status, map_id, x, y, actor_id``.  Status 1 exposes
    “领取任务”; status 3 exposes “提交任务”.
    """
    records = tuple(entries)
    fields: list[Field] = [byte(50), short(0), byte(len(records))]
    for task, status in records:
        route = task.client_route
        fields.extend((
            integer(task.task_id),
            string(task.name),
            integer(int(status)),
            integer(route.accept_map_id),
            integer(route.accept_x),
            integer(route.accept_y),
            integer(route.accept_actor_id),
        ))
    return encode_frame(TASK_MESSAGE_ID, fields)


def active_task_list_frame(
    category_wire_id: int,
    entries: Iterable[tuple[TaskDefinition, str]],
) -> bytes:
    """Encode action 6 using the APK's nine-field active-task row."""
    records = tuple(entries)
    fields: list[Field] = [
        byte(6),
        short(0),
        byte(len(records)),
        byte(int(category_wire_id)),
    ]
    for task, status in records:
        route = task.client_route
        fields.extend((
            integer(task.task_id),
            string(task.name),
            integer(task.level_requirement),
            integer(ACTIVE_STYLE_DEFAULT),
            integer(ACTIVE_STATE_READY if status == 'ready' else ACTIVE_STATE_ACTIVE),
            integer(route.submit_map_id),
            integer(route.submit_x),
            integer(route.submit_y),
            integer(route.submit_actor_id),
        ))
    return encode_frame(TASK_MESSAGE_ID, fields)


def safe_detail_ack_frame() -> bytes:
    """Release the client's waiting state without opening the untraced detail UI."""
    return encode_frame(TASK_MESSAGE_ID, [byte(1)])
