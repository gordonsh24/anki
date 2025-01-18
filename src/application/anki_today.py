#!/usr/bin/env python3

from ..domain import AnkiTodayService
from ..core.ports import ReviewPresenter

class AnkiToday:
    def __init__(self, service: AnkiTodayService, presenter: ReviewPresenter):
        self.service = service
        self.presenter = presenter

    def get_today_reviews(self) -> None:
        """Display all cards that need to be reviewed today."""
        today_review = self.service.get_cards()
        result = self.presenter.present(today_review)
        print(result["message"])
        print(f"\nTotal cards to review: {result['total_cards']}") 