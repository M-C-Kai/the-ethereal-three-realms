"""装备孔位领域模型。

客户端线协议仍只接收 1008 fields[34..38] -> g.x[0..4]，
服务端额外持久化 socket_types[0..4] 保存原始孔型，供镶嵌/拆除/洗孔使用。
"""
from __future__ import annotations

from typing import Mapping, MutableMapping

SOCKET_COUNT = 5
SOCKET_STATE_VERSION = 1

SOCKET_NONE = 0
SOCKET_CYAN = 1
SOCKET_GOLD = 2
SOCKET_RED = 3
SOCKET_YELLOW = 4
SOCKET_BLUE = 5
SOCKET_DARK = 6
SOCKET_PURPLE = 7

VALID_SOCKET_TYPES = frozenset(range(1, 8))
COMMON_SOCKET_TYPES = frozenset(range(1, 7))

# APK g.e(j)/g.b(int) 已锁定的 9 个镶嵌物族。
# 名称中的两组仍有中文名二选一问题，但“族 -> 客户端孔类别”已经锁定。
_GEM_FAMILY_SOCKET_TYPES: tuple[tuple[int, int, int], ...] = (
    (322_000_000, 322_000_011, SOCKET_CYAN),  # 佛骨舍利
    (322_000_100, 322_000_111, SOCKET_CYAN),  # 木曜/土曜
    (322_000_200, 322_000_211, SOCKET_CYAN),  # 土曜/木曜
    (322_001_000, 322_001_011, SOCKET_GOLD),  # 金曜（APK g.b 分支遗漏）
    (322_002_000, 322_002_011, SOCKET_RED),   # 火曜
    (322_003_000, 322_003_011, SOCKET_YELLOW),# 炎曜
    (322_004_000, 322_004_011, SOCKET_BLUE),  # 水曜
    (322_005_000, 322_005_011, SOCKET_DARK),  # 玄曜/魔曜
    (322_006_000, 322_006_011, SOCKET_PURPLE),# 魔曜/玄曜
)


def _normalized_five(raw: object) -> list[int]:
    source = raw if isinstance(raw, (list, tuple)) else ()
    result: list[int] = []
    for index in range(SOCKET_COUNT):
        value = source[index] if index < len(source) else 0
        try:
            result.append(max(0, int(value)))
        except (TypeError, ValueError):
            result.append(0)
    return result


def native_socket_slots(item: Mapping[str, object]) -> list[int]:
    """返回客户端权威当前状态 g.x[0..4]。"""
    return _normalized_five(item.get('extra_attributes'))


def socket_types(item: Mapping[str, object]) -> list[int]:
    """返回服务端持久化的原始孔型；旧实例缺失时返回全 0。"""
    raw = _normalized_five(item.get('socket_types'))
    return [value if value in VALID_SOCKET_TYPES else 0 for value in raw]


def gem_socket_type(template_id: int) -> int | None:
    """由已锁定的宝石模板族恢复其唯一兼容孔类别。"""
    for lower, upper, socket_type in _GEM_FAMILY_SOCKET_TYPES:
        if lower <= template_id <= upper:
            return socket_type
    return None


def is_socket_gem_template(template_id: int) -> bool:
    return gem_socket_type(template_id) is not None


def opened_socket_count(item: Mapping[str, object]) -> int:
    """优先按持久化孔型计数；旧实例回退到客户端当前状态。"""
    types = socket_types(item)
    if any(types):
        return sum(1 for value in types if value != 0)
    return sum(1 for value in native_socket_slots(item) if value != 0)


def first_unopened_socket(item: Mapping[str, object]) -> int | None:
    types = socket_types(item)
    for index, value in enumerate(types):
        if value == SOCKET_NONE:
            return index
    return None


def first_empty_open_socket(item: Mapping[str, object]) -> int | None:
    types = socket_types(item)
    current = native_socket_slots(item)
    for index, socket_type in enumerate(types):
        if socket_type != SOCKET_NONE and current[index] == socket_type:
            return index
    return None


def socket_is_open(item: Mapping[str, object], index: int) -> bool:
    return 0 <= index < SOCKET_COUNT and socket_types(item)[index] != SOCKET_NONE


def socket_has_gem(item: Mapping[str, object], index: int) -> bool:
    if not socket_is_open(item, index):
        return False
    value = native_socket_slots(item)[index]
    return is_socket_gem_template(value)


def socket_gem_template(item: Mapping[str, object], index: int) -> int | None:
    if not socket_has_gem(item, index):
        return None
    return native_socket_slots(item)[index]


def restore_empty_socket(item: MutableMapping[str, object], index: int) -> None:
    if not 0 <= index < SOCKET_COUNT:
        raise IndexError('socket index must be 0..4')
    types = socket_types(item)
    if types[index] == SOCKET_NONE:
        raise ValueError('socket is not opened')
    current = native_socket_slots(item)
    current[index] = types[index]
    item['extra_attributes'] = current


def ensure_socket_state(
    item: MutableMapping[str, object],
    *,
    socketable: bool,
    legacy_socket_count: int = 0,
) -> bool:
    """一次性把旧装备迁移到 socket_types + extra_attributes 双层模型。

    Phase 1 只建立持久化结构，不主动改变已验证的运行时开孔流程。
    旧错误空孔码 8..10 归一为 1；1..7 真实孔型保留。
    已镶嵌的已知宝石可由模板族恢复其原始孔色。
    """
    before_types = item.get('socket_types')
    before_extra = item.get('extra_attributes')

    if not socketable:
        target_types = [0] * SOCKET_COUNT
        # 不可开孔装备（当前主要是戒指/扩展槽）不保留历史伪孔位。
        target_extra = [0] * SOCKET_COUNT
    else:
        current = native_socket_slots(item)
        has_current_state = isinstance(before_extra, (list, tuple)) and len(before_extra) == SOCKET_COUNT

        if has_current_state:
            target_extra = list(current)
            target_types: list[int] = []
            for index, value in enumerate(current):
                if value == 0:
                    target_types.append(0)
                elif value in VALID_SOCKET_TYPES:
                    target_types.append(value)
                elif 8 <= value <= 10:
                    # 早期兼容版本错误把装备槽号写进空孔；资源帧 8..10 为空。
                    target_types.append(SOCKET_CYAN)
                    target_extra[index] = SOCKET_CYAN
                else:
                    gem_type = gem_socket_type(value)
                    # 已知镶嵌宝石可以恢复唯一孔类别；未知历史值保守视为青孔，
                    # 但保留 extra_attributes 原值，避免破坏客户端当前数据。
                    target_types.append(gem_type or SOCKET_CYAN)
        else:
            count = max(0, min(SOCKET_COUNT, int(legacy_socket_count or 0)))
            target_types = [SOCKET_CYAN if i < count else 0 for i in range(SOCKET_COUNT)]
            target_extra = list(target_types)

    changed = (
        before_types != target_types
        or before_extra != target_extra
    )
    if changed:
        item['socket_types'] = target_types
        item['extra_attributes'] = target_extra
    return changed
