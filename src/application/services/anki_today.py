"""Service for getting today's Anki review cards."""

from ...core.entities import TodayReview
from ...core.ports.repositories import CardRepository


class AnkiTodayService:
    """Service for getting today's Anki review cards."""

    def __init__(self, card_repository: CardRepository):
        """Initialize the service.
        
        Args:
            card_repository: Repository for accessing card data
        """
        self._repository = card_repository

    def get_cards(self) -> TodayReview:
        """Get all cards that are due for review today.
        
        Returns:
            TodayReview object containing all cards due for review
            
        Raises:
            RuntimeError: If there's an error getting the cards
        """
        return self._repository.get_today_review() 