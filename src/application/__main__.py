"""Main entry point for the Anki Today application."""

from .container import Container

def main():
    """Run the application."""
    container = Container()
    app = container.anki_today()
    app.execute()

if __name__ == "__main__":
    main() 