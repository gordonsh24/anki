"""Command Line Interface for Anki CLI."""

from typing import Optional
import typer
from rich import print
from rich.console import Console
from rich.table import Table

from src.application.containers import Container

app = typer.Typer(
    name="anki",
    help="CLI tool for interacting with Anki",
    add_completion=False,
)

console = Console()


@app.command()
def today(
    deck: Optional[str] = typer.Option(None, help="Filter reviews by deck name"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed information"),
):
    """Show today's reviews."""
    try:
        container = Container()
        anki_today = container.anki_today()
        anki_today.execute()
    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        raise typer.Exit(code=1)


@app.callback()
def callback():
    """CLI tool for interacting with Anki."""
    pass


if __name__ == "__main__":
    app() 