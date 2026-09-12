from __future__ import annotations

import time
from dataclasses import dataclass, field


CONTACT_RADIUS_TILES = 1
RETRIGGER_TIMEOUT_SECONDS = 2.0


@dataclass(frozen=True)
class CombatStats:
    max_hp: int
    physical_attack: int
    physical_defence: int


@dataclass
class LocalBattleState:
    """Connection-local authoritative battle state.

    The APK owns rendering and animation. The compatibility server keeps only
    the confirmed 1040/1041/1042 state plus encounter context needed to decide
    whether the same map monster may immediately retrigger after escape.
    """

    active: bool = False
    round: int = 1
    player_id: int = 0
    monster_id: int = 0
    monster_ids: tuple[int, ...] = ()
    monster_hp_by_id: dict[int, int] = field(default_factory=dict)
    player_hp: int = 100
    player_max_hp: int = 100
    monster_hp: int = 100
    monster_max_hp: int = 100
    player_attack: int = 10
    player_defence: int = 0
    monster_attack: int = 10
    monster_defence: int = 0
    monster_defeated: bool = False
    phase: str = 'idle'
    encounter_seq: int = 0
    trace_id: str = ''
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
            int(item)
            for item in (monster_ids if monster_ids is not None else (monster_id,))
        ))
        if int(monster_id) not in encounter_ids:
            encounter_ids = (int(monster_id),) + encounter_ids
        if not 1 <= len(encounter_ids) <= 10:
            raise ValueError('battle encounter requires between 1 and 10 monsters')

        self.active = True
        self.round = 1
        self.player_id = int(player_id)
        self.monster_id = int(monster_id)
        self.monster_ids = encounter_ids
        self.player_max_hp = max(1, int(selected_stats.max_hp))
        self.player_hp = self.player_max_hp
        self.monster_max_hp = 100
        self.monster_hp = self.monster_max_hp
        self.monster_hp_by_id = {
            current_id: self.monster_max_hp
            for current_id in self.monster_ids
        }
        self.player_attack = max(1, int(selected_stats.physical_attack))
        self.player_defence = max(0, int(selected_stats.physical_defence))
        self.monster_attack = 10
        self.monster_defence = 0
        self.phase = 'idle'
        self.encounter_seq += 1
        self.trace_id = f'BT-{self.player_id}-{self.monster_id}-{self.encounter_seq}'
        self.escape_guard = None

    def finish(self) -> None:
        self.active = False
        self.phase = 'idle'

    def reset_encounter(self) -> None:
        """Respawn the connection-local encounter after a map reload."""
        self.finish()
        self.monster_defeated = False
        self.trace_id = ''
        self.escape_guard = None
        self.player_tile = None
        self.contact_tile = None

    def set_escape_guard(
        self,
        map_id: int,
        monster_id: int,
        player_id: int,
        origin: tuple[int, int] | None,
        *,
        now: float | None = None,
    ) -> None:
        """Protect one escaped encounter until radius exit or two-second timeout."""
        self.escape_guard = {
            'map_id': int(map_id),
            'monster_id': int(monster_id),
            'player_id': int(player_id),
            'origin': (int(origin[0]), int(origin[1])) if origin else None,
            'created_at': time.monotonic() if now is None else float(now),
        }

    def clear_escape_guard(self) -> None:
        self.escape_guard = None

    def should_suppress_retrigger(
        self,
        map_id: int,
        monster_id: int,
        *,
        now: float | None = None,
    ) -> bool:
        """Suppress only the guarded same-map/same-monster encounter."""
        guard = self.escape_guard
        if not guard:
            return False
        if (
            int(guard.get('map_id', -1)) != int(map_id)
            or int(guard.get('monster_id', -1)) != int(monster_id)
        ):
            return False

        created_at = guard.get('created_at')
        if created_at is None:
            # Keep old unstamped guards movement-gated during migration.
            return True
        current = time.monotonic() if now is None else float(now)
        if current - float(created_at) >= RETRIGGER_TIMEOUT_SECONDS:
            self.clear_escape_guard()
            return False
        return True

    def update_player_tile(
        self,
        x: int,
        y: int,
        *,
        now: float | None = None,
    ) -> bool:
        """Record movement and clear escape protection when either release rule wins."""
        new_tile = (int(x), int(y))
        self.player_tile = new_tile
        guard = self.escape_guard
        if not guard:
            return False

        created_at = guard.get('created_at')
        if created_at is not None:
            current = time.monotonic() if now is None else float(now)
            if current - float(created_at) >= RETRIGGER_TIMEOUT_SECONDS:
                self.clear_escape_guard()
                return True

        origin = guard.get('origin')
        if origin is None:
            guard['origin'] = new_tile
            return False
        origin_x, origin_y = int(origin[0]), int(origin[1])
        if max(abs(new_tile[0] - origin_x), abs(new_tile[1] - origin_y)) <= CONTACT_RADIUS_TILES:
            return False

        self.clear_escape_guard()
        return True

    def escape(self, *, now: float | None = None) -> bool:
        """Finish battle state and create the post-escape encounter guard."""
        if not self.active:
            return False
        # The encounter contact tile is the monster-contact anchor. Fall back
        # to the last player tile for older entry paths that do not provide it.
        origin = self.contact_tile if self.contact_tile is not None else self.player_tile
        self.finish()
        self.set_escape_guard(
            self.map_id,
            self.monster_id,
            self.player_id,
            origin,
            now=now,
        )
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

    def apply_basic_attack(
        self,
        damage: int = 10,
        *,
        target_id: int | None = None,
    ) -> bool:
        """Apply one deterministic local attack and report encounter victory."""
        if not self.active:
            return True
        wanted = self.monster_id if target_id is None else int(target_id)
        if wanted not in self.monster_ids:
            return False
        remaining = max(0, self.monster_hp_for(wanted) - max(1, int(damage)))
        self.monster_hp_by_id[wanted] = remaining
        if wanted == self.monster_id:
            self.monster_hp = remaining
        return self.all_monsters_defeated()

    def player_basic_attack_damage(self) -> int:
        return max(1, self.player_attack - (self.monster_defence // 2))

    def monster_basic_attack_damage(self, *, defending: bool = False) -> int:
        damage = max(1, self.monster_attack - (self.player_defence // 2))
        return max(1, damage // 2) if defending else damage
