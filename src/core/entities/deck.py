"""
Deck entity representing a collection of cards.
"""

from dataclasses import dataclass
from typing import List

@dataclass
class DeckCards:
    """Represents a deck and its cards due for review."""
    deck_name: str
    new_cards: List[str]
    learning_cards: List[str]
    review_cards: List[str]

    @property
    def total_cards(self) -> int:
        """Get the total number of cards in the deck."""
        return len(self.new_cards) + len(self.learning_cards) + len(self.review_cards) 