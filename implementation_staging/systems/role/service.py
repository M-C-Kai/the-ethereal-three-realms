"""角色创建、登录、属性与持久化业务规则。"""

from __future__ import annotations


def normalized_sect_id(role: dict[str, object], registry: SectRegistry) -> int:
    """Return a client-safe sect ID for the 1006 property table."""
    try:
        sect_id = int(role.get('sect_id', 0))
        # Validate sect_id exists in registry
        if registry.sect(sect_id) is None:
            return 0
        return sect_id
    except (TypeError, ValueError):
        return 0



def join_sect(role: dict[str, object], sect_id: int, registry: SectRegistry) -> bool:
    """Join one valid sect while the role currently has no sect."""
    if sect_id == 0:
        return False

    if registry.sect(sect_id) is None:
        return False

    if normalized_sect_id(role, registry) != 0:
        return False

    role['sect_id'] = sect_id
    return True

from dataclasses import dataclass, field
# ---------------------------------------------------------------------------
# 角色业务：账号/角色存储、属性、升级、门派与初始角色装配（自 server.py 迁入）。
# ---------------------------------------------------------------------------
import json
import logging
import hashlib
import hmac
import re
import secrets
from pathlib import Path

from systems.fuyuan import service as fuyuan
from protocol import (
    Field, TYPE_BYTE, TYPE_INT, TYPE_SHORT, byte, encode_frame, integer, short, string,
)
from systems.role.events import CharacterUpdateBus
from systems.inventory.protocol import (
    is_equipment, is_strengthenable_weapon, item_frame, item_slot, role_items,
)
import copy
import string as ascii_string
from systems.inventory.registry import (
    STRENGTHENING_ATTACK_BONUSES, default_item_registry,
    normalized_strengthen_level, recalculate_equipment_attributes,
    weapon_appearance_field_from_icon_and_strengthen,
)
from systems.inventory.service import (
    DEFAULT_BAG_CAPACITY, ROLE_BAG_RESET_VERSION, ROLE_BAG_PREVIEW_SUPPRESSION_VERSION,
    bag_capacity, bag_item_count, clear_role_bag_once,
    ensure_all_mount_series_items, ensure_equipment_resource_preview_items,
    is_strengthening_stone, role_items, starter_items,
)
from systems.task.service import ensure_task_state

LOG = logging.getLogger('piaomiao-local')

@dataclass(frozen=True)
class CombatStats:
    max_hp: int
    physical_attack: int
    physical_defence: int
    speed: int = 0


def equipped_attribute_totals(
    role: dict[str, object],
    registry: ItemRegistry | None = None,
) -> tuple[int, int, int, int]:
    """Aggregate the four protocol equipment attributes of all equipped items."""
    if registry is None:
        registry = default_item_registry()
    totals = [0, 0, 0, 0]
    for item in role_items(role):
        if item.get('location') != 'equipped':
            continue
        try:
            resolved = registry.resolve(item)
        except Exception:
            continue
        if int(resolved.get('equipment_slot', 0)) <= 0:
            continue
        attributes = list(resolved.get('equipment_attributes', [0, 0, 0, 0]))
        for index, value in enumerate((attributes + [0, 0, 0, 0])[:4]):
            if type(value) is int:
                totals[index] += max(0, int(value))
    return tuple(totals)


def effective_character_stats(
    role: dict[str, object],
    registry: ItemRegistry | None = None,
) -> list[int]:
    """Return the five character-panel values after confirmed equipment bonuses."""
    raw_stats = [int(value) for value in list(role.get('stats', []))]
    values = [max(0, value) for value in (raw_stats + [10, 10, 10, 10, 10])[:5]]
    equipment = equipped_attribute_totals(role, registry)
    # Compatibility evidence: equipment attribute[0] is attack and [1] is
    # defence.  Do not invent meanings for the remaining two fields.
    values[0] += equipment[0]
    values[1] += equipment[1]
    return values


def equipped_weapon_attack(
    role: dict[str, object],
    registry: ItemRegistry | None = None,
) -> int:
    """Return the effective first attribute of the equipped slot-10 weapon."""
    if registry is None:
        registry = default_item_registry()
    for item in role_items(role):
        if item.get('location') != 'equipped':
            continue
        resolved = registry.resolve(item)
        if int(resolved.get('equipment_slot', 0)) != 10:
            continue
        attributes = list(resolved.get('equipment_attributes', [0, 0, 0, 0]))
        if not attributes or type(attributes[0]) is not int:
            return 0
        return max(0, int(attributes[0]))
    return 0



