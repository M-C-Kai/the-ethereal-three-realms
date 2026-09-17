import json
from pathlib import Path

from systems.skill.registry import default_life_skill_registry


ROOT = Path(__file__).resolve().parent.parent
CATALOG_FILE = ROOT / 'data' / 'catalog' / 'life_skills.json'


def _catalog():
    return json.loads(CATALOG_FILE.read_text(encoding='utf-8'))


def test_life_skill_catalog_loads_with_existing_registry():
    registry = default_life_skill_registry()

    assert set(registry.skills) == {2001, 2002, 2003, 2004, 2005}
    assert registry.skills[2001].name == '百草术'
    assert registry.skills[2004].name == '工巧术'


def test_four_official_life_skills_are_independent_and_level_50():
    data = _catalog()
    official = [skill for skill in data['skills'] if skill['category'] == 'official_life']

    assert {skill['name'] for skill in official} == {'百草术', '采矿术', '丹药术', '工巧术'}
    assert all(skill['max_level'] == 50 for skill in official)
    assert all(skill['can_learn_with_other_life_skills'] for skill in official)
    assert data['defaults']['conflict_limit'] == 'none'


def test_proficiency_upgrade_model_matches_source_notes():
    data = _catalog()
    rules = {rule['skill_id']: rule for rule in data['upgrade_rules']}

    for skill_id in (2001, 2002, 2003):
        assert rules[skill_id]['method'] == 'proficiency_action'
        assert rules[skill_id]['per_level_proficiency_required'] == 100

    assert rules[2004]['method'] == 'trainer_direct'
    assert rules[2004]['per_level_proficiency_required'] == 0


def test_quality_grades_are_common_fine_rare_perfect():
    data = _catalog()

    assert [grade['name'] for grade in data['quality_grades']] == ['普品', '佳品', '珍品', '绝品']
    assert [grade['quality_key'] for grade in data['quality_grades']] == [
        'common', 'fine', 'rare', 'perfect',
    ]


def test_initial_recognition_and_formula_unlocks():
    data = _catalog()
    unlocks = {entry['skill_id']: entry for entry in data['recognition_unlocks']}

    assert unlocks[2001]['unlock_type'] == 'herb_recognition'
    assert unlocks[2001]['initial_count'] == 2
    assert unlocks[2002]['unlock_type'] == 'ore_recognition'
    assert unlocks[2002]['initial_count'] == 2
    assert unlocks[2003]['unlock_type'] == 'pill_formula'
    assert unlocks[2003]['initial_count'] == 2


def test_moonlight_box_level_ranges_and_luban_secret():
    data = _catalog()
    products = {product['name']: product for product in data['craft_products']}

    assert products['绿色月光匣']['level_min'] == 1
    assert products['绿色月光匣']['level_max'] == 19
    assert products['蓝色月光匣']['level_min'] == 20
    assert products['蓝色月光匣']['level_max'] == 39
    assert products['红色月光匣']['level_min'] == 40
    assert products['红色月光匣']['level_max'] == 50
    assert products['红色月光匣']['required_unlock_key'] == 'luban_secret_record'


def test_spirit_bead_conversion_mapping():
    data = _catalog()
    mapping = {entry['bead_name']: entry['attribute'] for entry in data['spirit_bead_conversions']}

    assert mapping == {
        '金灵珠': '力量',
        '木灵珠': '耐力',
        '水灵珠': '敏捷',
        '火灵珠': '智力',
        '土灵珠': '精神',
    }


def test_trainers_are_in_changan_with_distinct_entries():
    data = _catalog()

    assert {trainer['location'] for trainer in data['trainers']} == {'长安城'}
    assert {trainer['name'] for trainer in data['trainers']} == {
        '百草术训练师',
        '采矿术训练师',
        '丹药术训练师',
        '工巧术训练师',
        '灵珠大师',
    }
    taught_entries = [
        entry_id
        for trainer in data['trainers']
        for entry_id in trainer['entry_ids']
    ]
    assert sorted(taught_entries) == [5001, 5002, 5003, 5004, 5005]
