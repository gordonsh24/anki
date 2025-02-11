"""Mapper for converting AnkiConnect data to domain entities."""

import time
from datetime import datetime, timezone
from typing import List, Dict, Any

from src.core.entities import DeckCards, Card


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
            if not card_type:  # Skip cards that aren't due today
                continue
                
            front = self._get_first_field_value(card)
            card_entity = Card(front=front)

            if card_type == "new":
                new_cards.append(card_entity)
            elif card_type == "learning":
                learning_cards.append(card_entity)
            elif card_type == "review":
                review_cards.append(card_entity)

        return DeckCards(
            deck_name=deck_name,
            new_cards=new_cards,
            learning_cards=learning_cards,
            review_cards=review_cards
        )

    @staticmethod
    def _get_card_type(card: Dict[str, Any]) -> str | None:
        """Determine the type of card based on its queue and type fields.
        Only returns a type for cards that are due today or in learning.

        Args:
            card: Card data from AnkiConnect.

        Returns:
            The type of card as a string: "new", "learning", or "review", or None if not due today.
        """
        queue = card.get("queue", -1)
        card_type = card.get("type", 0)
        due = card.get("due", 0)
        odue = card.get("odue", 0)  # Original due date

        # Learning cards (queue=1 or queue=3 for learning cards in review)
        # For learning cards, due is a Unix timestamp in milliseconds
        if queue in (1, 3):
            current_timestamp = int(time.time() * 1000)  # Current timestamp in milliseconds
            # Only show learning cards that are due now or in the past
            if due <= current_timestamp:
                return "learning"
            return None
            
        # New cards due today (queue=0)
        if queue == 0:
            return "new"
            
        # Review cards due today (queue=2)
        # For review cards, the due field is the day number when the card is due
        # relative to the collection creation date
        if queue == 2:
            # Get today's day number from Anki's perspective
            # This is the number of days since the Unix epoch
            today = int(time.time() / (24 * 60 * 60))
            # Use odue if it's set (for filtered/rescheduled cards), otherwise use due
            target_due = odue if odue > 0 else due
            if target_due <= today:
                return "review"
            
        return None

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