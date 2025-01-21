"""Repository implementation using AnkiConnect."""

from typing import List

from src.core.ports import CardRepository
from src.core.entities import DeckCards, TodayReview
from .client import AnkiConnectClient
from .mapper import AnkiCardMapper


class AnkiConnectCardRepository(CardRepository):
    """Repository for retrieving cards from Anki using AnkiConnect."""

    def __init__(self, client: AnkiConnectClient, mapper: AnkiCardMapper):
        """Initialize the repository.
        
        Args:
            client: AnkiConnect client for making requests
            mapper: Mapper for converting AnkiConnect data to domain entities
        """
        self._client = client
        self._mapper = mapper

    def get_today_review(self) -> TodayReview:
        """Get today's review cards.
        
        Returns:
            TodayReview containing the decks and their cards
        """
        deck_names = self._client.get_deck_names()
        decks = []

        for deck_name in deck_names:
            query = f"deck:{deck_name}"
            card_ids = self._client.find_cards(query)
            
            if not card_ids:
                continue
                
            cards = self._client.get_cards_info(card_ids)
            if not cards:
                continue
                
            deck_cards = self._mapper.to_deck_cards(deck_name, cards)
            if deck_cards.total_cards > 0:
                decks.append(deck_cards)

        return TodayReview(decks) 