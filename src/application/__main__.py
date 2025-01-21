"""Main entry point for the Anki Today application."""

from .containers import Container


def main() -> None:
    """Run the application."""
    container = Container()
    container.init_resources()
    container.anki_today().execute()


if __name__ == "__main__":
    main() 