from typing import Annotated

import typer
from rich.console import Console

from kingshot_helper.display.panels import profile_panel
from kingshot_helper.models.profile import UserProfile

app = typer.Typer(no_args_is_help=True)
console = Console()


@app.command()
def init(
    name: Annotated[str, typer.Argument(help="Profile name")] = "default",
    tc_level: Annotated[int, typer.Option("--tc", help="Town Center level")] = 1,
):
    """Create a new player profile."""
    p = UserProfile(name=name, town_center_level=tc_level)
    path = p.save()
    console.print(f"[green]Profile created:[/] {path}")
    console.print("[dim]Edit the JSON file directly or use 'ks profile set' to update values.[/]")


@app.command()
def show(
    name: Annotated[str, typer.Argument(help="Profile name")] = "default",
):
    """Display a saved profile."""
    path = UserProfile.profile_dir() / f"{name}.json"
    if not path.exists():
        console.print(f"[red]Profile '{name}' not found. Run 'ks profile init' first.[/]")
        raise typer.Exit(1)
    p = UserProfile.load(path)
    console.print(profile_panel(p))


@app.command(name="set")
def set_value(
    key: Annotated[str, typer.Argument(help="Field to set (e.g. town_center_level)")],
    value: Annotated[str, typer.Argument(help="New value")],
    name: Annotated[str, typer.Option("--profile", "-p", help="Profile name")] = "default",
):
    """Update a top-level profile field."""
    path = UserProfile.profile_dir() / f"{name}.json"
    if not path.exists():
        console.print(f"[red]Profile '{name}' not found.[/]")
        raise typer.Exit(1)

    p = UserProfile.load(path)
    if not hasattr(p, key):
        console.print(f"[red]Unknown field: {key}[/]")
        console.print(f"[dim]Valid fields: {', '.join(p.model_fields.keys())}[/]")
        raise typer.Exit(1)

    field_info = p.model_fields[key]
    try:
        if field_info.annotation is int:
            setattr(p, key, int(value))
        elif field_info.annotation is str:
            setattr(p, key, value)
        else:
            console.print(
                f"[yellow]Complex fields should be edited in the JSON directly: {path}[/]"
            )
            raise typer.Exit(0)
    except (ValueError, TypeError) as e:
        console.print(f"[red]Invalid value: {e}[/]")
        raise typer.Exit(1) from None

    p.save(path)
    console.print(f"[green]Updated {key} = {value}[/]")


@app.command()
def path(
    name: Annotated[str, typer.Argument(help="Profile name")] = "default",
):
    """Show the file path for a profile."""
    p = UserProfile.profile_dir() / f"{name}.json"
    console.print(str(p))
