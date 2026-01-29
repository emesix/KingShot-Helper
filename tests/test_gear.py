from kingshot_helper.engines.gear import (
    calc_enhancement_xp,
    calc_forgehammer,
    calc_mithril_upgrade,
)
from kingshot_helper.models.enums import Rarity


def test_enhancement_mythic():
    result = calc_enhancement_xp(0, 100, Rarity.MYTHIC)
    assert result.total_xp > 0
    assert result.max_level == 100
    assert not result.capped


def test_enhancement_capped():
    result = calc_enhancement_xp(0, 100, Rarity.BLUE)
    assert result.capped
    assert result.target_level == 60


def test_forge_1_to_10():
    result = calc_forgehammer(0, 10)
    assert result.total_hammers == sum(range(10, 110, 10))  # 10+20+...+100 = 550
    assert result.total_mythic_gears == 0
    assert result.stat_bonus_percent == 100.0


def test_forge_10_to_20():
    result = calc_forgehammer(10, 20)
    assert result.total_mythic_gears == sum(range(1, 11))  # 1+2+...+10 = 55
    assert result.total_hammers > 0


def test_mithril_full():
    result = calc_mithril_upgrade(100, 200)
    assert result.total_mithril == 150
    assert result.total_mythic_gears == 33  # 3+5+5+10+10
    assert len(result.blocks) == 5


def test_mithril_partial():
    result = calc_mithril_upgrade(100, 140)
    assert result.total_mithril == 30  # 10 + 20
    assert len(result.blocks) == 2
