from kingshot_helper.engines.heroes import calc_hero_xp, calc_shards, drill_camp_xp


def test_hero_xp_basic():
    result = calc_hero_xp(1, 10)
    assert result.total_xp > 0
    assert result.current_level == 1
    assert result.target_level == 10
    assert len(result.breakdown) > 0


def test_hero_xp_level_2():
    result = calc_hero_xp(1, 2)
    assert result.total_xp == 480
    assert result.tc_required == 4


def test_hero_xp_full():
    result = calc_hero_xp(1, 80)
    assert result.total_xp > 10_000_000
    assert result.tc_required == 26


def test_shards_full():
    result = calc_shards(0, 5)
    assert result.shards_needed == 1065
    assert result.shards_deficit == 1065
    assert len(result.per_star) == 5


def test_shards_with_owned():
    result = calc_shards(3, 5, shards_owned=500)
    needed = 300 + 600  # star 4 + star 5
    assert result.shards_needed == needed
    assert result.shards_deficit == max(0, needed - 500)


def test_shards_single_star():
    result = calc_shards(0, 1)
    assert result.shards_needed == 10


def test_drill_camp_spillover():
    assert drill_camp_xp(1000) == 800
    assert drill_camp_xp(0) == 0
