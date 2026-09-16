"""social 系统协议帧构造。

所有帧的字段下标都来自 APK 反编译证据（pmsj/work/main/e.smali 主分发器与
对应界面类），见 docs/protocol/15-玩家交互协议.md。方向均为 S→C。
"""
from __future__ import annotations

from protocol import byte, encode_frame, integer, short, string
from systems.inventory.protocol import (
    is_equipment, item_display_name, role_items,
)
from systems.inventory.registry import default_item_registry

# 聊天频道：0x7de=2014 私聊（C→S 带对方名字，定向转发）。
CHAT_CHANNEL_PRIVATE = 2014


def _default_title(value: object) -> str:
    text = str(value or '').strip()
    return text if text else '无'


def player_view_frame(settings, role: dict[str, object], actor_id: int) -> bytes:
    """S→C 1303/action=1：更新地图上已有的 b/v 并打开查看面板（e/ey pswitch_11）。

    地图菜单的"查看"目标一定在查看者视野内（m.n(actor_id) 可命中），因此
    使用动作 1：客户端直接复用该 b/v 已有的 1014 属性表渲染面板，服务端只
    需补齐面板专属属性与装备列表。字段布局（e/ey.a pswitch_11）：

        0: byte action=1
        1: int 对方 actor id（m.n 查找键）
        2: string prop54（配偶）
        3: string prop75（人气）
        4: int 已装备数量 N
        5..: 每件装备 6 个字段
        末尾: string prop79（师傅）+ int prop84（斗法排名，0=未上榜）

    每件装备字段（e/ey.a(w,4) 辅助函数）：
        [int 模板, byte 槽位, string 名字, int 图标, int 实例 id, short 数量]
    槽位字节决定装备落在面板哪个格子（ag() 用 0x17700+k 定位）。
    """
    level = max(1, int(role.get('level', 1)))
    equips = [
        item for item in role_items(role)
        if item.get('location') == 'equipped' and is_equipment(item)
    ]
    registry = settings.item_registry or default_item_registry()
    fields = [
        byte(1),
        integer(int(actor_id)),
        string(_default_title(role.get('spouse'))),
        string(str(role.get('popularity', 0) or 0)),
        integer(len(equips)),
    ]
    for item in equips:
        resolved = registry.resolve(item)
        fields.extend([
            integer(int(resolved.get('template_id', 0))),
            byte(int(resolved.get('equipment_slot', 0))),
            string(item_display_name(resolved)),
            integer(int(resolved.get('icon_code', 0))),
            integer(int(item.get('id', 0))),
            short(int(item.get('quantity', 1))),
        ])
    fields.append(string(_default_title(role.get('master'))))
    fields.append(integer(0))
    return encode_frame(1303, fields)


def character_view_rows_frame(columns: list[tuple[int, int]] | None = None) -> bytes:
    """S→C 1089/action=2：e/ey.b(w) 查看面板附加列。

    帧布局 `[byte 2, int 0, byte N, int...]`（N=列数）：
        - field 2 为列数（byte），客户端 `rows=(字段总数-3)/columns`；
        - 之后每列 2 个 int：数字图标图集下标、数值（>0 绿 / ≤0 黄）。
        每列恰 2 值，故字段总数为 3+2N。
    APK 证据：ey.smali `b(w)`(1758) + `k()`(674)、a/c/x.smali `a(IIw)`(2138)，
    证据等级 B 级（见 docs/development/APK_VERIFICATION_1089_ACTION2.md v1.1）。

    columns 为空（None/[]）时输出 `[byte 2, int 0, byte 0]`，客户端 0 行刷新，
    保持既有安全默认（属性→图标映射仍为 C 级，内容由上层配置决定）。
    """
    columns = columns or []
    fields: list[object] = [byte(2), integer(0), byte(len(columns))]
    for icon, value in columns:
        fields.extend([integer(int(icon)), integer(int(value))])
    return encode_frame(1089, fields)


# ---------------------------------------------------------------------------
# 好友（1019）
# ---------------------------------------------------------------------------
def friend_request_prompt_frame(
    from_role_id: int,
    from_name: str,
    from_level: int,
) -> bytes:
    """S→C 1019/10：e.ah pswitch_f9 "XX请求加您为好友" 确认框。

    e.ah 读取 c(1)=role_id、e(2)=名字、b(3)=short、c(4)=int；确定/拒绝分别
    回发 1019/11 与 1019/20（携带同一个 role_id）。
    """
    return encode_frame(1019, [
        byte(10),
        integer(int(from_role_id)),
        string(str(from_name)),
        short(max(1, int(from_level))),
        integer(0),
    ])


