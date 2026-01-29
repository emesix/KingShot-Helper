from typing import Annotated

import typer
from rich.console import Console

from kingshot_helper.display.panels import recommendations_panel
from kingshot_helper.engines.advisor import get_recommendations
from kingshot_helper.models.profile import UserProfile

console = Console()


def recommend(
    profile_name: Annotated[str, typer.Argument(help="Profile name")] = "default",
    top: Annotated[int, typer.Option(help="Number of recommendations")] = 5,
):
    """Get prioritized upgrade recommendations based on your profile."""
    path = UserProfile.profile_dir() / f"{profile_name}.json"
    if not path.exists():
        console.print(f"[red]Profile '{profile_name}' not found. Run 'ks profile init' first.[/]")
        raise typer.Exit(1)
    profile = UserProfile.load(path)
    recs = get_recommendations(profile, top_n=top)
    console.print(recommendations_panel(recs))
