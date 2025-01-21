"""Mapper for converting AnkiConnect responses to domain entities."""

from typing import Dict, Any, List

from src.core.entities import DeckCards, TodayReview


class AnkiCardMapper:
    """Mapper for converting AnkiConnect card data to domain entities."""

    @staticmethod
    def get_card_question(card: Dict[str, Any]) -> str:
        """Extract the question text from a card.
        
        Args:
            card: Card data from AnkiConnect
            
        Returns:
            Question text from the first field
        """
        fields = card.get('fields', {})
        return next(iter(fields.values()), {}).get('value', 'Unknown Card')

    @staticmethod
    def determine_card_type(card: Dict[str, Any]) -> str:
        """Determine the type of a card based on its queue and type.
        
        Args:
            card: Card data from AnkiConnect
            
        Returns:
            One of: 'new', 'learning', 'review'
        """
        queue = card.get('queue', 0)
        
        if queue == 0 or queue == -1:  # New card
            return 'new'
        elif queue in [1, 3]:  # Learning/Relearning
            return 'learning'
        elif queue == 2:  # Review
            return 'review'
        return 'unknown'

    @classmethod
    def to_deck_cards(cls, cards_info: List[Dict[str, Any]]) -> List[DeckCards]:
        """Convert a list of card info to DeckCards entities.
        
        Args:
            cards_info: List of card data from AnkiConnect
            
        Returns:
            List of DeckCards entities
        """
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

            question = cls.get_card_question(card)
            card_type = cls.determine_card_type(card)
            deck_cards[deck_name][card_type].append(question)

        # Create DeckCards objects
        return [
            DeckCards(
                deck_name=deck_name,
                new_cards=cards['new'],
                learning_cards=cards['learning'],
                review_cards=cards['review']
            )
            for deck_name, cards in deck_cards.items()
        ]

    @classmethod
    def to_today_review(cls, cards_info: List[Dict[str, Any]]) -> TodayReview:
        """Convert a list of card info to a TodayReview entity.
        
        Args:
            cards_info: List of card data from AnkiConnect
            
        Returns:
            TodayReview entity
        """
        deck_cards = cls.to_deck_cards(cards_info)
        return TodayReview(deck_cards) 