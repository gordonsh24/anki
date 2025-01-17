from dataclasses import dataclass
from typing import List

@dataclass
class DeckCards:
    """Represents cards grouped by their type in a deck."""
    deck_name: str
    new_cards: List[str]
    learning_cards: List[str]
    review_cards: List[str]

    @property
    def total_cards(self) -> int:
        return len(self.new_cards) + len(self.learning_cards) + len(self.review_cards)

@dataclass
class TodayReview:
    """Represents all cards to review today across all decks."""
    decks: List[DeckCards]

    @property
    def total_cards(self) -> int:
        return sum(deck.total_cards for deck in self.decks) 