def equipped_weapon_battle_field2(
    role: dict[str, object],
    registry: ItemRegistry | None = None,
) -> int:
    """Return APK 1048 field[2] for the currently equipped slot-10 weapon.

    Map property7 and battle field[2] use different resource namespaces.
    The equipment icon is the shared source of truth; the battle value is
    derived through the user-confirmed icon-group -> battle-family mapping.
    """
    if registry is None:
        registry = default_item_registry()
    weapon = next(
        (
            item
            for item in role_items(role)
            if item.get('location') == 'equipped'
            and is_equipment(item)
            and item_slot(item, registry) == 10
        ),
        None,
    )
    if weapon is None:
        return 0
    resolved = registry.resolve(weapon)
    return weapon_appearance_field_from_icon_and_strengthen(
        int(resolved.get('icon_code', 0)),
        normalized_strengthen_level(resolved),
    )


def combat_stats(
    role: dict[str, object],
    registry: ItemRegistry | None = None,
) -> CombatStats:
    """Derive battle values from the same equipped state shown by the character UI."""
    level = max(1, int(role.get('level', 1)))
    raw_stats = [int(value) for value in list(role.get('stats', []))]
    base_stats = [max(0, value) for value in (raw_stats + [10, 10, 10, 10, 10])[:5]]
    equipment = equipped_attribute_totals(role, registry)
    return CombatStats(
        max_hp=fuyuan.hp_limit(role, 100 + ((level - 1) * 10) + base_stats[1]),
        physical_attack=(10 + base_stats[0] + ((level - 1) * 2) + equipment[0]),
        physical_defence=base_stats[1] + (level - 1) + equipment[1],
        speed=effective_character_stats(role, registry)[4],
    )
MAX_ROLE_LEVEL = 99
LEVEL_BASE_STAT_GAIN = 1
DEFAULT_CURRENCY_BALANCE = 10_000_000
MAX_CURRENCY_BALANCE = 2_147_483_647
CURRENCY_PROPERTIES = {
    'immortal_stones': 49,
    'silver': 50,
    'immortal_crystals': 52,
}
def initial_currency_balances() -> dict[str, int]:
    return {
        name: DEFAULT_CURRENCY_BALANCE
        for name in CURRENCY_PROPERTIES
    }


def normalized_currency_balance(value: object) -> int:
    if type(value) is int and 0 <= value <= MAX_CURRENCY_BALANCE:
        return value
    return DEFAULT_CURRENCY_BALANCE
# 1042 only appends records to the APK's battle queue. The following full
# 1040/action=2 calls the battle screen's i() method and starts playback. The
# client then returns the short [action=2, round] acknowledgement after the
# complete queue has drained, so the server never guesses sprite timings.
ROLE_MODELS = (
    ((0, 2, 4), (19, 23, 1, 3, 5)),
    ((6, 8, 10), (7, 9, 11)),
    ((12, 14, 16), (13, 15, 17)),
)

ROLE_STATS = (
    (2, 16, 7, 28, 7, 18, 3, 15, 2, 15, 7, 14, 8, 15, 3, 11, 17, 28, 2, 16, 7, 28, 7, 18),
    (7, 7, 3, 25, 3, 25, 4, 22, 2, 22, 3, 23, 2, 22, 4, 1, 5, 25, 7, 7, 3, 25, 3, 25),
    (16, 14, 17, 41, 2, 9, 4, 13, 17, 7, 17, 9, 5, 13, 4, 9, 6, 41, 16, 14, 17, 41, 2, 9),
    (3, 0, 10, 49, 4, 6, 8, 10, 9, 4, 10, 0, 5, 10, 8, 0, 6, 49, 3, 0, 10, 49, 4, 6),
    (3, 6, 4, 16, 7, 5, 0, 4, 9, 7, 4, 1, 9, 4, 9, 6, 1, 16, 3, 6, 4, 16, 7, 5),
    (4, 21, 1, 46, 1, 9, 7, 1, 27, 1, 1, 5, 4, 1, 7, 22, 8, 46, 4, 21, 1, 46, 1, 9),
    (2, 1, 7, 3, 5, 3, 4, 7, 9, 5, 7, 6, 6, 7, 4, 9, 3, 3, 2, 1, 7, 3, 5, 3),
)
DEFAULT_MOUNT_MODEL = 105000
MOUNT_EQUIPMENT_SLOT = 17  # APK resource 0x4661: the dedicated "坐骑" slot.
def role_race_and_gender(model: int) -> tuple[int, int]:
    for race, gender_models in enumerate(ROLE_MODELS):
        for gender, models in enumerate(gender_models):
            if model in models:
                return race, gender
    return 0, 0


def role_stats(model: int) -> list[int]:
    if not 0 <= model < 24:
        return [0] * 8
    return [values[model] for values in ROLE_STATS] + [0]


