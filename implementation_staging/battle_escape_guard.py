"""Compatibility wrapper for the consolidated battle-state escape policy.

New code should import from :mod:`battle.state`. This module remains during the
migration so the active launcher and existing tests keep their public imports.
"""

from battle.state import (
    CONTACT_RADIUS_TILES,
    RETRIGGER_TIMEOUT_SECONDS,
    guard_timed_out as timed_out,
    movement_outside_guard_radius,
    should_suppress_guard as should_suppress,
    stamp_guard,
)

__all__ = [
    'CONTACT_RADIUS_TILES',
    'RETRIGGER_TIMEOUT_SECONDS',
    'movement_outside_guard_radius',
    'should_suppress',
    'stamp_guard',
    'timed_out',
]
