"""Main entry point for the application."""

from .container import Container


def main():
    """Run the application."""
    container = Container()
    
    # Get today's review cards
    service = container.anki_today_service()
    presenter = container.console_presenter()
    
    # Get and display the cards
    review = service.get_cards()
    presenter.show_review(review)


if __name__ == "__main__":
    main() 