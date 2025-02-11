"""Repository interfaces for the core domain."""

from abc import ABC, abstractmethod
from typing import Optional
from ..entities import TodayReview


class CardRepository(ABC):
    """Interface for accessing card data."""

    @abstractmethod
    def get_today_review(self, deck_name: Optional[str] = None) -> TodayReview:
        """Get today's review cards.
        
        Args:
            deck_name: Optional deck name to filter by
            
        Returns:
            TodayReview entity containing cards grouped by deck
            
        Raises:
            RuntimeError: If there's an error accessing the data
        """
        pass

    @abstractmethod
    def get_all_cards(self, limit: int = 20, offset: int = 0, deck_name: Optional[str] = None, random: bool = False) -> TodayReview:
        """Get all cards, optionally filtered by deck.

        Args:
            limit: Maximum number of cards per deck to fetch
            offset: Number of cards to skip
            deck_name: Optional deck name to filter by
            random: Whether to randomize the order of cards

        Returns:
            A TodayReview entity containing the cards
        """
        pass 