"""Gang system static catalog and constants.

The values here mirror the APK client (``pmsj.work.e.cx/ed/ef/ec/ee`` and
``pmsj.work.b.v``) as audited from the decoded smali:

- gang protocol command ``0x453`` (1107) with short sub-commands,
- gang list ``0x470`` (1136), member list/detail ``0x471`` (1137) and
  application list ``0x474`` (1140),
- gang position codes consumed by ``b/v.w(I)``: 1000 帮主, 200 帮众,
- self gang position published through the 1006 property table at slot 21
  (``b/v.W()`` reads player record field ``0x15``).
"""

from __future__ import annotations

GANG_COMMAND = 1107
GANG_LIST_COMMAND = 1136
MEMBER_LIST_COMMAND = 1137
APPLICATION_LIST_COMMAND = 1140

GANG_MESSAGE_IDS = (GANG_COMMAND, GANG_LIST_COMMAND, MEMBER_LIST_COMMAND, APPLICATION_LIST_COMMAND)

SUB_GANG_INFO = 0x0B
SUB_LEAVE = 0x03
SUB_KICK = 0x04
SUB_ABDICATE = 0x10
SUB_REJECT_INVITE = 0x19
SUB_REJECT_APPLICATION = 0x1A
SUB_APPLY = 0x1B
SUB_ACCEPT_APPLICATION = 0x1C
SUB_INVITE = 0x1D
SUB_ACCEPT_INVITE = 0x1E
SUB_MODIFY_MOTTO = 0x1F

GANG_POSITION_NONE = 0
GANG_POSITION_MEMBER = 0xC8
GANG_POSITION_LEADER = 0x3E8

# 1006/1017 property slot holding the player's own gang position.
GANG_POSITION_PROPERTY = 21

MAX_GANG_NAME_LENGTH = 12
MAX_MOTTO_LENGTH = 60
MAX_GANG_MEMBERS = 50
MAX_PENDING_APPLICATIONS = 30

FIRST_GANG_ID = 2001

# --- 帮派管理员 NPC（长安 12,68，外观 96020）---
GANG_ADMIN_SERVICE = 'gang_admin'
GANG_ADMIN_NPC_ID = 1900005
# 2032 对话选项：创建帮派走 kind 3 记录（客户端原生输入框），
# 解散帮派走两步确认（先回发确认对话，再收确认选项）。
GANG_ADMIN_CREATE_OPTION = 1
GANG_ADMIN_DISBAND_OPTION = 2
GANG_ADMIN_DISBAND_CONFIRM_OPTION = 3
GANG_CREATION_COST_SILVER = 10000
# 1006/1017 货币属性槽：50 = 银两。
SILVER_CURRENCY_PROPERTY = 50


class GangSeedDefinition:
    """A starter gang published on the 1136 list for empty servers."""

    def __init__(self, name: str, motto: str) -> None:
        self.name = name
        self.motto = motto


DEFAULT_GANG_SEEDS = (
    GangSeedDefinition('天罡盟', '替天行道，护佑苍生'),
    GangSeedDefinition('玄水阁', '上善若水，厚德载物'),
    GangSeedDefinition('落霞山庄', '落霞与孤鹜齐飞'),
)
