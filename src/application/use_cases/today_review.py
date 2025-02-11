"""Use case for getting today's review cards."""

from typing import Optional
from src.core.ports import CardRepository, ReviewPresenter


class AnkiToday:
    """Use case for getting today's review cards."""

    def __init__(self, repository: CardRepository, presenter: ReviewPresenter):
        """Initialize AnkiToday with required dependencies.

        Args:
            repository: Repository for accessing card data
            presenter: Presenter for displaying the results
        """
        self._repository = repository
        self._presenter = presenter

    def execute(self, deck_name: Optional[str] = None) -> None:
        """Execute the use case to get today's review cards.

        Args:
            deck_name: Optional deck name to filter by
        """
        review = self._repository.get_today_review(deck_name=deck_name)
        self._presenter.present(review) 