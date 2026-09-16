"""战斗系统业务：连接级战斗状态、逃跑保护与奖励结算。"""
from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field

from systems.fuyuan import service as fuyuan
from protocol import (
    Field, TYPE_BYTE, TYPE_INT, TYPE_SHORT,
    binary, byte, encode_frame, integer, long_integer, short, string,
)
from systems.inventory.registry import ItemRegistry, default_item_registry
from systems.inventory.service import bag_capacity, bag_item_count, role_items
from systems.role.service import CombatStats, MAX_ROLE_LEVEL, apply_one_level

LOG = logging.getLogger('piaomiao-local')


def ordered_combatants(ids, initiative, preferred_id):
    """User-confirmed rule; missing authoritative values remain unknown/zero.

    Stable input order resolves monster-only ties, a local compatibility rule.
    No APK Property or character level is guessed as an initiative source.
    """
    return sorted(ids, key=lambda actor: (
        -initiative.get(actor, (0, 0))[0],
        -initiative.get(actor, (0, 0))[1],
        actor != preferred_id,
    ))


@dataclass
class PvpDuel:
    """一场双人即时对决（切磋/PK）的共享权威状态。

    两名玩家各自的对战画面（1048 参与者 + 1042 动作）都引用同一份
    ``hp``/``stats``，由战斗系统在任一方发出 1041 指令时推进一轮并
    向双方广播，保证两边血量一致。不与连接级 ``LocalBattleState``
    混用：对决状态挂在战斗系统的进程内注册表上。
    """

    kind: str
    a_id: int
    b_id: int
    stats: dict[int, CombatStats]
    hp: dict[int, int]
    initiative: dict[int, tuple[int, int]] = field(default_factory=dict)
    round: int = 0
    finished: bool = False
    seq: int = 0

    @property
    def trace_id(self) -> str:
        return f'PVP-{self.kind}-{self.a_id}-{self.b_id}-{self.seq}'

    def opponent_of(self, role_id: int) -> int:
        return self.b_id if int(role_id) == int(self.a_id) else self.a_id

    def participants(self) -> tuple[int, int]:
        return int(self.a_id), int(self.b_id)

    def attack_damage(self, attacker_id: int, defender_id: int) -> int:
        attack = max(1, self.stats[int(attacker_id)].physical_attack)
        defence = max(0, self.stats[int(defender_id)].physical_defence)
        return max(1, attack - defence // 2)

    def apply_damage(self, target_id: int, damage: int) -> int:
        remaining = max(0, int(self.hp[int(target_id)]) - max(1, int(damage)))
        self.hp[int(target_id)] = remaining
        return remaining

    def someone_dead(self) -> bool:
        return any(value <= 0 for value in self.hp.values())


@dataclass
class LocalBattleState:
    """Connection-local state for the deliberately small APK battle probe.

    The APK owns rendering and animation; the compatibility server only keeps
    enough state to answer the confirmed 1040/1041/1042 messages for one
    player and up to ten monsters.  Nothing is persisted to the role store.
    """

    active: bool = False
    round: int = 1
    player_id: int = 0
    monster_id: int = 0
    monster_ids: tuple[int, ...] = ()
    monster_hp_by_id: dict[int, int] = field(default_factory=dict)
    initiative: dict[int, tuple[int, int]] = field(default_factory=dict)
    player_hp: int = 100
    player_max_hp: int = 100
    monster_hp: int = 100
    monster_max_hp: int = 100
    player_attack: int = 10
    player_defence: int = 0
    monster_attack: int = 10
    monster_defence: int = 0
    # A defeated monster remains absent until the client reloads the map. This
    # covers automatic battle's short race with the removal frame.
    monster_defeated: bool = False
    # ``round_ack`` means the complete 1042 action queue has been sent and the
    # server is waiting for the APK to report that its animation queue drained.
    phase: str = 'idle'
    # Lightweight per-encounter id so map/battle/resource logs can be grepped
    # together.  It is diagnostic only and never written to the protocol.
    encounter_seq: int = 0
    trace_id: str = ''
    # Map/tile context anchors the post-escape re-trigger guard. The active APK
    # may start a battle through 1010/7 without a tile, so both values are
    # optional and the guard itself must not depend on contact_tile.
    map_id: int = 0
    contact_tile: tuple[int, int] | None = None
    escape_guard: dict[str, object] | None = None
    player_tile: tuple[int, int] | None = None

    def begin(
        self,
        player_id: int,
        monster_id: int,
        player_stats: CombatStats | None = None,
        *,
        monster_ids: tuple[int, ...] | list[int] | None = None,
    ) -> None:
        selected_stats = player_stats or CombatStats(100, 10, 0)
        encounter_ids = tuple(dict.fromkeys(
            int(item) for item in (monster_ids if monster_ids is not None else (monster_id,))
        ))
        if int(monster_id) not in encounter_ids:
            encounter_ids = (int(monster_id),) + encounter_ids
        if not 1 <= len(encounter_ids) <= 10:
            raise ValueError('battle encounter requires between 1 and 10 monsters')
        self.active = True
        self.round = 1
        self.player_id = player_id
        self.monster_id = monster_id
        self.monster_ids = encounter_ids
        self.initiative.clear()
        self.initiative[player_id] = (selected_stats.speed, 0)
        self.player_max_hp = max(1, selected_stats.max_hp)
        self.player_hp = self.player_max_hp
        self.monster_max_hp = 100
        self.monster_hp = self.monster_max_hp
        self.monster_hp_by_id = {
            current_id: self.monster_max_hp
            for current_id in self.monster_ids
        }
        self.player_attack = max(1, selected_stats.physical_attack)
        self.player_defence = max(0, selected_stats.physical_defence)
        self.monster_attack = 10
        self.monster_defence = 0
        self.phase = 'idle'
        self.encounter_seq += 1
        self.trace_id = f'BT-{player_id}-{monster_id}-{self.encounter_seq}'
        self.escape_guard = None

    def finish(self) -> None:
        self.active = False
        self.phase = 'idle'

    def reset_encounter(self) -> None:
        """Respawn the connection-local trial monster on a map reload."""
        self.finish()
        self.monster_defeated = False
        self.trace_id = ''
        self.escape_guard = None
        self.player_tile = None

    def set_escape_guard(
        self,
        map_id: int,
        monster_id: int,
        player_id: int,
        origin: tuple[int, int] | None,
    ) -> None:
        """Prevent an immediate same-map/same-monster re-trigger."""
        self.escape_guard = stamp_guard({
            'map_id': int(map_id),
            'monster_id': int(monster_id),
            'player_id': int(player_id),
            'origin': (int(origin[0]), int(origin[1])) if origin else None,
        })

    def clear_escape_guard(self) -> None:
        self.escape_guard = None

    def escape(self) -> bool:
        """Finish server state as the APK starts its native escape movement."""
        if not self.active:
            return False
        origin = self.player_tile
        self.finish()
        self.set_escape_guard(self.map_id, self.monster_id, self.player_id, origin)
        return True

    def monster_hp_for(self, monster_id: int) -> int:
        wanted = int(monster_id)
        if wanted == self.monster_id:
            return self.monster_hp
        return int(self.monster_hp_by_id.get(wanted, 0))

    def all_monsters_defeated(self) -> bool:
        return bool(self.monster_ids) and all(
            self.monster_hp_for(monster_id) <= 0
            for monster_id in self.monster_ids
        )

    def apply_basic_attack(self, damage: int = 10, *, target_id: int | None = None) -> bool:
        """Apply one deterministic local attack and report whether all monsters died."""
        if not self.active:
            return True
        wanted = self.monster_id if target_id is None else int(target_id)
        if wanted not in self.monster_ids:
            return False
        remaining = max(0, self.monster_hp_for(wanted) - max(1, damage))
        self.monster_hp_by_id[wanted] = remaining
        if wanted == self.monster_id:
            self.monster_hp = remaining
        return self.all_monsters_defeated()

    def player_basic_attack_damage(self) -> int:
        return max(1, self.player_attack - (self.monster_defence // 2))

    def monster_basic_attack_damage(self, *, defending: bool = False) -> int:
        damage = max(1, self.monster_attack - (self.player_defence // 2))
        return max(1, damage // 2) if defending else damage
# The APK does not contain the authoritative server-side reward table.  Keep
# the local trial encounter deterministic, but persist its result through the
# same role/inventory records used by the rest of the service.
BATTLE_EXP_REWARD = 50
BATTLE_DROP_TEMPLATE_ID = 260_000_001
def is_player_escape_command(command_code: int) -> bool:
    """C->S 1041 command 6 is escape; command 10 is quit-spectator."""
    return int(command_code) == 6


def battle_command_target_id(
    values: list[object],
    state: LocalBattleState,
) -> int | None:
    """Read the APK-confirmed 1041 attack target at field index four."""
    if len(values) <= 4:
        return None
    target_id = int(values[4])
    if target_id not in state.monster_ids or state.monster_hp_for(target_id) <= 0:
        return None
    return target_id


def should_suppress_escape_retrigger(
    guard: dict[str, object] | None,
    map_id: int,
    monster_id: int,
) -> bool:
    """Apply the battle-owned OR policy: leave radius or wait two seconds."""
    return should_suppress(guard, map_id, monster_id)


def update_escape_guard_for_movement(state: LocalBattleState, x: int, y: int) -> bool:
    """Clear escape protection only after timeout or leaving the one-tile radius."""
    new_tile = (int(x), int(y))
    state.player_tile = new_tile
    guard = state.escape_guard
    if not guard:
        return False
    if timed_out(guard):
        state.clear_escape_guard()
        return True
    origin = guard.get('origin')
    if origin is None:
        guard['origin'] = new_tile
        return False
    if not movement_outside_guard_radius(guard, new_tile[0], new_tile[1]):
        return False
    state.clear_escape_guard()
    return True


def battle_state_for(session: dict[str, object]) -> LocalBattleState:
    """Connection-scoped battle state, shared with the map system."""
    state = session.get('battle')
    if not isinstance(state, LocalBattleState):
        state = LocalBattleState()
        session['battle'] = state
    return state


def apply_battle_rewards(
    role: dict[str, object],
    experience: int = BATTLE_EXP_REWARD,
    registry: ItemRegistry | None = None,
) -> tuple[dict[str, object] | None, bool]:
    """Persist one trial victory and return the changed item plus level-up flag."""
    old_level = max(1, int(role.get('level', 1)))
    role['experience'] = max(0, int(role.get('experience', 0))) + fuyuan.experience_reward(role, experience)
    if bool(role.get('auto_level', True)):
        while int(role.get('level', 1)) < MAX_ROLE_LEVEL and apply_one_level(role):
            pass

    if registry is None:
        registry = default_item_registry()
    item = next(
        (candidate for candidate in role_items(role)
         if int(candidate.get('template_id', 0)) == BATTLE_DROP_TEMPLATE_ID
         and str(candidate.get('location', 'bag')) == 'bag'),
        None,
    )
    level_up = int(role.get('level', 1)) > old_level
    if item is None:
        if bag_item_count(role) >= bag_capacity(role):
            return None, level_up
        definition = registry.require(BATTLE_DROP_TEMPLATE_ID)
        item = {
            'id': (int(role.get('id', 0)) * 100) + 17,
            'template_id': BATTLE_DROP_TEMPLATE_ID,
            'quantity': 1,
            'location': 'bag',
        }
        role_items(role).append(item)
    else:
        definition = registry.require(BATTLE_DROP_TEMPLATE_ID)
        item['quantity'] = min(
            definition.max_quantity,
            int(item.get('quantity', 0)) + 1,
        )
    return item, level_up

# ---------------------------------------------------------------------------
# 逃跑保护策略（自 battle_escape_guard.py 收编）。
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# 逃跑保护策略（自 battle_escape_guard.py 收编）。
# ---------------------------------------------------------------------------
CONTACT_RADIUS_TILES = 1
RETRIGGER_TIMEOUT_SECONDS = 2.0
_CREATED_AT_KEY = 'created_at'


def stamp_guard(
    guard: dict[str, object] | None,
    *,
    now: float | None = None,
) -> dict[str, object] | None:
    """Stamp a freshly-created battle escape guard with monotonic time."""
    if guard is None:
        return None
    guard[_CREATED_AT_KEY] = time.monotonic() if now is None else float(now)
    return guard


def _matches(
    guard: dict[str, object] | None,
    map_id: int,
    monster_id: int,
) -> bool:
    if not guard:
        return False
    return (
        int(guard.get('map_id', -1)) == int(map_id)
        and int(guard.get('monster_id', -1)) == int(monster_id)
    )


def timed_out(
    guard: dict[str, object] | None,
    *,
    now: float | None = None,
    timeout_seconds: float = RETRIGGER_TIMEOUT_SECONDS,
) -> bool:
    """Return whether a stamped guard has reached its retrigger timeout."""
    if not guard:
        return False
    created_at = guard.get(_CREATED_AT_KEY)
    if created_at is None:
        # Legacy guards created before this policy stay movement-gated rather
        # than being treated as already expired.
        return False
    current = time.monotonic() if now is None else float(now)
    return current - float(created_at) >= float(timeout_seconds)


def should_suppress(
    guard: dict[str, object] | None,
    map_id: int,
    monster_id: int,
    *,
    now: float | None = None,
) -> bool:
    """Suppress the same encounter only until the two-second timeout expires."""
    if not _matches(guard, map_id, monster_id):
        return False
    return not timed_out(guard, now=now)


def movement_outside_guard_radius(
    guard: dict[str, object] | None,
    x: int,
    y: int,
    *,
    radius: int = CONTACT_RADIUS_TILES,
) -> bool:
    """Return whether movement leaves the one-tile escape contact radius."""
    if not guard:
        return False
    origin = guard.get('origin')
    if origin is None:
        return False
    origin_x, origin_y = int(origin[0]), int(origin[1])
    return max(abs(int(x) - origin_x), abs(int(y) - origin_y)) > int(radius)
