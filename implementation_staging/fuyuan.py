"""Local 福缘 rules and APK-native 1054 screen (338/ak) protocol.

ak.smali: j() requests BYTE 0/page/size; a(w) consumes five-field rows;
b(String) sends BYTE 2, INT 338, BYTE 0, INT row_id, BYTE menu_index.
main/e.v routes actions 0..6 to the existing screen, 7 resets an effect,
8 belongs to logout and is deliberately excluded from this module.
"""
from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from pathlib import Path

from protocol import Field, TYPE_BYTE, TYPE_INT, byte, integer, string, encode_frame

MAX_POINTS = 2_000_000_000


def load_catalog(path: Path | None = None) -> dict:
    path = path or Path(__file__).with_name('data') / 'fuyuan.json'
    data = json.loads(path.read_text(encoding='utf-8'))
    for key in ('initial_points', 'silver_per_point', 'quote_lifetime_seconds'):
        value = data[key]
        if type(value) is not int or not 0 <= value <= MAX_POINTS:
            raise ValueError(f'invalid fuyuan {key}')
    if not data['silver_per_point'] or not data['quote_lifetime_seconds']:
        raise ValueError('fuyuan price and quote lifetime must be positive')
    packages = data['topup_packages']
    if not isinstance(packages, list) or not 1 <= len(packages) <= 20:
        raise ValueError('invalid fuyuan topup packages')
    if any(type(p) is not int or not 0 < p <= MAX_POINTS for p in packages):
        raise ValueError('invalid fuyuan package points')
    rows = data['benefits']
    if not isinstance(rows, list) or not 1 <= len(rows) <= 100:
        raise ValueError('invalid fuyuan benefits')
    ids = set()
    for row in rows:
        if type(row['id']) is not int or not 0 < row['id'] < 1000 or row['id'] in ids:
            raise ValueError('invalid/duplicate fuyuan benefit id')
        ids.add(row['id'])
        if type(row['tier']) is not int or row['tier'] not in (1, 2, 3):
            raise ValueError('invalid fuyuan benefit tier')
        if type(row['implemented']) is not bool:
            raise ValueError('invalid fuyuan benefit state')
        if any(not isinstance(row[key], str) or not row[key] for key in ('name', 'description')):
            raise ValueError('invalid fuyuan benefit text')
    return data


CATALOG = load_catalog()


def _nonnegative(value: object, default: int = 0) -> int:
    try:
        return max(0, min(MAX_POINTS, int(value)))
    except (ValueError, TypeError, OverflowError):
        return default


def _now(now: int | None) -> int:
    return int(time.time()) if now is None else int(now)


def ensure_state(role: dict, *, now: int | None = None) -> bool:
    """One-time grant only when absent; malformed existing states get no grant."""
    timestamp = _now(now)
    absent = 'fuyuan' not in role
    state = role.get('fuyuan')
    if not isinstance(state, dict):
        state = {}
    normalized = dict(state)
    normalized.update(
        version=1,
        points=_nonnegative(state.get('points', CATALOG['initial_points'] if absent else 0)),
        settled_at=_nonnegative(state.get('settled_at'), timestamp),
        purchased_points=_nonnegative(state.get('purchased_points')),
        claims=state.get('claims') if isinstance(state.get('claims'), dict) else {},
    )
    if 'settled_at' not in state:
        normalized['settled_at'] = timestamp
    if absent or normalized != role.get('fuyuan'):
        role['fuyuan'] = normalized
        return True
    return False


def remaining_points(role: dict, *, now: int | None = None) -> int:
    state = role.get('fuyuan')
    if not isinstance(state, dict):
        return 0
    timestamp = _now(now)
    elapsed = max(0, timestamp - int(state.get('settled_at', timestamp))) // 60
    return max(0, _nonnegative(state.get('points')) - elapsed)


def tier_for_points(points: int) -> int:
    return 3 if points > 15000 else 2 if points > 5000 else 1 if points > 0 else 0


def tier(role: dict, *, now: int | None = None) -> int:
    return tier_for_points(remaining_points(role, now=now))


def settle(role: dict, *, now: int | None = None) -> bool:
    timestamp = _now(now)
    changed = ensure_state(role, now=timestamp)
    state = role['fuyuan']
    elapsed = max(0, timestamp - state['settled_at']) // 60
    if elapsed and state['points']:
        state['points'] = max(0, state['points'] - elapsed)
        state['settled_at'] += elapsed * 60
        return True
    return changed


def experience_reward(role: dict, base: int) -> int:
    base = max(0, int(base))
    return base * 105 // 100 if tier(role) >= 1 else base


def hp_limit(role: dict, base: int) -> int:
    return base * 120 // 100 if tier(role) >= 2 else base


def capacity_bonus(role: dict) -> int:
    return 20 if tier(role) >= 3 else 0


def status_text(role: dict, *, now: int | None = None) -> str:
    points = remaining_points(role, now=now)
    grade = tier_for_points(points)
    return f'福缘{grade}阶  剩余{points}点（约{points // 60}小时{points % 60}分）'


def status_frame(role: dict, text: str = '', *, now: int | None = None) -> bytes:
    return encode_frame(1054, [byte(1), string(status_text(role, now=now) + ('_' + text if text else ''))])


def list_frame(rows: list, *, title: str = '福缘系统', page: int = 0, size: int = 20) -> bytes:
    # d/i.c() is a zero-based page cursor, d() is the requested page size.
    size = max(1, min(100, size))
    selected = rows[page * size:(page + 1) * size]
    fields = [byte(0), string(title), byte(len(rows)), byte(len(selected))]
    for row in selected:
        fields.extend([integer(row['id']), string(row['name']), integer(row['tier']),
                       string(row['menu']), string(row['description'])])
    return encode_frame(1054, fields)


