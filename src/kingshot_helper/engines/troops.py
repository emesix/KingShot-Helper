from __future__ import annotations

from dataclasses import dataclass

from kingshot_helper.data import load_json
from kingshot_helper.models.enums import EventType, TroopType


@dataclass
class TrainingCost:
    tier: int
    troop_type: TroopType
    count: int
    bread: int
    wood: int
    stone: int
    iron: int
    total_resources: int


@dataclass
class EventPoints:
    tier: int
    event: EventType
    count: int
    points_per_unit: int
    total_points: int
    power_per_unit: int
    total_power: int


def calc_training_cost(tier: int, troop_type: TroopType, count: int) -> TrainingCost:
    """Total resources to train `count` troops of given tier and type."""
    data = load_json("troop_costs.json")
    per = data["per_unit"][str(tier)][troop_type.value]
    b = per["bread"] * count
    w = per["wood"] * count
    s = per["stone"] * count
    i = per["iron"] * count
    return TrainingCost(tier, troop_type, count, b, w, s, i, b + w + s + i)


def calc_event_points(tier: int, event: EventType, count: int) -> EventPoints:
    """Event points for training `count` troops of given tier."""
    pts_data = load_json("troop_points.json")
    ppu = pts_data[event.value][str(tier)]
    pow_data = pts_data["power"]
    power_per = pow_data[str(tier)]
    return EventPoints(tier, event, count, ppu, ppu * count, power_per, power_per * count)


def points_per_resource(tier: int, troop_type: TroopType, event: EventType) -> float:
    """Event points earned per total resource spent for one troop."""
    costs = load_json("troop_costs.json")
    pts = load_json("troop_points.json")
    per = costs["per_unit"][str(tier)][troop_type.value]
    total_cost = per["bread"] + per["wood"] + per["stone"] + per["iron"]
    ppu = pts[event.value][str(tier)]
    return ppu / total_cost if total_cost > 0 else 0.0
