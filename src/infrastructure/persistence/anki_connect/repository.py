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
        all_deck_names = self._client.get_deck_names()
        main_deck_names = self._filter_main_decks(all_deck_names)
        decks = []

        for deck_name in main_deck_names:
            # Only get cards from the main deck that are due today
            query = f'deck:"{deck_name}" is:due'  # Exact match for deck name and due today
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

    @staticmethod
    def _filter_main_decks(deck_names: List[str]) -> List[str]:
        """Filter out sub-decks and return only main deck names.
        
        Args:
            deck_names: List of all deck names including sub-decks
            
        Returns:
            List of main deck names
        """
        main_decks = set()
        
        for deck_name in deck_names:
            # Get the top-level deck name (before first ::)
            main_deck = deck_name.split("::")[0]
            main_decks.add(main_deck)
            
        return sorted(main_decks) 