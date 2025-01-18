from typing import Dict, Any
from ..domain.presenter import ReviewPresenter
from ..core.entities import TodayReview

class ConsolePresenter(ReviewPresenter):
    """Console implementation of the review presenter."""

    def present(self, review: TodayReview) -> Dict[str, Any]:
        """Present the review data in a format suitable for console display."""
        if not review.decks:
            return {
                "total_cards": 0,
                "message": "No cards to review today!"
            }

        deck_messages = []
        for deck in review.decks:
            deck_message = f"\n{deck.deck_name}:"
            if deck.new_cards:
                deck_message += f"\n  New cards ({len(deck.new_cards)}):"
                for card in deck.new_cards:
                    deck_message += f"\n    - {card}"
            if deck.learning_cards:
                deck_message += f"\n  Learning cards ({len(deck.learning_cards)}):"
                for card in deck.learning_cards:
                    deck_message += f"\n    - {card}"
            if deck.review_cards:
                deck_message += f"\n  Review cards ({len(deck.review_cards)}):"
                for card in deck.review_cards:
                    deck_message += f"\n    - {card}"
            deck_messages.append(deck_message)

        return {
            "total_cards": review.total_cards,
            "message": "\n".join(deck_messages)
        } 