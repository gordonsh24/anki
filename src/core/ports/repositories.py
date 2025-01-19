"""Repository interfaces for the core domain."""

from abc import ABC, abstractmethod
from ..entities import TodayReview


class CardRepository(ABC):
    """Interface for accessing card data."""

    @abstractmethod
    def get_today_review(self) -> TodayReview:
        """Get today's review cards.
        
        Returns:
            TodayReview entity containing cards grouped by deck
            
        Raises:
            RuntimeError: If there's an error accessing the data
        """
        pass 