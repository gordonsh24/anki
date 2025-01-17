from ..domain.presenter import ReviewPresenter

class ConsolePresenter(ReviewPresenter):
    """Console-based implementation of ReviewPresenter."""
    
    def show_no_cards(self) -> None:
        print("\nNo cards to review today!")
    
    def show_deck_list(self, deck_names: list[str]) -> None:
        print("\nDecks found:", deck_names)
        print("\nCards due today by deck:")
        print("-" * 50)
    
    def show_deck_cards(self, deck_name: str, new_cards: list[str], 
                       learning_cards: list[str], review_cards: list[str], 
                       total: int) -> None:
        print(f"\n{deck_name}:")
        
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
        
        print(f"  Total in deck: {total}")
    
    def show_total_cards(self, total: int) -> None:
        print("\n" + "-" * 50)
        print(f"Total cards to review: {total}")
    
    def show_connection_error(self) -> None:
        print("Error: Could not connect to Anki.")
        print("Please make sure that:")
        print("1. Anki is running")
        print("2. AnkiConnect add-on is installed")
        print("3. No firewall is blocking the connection")
    
    def show_connection_success(self, version: str) -> None:
        print(f"Connected to AnkiConnect v{version}") 