"""Repository implementation for accessing Anki data via AnkiConnect."""

from typing import List, Dict, Any
from ....core.ports.repositories import CardRepository
from ....core.entities import TodayReview
from .client import AnkiConnectClient
from .mapper import AnkiCardMapper


class AnkiConnectCardRepository(CardRepository):
    """Repository for accessing card data via AnkiConnect."""

    def __init__(self, client: AnkiConnectClient):
        """Initialize the repository.
        
        Args:
            client: AnkiConnect client for making API calls
        """
        self._client = client
        self._mapper = AnkiCardMapper()

    def get_today_review(self) -> TodayReview:
        """Get today's review cards.
        
        Returns:
            TodayReview entity containing cards grouped by deck
            
        Raises:
            RuntimeError: If there's an error communicating with Anki
        """
        # Get all deck names
        decks = self._client.get_deck_names()
        if not decks:
            return TodayReview([])

        # Get card IDs for each deck
        card_ids = []
        for deck in decks:
            deck_cards = self._client.find_cards(f'deck:"{deck}"')
            if deck_cards:
                card_ids.extend(deck_cards)

        if not card_ids:
            return TodayReview([])

        # Get card info
        cards_info = self._client.get_cards_info(card_ids)
        if not cards_info:
            return TodayReview([])

        # Convert to domain entity
        return self._mapper.to_today_review(cards_info) 