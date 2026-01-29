from __future__ import annotations

from dataclasses import dataclass

from kingshot_helper.data import load_json


@dataclass
class TCUnlockInfo:
    current_level: int
    unlocked: dict[int, str]
    next_unlock: tuple[int, str] | None


def tc_unlocks(tc_level: int) -> TCUnlockInfo:
    """What the current TC level has unlocked and what's next."""
    data = load_json("buildings.json")
    unlock_map = data["tc_unlocks"]

    unlocked = {int(k): v for k, v in unlock_map.items() if int(k) <= tc_level}
    remaining = {int(k): v for k, v in unlock_map.items() if int(k) > tc_level}
    next_unlock = min(remaining.items(), key=lambda x: x[0]) if remaining else None

    return TCUnlockInfo(tc_level, unlocked, next_unlock)


def building_info() -> dict:
    """Return building configuration data."""
    return load_json("buildings.json")
