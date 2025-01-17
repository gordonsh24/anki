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