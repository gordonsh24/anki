"""Repository interface for accessing Anki cards."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
from ..entities import DeckCards, TodayReview


class CardRepository(ABC):
    """Interface for accessing and querying Anki cards."""

    @abstractmethod
    def get_decks(self) -> List[str]:
        """Get all available deck names.
        
        Returns:
            List of deck names.
        """
        pass

    @abstractmethod
    def get_due_cards(self) -> TodayReview:
        """Get all cards that are due for review today.
        
        Returns:
            TodayReview object containing all cards due for review.
        """
        pass 