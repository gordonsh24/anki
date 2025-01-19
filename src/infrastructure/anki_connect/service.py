"""AnkiConnect implementation of the Anki service interface."""

from typing import List, Dict, Any, Optional
from ...core.ports.anki_service import AnkiService
from .port import AnkiConnectPort


class AnkiConnectService(AnkiService):
    """AnkiConnect implementation of the Anki service interface."""

    def __init__(self, client: AnkiConnectPort):
        """Initialize service with AnkiConnect client.
        
        Args:
            client: AnkiConnect client for making requests
        """
        self._client = client

    def test_connection(self) -> Optional[str]:
        """Test connection to Anki.
        
        Returns:
            Version string if connection successful, None otherwise.
        """
        response = self._client.request("version")
        if not response or 'result' not in response:
            return None
        return str(response['result'])

    def get_deck_names(self) -> Optional[List[str]]:
        """Get all available deck names.
        
        Returns:
            List of deck names if successful, None otherwise.
        """
        response = self._client.request("deckNames")
        if not response or 'result' not in response:
            return None
        return response['result']

    def find_due_cards(self, deck_name: Optional[str] = None) -> Optional[List[int]]:
        """Find cards that are due for review.
        
        Args:
            deck_name: Optional deck name to filter cards by
            
        Returns:
            List of card IDs if successful, None otherwise.
        """
        query = "is:due"
        if deck_name:
            query += f' deck:"{deck_name}"'
            
        response = self._client.request("findCards", {"query": query})
        if not response or 'result' not in response:
            return None
        return response['result']

    def get_cards_info(self, card_ids: List[int]) -> Optional[List[Dict[str, Any]]]:
        """Get detailed information about specific cards.
        
        Args:
            card_ids: List of card IDs to get information for
            
        Returns:
            List of card information if successful, None otherwise.
        """
        if not card_ids:
            return []
            
        response = self._client.request("cardsInfo", {"cards": card_ids})
        if not response or 'result' not in response:
            return None
        return response['result'] 