def default_role(settings: Settings) -> dict[str, object]:
    initial_map = settings.map_registry.require(settings.default_map_id)
    role = {
        'id': settings.role_id,
        'name': settings.role_name,
        'model': settings.role_model,
        'slot': 0,
        'race': 0,
        'sect_id': 0,
        'gender': 0,
        'level': 1,
        'experience': 0,
        'auto_level': True,
        'stats': [0] * 8,
        'map_id': initial_map.id,
        'map_name': initial_map.name,
        'map_x': initial_map.spawn_x,
        'map_y': initial_map.spawn_y,
        'mount_model': 0,
        'bag_capacity': DEFAULT_BAG_CAPACITY,
        'currencies': initial_currency_balances(),
    }
    role['items'] = starter_items(int(role['id']), settings.item_registry)
    ensure_equipment_resource_preview_items(role, settings.item_registry)
    role['strengthening_stones_initialized'] = True
    role['mailbox'] = starter_mail(int(role['id']))
    role['mailbox_initialized'] = True
    role['bag_reset_version'] = ROLE_BAG_RESET_VERSION
    ensure_task_state(role)
    fuyuan.ensure_state(role)
    return role
def starter_mail(role_id: int) -> list[dict[str, object]]:
    """Return the one persisted system mail delivered to a new or legacy role."""
    return [{
        'id': (role_id * 100) + 90,
        'sender': '系统',
        'subject': '欢迎来到本地服',
        'body': '欢迎来到《飘渺三界2》本地服。_这封邮件会随角色存档保存。',
        'sent_at': '2026-09-01',
        'expires_at': '长期有效',
        'read': False,
    }]
class AccountStore:
    """Persist local credentials without storing plaintext passwords."""

    USERNAME_PATTERN = re.compile(r'^[A-Za-z0-9]{1,32}$')
    PASSWORD_PATTERN = re.compile(r'^[A-Za-z0-9]{4,13}$')
    MOBILE_PATTERN = re.compile(r'^1[3-9][0-9]{9}$')

    def __init__(self, settings: Settings):
        path = Path(settings.account_data_file)
        self.path = path if path.is_absolute() else Path(__file__).resolve().parents[2] / path
        self.iterations = max(1, int(settings.password_hash_iterations))
        self.data: dict[str, object] = {'version': 1, 'accounts': {}}
        if self.path.exists():
            try:
                loaded = json.loads(self.path.read_text(encoding='utf-8'))
                if isinstance(loaded, dict) and isinstance(loaded.get('accounts'), dict):
                    self.data = loaded
            except (OSError, ValueError) as exc:
                LOG.warning('failed to load account data %s: %s', self.path, exc)

    def _save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_suffix(self.path.suffix + '.tmp')
        temporary.write_text(json.dumps(self.data, ensure_ascii=False, indent=2), encoding='utf-8')
        temporary.replace(self.path)

    @staticmethod
    def _derive(password: str, salt: bytes, iterations: int) -> str:
        return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, iterations).hex()

    def _new_record(self, username: str, password: str) -> dict[str, object]:
        salt = secrets.token_bytes(16)
        return {
            'salt': salt.hex(),
            'password_hash': self._derive(password, salt, self.iterations),
            'iterations': self.iterations,
            'recovery_phone': username if self.MOBILE_PATTERN.fullmatch(username) else '',
        }

    def register(self, username: str, password: str) -> str:
        username = username.strip()
        if not self.USERNAME_PATTERN.fullmatch(username) or not self.PASSWORD_PATTERN.fullmatch(password):
            return 'invalid'
        accounts = self.data['accounts']
        assert isinstance(accounts, dict)
        if username in accounts:
            return 'exists'
        accounts[username] = self._new_record(username, password)
        self._save()
        return 'ok'

    def authenticate(self, username: str, password: str) -> bool:
        accounts = self.data['accounts']
        assert isinstance(accounts, dict)
        record = accounts.get(username)
        if not isinstance(record, dict):
            return False
        try:
            salt = bytes.fromhex(str(record['salt']))
            iterations = int(record['iterations'])
            expected = str(record['password_hash'])
        except (KeyError, TypeError, ValueError):
            return False
        return hmac.compare_digest(self._derive(password, salt, iterations), expected)

    def change_password(self, username: str, old_password: str, new_password: str) -> str:
        if not self.PASSWORD_PATTERN.fullmatch(new_password):
            return 'invalid'
        if not self.authenticate(username, old_password):
            return 'denied'
        accounts = self.data['accounts']
        assert isinstance(accounts, dict)
        previous = accounts[username]
        assert isinstance(previous, dict)
        replacement = self._new_record(username, new_password)
        replacement['recovery_phone'] = str(previous.get('recovery_phone', ''))
        accounts[username] = replacement
        self._save()
        return 'ok'

    def recover_password(self, username: str, phone: str) -> tuple[str, str | None]:
        accounts = self.data['accounts']
        assert isinstance(accounts, dict)
        record = accounts.get(username)
        if not isinstance(record, dict) or not str(record.get('recovery_phone', '')):
            return 'denied', None
        registered_phone = str(record.get('recovery_phone', ''))
        if not hmac.compare_digest(registered_phone, phone):
            return 'denied', None
        alphabet = ascii_string.ascii_letters + ascii_string.digits
        temporary_password = ''.join(secrets.choice(alphabet) for _ in range(8))
        replacement = self._new_record(username, temporary_password)
        replacement['recovery_phone'] = registered_phone
        accounts[username] = replacement
        self._save()
        return 'ok', temporary_password

