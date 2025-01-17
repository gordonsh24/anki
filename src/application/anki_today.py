#!/usr/bin/env python3

from ..domain import AnkiTodayService
from ..domain.presenter import ReviewPresenter

class AnkiToday:
    def __init__(self, service: AnkiTodayService, presenter: ReviewPresenter):
        self.service = service
        self.presenter = presenter

    def get_today_reviews(self) -> None:
        """Display all cards that need to be reviewed today."""
        today_review = self.service.get_cards()
        
        if not today_review.decks:
            self.presenter.show_no_cards()
            return
        
        self.presenter.show_deck_list([deck.deck_name for deck in today_review.decks])
        
        for deck in today_review.decks:
            self.presenter.show_deck_cards(
                deck_name=deck.deck_name,
                new_cards=deck.new_cards,
                learning_cards=deck.learning_cards,
                review_cards=deck.review_cards,
                total=deck.total_cards
            )
        
        self.presenter.show_total_cards(today_review.total_cards)

def main():
    from .container import Container
    
    # Create and configure the container
    container = Container()
    
    # Get the application instance
    anki = container.anki_today()
    
    # Check if Anki is running and accessible
    version = container.anki_client().test_connection()
    if version is None:
        container.presenter().show_connection_error()
        return
    
    container.presenter().show_connection_success(version)
    anki.get_today_reviews()

if __name__ == "__main__":
    main() 