from kingshot_helper.engines.battle import recommend_formation
from kingshot_helper.models.enums import BattleMode


def test_bear_hunt():
    result = recommend_formation(BattleMode.BEAR_HUNT, 100_000)
    assert result.archer_count == 80_000
    assert result.infantry_count == 10_000
    assert result.cavalry_count == 10_000
    assert result.hero_recommendations is not None


def test_pvp_rally():
    result = recommend_formation(BattleMode.PVP_RALLY, 100_000)
    assert result.infantry_count == 50_000
    assert result.archer_count == 30_000
    assert result.cavalry_count == 20_000


def test_garrison_no_archers():
    result = recommend_formation(BattleMode.GARRISON, 100_000)
    assert result.archer_count == 0
    assert result.infantry_count == 70_000
    assert result.cavalry_count == 30_000


def test_formation_rounding():
    result = recommend_formation(BattleMode.BEAR_HUNT, 99)
    total = result.infantry_count + result.archer_count + result.cavalry_count
    assert total == 99
