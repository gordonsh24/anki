"""Domain interface for Anki operations."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class AnkiService(ABC):
    """Domain interface for interacting with Anki."""

    @abstractmethod
    def test_connection(self) -> Optional[str]:
        """Test connection to Anki.
        
        Returns:
            Version string if connection successful, None otherwise.
        """
        pass

    @abstractmethod
    def get_deck_names(self) -> Optional[List[str]]:
        """Get all available deck names.
        
        Returns:
            List of deck names if successful, None otherwise.
        """
        pass

    @abstractmethod
    def find_due_cards(self, deck_name: Optional[str] = None) -> Optional[List[int]]:
        """Find cards that are due for review.
        
        Args:
            deck_name: Optional deck name to filter cards by
            
        Returns:
            List of card IDs if successful, None otherwise.
        """
        pass

    @abstractmethod
    def get_cards_info(self, card_ids: List[int]) -> Optional[List[Dict[str, Any]]]:
        """Get detailed information about specific cards.
        
        Args:
            card_ids: List of card IDs to get information for
            
        Returns:
            List of card information if successful, None otherwise.
        """
        pass 