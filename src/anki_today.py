#!/usr/bin/env python3

from typing import List, Dict, Any, Optional
from api_client import ApiClient

class AnkiToday:
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

    @staticmethod
    def get_first_field_value(card: Dict[str, Any]) -> str:
        """Get the value of the first field in the card, regardless of its name."""
        if not card['fields']:
            return "Empty card"
        # Get the first field's value
        first_field = next(iter(card['fields'].values()))
        return first_field['value']

    def get_today_reviews(self) -> None:
        # Get all deck names first
        decks = self.get_deck_names()
        if decks is None:
            return
        
        print("\nDecks found:", decks)
        print("\nCards due today by deck:")
        print("-" * 50)
        
        total_cards = 0
        
        for deck in decks:
            # Find cards due today in this deck
            query = f'deck:"{deck}" (is:due or is:new)'
            result = self.client.invoke('findCards', query=query)
            
            if result.get('error'):
                print(f"Error finding cards in {deck}: {result['error']}")
                continue
                
            card_ids = result['result']
            if not card_ids:
                continue
                
            cards_info = self.get_card_info(card_ids)
            if not cards_info:
                continue
                
            print(f"\n{deck}:")
            
            # Group cards by type
            new_cards = []
            review_cards = []
            learning_cards = []
            
            for card in cards_info:
                question = self.get_first_field_value(card)
                if card['type'] == 0:  # New card
                    new_cards.append(question)
                elif card['type'] == 1:  # Learning card
                    learning_cards.append(question)
                elif card['type'] == 2:  # Review card
                    review_cards.append(question)
            
            if new_cards:
                print("  New cards:")
                for q in new_cards:
                    print(f"    - {q}")
            
            if learning_cards:
                print("  Learning cards:")
                for q in learning_cards:
                    print(f"    - {q}")
            
            if review_cards:
                print("  Review cards:")
                for q in review_cards:
                    print(f"    - {q}")
            
            deck_total = len(new_cards) + len(learning_cards) + len(review_cards)
            total_cards += deck_total
            print(f"  Total in deck: {deck_total}")
        
        print("\n" + "-" * 50)
        print(f"Total cards to review: {total_cards}")

def main():
    client = ApiClient()
    anki = AnkiToday(client)
    
    # Check if Anki is running and accessible
    version = client.test_connection()
    if version is None:
        print("Error: Could not connect to Anki.")
        print("Please make sure that:")
        print("1. Anki is running")
        print("2. AnkiConnect add-on is installed")
        print("3. No firewall is blocking the connection")
        return
    
    print(f"Connected to AnkiConnect v{version}")
    anki.get_today_reviews()

if __name__ == "__main__":
    main() 