class RoleStore:
    def __init__(self, settings: Settings):
        path = Path(settings.role_data_file)
        self.path = path if path.is_absolute() else Path(__file__).resolve().parents[2] / path
        self.settings = settings
        # 装配期注入的角色加载钩子（如宠物系统 schema 迁移）。
        self.role_loaded_hooks: list = []
        self.data: dict[str, object] = {'next_role_id': settings.role_id + 1, 'accounts': {}}
        if self.path.exists():
            try:
                loaded = json.loads(self.path.read_text(encoding='utf-8'))
                if isinstance(loaded, dict) and isinstance(loaded.get('accounts'), dict):
                    self.data = loaded
            except (OSError, ValueError) as exc:
                LOG.warning('failed to load role data %s: %s', self.path, exc)

    def _save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_suffix(self.path.suffix + '.tmp')
        temporary.write_text(json.dumps(self.data, ensure_ascii=False, indent=2), encoding='utf-8')
        temporary.replace(self.path)

    def save(self) -> None:
        self._save()

    def _ensure_items(
        self,
        role: dict[str, object],
    ) -> bool:
        registry = self.settings.item_registry
        items = role.get('items')
        if not isinstance(items, list):
            role['items'] = starter_items(int(role.get('id', 0)), registry)
            role['strengthening_stones_initialized'] = True
            ensure_equipment_resource_preview_items(role, registry)
            ensure_all_mount_series_items(role, registry)
            return True
        changed = False
        stones_initialized = bool(role.get('strengthening_stones_initialized', False))
        defaults = starter_items(int(role.get('id', 0)), registry)
        by_id = {
            int(item.get('id', 0)): item
            for item in items
            if isinstance(item, dict)
        }
        stones_by_template = {
            int(item.get('template_id', 0)): item
            for item in items
            if isinstance(item, dict) and is_strengthening_stone(item)
        }
        # Strip template fields from legacy items that still carry them.
        template_owned_fields = {
            'kind', 'name', 'description', 'max_quantity', 'price',
            'level_required', 'icon_code', 'quality', 'sort_group',
            'sort_order', 'equipment_slot', 'innate_attributes',
            'acquired_attributes', 'extra_attributes', 'appearance_properties',
            'item_flags', 'action_flags', 'heal', 'mount_model',
        }
        for item in items:
            if not isinstance(item, dict):
                continue
            before_keys = set(item.keys())
            for field_name in template_owned_fields:
                item.pop(field_name, None)
            if set(item.keys()) != before_keys:
                changed = True
        # Upgrade the two legacy test items in place and append the missing
        # equipment slots.  Location and quantities are player state, so they
        # survive this catalogue migration.
        for default in defaults:
            item_id = int(default['id'])
            if is_strengthening_stone(default):
                template_id = int(default['template_id'])
                current = stones_by_template.get(template_id)
                if current is None and stones_initialized:
                    continue
                if current is None:
                    conflicting = by_id.get(item_id)
                    if conflicting is not None:
                        used_ids = set(by_id)
                        replacement_id = (int(role.get('id', 0)) * 100) + 20
                        while replacement_id in used_ids:
                            replacement_id += 1
                        conflicting['id'] = replacement_id
                        del by_id[item_id]
                        by_id[replacement_id] = conflicting
                        changed = True
                        LOG.warning(
                            'reassigned legacy item id collision role_id=%s old_id=%d new_id=%d',
                            role.get('id', 0),
                            item_id,
                            replacement_id,
                        )
            else:
                current = by_id.get(item_id)
            if current is None:
                items.append(default)
                by_id[item_id] = default
                if is_strengthening_stone(default):
                    stones_by_template[int(default['template_id'])] = default
                changed = True
                continue
            preserved = {
                key: current[key]
                for key in (
                    'id',
                    'location',
                    'quantity',
                    'last_heal',
                    'strengthen_level',
                    'base_equipment_attributes',
                )
                if key in current
            }
            # Only preserve equipment_attributes if the item has been modified
            # (strengthened or has base_equipment_attributes). Otherwise, let
            # the template default from the registry take precedence.
            if 'base_equipment_attributes' in current or 'strengthen_level' in current:
                if 'equipment_attributes' in current:
                    preserved['equipment_attributes'] = list(current['equipment_attributes'])
            resolved_default = registry.resolve(default)
            if (
                int(resolved_default.get('equipment_slot', 0)) == 10
                and 'base_equipment_attributes' not in current
                and 'equipment_attributes' in current
            ):
                # Before strengthening existed, the effective weapon values
                # were also its base values. Seed the new stable base from the
                # persisted weapon instead of replacing custom legacy stats
                # with the starter catalogue defaults.
                current_attributes = list(
                    current.get('equipment_attributes', [0, 0, 0, 0])
                )
                base_attributes = [
                    (
                        current_attributes[index]
                        if index < len(current_attributes)
                        and type(current_attributes[index]) is int
                        and current_attributes[index] >= 0
                        else 0
                    )
                    for index in range(4)
                ]
                raw_level = current.get('strengthen_level', 0)
                level = normalized_strengthen_level(current)
                if type(raw_level) is int and 0 < raw_level <= 9:
                    base_attributes[0] = max(
                        0,
                        base_attributes[0] - STRENGTHENING_ATTACK_BONUSES[level],
                    )
                preserved['base_equipment_attributes'] = base_attributes
            resolved_default = registry.resolve(default)
            # Determine if this is a weapon before stripping template fields.
            is_weapon = int(resolved_default.get('equipment_slot', 0)) == 10
            # Strip template-owned fields from the resolved default before
            # merging.  Only preserved instance state should survive into the
            # role item; template fields are resolved at read time.
            for field_name in template_owned_fields:
                resolved_default.pop(field_name, None)
            merged = {**resolved_default, **preserved}
            if is_weapon:
                weapon_level = normalized_strengthen_level(current) if 'strengthen_level' in current else normalized_strengthen_level(merged)
                merged['strengthen_level'] = weapon_level
                recalculate_equipment_attributes(merged)
            if current != merged:
                current.clear()
                current.update(merged)
                changed = True
        # Handle extra items that don't match any starter default.
        # These need template field stripping and weapon base seeding.
        for item in items:
            if not isinstance(item, dict):
                continue
            item_id = int(item.get('id', 0))
            if item_id in {int(d['id']) for d in defaults}:
                continue
            resolved = registry.resolve(item)
            if (
                int(resolved.get('equipment_slot', 0)) == 10
                and 'base_equipment_attributes' not in item
            ):
                if 'equipment_attributes' in item:
                    current_attributes = list(item['equipment_attributes'])
                else:
                    current_attributes = list(
                        resolved.get('equipment_attributes', [0, 0, 0, 0])
                    )
                base_attributes = [
                    (
                        current_attributes[index]
                        if index < len(current_attributes)
                        and type(current_attributes[index]) is int
                        and current_attributes[index] >= 0
                        else 0
                    )
                    for index in range(4)
                ]
                raw_level = item.get('strengthen_level', 0)
                level = normalized_strengthen_level(item)
                if type(raw_level) is int and 0 < raw_level <= 9:
                    base_attributes[0] = max(
                        0,
                        base_attributes[0] - STRENGTHENING_ATTACK_BONUSES[level],
                    )
                item['base_equipment_attributes'] = base_attributes
                changed = True
        if not stones_initialized:
            role['strengthening_stones_initialized'] = True
            changed = True
        changed = ensure_equipment_resource_preview_items(role, registry) or changed
        changed = ensure_all_mount_series_items(role, registry) or changed
        for item in items:
            if not isinstance(item, dict) or not is_strengthenable_weapon(item):
                continue
            before_strengthening = copy.deepcopy(item)
            raw_level = item.get('strengthen_level', 0)
            level = normalized_strengthen_level(item)
            if 'base_equipment_attributes' not in item:
                # For new weapons, initialise base from the catalogue
                # template rather than from the (possibly absent) instance
                # equipment_attributes.
                if 'equipment_attributes' in item:
                    current_attributes = list(item['equipment_attributes'])
                else:
                    resolved = registry.resolve(item)
                    current_attributes = list(
                        resolved.get('equipment_attributes', [0, 0, 0, 0])
                    )
                base_attributes = []
                for index in range(4):
                    value = current_attributes[index] if index < len(current_attributes) else 0
                    base_attributes.append(
                        value if type(value) is int and value >= 0 else 0
                    )
                if type(raw_level) is int and 0 < raw_level <= 9:
                    base_attributes[0] = max(
                        0,
                        base_attributes[0] - STRENGTHENING_ATTACK_BONUSES[level],
                    )
                item['base_equipment_attributes'] = base_attributes
            item['strengthen_level'] = level
            recalculate_equipment_attributes(item)
            if item != before_strengthening:
                changed = True
        return changed

    @staticmethod
    def _ensure_mailbox(role: dict[str, object]) -> bool:
        mailbox = role.get('mailbox')
        if not bool(role.get('mailbox_initialized', False)):
            if not isinstance(mailbox, list):
                role['mailbox'] = starter_mail(int(role.get('id', 0)))
            role['mailbox_initialized'] = True
            return True
        if not isinstance(mailbox, list):
            role['mailbox'] = []
            return True
        return False

    def roles_for(self, username: str, *, create_default: bool = True) -> list[dict[str, object]]:
        accounts = self.data['accounts']
        assert isinstance(accounts, dict)
        if username not in accounts:
            accounts[username] = [default_role(self.settings)] if create_default else []
            self._save()
        roles = accounts[username]
        assert isinstance(roles, list)
        changed = False
        for role in roles:
            for hook in self.role_loaded_hooks:
                if hook(role):
                    changed = True
            if ensure_task_state(role):
                changed = True
            if fuyuan.settle(role):
                changed = True
            if 'experience' not in role:
                role['experience'] = 0
                changed = True
            if 'auto_level' not in role:
                role['auto_level'] = True
                changed = True
            if 'sect_id' not in role:
                role['sect_id'] = 0
                changed = True
            try:
                existing_capacity = int(role.get('bag_capacity', 0))
            except (TypeError, ValueError):
                existing_capacity = 0
            new_capacity = max(existing_capacity, DEFAULT_BAG_CAPACITY)
            if role.get('bag_capacity') != new_capacity:
                role['bag_capacity'] = new_capacity
                changed = True
            currencies = role.get('currencies')
            if not isinstance(currencies, dict):
                currencies = initial_currency_balances()
                role['currencies'] = currencies
                changed = True
            for name in CURRENCY_PROPERTIES:
                current_balance = currencies.get(name)
                normalized_balance = normalized_currency_balance(current_balance)
                if type(current_balance) is not int or current_balance != normalized_balance:
                    currencies[name] = normalized_balance
                    changed = True

            # Migrate skill_levels to sect_skills
            if not isinstance(role.get("sect_skills"), dict):
                sect_skills = {}
                old_levels = role.get("skill_levels")

                if isinstance(old_levels, dict):
                    for skill_id_str, level in old_levels.items():
                        try:
                            skill_id = int(skill_id_str)
                            # Only migrate skills that exist in registry
                            if self.settings.sect_registry.skill(skill_id) is not None:
                                sect_skills[str(skill_id)] = {
                                    "level": max(0, int(level)),
                                }
                        except (TypeError, ValueError):
                            pass

                role["sect_skills"] = sect_skills
                changed = True
            try:
                current_map = self.settings.map_registry.require(
                    int(role.get('map_id', self.settings.default_map_id))
                )
            except (TypeError, ValueError):
                current_map = self.settings.map_registry.require(self.settings.default_map_id)
                LOG.warning(
                    'role %s referenced unknown map %r; migrating to default map %d',
                    role.get('id', 0),
                    role.get('map_id'),
                    current_map.id,
                )
                role['map_id'] = current_map.id
                changed = True
            if role.get('map_name') != current_map.name:
                role['map_name'] = current_map.name
                changed = True
            if 'map_x' not in role:
                role['map_x'] = current_map.spawn_x
                changed = True
            if 'map_y' not in role:
                role['map_y'] = current_map.spawn_y
                changed = True
            changed = self._ensure_items(role) or changed
            changed = clear_role_bag_once(role) or changed
            changed = self._ensure_mailbox(role) or changed
        if changed:
            self._save()
        return sorted(roles, key=lambda role: int(role.get('slot', 0)))

    def find(self, username: str, role_id: int) -> dict[str, object] | None:
        return next((role for role in self.roles_for(username) if int(role.get('id', 0)) == role_id), None)

    def create(self, username: str, name: str, model: int, requested_slot: int) -> dict[str, object]:
        roles = self.roles_for(username)
        occupied = {int(role.get('slot', 0)) for role in roles}
        slot = requested_slot if requested_slot in range(3) and requested_slot not in occupied else -1
        if slot < 0:
            slot = next((candidate for candidate in range(3) if candidate not in occupied), 0)
        valid_models = {value for race in ROLE_MODELS for gender in race for value in gender}
        if model not in valid_models:
            model = 0
        race, gender = role_race_and_gender(model)
        role_id = int(self.data.get('next_role_id', self.settings.role_id + 1))
        self.data['next_role_id'] = role_id + 1
        initial_map = self.settings.map_registry.require(self.settings.default_map_id)
        role: dict[str, object] = {
            'id': role_id,
            'name': name.strip() or f'本地侠客{role_id}',
            'model': model,
            'slot': slot,
            'race': race,
            'sect_id': 0,
            'gender': gender,
            'level': 1,
            'experience': 0,
            'auto_level': True,
            'stats': role_stats(model),
            'map_id': initial_map.id,
            'map_name': initial_map.name,
            'map_x': initial_map.spawn_x,
            'map_y': initial_map.spawn_y,
            'bag_capacity': DEFAULT_BAG_CAPACITY,
            'currencies': initial_currency_balances(),
        }
        role['items'] = starter_items(role_id, self.settings.item_registry)
        ensure_equipment_resource_preview_items(role, self.settings.item_registry)
        role['strengthening_stones_initialized'] = True
        role['mailbox'] = starter_mail(role_id)
        role['mailbox_initialized'] = True
        role['bag_reset_version'] = ROLE_BAG_RESET_VERSION
        ensure_task_state(role)
        fuyuan.ensure_state(role)
        for hook in self.role_loaded_hooks:
            hook(role)
        roles.append(role)
        accounts = self.data['accounts']
        assert isinstance(accounts, dict)
        accounts[username] = roles
        self._save()
        return role

    def delete(self, username: str, role_id: int) -> bool:
        roles = self.roles_for(username)
        remaining = [role for role in roles if int(role.get('id', 0)) != role_id]
        if len(remaining) == len(roles):
            return False
        accounts = self.data['accounts']
        assert isinstance(accounts, dict)
        accounts[username] = remaining
        self._save()
        return True

