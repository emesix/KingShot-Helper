from typing import Annotated

import typer
from rich.console import Console

from kingshot_helper.display.tables import forge_table, gear_enhance_table, mithril_table
from kingshot_helper.engines.gear import calc_enhancement_xp, calc_forgehammer, calc_mithril_upgrade
from kingshot_helper.models.enums import Rarity

app = typer.Typer(no_args_is_help=True)
console = Console()


@app.command()
def enhance(
    current: Annotated[int, typer.Argument(help="Current gear level")],
    target: Annotated[int, typer.Argument(help="Target gear level")],
    rarity: Annotated[Rarity, typer.Option(help="Gear rarity")] = Rarity.MYTHIC,
):
    """Calculate enhancement XP for a gear level range."""
    result = calc_enhancement_xp(current, target, rarity)
    console.print(gear_enhance_table(result))
    if result.capped:
        console.print(f"[yellow]⚠ {rarity.value} gear caps at level {result.max_level}[/]")


@app.command()
def forge(
    current: Annotated[int, typer.Argument(help="Current mastery level")] = 0,
    target: Annotated[int, typer.Argument(help="Target mastery level")] = 10,
):
    """Calculate forgehammers and mythic gears for mastery forging."""
    result = calc_forgehammer(current, target)
    console.print(forge_table(result))


@app.command()
def mithril(
    current: Annotated[int, typer.Argument(help="Current red gear level")] = 100,
    target: Annotated[int, typer.Argument(help="Target red gear level")] = 200,
):
    """Calculate mithril and mythic gear costs for red gear upgrades."""
    result = calc_mithril_upgrade(current, target)
    console.print(mithril_table(result))
