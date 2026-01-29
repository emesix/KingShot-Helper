# Kingshot Helper

CLI gameplay advisor for [Kingshot](https://kingshot.fandom.com/wiki/KingShot_Wiki) — calculates upgrade costs, event points, battle formations, and recommends your next best move.

## Install

```bash
git clone https://github.com/emesix/KingShot-Helper.git
cd KingShot-Helper
python -m venv .venv && source .venv/bin/activate
pip install -e .
```

## Usage

```
ks <domain> <command> [args]
```

### Hero Progression

```bash
# XP needed to reach level 80
ks hero xp 1 80

# Per-level breakdown
ks hero xp 40 80 -v

# Shards for 5-star ascension (with 200 owned)
ks hero shards 0 5 --owned 200

# Special hero unlock costs
ks hero shards 0 5 --hero amadeus
```

### Gear Enhancement

```bash
# Enhancement XP for mythic gear
ks gear enhance 0 100 --rarity mythic

# Blue gear (auto-caps at 60)
ks gear enhance 0 100 --rarity blue

# Forgehammer costs for mastery 0→10
ks gear forge 0 10

# Full mastery table (includes mythic gear costs 11-20)
ks gear forge 0 20

# Mithril + mythic gear for red gear upgrades
ks gear mithril 100 200
```

### Troop Training

```bash
# Resource cost for 1000 T10 infantry
ks troops train 10 infantry 1000

# HoG event points from training
ks troops points 10 5000 --event hog

# KvK/SVS points
ks troops points 8 10000 --event svs
```

### Battle Formations

```bash
# Bear Hunt (80% archers + hero recommendations)
ks battle bear 100000

# PvP rally (balanced 50/20/30)
ks battle pvp 100000

# Garrison defense (no archers)
ks battle garrison 100000
```

### Governor Gear & Charms

```bash
# Materials for green 0★ → purple 3★
ks gov gear green 0 purple 3

# With materials on hand
ks gov gear blue 1 mythic 0 --satin 5000 --threads 50

# Charm materials for level 0→10
ks gov charm 0 10 --guides 200 --designs 100
```

### Pets

```bash
# Leveling milestones for a blue pet
ks pet level 10 50 --rarity blue
```

### Buildings

```bash
# TC unlock gates and next milestone
ks build unlocks 22
```

### Events

```bash
# HoG training points with tier comparison
ks event hog 10 5000

# KvK prep phase estimate
ks event kvk --truegold 5 --speedups 120 --charms 5
```

### Profile & Recommendations

```bash
# Create a profile
ks profile init myaccount --tc 22

# View it
ks profile show myaccount

# Update a field
ks profile set town_center_level 25 -p myaccount

# Edit complex fields (heroes, gear) directly
nano ~/.config/kingshot-helper/myaccount.json

# Get prioritized upgrade advice
ks recommend myaccount
```

## Game Data

All game data is sourced from community resources and shipped as JSON files in the package:

| Data | Source |
|------|--------|
| Hero XP (1-80) | [KingShot Wiki](https://kingshot.fandom.com/wiki/Hero_XP_Requirements) |
| Hero Shards | [Kingshot Database](https://kingshotdata.com/database/hero-shards/) |
| Gear Enhancement XP | [Kingshot Database](https://kingshotdata.com/database/hero-gear-enhancement-chart/) |
| Forgehammer Costs | [Kingshot.net](https://kingshot.net/forgehammer-calculator) |
| Mithril / Red Gear | [Kingshot Database](https://kingshotdata.com/items/mithril/) |
| Troop Costs & Points | [Kingshot Calculator](https://kingshotcalculator.com/) |
| Governor Gear | [Kingshot Database](https://kingshotdata.com/database/governor-gear/) |
| Governor Charms | [Kingshot Database](https://kingshotdata.com/database/governor-charm/) |
| Pet Advancement | [KingShot Wiki](https://kingshot.fandom.com/wiki/Pets) |
| Battle Formations | [Kingshot Guide](https://www.kingshotguide.com/guides/troop-formations-combat-mechanics) |
| Event Points (HoG/KvK) | [Kingshot Database](https://kingshotdata.com/events/hall-of-governors/) |

To update data after a game patch, edit the JSON files in `src/kingshot_helper/data/`.

## Development

```bash
pip install -e ".[dev]"
pytest -v
ruff check src/ tests/
```

## License

MIT
