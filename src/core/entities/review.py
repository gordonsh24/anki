"""
Review entity representing a collection of decks for today's review.
"""

from dataclasses import dataclass
from typing import List
from .deck import DeckCards

@dataclass
class TodayReview:
    """Represents all cards that need to be reviewed today."""
    decks: List[DeckCards]

    @property
    def total_cards(self) -> int:
        """Get the total number of cards across all decks."""
        return sum(deck.total_cards for deck in self.decks) 