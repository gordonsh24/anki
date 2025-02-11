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
):
    """Show today's reviews."""
    try:
        container = Container()
        anki_today = container.anki_today()
        anki_today.execute(deck_name=deck)
    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        raise typer.Exit(code=1)


@app.command()
def list(
    limit: int = typer.Option(20, help="Limit of cards per deck to fetch"),
    offset: int = typer.Option(0, help="Number of cards to skip"),
    deck: Optional[str] = typer.Option(None, help="Get cards only from given deck"),
    random: bool = typer.Option(False, help="Randomize the order of cards"),
):
    """List all cards in Anki."""
    try:
        container = Container()
        anki_list = container.anki_list()
        anki_list.execute(limit=limit, offset=offset, deck=deck, random=random)
    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        raise typer.Exit(code=1)


@app.callback()
def callback():
    """CLI tool for interacting with Anki."""
    pass


if __name__ == "__main__":
    app() 