def _get_sect_skill_level(role: dict[str, object], skill_id: int, settings: Settings) -> int:
    """Get the level of a sect skill for a role.

    Supports both old skill_levels format and new sect_skills format.
    """
    # Try new sect_skills format first
    if 'sect_skills' in role:
        skill_data = role['sect_skills'].get(str(skill_id))
        if skill_data and isinstance(skill_data, dict):
            try:
                level = int(skill_data.get('level', 0))
                # Clamp to valid range
                skill = settings.sect_registry.skill(skill_id)
                if skill:
                    max_level = skill.max_level
                    return max(0, min(level, max_level))
                return max(0, level)
            except (TypeError, ValueError):
                pass
    
    # Fall back to old skill_levels format
    if 'skill_levels' in role:
        old_level = role['skill_levels'].get(str(skill_id))
        if old_level is not None:
            try:
                level = int(old_level)
                # Clamp to valid range
                skill = settings.sect_registry.skill(skill_id)
                if skill:
                    max_level = skill.max_level
                    return max(0, min(level, max_level))
                return max(0, level)
            except (TypeError, ValueError):
                pass
    
    # Use default level from registry if available
    skill = settings.sect_registry.skill(skill_id)
    if skill is not None:
        return max(0, min(skill.default_level, skill.max_level))
    
    return 0

