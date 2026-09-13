"""帮派系统：1107/1136/1137/1140 帮派协议。

入口对象从 systems.gang.handler 导入，避免包初始化期的循环导入。
"""

from systems.gang.handler import GangSystem, register_gang_routes

__all__ = ['GangSystem', 'register_gang_routes']
