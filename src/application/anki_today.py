#!/usr/bin/env python3

from ..integration import AnkiConnectClient
from ..domain import Query, AnkiTodayService
from ..domain.presenter import ReviewPresenter
from .console_presenter import ConsolePresenter

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
    # Set up dependencies
    client = AnkiConnectClient()
    query = Query(client)
    service = AnkiTodayService(query)
    presenter = ConsolePresenter()
    anki = AnkiToday(service, presenter)
    
    # Check if Anki is running and accessible
    version = client.test_connection()
    if version is None:
        presenter.show_connection_error()
        return
    
    presenter.show_connection_success(version)
    anki.get_today_reviews()

if __name__ == "__main__":
    main() 