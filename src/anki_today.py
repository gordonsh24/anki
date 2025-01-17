#!/usr/bin/env python3

from .api_client import ApiClient
from .query import Query
from .service import AnkiTodayService

class AnkiToday:
    def __init__(self, client: ApiClient):
        self.query = Query(client)
        self.service = AnkiTodayService(self.query)

    def get_today_reviews(self) -> None:
        """Display all cards that need to be reviewed today."""
        today_review = self.service.get_cards()
        
        if not today_review.decks:
            print("\nNo cards to review today!")
            return
        
        print("\nDecks found:", [deck.deck_name for deck in today_review.decks])
        print("\nCards due today by deck:")
        print("-" * 50)
        
        for deck in today_review.decks:
            print(f"\n{deck.deck_name}:")
            
            if deck.new_cards:
                print("  New cards:")
                for q in deck.new_cards:
                    print(f"    - {q}")
            
            if deck.learning_cards:
                print("  Learning cards:")
                for q in deck.learning_cards:
                    print(f"    - {q}")
            
            if deck.review_cards:
                print("  Review cards:")
                for q in deck.review_cards:
                    print(f"    - {q}")
            
            print(f"  Total in deck: {deck.total_cards}")
        
        print("\n" + "-" * 50)
        print(f"Total cards to review: {today_review.total_cards}")

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