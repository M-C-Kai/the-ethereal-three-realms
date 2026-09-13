"""福缘系统协议入口：1054 福缘页面与心跳结算。"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field

from app.context import SystemContext
from app.router import RouteResult, SystemRouter
from protocol import Field, TYPE_BYTE, TYPE_INT, byte, encode_frame, integer, string
from systems.fuyuan.protocol import fuyuan_update_frame, list_frame, status_frame
from systems.fuyuan.registry import CATALOG, MAX_POINTS
from systems.fuyuan.service import (
    _nonnegative, _now, remaining_points, settle, tier, tier_for_points,
)


LOG = logging.getLogger('piaomiao-local')


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


class FuyuanSystem:
    """fuyuan 系统边界：1054 福缘页面与周期结算。"""

    system_name = 'fuyuan'

    def __init__(self, save=None) -> None:
        self.save = save

    def can_handle(self, context: SystemContext, message_id: int, fields: list[object]) -> bool:
        if message_id != 1054:
            return False
        if not fields:
            return False
        # 登出页请求（BYTE 8）归角色系统；其余 1054 归福缘。
        from systems.role.protocol import is_logout_page_request
        return not is_logout_page_request(fields)

    def handle(self, context: SystemContext, message_id: int, fields: list[object]) -> RouteResult:
        role = context.active_role
        if role is None:
            return RouteResult.not_handled(reason='no_active_role')
        session = context.session
        fuyuan_session = session.get('fuyuan')
        if not isinstance(fuyuan_session, FuyuanSession):
            fuyuan_session = FuyuanSession()
            session['fuyuan'] = fuyuan_session
        before_fuyuan = role.get('fuyuan')
        replies = fuyuan_session.handle(role, fields)
        if replies and role.get('fuyuan') != before_fuyuan and self.save is not None:
            self.save()
        if replies:
            return RouteResult.handled((fuyuan_update_frame(role), *replies))
        return RouteResult.handled()

    def reset_session(self, context: SystemContext) -> None:
        """Quotes are connection/role scoped; drop them on role switch."""
        context.session['fuyuan'] = None

    def settle_and_frames(self, role: dict[str, object] | None) -> tuple[bytes, ...]:
        """Periodic settlement used by the heartbeat and the dispatch prelude."""
        if role is None or not settle(role):
            return ()
        if self.save is not None:
            self.save()
        return (fuyuan_update_frame(role), status_frame(role))


def register_fuyuan_routes(router: SystemRouter, system: FuyuanSystem) -> None:
    router.register(system.system_name, system.can_handle, system.handle)
