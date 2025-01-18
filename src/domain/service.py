from typing import Dict, Any
from .query import Query
from ..core.entities import DeckCards, TodayReview

class AnkiTodayService:
    def __init__(self, query: Query):
        self.query = query

    @staticmethod
    def get_first_field_value(card: Dict[str, Any]) -> str:
        """Get the value of the first field in the card, regardless of its name."""
        if not card.get('fields'):
            return "Empty card"
        # Get the first field's value
        first_field = next(iter(card['fields'].values()))
        return first_field['value']

    @staticmethod
    def get_card_type(card: Dict[str, Any]) -> int:
        """Get the card type based on queue and type fields."""
        queue = card.get('queue', -1)
        card_type = card.get('type', -1)
        
        # New card
        if queue == 0 or card_type == 0:
            return 0
        # Learning card
        elif queue == 1 or card_type == 1:
            return 1
        # Review card
        elif queue == 2 or card_type == 2:
            return 2
        return -1  # Unknown type

    def get_cards(self) -> TodayReview:
        """Get all cards that need to be reviewed today, grouped by deck."""
        decks = self.query.get_deck_names()
        if decks is None:
            return TodayReview(decks=[])

        deck_cards = []
        for deck in decks:
            # Find cards due today in this deck
            card_ids = self.query.find_cards_due_today(deck)
            if not card_ids:
                continue

            cards_info = self.query.get_card_info(card_ids)
            if not cards_info:
                continue

            # Group cards by type
            new_cards = []
            review_cards = []
            learning_cards = []

            for card in cards_info:
                question = self.get_first_field_value(card)
                card_type = self.get_card_type(card)
                
                if card_type == 0:  # New card
                    new_cards.append(question)
                elif card_type == 1:  # Learning card
                    learning_cards.append(question)
                elif card_type == 2:  # Review card
                    review_cards.append(question)

            if new_cards or learning_cards or review_cards:
                deck_cards.append(DeckCards(
                    deck_name=deck,
                    new_cards=new_cards,
                    learning_cards=learning_cards,
                    review_cards=review_cards
                ))

        return TodayReview(decks=deck_cards) 