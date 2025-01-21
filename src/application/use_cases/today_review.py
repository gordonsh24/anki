"""Today's review use case implementation."""

from src.core.ports import CardRepository, ReviewPresenter


class AnkiToday:
    """Main use case for getting today's Anki review information."""

    def __init__(self, repository: CardRepository, presenter: ReviewPresenter):
        """Initialize AnkiToday with required dependencies.

        Args:
            repository: Repository for accessing card data
            presenter: Presenter for displaying the results
        """
        self._repository = repository
        self._presenter = presenter

    def execute(self) -> None:
        """Execute the use case to get and display today's review information."""
        review = self._repository.get_today_review()
        self._presenter.present(review) 