from typing import Annotated

import typer
from rich.console import Console

from kingshot_helper.display.tables import charm_table, gov_gear_table
from kingshot_helper.engines.governor import calc_governor_charm, calc_governor_gear

app = typer.Typer(no_args_is_help=True)
console = Console()


@app.command()
def gear(
    current_tier: Annotated[
        str, typer.Argument(help="Current tier (green/blue/purple/mythic/red)")
    ],
    current_stars: Annotated[int, typer.Argument(help="Current stars (0-3)")],
    target_tier: Annotated[str, typer.Argument(help="Target tier")],
    target_stars: Annotated[int, typer.Argument(help="Target stars (0-3)")],
    satin: Annotated[int, typer.Option(help="Satin on hand")] = 0,
    threads: Annotated[int, typer.Option(help="Gilded Threads on hand")] = 0,
    visions: Annotated[int, typer.Option(help="Artisan's Vision on hand")] = 0,
):
    """Calculate materials for Governor Gear upgrade."""
    result = calc_governor_gear(
        current_tier,
        current_stars,
        target_tier,
        target_stars,
        satin,
        threads,
        visions,
    )
    console.print(gov_gear_table(result))


@app.command()
def charm(
    current: Annotated[int, typer.Argument(help="Current charm level")] = 0,
    target: Annotated[int, typer.Argument(help="Target charm level")] = 10,
    guides: Annotated[int, typer.Option(help="Charm Guides on hand")] = 0,
    designs: Annotated[int, typer.Option(help="Charm Designs on hand")] = 0,
):
    """Calculate materials for Governor Charm upgrade."""
    result = calc_governor_charm(current, target, guides, designs)
    console.print(charm_table(result))
