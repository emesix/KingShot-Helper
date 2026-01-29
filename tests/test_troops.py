from kingshot_helper.engines.troops import (
    calc_event_points,
    calc_training_cost,
    points_per_resource,
)
from kingshot_helper.models.enums import EventType, TroopType


def test_training_cost_t1():
    result = calc_training_cost(1, TroopType.INFANTRY, 100)
    assert result.bread == 3600
    assert result.wood == 2700
    assert result.count == 100


def test_training_cost_t10():
    result = calc_training_cost(10, TroopType.INFANTRY, 1)
    assert result.bread == 2804
    assert result.wood == 2091
    assert result.stone == 488
    assert result.iron == 253


def test_event_points_hog():
    result = calc_event_points(10, EventType.HOG, 1000)
    assert result.points_per_unit == 1960
    assert result.total_points == 1_960_000


def test_event_points_svs():
    result = calc_event_points(1, EventType.SVS, 100)
    assert result.points_per_unit == 3
    assert result.total_points == 300


def test_points_per_resource():
    ratio = points_per_resource(10, TroopType.INFANTRY, EventType.HOG)
    assert ratio > 0
    # Lower tiers are actually more resource-efficient (more points per resource)
    # Higher tiers give more points per unit but cost disproportionately more
    ratio_low = points_per_resource(1, TroopType.INFANTRY, EventType.HOG)
    assert ratio_low > ratio