def sect_skill_request_frames(
    role: dict[str, object],
    values: list[object],
    settings: Settings,
) -> tuple[bytes, ...]:
    from systems.role.protocol import sect_skill_detail_frame, sect_skill_list
    """Handle the confirmed native sect-skill request actions."""
    if not values:
        return (encode_frame(1103, [byte(3)]),)
    action = int(values[0])
    if action == 6:
        return (sect_skill_list(role, settings),)

    skill_id = int(values[1]) if len(values) > 1 else 0
    sect_id = normalized_sect_id(role, settings.sect_registry)
    skill = settings.sect_registry.skill(skill_id)

    if action == 2:
        return (sect_skill_detail_frame(role, skill_id, settings),)

    if action == 3:
        # Learn/upgrade skill
        if skill is None or not settings.sect_registry.skill_belongs_to_sect(skill_id, sect_id):
            LOG.warning(
                'SECT_SKILL_LEARN_REJECT role_id=%s sect_id=%d skill_id=%d reason=invalid_skill',
                role.get('id', 0), sect_id, skill_id,
            )
            return (encode_frame(1103, [byte(3)]),)

        current_level = _get_sect_skill_level(role, skill_id, settings)
        if current_level >= skill.max_level:
            LOG.info(
                'SECT_SKILL_LEARN_MAX_LEVEL role_id=%s skill_id=%d level=%d max_level=%d',
                role.get('id', 0), skill_id, current_level, skill.max_level,
            )
            return (
                sect_skill_list(role, settings),
                encode_frame(1103, [byte(5)]),
            )

        # Perform the upgrade
        new_level = current_level + 1

        # Use new sect_skills format
        if 'sect_skills' not in role:
            role['sect_skills'] = {}
        role['sect_skills'][str(skill_id)] = {'level': new_level}

        # Migrate old skill_levels format if needed
        if 'skill_levels' in role:
            role['skill_levels'][str(skill_id)] = new_level

        LOG.info(
            'SECT_SKILL_LEARN role_id=%s sect_id=%d skill_id=%d level=%d->%d',
            role.get('id', 0), sect_id, skill_id, current_level, new_level,
        )

        # Action 0 replaces the record in b/y by skill id; action 5 redraws
        # the native sect page.  1132 keeps the character skill container in
        # sync for the battle/person screens.
        return (
            sect_skill_list(role, settings),
            encode_frame(1103, [byte(5)]),
        )

    # Action 3 is a native no-op response.  It still passes through main/e's
    # dispatcher and clears the global wait flag for stale/invalid requests.
    return (encode_frame(1103, [byte(3)]),)