def _matches(fields: list[Field], action: int, types: tuple[int, ...]) -> bool:
    return (len(fields) == len(types) and tuple(f.type_id for f in fields) == types
            and fields[0].value == action)


@dataclass
class FuyuanSession:
    """Quotes belong to one connection/role, are consumed once, never trusted from wire."""
    quotes: dict = field(default_factory=dict)
    next_id: int = 1000
    rows: list = field(default_factory=list)

    def _overview(self, role: dict, text: str = '', *, now: int) -> list[bytes]:
        self.quotes.clear()
        self.rows = []
        for entry in CATALOG['benefits']:
            row = dict(entry)
            state = '自动生效' if tier(role, now=now) >= row['tier'] else '未达等阶'
            if not row['implemented']:
                state = '尚未开放'
            row.update(name=f'{row["name"]}（{state}）', menu='查看说明')
            self.rows.append(row)
        return [encode_frame(1054, [byte(6)]), status_frame(role, text, now=now), list_frame(self.rows)]

    def _offers(self, role: dict, *, upgrade: bool, now: int) -> list[bytes]:
        self.quotes.clear()
        self.rows = []
        points = remaining_points(role, now=now)
        targets = [n for n in (5001, 15001) if n > points] if upgrade else CATALOG['topup_packages']
        for target in targets:
            amount = target - points if upgrade else target
            if points + amount > MAX_POINTS:
                continue
            cost = amount * CATALOG['silver_per_point']
            self.next_id += 1
            row_id = self.next_id
            self.quotes[row_id] = dict(role_id=role['id'], points=amount, cost=cost,
                                      expires=now+CATALOG['quote_lifetime_seconds'], target=target if upgrade else 0)
            label = f'升至{tier_for_points(target)}阶' if upgrade else f'补充{amount}点'
            self.rows.append(dict(id=row_id, tier=0, name=f'{label}：{cost}银两',
                menu='确认购买_取消', description=f'{label}，补充{amount}点，花费{cost}银两。_点击此行后选择确认购买才会扣款。_此为本地服价格。'))
        if not self.rows:
            return self._overview(role, '已达到目标等阶或福缘值上限。', now=now)
        return [encode_frame(1054,[byte(6)]), status_frame(role,'请选择套餐，再确认购买。',now=now),
                list_frame(self.rows,title='快捷升阶' if upgrade else '补充福缘')]

    def handle(self, role: dict, fields: list[Field], *, now: int | None = None) -> list[bytes]:
        timestamp = _now(now)
        if _matches(fields, 0, (TYPE_BYTE, TYPE_BYTE, TYPE_BYTE)):
            page, size = int(fields[1].value), int(fields[2].value)
            if page < 0 or size <= 0:
                return [status_frame(role,'无效分页参数。',now=timestamp)]
            if page == 0 or not self.rows:
                replies = self._overview(role, now=timestamp)
                replies[-1] = list_frame(self.rows,page=page,size=size)
                return replies
            return [status_frame(role,now=timestamp),list_frame(self.rows,page=page,size=size)]
        if _matches(fields, 3, (TYPE_BYTE, TYPE_INT)):
            row_id = int(fields[1].value)
            row = next((r for r in self.rows if r['id']==row_id), None)
            row = row or next((r for r in CATALOG['benefits'] if r['id']==row_id), None)
            text = row['description'] if row else '内容已失效，请重新打开福缘。'
            return [encode_frame(1054,[byte(3),integer(row_id),string(text)])]
        if _matches(fields, 4, (TYPE_BYTE,)) or _matches(fields, 5, (TYPE_BYTE,)):
            settle(role, now=timestamp)
            return self._offers(role, upgrade=fields[0].value==5, now=timestamp)
        if not _matches(fields, 2, (TYPE_BYTE,TYPE_INT,TYPE_BYTE,TYPE_INT,TYPE_BYTE)):
            return []
        if fields[1].value != 338 or fields[2].value != 0:
            return []
        row_id, selection = int(fields[3].value), int(fields[4].value)
        if selection not in (0,1):
            return [status_frame(role,'无效选项。',now=timestamp)]
        quote = self.quotes.pop(row_id, None)
        if quote is None:
            entry = next((r for r in CATALOG['benefits'] if r['id']==row_id), None)
            return [status_frame(role,entry['description'] if entry else '操作已失效，请重新选择。',now=timestamp)]
        if selection == 1:
            return self._overview(role,'已取消，未扣除银两。',now=timestamp)
        settle(role, now=timestamp)
        state = role['fuyuan']
        if quote['role_id'] != role['id'] or timestamp > quote['expires']:
            return self._overview(role,'报价已失效，请重新选择。',now=timestamp)
        if quote['target'] and state['points'] + quote['points'] < quote['target']:
            return self._overview(role,'剩余福缘已变化，请重新选择快捷升阶以确认最新价格。',now=timestamp)
        currencies = role.get('currencies', {})
        balance = _nonnegative(currencies.get('silver')) if isinstance(currencies,dict) else 0
        if balance < quote['cost'] or state['points'] + quote['points'] > MAX_POINTS:
            return self._overview(role,'银两不足或福缘值超出上限，未扣款。',now=timestamp)
        currencies['silver'] = balance - quote['cost']
        if state['points'] == 0:
            state['settled_at'] = timestamp
        state['points'] += quote['points']
        state['purchased_points'] = min(MAX_POINTS,state['purchased_points']+quote['points'])
        return self._overview(role,f'补充成功：增加{quote["points"]}点，扣除{quote["cost"]}银两。',now=timestamp)
