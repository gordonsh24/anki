"""Main entry point for the Anki Today application."""

from .container import Container

def main():
    """Run the Anki Today application."""
    container = Container()
    app = container.anki_today()
    app.get_today_reviews()

if __name__ == "__main__":
    main() 