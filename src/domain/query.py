from typing import List, Dict, Any, Optional
from ..api_client import ApiClient

class Query:
    def __init__(self, client: ApiClient):
        self.client = client

    def get_deck_names(self) -> Optional[List[str]]:
        """Get a list of parent deck names from Anki."""
        decks = self.client.invoke('deckNames')
        if decks.get('error'):
            print(f"Error: {decks['error']}")
            return None
        
        # Filter out sub-decks by keeping only decks without "::"
        parent_decks = [deck for deck in decks['result'] if "::" not in deck]
        return parent_decks

    def get_card_info(self, card_ids: List[int]) -> List[Dict[str, Any]]:
        """Get detailed information about specific cards."""
        result = self.client.invoke('cardsInfo', cards=card_ids)
        if result.get('error'):
            print(f"Error getting card info: {result['error']}")
            return []
        return result['result']
    
    def find_cards_due_today(self, deck: str) -> List[int]:
        """Find all cards due today in a specific deck."""
        query = f'deck:"{deck}" (is:due or is:new)'
        result = self.client.invoke('findCards', query=query)
        
        if result.get('error'):
            print(f"Error finding cards in {deck}: {result['error']}")
            return []
            
        return result['result'] 