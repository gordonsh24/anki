"""Today's review use case implementation."""

from ..services import AnkiTodayService
from ..presentation import ConsolePresenter


class AnkiToday:
    """Main use case for getting today's Anki review information."""

    def __init__(self, service: AnkiTodayService, presenter: ConsolePresenter):
        """Initialize AnkiToday with required dependencies.

        Args:
            service: Service for retrieving Anki card information
            presenter: Presenter for displaying the results
        """
        self._service = service
        self._presenter = presenter

    def execute(self) -> None:
        """Execute the use case to get and display today's review information."""
        review = self._service.get_cards()
        self._presenter.present(review) 