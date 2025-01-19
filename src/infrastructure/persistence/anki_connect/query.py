"""AnkiConnect-specific query implementation."""

from typing import List, Dict, Any, Optional
from ....core.ports import AnkiConnectPort


class AnkiConnectQuery:
    """Query implementation specific to AnkiConnect protocol."""

    def __init__(self, client: AnkiConnectPort):
        """Initialize query with AnkiConnect client.
        
        Args:
            client: AnkiConnect client for making requests
        """
        self._client = client

    def get_deck_names(self) -> Optional[List[str]]:
        """Get all available deck names from Anki.
        
        Returns:
            List of deck names or None if request failed
        """
        response = self._client.request("deckNames")
        if not response or 'result' not in response:
            return None
        return response['result']

    def find_cards_due_today(self) -> Optional[List[int]]:
        """Find all card IDs that are due for review today.
        
        Returns:
            List of card IDs or None if request failed
        """
        query = "is:due"
        response = self._client.request("findCards", {"query": query})
        if not response or 'result' not in response:
            return None
        return response['result']

    def get_card_info(self, card_ids: List[int]) -> Optional[List[Dict[str, Any]]]:
        """Get detailed information about specific cards.
        
        Args:
            card_ids: List of card IDs to get information for
            
        Returns:
            List of card information dictionaries or None if request failed
        """
        if not card_ids:
            return []
            
        response = self._client.request("cardsInfo", {"cards": card_ids})
        if not response or 'result' not in response:
            return None
        return response['result'] 