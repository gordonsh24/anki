"""AnkiConnect-based implementation of the card repository."""

from typing import List, Dict, Any
from ....core.ports import CardRepository
from ....core.entities import DeckCards, TodayReview
from .query import AnkiConnectQuery


class AnkiConnectCardRepository(CardRepository):
    """Repository implementation using AnkiConnect for accessing cards."""

    def __init__(self, query: AnkiConnectQuery):
        """Initialize repository with AnkiConnect query.
        
        Args:
            query: AnkiConnect query for making requests
        """
        self._query = query

    def get_decks(self) -> List[str]:
        """Get all available deck names.
        
        Returns:
            List of deck names.
            
        Raises:
            RuntimeError: If the query fails
        """
        decks = self._query.get_deck_names()
        if decks is None:
            raise RuntimeError("Failed to get deck names from Anki")
        return decks

    def get_due_cards(self) -> TodayReview:
        """Get all cards that are due for review today.
        
        Returns:
            TodayReview object containing all cards due for review.
            
        Raises:
            RuntimeError: If any of the queries fail
        """
        # Get all cards due today
        card_ids = self._query.find_cards_due_today()
        if card_ids is None:
            raise RuntimeError("Failed to find due cards")

        # If no cards are due, return empty review
        if not card_ids:
            return TodayReview([])

        # Get detailed information about the cards
        cards_info = self._query.get_card_info(card_ids)
        if cards_info is None:
            raise RuntimeError("Failed to get card information")

        # Group cards by deck
        deck_cards: Dict[str, Dict[str, List[str]]] = {}
        for card in cards_info:
            deck_name = card.get('deckName', 'Unknown Deck')
            if deck_name not in deck_cards:
                deck_cards[deck_name] = {
                    'new': [],
                    'learning': [],
                    'review': []
                }

            # Get the first field as the card's question
            fields = card.get('fields', {})
            question = next(iter(fields.values()), {}).get('value', 'Unknown Card')

            # Determine card type based on queue and type
            queue = card.get('queue', 0)
            card_type = card.get('type', 0)

            if queue == 0 or queue == -1:  # New card
                deck_cards[deck_name]['new'].append(question)
            elif queue in [1, 3]:  # Learning/Relearning
                deck_cards[deck_name]['learning'].append(question)
            elif queue == 2:  # Review
                deck_cards[deck_name]['review'].append(question)

        # Create DeckCards objects for each deck
        decks = []
        for deck_name, cards in deck_cards.items():
            deck = DeckCards(
                deck_name=deck_name,
                new_cards=cards['new'],
                learning_cards=cards['learning'],
                review_cards=cards['review']
            )
            decks.append(deck)

        return TodayReview(decks) 