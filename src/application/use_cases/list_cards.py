"""Use case for listing all cards in Anki."""

from typing import Optional

from src.core.ports import CardRepository, ReviewPresenter


class AnkiList:
    """Use case for listing all cards in Anki."""

    def __init__(self, repository: CardRepository, presenter: ReviewPresenter):
        """Initialize AnkiList with required dependencies.

        Args:
            repository: Repository for accessing card data
            presenter: Presenter for displaying the results
        """
        self._repository = repository
        self._presenter = presenter

    def execute(self, limit: int = 20, offset: int = 0, deck: Optional[str] = None) -> None:
        """Execute the use case to list all cards.

        Args:
            limit: Maximum number of cards per deck to fetch
            offset: Number of cards to skip
            deck: Optional deck name to filter by
        """
        review = self._repository.get_all_cards(limit=limit, offset=offset, deck_name=deck)
        self._presenter.present(review) 