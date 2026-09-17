from systems.role.sect_skill_registry import default_sect_combat_skill_catalog


FORMAL_SECT_IDS = (1, 3, 5, 7, 9, 10, 11)


def test_catalog_loads_all_formal_sect_skills():
    catalog = default_sect_combat_skill_catalog()

    all_skills = [
        skill
        for sect_id in FORMAL_SECT_IDS
        for skill in catalog.skills_for_sect(sect_id, include_follow_up=True)
    ]

    assert len(all_skills) == 70
    assert len({skill.skill_id for skill in all_skills}) == 70


def test_public_sect_skill_listing_hides_follow_up_skills():
    catalog = default_sect_combat_skill_catalog()

    visible_shushan = catalog.skills_for_sect(7)
    all_shushan = catalog.skills_for_sect(7, include_follow_up=True)

    assert 10708 not in {skill.skill_id for skill in visible_shushan}
    assert 10709 not in {skill.skill_id for skill in visible_shushan}
    assert 10708 in {skill.skill_id for skill in all_shushan}
    assert 10709 in {skill.skill_id for skill in all_shushan}


def test_kunlun_thunder_is_two_target_magic_damage():
    catalog = default_sect_combat_skill_catalog()

    skill = catalog.skill(10101)
    cast_rule = catalog.cast_rule(10101)
    effects = catalog.effects_for(10101)

    assert skill is not None
    assert skill.name == '天雷轰'
    assert skill.damage_type == 'magic'
    assert cast_rule is not None
    assert cast_rule.target_type == 'random_multi'
    assert cast_rule.target_count == 2
    assert any(effect.effect_type == 'damage' and effect.rate_bp == 9000 for effect in effects)


def test_yaochi_revive_cannot_target_pet():
    catalog = default_sect_combat_skill_catalog()

    cast_rule = catalog.cast_rule(10305)
    effects = catalog.effects_for(10305)

    assert cast_rule is not None
    assert cast_rule.can_target_dead is True
    assert cast_rule.can_target_pet is False
    assert cast_rule.require_alive_target is False
    assert any(effect.effect_type == 'revive' and effect.flat_value == 228 for effect in effects)


def test_shushan_weapon_quality_scaling():
    catalog = default_sect_combat_skill_catalog()

    wan_jian_scaling = catalog.scaling_for(10703, 'weapon_quality')
    ren_jian_scaling = catalog.scaling_for(10704, 'weapon_quality')

    assert any(rule.condition_value == 'divine' and rule.target_count == 4 for rule in wan_jian_scaling)
    assert any(rule.condition_value == 'divine' and rule.damage_reduction_bp == 2000 for rule in ren_jian_scaling)


def test_xuanyuan_stances_are_mutually_exclusive():
    catalog = default_sect_combat_skill_catalog()

    gu_cheng = catalog.relations_for(10501, 'mutually_exclusive')
    chen_zhou = catalog.relations_for(10502, 'mutually_exclusive')

    assert any(rule.related_skill_id == 10502 for rule in gu_cheng)
    assert any(rule.related_skill_id == 10501 for rule in chen_zhou)


def test_biyou_poison_dot_cannot_kill():
    catalog = default_sect_combat_skill_catalog()

    poison_effects = catalog.effects_for(10901) + catalog.effects_for(10902)

    assert any(effect.effect_type == 'damage' and effect.cannot_kill for effect in poison_effects)


def test_xingtian_zhenyao_is_pve_only():
    catalog = default_sect_combat_skill_catalog()

    cast_rule = catalog.cast_rule(11007)

    assert cast_rule is not None
    assert cast_rule.can_target_player is False
    assert cast_rule.pvp_allowed is False


def test_youming_death_book_formula_is_not_guessed():
    catalog = default_sect_combat_skill_catalog()

    effects = catalog.effects_for(11109)

    assert any(
        effect.effect_type == 'death_check'
        and effect.params_json.get('formula_status') == 'needs_formula_confirmation'
        for effect in effects
    )
