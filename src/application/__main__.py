"""Main entry point for the Anki Today application."""

from .container import Container


def main() -> None:
    """Run the application."""
    container = Container()
    
    # Execute the use case
    anki_today = container.anki_today()
    anki_today.execute()


if __name__ == "__main__":
    main() 