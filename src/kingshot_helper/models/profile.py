from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field

from kingshot_helper.models.enums import GearSlot, PetRarity, Rarity, TroopType


class GearState(BaseModel):
    rarity: Rarity = Rarity.GREY
    level: int = 1
    mastery_level: int = 0


class HeroState(BaseModel):
    name: str
    level: int = 1
    stars: int = 0
    shards_owned: int = 0
    gear: dict[GearSlot, GearState] = Field(default_factory=dict)


class TroopState(BaseModel):
    counts: dict[int, dict[TroopType, int]] = Field(default_factory=dict)


class BuildingState(BaseModel):
    name: str
    level: int = 1
    truegold_level: int = 0


class GovernorGearState(BaseModel):
    tier: Rarity = Rarity.GREEN
    stars: int = 0
    satin: int = 0
    threads: int = 0
    visions: int = 0


class GovernorCharmState(BaseModel):
    level: int = 0
    guides_on_hand: int = 0
    designs_on_hand: int = 0


class PetState(BaseModel):
    name: str
    rarity: PetRarity = PetRarity.GREY
    level: int = 1


class Resources(BaseModel):
    bread: int = 0
    wood: int = 0
    stone: int = 0
    iron: int = 0
    truegold: int = 0
    mithril: int = 0
    forgehammers: int = 0


class UserProfile(BaseModel):
    name: str = "default"
    town_center_level: int = 1
    town_center_tg: int = 0
    heroes: list[HeroState] = Field(default_factory=list)
    troops: TroopState = Field(default_factory=TroopState)
    buildings: list[BuildingState] = Field(default_factory=list)
    governor_gear: GovernorGearState = Field(default_factory=GovernorGearState)
    governor_charm: GovernorCharmState = Field(default_factory=GovernorCharmState)
    pets: list[PetState] = Field(default_factory=list)
    resources: Resources = Field(default_factory=Resources)

    @staticmethod
    def profile_dir() -> Path:
        return Path.home() / ".config" / "kingshot-helper"

    def save(self, path: Path | None = None) -> Path:
        p = path or self.profile_dir() / f"{self.name}.json"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(self.model_dump_json(indent=2))
        return p

    @classmethod
    def load(cls, path: Path) -> UserProfile:
        return cls.model_validate_json(path.read_text())
