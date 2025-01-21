"""Mapper for converting AnkiConnect data to domain entities."""

from typing import List, Dict, Any

from src.core.entities import DeckCards


class AnkiCardMapper:
    """Maps AnkiConnect data to domain entities."""

    def to_deck_cards(self, deck_name: str, cards: List[Dict[str, Any]]) -> DeckCards:
        """Convert AnkiConnect card data to a DeckCards entity.

        Args:
            deck_name: The name of the deck.
            cards: List of card data from AnkiConnect.

        Returns:
            A DeckCards entity containing the card information.
        """
        new_cards = []
        learning_cards = []
        review_cards = []

        for card in cards:
            card_type = self._get_card_type(card)
            question = self._get_first_field_value(card)

            if card_type == "new":
                new_cards.append(question)
            elif card_type == "learning":
                learning_cards.append(question)
            elif card_type == "review":
                review_cards.append(question)

        return DeckCards(
            deck_name=deck_name,
            new_cards=new_cards,
            learning_cards=learning_cards,
            review_cards=review_cards
        )

    @staticmethod
    def _get_card_type(card: Dict[str, Any]) -> str:
        """Determine the type of card based on its queue and type fields.

        Args:
            card: Card data from AnkiConnect.

        Returns:
            The type of card as a string: "new", "learning", or "review".
        """
        queue = card.get("queue", -1)
        card_type = card.get("type", 0)

        if queue == 0 or card_type == 0:
            return "new"
        elif queue in (1, 3) or card_type == 1:
            return "learning"
        else:
            return "review"

    @staticmethod
    def _get_first_field_value(card: Dict[str, Any]) -> str:
        """Get the value of the first field from a card.

        Args:
            card: Card data from AnkiConnect.

        Returns:
            The value of the first field as a string.
        """
        fields = card.get("fields", {})
        if not fields:
            return ""

        first_field = next(iter(fields.values()), {})
        return first_field.get("value", "") 