\
"""Regression coverage for the APK six-field 1143/action-5 direct-use path."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from protocol import byte, decode_frame, encode_frame, field_values, integer
from server import (
    LocalGameServer,
    Settings,
    default_role,
    ensure_life_skills,
    is_life_direct_use_request,
    life_vitality,
    role_items,
)


ALCHEMY_SKILL_ID = 2003
REFINE_RECIPE_ID = 4001
INITIAL_STONE_TEMPLATE_ID = 322_260_000
POTION_TEMPLATE_ID = 260_000_001


def quantity_for(role: dict[str, object], template_id: int) -> int:
    return sum(
        int(item.get('quantity', 0))
        for item in role_items(role)
        if int(item.get('template_id', 0)) == template_id
        and item.get('location', 'bag') == 'bag'
    )


class LifeSkillDirectUseTests(unittest.TestCase):
    def test_direct_use_executes_one_authoritative_craft(self):
        with tempfile.TemporaryDirectory() as directory:
            settings = Settings(role_data_file=str(Path(directory) / 'roles.json'))
            server = LocalGameServer(settings)
            role = default_role(settings)
            state = ensure_life_skills(role, settings.life_registry)
            state['skills'][str(ALCHEMY_SKILL_ID)] = {
                'level': 1,
                'proficiency': 0,
            }
            state['learned_recipes'] = [REFINE_RECIPE_ID]

            stones_before = quantity_for(role, INITIAL_STONE_TEMPLATE_ID)
            potion_before = quantity_for(role, POTION_TEMPLATE_ID)
            vitality_before = life_vitality(role)

            fields = decode_frame(encode_frame(1143, [
                byte(5),
                integer(REFINE_RECIPE_ID),
                integer(0), integer(0), integer(0), integer(0),
            ]))[1]
            self.assertTrue(is_life_direct_use_request(fields))

            result = server.handle_life_craft(role, fields)

            self.assertTrue(result.changed, result.reason)
            self.assertEqual(
                quantity_for(role, INITIAL_STONE_TEMPLATE_ID),
                stones_before - 3,
            )
            self.assertEqual(
                quantity_for(role, POTION_TEMPLATE_ID),
                potion_before + 1,
            )
            self.assertEqual(life_vitality(role), vitality_before - 10)
            message_id, ack_fields = decode_frame(result.frames[-1])
            self.assertEqual(message_id, 1143)
            self.assertEqual(field_values(ack_fields), [5])


if __name__ == '__main__':
    unittest.main()
