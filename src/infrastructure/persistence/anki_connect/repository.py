"""Repository implementation for AnkiConnect."""

from typing import List

from src.core.ports import CardRepository
from src.core.entities import DeckCards, TodayReview
from src.infrastructure.anki_connect.client import AnkiConnectClient
from .mapper import AnkiCardMapper


class AnkiConnectCardRepository(CardRepository):
    """Repository for retrieving cards from Anki using AnkiConnect."""

    def __init__(self, client: AnkiConnectClient, mapper: AnkiCardMapper) -> None:
        """Initialize the repository.

        Args:
            client: The AnkiConnect client to use.
            mapper: The mapper to use for converting Anki data to domain entities.
        """
        self._client = client
        self._mapper = mapper

    def get_today_review(self) -> TodayReview:
        """Get today's review information.

        Returns:
            A TodayReview object containing information about cards to review.
        """
        deck_names = self._client.get_deck_names()
        decks = []

        for deck_name in deck_names:
            cards = self._client.find_cards(f"deck:{deck_name}")
            if not cards:
                continue

            cards_info = self._client.get_cards_info(cards)
            if not cards_info:
                continue

            deck = self._mapper.to_deck_cards(deck_name, cards_info)
            if deck.total_cards > 0:
                decks.append(deck)

        return TodayReview(decks) 