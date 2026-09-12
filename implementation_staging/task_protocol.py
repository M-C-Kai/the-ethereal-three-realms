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
AVAILABLE_RECORD_WIDTH = 6


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
    """Parse only the two APK-confirmed task-shaped 1145/action-0 forms.

    Other 1145 payloads (notably map pathfinding) deliberately return None so
    existing server routing can continue unchanged.
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


def available_task_list_frame(tasks: Iterable[TaskDefinition]) -> bytes:
    entries = tuple(tasks)
    # main/e.ad action 50/52 reads field1 as a short page/selection token and
    # field2 as the record count. It infers each record width from the total
    # remaining field count, so never transmit AVAILABLE_RECORD_WIDTH here.
    fields: list[Field] = [byte(50), short(0), byte(len(entries))]
    for task in entries:
        fields.extend((
            integer(task.task_id),
            string(task.name),
            integer(0),
            integer(task.client_route.route_id),
            byte(task.category_wire_id),
            byte(task.client_route.route_kind),
        ))
    return encode_frame(TASK_MESSAGE_ID, fields)


def active_task_list_frame(
    category_wire_id: int,
    entries: Iterable[tuple[TaskDefinition, str]],
) -> bytes:
    records = tuple(entries)
    # main/e.ad action 6 reads field1 as a short page/selection token, field2
    # as record count and field3 as category. The 9-field width is inferred.
    fields: list[Field] = [
        byte(6),
        short(0),
        byte(len(records)),
        byte(int(category_wire_id)),
    ]
    for task, status in records:
        ready = status == 'ready'
        fields.extend((
            integer(task.task_id),
            string(task.name),
            integer(0),
            integer(task.level_requirement),
            integer(4 if ready else 0),
            integer(task.client_route.route_id),
            byte(2 if ready else 4),
            byte(task.category_wire_id),
            integer(task.task_id),
        ))
    return encode_frame(TASK_MESSAGE_ID, fields)


def safe_detail_ack_frame() -> bytes:
    """Release the client's waiting state without opening the untraced detail UI."""
    return encode_frame(TASK_MESSAGE_ID, [byte(1)])
