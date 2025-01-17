#!/usr/bin/env python3

from typing import List, Dict, Any, Optional
from .api_client import ApiClient
from .query import Query

class AnkiToday:
    def __init__(self, client: ApiClient):
        self.client = client
        self.query = Query(client)

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
        decks = self.query.get_deck_names()
        if decks is None:
            return
        
        print("\nDecks found:", decks)
        print("\nCards due today by deck:")
        print("-" * 50)
        
        total_cards = 0
        
        for deck in decks:
            # Find cards due today in this deck
            card_ids = self.query.find_cards_due_today(deck)
            if not card_ids:
                continue
                
            cards_info = self.query.get_card_info(card_ids)
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