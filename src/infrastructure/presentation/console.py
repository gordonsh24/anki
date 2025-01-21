"""Console presenter implementation for displaying review information."""

from src.core.ports import ReviewPresenter
from src.core.entities import TodayReview


class ConsolePresenter(ReviewPresenter):
    """Presents review information in the console."""

    def present(self, review: TodayReview) -> None:
        """Present the review information in the console.

        Args:
            review: The review information to present.
        """
        if not review.decks:
            print("\nNo cards to review today!")
            return

        print(f"\nTotal cards to review today: {review.total_cards}")
        for deck in review.decks:
            print(f"{deck.deck_name}:")
            if deck.new_cards:
                print(f"  New cards ({len(deck.new_cards)}):")
                for card in deck.new_cards:
                    print(f"    - {card}")
            if deck.learning_cards:
                print(f"  Learning cards ({len(deck.learning_cards)}):")
                for card in deck.learning_cards:
                    print(f"    - {card}")
            if deck.review_cards:
                print(f"  Review cards ({len(deck.review_cards)}):")
                for card in deck.review_cards:
                    print(f"    - {card}") 