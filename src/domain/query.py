from typing import List, Dict, Any, Optional
from ..core.ports import AnkiConnectPort

class Query:
    """Query service for retrieving data from Anki."""

    def __init__(self, client: AnkiConnectPort):
        self.client = client

    def get_deck_names(self) -> Optional[List[str]]:
        """Get names of all available decks."""
        response = self.client.request("deckNames")
        if response and not response.get("error"):
            return response.get("result")
        return None

    def find_cards_due_today(self, deck_name: str) -> Optional[List[int]]:
        """Find all cards due today in a given deck."""
        query = f'"deck:{deck_name}" is:due'
        response = self.client.request("findCards", {"query": query})
        if response and not response.get("error"):
            return response.get("result")
        return None

    def get_card_info(self, card_ids: List[int]) -> Optional[List[Dict[str, Any]]]:
        """Get detailed information about specific cards."""
        response = self.client.request("cardsInfo", {"cards": card_ids})
        if response and not response.get("error"):
            return response.get("result")
        return None 