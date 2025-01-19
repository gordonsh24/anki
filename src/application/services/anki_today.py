"""Service for retrieving and organizing today's Anki reviews."""

from ...core.ports import CardRepository
from ...core.entities import TodayReview


class AnkiTodayService:
    """Service for getting today's Anki reviews."""

    def __init__(self, repository: CardRepository):
        """Initialize service with card repository.
        
        Args:
            repository: Repository for accessing Anki cards
        """
        self._repository = repository

    def get_cards(self) -> TodayReview:
        """Get all cards due for review today.
        
        Returns:
            TodayReview object containing all cards due for review.
        """
        return self._repository.get_due_cards() 