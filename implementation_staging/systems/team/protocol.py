"""APK-confirmed team frames. Data changes never use map movement messages."""
from __future__ import annotations

from protocol import byte, encode_frame, integer, short, string
from systems.role.protocol import character_appearance_frame
from systems.map.protocol import player_actor_object_id

TEAM_LEADER_FLAG = 0x40


def invite_frame(role_id: int, name: str, level: int, sect_id: int) -> bytes:
    return encode_frame(1023, [
        short(2), integer(int(role_id)), string(str(name)),
        short(max(1, int(level))), byte(int(sect_id)),
    ])


def member_frame(name: str, entry_id: int, hp: int, mp: int,
                 level: int, sect_id: int) -> bytes:
    """1026/0 appends one roster row to APK aa.a (role IDs, not map actors).

    e.aj pswitch_e 把 fields[2:] 整段作为一行加入 aa.a，行结构由消费方
    反推锁定（e/et 成员页、e.aj 的 1017 属性 40-43 回写列）：

        row[0] string 名字（成员页第 2 列）
        row[1] int    条目 id（aa.a([row])I / et 菜单 / m.o 查找键）——
                  本机自己的行 = raw role id，他人行 = actor id（b/m.o 语义）
        row[2] int    当前 MP（1017 prop 41 回写）
        row[3] int    当前 HP（1017 prop 40 回写）
        row[4] int    门派 id（成员页第 3 列 → b/v.v(I) 门派名）
        row[5] int    等级（成员页第 4 列）
        row[6] int    MP 上限（1017 prop 42 回写）
        row[7] int    HP 上限（1017 prop 43 回写）
        row[8] int    标志（bit0=暂离；et 状态列）

    field 1 是被 e.aj 跳过的占位（可以是任意字段）；行元素绝对不能
    以 byte 计数开头——旧实现把 byte(1) 留在行首，导致 row[0] 不是
    名字、id 查找/暂离标志全部错位，成员页呈"无队伍"。
    """
    return encode_frame(1026, [
        byte(0), byte(1),
        string(str(name)),
        integer(int(entry_id)),
        integer(max(0, int(mp))),
        integer(max(0, int(hp))),
        byte(int(sect_id)),
        integer(max(1, int(level))),
        integer(max(0, int(mp))),
        integer(max(0, int(hp))),
        integer(0),
    ])


def leader_flag_frame(role_id: int, enabled: bool) -> bytes:
    return character_appearance_frame(int(role_id), {0: TEAM_LEADER_FLAG if enabled else 0})


# prop0 队员位：主菜单"队伍"项按 b/v.Z()（0x40 队长）|| b/v.aa()（0x200000 队员）
# 决定打开成员花名册页（0x5c）还是"尚未组队"帮助页（0x5b，e/ep）。
TEAM_MEMBER_FLAG = 0x200000


def team_role_flag_frame(role_id: int, is_leader: bool) -> bytes:
    """1017 {prop0}：队长=0x40，队员=0x200000（b/v.Z()/b/v.aa() 的判定位）。"""
    flag = TEAM_LEADER_FLAG if is_leader else TEAM_MEMBER_FLAG
    return character_appearance_frame(int(role_id), {0: flag})


def member_state_frame(action: int, role_id: int) -> bytes:
    return encode_frame(1023, [short(int(action)), integer(int(role_id))])


def member_removed_frame(role_id: int) -> bytes:
    return encode_frame(1023, [short(1), integer(int(role_id))])


def disband_frame() -> bytes:
    return encode_frame(1023, [short(11)])


# 跟随链消息：0x40e → main/e.ai。1028（0x404）不在 APK 主接收分发表中，
# 发 1028 会被客户端静默丢弃——这是"队员不跟随"的根因。
FOLLOW_CHAIN_MESSAGE_ID = 1038


def follow_chain_frame(
    leader_id: int,
    viewer_id: int,
    member_ids: list[int],
    x: int,
    y: int,
) -> bytes:
    """S→C 1038（e.ai）：重建跟随链并命令链头走位，一帧完成。

    e.ai 读取 c(0)=链头 id、a(5)=链员数(byte)、d(6+i)=链员 id、
    d(3)/d(4)=落点：链头置 H=true，逐个链员 E() 停走并按序 a(n) 挂链
    （头.J=员1，员1.J=员2……尾.J=null），最后 b(x,y,false) 走位；
    本地玩家是链头且正在移动时只挂链不走位。

    id 语义（b/m.o(I) 的查找规则决定）：**本地玩家匹配 raw role id，
    其他玩家匹配 actor id（1_000_000+role_id，即 1014/1005 的对象键）**。
    因此每个接收方收到的帧必须按自己定制：队长客户端的链头用队长
    raw id、链员用 actor id；队员客户端的链头用队长 actor id、
    自己放链表首位用 raw id、其余链员用 actor id。
    """
    def entry(other_id: int) -> int:
        return int(other_id) if int(other_id) == int(viewer_id) else player_actor_object_id(other_id)

    fields = [
        integer(entry(leader_id)),
        integer(0),
        integer(0),
        integer(int(x)),
        integer(int(y)),
        byte(len(member_ids)),
    ]
    fields.extend(integer(entry(member_id)) for member_id in member_ids)
    return encode_frame(FOLLOW_CHAIN_MESSAGE_ID, fields)