def initial_skill_frames(role: dict[str, object], settings: Settings) -> tuple[bytes, bytes]:
    from systems.role.protocol import sect_skill_list
    from systems.skill.protocol import life_skill_list_frame
    """Preload both skill containers before their native pages are opened."""
    return life_skill_list_frame(role, settings), sect_skill_list(role, settings)

def role_entry_frames(settings: Settings, role: dict[str, object]) -> tuple[bytes, ...]:
    from systems.role.protocol import (
        character_extension_info, player_info, sect_skill_list,
    )
    from systems.skill.protocol import (
        gather_catalog_frame, gather_spawn_frame, life_skill_list_frame,
    )
    """Frames required after selecting or creating a role, before map init."""
    role_map_id = int(role.get('map_id', settings.default_map_id))
    gather_targets = settings.life_registry.gather_targets_for(role_map_id)
    return (
        player_info(settings, role),
        character_extension_info(),
        life_skill_list_frame(role, settings),
        sect_skill_list(role, settings),
        *(item_frame(item) for item in role_items(role) if item.get('location', 'bag') != 'consignment'),
        gather_catalog_frame(gather_targets),
        *(gather_spawn_frame(target) for target in gather_targets),
    )

def level_experience_required(level: int) -> int:
    """Return the deterministic local EXP cost for the next level."""
    return max(100, max(1, int(level)) * 100)