def friend_list_frame(friends: list[dict[str, object]], online_ids: set[int], level_of) -> bytes:
    """S→C 1019/15：好友列表，e.ah pswitch_5c 按 5 字段一行解析。

    每行 [int role_id, string 名字, int 在线(1/0), int 等级, int 0]；
    e.ah 动作 12 会把 row[2] 置为在线标记，因此第 3 个字段必须是 int。
    """
    rows = []
    for friend in friends:
        role_id = int(friend.get('id', 0))
        rows.extend([
            integer(role_id),
            string(str(friend.get('name', ''))),
            integer(1 if role_id in online_ids else 0),
            integer(max(1, int(level_of(role_id)))),
            integer(0),
        ])
    return encode_frame(1019, [byte(15), byte(len(rows) // 5), *rows])


def empty_enemy_list_frame() -> bytes:
    """S→C 1019/28：仇人列表（本地服恒为空，保持客户端 f.h 初始化）。"""
    return encode_frame(1019, [byte(28), byte(0)])


# ---------------------------------------------------------------------------
# 交易（1056）
# ---------------------------------------------------------------------------
def trade_request_frame(from_actor_id: int, from_name: str) -> bytes:
    """S→C 1056/1：e.sswitch_ad8 pswitch_ae4 "请求交易,是否接受?" 确认框。

    e.ah 读取 c(1)=发起人 actor id（接受后原样回发 1056/2）、e(3)=名字；
    字段 2 必须存在，否则 e(3) 越界异常。
    """
    return encode_frame(1056, [
        byte(1),
        integer(int(from_actor_id)),
        integer(0),
        string(str(from_name)),
    ])


def trade_open_frame(other_actor_id: int) -> bytes:
    """S→C 1056/5：打开交易窗口 e/eu（标题 "交易 <对方名字>"）。

    e/eu.a 动作 5 读取 c(1)=对方 actor id、d(2)/d(3)=双方暂存格数。
    """
    return encode_frame(1056, [byte(5), integer(int(other_actor_id)), integer(0), integer(0)])


def trade_peer_money_frame(amount: int) -> bytes:
    """S→C 1056/6：e/eu pswitch_112 显示 "银:<n>"（对方锁定金额）。"""
    return encode_frame(1056, [byte(6), integer(max(0, int(amount)))])


def trade_peer_items_frame(items: list[tuple[int, int, str, int, int, int]]) -> bytes:
    """S→C 1056/8：e/eu pswitch_a7 对方锁定物品行（图标网格）。

    每件物品 6 个字段（e/eu.a pswitch_a7 逐字段读取）：
        [int 实例 id(u 构造 + 行1), byte 槽位(行2), int 模板(行3),
         int 数量(行4), int 保留(行5), int 图标(行8→a/c/x.e 贴图)]
    """
    fields = [byte(8), byte(len(items))]
    for instance_id, template_id, name, icon, quantity, slot in items:
        fields.extend([
            integer(int(instance_id)),
            byte(int(slot)),
            integer(int(template_id)),
            integer(max(0, int(quantity))),
            integer(0),
            integer(max(0, int(icon))),
        ])
    return encode_frame(1056, fields)


def trade_enable_confirm_frame() -> bytes:
    """S→C 1056/10：e/eu pswitch_138 启用确认按钮（"对方已锁定"）。

    e/eu.c() 初始化时 0x3e92 确认按钮为禁用；仅在本帧到达后可点击，
    点击后客户端发送 C→S 1056/10 作为最终确认。
    """
    return encode_frame(1056, [byte(10)])


def trade_complete_frame() -> bytes:
    """S→C 1056/20：e/eu pswitch_134 置 ag 完成标记（结算后冻结窗口输入）。"""
    return encode_frame(1056, [byte(20)])


def trade_close_frames() -> tuple[bytes, ...]:
    """S→C 1056/11,12：e.sswitch pswitch_b66 关闭背包选择页与交易窗口。"""
    return (encode_frame(1056, [byte(11)]), encode_frame(1056, [byte(12)]))


# ---------------------------------------------------------------------------
# 聊天（1004）
# ---------------------------------------------------------------------------
def chat_frame(channel: int, speaker: str, target: str, text: str) -> bytes:
    """S→C 1004：e.sswitch_474 → main/d.a(S,String,String,String) 渲染。

    客户端读取 b(1)=频道、e(4)=说话人（"*4 名字：*3 正文"）、e(5)=对象、
    e(6)=正文；字段 0..3 的类型与 C→S 保持一致。
    """
    return encode_frame(1004, [
        integer(0),
        short(int(channel)),
        short(0),
        integer(0),
        string(str(speaker)),
        string(str(target)),
        string(str(text)),
    ])


# ---------------------------------------------------------------------------
# 切磋（1157）/ PK（1158）
# ---------------------------------------------------------------------------
def spar_ack_frame(requester_actor_id: int, target_actor_id: int) -> bytes:
    """S→C 1157/1：e/cu 打开后自动回发 1157/4 [f1, f2] 作为对局确认。

    e/cu.a 未处于观战模式时读取 1..3 三个 int 字段，随即以
    w.a(0x485, 4, f1, f2) 应答并关窗——即目标客户端的隐式应答通道。
    """
    return encode_frame(1157, [
        byte(1),
        integer(int(requester_actor_id)),
        integer(int(target_actor_id)),
        integer(0),
    ])


def pk_request_prompt_frame(requester_actor_id: int) -> bytes:
    """S→C 1158：e.sswitch_e56 "确认要PK吗?" 确认框（确定→1158/6）。

    e.sswitch_e56 读取 c(2)=发起人 actor id 存入 main/e.d。
    """
    return encode_frame(1158, [byte(0), integer(0), integer(int(requester_actor_id))])
