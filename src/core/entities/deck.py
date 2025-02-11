"""
Deck entity representing a collection of cards.
"""

from dataclasses import dataclass
from typing import List
from .card import Card

@dataclass
class DeckCards:
    """Represents a deck and its cards due for review."""
    deck_name: str
    new_cards: List[Card]
    learning_cards: List[Card]
    review_cards: List[Card]

    @property
    def total_cards(self) -> int:
        """Get the total number of cards in the deck."""
        return len(self.new_cards) + len(self.learning_cards) + len(self.review_cards) 