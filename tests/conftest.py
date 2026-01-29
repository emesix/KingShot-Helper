import pytest

from kingshot_helper.models.enums import GearSlot, PetRarity, Rarity
from kingshot_helper.models.profile import (
    GearState,
    GovernorCharmState,
    GovernorGearState,
    HeroState,
    PetState,
    Resources,
    UserProfile,
)


@pytest.fixture
def mid_game_profile():
    return UserProfile(
        name="test_mid",
        town_center_level=22,
        heroes=[
            HeroState(
                name="Howard",
                level=40,
                stars=3,
                shards_owned=50,
                gear={
                    GearSlot.GLOVES: GearState(rarity=Rarity.MYTHIC, level=60, mastery_level=5),
                    GearSlot.CHEST: GearState(rarity=Rarity.MYTHIC, level=40, mastery_level=3),
                },
            ),
            HeroState(name="Zoe", level=35, stars=2, shards_owned=20),
        ],
        governor_gear=GovernorGearState(tier=Rarity.BLUE, stars=1),
        governor_charm=GovernorCharmState(level=3),
        pets=[PetState(name="Wolf", rarity=PetRarity.PURPLE, level=25)],
        resources=Resources(
            bread=500_000,
            wood=400_000,
            stone=300_000,
            iron=200_000,
            forgehammers=50,
        ),
    )


@pytest.fixture
def early_game_profile():
    return UserProfile(
        name="test_early",
        town_center_level=10,
        heroes=[HeroState(name="Howard", level=15, stars=1, shards_owned=5)],
        resources=Resources(bread=50_000, wood=40_000),
    )