def role_level_properties(role: dict[str, object]) -> dict[int, int]:
    """Return the level-dependent properties shown by the APK character UI."""
    level = max(1, min(MAX_ROLE_LEVEL, int(role.get('level', 1))))
    raw_stats = [int(value) for value in list(role.get('stats', []))]
    base_stats = [max(0, value) for value in (raw_stats + [10, 10, 10, 10, 10])[:5]]
    max_hp = fuyuan.hp_limit(role, 100 + ((level - 1) * 10) + base_stats[1])
    max_mp = 50 + ((level - 1) * 5) + base_stats[2]
    return {
        11: level,
        31: max(0, int(role.get('experience', 0))),
        32: level_experience_required(level),
        40: max_hp,
        41: max_hp,
        42: max_mp,
        43: max_mp,
        **{property_index: value for property_index, value in enumerate(base_stats, start=44)},
        80: level,
        # ``main/e.O`` treats 85/86 as the high-word refresh for the 64-bit
        # experience fields 31/32.  The low words remain in 31/32; keeping
        # both halves in the frame mirrors the APK's incremental update path.
        85: max(0, int(role.get('experience', 0))) >> 32,
        86: level_experience_required(level) >> 32,
    }

def apply_one_level(role: dict[str, object]) -> bool:
    """Consume EXP for one level and persist deterministic base-stat growth."""
    level = max(1, int(role.get('level', 1)))
    experience = max(0, int(role.get('experience', 0)))
    if level >= MAX_ROLE_LEVEL or experience < level_experience_required(level):
        return False
    role['experience'] = experience - level_experience_required(level)
    role['level'] = level + 1
    raw_stats = [int(value) for value in list(role.get('stats', []))]
    base_stats = (raw_stats + [0] * 8)[:8]
    for index in range(5):
        base_stats[index] += LEVEL_BASE_STAT_GAIN
    role['stats'] = base_stats
    return True

def build_character_update_bus() -> CharacterUpdateBus:
    from systems.inventory.service import is_role_item_equipped
    from systems.role.protocol import (
        character_equipment_refresh_frames, equipment_panel_refresh_frame,
    )
    """Bind the generic update bus to the server's verified refresh builders."""
    return CharacterUpdateBus(
        build_full_refresh=character_equipment_refresh_frames,
        build_appearance_refresh=lambda role, registry: (
            equipment_panel_refresh_frame(role, registry),
        ),
        is_item_equipped=is_role_item_equipped,
    )
