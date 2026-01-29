from enum import IntEnum, StrEnum


class Rarity(StrEnum):
    GREY = "grey"
    GREEN = "green"
    BLUE = "blue"
    PURPLE = "purple"
    MYTHIC = "mythic"
    RED = "red"


class TroopType(StrEnum):
    INFANTRY = "infantry"
    ARCHER = "archer"
    CAVALRY = "cavalry"


class TroopTier(IntEnum):
    T1 = 1
    T2 = 2
    T3 = 3
    T4 = 4
    T5 = 5
    T6 = 6
    T7 = 7
    T8 = 8
    T9 = 9
    T10 = 10


class GearSlot(StrEnum):
    WEAPON = "weapon"
    HELMET = "helmet"
    CHEST = "chest"
    GLOVES = "gloves"
    LEGS = "legs"
    BOOTS = "boots"


class EventType(StrEnum):
    HOG = "hog"
    KVK = "kvk"
    SVS = "svs"


class BattleMode(StrEnum):
    BEAR_HUNT = "bear_hunt"
    PVP_RALLY = "pvp_rally"
    GARRISON = "garrison"
    OPEN_FIELD = "open_field"


class PetRarity(StrEnum):
    GREY = "grey"
    GREEN = "green"
    BLUE = "blue"
    PURPLE = "purple"
    LEGENDARY = "legendary"
