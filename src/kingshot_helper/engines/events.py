from __future__ import annotations

from dataclasses import dataclass

from kingshot_helper.data import load_json


@dataclass
class HoGTrainResult:
    tier: int
    count: int
    points_per_unit: int
    total_points: int


@dataclass
class KvKPointBreakdown:
    truegold_used: int
    truegold_points: int
    speedup_minutes: int
    speedup_points: int
    charm_points: int
    total: int


def calc_hog_training(tier: int, count: int) -> HoGTrainResult:
    """Hall of Governors training points."""
    data = load_json("troop_points.json")
    ppu = data["hog"][str(tier)]
    return HoGTrainResult(tier, count, ppu, ppu * count)


def calc_kvk_points(
    truegold: int = 0,
    speedup_minutes: int = 0,
    charm_levels: int = 0,
) -> KvKPointBreakdown:
    """KvK preparation phase point estimation."""
    tg_pts = truegold * 2000
    sp_pts = speedup_minutes * 30

    charm_level_scores = {
        1: 625,
        2: 1250,
        3: 3125,
        4: 8750,
        5: 11250,
        6: 12500,
        7: 12500,
        8: 13000,
        9: 14000,
        10: 15000,
        11: 16000,
    }
    charm_pts = sum(charm_level_scores.get(lv, 0) for lv in range(1, charm_levels + 1))

    return KvKPointBreakdown(
        truegold,
        tg_pts,
        speedup_minutes,
        sp_pts,
        charm_pts,
        tg_pts + sp_pts + charm_pts,
    )


def all_hog_tiers() -> list[dict]:
    """Overview of HoG points per tier for comparison."""
    data = load_json("troop_points.json")
    return [
        {"tier": int(k), "hog_points": v}
        for k, v in sorted(data["hog"].items(), key=lambda x: int(x[0]))
    ]
