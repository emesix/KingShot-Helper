from typing import Annotated

import typer
from rich.console import Console

from kingshot_helper.display.panels import pet_panel
from kingshot_helper.engines.pets import calc_pet_level
from kingshot_helper.models.enums import PetRarity

app = typer.Typer(no_args_is_help=True)
console = Console()


@app.command()
def level(
    current: Annotated[int, typer.Argument(help="Current pet level")],
    target: Annotated[int, typer.Argument(help="Target pet level")],
    rarity: Annotated[PetRarity, typer.Option(help="Pet rarity")] = PetRarity.LEGENDARY,
):
    """Calculate pet leveling requirements and advancement milestones."""
    result = calc_pet_level(current, target, rarity)
    console.print(pet_panel(result))
